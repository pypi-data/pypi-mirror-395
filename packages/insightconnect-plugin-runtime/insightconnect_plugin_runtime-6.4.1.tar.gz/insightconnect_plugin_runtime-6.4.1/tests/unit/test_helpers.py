import pytest
from insightconnect_plugin_runtime import helper
from insightconnect_plugin_runtime.exceptions import (
    HTTPStatusCodes,
    ResponseExceptionData,
    PluginException,
    APIException
)
import requests
import os
from unittest import TestCase
from unittest.mock import patch
from tests.unit.utils import mock_request
from parameterized import parameterized


def test_extract_value_successful():
    result = helper.extract_value(r"\s", "Shell", r":\s(.*)\s", "\nShell: /bin/bash\n")
    assert "/bin/bash" == result


def test_extract_value_failure():
    result = helper.extract_value(r"\s", "Shell", r":\s(.*)\s", "\nShell: /bin/bash\n")
    assert "/bin/bas" != result


def test_extract_no_exceptions():
    helper.extract_value(r"\s", "Shell", r":\s(.*)\s", "\nShell: /bin/bash\n")


# clean_dict


def test_clean_dict_not_equal_successful():
    sample = {"one": None, "two": "", "three": "woohoo"}
    assert sample != helper.clean_dict({"one": None, "two": "", "three": "woohoo"})


def test_clean_dict_equal_successful():
    sample = {"three": "woohoo"}
    assert sample == helper.clean_dict({"one": None, "two": "", "three": "woohoo"})


def test_clean_dict_no_exceptions():
    helper.clean_dict({"test": "yay"})


# clean_list


def test_clean_list_not_equal_successful():
    sample = ["", None, "test"]
    assert sample != helper.clean_list(["", None, "test"])


def test_clean_list_equal_successful():
    sample = ["test"]
    assert sample == helper.clean_list(["", None, "test"])


def test_clean_list_no_exceptions():
    helper.clean_list([])


# clean


def test_clean_not_equal_list_successful():
    sample = ["one", {"two": "", "three": None}, {"four": 4}, None]
    assert sample != helper.clean(
        ["one", {"two": "", "three": None}, {"four": 4}, None]
    )


def test_clean_equal_list_successful():
    sample = ["one", {"two": "", "three": None}, {"four": 4}, None]
    assert ["one", {}, {"four": 4}] == helper.clean(sample)


def test_clean_not_equal_dict_successful():
    sample = {"one": [1, None, "", {"two": None}, {"three": 3}], "four": 4}
    assert sample != helper.clean(
        {"one": [1, None, "", {"two": None}, {"three": 3}], "four": 4}
    )


def test_clean_equal_dict_successful():
    sample = {"one": [1, None, "", {"two": None}, {"three": 3}], "four": 4}
    assert {"one": [1, {}, {"three": 3}], "four": 4} == helper.clean(sample)


def test_clean_no_exceptions():
    helper.clean({"one": [1, None, "", {"two": None}, {"three": 3}], "four": 4})


def test_return_non_empty_successful():
    sample = {
        "test": 1,
        "test2": ["one", "", None],
        "test3": {"test": 1, "test2": "", "test3": None},
        "test4": "",
    }
    assert {
        "test": 1,
        "test2": ["one"],
        "test3": {"test": 1},
    } == helper.return_non_empty(sample)


# convert camel to snake
def test_convert_to_snake_case():
    sample = "letMeBeConverted"
    assert helper.convert_to_snake_case(sample) == "let_me_be_converted"


def test_convert_dict_to_snake_case():
    sample = [{"testMe": 1}, {"testMe2": 2, "testMe3": {"testMe4": 1}}]
    assert helper.convert_dict_to_snake_case(sample) == [
        {"test_me": 1},
        {"test_me2": 2, "test_me3": {"test_me4": 1}},
    ]


# convert snake to camel


def test_convert_to_camel_case():
    sample = "let_me_be_converted"
    assert helper.convert_to_camel_case(sample) == "letMeBeConverted"


def test_convert_dict_to_camel_case():
    sample = [{"test_me": 1}, {"test_me2": 2, "test_me3": {"test_me4": 1}}]
    assert helper.convert_dict_to_camel_case(sample) == [
        {"testMe": 1},
        {"testMe2": 2, "testMe3": {"testMe4": 1}},
    ]


# get_hashes_string


def test_get_hashes_string_equal_successful():
    test_string = "abcdefghijklmnopqrstuvwxyz"

    assert {
        "md5": "c3fcd3d76192e4007dfb496cca67e13b",
        "sha1": "32d10c7b8cf96570ca04ce37f2a19d84240d3a89",
        "sha256": "71c480df93d6ae2f1efad1447c66c9525e316218cf51fc8d9ed832f2daf18b73",
        "sha512": "4dbff86cc2ca1bae1e16468a05cb9881c97f1753bce3619034898faa1aabe429955a1bf8ec483d7421fe3c1646613"
        + "a59ed5441fb0f321389f77f48a879c7b1f1",
    } == helper.get_hashes_string(test_string)


def test_get_hashes_string_not_equal_successful():
    test_string = "abcdefghijklmnopqrstuvwxyz"
    assert {
        "sha1": "32d10c7b8cf96570ca04ce37f2a19d84240d3a89",
        "sha256": "71c480df93d6ae2f1efad1447c66c9525e316218cf51fc8d9ed832f2daf18b73",
        "sha512": "4dbff86cc2ca1bae1e16468a05cb9881c97f1753bce3619034898faa1aabe429955a1bf8ec483d7421fe3c1646613"
        + "a59ed5441fb0f321389f77f48a879c7b1f1",
    } != helper.get_hashes_string(test_string)


def test_get_hashes_string_no_exceptions():
    test_string = "abcdefghijklmnopqrstuvwxyz"
    helper.get_hashes_string(test_string)


def test_get_hashes_string_all_keys_present():
    test_string = "abcdefghijklmnopqrstuvwxyz"
    expected_keys = {"md5", "sha1", "sha256", "sha512"}

    hashes = set(helper.get_hashes_string(test_string))
    has_all_keys = len(expected_keys.difference(hashes)) == 0

    assert has_all_keys


# check_hashes


def test_check_hashes_true_md5_success():
    test_string = "abcdefghijklmnopqrstuvwxyz"
    assert helper.check_hashes(test_string, "c3fcd3d76192e4007dfb496cca67e13b")


def test_check_hashes_false_md5_failure():
    test_string = "abcdefghijklmnopqrstuvwxyz"
    assert not helper.check_hashes(test_string, "c3fcd3d76192asdfasdfasdf67e13z")


def test_check_hashes_true_sha1_success():
    test_string = "abcdefghijklmnopqrstuvwxyz"
    assert helper.check_hashes(test_string, "32d10c7b8cf96570ca04ce37f2a19d84240d3a89")


def test_check_hashes_false_sha1_failure():
    test_string = "abcdefghijklmnopqrstuvwxyz"
    assert not helper.check_hashes(
        test_string, "32d10c7b8cf96570ca04ce37f2a19d84240d3aasdf"
    )


def test_check_hashes_true_sha256_success():
    test_string = "abcdefghijklmnopqrstuvwxyz"
    assert helper.check_hashes(
        test_string, "71c480df93d6ae2f1efad1447c66c9525e316218cf51fc8d9ed832f2daf18b73"
    )


def test_check_hashes_false_sha256_failure():
    test_string = "abcdefghijklmnopqrstuvwxyz"
    assert not helper.check_hashes(
        test_string,
        "71c480df93d6ae2f1efad1447c66c9525e316218cf51fc8d9ed832f2dafasdfasdf",
    )


def test_check_hashes_true_sha512_success():
    test_string = "abcdefghijklmnopqrstuvwxyz"
    assert helper.check_hashes(
        test_string,
        "4dbff86cc2ca1bae1e16468a05cb9881c97f1753bce3619034898faa1aabe429955a1bf8ec483d7421fe3c1646613a59ed5441fb"
        + "0f321389f77f48a879c7b1f1",
    )


def test_check_hashes_false_sha512_failure():
    test_string = "abcdefghijklmnopqrstuvwxyz"
    assert not helper.check_hashes(
        test_string,
        "4dbff86cc2ca1bae1e16468a05cb9881c97f1753bce3619034898faa1aabe429955a1bf8ec483d7421fe3c1646613a59ed5441fb"
        + "0f32138asdfasdf",
    )


# open_url


# We can't reliably test known responses against dynamic responses from an endpoint we don't control,
# so this is the best we can do (to verify Python 2/3 compatibility)
def test_open_url_no_exceptions():
    response = helper.open_url(url="https://api.ipify.org?format=json")
    assert response is not None


# check_url


def test_check_url_success():
    assert helper.check_url("https://google.com")


def test_check_url_exception():
    with pytest.raises(requests.exceptions.InvalidURL):
        helper.check_url("http:google.com")


# exec_command


def test_exec_command_success():
    result = helper.exec_command("ls")
    expected_keys = {"stdout", "rcode", "stderr"}
    set_diff = expected_keys.difference(set(result))
    has_keys = len(set_diff) == 0
    assert has_keys


def test_exec_command_pipe_failure():
    result = helper.exec_command("ls -lrt|grep test")
    has_error = result["stderr"] != ""
    assert has_error


def test_exec_command_append_failure():
    result = helper.exec_command("ls -lrt >> outfile.log")
    has_error = result["stderr"] != ""
    assert has_error


# encode_string


def test_encode_string():
    sample = "hello world"
    expected = b"aGVsbG8gd29ybGQ="

    encoded = helper.encode_string(sample)

    assert expected == encoded


def test_encode_file_success():
    expected = b"a29tYW5kIGlzIGF3ZXNvbWU="

    f = open("test.txt", "w+")
    f.write("komand is awesome")
    f.close()

    actual = helper.encode_file("./test.txt")
    assert expected == actual

    os.remove("test.txt")


# get_url_content_disposition


def test_get_url_content_disposition_success():
    headers = {
        "Content-Type": "text/html; charset=utf-8",
        "Content-Disposition": "attachment; filename=test.html",
        "Content-Length": 22,
    }

    assert "test.html" == helper.get_url_content_disposition(headers)


class TestRequestsHelpers(TestCase):
    def test_response_handler(self):
        response = requests.Response()
        response._content = (
            b'{"message": "Unauthorized", "error": "invalid_credentials"}'
        )
        response.url = "https://example.com"
        response.reason = "UNAUTHORIZED"
        response.status_code = 401
        response.headers["Content-Type"] = "application/json"
        custom_configs = {
            HTTPStatusCodes.UNAUTHORIZED: PluginException(
                cause="Unauthorized custom", assistance="Check permissions custom"
            )
        }
        response = helper.response_handler(
            response, custom_configs, ResponseExceptionData.RESPONSE_JSON, [401]
        )
        self.assertEqual(response, None)

    def test_response_handler_error(self):
        response = requests.Response()
        response._content = (
            b'{"message": "Unauthorized", "error": "invalid_credentials"}'
        )
        response.url = "https://example.com"
        response.reason = "UNAUTHORIZED"
        response.status_code = 401
        response.headers["Content-Type"] = "application/json"
        custom_configs = {
            HTTPStatusCodes.UNAUTHORIZED: PluginException(
                cause="Unauthorized custom", assistance="Check permissions custom"
            )
        }
        with self.assertRaises(PluginException) as assertion:
            helper.response_handler(
                response, custom_configs, ResponseExceptionData.RESPONSE_JSON
            )
        self.assertEqual(
            assertion.exception.cause,
            "Unauthorized custom",
        )
        self.assertEqual(
            assertion.exception.assistance,
            "Check permissions custom",
        )
        self.assertEqual(
            assertion.exception.data,
            {"message": "Unauthorized", "error": "invalid_credentials"},
        )

    @patch("requests.Session.send", side_effect=mock_request)
    def test_make_request(self, mock_request):
        request = requests.Request(
            method="GET",
            url="https://example.com/success",
            params={"sample": "value"},
            data={"sample": "value"},
            json={"sample": "value"},
            headers={"Content-Type": "application/json"},
        )
        response = helper.make_request(_request=request, stream=True, max_response_size=100)
        expected = {
            "json": {"example": "sample"},
            "status_code": 200,
            "content": b"example",
            "url": "https://example.com/success",
            "content-length": "1",
        }
        self.assertEqual(response.content, expected.get("content"))
        self.assertEqual(response.status_code, expected.get("status_code"))
        self.assertEqual(response.url, expected.get("url"))
        self.assertEqual(response.headers.get("content-length"), expected.get("content-length"))

    @patch("requests.Session.send")
    def test_make_request_enforces_max_response_size(self, mocked_request):
        returned_max_size, test_max_size = "5000", 1527

        response = requests.Response()
        response.headers = {"content-length": returned_max_size, "content-type": "application/json"}
        mocked_request.return_value = response

        test_request = requests.Request(method="GET", url="https://event_source.com/api/v1/logs")

        with self.assertRaises(APIException) as api_err:
            helper.make_request(_request=test_request, stream=True, max_response_size=test_max_size)

        self.assertEqual(400, api_err.exception.status_code)
        exp_err_cause = f"API response is exceeding allowed limit of {test_max_size} bytes."
        exp_err_data = f"Content length returned was {returned_max_size} and max allowed is {test_max_size}"
        self.assertEqual(400, api_err.exception.status_code)
        self.assertEqual(exp_err_cause, api_err.exception.cause)
        self.assertEqual(exp_err_data, api_err.exception.data)


    @parameterized.expand(
        [
            ["401", "GET", "https://example.com/401", {}, PluginException],
            [
                "timeout",
                "GET",
                "https://example.com/timeout",
                {},
                requests.exceptions.Timeout,
            ],
            [
                "connectionerror",
                "GET",
                "https://example.com/connectionerror",
                {},
                requests.exceptions.ConnectionError,
            ],
            [
                "toomanyredirects",
                "GET",
                "https://example.com/toomanyredirects",
                {},
                requests.exceptions.TooManyRedirects,
            ],
            [
                "unknownerror",
                "GET",
                "https://example.com/unknownerror",
                {},
                PluginException,
            ],
            [
                "custom404",
                "GET",
                "https://example.com/404",
                {
                    404: PluginException(
                        cause="CustomCause", assistance="CustomAssistance"
                    )
                },
                PluginException,
            ],
        ]
    )
    @patch("requests.Session.send", side_effect=mock_request)
    def test_make_request_error_handling(
        self, test_name, method, url, exp_config, exception_type, mock_request
    ):
        request = requests.Request(method=method, url=url, json=None)
        with self.assertRaises(PluginException) as error:
            helper.make_request(
                _request=request,
                exception_custom_configs=exp_config,
                exception_data_location=ResponseExceptionData.RESPONSE,
            )
        assert (isinstance(error, exception_type), True)
        if test_name == "custom404":
            self.assertEqual(
                error.exception.cause,
                "CustomCause",
            )
            self.assertEqual(
                error.exception.assistance,
                "CustomAssistance",
            )
            self.assertEqual(error.exception.data.text, "example")
            self.assertEqual(error.exception.data.status_code, 404)

    @parameterized.expand(
        [
            ["401", "https://example.com/401", PluginException],
            [
                "timeout",
                "https://example.com/timeout",
                requests.exceptions.Timeout,
            ],
            [
                "connectionerror",
                "https://example.com/connectionerror",
                requests.exceptions.ConnectionError,
            ],
            [
                "toomanyredirects",
                "https://example.com/toomanyredirects",
                requests.exceptions.TooManyRedirects,
            ],
            [
                "unknownerror",
                "https://example.com/unknownerror",
                PluginException,
            ],
        ]
    )
    @patch("requests.request", side_effect=mock_request)
    def test_request_error_handling(self, test_name, url, exception_type, mock_request):
        @helper.request_error_handling()
        def dummy_request(self):
            response = requests.request("GET", url)
            response.raise_for_status()

        with self.assertRaises(PluginException) as error:
            dummy_request(self)
        assert (isinstance(error, exception_type), True)

    def test_extract_json(self):
        with self.assertRaises(PluginException) as error:
            response = requests.Response()
            response._content = (
                b'{"message": "Unauthorized", "error": "invalid_credentials'
            )
            response.url = "https://example.com"
            response.reason = "UNAUTHORIZED"
            response.status_code = 401
            response.headers["Content-Type"] = "application/json"
            helper.extract_json(response)
        assert (isinstance(error, PluginException), True)
        self.assertEqual(
            error.exception.cause, "Received an unexpected response from the server."
        )


class TestHashing(TestCase):
    def setUp(self) -> None:
        self.log = {"example": "value", "sample": "value"}

    def test_hash_sha1_no_keys(self):
        # Test hash with no keys provided
        expected_hash = "2e1ccc1a95e9b2044f13546c25fe380bbd039293"
        self.assertEqual(helper.hash_sha1(self.log), expected_hash)

    def test_hash_sha1_keys(self):
        # Test hash with valid key provided
        expected_hash = "61c908e52d66a763ceed0798b8e5f4b7f0328a21"
        self.assertEqual(helper.hash_sha1(self.log, keys=["example"]), expected_hash)

    def test_hash_sha1_keys_wrong_type(self):
        # Test hash with wrong type for keys
        with self.assertRaises(TypeError) as context:
            helper.hash_sha1(self.log, keys="test")

        self.assertEqual(
            str(context.exception),
            "The 'keys' parameter must be a list or None in the 'hash_sha1' function, not str"
        )

    def test_hash_sha1_keys_not_found(self):
        # Test hash with key not found
        with self.assertRaises(KeyError) as context:
            helper.hash_sha1(self.log, keys=["example", "test"])

        self.assertEqual(str(context.exception), "\"Key 'test' not found in the provided log.\"")

    def test_compare_and_dedupe_hashes(self):
        hashes = ["2e1ccc1a95e9b2044f13546c25fe380bbd039293"]
        logs = [
            {
                "example": "value",
                "sample": "value",
            },
            {"specimen": "new_value"},
        ]
        assert [{"specimen": "new_value"}], [
            "ad6ae80c0356e02b1561cb58408ee678eb1070bb"
        ] == helper.compare_and_dedupe_hashes(hashes, logs)
