# -*- coding: utf-8 -*-
from tests.plugin.hello_world import KomandHelloWorld
from insightconnect_plugin_runtime import CLI
from insightconnect_plugin_runtime.server import PluginServer
from unittest.mock import patch
from .utils import MockResponse
import pytest
import json

BASE_JSON = {"body": {"task": "monitor_events", "state": {"checkpoint": "16 Feb 2024"}},
             "type": "task_start", "version": "v1"}

ORG_1_ID, ORG_1 = "1234-5678-91011", {"default": "24", "lookback": "1st Feb 2024"}
ORG_2_ID, ORG_2 = "91011-1213-1415", {"default": "48"}
ALL_ORGS = {"default": "12"}

CONFIG_OPTIONS = {
        "hello_world": {
            ORG_1_ID: ORG_1,
            ORG_2_ID: ORG_2,  # never accessed either
            "*": ALL_ORGS  # applied to every org hitting this plugin
        },
        "other_plugin": {
            ORG_1_ID: {"default": "80"},  # not used as we're not testing `other_plugin`
        }
}


@pytest.fixture(scope="class")
def plugin_server():
    # Initialize plugin
    cli = CLI(KomandHelloWorld())

    with patch("insightconnect_plugin_runtime.server.request_get") as mock_req:
        with patch("insightconnect_plugin_runtime.server.is_running_in_cloud") as cloud:
            cloud.return_value = True
            mock_req.return_value = MockResponse({"plugins": CONFIG_OPTIONS})
            plugin = PluginServer(cli.plugin, port=10001, workers=1, threads=4, debug=False)

    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = plugin.app.test_client()

    # register APIs as handled usually by plugin.start()
    with plugin.app.app_context():
        plugin.register_blueprint()
        plugin.register_api_spec()

    # Establish an application context before running tests
    ctx = plugin.app.app_context()
    ctx.push()

    # Allow tests to run and provide client
    yield testing_client

    # Cleanup application context
    ctx.pop()


def test_task_api(plugin_server):
    # Quick test to ensure the task endpoint is up and running
    response = plugin_server.get("/api/v1/tasks")
    assert response.status_code == 200

    response_json = json.loads(response.data)
    expected = ["monitor_events"]

    assert sorted(expected) == sorted(response_json)


def test_task_api_pass_through_no_org_configs(plugin_server):
    # The plugin will always pass the same request into the endpoint
    req_params = make_request(plugin_server, BASE_JSON)

    # We shouldn't be updating the state this should remain untouched and not org_id passed to add custom_config
    # but the plugin should pick up the `*` config
    assert req_params["body"]["state"] == BASE_JSON["body"]["state"]
    assert req_params["body"]["custom_config"] == ALL_ORGS


def test_task_api_pass_through_org_2_config(plugin_server):
    # The plugin will always pass the same request into the endpoint
    req_params = make_request(plugin_server, BASE_JSON, {"X-IPIMS-ORGID": ORG_2_ID})

    # We pass an org ID that has a config for this plugin
    assert req_params["body"]["custom_config"] == ORG_2


def test_task_api_removes_lookback_if_state(plugin_server):
    req_json = BASE_JSON.copy()  # We edit this in this test, take a copy
    # Make first request
    req_params = make_request(plugin_server, req_json, {"X-IPIMS-ORGID": ORG_1_ID})

    # There is a state passed in so we ignore the lookback value the first time the task is triggered
    assert req_params["body"]["custom_config"] == {"default": ORG_1["default"]}

    # Second request after state has been cleared
    del req_json["body"]["state"]
    req_params_2 = make_request(plugin_server, req_json, {"X-IPIMS-ORGID": ORG_1_ID})
    # There is now no state passed in so include the whole config
    assert req_params_2["body"]["custom_config"] == ORG_1


def make_request(plugin_server, req_json, req_headers=None):
    """Helper to call the task endpoint and return the parameters used."""
    with patch("insightconnect_plugin_runtime.api.endpoints.Endpoints.run_action_trigger_task") as task_run:
        task_run.return_value = {'key': 'json returned by task output'}
        # during the processing of the request the server should check for any configs pulled from komand-props
        plugin_server.post("/api/v1/tasks/monitor_events", json=req_json, headers=req_headers if req_headers else {})

        return task_run.call_args.args[0]
