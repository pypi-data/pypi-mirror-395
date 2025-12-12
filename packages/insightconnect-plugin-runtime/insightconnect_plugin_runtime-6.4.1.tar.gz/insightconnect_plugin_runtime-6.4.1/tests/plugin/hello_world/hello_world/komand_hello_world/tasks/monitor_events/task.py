import insightconnect_plugin_runtime
from .schema import MonitorEventsInput, MonitorEventsOutput, MonitorEventsState, Component


class MonitorEvents(insightconnect_plugin_runtime.Task):

    def __init__(self):
        super(self.__class__, self).__init__(
                name="monitor_events",
                description=Component.DESCRIPTION,
                input=MonitorEventsInput(),
                output=MonitorEventsOutput(),
                state=MonitorEventsState())

    def run(self, params={}, state={}, custom_config={}):
        # Only being used to test API in unit tests for passing komand-props, no need to implement
        return {}, {}
