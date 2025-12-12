import json
import unittest
from typing import Any, Dict

from insightconnect_plugin_runtime import Input
from insightconnect_plugin_runtime.action import Action
from insightconnect_plugin_runtime.api.endpoints import Endpoints
from insightconnect_plugin_runtime.connection import Connection
from insightconnect_plugin_runtime.plugin import Plugin
from insightconnect_plugin_runtime.task import Task
from parameterized import parameterized

MOCKED_CONFIG = {
    "*": {
        "first_property": "first_property_global",
        "second_property": "second_property_global",
        "task_name_1": {"second_property": "second_property_global_task_name_1"},
    },
    "org_1": {
        "first_property": "first_property_org_1",
        "11111111-1111-1111-1111-111111111111": {
            "first_property": "first_property_org_1_11111111-1111-1111-1111-111111111111"
        },
        "task_name_2": {"second_property": "second_property_task_name_2"},
        "task_name_3": {
            "first_property": "first_property_task_name_3",
            "second_property": "second_property_task_name_3",
        },
        "22222222-2222-2222-2222-222222222222": {
            "first_property": "first_property_org_1_22222222-2222-2222-2222-222222222222",
            "second_property": "second_property_org_1_22222222-2222-2222-2222-222222222222",
        },
    },
    "org_2": {
        "first_property": "first_property_org_2",
        "second_property": "second_property_org_2",
        "task_name_1": {"first_property": "first_property_org_1_task_name_1"},
    },
}


class TestDefinitionsAllActions(unittest.TestCase):
    def setUp(self) -> None:
        self.endpoints = Endpoints(
            logger=None,
            plugin=None,
            spec=None,
            debug=None,
            workers=None,
            threads=None,
            master_pid=None,
            config_options=MOCKED_CONFIG,
        )

        plugin = Plugin(
            name="Example",
            vendor="NoVendor",
            description="Example Plugin",
            version="0.0.1",
            connection=Connection(input=None),
        )

        # Add example tasks
        for task in ("task_name_1", "task_name_2", "task_name_3"):
            plugin.add_task(
                Task(name=task, description="Test", input=None, output=None)
            )
        self.endpoints.plugin = plugin

    def test_input_good(self):
        schema = json.loads(
            """
                   {
                  "type": "object",
                  "title": "Variables",
                  "properties": {
                    "name": {
                      "type": "string",
                      "title": "Name",
                      "description": "Name to say goodbye to",
                      "order": 1
                    }
                  },
                  "required": [
                    "name"
                  ]
                }
                    """
        )

        self.endpoints.plugin.actions = {
            "test": Action(
                name="test",
                description="test action",
                input=Input(schema=schema),
                output=None,
            )
        }

        expected = {
            "actionsDefinitions": [
                {
                    "identifier": "test",
                    "inputJsonSchema": {
                        "properties": {
                            "name": {
                                "description": "Name to say goodbye to",
                                "order": 1,
                                "title": "Name",
                                "type": "string",
                            }
                        },
                        "required": ["name"],
                        "title": "Variables",
                        "type": "object",
                    },
                }
            ]
        }

        actual = self.endpoints._create_action_definitions_payload()

        self.assertEqual(expected, actual)

    def test_input_good_no_inputs(self):
        schema = json.loads("{}")

        self.endpoints.plugin.actions = {
            "test": Action(
                name="test",
                description="test action",
                input=Input(schema=schema),
                output=None,
            )
        }

        expected = {
            "actionsDefinitions": [{"identifier": "test", "inputJsonSchema": {}}]
        }

        actual = self.endpoints._create_action_definitions_payload()

        self.assertEqual(expected, actual)

    def test_input_invalid_format_misspell_actionsDefinitions(self):
        schema = json.loads(
            """
                   {
                  "type": "object",
                  "title": "Variables",
                  "properties": {
                    "name": {
                      "type": "string",
                      "title": "Name",
                      "description": "Name to say goodbye to",
                      "order": 1
                    }
                  },
                  "required": [
                    "name"
                  ]
                }
                    """
        )

        self.endpoints.plugin.actions = {
            "test": Action(
                name="test",
                description="test action",
                input=Input(schema=schema),
                output=None,
            )
        }

        expected = {
            "actionDefinition": [
                {
                    "identifier": "test",
                    "inputJsonSchema": {
                        "properties": {
                            "name": {
                                "description": "Name to say goodbye to",
                                "order": 1,
                                "title": "Name",
                                "type": "string",
                            }
                        },
                        "required": ["name"],
                        "title": "Variables",
                        "type": "object",
                    },
                }
            ]
        }

        actual = self.endpoints._create_action_definitions_payload()

        self.assertNotEqual(expected, actual)

    def test_input_invalid_format_missing_identifier(self):
        schema = json.loads(
            """
                   {
                  "type": "object",
                  "title": "Variables",
                  "properties": {
                    "name": {
                      "type": "string",
                      "title": "Name",
                      "description": "Name to say goodbye to",
                      "order": 1
                    }
                  },
                  "required": [
                    "name"
                  ]
                }
                    """
        )

        self.endpoints.plugin.actions = {
            "test": Action(
                name="test",
                description="test action",
                input=Input(schema=schema),
                output=None,
            )
        }

        expected = {
            "actionsDefinitions": [
                {
                    "inputJsonSchema": {
                        "properties": {
                            "name": {
                                "description": "Name to say goodbye to",
                                "order": 1,
                                "title": "Name",
                                "type": "string",
                            }
                        },
                        "required": ["name"],
                        "title": "Variables",
                        "type": "object",
                    }
                }
            ]
        }

        actual = self.endpoints._create_action_definitions_payload()

        self.assertNotEqual(expected, actual)

    @parameterized.expand(
        [
            (
                "",
                "",
                "no_task_in_properties",
                {
                    "first_property": "first_property_global",
                    "second_property": "second_property_global",
                },
            ),
            (
                "",
                "",
                "task_name_1",
                {
                    "first_property": "first_property_global",
                    "second_property": "second_property_global_task_name_1",
                },
            ),
            (
                "org_1",
                "",
                "no_task_in_properties",
                {
                    "first_property": "first_property_org_1",
                    "second_property": "second_property_global",
                },
            ),
            (
                "org_1",
                "11111111-1111-1111-1111-111111111111",
                "no_task_in_properties",
                {
                    "first_property": "first_property_org_1_11111111-1111-1111-1111-111111111111",
                    "second_property": "second_property_global",
                },
            ),
            (
                "org_1",
                "11111111-1111-1111-1111-111111111111",
                "task_name_2",
                {
                    "first_property": "first_property_org_1_11111111-1111-1111-1111-111111111111",
                    "second_property": "second_property_task_name_2",
                },
            ),
            (
                "org_1",
                "11111111-1111-1111-1111-111111111111",
                "task_name_3",
                {
                    "first_property": "first_property_org_1_11111111-1111-1111-1111-111111111111",
                    "second_property": "second_property_task_name_3",
                },
            ),
            (
                "org_1",
                "22222222-2222-2222-2222-222222222222",
                "no_task_in_properties",
                {
                    "first_property": "first_property_org_1_22222222-2222-2222-2222-222222222222",
                    "second_property": "second_property_org_1_22222222-2222-2222-2222-222222222222",
                },
            ),
            (
                "org_1",
                "22222222-2222-2222-2222-222222222222",
                "task_name_2",
                {
                    "first_property": "first_property_org_1_22222222-2222-2222-2222-222222222222",
                    "second_property": "second_property_org_1_22222222-2222-2222-2222-222222222222",
                },
            ),
            (
                "org_2",
                "",
                "",
                {
                    "first_property": "first_property_org_2",
                    "second_property": "second_property_org_2",
                },
            ),
            (
                "org_2",
                "",
                "task_name_1",
                {
                    "first_property": "first_property_org_1_task_name_1",
                    "second_property": "second_property_org_2",
                },
            ),
        ]
    )
    def test_add_plugin_custom_config(
        self, org_id: str, int_id: str, task_name: str, expected: Dict[str, Any]
    ) -> None:
        response = self.endpoints.add_plugin_custom_config(
            {"body": {}}, org_id, int_id, task_name
        )
        custom_config = response.get("body", {}).get("custom_config", {})
        self.assertEqual(custom_config, expected)
