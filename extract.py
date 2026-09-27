import ollama
import json

EXTRACTION_PROMPT = """You are analyzing a conversation to decide what facts should be remembered for future sessions.

Read the conversation below. Extract 0-3 genuinely important facts worth remembering long-term.
For each fact, assign ONE category: preference, technical_fact, or project_status.

Respond ONLY with valid JSON, in this exact format:
[{{"fact": "...", "category": "..."}}]

If nothing is worth remembering, respond with an empty list: []

CONVERSATION:
{conversation}
"""


def extract_facts(conversation_text, model_name="llama3.1:8b"):
    prompt = EXTRACTION_PROMPT.format(conversation=conversation_text)
    response = ollama.generate(model=model_name, prompt=prompt)
    raw_output = response.get("response", "").strip()

    try:
        facts = json.loads(raw_output)
        return facts
    except json.JSONDecodeError:
        return []
