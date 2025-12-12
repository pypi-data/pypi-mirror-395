import insightconnect_plugin_runtime
import time
from .schema import HelloTriggerInput, HelloTriggerOutput

# Custom imports below


class HelloTrigger(insightconnect_plugin_runtime.Trigger):
    def __init__(self):
        super(self.__class__, self).__init__(
            name="hello_trigger",
            description="Prints a greeting every 10 seconds",
            input=HelloTriggerInput(),
            output=HelloTriggerOutput(),
        )

    def run(self, params={}):
        """Run the trigger"""
        while True:
            self.logger.info("I am the log")
            resp = {"message": self.connection.greeting.format(params["name"])}
            self.send(resp)
            time.sleep(10)
            # because this is a test we need to return otherwise the thread runs indefinitely to match how
            # triggers run in production. Check using params 'test' so that if we build image of this plugin and
            # test we will enter the loop as usual.
            if params["test"]:
                return resp

    def test(self):
        self.logger.info("This is a test")
        return {"message": "Test greeting"}
