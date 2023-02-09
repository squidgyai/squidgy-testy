from squidgy_testy.runner import Runner
from squidgy_testy.model import *
from squidgy_testy.recorder import Recorder
from squidgy_testy.store import MockTestStore

from .base_tests import *

def test_load_test_suites(mocker: MockerFixture):
    suite = TestSuite(
        tests={
            'equalTo': Test(
                prompt_file="prompt_file",
                prompt="prompt",
                params={},
                stop=[],
                assertions=[EqualToAssertion(
                    equalTo="equalTo",
                )]
            )
        }
    )

    service = mocker.Mock()
    service.invoke = mocker.Mock(return_value="equalTo")

    # patch the generate_prompt method to return the prompt
    mocker.patch("squidgy_testy.runner.generate_prompt", return_value="prompt")

    recorder = Recorder()

    runner = Runner({"suite" : suite}, recorder, MockTestStore(), service)

    runner.run_tests()