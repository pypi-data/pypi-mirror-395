from insightconnect_plugin_runtime.exceptions import PluginException, APIException
from unittest import TestCase


class TestExceptions(TestCase):
    def test_exceptions(self):
        exception_data = [
            {
                "preset": PluginException.Preset.API_KEY,
                "expected_cause": "Invalid API key provided.",
                "expected_assistance": "Verify your API key configured in your connection is correct.",
            },
            {
                "preset": PluginException.Preset.UNAUTHORIZED,
                "expected_cause": "The account configured in your connection is unauthorized to access this service.",
                "expected_assistance": "Verify the permissions for your account and try again.",
            },
            {
                "preset": PluginException.Preset.RATE_LIMIT,
                "expected_cause": "The account configured in your plugin connection is currently rate-limited.",
                "expected_assistance": "Adjust the time between requests if possible.",
            },
            {
                "preset": PluginException.Preset.USERNAME_PASSWORD,
                "expected_cause": "Invalid username or password provided.",
                "expected_assistance": "Verify your username and password are correct.",
            },
            {
                "preset": PluginException.Preset.NOT_FOUND,
                "expected_cause": "Invalid or unreachable endpoint provided.",
                "expected_assistance": "Verify the URLs or endpoints in your configuration are correct.",
            },
            {
                "preset": PluginException.Preset.SERVER_ERROR,
                "expected_cause": "Server error occurred",
                "expected_assistance": "Verify your plugin connection inputs are correct and not malformed and try again."
                " If the issue persists, please contact support.",
            },
            {
                "preset": PluginException.Preset.SERVICE_UNAVAILABLE,
                "expected_cause": "The service is currently unavailable.",
                "expected_assistance": "Try again later. If the issue persists, please contact support.",
            },
            {
                "preset": PluginException.Preset.INVALID_JSON,
                "expected_cause": "Received an unexpected response from the server.",
                "expected_assistance": "(non-JSON or no response was received).",
            },
            {
                "preset": PluginException.Preset.UNKNOWN,
                "expected_cause": "Something unexpected occurred.",
                "expected_assistance": "Check the logs and if the issue persists please contact support.",
            },
            {
                "preset": PluginException.Preset.BASE64_ENCODE,
                "expected_cause": "Unable to base64 encode content due to incorrect padding length.",
                "expected_assistance": "This is likely a programming error, if the issue persists please contact support.",
            },
            {
                "preset": PluginException.Preset.BASE64_DECODE,
                "expected_cause": "Unable to base64 decode content due to incorrect padding length.",
                "expected_assistance": "This is likely a programming error, if the issue persists please contact support.",
            },
            {
                "preset": PluginException.Preset.TIMEOUT,
                "expected_cause": "The connection timed out.",
                "expected_assistance": "This is likely a network error. "
                "Verify the network activity. If the issue persists, please contact support.",
            },
            {
                "preset": PluginException.Preset.BAD_REQUEST,
                "expected_cause": "The server is unable to process the request.",
                "expected_assistance": "Verify your plugin input is correct and not malformed and try again. "
                "If the issue persists, please contact support.",
            },
            {
                "preset": PluginException.Preset.INVALID_CREDENTIALS,
                "expected_cause": "Authentication failed: invalid credentials.",
                "expected_assistance": "Please verify the credentials for your account and try again.",
            },
        ]

        for test_data in exception_data:
            with self.assertRaises(PluginException) as context:
                raise (PluginException(preset=test_data.get("preset")))
            assert context.exception.cause == test_data.get("expected_cause")
            assert context.exception.assistance == test_data.get("expected_assistance")

    def test_api_exception(self):
        with self.assertRaises(APIException) as context:
            raise (
                APIException(
                    preset=PluginException.Preset.NOT_FOUND,
                    status_code=404,
                    data="example",
                )
            )
        assert context.exception.cause == "Invalid or unreachable endpoint provided."
        assert (
            context.exception.assistance
            == "Verify the URLs or endpoints in your configuration are correct."
        )
        assert context.exception.data == "example"
        assert context.exception.status_code == 404
