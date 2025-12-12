# Ontonaut Examples

Example marimo notebooks demonstrating Ontonaut widgets.

## Setup

1. **Install dependencies:**
   ```bash
   cd /Users/ashleycottrell/dev/repos/ontonaut
   source .venv/bin/activate
   uv pip install openai python-dotenv  # Already installed!
   ```

2. **Configure API keys:**

   Your `.env` file is already set up! It should contain:
   ```
   OPENAI_API_KEY=sk-...
   ```

3. **Run examples:**
   ```bash
   marimo edit examples/simple_openai.py
   marimo edit examples/openai_streaming.py
   marimo edit examples/company_openai_wrapper.py
   ```

## 📚 Examples

### `simple_openai.py`
**The simplest OpenAI streaming example**
- Loads API key from `.env`
- Basic GPT-4 streaming
- ~20 lines of code

```python
from ontonaut import ChatBot
import openai

client = openai.OpenAI(api_key=api_key)

def stream_openai(user_input: str):
    stream = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": user_input}],
        stream=True
    )
    for chunk in stream:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

chatbot = ChatBot(handler=stream_openai)
```

### `openai_streaming.py`
**Full-featured OpenAI example**
- System prompts
- Temperature control
- Error handling
- Documentation

### `company_openai_wrapper.py`
**Production-ready company wrapper**
- Custom authentication
- Rate limiting
- Content filtering
- Request logging
- Cost tracking
- Error handling

Perfect for integrating your company's existing OpenAI infrastructure!

### `basic_usage.py`
**CodeEditor examples**
- Custom code executors
- Different languages
- DSL examples

### `chatbot_examples.py`
**Various handler examples**
- Echo handler (testing)
- Custom handlers
- MCP integration

## 🚀 Quick Test

```bash
# Run the simple example
marimo edit examples/simple_openai.py

# Type something like:
# "Explain what marimo is in one sentence"

# Watch it stream! ✨
```

## 📝 Notes

- All examples load API key from `.env`
- The `.env` file is gitignored for security
- Streaming is smooth with no flashing
- Both ChatBot and CodeEditor work together
- Use Cmd/Ctrl+Enter to execute

## 🔧 Troubleshooting

**"Module not found: openai"**
```bash
uv pip install openai
```

**"API key not found"**
- Check your `.env` file exists
- Verify `OPENAI_API_KEY=sk-...` is set
- Make sure you're running from the project root

**"ImportError: python-dotenv"**
```bash
uv pip install python-dotenv
```

## 🎯 Your Turn

Modify `company_openai_wrapper.py` to match your company's:
- Authentication system
- Rate limiting logic
- Logging infrastructure
- Custom policies
- Cost tracking

The widget handles streaming automatically - you just yield chunks!
