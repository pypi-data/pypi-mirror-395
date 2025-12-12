# -*- coding: utf-8 -*-
import copy
import logging
import os
import re
import sys
from datetime import timedelta
from typing import Any, Dict, List, Tuple, Union

import python_jsonschema_objects as pjs

KEYS_TO_CHECK_SECRETS = ("secretKey", "password", "key", "token")
DEFAULT_REPLACE_THRESHOLD = 0.8
DEFAULT_NUMBER_OF_ITERATIONS = 50
OTEL_ENDPOINT = "otel_tracing"


class OutputMasker:
    @staticmethod
    def extract_connection_values(
        connection: Dict[str, Any], keys_to_check: Tuple[str] = KEYS_TO_CHECK_SECRETS
    ) -> List[Any]:
        """
        extract_connection_values. Extracts the str values of the connection dictionary and returns them in a sorted list.

        :param connection: A dictionary containing the connection details.
        :type: Dict[str, Any]
        :param keys_to_check: A dictionary containing the connection details. Defaults to KEYS_TO_CHECK_SECRETS.
        :type: Tuple[str]
        :return: A tuple containing the values of keys to be searched.
        :rtype: List[Any]
        """

        connection_values = []
        if connection and isinstance(connection, dict):
            for key, value in connection.items():
                if isinstance(value, dict):
                    connection_values.extend(
                        OutputMasker.extract_connection_values(value)
                    )
                elif isinstance(value, str) and value and key in keys_to_check:
                    connection_values.append(value)
        return sorted(set(connection_values))

    @staticmethod
    def count_percentage_leak(text: str, body: str) -> Tuple[str, float]:
        """
        count_percentage_leak. Counts the percentage of text that appears in the body string.

        :param text: The text to be searched for
        :type: str

        :param body: The body of text to be searched in
        :type: str

        :return: A tuple containing the matching portion of the text
            string (str) and the percentage (float) of the text string
            that appears, starting from the beginning and counting only the
            consecutive matches
        :rtype: Tuple[str, float]
        """

        count = 0
        for character in body:
            if character == text[count]:
                count += 1
            if count == len(text):
                break
        return text[:count], count / len(text)

    @staticmethod
    def mask_str_in_dict(
        text: str,
        input_: Union[Dict[str, Any], List[Dict[str, Any]], str],
        threshold: float = DEFAULT_REPLACE_THRESHOLD,
        number_of_iterations: int = DEFAULT_NUMBER_OF_ITERATIONS,
    ) -> Dict[str, Any]:
        """
        mask_str_in_dict. Mask output data in the input text. This function searches the given text for output data
        and masks it. The input data can either be a string or a dictionary / list
        of dictionaries, where each dictionary is checked for output data and masked accordingly. The output is a
        dictionary containing the masked data.

        :param text: A string indicating the text to be searched for output data.
        :type: str

        :param input_: The input data which may contain the output data to be masked.
        :type: Union[Dict[str, Any], List[Dict[str, Any]], str]

        :param threshold: The minimum percentage of the exact text in the body to be considered a match.
         Defaults to DEFAULT_REPLACE_THRESHOLD.
        :type: float

        :param number_of_iterations: The number of iterations for a loop to iterate when replace is required.
         Defaults to DEFAULT_NUMBER_OF_ITERATIONS.
        :type: int

        :return: A dictionary containing the masked output data.
        :rtype: Dict[str, Any]
        """

        if isinstance(input_, dict):
            for key, value in input_.items():
                input_[key] = OutputMasker.mask_str_in_dict(text, value)
        elif isinstance(input_, list):
            for index, item in enumerate(input_):
                input_[index] = OutputMasker.mask_str_in_dict(text, item)
        else:
            if isinstance(text, str) and isinstance(input_, str):
                for _ in range(0, number_of_iterations):
                    (
                        text_to_be_replaced,
                        percentage_leak,
                    ) = OutputMasker.count_percentage_leak(text, input_)
                    if percentage_leak > threshold:
                        input_ = input_.replace(text_to_be_replaced, "*" * 8)
                    else:
                        break
        return input_

    @staticmethod
    def mask_output_data(
        connection: Dict[str, Any], output: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        mask_output_data. Masks sensitive data in the output dictionary using the connection dictionary.
        Given a connection dictionary with properties such as "username" and "password", this function masks sensitive
        data in the given output dictionary, replacing any sensitive values with "*".

        :param connection: A dictionary containing the connection details.
        :type: Dict[str, Any]

        :param output: A dictionary containing the output data.
        :type: Dict[str, Any]

        :return: A dictionary containing the masked output data.
        :rtype: Dict[str, Any]
        """

        connection_data = OutputMasker.extract_connection_values(connection)
        masked_response = output.copy()
        for element in connection_data:
            masked_response = OutputMasker.mask_str_in_dict(element, masked_response)
        return masked_response


def flush_logging_handlers(logger: logging.Logger) -> None:
    """
    Flush all the logging handlers attached to the logger.

    :param logger: The logger object to flush the handlers for.
    :type: logging.Logger

    :return: None
    :rtype: None
    """

    for handler in logger.handlers:
        handler.flush()


def default_for_object(obj, defs):
    defaults = {}

    if not obj.get("properties"):
        return defaults

    for key, prop in obj["properties"].items():
        defaults[key] = default_for(prop, defs)
    return defaults


def default_for(prop, defs):
    if "default" in prop:
        return prop["default"]

    # TODO should really follow this
    if prop.get("$ref") and defs:
        items = defs.get(prop.get("$ref"))
        if items:
            return default_for(items, defs)

        return {}

    if "oneOf" in prop:
        for o in prop["oneOf"]:
            t = default_for(o, defs)
            if t is not None:
                return t

    if "type" not in prop:
        return None

    if "enum" in prop:
        return prop["enum"][0]

    if prop["type"] == "array":
        return []

    if prop["type"] == "object":
        return default_for_object(prop, defs)

    if prop["type"] == "string":
        return ""

    if prop["type"] == "boolean":
        return False

    if prop["type"] == "integer" or prop["type"] == "number":
        return 0

    return None


def sample(source):
    if not source or ("properties" not in source) or len(source["properties"]) == 0:
        return {}

    schema = {
        "title": "Example",
        "properties": {},
        "type": "object",
        "required": [],
    }

    definitions = {}

    if source.get("definitions"):
        schema["definitions"] = source["definitions"]

        for key, defin in source["definitions"].items():
            definitions["#/definitions/" + key] = defin

    defaults = default_for_object(source, definitions)

    for key, prop in source["properties"].items():
        prop = copy.copy(prop)
        schema["properties"][key] = prop
        schema["required"].append(key)

    # Get logger instances before sampling runs and suppress them.
    # This will allow us to generate samples WITHOUT having to grep through the debug messages
    loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]
    for logger in loggers:
        logger.disabled = True

    builder = pjs.ObjectBuilder(schema)
    ns = builder.build_classes(strict=True)
    clazz = ns.Example
    o = clazz(**defaults)

    # Re-enable logging after we're done
    for logger in loggers:
        logger.disabled = False

    return o.as_dict()


def trace():
    """Returns the trace from an exception"""
    return sys.exc_info()[2]


def is_running_in_cloud():
    return os.environ.get("PLUGIN_RUNTIME_ENVIRONMENT") == "cloud"


def parse_from_string(
    duration: str,
    default: timedelta = timedelta(days=2),
    unit_map: Dict[str, str] = None,
) -> timedelta:
    """
    Parse a string duration (i.e. '5d', '12h', '30m', '45s') into a timedelta object.

    :param duration: String in format like '5d', '12h', '30m', '45s'
    :type duration: str

    :param default: Default timedelta to return if parsing fails
    :type default: timedelta

    :param unit_map: Mapping of unit letters to timedelta parameter names
    :type unit_map: Dict[str, str]

    :return: Parsed timedelta or default if parsing fails
    :rtype: timedelta
    """

    # If unit_map is not provided, use the default mapping
    if unit_map is None:
        unit_map = {"s": "seconds", "m": "minutes", "h": "hours", "d": "days"}

    # Check if duration is not empty and is a string
    if not duration or not isinstance(duration, str):
        return default

    # Use regex to match the duration format
    match = re.match(r"(\d+)([smhd])", duration.lower())
    if not match:
        return default

    # If match is found, extract the value and unit
    value, unit = match.groups()

    # Return a timedelta object based on the matched value and unit from the unit_map
    return timedelta(**{unit_map[unit]: int(value)})
