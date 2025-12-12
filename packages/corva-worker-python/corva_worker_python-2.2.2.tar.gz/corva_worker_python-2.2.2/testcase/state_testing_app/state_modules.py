import time

from worker.app.modules import Module


class TestRedis(Module):
    module_key = "redis-tester"
    collection = "None"

    module_state_fields = {
        "message": str,
    }

    # override
    def run_module(self, event, beginning_results):
        start_timer = time.time()

        self.reset_states()
        self.test_save_load()
        self.test_delete_states()
        self.state = {"message": f"This state is auto saved for {self.module_key}"}
        print(f"Redis tests completed in {int(time.time() - start_timer)} seconds.\n")

    def run(self, wits_stream: list):
        self.run_module(wits_stream, [])

    def reset_states(self):
        # Initialize and reset states
        print("Initialize test")
        asset_id = self.global_state["asset_id"]
        state_key = self.get_formatted_state_key(asset_id, self.app_key, self.module_key)
        self.delete_states(state_key)
        self.get_state()

    def test_save_load(self):
        # Save/load tests
        print("Save/load test")
        self.state = {"message": "This state is and example state"}
        self.save_state()
        state = self.get_state()
        assert self.state == state
        print("Save/load test completed")

    def test_delete_states(self):
        # Deletion Tests
        asset_id = self.global_state["asset_id"]

        modules = []
        for i in range(5):
            _module_key = f"delete.test{i}"
            module = TestRedis(self.global_state)
            module.module_key = _module_key
            state_key = module.get_formatted_state_key(asset_id, module.app_key, _module_key)
            state = {"message": f"Redis state with {state_key=}"}
            print(f"Set the {state=}")
            module.state = state
            module.save_state()
            modules.append(module)
            time.sleep(0.1)  # back-off to prevent blocking by redis

        # Delete Multiple
        state_keys = [self.get_formatted_state_key(asset_id, module.app_key, module.module_key) for module in modules]

        multiple_state_keys = state_keys[0:4]
        print(f"Deleting following {multiple_state_keys=}")
        self.delete_states(multiple_state_keys)
        for i in range(4):
            _module_key = f"delete.test{i}"
            current_state = modules[i].get_state()
            assert current_state == {"message": None}

        # Delete Single
        single_state_key = state_keys[4]
        print(f"Deleting following single {single_state_key=}")
        self.delete_states(single_state_key)
        current_state = modules[4].get_state()
        assert current_state == {"message": None}
