# -*- coding: utf-8 -*-
import copy
import inspect
import io
import json
import logging

import jsonschema
import structlog

from insightconnect_plugin_runtime.connection import ConnectionCache
from insightconnect_plugin_runtime.dispatcher import Stdout, Http
from insightconnect_plugin_runtime.exceptions import (
    ClientException,
    ServerException,
    LoggedException,
    ConnectionTestException,
    PluginException,
)
from insightconnect_plugin_runtime.metrics import MetricsBuilder
from insightconnect_plugin_runtime.util import (
    is_running_in_cloud,
    flush_logging_handlers,
)

logger = structlog.get_logger("plugin")

message_output_type = {
    "action_start": "action_event",
    "trigger_start": "trigger_event",
    "task_start": "task_event",
    "connection_test": "connection_test",
}


class Workflow(object):
    def __init__(
        self,
        shortOrgId=None,
        orgProductToken=None,
        uiHostUrl=None,
        jobId=None,
        stepId=None,
        versionId=None,
        nextStepId=None,
        nextEdgeId=None,
        triggerId=None,
        jobExecutionContextId=None,
        time=None,
        connectionTestId=None,
        connectionTestTimeout=None,
        workflowId=None,
    ):
        """
        Worflow object for the Meta Class
        :param shortOrgId: Short version of the Organization ID
        :param orgProductToken: Organization Product Token
        :param uiHostUrl: Job URL for triggers
        :param jobId: Job UUID
        :param stepId: Step UUID
        :param versionId:  Workflow Version UUID
        :param nextStepId: Next Step UUID
        :param nextEdgeId: Next Edge UUID
        :param triggerId: Trigger UUID
        :param jobExecutionContextId: Job Execution Context UUID
        :param time: Time the action or trigger was executed
        :param connectionTestId: Connection Test ID
        :param connectionTestTimeout: Connection Test Timeout
        :param workflowId: Workflow ID
        """
        self.shortOrgId = shortOrgId
        self.orgProductToken = orgProductToken
        self.uiHostUrl = uiHostUrl
        self.jobId = jobId
        self.stepId = stepId
        self.versionId = versionId
        self.nextStepId = nextStepId
        self.nextEdgeId = nextEdgeId
        self.triggerId = triggerId
        self.jobExecutionContextId = jobExecutionContextId
        self.time = time
        self.connectionTestId = connectionTestId
        self.connectionTestTimeout = connectionTestTimeout
        self.workflowId = workflowId

    @classmethod
    def from_komand(cls, input_message):
        """Creates a Workflow object from Komand"""
        return cls(
            workflowId=input_message.get("workflow_uid", None),
            stepId=input_message.get("step_uid", None),
            versionId=input_message.get("workflow_version_uid", None),
        )

    @classmethod
    def from_insight_connect(cls, input_message):
        """Creates a Workflow object from Insight Connect"""
        return cls(
            shortOrgId=input_message.get("shortOrgId", None),
            orgProductToken=input_message.get("orgProductToken", None),
            uiHostUrl=input_message.get("uiHostUrl", None),
            jobId=input_message.get("jobId", None),
            stepId=input_message.get("stepId", None),
            versionId=input_message.get("versionId", None),
            nextStepId=input_message.get("nextStepId", None),
            nextEdgeId=input_message.get("nextEdgeId", None),
            triggerId=input_message.get("triggerId", None),
            jobExecutionContextId=input_message.get("jobExecutionContextId", None),
            time=input_message.get("time", None),
            connectionTestId=input_message.get("connectionTestId", None),
            connectionTestTimeout=input_message.get("connectionTestTimeout", None),
        )


class Meta(object):
    """Meta properties for a plugin"""

    def __init__(self, name="", vendor="", description="", version="", workflow=None):
        self.name, self.vendor, self.description, self.version, self.workflow = (
            name,
            vendor,
            description,
            version,
            workflow,
        )

    def set_workflow(self, input_message):
        """
        Sets the workflow attribute within the Meta class
        :param input_message:
        :return:
        """
        if input_message.get("workflow_uid"):
            self.workflow = Workflow.from_komand(input_message)
        else:
            self.workflow = Workflow.from_insight_connect(input_message)


class Plugin(object):
    """A Komand Plugin."""

    def __init__(
        self,
        name="",
        vendor="",
        description="",
        version="",
        connection=None,
        custom_encoder=None,
        custom_decoder=None,
    ):
        self.name = name
        self.vendor = vendor
        self.description = description
        self.version = version
        self.connection = connection

        self.connection.meta = Meta(
            name=name, vendor=vendor, description=description, version=version
        )

        self.connection_cache = ConnectionCache(connection)
        self.triggers = {}
        self.actions = {}
        self.tasks = {}
        self.debug = False
        self.custom_decoder = custom_decoder
        self.custom_encoder = custom_encoder

    def add_trigger(self, trigger):
        """add a new trigger"""
        self.triggers[trigger.name] = trigger

    def add_action(self, action):
        """add a new action"""
        self.actions[action.name] = action

    def add_task(self, task):
        """add a new task"""
        self.tasks[task.name] = task

    def envelope(
        self,
        message_type,
        input_message,
        log,
        success,
        output,
        error_message,
        state,
        has_more_pages,
        status_code,
        error_object,
        ex: None,
        is_test: False,
    ):
        """
        Creates an output message of a step's execution.

        :param message_type: The message type
        :param input_message: The input message
        :param log: The log of the step, as a single string
        :param success: whether or not the step was successful
        :param output: The step data output
        :param error_message: An error message if an error was thrown
        :param state: The state of task_event. Only applicable to tasks.
        :param has_more_pages: Whether or not a task_event has more pages to be consumed. Only applicable to tasks.
        :param status_code: Contains the status code of requests. Only applicable to tasks.
        :param error_object: Contains the error object if any error occurs. Only applicable to tasks.
        :param ex: An error that was thrown
        :param is_test: whether or not the step is part of a Connection Test
        :return: An output message
        """

        output_message = {
            "log": log,
            "status": "ok" if success else "error",
            "meta": input_message["body"].get("meta", None),
        }

        if state is not None:
            output_message["state"] = state

        if has_more_pages is not None:
            output_message["has_more_pages"] = has_more_pages

        if status_code is not None:
            output_message["status_code"] = status_code

        if error_object is not None and isinstance(
            error_object, (ConnectionTestException, PluginException)
        ):
            output_message["exception"] = {
                "cause": error_object.cause,
                "assistance": error_object.assistance,
                "data": error_object.data,
            }

        if success:
            output_message["output"] = output
        else:
            output_message["error"] = error_message

            if ex:
                if isinstance(ex, ConnectionTestException):
                    error_data = ex.data if ex.data else None
                    info_log = f"cause={ex.cause}, assistance={ex.assistance}, data={error_data}"
                    logger.error(f"Plugin exception raised. {info_log}")
                    output_message["exception"] = {
                        "cause": ex.cause,
                        "assistance": ex.assistance,
                        "data": ex.data,
                    }

                if is_test and not isinstance(ex, ConnectionTestException):
                    output_message["exception"] = {
                        "cause": "Plugin connection test failed.",
                        "assistance": "See error log for more details.",
                        "data": ex.__repr__(),
                    }

                # Build the metrics blob to attach to the output payload
                # Only supported in cloud environments right now
                if is_running_in_cloud():
                    metrics_builder = MetricsBuilder(
                        plugin_name=self.name,
                        plugin_version=self.version,
                        plugin_vendor=self.vendor,
                        input_message=input_message,
                        exception_=ex,
                        workflow_id=self.connection.meta.workflow.workflowId,
                        org_id=self.connection.meta.workflow.shortOrgId,
                    )
                    output_message["metrics"] = metrics_builder.build()

        return {"body": output_message, "version": "v1", "type": message_type}

    def marshal(self, msg, fd):
        """Marshal a message to fd."""

        if self.custom_encoder is None:
            json.dump(msg, fd)
        else:
            json.dump(msg, fd, cls=self.custom_encoder)
        fd.flush()

    def unmarshal(self, fd):
        """Unmarshal a message."""

        if self.custom_decoder is None:
            msg = json.load(fd)
        else:
            msg = json.load(fd, cls=self.custom_decoder)
        return msg

    @staticmethod
    def validate_json(json_object, schema):
        try:
            jsonschema.validate(json_object, schema)
        except jsonschema.exceptions.ValidationError as e:
            raise ClientException("input JSON was invalid", e)
        except Exception as e:
            raise Exception("Unable to validate input JSON", e)

    @staticmethod
    def validate_input_message(input_message):
        if input_message is None:
            raise ClientException("Input message was None")
        if not isinstance(input_message, dict):
            raise ClientException("Input message is not a dictionary")
        if "type" not in input_message:
            raise ClientException('"type" missing from input message')
        if "version" not in input_message:
            raise ClientException('"version" missing from input message')
        if "body" not in input_message:
            raise ClientException('"body" missing from input message')

        version = input_message["version"]
        type_ = input_message["type"]
        body = input_message["body"]

        if version != "v1":
            raise ClientException(
                f"Unsupported version '{version}'. Only v1 is supported"
            )
        if type_ == "action_start":
            if "action" not in body:
                raise ClientException(
                    'Message is action_start but field "action" is missing from body'
                )
            if not isinstance(body["action"], str):
                raise ClientException("Action field must be a string")
        elif type_ == "trigger_start":
            if "trigger" not in body:
                raise ClientException(
                    'Message is trigger_start but field "trigger" is missing from body'
                )
            if not isinstance(body["trigger"], str):
                raise ClientException("Trigger field must be a string")
        elif type_ == "task_start":
            if "task" not in body:
                raise ClientException(
                    'Message is task_start but field "task" is missing from body'
                )
            if not isinstance(body["task"], str):
                raise ClientException("Task field must be a string")
        elif type_ == "connection_test":
            pass
        else:
            raise ClientException(
                "Unsupported message type %s. Must be action_start, trigger_start, connection_test, or task_start"
            )

        if "meta" not in body:
            body["meta"] = {}

        # This is existing behavior.
        if "connection" not in body:
            body["connection"] = {}
        if "dispatcher" not in body:
            body["dispatcher"] = {}
        if "input" not in body:
            body["input"] = {}

    def handle_step(self, input_message, is_test=False, is_debug=False, connection_test_type="test"):
        """
        Executes a single step, given the input message dictionary.

        Execution of this method is designed to be thread safe.

        :param input_message: The input message
        :param is_test: Whether or not this is
        :param is_debug:
        :return:
        """
        input_message_meta = input_message["body"].get("meta", {})

        if input_message_meta is None:
            input_message_meta = {}
        self.connection.meta.set_workflow(input_message_meta)

        # Add StreamHandler to record plugin action/trigger/task logs for output back to consumer
        # log_stream will record logs via StreamHandler and be included in the plugin output
        log_stream = io.StringIO()
        stream_handler = logging.StreamHandler(log_stream)
        stream_handler.setLevel(logging.DEBUG if is_debug else logging.INFO)

        # Getting logger instances, struct_logger is formatted and mainly used in actions, triggers, and tasks
        # while plugin_logger is the same instance that is used to add/remove and flush handlers during step execution
        struct_logger = structlog.get_logger("plugin")
        plugin_logger = logging.getLogger("plugin")
        plugin_logger.addHandler(stream_handler)

        success = True
        caught_exception = None
        output = None
        out_type = None

        # Properties specific to tasks
        state = None
        has_more_pages = None
        status_code = None
        error_object = None

        # Properties specific to tasks tests
        task_test_log = None

        try:
            # Attempt to grab message type first
            message_type = input_message.get("type")
            out_type = message_output_type.get(message_type)
            if message_type not in [
                "action_start",
                "trigger_start",
                "task_start",
                "connection_test",
            ]:
                raise ClientException(
                    'Unsupported message type "{}"'.format(message_type)
                )

            Plugin.validate_input_message(input_message)

            if message_type == "action_start":
                out_type = "action_event"
                output = self.start_step(
                    input_message["body"],
                    "action",
                    struct_logger,
                    log_stream,
                    is_test,
                    is_debug,
                    connection_test_type=connection_test_type
                )
            elif message_type == "trigger_start":
                out_type = "trigger_event"
                output = self.start_step(
                    input_message["body"],
                    "trigger",
                    struct_logger,
                    log_stream,
                    is_test,
                    is_debug,
                    connection_test_type=connection_test_type
                )
            elif message_type == "task_start":
                out_type = "task_event"
                if is_test:
                    # state will not be returned by task's test method
                    output, task_test_log = self.start_step(
                        input_message["body"],
                        "task",
                        struct_logger,
                        log_stream,
                        is_test,
                        is_debug,
                        connection_test_type=connection_test_type
                    )
                else:
                    (
                        output,
                        state,
                        has_more_pages,
                        status_code,
                        error_object,
                    ) = self.start_step(
                        input_message["body"],
                        "task",
                        struct_logger,
                        log_stream,
                        is_test,
                        is_debug,
                        connection_test_type=connection_test_type
                    )
            elif message_type == "connection_test":
                out_type = "connection_test"
                output, task_test_log = self.start_step(
                    input_message["body"],
                    "connection_test",
                    struct_logger,
                    log_stream,
                    is_test,
                    is_debug,
                    is_connection_test=True,
                    connection_test_type=connection_test_type
                )
        except (
            ClientException,
            ServerException,
            PluginException,
            ConnectionTestException,
            Exception,
        ) as error_message:
            success = False
            caught_exception = error_message
            struct_logger.exception(error_message)

            # now returning the value of data instead of the log buffer for connection task tests - SOAR-16566
            if isinstance(error_message, ConnectionTestException) and connection_test_type == "test_task":
                task_test_log = f"{error_message.data}" if error_message.data else "Connection test failed"
        finally:
            # if we are running a task connection test we want to return the pre-defined message
            # rather than a stack trace of logs - SOAR-16566
            log_message = task_test_log if task_test_log else log_stream.getvalue()
            output = self.envelope(
                out_type,
                input_message,
                log_message,
                success,
                output,
                str(caught_exception),
                state,
                has_more_pages,
                status_code,
                error_object,
                caught_exception,
                is_test,
            )

            # Flush all the handlers and remove the one that was previously created
            flush_logging_handlers(plugin_logger)
            plugin_logger.removeHandler(stream_handler)

            if not success:
                raise LoggedException(caught_exception, output)
            return output

    def start_step(
        self,
        message_body,
        step_key,
        logger,
        log_stream,
        is_test=False,
        is_debug=False,
        is_connection_test=False,
        connection_test_type="test"
    ):
        """
        Starts an action.
        :param message_body: The action_start message.
        :param step_key: The type of step to execute
        :param logger the logger for logging
        :param log_stream the raw stream for the log
        :param is_test: True if the action's test method should execute
        :param is_debug: True if debug is enabled
        :param is_connection_test: True if connection test is running
        :param connection_test_type: The type of connection test to be run
        :return: An action_event message
        """
        connection = self.connection_cache.get(message_body["connection"], logger)
        if is_connection_test:
            logger.info(
                "{vendor}/{plugin_name}:{plugin_version}".format(
                    vendor=connection.meta.vendor,
                    plugin_name=connection.meta.name,
                    plugin_version=connection.meta.version,
                )
            )

            # As the message type for both api/v1/connection/test and api/v1/connection/test_task calls are
            # message_type == "connection_test", this means that both the task and normal connection test code
            # hits this path and needs to have the same return structure, as a result we return None when
            # connection.test is called, as there is no message returned along side it,
            # and the code above then sees this and reads the "message" from the io buffer as normal
            if hasattr(connection, "test_task") and connection_test_type == "test_task":
                # Get the test_task function from the connection
                func = connection.test_task

                # Inspect the function to see if it requires args
                arguments = inspect.signature(func).parameters

                # If the function has parameters, we pass the task name
                if len(arguments) > 0 and "task" in message_body:
                    output, log = func(message_body["task"])
                else:
                    output, log = func()
                return output, log
            elif hasattr(connection, "test"):
                func = connection.test
                output = func()
                return output, None
            else:
                raise NotImplementedError(
                    "The server successfully processed the request and is not "
                    "returning any content (no connection test function)"
                )

        else:
            action_name = message_body[step_key]
            dictionary = getattr(self, step_key + "s")
            if action_name not in dictionary:
                raise ClientException('Unknown {} "{}"'.format(step_key, action_name))
            action = dictionary[action_name]

            # Copy the action for thread safety.
            # This is necessary because the object itself contains stateful fields like connection and debug.
            step = copy.copy(action)

            step.debug = is_debug
            step.connection = connection
            step.logger = logger

            # Extra setup for triggers
            if step_key == "trigger":
                step.log_stream = log_stream
                step.meta = message_body["meta"]
                step.webhook_url = message_body["dispatcher"]["webhook_url"]
                step.url = message_body["dispatcher"]["url"]

                if not step.dispatcher:
                    if step.debug:
                        step.dispatcher = Stdout(message_body["dispatcher"])
                    else:
                        step.dispatcher = Http(message_body["dispatcher"])

            params = message_body["input"]
            # passed to task; state is retrieved from DynamoDB & custom_config is retrieved from komand-properties
            state, custom_config = {}, {}
            has_more_pages = None
            status_code = None
            error_object = None

            if not is_test:
                # Validate input message
                try:
                    step.input.validate(params)
                    if step_key == "task":
                        state = message_body["state"]
                        step.state.validate(state)
                        custom_config = message_body.get(
                            "custom_config", {}
                        )  # we don't validate this for now

                    # Validate required inputs
                    # Step inputs will be checked against schema for required properties existence
                    # This is needed to prevent null/empty string values from being passed as output to input of steps
                    step.input.validate_required(params)
                except jsonschema.exceptions.ValidationError as e:
                    raise ClientException(
                        "{} input JSON was invalid".format(step_key), e
                    )
                except Exception as e:
                    raise Exception(
                        "Unable to validate {} input JSON".format(step_key), e
                    )

            # Log step information for improved debugging with users
            step.logger.info(
                "{vendor}/{plugin_name}:{plugin_version}. Step name: {step_name}".format(
                    vendor=step.connection.meta.vendor,
                    plugin_name=step.connection.meta.name,
                    plugin_version=step.connection.meta.version,
                    step_name=step.name,
                )
            )

            if is_test:
                # Check if connection test func available. If so - use it (preferred). Else fallback to action/trigger test
                if hasattr(step.connection, "test"):
                    if hasattr(step.connection, "test_task") and connection_test_type == "test_task":
                        # Get the test_task function from the connection
                        func = connection.test_task

                        # Inspect the function to see if it requires args
                        arguments = inspect.signature(func).parameters

                        # If the function has parameters, we pass the task name
                        if len(arguments) > 0 and "task" in message_body:
                            output, log = func(message_body["task"])
                        else:
                            output, log = func()
                        return output, log
                    else:
                        func = step.connection.test
                else:
                    func = step.test
            else:
                func = step.run

            # Backward compatibility with steps with missing argument params
            # The SDK has always defined the signature of the run/test methods to include the params dictionary.
            # However, the code generation generates the test method without the params argument.
            parameters = inspect.signature(func)
            if len(parameters.parameters) > 0:
                if step_key == "task" and not is_test:
                    output, state, has_more_pages, status_code, error_object = func(
                        params, state, custom_config
                    )
                else:
                    output = func(params)
            else:
                if step_key == "task" and not is_test:
                    output, state, has_more_pages, status_code, error_object = func()
                else:
                    output = func()

            # Don't validate output for any test functions - action/trigger tests shouldn't be validated due to them
            # not providing value and a connection test shouldn't be validated due to it being generic/universal
            if not is_test:
                step.output.validate(output)

            if step_key == "task" and not is_test:
                return output, state, has_more_pages, status_code, error_object

            return output
