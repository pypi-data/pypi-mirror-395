from insightconnect_plugin_runtime.plugin import Plugin
import json
import jsonschema
from insightconnect_plugin_runtime.util import OutputMasker

input_message_schema = json.load(
    open("./insightconnect_plugin_runtime/data/input_message_schema.json")
)
input_message_body = json.load(open("./tests/unit/payloads/input_message_example.json"))
input_message_body_credential_missed = json.load(
    open("./tests/unit/payloads/input_message_example_one_credential_missing.json")
)
output_say_hello_unmasked = json.load(
    open("./tests/unit/payloads/output_say_hello.json")
)
output_say_hello_masked = json.load(
    open("./tests/unit/payloads/output_say_hello_masked.json")
)
output_say_hello_unmasked_2 = json.load(
    open("./tests/unit/payloads/output_say_hello_unmasked_2.json")
)
output_say_hello_masked_2 = json.load(
    open("./tests/unit/payloads/output_say_hello_masked_2.json")
)
output_say_hello_unmasked_3 = json.load(
    open("./tests/unit/payloads/output_say_hello_unmasked_2.json")
)
output_say_hello_masked_3 = json.load(
    open("./tests/unit/payloads/output_say_hello_masked_3.json")
)


def code_agrees(input_message):
    plugin_success = True
    jsonschema_success = True
    try:
        Plugin.validate_input_message(input_message)
    except Exception as e:
        plugin_success = False
    try:
        jsonschema.validate(input_message, input_message_schema)
    except Exception as e:
        jsonschema_success = False
    assert plugin_success == jsonschema_success


def test_schema_matches_1():
    code_agrees(
        {
            "version": "v1",
            "type": "action_start",
            "body": {
                "meta": None,
                "action": "hello",
                "trigger": "",
                "connection": {"greeting": "Hello, {}!"},
                "dispatcher": None,
                "input": {"name": "wow"},
            },
        }
    )


def test_schema_matches_2():
    code_agrees(
        {
            "version": "v1",
            "type": "bad",
            "body": {
                "meta": None,
                "action": "hello",
                "trigger": "",
                "connection": {"greeting": "Hello, {}!"},
                "dispatcher": None,
                "input": {"name": "wow"},
            },
        }
    )


def test_schema_matches_3():
    code_agrees(
        {
            "version": "v2",
            "type": "action_start",
            "body": {
                "meta": None,
                "action": "hello",
                "trigger": "",
                "connection": {"greeting": "Hello, {}!"},
                "dispatcher": None,
                "input": {"name": "wow"},
            },
        }
    )


def test_schema_matches_4():
    code_agrees(
        {
            "version": "v1",
            "type": "action_start",
            "body": {
                "meta": None,
                "action": "hello",
                "trigger": "",
                "connection": {"greeting": "Hello, {}!"},
                "dispatcher": None,
                "input": None,
            },
        }
    )


def test_output_masking():
    connection = input_message_body.get("body", {}).get("connection", {})
    masked_output = OutputMasker.mask_output_data(connection, output_say_hello_unmasked)
    assert masked_output == output_say_hello_masked


def test_output_masking_2():
    connection = input_message_body.get("body", {}).get("connection", {})
    masked_output = OutputMasker.mask_output_data(
        connection, output_say_hello_unmasked_2
    )
    assert masked_output == output_say_hello_masked_2


def test_output_masking_3():
    connection = input_message_body_credential_missed.get("body", {}).get(
        "connection", {}
    )
    masked_output = OutputMasker.mask_output_data(
        connection, output_say_hello_unmasked_3
    )
    assert masked_output == output_say_hello_masked_3


def test_output_masking_when_connection_is_none():
    connection = None
    masked_output = OutputMasker.mask_output_data(
        connection, output_say_hello_unmasked_3
    )
    assert masked_output == output_say_hello_unmasked_3
