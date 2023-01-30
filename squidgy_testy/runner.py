
import os
from .model import *
from .service import PromptService, generate_prompt
from .recorder import Recorder
from .store import TestStore

def load_test_suites(directory: str, test_suite: str, test_name_to_run: str = None) -> dict[str,TestSuite]:
    if directory is None:
        directory = "."

    tests: dict[str, TestSuite] = {}

    # lists all yaml files in the tests directory and parses them into Python objects
    for root, dirs, files in os.walk(directory + "/tests"):
        for file in files:
            if file.endswith(".yaml"):
                test_suite_name = os.path.splitext(os.path.split(file)[-1])[0]
                if (test_suite is None or file == test_suite or test_suite == test_suite_name):
                    with open(os.path.join(root, file)) as f:
                        doc = TestSuite.parse_raw(f, proto="yaml")

                        tests[test_suite_name] = doc

    # only load the test that was specified
    for suite_name in tests:
        test_suite = tests[suite_name]
        for test_name in test_suite:
            if test_name_to_run is not None and test_name_to_run != test_name:
                del test_suite[test_name]

    return tests

class Runner:

    def __init__(
        self,
        test_suites: dict[str, TestSuite],
        recorder: Recorder,
        store: TestStore,
        service: PromptService,
        prompt_directory: str = "."
    ):
        self.test_suites = test_suites
        self.recorder = recorder
        self.store = store
        self.service = service
        self.prompt_directory = prompt_directory
 
    def run_tests(self):
        
        self.recorder.start()

        for test_suite_name in self.test_suites:
            test_suite = self.test_suites[test_suite_name]

            self.recorder.start_test_suite(test_suite_name)

            for test_name in test_suite.tests:
                test = test_suite.tests[test_name]

                self.recorder.start_test(test_suite_name, test_name)

                if test.prompt_file is None:
                    raise Exception(f"Test {test_name} must contain a base prompt")

                stop = ['\n\n']
                if test.stop is not None:
                    stop = test.stop

                # combine prompt directory with the prompt file
                prompt_file = os.path.join(self.prompt_directory, test.prompt_file)

                prompt = generate_prompt(prompt_file, test.params, test.prompt_append)

                # Nothing changed, let's not rerun
                if not self.store.should_run(test_suite_name, test_name, prompt):
                    self.recorder.skip_test(test_suite_name, test_name)
                    continue

                reply = self.service.invoke(prompt, stop=stop)

                reply = reply.strip()

                test_success = True

                if test.assertions.equalTo is not None:
                    expected = test.assertions.equalTo
                    assertion_success = reply == expected
                    test_success = test_success and assertion_success

                    self.recorder.assertion(test_suite_name, test_name, "equalTo", assertion_success, test.assertions.equalTo, reply)

                self.recorder.end_test(test_suite_name, test_name, test_success)