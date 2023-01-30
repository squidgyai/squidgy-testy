from squidgy_testy.store import TestStore

def test_store():
    store = TestStore("output/test_store.json")

    assert store.should_run("test_suite", "test_name", "v1")
    assert not store.should_run("test_suite", "test_name", "v1")
    
    assert store.should_run("test_suite", "test_name", "v2")