"""OpenAI streaming example with ChatBot widget."""

import marimo

__generated_with = "0.18.3"
app = marimo.App(width="medium")


@app.cell
def _():
    import os

    import marimo as mo
    from dotenv import load_dotenv
    from ontonaut import ChatBot

    # Load environment variables from .env file
    load_dotenv()
    return ChatBot, load_dotenv, mo, os


@app.cell
def _(mo):
    mo.md(
        """
    # OpenAI Streaming with ChatBot

    This example shows how to use the ChatBot widget with OpenAI's streaming API.

    **Setup:**
    1. Create a `.env` file in the project root
    2. Add your OpenAI API key: `OPENAI_API_KEY=sk-...`
    3. Run this notebook!
    """
    )
    return


@app.cell
def _(mo, os):
    # Check if API key is set
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        mo.md(
            """
        ⚠️ **OpenAI API key not found!**

        Please create a `.env` file in the project root with:
        ```
        OPENAI_API_KEY=sk-your-key-here
        ```
        """
        )
    else:
        mo.md("✅ OpenAI API key loaded successfully!")
    return (api_key,)


@app.cell
def _(ChatBot, api_key):
    import openai

    # Initialize OpenAI client
    client = openai.OpenAI(api_key=api_key)

    def openai_handler(user_input: str):
        """
        Stream responses from OpenAI GPT-4.

        Args:
            user_input: User's question or prompt

        Yields:
            Streaming response chunks from OpenAI
        """
        try:
            stream = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful AI assistant in a marimo notebook.",
                    },
                    {"role": "user", "content": user_input},
                ],
                stream=True,
                temperature=0.7,
            )

            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content

        except Exception as e:
            yield f"Error: {str(e)}"

    # Create ChatBot with OpenAI streaming
    chatbot = ChatBot(
        handler=openai_handler, placeholder="Ask GPT-4 anything...", theme="light"
    )

    chatbot
    return chatbot, client, openai, openai_handler


@app.cell
def _(mo):
    mo.md(
        """
    ## How It Works

    1. **Input**: Type your question in the text area above
    2. **Click Run**: Or press Cmd/Ctrl+Enter
    3. **Watch it stream**: GPT-4's response appears token-by-token
    4. **No flashing**: Smooth streaming without re-renders

    ### Under the Hood

    ```python
    def openai_handler(user_input: str):
        stream = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": user_input}],
            stream=True
        )

        for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    chatbot = ChatBot(handler=openai_handler)
    ```

    That's it! The widget handles the rest.
    """
    )
    return


@app.cell
def _(mo):
    mo.md(
        """
    ## Customize Your Handler

    You can easily customize the OpenAI handler:

    ### Add System Prompt
    ```python
    messages=[
        {"role": "system", "content": "You are a Python expert."},
        {"role": "user", "content": user_input}
    ]
    ```

    ### Change Model
    ```python
    model="gpt-3.5-turbo"  # Faster, cheaper
    model="gpt-4-turbo"    # Latest GPT-4
    ```

    ### Adjust Temperature
    ```python
    temperature=0.2  # More focused
    temperature=1.0  # More creative
    ```

    ### Add Max Tokens
    ```python
    max_tokens=500  # Limit response length
    ```
    """
    )
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
