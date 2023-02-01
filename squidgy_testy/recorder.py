
import difflib
from .model import SimilarToAssertion

class Recorder:
    
    def start(self):
        print(f"Running tests...")

    def start_test_suite(self, test_suite: str):
        print(f"{test_suite}:")

    def start_test(self, test_suite: str, test: str):
        print(f"* {test}: ")

    def _assertion_start(self, assertion_type: str, success: bool, cached: bool):
        print("  * %s: " % assertion_type, end="")
        if success:
            print("✓ ", end="")
        else:
            print("FAILED ", end="")

        if cached:
            print("(cached)", end="")

    def equal_to_assertion(self, test_suite: str, test: str, assertion_type: str, success: bool, expected: str, actual: str, cached: bool):
        self._assertion_start(assertion_type, success, cached)

        if not success:
            print()
            print("    * Diff:")
            diff = difflib.ndiff(expected.splitlines(keepends=True), actual.splitlines(keepends=True))
            print('      ' + '      \n'.join(diff))

    def similar_to_assertion(self, test_suite: str, test: str, assertion_type: str, success: bool, expected: SimilarToAssertion, actual: str, score: float, cached: bool):
        self._assertion_start(assertion_type, success, cached)
        
        if not success:
            print()
            print("    * Similarity: %f" % score)
            print("    * Threshold: %f" % expected.threshold)

            # create a character diff of the expected vs reply strings:
            print("    - Diff:")
            diff = difflib.ndiff(expected.value.splitlines(keepends=True), actual.splitlines(keepends=True))
            print('      ' + '      '.join(diff))


    def end_test(self, test_suite: str, test: str, success: bool, cached: bool):
        print()
