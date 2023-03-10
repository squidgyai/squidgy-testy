import hashlib
import os
import json
from datetime import datetime

class TestStore:
    """
    Records test results so that if a test hasn't changed, it doesn't get run again.
    Test results are stored in a JSON file. Before a test is run, it sends a string of all
    the prompt data. The store hashes this value and compares it to the stored value. If
    they match, the function returns falls. If they don't match, the function returns true and
    it records the new hash and time in the JSON file.
    """
    def __init__(self, file_name: str):
        self.file_name = file_name

        # make sure the directory exists
        os.makedirs(os.path.dirname(file_name), exist_ok=True)

        if os.path.exists(file_name):
            with open(file_name, "r") as f:
                self.data = json.load(f)
        else:
            self.data = {}

    def get_cached_result(self, test_suite: str, test: str, prompt: str, stop: list[str]) -> str:
        """
        Returns true if the test should be run, false if it should be skipped.
        """
        prompt_hash = hashlib.sha256((prompt + "\n".join(stop)).encode("utf-8")).hexdigest()

        if test_suite not in self.data:
            self.data[test_suite] = {}

        if test not in self.data[test_suite]:
            self.data[test_suite][test] = {}

        test_data = self.data[test_suite][test]

        if "hash" not in test_data or test_data["hash"] != prompt_hash:
            return None

        return test_data['result']

    def set_result(self, test_suite: str, test: str, prompt: str, stop: list[str], result: str):
        """
        Sets the result of a test.
        """
        if test_suite not in self.data:
            self.data[test_suite] = {}

        if test not in self.data[test_suite]:
            self.data[test_suite][test] = {}

        test_data = self.data[test_suite][test]

        test_data["hash"] = hashlib.sha256((prompt + "\n".join(stop)).encode("utf-8")).hexdigest()
        test_data["result"] = result
        test_data["last_run"] = datetime.now().isoformat()
        self.save()

    def save(self):
        with open(self.file_name, "w") as f:
            json.dump(self.data, f, indent=4)

"""A mock version of the TestStore which always returns true"""
class MockTestStore:
    def set_result(self, test_suite: str, test: str, prompt: str, stop: list[str], result: str):
        pass

    def get_cached_result(self, test_suite: str, test: str, prompt: str, stop: list[str]) -> str:
        return None