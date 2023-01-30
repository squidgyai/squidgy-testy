from squidgy_testy.runner import *

def test_load_test_suites():
    suites = load_test_suites(".", "test_parsing")

    assert len(suites) == 1

    suite = suites['test_parsing']

    assert suite is not None

    test = suite.tests['equalTo']
    
    assert test is not None
    assert test.assertions.equalTo == "equalTo"
