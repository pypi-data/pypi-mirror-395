import contextvars
from datetime import UTC, datetime
from functools import partial, wraps
from typing import Any, Callable, List, Union

from dateutil.parser import parse
from flask.app import Flask
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace import Status, StatusCode

from insightconnect_plugin_runtime.plugin import Plugin
from insightconnect_plugin_runtime.util import (
    OTEL_ENDPOINT,
    is_running_in_cloud,
    parse_from_string,
)


def init_tracing(app: Flask, plugin: Plugin, endpoint: str) -> None:
    """
    Initialize OpenTelemetry Tracing

    The function sets up the tracer provider, span processor and exporter with auto-instrumentation

    :param app: The Flask Application
    :param plugin: The plugin to derive the service name from
    :param endpoint: The Otel Endpoint to emit traces to
    """

    if not is_running_in_cloud():
        return

    resource = Resource(
        attributes={
            "service.name": f'pif.{plugin.name.lower().replace(" ", "_")}',
            "service.version": plugin.version,
        })

    trace_provider = TracerProvider(resource=resource)
    exporter = OTLPSpanExporter(endpoint=endpoint)
    trace_provider.add_span_processor(BatchSpanProcessor(exporter))
    trace.set_tracer_provider(trace_provider)

    FlaskInstrumentor().instrument_app(app)

    def requests_callback(span: trace.Span, _: Any, response: Any) -> None:
        if hasattr(response, "status_code"):
            span.set_status(Status(StatusCode.OK if response.status_code < 400 else StatusCode.ERROR))

    RequestsInstrumentor().instrument(trace_provider=trace_provider, response_hook=requests_callback)


def auto_instrument(func: Callable) -> Callable:
    """
    Decorator that auto-instruments a function with a trace

    :param func: function to instrument
    :return:
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        tracer = trace.get_tracer(__name__)
        with tracer.start_as_current_span(func.__name__):
            return func(*args, **kwargs)

    return wrapper


def create_post_fork(app_getter: Callable, plugin_getter: Callable, config_getter: Callable) -> Callable:
    def post_fork(server, worker):
        app = app_getter()
        plugin = plugin_getter()
        endpoint = config_getter().get(OTEL_ENDPOINT, None)
        if endpoint:
            init_tracing(app, plugin, endpoint)

    return post_fork


def with_context(context: contextvars.Context, function: Callable) -> Callable:
    """
    Creates a wrapper function that executes the target function with the specified context.

    :param context: The Context object to apply when executing the function
    :type context: contextvars.Context

    :param function: The function to wrap with the specified context
    :type function: Callable

    :return: A wrapper function that applies the context when called
    :rtype: Callable
    """

    def _wrapper(context_: contextvars.Context, function_: Callable, *args, **kwargs):
        return context_.copy().run(function_, *args, **kwargs)

    return partial(_wrapper, context, function)


def monitor_task_delay(
    timestamp_keys: Union[str, List[str]], default_delay_threshold: str = "2d"
) -> Callable:
    """Monitor timestamp fields in task state to detect processing delays.

    This decorator checks if specified timestamp fields in a task's state have fallen
    behind a configurable threshold, indicating the task is processing data with a lag.
    When timestamps fall behind the threshold, an error is logged.

    The threshold can be overridden at runtime by setting the "task_delay_threshold" key
    in the task's custom_config.

    :param timestamp_keys: One or more state keys containing timestamps to monitor
    :type timestamp_keys: Union[str, List[str]]

    :param default_delay_threshold: Time duration string representing maximum acceptable lag (e.g. "2d" for 2 days).
    :type default_delay_threshold: str

    :return: Decorator function that wraps the original task function
    :rtype: Callable
    """

    # Check if time_fields is a string and convert it to a list
    if isinstance(timestamp_keys, str):
        timestamp_keys = [timestamp_keys]

    def _decorator(function_: Callable):
        @wraps(function_)
        def _wrapper(self, *args, **kwargs):
            # Unpack response tuple from task `def run()` method
            output, state, has_more_pages, status_code, error_object = function_(
                self, *args, **kwargs
            )

            # Try-except with pass to make sure any exception won't stop the task from running
            try:
                # Check if any time fields are in the past
                threshold = kwargs.get("custom_config", {}).get(
                    "task_delay_threshold", default_delay_threshold
                )

                # Calculate the delayed time based on the threshold
                delay_threshold_time = (
                    datetime.now(UTC) - parse_from_string(threshold)
                ).replace(tzinfo=None)

                # Loop over the state time fields and check if they are below the set threshold
                for state_time in timestamp_keys:
                    # Check if the state time exists in the state dictionary
                    if not (current_state_time := state.get(state_time)):
                        continue

                    # Parse and normalize the state time value
                    try:
                        # First, try to parse the epoch timestamp in seconds
                        try:
                            normalized_state_time = datetime.fromtimestamp(
                                float(current_state_time)
                            )
                        except ValueError:
                            # If it fails, assume it's in milliseconds and convert accordingly
                            normalized_state_time = datetime.fromtimestamp(
                                float(current_state_time) / 1000.0
                            )
                    except (ValueError, TypeError):
                        # If parsing fails, parse as a string
                        normalized_state_time = parse(str(current_state_time))

                    # Normalize the state time to UTC and remove timezone info
                    normalized_state_time = normalized_state_time.astimezone(
                        UTC
                    ).replace(tzinfo=None)

                    # If the normalized state time is below the threshold, log an error message
                    if normalized_state_time < delay_threshold_time:
                        # Log an error message that indicates the integration state time is below the threshold
                        self.logger.error(
                            f"ERROR: THE INTEGRATION IS FALLING BEHIND",
                            field=state_time,
                            current_value=current_state_time,
                            normalized_time=normalized_state_time,
                            threshold_time=delay_threshold_time,
                            configured_threshold=threshold,
                            has_more_pages=has_more_pages,
                        )
                        break
            except Exception as error:
                self.logger.error(
                    f"An exception occurred while checking task delay. The exception was: {error}"
                )

            # Return task output
            return output, state, has_more_pages, status_code, error_object

        return _wrapper

    return _decorator
