from squidgy_testy.runner import *

def test_load_test_suites():
    suites = load_test_suites(".", "test_parsing")

    assert len(suites) == 1

    suite = suites['test_parsing']

    assert suite is not None

    test = suite.tests['equalTo']
    
    assert test is not None
    assert type(test.assertions[0]) == EqualToAssertion
    assert test.assertions[0].equalTo == "equalTo"

    assert type(test.assertions[1]) == SimilarToAssertion
    assert test.assertions[1].similarTo.value == "similarTo"

    assert type(test.assertions[2]) == StartsWithAssertion
    assert test.assertions[2].startsWith == "startsWith"


def test_example():
    suites = load_test_suites("./example")

    assert len(suites) == 1