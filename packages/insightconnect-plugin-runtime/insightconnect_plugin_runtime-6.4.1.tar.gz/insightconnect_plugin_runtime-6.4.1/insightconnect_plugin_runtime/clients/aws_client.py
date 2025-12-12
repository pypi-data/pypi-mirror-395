import base64
import datetime
import json
import re
import uuid
from typing import Any, Callable, Dict, List, Tuple, Union

import boto3
import botocore.exceptions
import botocore.response
import botocore.session
import requests
from botocore.exceptions import ClientError

import insightconnect_plugin_runtime
from insightconnect_plugin_runtime.action import Action
from insightconnect_plugin_runtime.exceptions import (
    PluginException,
    ConnectionTestException,
)
from insightconnect_plugin_runtime.helper import clean
from insightconnect_plugin_runtime.util import is_running_in_cloud

REGION = "region"
EXTERNAL_ID = "external_id"
ROLE_ARN = "role_arn"
ASSUME_ROLE_PARAMETERS = "assume_role_params"
AWS_CLIENT_ERRORS = [
    "AccessDeniedException",
    "InternalServerException",
    "ResourceNotFoundException",
    "InternalFailure",
    "InvalidClientTokenId",
    "NotAuthorized",
    "ServiceUnavailable",
    "OptInRequired",
]


class PaginationHelper:
    """
    A helper class for dealing with paginated requests.
    """

    def __init__(
        self,
        input_token: List[str],
        output_token: List[str],
        result_key: List[str],
        limit_key: str = None,
        more_results: str = None,
        non_aggregate_keys: List[str] = None,
        max_pages: int = None,  # if we want to limit how many pages of data we pull from AWS
    ):
        self.input_token = input_token
        self.output_token = output_token
        self.result_key = result_key
        self.limit_key = limit_key
        self.more_results = more_results
        self.non_aggregate_keys = non_aggregate_keys
        self.keys_to_remove = []
        self.keys_to_remove.extend(input_token)
        self.keys_to_remove.extend(output_token)
        self.max_pages = max_pages
        if more_results:
            self.keys_to_remove.append(self.more_results)

    def remove_keys(self, params: Dict[str, Any]) -> None:
        """
        Remove pagination related keys from output parameters.
        :param params: params.
        :return: None
        """
        for key in self.keys_to_remove:
            params.pop(key, None)

    def check_pagination(self, input_: Dict[str, Any], output: Dict[str, Any]) -> bool:
        """
        Looks at the output of a rest call and determines if the call was paginated.

        :param input_: The input variables
        :param output: The output variables
        :return: True if more results are available, False otherwise
        """

        is_paginated = False

        if (
            self.more_results
            and self.more_results in output.keys()
            and output[self.more_results]
        ):
            is_paginated = True

        for idx, _ in enumerate(self.input_token):
            if self.output_token[idx] in output.keys():
                input_[self.input_token[idx]] = output[self.output_token[idx]]
                is_paginated = True

        return is_paginated

    def check_total_results(self, params, response: Dict[str, Any]) -> bool:
        """
        Check if we have ran the AWS call too many times, eg params[max_keys] * max_pages = len response
        :param params: parameters used within the ListObjectsv2 command
        :param response: response contents from ListObjectsv2
        :return: boolean to indicate if we have reached the max amount of objects to be returned in one execution.
        """
        if self.max_pages:
            max_allowed = params[self.limit_key] * self.max_pages
            if max_allowed >= len(response[self.result_key[0]]):
                return True

        return False

    def merge_responses(
        self,
        input_: Dict[str, Any],
        response_1: Dict[str, Any],
        response_2: Dict[str, Any],
    ) -> Tuple[Dict[str, Any], bool]:
        """
        Merges two output dictionaries together.
        :param input_: Input dictionary containing limit_key
        :type: Dict[str, Any]
        :param response_1: First input response
        :type: Dict[str, Any]
        :param response_2: Second input response
        :type: Dict[str, Any]
        :return: Tuple containing the dictionary with merged, limited responses, and the boolean flag max_hit
        :rtype: Tuple[Dict[str, Any], bool]
        """

        max_hit = False

        for response in self.result_key:
            temporary_1 = response_1[response]
            response_1[response] = response_2[response]
            response_1[response].extend(temporary_1)

            if self.limit_key and self.limit_key in input_.keys():
                if len(response_1[response]) >= input_[self.limit_key]:
                    max_hit = True
                    response_1[response] = response_1[response][
                        : input_[self.limit_key]
                    ]

        return response_1, max_hit


class ActionHelper:
    """
    Helper class for invoking AWS.
    """

    @staticmethod
    def to_upper_camel_case(snake_str: str) -> str:
        """
        Convert the snake case string to upper camel case.
        :param snake_str: Input snake string.
        :type: str
        :return: Upper camel case string.
        :rtype: str
        """

        components = snake_str.split("_")
        return "".join(x.title() for x in components)

    @classmethod
    def format_input(cls, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Formats the input parameters to be consumable by botocore.

        Keys are formatted to upper camel case.

        Input parameters should be left out of the botocore request if the variable is:
        * an empty list
        * an empty dict
        * a zero-length string

        :param params: The input parameters.
        :return: The formatted input parameters as a new dictionary.
        """
        formatted_params = {}

        # Drop invalid empty parameters
        for key, value in params.items():
            if isinstance(value, list) and (len(value) == 0):
                continue
            if isinstance(value, dict) and (len(value.keys()) == 0):
                continue
            if isinstance(value, str) and (value == ""):
                continue
            formatted_params[key.replace("$", "")] = value

        formatted_params = cls.convert_all_to_upper_camel_case(formatted_params)

        return formatted_params

    @staticmethod
    def get_empty_output(output_schema: Dict[str, Any]) -> Dict[str, Any]:
        """
        Returns a dictionary which maps output parameters to default values.

        To adhere to an action's output schema, empty lists and dictionaries must exist.

        :param output_schema: The output schema.
        :return: A dictionary which maps properties to empty values.
        """
        empty_output = {}
        if "properties" in output_schema:
            output_properties = output_schema["properties"]
            for prop_key in output_properties:
                prop = output_properties[prop_key]
                if "type" in prop:
                    if prop["type"] == "array":
                        empty_output[prop_key] = []
                    elif prop["type"] == "object":
                        empty_output[prop_key] = {}
                elif "$ref" in prop:
                    prop = output_schema["definitions"][prop_key]
                    if "type" in prop:
                        if prop["type"] == "array":
                            empty_output[prop_key] = []
                        elif prop["type"] == "object":
                            empty_output[prop_key] = {}

        empty_output["response_metadata"] = {"request_id": "", "http_status_code": 0}
        return empty_output

    @classmethod
    def fix_output_types(cls, output: Dict[str, Any]) -> Any:  # noqa: C901
        """
        Formats the output of a botocore call to be correct types.

        The botocore response dictionary contains types which are not supported by Komand.

        * Dictionary values are recursively formatted
        * List values are recursively formatted
        * Primitive types are matched as best as possible

        :param output: the output dictionary.
        :return: A formatted output dictionary.
        """

        if isinstance(output, dict):
            new_dict = {}
            for key in output:
                new_dict[key] = cls.fix_output_types(output[key])
            return new_dict
        elif isinstance(output, list):
            new_list = []
            for item in output:
                new_list.append(cls.fix_output_types(item))
            return new_list
        elif isinstance(output, str):
            return output
        elif isinstance(output, botocore.response.StreamingBody):
            return base64.b64encode(output.read()).decode("utf-8")
        elif isinstance(output, bytes):
            return base64.b64encode(output).decode("utf-8")
        elif isinstance(output, int):
            return output
        elif isinstance(output, bool):
            return output
        elif isinstance(output, float):
            return str(output)
        elif isinstance(output, datetime.datetime):
            return output.isoformat()
        else:
            return json.dumps(output)

    first_cap_re = re.compile("(.)([A-Z][a-z]+)")
    all_cap_re = re.compile("([a-z0-9])([A-Z])")

    @classmethod
    def to_snake_case(cls, camel_case: str) -> str:
        """
        Converts an upper camel case string to snake case.

        :param camel_case: The upper camel case string.
        :return: The same string in snake_case
        """

        s1 = cls.first_cap_re.sub(r"\1_\2", camel_case)
        return cls.all_cap_re.sub(r"\1_\2", s1).lower()

    @classmethod
    def convert_all_to_upper_camel_case(cls, obj: Dict[str, Any]) -> Any:
        """
        Recursively converts dictionary keys to upper camel case from snake case.
        :param obj: The object.
        :return: The object with snake case keys.
        """

        if isinstance(obj, dict):
            new_obj = {}
            for key, value in obj.items():
                new_value = cls.convert_all_to_upper_camel_case(value)
                new_obj[cls.to_upper_camel_case(key)] = new_value
            return new_obj
        elif isinstance(obj, list):
            new_obj = []
            for list_ in obj:
                new_list = cls.convert_all_to_upper_camel_case(list_)
                new_obj.append(new_list)
            return new_obj
        else:
            return obj

    @classmethod
    def convert_all_to_snake_case(cls, obj: Dict[str, Any]) -> Any:
        """
        Recursively converts dictionary keys from upper camel case to snake case.
        :param obj: The object.
        :return: The object with snake case keys.
        """

        if isinstance(obj, dict):
            new_obj = {}
            for key, value in obj.items():
                new_value = cls.convert_all_to_snake_case(value)
                new_obj[cls.to_snake_case(key)] = new_value
            return new_obj
        elif isinstance(obj, list):
            new_obj = []
            for list_ in obj:
                new_list = cls.convert_all_to_snake_case(list_)
                new_obj.append(new_list)
            return new_obj
        else:
            return obj

    @classmethod
    def format_output(
        cls, output_schema: Union[Dict[str, Any], None], output: Dict[str, Any]
    ) -> Any:
        """
        Formats a botocore response into a correct Komand response.

        Keys are formatted to snake case.

        :param output_schema: The output json schema
        :param output: The response from the botocore call
        :return: Correctly formatted botocall response
        """
        # Fix types
        output = cls.fix_output_types(output)
        output = cls.convert_all_to_snake_case(output)

        # Add empty lists/dicts if values are missing
        if output_schema:
            empty = cls.get_empty_output(output_schema)
            for key in empty:  # pylint:disable=consider-using-dict-items
                if key not in output:
                    output[key] = empty[key]

        return output


class AWSAction(Action):
    """
    Abstract class for handling any aws-cli request.
    """

    def __init__(
        self,
        name: str,
        description: str,
        input_: insightconnect_plugin_runtime.Input,
        output: insightconnect_plugin_runtime.Output,
        aws_service: str,
        aws_command: str,
        pagination_helper: PaginationHelper = None,
        close_client: bool = None,
    ):
        """

        Initializes a new AwsAction object.

        :param name: The name of the action. Should be snake case.
        :param description: The description fo the action.
        :param input_: The input schema object
        :param output: The output schema object
        :param aws_service: The AWS service. Should be snake case.
        :param aws_command: The type of request to invoke. Should be snake case.
        :param pagination_helper: Paginating helper indicate attrs like max_pages and token location.
        :param close_client: Determine if the created client should be closed at the end of the action.
        """

        super().__init__(
            name=name, description=description, input=input_, output=output
        )
        self.aws_service = aws_service
        self.aws_command = aws_command
        self.pagination_helper = pagination_helper

        # when running in cloud mode we won't hold this connection, so each call to action.run() will spawn a new
        # client, in this case we should close the client unless otherwise specified. A use case to not close
        # is on a task plugin that re-uses the client for list_objects_v2 and get_bucket_content.
        self.close_client = is_running_in_cloud() if close_client is None else close_client

    def _handle_botocore_function(
        self, client_function: Callable, params: Dict
    ) -> Dict:
        try:
            response = client_function(**params)
        except botocore.exceptions.NoRegionError as error:
            self.logger.error(
                f"Error occurred when invoking the aws-cli. No region specified. Boto3 response: {error}"
            )
            raise PluginException(
                cause="Error occurred when invoking the aws-cli. No region specified",
                assistance="Please specify a valid region to access the AWS services.",
                data=error,
            )
        except botocore.exceptions.EndpointConnectionError as error:
            self.logger.error(
                "Error occurred when invoking the aws-cli: Unable to reach the URL endpoint. Check the connection "
                f"region is correct. Boto3 response: {error}"
            )
            raise PluginException(
                cause="Error occurred when invoking the aws-cli: Unable to reach the url endpoint.",
                assistance="Check if the connection region is correct.",
                data=error,
            )
        except botocore.exceptions.ParamValidationError as error:
            self.logger.error(
                f"Error occurred when invoking the aws-cli. Input parameters were missing or incorrect. Boto3 response: {error}"
            )
            raise PluginException(
                cause="Error occurred when invoking the aws-cli.",
                assistance="Input parameters were missing or incorrect",
                data=error,
            )
        except botocore.exceptions.ClientError as error:
            self.logger.error(
                "Error occurred when invoking the aws-cli. Check client connection keys and input arguments. Boto3 "
                f"response: {error}"
            )
            raise PluginException(
                cause="Error occurred when invoking the aws-cli.",
                assistance="Check client connection keys and input arguments.",
                data=error,
            )
        except Exception as error:
            self.logger.error(
                f"Error occurred when invoking the aws-cli. Boto3 response: {error}"
            )
            raise PluginException(
                cause="Error occurred when invoking the aws-cli.", data=error
            )
        finally:
            if self.close_client:
                self.connection.client.close()
        return response

    def _handle_format_output(self, response: Dict, helper: ActionHelper) -> Dict:
        try:
            if "properties" in self.output.schema:
                response = helper.format_output(self.output.schema, response)
            else:
                response = helper.format_output(None, response)
        except Exception:
            self.logger.error("Unable to format output parameters")
            raise PluginException(cause="Error occurred when invoking the aws-cli.")
        return response

    def handle_rest_call(self, client_function: Callable, params: Dict) -> Dict:
        helper = self.connection.helper

        # Format the input parameters for the botocall call
        self.logger.debug(params)
        try:
            params = helper.format_input(params)
        except Exception:
            self.logger.error("Unable to format input parameters")
            raise PluginException(cause="Unable to format input parameters")

        # Execute the botocore function
        self.logger.debug(params)
        response = self._handle_botocore_function(client_function, params)

        # Format the output parameters for the komand action output schema
        response = self._handle_format_output(response, helper)
        return response

    def run(self, params={}):
        """
        Executes the aws-cli command with the given input parameters.

        Exceptions are raised if:
        * The command cannot be found inside botocore.
        * The input parameters are invalid.
        * The output parameters cannot be formatted.
        * The call to AWS fails

        :param self: The action object.
        :param params: The input parameters, which adhere to the input schema
        :return: the output parameters, which adhere to the output schema
        """

        # Retrieve the assume_role_params from action
        assume_role_params = params.pop(ASSUME_ROLE_PARAMETERS, {})

        # Overwrite the region if it's empty with the value from the connection assume_role_params
        if not assume_role_params.get(REGION):
            assume_role_params[REGION] = self.connection.assume_role_params.get(REGION)

        # Retrieve client object, and auth_params from the connection
        auth_params = self.connection.auth_params
        client = self.connection.client

        # Try to assume role...
        if assume_role_params.get(ROLE_ARN):
            client = self.try_to_assume_role(
                self.aws_service, assume_role_params, auth_params
            )

        # There exists a function for each command in the service client object.
        try:
            client_function = getattr(client, self.aws_command)
        except AttributeError:
            error_message = (
                'Unable to find the command "'
                + self.aws_service
                + " "
                + self.aws_command
                + '"'
            )
            self.logger.error(error_message)
            raise PluginException(cause=error_message)

        response = self.handle_rest_call(client_function, params)

        # Handle possible pagination if this action supports pagination.
        if self.pagination_helper:
            while self.pagination_helper.check_pagination(params, response):
                if self.pagination_helper.check_total_results(params, response):
                    self.logger.info(
                        "Reached max amount of pages per execution breaking..."
                    )
                    break

                self.logger.info("Response was paginated. Performing another call.")
                response, max_hit = self.pagination_helper.merge_responses(
                    params, self.handle_rest_call(client_function, params), response
                )

                if max_hit:  # all data possible in this particular AWS call
                    break

            # if we have pagination enabled for AWS we want to take note of the tokens
            if not self.pagination_helper.max_pages:
                self.pagination_helper.remove_keys(response)

        if self.close_client:
            self.connection.client.close()

        return response

    def test(self, params={}):
        """
        Tests that the aws-cli command is executable with the given connection.

        This tests simply curls the url endpoint to check for internet connectivity.

        :param self: The action object.
        :param params: The input parameters.
        :return: None on success, exception on failure.
        """

        self.logger.debug(params)
        client = self.connection.client
        helper = self.connection.helper

        endpoint = client._endpoint.host  # pylint:disable=protected-access
        response = requests.get(endpoint)

        response_text = response.text
        status_code = response.status_code

        # AWS client errors are not always mapped predictably, and some service endpoints will return an unexpected
        # result
        if not (200 <= status_code <= 299):
            if (
                status_code in [401, 403, 404, 500, 503]
                and "UnknownOperationException" not in response_text
            ):
                raise ConnectionTestException(
                    cause=f"Error code {status_code} returned from AWS service",
                    assistance="Please check the response for more information",
                    data=response_text,
                )
            for error in AWS_CLIENT_ERRORS:
                if error in response_text:
                    raise ConnectionTestException(
                        cause=f"Error code {status_code} returned from AWS service with {error} exception",
                        assistance="Please check the response for more information",
                        data=response_text,
                    )

        if "properties" in self.output.schema:
            response = helper.format_output(self.output.schema, {})
        else:
            response = helper.format_output(None, {})

        return response

    @staticmethod
    def try_to_assume_role(
        service_name: str,
        assume_role_params: Dict[str, str],
        auth_params: Dict[str, str],
    ):
        session_name = str(uuid.uuid1())
        sts_client = boto3.client("sts", **auth_params, region_name=assume_role_params.get(REGION))
        try:
            assumed_role_object = sts_client.assume_role(
                **clean(
                    {
                        "RoleArn": assume_role_params.get(ROLE_ARN),
                        "RoleSessionName": session_name,
                        "ExternalId": assume_role_params.get(EXTERNAL_ID),
                    }
                )
            )
            sts_client.close()
        except ClientError as error:
            raise PluginException(
                cause=f"Boto3 raised following error during assume role: {error.response['Error']['Code']}",
                assistance="Please verify your role ARN and external ID are correct",
            )
        credentials = assumed_role_object["Credentials"]
        boto_client = boto3.client(
            service_name,
            aws_access_key_id=credentials["AccessKeyId"],
            aws_secret_access_key=credentials["SecretAccessKey"],
            aws_session_token=credentials["SessionToken"],
            region_name=assume_role_params[REGION],
        )

        return boto_client
