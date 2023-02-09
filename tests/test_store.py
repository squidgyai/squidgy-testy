from squidgy_testy.store import TestStore
import os
def test_store():
    # remove the test_store file
    if os.path.exists(".squidgy_testy/test_store.json"):
        os.remove(".squidgy_testy/test_store.json")

    store = TestStore(".squidgy_testy/test_store.json")

    assert store.get_cached_result("test_suite", "test_name", "v1", ['stop']) is None

    store.set_result("test_suite", "test_name", "v1", ['stop'], "result1")
    assert store.get_cached_result("test_suite", "test_name", "v1", ['stop']) == "result1"
    assert store.get_cached_result("test_suite", "test_name", "v2", ['stop']) is None
    
    store.set_result("test_suite", "test_name", "v2", ['stop'], "result2")
    assert store.get_cached_result("test_suite", "test_name", "v2", ['stop']) == "result2"