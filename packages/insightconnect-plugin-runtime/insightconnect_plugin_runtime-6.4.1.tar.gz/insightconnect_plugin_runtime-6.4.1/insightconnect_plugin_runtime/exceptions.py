# -*- coding: utf-8 -*-
class ResponseExceptionData:
    RESPONSE_TEXT = "response_text"
    RESPONSE_JSON = "response_json"
    RESPONSE = "response"
    EXCEPTION = "exception"


class HTTPStatusCodes:

    # 4xx Client Errors
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    PAYMENT_REQUIRED = 402
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    NOT_ACCEPTABLE = 406
    PROXY_AUTHENTICATION_REQUIRED = 407
    REQUEST_TIMEOUT = 408
    CONFLICT = 409
    GONE = 410
    LENGTH_REQUIRED = 411
    PRECONDITION_FAILED = 412
    PAYLOAD_TOO_LARGE = 413
    URI_TOO_LONG = 414
    UNSUPPORTED_MEDIA_TYPE = 415
    RANGE_NOT_SATISFIABLE = 416
    EXPECTATION_FAILED = 417
    I_AM_A_TEAPOT = 418
    MISDIRECTED_REQUEST = 421
    UNPROCESSABLE_ENTITY = 422
    LOCKED = 423
    FAILED_DEPENDENCY = 424
    TOO_EARLY = 425
    UPGRADE_REQUIRED = 426
    PRECONDITION_REQUIRED = 428
    TOO_MANY_REQUESTS = 429
    REQUEST_HEADER_FIELDS_TOO_LARGE = 431
    UNAVAILABLE_FOR_LEGAL_REASONS = 451

    # 5xx Server Errors
    INTERNAL_SERVER_ERROR = 500
    NOT_IMPLEMENTED = 501
    BAD_GATEWAY = 502
    SERVICE_UNAVAILABLE = 503
    GATEWAY_TIMEOUT = 504
    HTTP_VERSION_NOT_SUPPORTED = 505
    VARIANT_ALSO_NEGOTIATES = 506
    INSUFFICIENT_STORAGE = 507
    LOOP_DETECTED = 508
    NOT_EXTENDED = 510
    NETWORK_AUTHENTICATION_REQUIRED = 511


class ClientException(Exception):
    """
    An exception which marks an error made by the plugin invoker.

    Some examples of when to use this are:
    - Malformed/Incorrect input data
    - External HTTP server throws a 400 level error

    """

    pass


class ServerException(Exception):
    """
    An Exception which marks an error made by an external server.

    Some examples of when to use this are:
    - External server throws a 500 Error

    """

    pass


class LoggedException(Exception):
    """
    An Exception which holds the step output dictionary.
    """

    def __init__(self, ex, output):
        super(LoggedException, self).__init__(ex)
        self.ex = ex
        self.output = output


class ConnectionTestException(Exception):
    """
    An Exception which marks an error that occurred during a connection test.

    This Exception provides a method for consistent and well-handled error messaging.
    """

    class Preset(object):
        """
        Constants available for use as preset arguments to the initializer
        """

        API_KEY = "api_key"
        UNAUTHORIZED = "unauthorized"
        RATE_LIMIT = "rate_limit"
        USERNAME_PASSWORD = "username_password"
        NOT_FOUND = "not_found"
        SERVER_ERROR = "server_error"
        SERVICE_UNAVAILABLE = "service_unavailable"
        INVALID_JSON = "invalid_json"
        UNKNOWN = "unknown"
        BASE64_ENCODE = "base64_encode"
        BASE64_DECODE = "base64_decode"
        TIMEOUT = "timeout"
        BAD_REQUEST = "bad_request"
        INVALID_CREDENTIALS = "invalid_credentials"
        METHOD_NOT_ALLOWED = "method_not_allowed"
        CONFLICT = "conflict"
        CONNECTION_ERROR = "connection_error"
        REDIRECT_ERROR = "redirect_error"

    # Dictionary of cause messages
    causes = {
        Preset.API_KEY: "Invalid API key provided.",
        Preset.UNAUTHORIZED: "The account configured in your connection is unauthorized to access this service.",
        Preset.RATE_LIMIT: "The account configured in your plugin connection is currently rate-limited.",
        Preset.USERNAME_PASSWORD: "Invalid username or password provided.",
        Preset.NOT_FOUND: "Invalid or unreachable endpoint provided.",
        Preset.SERVER_ERROR: "Server error occurred",
        Preset.SERVICE_UNAVAILABLE: "The service is currently unavailable.",
        Preset.INVALID_JSON: "Received an unexpected response from the server.",
        Preset.UNKNOWN: "Something unexpected occurred.",
        Preset.BASE64_ENCODE: "Unable to base64 encode content due to incorrect padding length.",
        Preset.BASE64_DECODE: "Unable to base64 decode content due to incorrect padding length.",
        Preset.TIMEOUT: "The connection timed out.",
        Preset.BAD_REQUEST: "The server is unable to process the request.",
        Preset.INVALID_CREDENTIALS: "Authentication failed: invalid credentials.",
        Preset.METHOD_NOT_ALLOWED: "The request method is not allowed for this resource.",
        Preset.CONFLICT: "Request cannot be completed due to a conflict with the current state of the resource.",
        Preset.CONNECTION_ERROR: "Failed to connect to the server.",
        Preset.REDIRECT_ERROR: "Request redirected more than the set limit for the server.",
    }

    # Dictionary of assistance/remediation messages
    assistances = {
        Preset.API_KEY: "Verify your API key configured in your connection is correct.",
        Preset.UNAUTHORIZED: "Verify the permissions for your account and try again.",
        Preset.RATE_LIMIT: "Adjust the time between requests if possible.",
        Preset.USERNAME_PASSWORD: "Verify your username and password are correct.",
        Preset.NOT_FOUND: "Verify the URLs or endpoints in your configuration are correct.",
        Preset.SERVER_ERROR: "Verify your plugin connection inputs are correct and not malformed and try again. "
        "If the issue persists, please contact support.",
        Preset.SERVICE_UNAVAILABLE: "Try again later. If the issue persists, please contact support.",
        Preset.INVALID_JSON: "(non-JSON or no response was received).",
        Preset.UNKNOWN: "Check the logs and if the issue persists please contact support.",
        Preset.BASE64_ENCODE: "This is likely a programming error, if the issue persists please contact support.",
        Preset.BASE64_DECODE: "This is likely a programming error, if the issue persists please contact support.",
        Preset.TIMEOUT: "This is likely a network error. "
        "Verify the network activity. If the issue persists, please contact support.",
        Preset.BAD_REQUEST: "Verify your plugin input is correct and not malformed and try again. "
        "If the issue persists, please contact support.",
        Preset.INVALID_CREDENTIALS: "Please verify the credentials for your account and try again.",
        Preset.METHOD_NOT_ALLOWED: "Please try a supported method for this resource.",
        Preset.CONFLICT: "Please check your request, and try again.",
        Preset.CONNECTION_ERROR: "Please check your network connection and try again.",
        Preset.REDIRECT_ERROR: "Please check your request and try again.",
    }

    def __init__(self, cause=None, assistance=None, data=None, preset=None):
        """
        Initializes a new ConnectionTestException. User must supply all punctuation/grammar.
        :param cause: Cause of the error. Leave empty if using preset.
        :param assistance: Possible remediation steps for the error. Leave empty if using preset.
        :param data: Possible response data related to the error.
        :param preset: Preset error and remediation steps to use.
        """

        self.preset = preset

        if preset:
            self.cause, self.assistance = self.causes[preset], self.assistances[preset]
        else:
            self.cause = cause if cause else ""
            self.assistance = assistance if assistance else ""

        self.data = str(data) if data else ""

    def __str__(self):
        str_rep = f"Connection test failed! {self.cause} {self.assistance}"
        if self.data:
            str_rep += f" Response was: {self.data}"
        return str_rep


class PluginException(ConnectionTestException):
    def __str__(self):
        str_repr = f"An error occurred during plugin execution! {self.cause} {self.assistance}"
        if self.data:
            str_repr += f" Response was {self.data}"
        return str_repr


class APIException(PluginException):
    def __init__(self, cause=None, assistance=None, data=None, preset=None, status_code=None):
        super().__init__(cause, assistance, data, preset)
        self.status_code = status_code
