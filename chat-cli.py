import json
import requests
from memory import init_db, add_turn, get_recent_turns, clear_memory

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.1:8b"


def era_check_and_rewrite(persona: str, user: str, assistant: str) -> str:
    check_prompt = f"""{persona}

You are performing a strict compliance check.

Task:
1) Determine if the Assistant answer contains any post-1956 knowledge, modern technology, or anachronistic language.
2) If it violates, rewrite it to be fully consistent with 1956 knowledge and speech.
3) If it does NOT violate, return the original answer unchanged.

Return ONLY the final assistant answer (no explanation).

User: {user}
Assistant: {assistant}
Final:"""
    return ask(check_prompt)


def load_persona(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()


def ask(prompt: str) -> str:
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        # You can control creativity later:
        "options": {
            "temperature": 0.7,
            "top_p": 0.9
        }
    }
    r = requests.post(OLLAMA_URL, json=payload, timeout=120)
    r.raise_for_status()
    return r.json()["response"].strip()


def main():
    persona = load_persona("persona-1956.txt")
    with open("character.json", "r") as f:
        character = json.load(f)
        character_block = json.dumps(character, indent=2)
    init_db()
    print("1956 Agent CLI. Type 'exit' to quit.\n")

    recent = get_recent_turns(limit=12)
    history = "\n".join([f"{r.capitalize()}: {c}" for r, c in recent])

    while True:
        user = input("You: ").strip()
        if user.lower() in {"exit", "quit"}:
            break

        if user.lower() == "/reset":
            clear_memory()
            print("\n(Memory cleared.)\n")
            continue

        prompt = f"""{persona}

Character sheet:
{character_block}

Conversation so far:
{history}

User: {user}
Assistant:"""

        assistant_raw = ask(prompt)
        assistant = era_check_and_rewrite(persona, user, assistant_raw)
        print(f"\nAssistant: {assistant}\n")
        add_turn("user", user)
        add_turn("assistant", assistant)

        # Append to history (keep it short for now)
        history += f"User: {user}\nAssistant: {assistant}\n"


if __name__ == "__main__":
    main()
