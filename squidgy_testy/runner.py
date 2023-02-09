
import os
from .model import *
from .service import PromptService, generate_prompt
from .recorder import Recorder
from .store import TestStore
from .assertions import *

def load_test_suites(directory: str, test_suite_to_run: str = None, test_name_to_run: str = None) -> dict[str,TestSuite]:
    if directory is None:
        directory = "."

    suites: dict[str, TestSuite] = {}

    # get current working directory
    directory = os.path.abspath(directory)
    print(directory)
    # lists all yaml files in the tests directory and parses them into Python objects
    for root, dirs, files in os.walk(directory + "/tests"):
        for file in files:
            if file.endswith(".yaml"):
                test_suite_name = os.path.splitext(os.path.split(file)[-1])[0]
                if (test_suite_to_run is None or file == test_suite_to_run or test_suite_to_run == test_suite_name):
                    with open(os.path.join(root, file)) as f:
                        doc = TestSuite.parse_raw(f, proto="yaml")

                        suites[test_suite_name] = doc

    # only load the test that was specified
    if test_name_to_run is not None:
        return {
            test_suite_to_run: TestSuite(
                tests={
                    test_name_to_run: suites[test_suite_to_run].tests[test_name_to_run]
                }
            )
        }

    return suites

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
                elif test_suite.stop is not None:
                    stop = test_suite.stop

                # combine prompt directory with the prompt file
                prompt_file = os.path.join(self.prompt_directory, test.prompt_file)

                prompt = generate_prompt(prompt_file, test.params, test.prompt_append)

                # Nothing changed, let's not rerun
                result = self.store.get_cached_result(test_suite_name, test_name, prompt, stop)
                is_cached = result is not None
                if result is None:
                    result = self.service.invoke(prompt, stop=stop)
                    result = result.strip()
                    self.store.set_result(test_suite_name, test_name, prompt, stop, result)

                test_success = True

                for assertion in test.assertions:
                    if type(assertion) == EqualToAssertion:
                        expected = assertion.equalTo
                        assertion_success = equalTo(result, expected)
                        test_success = test_success and assertion_success

                        self.recorder.text_comparison_assertion(test_suite_name, test_name, "equalTo", assertion_success, assertion.equalTo, result, is_cached)
                    
                    if type(assertion) == SimilarToAssertion:
                        expected = assertion.similarTo
                        assertion_success, score = similarTo(self.service, result, expected)
                        test_success = test_success and assertion_success

                        self.recorder.similar_to_assertion(test_suite_name, test_name, "similarTo", assertion_success, assertion.similarTo, result, score, is_cached)

                    if type(assertion) == StartsWithAssertion:
                        expected = assertion.startsWith
                        assertion_success, score = startsWith(self.service, result, expected)
                        test_success = test_success and assertion_success

                        self.recorder.text_comparison_assertion(test_suite_name, test_name, "startsWith", assertion_success, assertion.similarTo, result, is_cached)


                self.recorder.end_test(test_suite_name, test_name, test_success, is_cached)