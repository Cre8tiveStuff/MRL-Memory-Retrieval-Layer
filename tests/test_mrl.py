from mrl import store_fact, get_all_facts

def test_store_and_retrieve_fact():
    store_fact("test_session", "This is a test fact.")
    facts = get_all_facts()
    assert len(facts) >= 1
    assert facts[-1][0] == "test_session"
    assert facts[-1][1] == "This is a test fact."