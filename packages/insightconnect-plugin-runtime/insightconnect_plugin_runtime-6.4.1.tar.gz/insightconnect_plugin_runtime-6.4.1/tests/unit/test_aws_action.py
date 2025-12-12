import datetime
import io
import json
import unittest
import unittest.mock
from os import environ
from pathlib import Path

import botocore.exceptions as be
import botocore.response as br
from parameterized import parameterized

from insightconnect_plugin_runtime import Input, Output, Connection
from insightconnect_plugin_runtime.clients.aws_client import AWSAction, ActionHelper, PaginationHelper
from insightconnect_plugin_runtime.exceptions import PluginException


def raise_attribiute_error(arg1, arg2):
    raise AttributeError()


class Boto3Stub:
    def assume_role(self, *args, **kwargs):
        return {
            "Credentials": {
                "AccessKeyId": "123",
                "SecretAccessKey": "456",
                "SessionToken": "token",
            }
        }

    def close(self):
        # stub for closing the sts client after assuming the role
        pass


class TestAwsAction(unittest.TestCase):
    def setUp(self) -> None:
        self.auth_params = {
            "aws_access_key_id": "123",
            "aws_secret_access_key": "321",
        }
        self.region = "us-east"

        self.assume_role_params = {
            "role_arn": "test_role",
            "external_id": "test_id",
            "region": "test-region",
        }

        self.aws_action = AWSAction(
            "NewAction", "Description", None, None, "ec2", "service"
        )
        self.aws_action.connection = unittest.mock.create_autospec(Connection)
        self.aws_action.connection.helper = unittest.mock.create_autospec(ActionHelper)
        self.aws_action.input = Input({})
        self.aws_action.output = Output({})

    @unittest.mock.patch("boto3.client", return_value=Boto3Stub())
    def test_assume_role(self, mock_sts_client):
        AWSAction.try_to_assume_role("ec2", self.assume_role_params, self.auth_params)

        self.assertEqual(mock_sts_client.call_count, 2)  # twice for assume role and create client afterwards

    @unittest.mock.patch("botocore.session.Session", return_value=unittest.mock.Mock())
    @unittest.mock.patch("boto3.client", return_value=Boto3Stub())
    def test_assume_role_without_role_arn(self, mock_session, mock_sts_client):
        assume_role_params = {"role_arn": "", "external_id": "", "region": ""}
        aws_session = unittest.mock.Mock()

        if assume_role_params.get("role_arn"):
            AWSAction.try_to_assume_role("ec2", assume_role_params, self.auth_params)

        mock_sts_client.assert_not_called()

    @unittest.mock.patch("botocore.session.Session", return_value=unittest.mock.Mock())
    @unittest.mock.patch("boto3.client", return_value=Boto3Stub())
    def test_run_action(self, mock_session, mock_sts_client):
        client_function = getattr(mock_session, "service")
        self.aws_action.handle_rest_call(client_function, {})

        client_function.assert_called_once()
        self.aws_action.connection.helper.format_input.assert_called_once()
        self.aws_action.connection.helper.format_output.assert_called_once()

    @unittest.mock.patch("botocore.session.Session", return_value=unittest.mock.Mock())
    @unittest.mock.patch("boto3.client", return_value=Boto3Stub())
    def test_run_action_pagination(self, mock_session, mock_sts_client):
        """
        Test when max_pages attribute is on the pagination_helper that the response is not cleaned
        allowing the two tokens (next_continuation_token & contination_token) to be returned.
        """
        client_function = getattr(mock_session, "service")
        # Mock connection as we're calling action.run() in this unit test
        self.aws_action.connection.assume_role_params = {}
        self.aws_action.connection.auth_params = {}
        self.aws_action.connection.client = {}

        self.aws_action.pagination_helper = unittest.mock.create_autospec(PaginationHelper)
        self.aws_action.connection.client = mock_session

        # First run has no pagination set so we clean the response
        self.aws_action.pagination_helper.max_pages = None
        self.aws_action.run()

        client_function.assert_called_once()
        self.aws_action.connection.helper.format_input.assert_called_once()
        self.aws_action.connection.helper.format_output.assert_called_once()
        self.aws_action.pagination_helper.remove_keys.assert_called_once()

        # Call again with max_pages set and this means remove_keys is not called
        self.aws_action.pagination_helper.max_pages = 1
        self.aws_action.pagination_helper.remove_keys.reset_mock()
        self.aws_action.run()
        self.aws_action.pagination_helper.remove_keys.assert_not_called()

    def _mock_call_raise_endpoint_connection_error(self):
        raise be.EndpointConnectionError(**{"endpoint_url": "test_url"})

    def test_handle_rest_call_endpoint_connection_error(self):
        with self.assertRaises(PluginException):
            mock_call = self._mock_call_raise_endpoint_connection_error
            self.aws_action.handle_rest_call(mock_call, {})

    def _mock_call_raise_param_validation_error(self):
        raise be.ParamValidationError(**{"endpoint_url": "test_url"})

    def test_handle_rest_call_param_validation_error(self):
        with self.assertRaises(PluginException):
            mock_call = self._mock_call_raise_param_validation_error
            self.aws_action.handle_rest_call(mock_call, {})

    def _mock_call_raise_client_error(self):
        raise be.ClientError(**{"endpoint_url": "test_url"})

    def test_handle_rest_call_client_error(self):
        mock_call = self._mock_call_raise_client_error
        with self.assertRaises(PluginException):
            self.aws_action.handle_rest_call(mock_call, {})

    @unittest.mock.patch.dict(environ, {"PLUGIN_RUNTIME_ENVIRONMENT": "orchestrator"})
    @unittest.mock.patch.object(AWSAction, "handle_rest_call", return_value={"mock_key": "mock_value"})
    def test_run_client_non_cloud_mode_in_action_default_behaviour(self, _mock_handle_rest_call):
        # Test AWSAction called for customers running on an orchestrator that their client can remain open
        aws_action = AWSAction("NewAction", "Description", None, None, "s3", "service")
        aws_action.connection = unittest.mock.create_autospec(Connection)
        aws_action.connection.assume_role_params = self.assume_role_params
        aws_action.connection.auth_params = self.auth_params
        aws_action.connection.client = unittest.mock.create_autospec(Boto3Stub)
        aws_action.connection.client.service = unittest.mock.MagicMock()
        aws_action.run()
        aws_action.connection.client.close.assert_not_called()

    @unittest.mock.patch.dict(environ, {"PLUGIN_RUNTIME_ENVIRONMENT": "cloud"})
    @unittest.mock.patch.object(AWSAction, "handle_rest_call", return_value={"mock_key": "mock_value"})
    def test_run_client_cloud_mode_in_normal_action(self, _mock_handle_rest_call):
        # Test the same AWSAction as above but now running in cloud - we should close this client
        aws_action = AWSAction("NewAction", "Description", None, None, "s3", "service")
        aws_action.connection = unittest.mock.create_autospec(Connection)
        aws_action.connection.assume_role_params = self.assume_role_params
        aws_action.connection.auth_params = self.auth_params
        aws_action.connection.client = unittest.mock.create_autospec(Boto3Stub)
        aws_action.connection.client.service = unittest.mock.MagicMock()
        aws_action.run()
        aws_action.connection.client.close.assert_called_once()

    @unittest.mock.patch.dict(environ, {"PLUGIN_RUNTIME_ENVIRONMENT": "orchestrator"})
    @unittest.mock.patch.object(AWSAction, "handle_rest_call", return_value={"mock_key": "mock_value"})
    def test_run_client_non_cloud_mode_in_action_default_override(self, _mock_handle_rest_call):
        # Test AWSAction when we have specified to close the client
        aws_action = AWSAction("NewAction", "Description", None, None, "s3", "service", close_client=True)
        aws_action.connection = unittest.mock.create_autospec(Connection)
        aws_action.connection.assume_role_params = self.assume_role_params
        aws_action.connection.auth_params = self.auth_params
        aws_action.connection.client = unittest.mock.create_autospec(Boto3Stub)
        aws_action.connection.client.service = unittest.mock.MagicMock()
        aws_action.run()
        aws_action.connection.client.close.assert_called_once()

    @unittest.mock.patch.dict(environ, {"PLUGIN_RUNTIME_ENVIRONMENT": "cloud"})
    @unittest.mock.patch.object(AWSAction, "handle_rest_call", return_value={"mock_key": "mock_value"})
    def test_run_client_cloud_mode_in_typical_c2c_task(self, _mock_handle_rest_call):
        # Test AWSAction used within a C2C task, we want to keep the client for subsequent calls
        aws_action = AWSAction("NewAction", "Description", None, None, "s3", "service", close_client=False)
        aws_action.connection = unittest.mock.create_autospec(Connection)
        aws_action.connection.assume_role_params = self.assume_role_params
        aws_action.connection.auth_params = self.auth_params
        aws_action.connection.client = unittest.mock.create_autospec(Boto3Stub)
        aws_action.connection.client.service = unittest.mock.MagicMock()
        aws_action.run()
        aws_action.connection.client.close.assert_not_called()

    def mocked_requests_get(*args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code
                self.ok = True
                self.text = str(json_data)

        return MockResponse(None, 200)

    @unittest.mock.patch("requests.get", side_effect=mocked_requests_get)
    @unittest.mock.patch("botocore.session.Session", return_value=unittest.mock.Mock())
    @unittest.mock.patch("boto3.client", return_value=Boto3Stub())
    def test_test(self, mock_get, mock_session, mock_sts_client):
        self.aws_action.connection.client = mock_session
        self.aws_action.test()
        self.aws_action.connection.helper.format_output.assert_called_once()


class Test(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()

    @parameterized.expand(
        [
            ("snake_str_1", "SnakeStr1"),
            ("sssnake31_#test", "Sssnake31#Test"),
            ("s__o", "SO"),
            ("_private_variable", "PrivateVariable"),
        ],
    )
    def test_to_upper_camel_case(self, input_str, output_str):
        camel_case_str = ActionHelper.to_upper_camel_case(input_str)
        self.assertEqual(camel_case_str, output_str)

    def test_get_empty_input(self):
        formatted_params = ActionHelper.format_input(
            {"$param1": {}, "$param2": {}, "$param3": [], "$param4": "test"}
        )
        self.assertEqual(formatted_params, {"Param4": "test"})

    def test_get_empty_output(self):
        path = Path(__file__).parent / f"payloads/output_schema.json"
        with open(path) as file:
            output_schema = json.load(file)
        empty_output = ActionHelper.get_empty_output(output_schema)
        self.assertEqual(
            empty_output,
            {
                "reservations": [],
                "response_metadata": {"http_status_code": 0, "request_id": ""},
            },
        )

    @parameterized.expand(
        [
            (datetime.datetime(2022, 9, 4), "2022-09-04T00:00:00"),
            (2.467, "2.467"),
            (b"a", "YQ=="),
            (br.StreamingBody(io.BytesIO(b"\x01\x02\x03\x04"), 4), "AQIDBA=="),
            ("test string", "test string"),
            ([3.14, 2.71], ["3.14", "2.71"]),
            ([{"key1": 3.14}, {"key2": 2.71}], [{"key1": "3.14"}, {"key2": "2.71"}]),
        ]
    )
    def test_fix_output_types(self, input_type, output_type):
        ah = ActionHelper()
        date = ah.fix_output_types(input_type)
        self.assertEqual(output_type, date)

    @parameterized.expand(
        [
            ({"UpperCamel": "OutputValue"}, {"upper_camel": "OutputValue"}),
            ([{"UpperCamel": "OutputValue"}], [{"upper_camel": "OutputValue"}]),
        ]
    )
    def test_convert_all_to_snake_case(self, test_input, test_output):
        converted = ActionHelper.convert_all_to_snake_case(test_input)
        self.assertEqual(converted, test_output)

    def test_format_output(self):
        ah = ActionHelper()
        path = Path(__file__).parent / f"payloads/output_schema.json"
        with open(path) as file:
            output_schema = json.load(file)
        test_input = {"Reservations": [{"key1": 1}]}
        output = ah.format_output(output_schema, test_input)
        correct_output = {
            "reservations": [{"key1": 1}],
            "response_metadata": {"http_status_code": 0, "request_id": ""},
        }
        self.assertEqual(output, correct_output)

    @parameterized.expand(
        [
            ({"snake_case": "OutputValue"}, {"SnakeCase": "OutputValue"}),
            ([{"snake_case": "OutputValue"}], [{"SnakeCase": "OutputValue"}]),
        ]
    )
    def test_convert_all_to_upper_camel_case(self, test_input, test_output):
        converted = ActionHelper.convert_all_to_upper_camel_case(test_input)
        self.assertEqual(test_output, converted)
