from requests.exceptions import HTTPError, Timeout, TooManyRedirects, ConnectionError
from parameterized import parameterized
from unittest import TestCase, skip
from unittest.mock import patch, MagicMock

from insightconnect_plugin_runtime.server import PluginServer
from insightconnect_plugin_runtime.util import OTEL_ENDPOINT
from tests.plugin.hello_world import KomandHelloWorld
from .utils import MockResponse, Logger

SCHEDULE_INTERVAL, PLUGIN_VALUE_1, PLUGIN_VALUE_2 = 25, {"*": 24}, {"org_1": "Tues 14th Sept 2024"}


@patch("gunicorn.arbiter.Arbiter.run", side_effect=MagicMock())
@patch("insightconnect_plugin_runtime.server.is_running_in_cloud", return_value=True)
class TestServerCloudPlugins(TestCase):
    def setUp(self) -> None:
        self.plugin = KomandHelloWorld()
        self.plugin_name = self.plugin.name.lower().replace(" ", "_")

    @parameterized.expand([["Set cloud to false", False], ["Set cloud to true", True]])
    @patch("insightconnect_plugin_runtime.server.request_get")
    def test_cloud_plugin_no_tasks_ignore_cps(self, _test_name, cloud, mocked_req, mock_cloud, _run):
        fake_endpoint = "http://fake.endpoint.com"
        mocked_req.return_value = MockResponse({OTEL_ENDPOINT: fake_endpoint}) if cloud else MockResponse({})
        mock_cloud.return_value = cloud  # Mock plugin running in cloud vs not
        self.plugin.tasks = None  # ensure still no tasks as other tests edit this and could fail before reverting

        plugin_server = PluginServer(self.plugin)  # this plugin has no tasks by default
        plugin_server.start()

        self.assertEqual(plugin_server.config_options, {OTEL_ENDPOINT: fake_endpoint} if cloud else {})

        # Plugin server calls out to CPS when cloud to get tracing endpoint
        self.assertEqual(mocked_req.called, cloud)


    @patch("insightconnect_plugin_runtime.server.request_get")
    def test_cloud_plugin_calls_cps(self, mocked_req, _mock_cloud, _run):
        mocked_req.return_value = MockResponse({"plugins":{self.plugin_name: PLUGIN_VALUE_1, 'plugin': PLUGIN_VALUE_2},
                                                "config": {"interval": 25}})
        self.plugin.tasks = 'fake tasks'  # this plugin by default has no tasks so force it to have some
        plugin_server = PluginServer(self.plugin)
        plugin_server.start()

        # Plugin server should call out to CPS and save the response
        self.assertTrue(mocked_req.called)

        # We only save the plugin config for the current config and ignore `other_plugin`
        self.assertDictEqual(plugin_server.config_options, PLUGIN_VALUE_1)

        self.plugin.tasks = None  # reset tasks value

    @parameterized.expand(
        [
            ["error", HTTPError],
            ["error", Timeout],
            ["unexpected", TooManyRedirects],
            ["Connection refused", ConnectionError],
        ]
    )
    @patch("insightconnect_plugin_runtime.server.request_get")
    @patch("structlog.get_logger")
    @patch(
        "insightconnect_plugin_runtime.server.CPS_RETRY", new=2
    )  # reduce retries in unit tests
    @patch(
        "insightconnect_plugin_runtime.server.RETRY_SLEEP", new=1
    )  # reduce sleep in unit tests
    def test_cps_raises_an_error(self, test_cond, exception, log, mocked_req, _mock_cloud, _run):
        log.return_value = Logger()
        # If we have successfully got config and scheduler options, and later this call fails we should keep values
        mocked_req.return_value = MockResponse({"plugins": {self.plugin_name: PLUGIN_VALUE_1, 'plugin': PLUGIN_VALUE_2},
                                                "config": {"unused_config": "value"}})
        self.plugin.tasks = 'fake tasks'  # this plugin by default has no tasks so force it to have some
        self.plugin.name = "plugin"  # force to use next plugin name from previous test
        plugin_server = PluginServer(self.plugin)
        plugin_server.start()

        self.assertDictEqual(plugin_server.config_options, PLUGIN_VALUE_2)

        if test_cond == "Connection refused":
            mocked_req.side_effect = ConnectionError("Connection Refused")
            plugin_server.get_plugin_properties_from_cps()
            # we log error as info log, as this is likely to be hit when the pod is just starting up
            self.assertIn(test_cond, plugin_server.logger.last_info[-1])

        else:
            # First call has happened and now successful - force to hit specific handled and unexpected errors.
            mocked_req.side_effect = exception("Warning HTTP error returned...")
            plugin_server.get_plugin_properties_from_cps()
            # we log error in all and `unexpected` in TooManyRedirects as there is no direct catch for this
            self.assertIn(test_cond, plugin_server.logger.last_error[-2])

        # Values should not have changed
        self.assertDictEqual(plugin_server.config_options, PLUGIN_VALUE_2)

        # Next schedule returns no configurations for plugins
        mocked_req.return_value = MockResponse({})
        mocked_req.side_effect = None
        plugin_server.get_plugin_properties_from_cps()

        # And this new values are now updated for the plugin server
        self.assertDictEqual(plugin_server.config_options, {})

        self.plugin.tasks = None  # reset tasks value
