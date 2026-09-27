# MRL
### Memory Retrieval Layer

**Open towards Team Collaborations & Contract Opportunities.**

A self-curating memory system for AI agents: reads a conversation, decides what's worth remembering, categorizes it, and makes it retrievable by meaning in future sessions — closing the "Memory: unowned" gap identified in the original six-component context-engineering framework this whole system was built against.

## Why this matters architecturally

Most agent memory implementations are either nothing (every session starts from zero) or everything (raw conversation logs, unfiltered and unstructured). MRL is neither — it's a genuine six-layer pipeline, each layer doing exactly one job, independently testable and independently correct:

| Layer | Function | Job |
|---|---|---|
| 1. Persistence | init_memory_db() | Schema: session, fact, category, embedding, timestamp |
| 2. Representation | embed_fact() | Text to vector, via the same model procurement-rag uses |
| 3. Write Path | store_fact() | Embed once, at write-time, not on every future read |
| 4. Read Path | get_all_facts_with_embeddings() | Deserialize stored vectors back into usable form |
| 5. Retrieval | search_facts() | Semantic ranking, with optional category filtering |
| 6. Extraction | process_conversation() | An LLM call judges its own conversation, the genuinely new mechanism |

## The real proof, not a claim

A raw conversation went in. No human decided what to store. llama3.1:8b extracted three genuinely distinct facts, correctly categorized each one, and a later semantic search using words that never appeared in the original text correctly retrieved the right one.

## A real architectural lesson learned building this

Serialization has a real, measurable cost: a 384-dimension embedding is about 1,536 bytes as raw binary, but roughly 3-4x larger once serialized to JSON text for SQLite storage. Fine at MRL's current scale; a genuine, honest scaling constraint at production volume.

## Status

| Component | Status |
|---|---|
| Storage layer | Built, tested |
| Semantic search | Built, tested |
| Scaling fix | Built, tested |
| Taxonomy filtering | Built, tested |
| LLM extraction layer | Built, tested, verified end-to-end |
| Integration with CCL/O2A | Not yet wired in |

## Installation

git clone https://github.com/Cre8tiveStuff/MRL-Memory-Retrieval-Layer.git
cd MRL-Memory-Retrieval-Layer
python3 -m venv venv
source venv/bin/activate
pip install -e .

Requires Ollama running locally with llama3.1:8b pulled.

## Running tests

pytest tests/

## Related projects

Part of a six-repo system. Uses the same embedding model as procurement-rag; designed to eventually feed into CCL and O2A's agent loop.

---

Building in the open, feedback and collaboration welcome.