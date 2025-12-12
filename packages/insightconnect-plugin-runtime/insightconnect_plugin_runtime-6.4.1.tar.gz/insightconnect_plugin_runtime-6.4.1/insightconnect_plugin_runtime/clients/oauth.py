from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from insightconnect_plugin_runtime.exceptions import PluginException
from typing import Dict, Any


class OAuth20ClientMessages:
    PLUGIN_EXCEPTION_CAUSE = (
        "An unexpected error occurred while obtaining the OAuth token."
    )
    PLUGIN_EXCEPTION_ASSISTANCE = (
        "Please make sure the information you provide is correct."
    )


class OAuth20ClientCredentialMixin:
    """
    The class enables the use of oauth credential flow to obtain an authorization token for sent requests. To do
    this, inherit the used API Client from this class, and then use self.oauth.request instead of the requests module

    Example:
    Instead of requests.request("GET", ...) -> self.oauth.request("GET", ...)
    """

    def __init__(
        self, client_id: str, client_secret: str, token_url: str, **kwargs
    ) -> None:
        """
        Constructor method

        :param client_id: Client identifier required for OAuthSession
        :type client_id: str

        :param client_secret: Client Secret Key required to obtain the Authorization token
        :type client_secret: str

        :param token_url: Endpoint URL that allows you to obtain an authorization token
        :type token_url: str
        """

        client = BackendApplicationClient(client_id=client_id)
        self.oauth = OAuth2Session(client=client)
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_url = token_url
        self.kwargs = kwargs
        self.token = {}
        self._refresh_token()

    @property
    def auth_token(self) -> Dict[str, Any]:
        """
        The property allows you to refresh, and obtain the token dictionary
        """

        self._refresh_token()
        return self.token

    def _refresh_token(self) -> None:
        """
        Method allows to fetch the token
        """

        try:
            self.token = self.oauth.fetch_token(
                token_url=self.token_url,
                client_id=self.client_id,
                client_secret=self.client_secret,
                **self.kwargs
            )
        except Exception as error:
            raise PluginException(
                cause=OAuth20ClientMessages.PLUGIN_EXCEPTION_CAUSE,
                assistance=OAuth20ClientMessages.PLUGIN_EXCEPTION_ASSISTANCE,
                data=error,
            )
