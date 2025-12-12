import unittest
from unittest import mock

from insightconnect_plugin_runtime.exceptions import PluginException
from insightconnect_plugin_runtime.metrics import MetricsBuilder


class BuildErrorBlobTest(unittest.TestCase):
    def setUp(self) -> None:
        self.metrics_builder = MetricsBuilder(
            plugin_name="",
            plugin_version="",
            plugin_vendor="",
            input_message={},
            exception_=Exception(),
        )

    def test_build_error_blob_plugin_exception_good(self):
        self.metrics_builder.exception_ = PluginException(
            preset=PluginException.Preset.NOT_FOUND
        )
        expected = {
            "cause": "not_found",
            "known": True,
            "message": "An error occurred during plugin execution! Invalid or unreachable endpoint "
            "provided. Verify the URLs or endpoints in your configuration are correct.",
        }

        actual = self.metrics_builder._build_error_blob()

        self.assertEqual(expected, actual)

    def test_build_error_blob_index_error_good(self):
        expected = {
            "cause": "IndexError",
            "known": False,
            "message": "list index out of range",
        }

        try:
            [][0]
        except Exception as e:
            self.metrics_builder.exception_ = e
            actual = self.metrics_builder._build_error_blob()
            self.assertEqual(expected, actual)

    def test_build_error_blob_index_error_erroneous_known_false(self):
        expected = {
            "cause": "IndexError",
            "known": True,
            "message": "list index out of range",
        }

        try:
            [][0]
        except Exception as e:
            self.metrics_builder.exception_ = e
            actual = self.metrics_builder._build_error_blob()
            self.assertNotEqual(expected, actual)

    def test_build_error_blob_index_error_is_string_class_name(self):
        expected = {
            "cause": "<class 'IndexError'>",
            "known": True,
            "message": "list index out of range",
        }

        try:
            [][0]
        except Exception as e:
            self.metrics_builder.exception_ = e
            actual = self.metrics_builder._build_error_blob()
            self.assertNotEqual(expected, actual)

    def test_build_error_blob_plugin_exception_preset_mismatched(self):
        self.metrics_builder.exception_ = PluginException(
            preset=PluginException.Preset.NOT_FOUND
        )
        expected = {
            "cause": "mismatched",
            "known": True,
            "message": "An error occurred during plugin execution!\n\nInvalid or unreachable endpoint "
            "provided. Verify the endpoint/URL/hostname configured in your "
            "plugin connection is correct.",
        }

        actual = self.metrics_builder._build_error_blob()

        self.assertNotEqual(expected, actual)

    def test_build_error_blob_plugin_exception_erroneous_known_false(self):
        self.metrics_builder.exception_ = PluginException(
            preset=PluginException.Preset.NOT_FOUND
        )
        expected = {
            "cause": "not_found",
            "known": False,
            "message": "An error occurred during plugin execution!\n\nInvalid or unreachable endpoint "
            "provided. Verify the endpoint/URL/hostname configured in your "
            "plugin connection is correct.",
        }

        actual = self.metrics_builder._build_error_blob()

        self.assertNotEqual(expected, actual)


@mock.patch(
    "insightconnect_plugin_runtime.metrics.time.time",
    mock.MagicMock(return_value=1661545868.139564),
)
class GetTimestampTest(unittest.TestCase):
    def test_good(self):
        self.assertEqual(MetricsBuilder._get_timestamp(), "1661545868")


@mock.patch(
    "insightconnect_plugin_runtime.metrics.time.time",
    mock.MagicMock(return_value=1661545868.139564),
)
class CreateMetricsPayloadTest(unittest.TestCase):
    def test_good(self):
        metrics_builder = MetricsBuilder(
            plugin_name="Example Plugin",
            plugin_version="1.0.0",
            plugin_vendor="ExampleCorp",
            input_message={"body": {"input": {"type": "PluginException-Preset"}}},
            exception_=Exception(),
        )
        expected = {
            "plugin": {
                "name": "Example Plugin",
                "version": "1.0.0",
                "vendor": "ExampleCorp",
            },
            "workflow": {
                "step": {
                    "inputs": ["type"],
                    "error": None,
                },
                "id": None,
            },
            "organization_id": None,
            "measurement_time": "1661545868",
        }

        actual = metrics_builder._create_metrics_payload()

        self.assertEqual(expected, actual)

    def test_no_inputs(self):
        metrics_builder = MetricsBuilder(
            plugin_name="Example Plugin",
            plugin_version="1.0.0",
            plugin_vendor="ExampleCorp",
            input_message={"body": {"input": {}}},
            exception_=Exception(),
        )

        expected = {
            "plugin": {
                "name": "Example Plugin",
                "version": "1.0.0",
                "vendor": "ExampleCorp",
            },
            "workflow": {
                "step": {
                    "inputs": [],
                    "error": None,
                },
                "id": None,
            },
            "organization_id": None,
            "measurement_time": "1661545868",
        }

        actual = metrics_builder._create_metrics_payload()

        self.assertEqual(expected, actual)

    def test_plugin_info_mutations(self):
        metrics_builder = MetricsBuilder(
            plugin_name="exampleplugin",
            plugin_version="1.0.0",
            plugin_vendor="examplecorp",
            input_message={},
            exception_=Exception(),
        )

        expected = {
            "plugin": {
                "name": "Example Plugin",
                "version": "1.0.0",
                "vendor": "ExampleCorp",
            },
            "workflow": {
                "step": {
                    "inputs": {},
                    "error": None,
                },
                "id": None,
            },
            "organization_id": None,
            "measurement_time": "1661545868",
        }

        actual = metrics_builder._create_metrics_payload()

        self.assertNotEqual(expected, actual)


@mock.patch(
    "insightconnect_plugin_runtime.metrics.time.time",
    mock.MagicMock(return_value=1661545868.139564),
)
class BuildTest(unittest.TestCase):
    def test_good(self):
        metrics_builder = MetricsBuilder(
            plugin_name="Example Plugin",
            plugin_version="1.0.0",
            plugin_vendor="ExampleCorp",
            input_message={"body": {"input": {"type": "PluginException-Preset"}}},
            exception_=PluginException(preset=PluginException.Preset.NOT_FOUND),
        )

        expected = {
            "organization_id": None,
            "measurement_time": "1661545868",
            "plugin": {
                "name": "Example Plugin",
                "vendor": "ExampleCorp",
                "version": "1.0.0",
            },
            "workflow": {
                "id": None,
                "step": {
                    "error": {
                        "cause": "not_found",
                        "known": True,
                        "message": "An error occurred during plugin execution! Invalid or "
                        "unreachable endpoint provided. Verify the URLs or endpoints in your configuration are correct.",
                    },
                    "inputs": ["type"],
                },
            },
        }

        actual = metrics_builder.build()

        self.assertEqual(expected, actual)
