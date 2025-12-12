import unittest
from unittest import mock
from unittest.mock import Mock

from insightconnect_plugin_runtime.clients.oauth import (
    OAuth20ClientCredentialMixin,
    OAuth20ClientMessages,
)
from insightconnect_plugin_runtime.exceptions import PluginException


class ExampleApiClass(OAuth20ClientCredentialMixin):
    def __init__(self, client_id: str, client_secret: str, token_url: str) -> None:
        super().__init__(client_id, client_secret, token_url)


STUB_OAUTH_CLIENT_CREDENTIALS = {
    "client_id": "ExampleID",
    "client_secret": "ExampleSecret",
    "token_url": "https://example.com",
}


class TestOAuth2(unittest.TestCase):
    @mock.patch("requests.Session.request")
    @mock.patch(
        "oauthlib.oauth2.BackendApplicationClient.parse_request_body_response",
        return_value="ExampleToken",
    )
    def setUp(self, mock_request: Mock, mock_backend: Mock) -> None:
        self.client = ExampleApiClass(**STUB_OAUTH_CLIENT_CREDENTIALS)

    @mock.patch("requests_oauthlib.OAuth2Session.fetch_token")
    def test_fetch_token(self, mock_fetch_token: Mock) -> None:
        self.client.auth_token()
        mock_fetch_token.assert_called_once()
        mock_fetch_token.assert_called_with(**STUB_OAUTH_CLIENT_CREDENTIALS)

    @mock.patch("requests_oauthlib.OAuth2Session.fetch_token")
    def test_fetch_token_on_object_create(self, mock_fetch_token: Mock) -> None:
        ExampleApiClass(**STUB_OAUTH_CLIENT_CREDENTIALS)
        mock_fetch_token.assert_called_once()
        mock_fetch_token.assert_called_with(**STUB_OAUTH_CLIENT_CREDENTIALS)

    @mock.patch("requests_oauthlib.OAuth2Session.request")
    def test_fetch_token_exception(self, mock_request: Mock) -> None:
        with self.assertRaises(PluginException) as context:
            ExampleApiClass(**STUB_OAUTH_CLIENT_CREDENTIALS)
        self.assertEqual(
            context.exception.cause, OAuth20ClientMessages.PLUGIN_EXCEPTION_CAUSE
        )
        self.assertEqual(
            context.exception.assistance,
            OAuth20ClientMessages.PLUGIN_EXCEPTION_ASSISTANCE,
        )
