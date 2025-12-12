from os import environ
from unittest import TestCase
from unittest.mock import patch, MagicMock

from insightconnect_plugin_runtime.connection import Connection, ConnectionCache, key

"""
Any time an action / task / trigger API is called and we route through `plugin.py` -> `start_step`
the request body, containing the connection JSON is parsed and we make use of the `ConnectionCache` to retrieve
a connection that has already been validated or we create the new `Connection` object and call the `connect` method
which should be implemented within the paryicular plugin. 

These unit test file is testing that the validation, and caching logic works as expected both when running
on an orchestrator or when running on the cloud. Cloud enabled plugins we do not want to re-use a previously
validated connection as more customers use the plugin, more and more connection objects can be left on the pod
which increases the memory usage and instead these should always be freshly created. 
"""


class TestCloudConnections(TestCase):
    def setUp(self):
        # Create a sample connection schema that will be validated
        self.connection_schema = {
            "type": "object",
            "properties": {
                "username": {"type": "string"},
            },
            "required": ["username"],
        }
        # these initialisations happen during plugin start up
        self.connection = Connection(self.connection_schema)
        self.connection_cache = ConnectionCache(self.connection)

        self.connection = {
            "username": "test_user@rapid7.com"
        }

        self.logger = MagicMock()

    def stub_con(self, params):
        # very basic example of what our connections do in plugins
        self.logger.info("Connect: Connecting...")
        self.username = params.get("username")

    @patch.dict(environ, {"PLUGIN_RUNTIME_ENVIRONMENT": "cloud"})
    @patch.object(Connection, "connect", new=stub_con)
    def test_running_cloud_has_no_cache(self):
        conn = self.connection_cache.get(self.connection, self.logger)
        self.assertEqual(conn.parameters, self.connection)
        self.assertDictEqual(self.connection_cache.connections, {})

    @patch.dict(environ, {"PLUGIN_RUNTIME_ENVIRONMENT": "cloud"})
    @patch.object(Connection, "connect", new=stub_con)
    def test_running_cloud_has_no_cache_on_subsequent_run(self):
        # call twice and we should still have no connection cache values
        with patch("insightconnect_plugin_runtime.connection.key", MagicMock(side_effect=key)) as stub_key:
            conn = self.connection_cache.get(self.connection, self.logger)
            _ = self.connection_cache.get(self.connection, self.logger)
        self.assertEqual(conn.parameters, self.connection)
        self.assertDictEqual(self.connection_cache.connections, {})
        self.assertEqual(stub_key.call_count, 0)  # shouldn't call this at all

    @patch.object(Connection, "connect", new=stub_con)
    def test_running_onprem_has_cached_connection(self):
        conn = self.connection_cache.get(self.connection, self.logger)
        self.assertEqual(conn.parameters, self.connection)
        self.assertNotEqual(self.connection_cache.connections, {})

        # the connection cache key should exist
        hashed_key = key(conn.parameters)
        self.assertIn(hashed_key, self.connection_cache.connections)
        self.assertTrue(type(self.connection_cache.connections[hashed_key] == Connection))

    @patch.object(ConnectionCache, "create_and_validate_connection")
    def test_running_onprem_uses_cache_on_subsequent_calls(self, stub_create):
        with patch("insightconnect_plugin_runtime.connection.key", MagicMock(side_effect=key)) as stub_key:
            # Mock the return value of create_and_validate_connection
            pretend_obj = 'for this unit test pretend this is a conn object'
            stub_create.return_value = pretend_obj

            # first call the connection cache for the first time adding a new entry
            conn = self.connection_cache.get(self.connection, self.logger)
            self.assertEqual(len(self.connection_cache.connections), 1)
            self.assertEqual(list(self.connection_cache.connections.values())[0], pretend_obj)
            self.assertEqual(conn, pretend_obj)
            self.assertEqual(stub_key.call_count, 1)

            # on a second call we get the same value but the create_and_validate shouldn't be called again
            conn2 = self.connection_cache.get(self.connection, self.logger)
            self.assertEqual(conn, conn2)
            stub_create.assert_called_once_with(self.connection, self.logger)

            # on a third call we add a new entry to the cached connections
            new_conn = self.connection.copy()
            new_conn["username"] = "test_user_2@rapid7.com"
            _ = self.connection_cache.get(new_conn, self.logger)
            self.assertEqual(len(self.connection_cache.connections), 2)  # new entry added

            self.assertEqual(stub_key.call_count, 3)  # should have been called each time

    def test_connection_not_implemented_raised(self):
        with self.assertRaises(NotImplementedError):  # we haven't stubbed this so the error is expected
            _conn = self.connection_cache.get(self.connection, self.logger)

        # this means the connection object is not saved in cache
        self.assertEqual(self.connection_cache.connections, {})

    def test_connection_validation_raised(self):
        with self.assertRaises(Exception):  # not the expected input to match the connection schema
            _conn = self.connection_cache.get({"not_expected_key": "value"}, self.logger)

        # this means the connection object is not saved in cache
        self.assertEqual(self.connection_cache.connections, {})
