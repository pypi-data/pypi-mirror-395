import json
import logging
import os
import sys
from time import sleep

import gunicorn.app.base
import structlog
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask import Flask, request_started, request
from gunicorn.arbiter import Arbiter
from pythonjsonlogger.jsonlogger import JsonFormatter, RESERVED_ATTRS
from requests import get as request_get
from requests.exceptions import (
    HTTPError,
    MissingSchema,
    Timeout,
    JSONDecodeError,
    ConnectionError,
)
from werkzeug.utils import secure_filename

from insightconnect_plugin_runtime.api.endpoints import Endpoints, handle_errors
from insightconnect_plugin_runtime.api.schemas import (
    PluginInfoSchema,
    ActionTriggerOutputBodySchema,
    ActionTriggerOutputSchema,
    TaskOutputBodySchema,
    TaskOutputSchema,
    ActionTriggerInputBodySchema,
    ActionTriggerInputSchema,
    TaskInputBodySchema,
    TaskInputSchema,
    ActionTriggerDetailsSchema,
    TaskDetailsSchema,
    ConnectionDetailsSchema,
    ConnectionTestSchema,
)
from insightconnect_plugin_runtime.helper import clean_dict
from insightconnect_plugin_runtime.telemetry import create_post_fork
from insightconnect_plugin_runtime.util import is_running_in_cloud, OTEL_ENDPOINT

API_TITLE = "InsightConnect Plugin Runtime API"
API_VERSION = "1.0"
OPEN_API_VERSION = "2.0"
VERSION_MAPPING = {"legacy": "/", "v1": "/api/v1"}
CPS_RETRY = 5
RETRY_SLEEP = 10
CPS_ENDPOINT = os.getenv(
    "CPS_ENDPOINT"
)  # endpoint to retrieve plugin custom configs (set in cloud deployments.tf)
DEFAULT_SCHEDULE_INTERVAL_MINUTES = (
    3  # default to 3 as most integrations run on 5 minute interval
)


class PluginServer(gunicorn.app.base.BaseApplication):
    """
    Server which runs the plugin as an HTTP server.

    Serves the following endpoints:

    POST http://host/actions/[action]        Executes action's run method
    POST http://host/actions/[action]/test   Executes action's test method
    POST http://host/triggers/[trigger]/test Executes trigger's test method

    NOTE: starting a trigger is not supported. Triggers should be started in legacy mode.

    """

    def __init__(
            self,
            plugin,
            port=10001,
            workers=1,
            threads=4,
            debug=False,
            worker_class="sync",
            worker_connections=200,
    ):

        gunicorn_file = os.environ.get("GUNICORN_CONFIG_FILE")
        if gunicorn_file:
            with open(secure_filename(gunicorn_file)) as gf:
                self.gunicorn_config = json.load(gf)
        else:
            self.gunicorn_config = {
                "bind": "%s:%s" % ("0.0.0.0", port),
                "workers": workers,
                "worker_class": worker_class,
                "loglevel": "debug" if debug else "info",
            }
            if worker_class == "gevent":
                self.gunicorn_config["worker_connections"] = worker_connections
            else:
                self.gunicorn_config["threads"] = threads

        super(PluginServer, self).__init__()
        self.plugin = plugin
        self.arbiter = Arbiter(self)

        self.configure_structlog_instance(is_debug=debug)
        self.logger = structlog.get_logger("plugin")

        self.debug = debug
        # Create an APISpec
        self.spec = APISpec(
            title=API_TITLE,
            version=API_VERSION,
            openapi_version=OPEN_API_VERSION,
            plugins=[FlaskPlugin(), MarshmallowPlugin()],
        )
        self.workers = workers
        self.threads = threads
        # initialise before reaching out to CPS for configured values
        self.config_options = {}
        self.get_plugin_properties_from_cps()
        self.app, self.blueprints = self.create_flask_app()

        if os.environ.get(OTEL_ENDPOINT):
            self.config_options[OTEL_ENDPOINT] = os.environ[OTEL_ENDPOINT]

    @staticmethod
    def configure_structlog_instance(is_debug: bool) -> None:
        structlog.configure(
            processors=[
                structlog.stdlib.merge_contextvars,  # Preserves contextvars, must come first in processors list
                structlog.stdlib.filter_by_level,
                structlog.stdlib.add_log_level,
                structlog.stdlib.PositionalArgumentsFormatter(),
                structlog.processors.StackInfoRenderer(),
                structlog.processors.UnicodeDecoder(),
                structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M.%S"),
                structlog.stdlib.render_to_log_kwargs,
            ],
            context_class=dict,
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True,
        )
        logger = logging.getLogger("plugin")
        logger.setLevel(logging.DEBUG if is_debug else logging.INFO)

        console_handler = logging.StreamHandler()
        if is_running_in_cloud():
            console_handler.setFormatter(
                # since python bump to 3.13 the logging lib now includes a bunch of extra keywords we want to discard
                JsonFormatter(reserved_attrs=RESERVED_ATTRS + ("taskName",))
            )  # Only log in JSON if running in cloud

        logger.addHandler(console_handler)

    def init(self, parser, opts, args):
        pass

    def load(self):
        return self.app

    def load_config(self):
        config = dict(
            [
                (key, value)
                for key, value in self.gunicorn_config.items()
                if key in self.cfg.settings and value is not None
            ]
        )
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

        post_fork = create_post_fork(lambda: self.app, lambda: self.plugin, lambda: self.config_options)
        self.cfg.set("post_fork", post_fork)

    def create_flask_app(self):
        app = Flask(__name__)

        # Add structured logging middlware - requires 'blinker' library
        # See https://flask.palletsprojects.com/en/2.2.x/signals/
        request_started.connect(self.bind_request_details, app)

        endpoints = Endpoints(
            self.logger,
            self.plugin,
            self.spec,
            self.debug,
            self.workers,
            self.threads,
            os.getpid(),
            self.config_options,
        )

        for code in [400, 404, 500]:
            app.register_error_handler(code, handle_errors)

        blueprints = endpoints.create_endpoints()
        # Return flask app and list of blueprints
        return app, blueprints

    def get_plugin_properties_from_cps(self):
        # Call out to komand-props to get configurations related to only the plugin pod running.
        if is_running_in_cloud():
            for attempt in range(1, CPS_RETRY + 1):
                self.logger.info(
                    f"Getting plugin configuration information... (attempt {attempt}/{CPS_RETRY})"
                )
                try:
                    request_response = request_get(CPS_ENDPOINT, timeout=30)
                    resp_json = request_response.json()
                    plugin = self.plugin.name.lower().replace(
                        " ", "_"
                    )  # match how we name our images
                    plugin_config = resp_json.get("plugins", {}).get(plugin, {})

                    if self.plugin.tasks:
                        self.config_options = plugin_config

                    if resp_json.get(OTEL_ENDPOINT, {}):
                        self.config_options[OTEL_ENDPOINT] = resp_json.get(OTEL_ENDPOINT, {})

                    self.logger.info("Plugin configuration successfully retrieved...")
                    return
                except MissingSchema as missing_schema:
                    self.logger.error(
                        f"Invalid URL being requested: {CPS_ENDPOINT}, error={missing_schema}"
                    )
                except Timeout as timeout:
                    self.logger.error(
                        f"Connection timeout hit. CPS={CPS_ENDPOINT}, error={timeout}"
                    )
                except HTTPError as http_error:
                    self.logger.error(
                        f"Connection error when trying to reach CPS. CPS={CPS_ENDPOINT}, error={http_error}"
                    )
                except JSONDecodeError as bad_json:
                    self.logger.error(
                        f"Got bad JSON back. Response content={request_response.content}, error={bad_json}"
                    )
                except ConnectionError as http_connection_pool_error:
                    self.logger.info(
                        "Connection refused when trying to reach CPS, retrying as the connection is still establishing."
                    )
                except Exception as error:
                    self.logger.error(
                        f"Hit an unexpected error when retrieving plugin custom configs, error={error}"
                    )
                sleep(RETRY_SLEEP)
            self.logger.error(
                f"Unable to reach CPS after {CPS_RETRY} attempts. CPS={CPS_ENDPOINT}"
            )

    def register_api_spec(self):
        """Register all swagger schema definitions and path objects"""
        self.spec.components.schema("PluginInfo", schema=PluginInfoSchema)
        self.spec.components.schema(
            "ActionTriggerOutputBody", schema=ActionTriggerOutputBodySchema
        )
        self.spec.components.schema(
            "ActionTriggerOutput", schema=ActionTriggerOutputSchema
        )
        self.spec.components.schema("TaskOutputBody", schema=TaskOutputBodySchema)
        self.spec.components.schema("TaskOutput", schema=TaskOutputSchema)
        self.spec.components.schema(
            "ActionTriggerInputBody", schema=ActionTriggerInputBodySchema
        )
        self.spec.components.schema(
            "ActionTriggerInput", schema=ActionTriggerInputSchema
        )
        self.spec.components.schema("TaskInputBody", schema=TaskInputBodySchema)
        self.spec.components.schema("TaskInput", schema=TaskInputSchema)
        self.spec.components.schema(
            "ActionTriggerDetails", schema=ActionTriggerDetailsSchema
        )
        self.spec.components.schema("ConnectionDetails", schema=ConnectionDetailsSchema)
        self.spec.components.schema("ConnectionTestOutput", schema=ConnectionTestSchema)
        self.spec.components.schema("TaskDetails", schema=TaskDetailsSchema)
        self.spec.path(view=self.app.view_functions["v1.api_spec"])
        self.spec.path(view=self.app.view_functions["v1.plugin_info"])
        self.spec.path(view=self.app.view_functions["v1.plugin_spec"])
        self.spec.path(view=self.app.view_functions["v1.actions"])
        self.spec.path(view=self.app.view_functions["v1.triggers"])
        self.spec.path(view=self.app.view_functions["v1.tasks"])
        self.spec.path(view=self.app.view_functions["v1.status"])
        self.spec.path(view=self.app.view_functions["v1.action_run"])
        self.spec.path(view=self.app.view_functions["v1.task_run"])
        self.spec.path(view=self.app.view_functions["v1.action_test"])
        self.spec.path(view=self.app.view_functions["v1.trigger_test"])
        self.spec.path(view=self.app.view_functions["v1.task_test"])
        self.spec.path(view=self.app.view_functions["v1.action_details"])
        self.spec.path(view=self.app.view_functions["v1.trigger_details"])
        self.spec.path(view=self.app.view_functions["v1.task_details"])
        self.spec.path(view=self.app.view_functions["v1.connection"])
        self.spec.path(view=self.app.view_functions["v1.connection_test"])

    def register_blueprint(self):
        """Register all blueprints"""
        for blueprint in self.blueprints:
            self.app.register_blueprint(
                blueprint, url_prefix=VERSION_MAPPING[blueprint.name]
            )

    @staticmethod
    def bind_request_details(sender: Flask, **extras) -> None:
        """
        Middleware for binding request ID headers to structlog context
        @param sender: Flask instance
        @param extras: kwargs
        @return: None
        """

        request_id = "X-REQUEST-ID"
        org_id = "X-IPIMS-ORGID"
        int_id = "X-INTEGRATION-ID"

        structlog.contextvars.clear_contextvars()
        if is_running_in_cloud():
            structlog.contextvars.bind_contextvars(
                **clean_dict(
                    {
                        "request_path": request.path,
                        "request_id": request.headers.get(request_id),
                        "org_id": request.headers.get(org_id),
                        "int_id": request.headers.get(int_id),
                    }
                )
            )

    def start(self):
        """start server"""
        with self.app.app_context():
            try:
                self.register_blueprint()
                self.register_api_spec()
                self.arbiter.run()
            except RuntimeError as e:
                sys.stderr.write("\nError: %s\n" % e)
                sys.stderr.flush()
                sys.exit(1)
