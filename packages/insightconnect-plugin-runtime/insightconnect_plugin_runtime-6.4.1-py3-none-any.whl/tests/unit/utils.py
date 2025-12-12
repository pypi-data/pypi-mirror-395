import requests


class MockResponse:
    """Mocked response from CPS"""

    def __init__(self, value):
        self.json_value = value

    def json(self):
        return self.json_value


class Logger:
    """Mocked logger to easily find last log triggered from SDK server."""

    def __init__(self):
        self.last_error = []
        self.last_info = []

    def info(self, log: str):
        self.last_info.append(log)

    def error(self, log: str):
        self.last_error.append(log)


def get_mock_response(
    status_code: int, url: str, reason: str, content: str = None, data: dict = {}
):
    response = requests.Response()
    response.status_code = status_code
    bytes_string = content.encode("utf-8")
    response._content = bytes_string
    response.url = url
    response.reason = reason
    response.headers = {"content-length": "1", "content-type": "application/json"}

    def return_json():
        return data

    response.json = return_json
    return response


def mock_request(*args, **kwargs):
    if isinstance(args[0], requests.PreparedRequest):
        url = args[0].url
    else:
        url = args[1]
    if url == "https://example.com/success?sample=value":
        return get_mock_response(
            200, "https://example.com/success", None, "example", {"example": "sample"}
        )
    if url == "https://example.com/401":
        return get_mock_response(
            401,
            "https://example.com/401",
            "UNAUTHORIZED",
            "example",
            {"example": "sample"},
        )
    if url == "https://example.com/404":
        return get_mock_response(
            404,
            "https://example.com/404",
            "NOT_FOUND",
            "example",
            {"example": "sample"},
        )
    if url == "https://example.com/timeout":
        raise requests.exceptions.Timeout()
    if url == "https://example.com/connectionerror":
        raise requests.exceptions.ConnectionError()
    if url == "https://example.com/toomanyredirects":
        raise requests.exceptions.TooManyRedirects()
    if url == "https://example.com/unknownerror":
        raise requests.exceptions.ContentDecodingError
    raise NotImplementedError("Not implemented")
