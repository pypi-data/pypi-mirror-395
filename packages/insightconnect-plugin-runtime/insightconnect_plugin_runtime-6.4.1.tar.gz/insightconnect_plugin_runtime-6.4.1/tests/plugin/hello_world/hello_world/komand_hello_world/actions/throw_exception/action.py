import insightconnect_plugin_runtime
from .schema import ThrowExceptionInput, ThrowExceptionOutput

# Custom imports below


class ThrowException(insightconnect_plugin_runtime.Action):
    def __init__(self):
        super(self.__class__, self).__init__(
            name="throw_exception",
            description="This action will always throw an exception as soon as its invoked",
            input=ThrowExceptionInput(),
            output=ThrowExceptionOutput(),
        )

    def run(self, params={}):
        if params.get("bad_request"):
            raise insightconnect_plugin_runtime.exceptions.PluginException(
                preset=insightconnect_plugin_runtime.exceptions.PluginException.Preset.BAD_REQUEST
            )
        raise Exception("because I can")

    def test(self, params={}):
        if params.get("bad_request"):
            raise insightconnect_plugin_runtime.exceptions.PluginException(
                preset=insightconnect_plugin_runtime.exceptions.PluginException.Preset.BAD_REQUEST
            )
        raise Exception("because I can")
