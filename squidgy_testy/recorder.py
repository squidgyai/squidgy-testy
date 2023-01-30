
import difflib

class Recorder:
    
    def start(self):
        print(f"Running tests...")

    def start_test_suite(self, test_suite: str):
        print(f"{test_suite}:")

    def start_test(self, test_suite: str, test: str):
        print(f"- {test}: ", end="")

    def assertion(self, test_suite: str, test: str, assertion_type: str, success: bool, expected: str, actual: str):
        if success:
            return

        print("Failed")

        # create a character diff of the expected vs reply strings:
        print("----- Diff -----")
        diff = difflib.ndiff(expected.splitlines(keepends=True), actual.splitlines(keepends=True))
        print(''.join(diff))

        print("----------------")    

    def end_test(self, test_suite: str, test: str, success: bool):
        if success:
            print("Passed")

