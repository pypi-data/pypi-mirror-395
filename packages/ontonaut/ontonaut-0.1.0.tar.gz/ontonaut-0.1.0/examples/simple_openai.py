"""Simplest OpenAI streaming example."""

import marimo

__generated_with = "0.18.3"
app = marimo.App(width="medium")


@app.cell
def _():
    import os

    from dotenv import load_dotenv
    from ontonaut import ChatBot

    # Load .env file
    load_dotenv()
    return ChatBot, os


@app.cell(hide_code=True)
def _(ChatBot, os):
    import openai

    # Get API key from .env
    api_key = os.getenv("OPENAI_API_KEY")

    # Initialize OpenAI client
    client = openai.OpenAI(api_key=api_key)

    # Define streaming handler
    def stream_openai(user_input: str):
        """Stream from OpenAI GPT-4."""
        stream = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": user_input}],
            stream=True,
        )

        for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    # Create widget
    chatbot = ChatBot(handler=stream_openai, theme="dark")
    chatbot
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
