# 1956 Person

A CLI chatbot that roleplays as a person living in 1956 California, using a local LLM via Ollama.

## How It Works

- **Persona system**: Uses a detailed prompt (`persona-1956.txt`) to constrain the AI to 1956-era knowledge and speech patterns
- **Character sheet**: Defines "Frank", a 34-year-old automotive shop foreman in Sacramento with period-appropriate values and interests
- **Era compliance check**: Two-pass generation that first produces a response, then validates/rewrites it to remove any anachronisms
- **Persistent memory**: SQLite database stores conversation history across sessions

## Requirements

- Python 3.x
- [Ollama](https://ollama.ai) running locally with `llama3.1:8b` model
- `requests` library

## Usage

```bash
# Start Ollama with the model
ollama run llama3.1:8b

# Run the chatbot
python chat-cli.py
```

Type your messages and chat with Frank. Type `exit` or `quit` to end the session.

## Files

- `chat-cli.py` - Main CLI application
- `memory.py` - SQLite conversation storage
- `character.json` - Character definition (editable)
- `persona-1956.txt` - System prompt with era rules
