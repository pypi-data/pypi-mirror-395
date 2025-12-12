from worker import constants

constants.update(
    {
        "global": {
            "app-name": "WorkerTest-DrillingEfficiency",
            "app-key": "drilling-efficiency",
            "event-type": "scheduler",
            "query-limit": 3600,
            "wits_query_fields": "_id, timestamp, collection, asset_id, company_id, app, metadata, data.state, "
            "data.weight_on_bit, data.rotary_rpm, data.rotary_torque, data.rop",
        },
        "drilling-efficiency": {
            "mse": {
                "lookback-duration": 30,
                "export-duration": 30,  # update and export results every 30 seconds
                "drilling-activity": ["Rotary Drilling", "Slide Drilling"],
                "required-channels": ["weight_on_bit", "rotary_rpm", "rotary_torque", "rop"],
                "running-string": ["drillstring"],
                "reset-config": ["drillstring"],
            }
        },
    }
)
