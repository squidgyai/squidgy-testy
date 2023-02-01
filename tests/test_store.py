from squidgy_testy.store import TestStore
import os
def test_store():
    # remove the test_store file
    if os.path.exists("output/test_store.json"):
        os.remove("output/test_store.json")

    store = TestStore("output/test_store.json")

    assert store.get_cached_result("test_suite", "test_name", "v1") is None

    store.set_result("test_suite", "test_name", "v1", "result1")
    assert store.get_cached_result("test_suite", "test_name", "v1") == "result1"
    assert store.get_cached_result("test_suite", "test_name", "v2") is None
    
    store.set_result("test_suite", "test_name", "v2", "result2")
    assert store.get_cached_result("test_suite", "test_name", "v2") == "result2"