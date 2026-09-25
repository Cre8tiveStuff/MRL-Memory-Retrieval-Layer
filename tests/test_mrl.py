from mrl import store_fact, search_facts

def test_search_finds_relevant_fact():
    store_fact("test_session", "The favorite repository is procurement-rag.")
    store_fact("test_session", "ARC uses Redis for atomic locking.")

    results = search_facts("what does the user like best?", top_k=1)

    assert len(results) == 1
    assert "procurement-rag" in results[0][2]