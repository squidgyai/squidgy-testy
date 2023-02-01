import argparse
from .runner import Runner, load_test_suites
from .recorder import Recorder
from .store import TestStore
from .gpt3 import Gpt3PromptService
import os

# run tests when executed
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Squidgy Prompts Test Runner.')

    #training arguments
    parser.add_argument('--directory', type=str, required=False, default=".")
    parser.add_argument('--test-suite', type=str, required=False)
    parser.add_argument('--test', type=str, required=False)

    args = parser.parse_args()

    test_suites = load_test_suites(args.directory, args.test_suite, args.test)

    runner = Runner(
        test_suites,
        Recorder(),
        TestStore(os.path.join(args.directory, ".squidgy_testy/squidgy_testy.json")),
        Gpt3PromptService(),
        args.directory
    )
    runner.run_tests()