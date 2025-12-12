# -*- coding: utf-8 -*-
import copy
import hashlib
import json

from jsonschema import validate

from .util import sample as utilsample, is_running_in_cloud


def key(parameters):
    """key is a unique connection key"""

    if (
        parameters is not None
        and "connection_cache_key" in parameters
        and parameters["connection_cache_key"] != ""
    ):
        return parameters["connection_cache_key"]

    return hashlib.sha1(
        json.dumps(parameters, sort_keys=True).encode("utf-8")
    ).hexdigest()


class ConnectionCache(object):
    def __init__(self, prototype):
        self.connections = {}
        self.prototype = prototype  # connection JSON which does not contain a logger or validation on the values

    def get(self, parameters, logger):
        # when we're running in cloud mode we don't want to create and store connections to reduce the number
        # of connection objects lying around in memory as this isn't safe and can cause OOM errors.
        if is_running_in_cloud():
            conn = self.create_and_validate_connection(parameters, logger)
        else:
            # first check if we have an existing connection obj we can return as it's been validated already
            conn_key = key(parameters)
            if not (conn := self.connections.get(conn_key)):  # otherwise create a new conn obj and save in cache
                conn = self.create_and_validate_connection(parameters, logger)
                self.connections[conn_key] = conn
        return conn

    def create_and_validate_connection(self, parameters, logger):
        conn = copy.copy(self.prototype)
        conn.logger = logger
        conn.set_(parameters)
        conn.connect(parameters)

        return conn


class Connection(object):
    """Komand connection"""

    def __init__(self, input):
        # Maintain backwards compatibility here - if Input object passed in it will have a 'schema' property so use that
        # Otherwise, the input is a JSON schema, so just use it directly
        if hasattr(input, "schema"):
            self.schema = input.schema
        else:
            self.schema = input
        self.parameters = {}
        self.logger = None

    def set_(self, parameters):
        """Set parameters"""
        self.parameters = parameters
        self._validate()

    def _validate(self):
        """Validate variables"""
        if self.schema:
            validate(self.parameters, self.schema)

    def connect(self, params={}):
        """Connect"""
        raise NotImplementedError

    def sample(self):
        """Sample object"""
        if self.schema:
            return utilsample(self.schema)
