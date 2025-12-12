import importlib.metadata as importlib_metadata
import json
import os
import signal
import subprocess
from typing import Any, Dict

import structlog
import yaml
from flask import Blueprint, abort, jsonify, make_response, request
from werkzeug.exceptions import HTTPException, InternalServerError

from insightconnect_plugin_runtime.api.schemas import (
    ActionTriggerDetailsSchema,
    ConnectionDetailsSchema,
    PluginInfoSchema,
    TaskDetailsSchema,
)
from insightconnect_plugin_runtime.exceptions import (
    ClientException,
    ConnectionTestException,
    LoggedException,
    PluginException,
    ServerException,
)
from insightconnect_plugin_runtime.util import OutputMasker
from uuid import UUID

logger = structlog.get_logger("plugin")
ORG_ID = "X-IPIMS-ORGID"
INT_ID = "X-INTEGRATION-ID"

PLUGIN_SPEC_DOCKERFILE = "/python/src/plugin.spec.yaml"
PLUGIN_SPEC_PACK = "/workspace/plugin.spec.yaml"


# Must be defined at application level in order to capture all 404's with blueprints,
# see https://flask.palletsprojects.com/en/2.3.x/errorhandling/#blueprint-error-handlers
def handle_errors(error: HTTPException):
    # Get default values
    status_code = error.code
    error_description = error.description
    error_name = error.name

    resp = {}

    # If there is an ISE then there is additional information to capture
    if isinstance(error, InternalServerError):
        resp["original_exception"] = {
            "exception": error.original_exception.__class__.__name__,
            "message": str(error.original_exception),
        }
        error_name = error.original_exception.__class__.__name__

        if isinstance(error.original_exception, LoggedException):
            resp["log"] = error.original_exception.output["body"]["log"]

            # Capture metrics if available (eg. running in cloud)
            if "metrics" in error.original_exception.output["body"]:
                resp["metrics"] = error.original_exception.output["body"]["metrics"]

            error_description = str(error.original_exception)

            # If ClientException occurs, it is due to a bad request from the consumer, so send a 400
            if isinstance(error.original_exception.ex, ClientException):
                status_code = 400

    resp.update(
        {
            "code": status_code,
            "description": error_description,
            "name": error_name,
            "response": error.response,
            "url": request.url,
            "method": request.method,
        }
    )

    logger.error(
        error,
        code=status_code,
        method=request.method,
        url=request.url,
        error_description=error_description,
    )

    return jsonify(resp), status_code


class Endpoints:
    def __init__(
        self,
        logger,
        plugin,
        spec,
        debug,
        workers,
        threads,
        master_pid,
        config_options=None,
    ):
        self.plugin = plugin
        self.logger = structlog.get_logger("plugin")
        self.spec = spec
        self.debug = debug
        self.workers = workers
        self.threads = threads
        self.master_pid = master_pid
        self.config_options = config_options

    def create_endpoints(self):
        legacy = Blueprint("legacy", __name__)
        v1 = Blueprint("v1", __name__)

        @v1.route("/actions/<string:name>", methods=["POST"])
        @legacy.route("/actions/<string:name>", methods=["POST"])
        def action_run(name):
            """Run action endpoint.
            ---
            post:
              summary: Run an action
              description: Run an action
              parameters:
                - in: path
                  name: name
                  description: Name of the action
                  type: string
                - in: body
                  name: Action Input
                  description: Input to run an action
                  required: true
                  schema: ActionTriggerInputSchema
              responses:
                200:
                  description: Action output to be returned
                  schema: ActionTriggerOutputSchema
                400:
                  description: Bad request
                500:
                  description: Unexpected error
            """
            input_message = request.get_json(force=True)
            self.logger.debug("Request input: %s", input_message)
            Endpoints.validate_action_trigger_task_empty_input(
                input_message
            )  # TODO: This may not be necessary
            Endpoints.validate_action_trigger_task_name(input_message, name, "action")
            output = self.run_action_trigger_task(input_message)
            return output

        @v1.route("/tasks/<string:name>", methods=["POST"])
        @legacy.route("/tasks/<string:name>", methods=["POST"])
        def task_run(name):
            """Run task endpoint.
            ---
            post:
              summary: Run a task
              description: Run a task
              parameters:
                - in: path
                  name: name
                  description: Name of the task
                  type: string
                - in: body
                  name: Task Input
                  description: Input to run a task
                  required: true
                  schema: TaskInputSchema
              responses:
                200:
                  description: Task output to be returned
                  schema: TaskOutputSchema
                400:
                  description: Bad request
                500:
                  description: Unexpected error
            """

            self.logger.info("Plugin task beginning execution...")
            input_message = request.get_json(force=True)
            self.logger.debug("Request input: %s", input_message)
            Endpoints.validate_action_trigger_task_empty_input(input_message)
            Endpoints.validate_action_trigger_task_name(input_message, name, "task")

            # No validation on the plugin custom config to leave this as configurable as possible.
            # `add_plugin_custom_config` will pass any available values to the plugin for interpretation.
            input_message = self.add_plugin_custom_config(
                input_message,
                request.headers.get(ORG_ID, ""),
                request.headers.get(INT_ID, ""),
                name,
            )
            output = self.run_action_trigger_task(input_message, mask_output=False)
            self.logger.info("Plugin task finished execution...")
            return output

        @legacy.route("/triggers/<string:name>/test", methods=["POST"])
        @v1.route("/triggers/<string:name>/test", methods=["POST"])
        def trigger_test(name):
            """Run trigger test endpoint.
            ---
            post:
              summary: Run trigger test
              description: Run trigger test
              parameters:
                - in: path
                  name: name
                  description: Name of the trigger
                  type: string
                - in: body
                  name: Trigger Input
                  description: Input to run a trigger
                  required: true
                  schema: ActionTriggerInputSchema
              responses:
                200:
                  description: Trigger test output to be returned
                  schema: ActionTriggerOutputSchema
                400:
                  description: Bad request
                500:
                  description: Unexpected error
            """
            input_message = request.get_json(force=True)
            self.logger.debug("Request input: %s", input_message)
            Endpoints.validate_action_trigger_task_empty_input(input_message)
            Endpoints.validate_action_trigger_task_name(input_message, name, "trigger")
            output = self.run_action_trigger_task(input_message, True)
            return output

        @legacy.route("/actions/<string:name>/test", methods=["POST"])
        @v1.route("/actions/<string:name>/test", methods=["POST"])
        def action_test(name):
            """Run action test endpoint.
            ---
            post:
              summary: Run action test
              description: Run action test
              parameters:
                - in: path
                  name: name
                  description: Name of the action
                  type: string
                - in: body
                  name: Action Input
                  description: Input to run an action
                  required: true
                  schema: ActionTriggerInputSchema
              responses:
                200:
                  description: Action test output to be returned
                  schema: ActionTriggerOutputSchema
                400:
                  description: Bad request
                500:
                  description: Unexpected error
            """
            input_message = request.get_json(force=True)
            self.logger.debug("Request input: %s", input_message)
            Endpoints.validate_action_trigger_task_empty_input(input_message)
            Endpoints.validate_action_trigger_task_name(input_message, name, "action")
            output = self.run_action_trigger_task(input_message, True)
            return output

        @legacy.route("/tasks/<string:name>/test", methods=["POST"])
        @v1.route("/tasks/<string:name>/test", methods=["POST"])
        def task_test(name):
            """Run task test endpoint.
            ---
            post:
              summary: Run task test
              description: Run task test
              parameters:
                - in: path
                  name: name
                  description: Name of the task
                  type: string
                - in: body
                  name: Task Input
                  description: Input to run a task
                  required: true
                  schema: TaskInputSchema
              responses:
                200:
                  description: Task test output to be returned
                  schema: TaskOutputSchema
                400:
                  description: Bad request
                500:
                  description: Unexpected error
            """
            input_message = request.get_json(force=True)
            self.logger.debug("Request input: %s", input_message)
            Endpoints.validate_action_trigger_task_empty_input(input_message)
            Endpoints.validate_action_trigger_task_name(input_message, name, "task")
            output = self.run_action_trigger_task(input_message, True, connection_test_type="test_task")
            return output

        @v1.route("/api")
        def api_spec():
            """API spec details endpoint.
            ---
            get:
              summary: Get API spec details
              description: Get Swagger v2.0 API Specification
              parameters:
                - in: query
                  name: format
                  type: string
                  description: Format to return swagger spec; defaults to JSON
                  enum: [json, yaml]
              responses:
                200:
                  description: Swagger Specification to be returned
                  schema:
                    type: object
                422:
                  description: The specified format is not supported
            """
            format_ = request.args.get("format", "json")
            if format_ == "json":
                return json.dumps(self.spec.to_dict())
            elif format_ == "yaml":
                return self.spec.to_yaml()
            else:
                return make_response(
                    jsonify({"error": "The specified format is not supported"}), 422
                )

        @v1.route("/info")
        def plugin_info():
            """Plugin spec details endpoint.
            ---
            get:
              summary: Get plugin details
              description: Get InsightConnect plugin details
              responses:
                200:
                  description: InsightConnect Plugin Information to be returned
                  schema: PluginInfoSchema
            """
            plugin_spec_json = Endpoints.load_plugin_spec_file()
            plugin_info_fields = [
                "name",
                "description",
                "version",
                "vendor",
                "plugin_spec_version",
                "title",
                "support",
                "tags",
                "enable_cache",
            ]
            response = Endpoints.get_plugin_info(plugin_spec_json, plugin_info_fields)
            # Add workers and threads
            response.update(
                {
                    "number_of_workers": self.workers,
                    "threads": self.threads,
                    "sdk_version": self.get_plugin_sdk_version(),
                }
            )
            return jsonify(PluginInfoSchema().dump(response))

        @v1.route("/actions")
        def actions():
            """Plugin actions list endpoint.
            ---
            get:
              summary: Get list of plugin actions
              description: Get InsightConnect plugin all actions
              responses:
                200:
                  description: InsightConnect Plugin actions list to be returned
                  schema:
                    type: array
                    items:
                      type: string
            """
            action_list = []
            for action in self.plugin.actions.keys():
                action_list.append(action)
            return jsonify(action_list)

        @v1.route("/definitions/actions")
        def definitions_all_actions():
            """Return definitions for all actions
            ---
            get:
              summary: Get list of plugin actions with associated input schemas
              description: Get InsightConnect plugin all actions with associated input schemas
              responses:
                200:
                  description: InsightConnect Plugin actions with input schemas list to be returned
                  schema:
                    type: object
            """

            response = self._create_action_definitions_payload()
            return jsonify(response)

        @v1.route("/tasks")
        def tasks():
            """Plugin tasks list endpoint.
            ---
            get:
              summary: Get list of plugin tasks
              description: Get InsightConnect plugin all tasks
              responses:
                200:
                  description: InsightConnect Plugin tasks list to be returned
                  schema:
                    type: array
                    items:
                      type: string
            """
            task_list = []
            for task in self.plugin.tasks.keys():
                task_list.append(task)
            return jsonify(task_list)

        @v1.route("/actions/<string:name>")
        def action_details(name):
            """Get action details endpoint.
            ---
            get:
              summary: Retrieve action details
              description: Retrieve action details
              parameters:
                - in: path
                  name: name
                  description: Name of the action
                  type: string
              responses:
                200:
                  description: Action details to be returned
                  schema: ActionTriggerDetailsSchema
                400:
                  description: Bad request
            """
            plugin_spec_json = Endpoints.load_plugin_spec_file()
            Endpoints.action_trigger_task_exists(plugin_spec_json, "actions", name)
            return jsonify(
                ActionTriggerDetailsSchema().dump(
                    plugin_spec_json.get("actions").get(name)
                )
            )

        @v1.route("/tasks/<string:name>")
        def task_details(name):
            """Get task details endpoint.
            ---
            get:
              summary: Retrieve task details
              description: Retrieve task details
              parameters:
                - in: path
                  name: name
                  description: Name of the task
                  type: string
              responses:
                200:
                  description: Task details to be returned
                  schema: TaskDetailsSchema
                400:
                  description: Bad request
            """
            plugin_spec_json = Endpoints.load_plugin_spec_file()
            Endpoints.action_trigger_task_exists(plugin_spec_json, "tasks", name)
            return jsonify(
                TaskDetailsSchema().dump(plugin_spec_json.get("tasks").get(name))
            )

        @v1.route("/triggers/<string:name>")
        def trigger_details(name):
            """Get trigger details endpoint.
            ---
            get:
              summary: Retrieve trigger details
              description: Retrieve trigger details
              parameters:
                - in: path
                  name: name
                  description: Name of the trigger
                  type: string
              responses:
                200:
                  description: Trigger details to be returned
                  schema: ActionTriggerDetailsSchema
                400:
                  description: Bad request
            """
            plugin_spec_json = Endpoints.load_plugin_spec_file()
            Endpoints.action_trigger_task_exists(plugin_spec_json, "triggers", name)
            return jsonify(
                ActionTriggerDetailsSchema().dump(
                    plugin_spec_json.get("triggers").get(name)
                )
            )

        @v1.route("/triggers")
        def triggers():
            """Plugin triggers list endpoint.
            ---
            get:
              summary: Get list of plugin triggers
              description: Get InsightConnect plugin all triggers
              responses:
                200:
                  description: InsightConnect Plugin triggers list to be returned
                  schema:
                    type: array
                    items:
                      type: string
            """
            trigger_list = []
            for action in self.plugin.triggers.keys():
                trigger_list.append(action)
            return jsonify(trigger_list)

        @v1.route("/status")
        def status():
            """Web service status endpoint
            ---
            get:
              summary: Get web service status
              description: Get web service status
              responses:
                200:
                  description: Status to be returned
                  schema:
                    type: object
            """
            # TODO: Add logic to figure out status (Ready, Running, Down) of web service.
            return jsonify({"status": "Ready"})

        @v1.route("/spec")
        def plugin_spec():
            """Plugin spec details endpoint.
            ---
            get:
              summary: Get plugin spec details
              description: Get plugin specification
              parameters:
                - in: query
                  name: format
                  type: string
                  description: Format to return plugin spec; defaults to JSON
                  enum: [json, yaml]
              responses:
                200:
                  description: Plugin specification to be returned
                  schema:
                    type: object
                422:
                  description: The specified format is not supported
            """
            format_ = request.args.get("format", "json")
            if format_ not in ["json", "yaml"]:
                return make_response(
                    jsonify({"error": "The specified format is not supported"}), 422
                )

            try:
                with open(PLUGIN_SPEC_DOCKERFILE, "r") as p_spec:
                    plugin_spec = p_spec.read()
            except FileNotFoundError:
                with open(PLUGIN_SPEC_PACK, "r") as p_spec:
                    plugin_spec = p_spec.read()

            if format_ == "yaml":
                return plugin_spec
            return jsonify(yaml.safe_load(plugin_spec))

        @v1.route("/workers/add", methods=["POST"])
        def add_worker():
            """
            Adds a worker (another process)
            :return: Json Response
            """
            response = {}

            # Linux signal examples here:
            # https://docs.gunicorn.org/en/stable/signals.html#master-process
            try:
                self.logger.info("Adding a worker")
                self.logger.info("Current process is: %s" % self.master_pid)
                os.kill(self.master_pid, signal.SIGTTIN)
            except Exception as error:
                response.status_code = 500
                response.error = error
                return jsonify(response)

            response["num_workers"] = Endpoints._number_of_workers()
            return jsonify(response)

        @v1.route("/workers/remove", methods=["POST"])
        def remove_worker():
            """
            Shuts down a worker (another process)
            If there is only 1 worker, nothing happens

            :return: Json Response
            """

            response = {}

            # Linux signal examples here:
            # https://docs.gunicorn.org/en/stable/signals.html#master-process
            try:
                self.logger.info("Removing a worker")
                self.logger.info("Current process is: %s" % self.master_pid)
                os.kill(self.master_pid, signal.SIGTTOU)
            except Exception as error:
                response = {}
                response.status_code = 500
                response.error = error
                return jsonify(response)

            return jsonify(response)  # Flask or Gunicorn expect a return

        @v1.route("/workers", methods=["GET"])
        def num_workers():
            response = {"num_workers": Endpoints._number_of_workers()}
            return jsonify(response)

        @v1.route("/connection", methods=["GET"])
        def connection():
            """Plugin connection details endpoint
            ---
            get:
              summary: Get plugin connection details
              description: Get InsightConnect plugin connection details
              responses:
                200:
                  description: InsightConnect plugin connection details to be returned
                  schema: ConnectionDetailsSchema
            """
            conn = self.plugin.connection
            schema = conn.schema
            return jsonify(ConnectionDetailsSchema().dump(schema))

        @v1.route("/connection/<string:connection_test_type>", methods=["POST"])
        def connection_test(connection_test_type: str):
            """
            Run connection test endpoint
            ---
            post:
              summary: Run connection test
              description: Run InsightConnect plugin connection test
              parameters:
                - in: path
                  name: connection_test_type
                  description: Type of connection test to be run
                  type: string
              responses:
                200:
                  description: Connection test output to be returned
                  schema: ConnectionTestSchema
                204:
                  description: The server successfully processed the request and is not returning any content
                400:
                  description: A ConnectionTestException has occurred
                500:
                  description: Internal server error
                501:
                  description: The connection test() is not implmented
            """
            status_code = 200
            output = None

            supported_tests = ["test", "test_task"]
            if connection_test_type not in supported_tests:
                return make_response(
                    jsonify(
                        {
                            "error": f"The requested endpoint is not available, only {supported_tests} are supported.",
                            "code": 404,
                            "method": "POST",
                            "name": "Not Found"
                        }
                    ),
                    404,
                )

            input_message = request.get_json(force=True)
            Endpoints.validate_action_trigger_task_empty_input(input_message)

            try:
                output = self.plugin.handle_step(
                    input_message, is_debug=self.debug, is_test=True, connection_test_type=connection_test_type
                )
                if output.get("body", {}).get("output") is None:
                    status_code = 204
            except LoggedException as error:
                wrapped_exception = error.ex
                self.logger.exception(wrapped_exception)

                output = error.output
                status_code = Endpoints.handle_wrapped_exception(wrapped_exception)
            finally:
                response = jsonify(output)
                response.status_code = status_code
                return response

        blueprints = [legacy, v1]
        return blueprints

    def _create_action_definitions_payload(self):
        """
        Creates a payload containing definitions for all actions within a given plugin
        :return: Dictionary containing an actions definitions payload for a plugin
        """

        payload = {"actionsDefinitions": []}
        for key, value in self.plugin.actions.items():
            definition = {"identifier": key, "inputJsonSchema": value.input.schema}

            payload["actionsDefinitions"].append(definition)

        return payload

    @staticmethod
    def _number_of_workers():
        """
        Number of workers tries to return the number of workers in use for gunicorn
        It finds all processes named komand or icon and returns the number it finds minus 1.

        The minus 1 is due to gunicorn always having a master process and at least 1 worker.

        This function will likely produce unreliable results if used outside of a docker container

        :return: integer
        """
        output = subprocess.check_output(
            'ps | grep "icon\\|komand" | grep -v "grep" | wc -l', shell=True
        )
        num_workers = int(output.decode())

        # num_workers - 1 due to a master process being run as well
        return num_workers - 1

    @staticmethod
    def action_trigger_task_exists(plugin_spec_json, p_type, p_name):
        actions_triggers_tasks = plugin_spec_json.get(p_type)
        if actions_triggers_tasks is None or actions_triggers_tasks.get(p_name) is None:
            msg = f"{p_type[:-1].capitalize()} {p_name} does not exist"
            response = make_response(jsonify({"error": msg}), 400)
            abort(response)
        return actions_triggers_tasks.get(p_name)

    @staticmethod
    def load_plugin_spec_file() -> Dict[str, Any]:
        try:
            return Endpoints.load_file_json_format(PLUGIN_SPEC_DOCKERFILE)
        except FileNotFoundError:
            return Endpoints.load_file_json_format(PLUGIN_SPEC_PACK)

    @staticmethod
    def load_file_json_format(filename: str) -> Dict[str, Any]:
        with open(filename, "r") as plugin_spec:
            return yaml.safe_load(plugin_spec.read())

    @staticmethod
    # TODO: I don't think this function actually does anything - lack of an input message is caught earlier in the call chain
    def validate_action_trigger_task_empty_input(input_message):
        if not input_message:
            response = make_response(jsonify({"error": "Empty input provided"}), 400)
            abort(response)

    @staticmethod
    def validate_action_trigger_task_name(input_message, name, p_type):
        name_in_input_msg = input_message.get("body", {}).get(p_type)
        if name_in_input_msg != name:
            msg = (
                f"{p_type.capitalize()} name ({name_in_input_msg}) in input "
                f"body is not matching with name ({name}) in route"
            )
            abort(400, description=msg)

    @staticmethod
    def get_plugin_info(plugin_spec_json, fields):
        plugin_info = {}
        for field in fields:
            plugin_info.update({field: plugin_spec_json.get(field)})
        return plugin_info

    def get_plugin_sdk_version(self):
        try:
            version = importlib_metadata.version("insightconnect-plugin-runtime")
        except Exception:
            self.logger.warn("Unable to get SDK version")
            version = "0.0.0"
        return version

    def add_plugin_custom_config(
        self, input_data: Dict[str, Any], org_id: str, int_id: str, task_name: str
    ) -> Dict[str, Any]:
        """
        Using the retrieved configs pulled from komand-props, pass the configuration that matches the requesting
        Org ID which is passed to the task via a header (`X-IPIMS-ORGID`) from the plugin sidecar.

        Config example: {'org_1': {"default": 24, "lookback": "108"}, "*": {"default": 12, "lookback": 100}}

        In this config example the following we be applied:
        - org 1 to has a custom default time of 24 hours for their timings.
        - org 1 when in lookback mode will pull back 108 hours (task triggered with no state).
        - all orgs for default runs will poll back 12 hours.
        - all orgs in lookback mode will be 100 hours (task triggered with no state).

        When Int ID is specified or task name. Then it can be used across all orgs (global config) or specific Org ID.
        There's a hierarchy between task related config and Int ID related, where Int ID will always
        replace task related config due to its higher priority.

        Config example:
        {
            "org_1": {
                "task_name_1": {
                    "default": 12,
                    "lookback": "100"
                },
                "int_1": {
                    "default": 6,
                    "lookback": "50"
                },
                {
                    "default": 24,
                    "lookback": "108"
                }
            },
            "*": {
                "default": 24,
                "lookback": 200
                "task_name_2": {
                    "default": 2,
                    "lookback": "10"
                }
            }
        }

        In this config example the following we be applied:
        - org 1 to has a custom default time of 24 hours for their timings.
        - org 1 when in lookback mode will pull back 108 hours (task triggered with no state).
        - org 1 all integrations that uses task with 'task_name_1' will pull back 100 hours
        and have a custom default time of 12 hours for their timings.
        - org 1 specific integration 'int_1' will pull back 50 hours and have a custom
        default time of 6 hours for their timings.
        - all orgs for default runs will poll back 24 hours.
        - all orgs in lookback mode will be 200 hours (task triggered with no state).
        - all orgs that uses task with 'task_name_2' will pull back 2 hours
        - all orgs that uses task with 'task_name_2' in lookback mode will be 10 hours
        """

        # Parse configuration based on organization or global. Use its copies, not to modify original dict.
        organization_config, global_config = self.config_options.get(org_id, {}).copy(), self.config_options.get("*", {}).copy()

        # Definition of additional config and its type variables.
        additional_config, config_type = {}, ""

        # Check if we have a global config.
        # Also, use "config_type" variable just for logging purposes to have an indicator from where the config was pulled.
        if global_config:
            # Setup global config as starting point.
            additional_config, config_type = global_config, "GLOBAL"

            # If task configuration was found under global config, update it with task config to replace necessary values.
            if task_config := global_config.get(task_name):
                additional_config.update(task_config)
                config_type = "GLOBAL_TASK"

        # If organization config is present, then replace its values with the ones coming from global config.
        if organization_config:
            # Update additional config with values coming from organization config.
            additional_config.update(organization_config)
            config_type = "ORG"

            # If task configuration was found under organization, replace its values with organization config.
            if task_config := organization_config.get(task_name):
                additional_config.update(task_config)
                config_type = "ORG_TASK"

            # If integration config was found under organization replace its values with organization
            # and task config (higher priority).
            if integration_config := organization_config.get(int_id):
                additional_config.update(integration_config)
                config_type = "ORG_INT"

        if additional_config:
            self.logger.info(
                f"Found config options ({config_type}); adding this to the request parameters..."
            )

            # Sopy to preserve the referenced value in self.config_options.
            # Also, remove unnecessary fields from that config (int_ids, or task_names) that occurs
            # when updated global dictionary above. This thing is that we use global config as base
            # and then updating some fields depending on the configuration.
            additional_config = self._remove_unnecessary_fields_from_custom_config(additional_config)

            # As a safeguard we only pass the lookback config params if the plugin has no state
            # This means we still need to manually delete the state for plugins on a per org basis.
            # This also means first time customers for their 'initial' lookup would get the lookback value passed in.
            if input_data.get("body", {}).get("state") and additional_config.get(
                "lookback"
            ):
                self.logger.info(
                    "Found an existing plugin state, not passing lookback value..."
                )
                del additional_config["lookback"]
            input_data.get("body", {}).update({"custom_config": additional_config})
            self.logger.info(f"Custom config being sent to plugin: {additional_config}")

        return input_data

    def run_action_trigger_task(self, input_message, test=False, connection_test_type="test", mask_output=True):
        connection = input_message.get("body", {}).get("connection", {})
        status_code = 200
        output = None
        try:
            output = self.plugin.handle_step(
                input_message, is_debug=self.debug, is_test=test, connection_test_type=connection_test_type
            )
        except LoggedException as error:
            wrapped_exception = error.ex
            self.logger.exception(wrapped_exception)

            output = error.output
            if isinstance(wrapped_exception, ClientException):
                status_code = 400
            elif (
                isinstance(wrapped_exception, PluginException)
                and wrapped_exception.preset is PluginException.Preset.BAD_REQUEST
            ):
                status_code = 400
            elif isinstance(wrapped_exception, (ConnectionTestException, ClientException)):
                status_code = 400
            elif isinstance(wrapped_exception, ServerException):
                # I'm unsure about this
                status_code = 500
            else:
                status_code = 500
        finally:
            self.logger.debug("Request output: %s", output)
            # As this processing can take quite a while on large task ouputs we want to skip this
            if mask_output:
                response = jsonify(OutputMasker.mask_output_data(connection, output))
            else:
                response = jsonify(output)
            response.status_code = status_code
            return response

    @staticmethod
    def handle_wrapped_exception(wrapped_exception):
        if isinstance(wrapped_exception, (ConnectionTestException, ClientException)):
            return 400
        elif (
            isinstance(wrapped_exception, PluginException)
            and wrapped_exception.preset is PluginException.Preset.BAD_REQUEST
        ):
            return 400
        elif isinstance(wrapped_exception, ServerException):
            return 500
        elif isinstance(wrapped_exception, NotImplementedError):
            return 501
        else:
            return 500

    def _remove_unnecessary_fields_from_custom_config(self, additional_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Removes unnecessary fields from custom config such as other task names, and int_ids,
        leaving only the fields that needs to be parsed.

        :param additional_config: The custom config dictionary on which, unnecessary fields will be removed.
        :type additional_config: Dict[str, Any]

        :return: New custom config dictionary with unnecessary fields removed.
        :rtype: Dict[str, Any]
        """

        # Copy 'additional_config' not to operate on it
        config_copy = additional_config.copy()

        # Remove other task names from config
        for task_ in self.plugin.tasks.keys():
            config_copy.pop(task_, None)

        # Remove other int_ids from config
        for key_ in additional_config.keys():
            if self._check_if_uuid(key_):
                config_copy.pop(key_, None)
        return config_copy

    @staticmethod
    def _check_if_uuid(input_string: str) -> bool:
        """
        Validates whether the provided string matches UUID format specifications.

        :param input_string: The string to validate against UUID format standards
        :type input_string: str

        :return: True if the string is a valid UUID, False otherwise
        :rtype: bool
        """

        try:
            UUID(input_string)
            return True
        except (TypeError, ValueError):
            return False
