from testcase.state_testing_app.state_testing_app import TestingApp


def lambda_handler(event, context):
    """
    This function is the main entry point of the AWS Lambda function
    :param event: a scheduler or kafka event
    :param context: AWS Context
    :return:
    """
    app = TestingApp()
    app.load(None, event)
    app.asset_id = event[0].get("asset_id")
    app.state = app.load_state()

    app.state["last_processed_timestamp"] = 0
    app.state["message"] = "This is the app state on Redis"
    app.event = event
    app.run_modules()
    app.save_state()
