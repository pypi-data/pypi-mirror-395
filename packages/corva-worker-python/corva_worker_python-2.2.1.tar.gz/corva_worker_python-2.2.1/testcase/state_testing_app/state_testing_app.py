from testcase.state_testing_app.state_modules import TestRedis
from worker.app import App


class TestingApp(App):
    # override
    def get_modules(self):
        return [
            TestRedis,  # Redis testing module
        ]

    def load(self, event_type, event):
        # Do not want to run the super().load method
        return
