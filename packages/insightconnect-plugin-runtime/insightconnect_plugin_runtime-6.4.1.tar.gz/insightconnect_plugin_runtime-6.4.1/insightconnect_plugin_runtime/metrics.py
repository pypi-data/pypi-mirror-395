import time
from typing import Union, Optional

from .exceptions import ConnectionTestException


class MetricsBuilder:
    def __init__(
        self,
        plugin_name: str,
        plugin_version: str,
        plugin_vendor: str,
        input_message: dict,
        exception_: Union[ConnectionTestException, Exception],
        workflow_id: Optional[str] = None,
        org_id: Optional[str] = None,
    ):
        self.plugin_name = plugin_name
        self.plugin_version = plugin_version
        self.plugin_vendor = plugin_vendor
        self.input_message = input_message.get("body", {}).get("input", {})
        self.exception_ = exception_
        self.workflow_id = workflow_id
        self.org_id = org_id

    def build(self) -> dict:
        """
        Build a plugin metrics payload
        :return: Dictionary representing a payload containing various plugin metrics
        """
        payload = self._create_metrics_payload()
        payload["workflow"]["step"]["error"] = self._build_error_blob()

        return payload

    def _create_metrics_payload(self) -> dict:
        """
        Update a plugin output payload with metrics information
        :return: Dictionary containing metrics
        """

        # Sanitize input message
        provided_input = self._sanitize_input()

        payload = {
            "plugin": {
                "name": self.plugin_name,
                "version": self.plugin_version,
                "vendor": self.plugin_vendor,
            },
            "workflow": {
                "step": {
                    "inputs": provided_input,
                    "error": None,
                },
                "id": self.workflow_id,
            },
            "organization_id": self.org_id,
            "measurement_time": self._get_timestamp(),
        }

        return payload

    def _build_error_blob(self) -> dict:
        """
        Builds an error blob by extracting information from an exception
        :return: Dictionary containing error information
        """

        error = {}
        if isinstance(self.exception_, ConnectionTestException):
            error["cause"] = (
                self.exception_.preset
                if self.exception_.preset
                else self.exception_.cause
            )
            error["known"] = True
        else:
            error["cause"] = type(self.exception_).__name__  # Get type as a string

            # False, since this is not an error we explicitly handled in the plugin, eg. IndexError
            error["known"] = False
        error["message"] = str(self.exception_)

        return error

    @staticmethod
    def _get_timestamp() -> str:
        """
        Gets the current unix timestamp in seconds
        :return: Unix timestamp for 'now' in seconds
        """
        return str(int(time.time()))

    def _sanitize_input(self) -> [str]:
        """
        Strips input values from an input message to ensure sensitive data is not collected
        :return: List of input fields that were present in the input message, without values
        """
        input_fields = list(self.input_message.keys())

        return input_fields
