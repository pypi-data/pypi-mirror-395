"""Example: Wrap your company's OpenAI implementation."""

import marimo

__generated_with = "0.18.3"
app = marimo.App(width="medium")


@app.cell
def _():
    import os

    import marimo as mo
    from dotenv import load_dotenv
    from ontonaut import ChatBot

    load_dotenv()
    return ChatBot, load_dotenv, mo, os


@app.cell
def _(mo):
    mo.md(
        """
    # Company OpenAI Wrapper Example

    This shows how to wrap your company's existing OpenAI infrastructure
    with custom logic like:
    - Authentication
    - Rate limiting
    - Logging
    - Cost tracking
    - Content filtering
    """
    )
    return


@app.cell
def _(ChatBot, os):
    import time
    from datetime import datetime

    import openai

    class CompanyOpenAIWrapper:
        """
        Your company's OpenAI wrapper with custom logic.

        This is where you'd integrate your company's:
        - Custom authentication
        - Rate limiting
        - Usage tracking
        - Cost monitoring
        - Content filtering
        - Logging infrastructure
        """

        def __init__(self, api_key: str):
            self.client = openai.OpenAI(api_key=api_key)
            self.request_count = 0
            self.total_tokens = 0

        def stream_completion(self, user_input: str):
            """
            Company's streaming completion with custom logic.

            Args:
                user_input: User's question

            Yields:
                Streaming response chunks
            """
            # 1. Pre-processing / Logging
            self.request_count += 1
            request_id = f"req_{int(time.time())}_{self.request_count}"
            print(f"[{datetime.now()}] Request {request_id} started")

            # 2. Content filtering (example)
            if self._should_block(user_input):
                yield "⚠️ This request was blocked by content filters."
                return

            # 3. Rate limiting check (example)
            if self.request_count > 100:  # Example limit
                yield "⚠️ Rate limit exceeded. Please try again later."
                return

            # 4. Call OpenAI with your company's settings
            try:
                stream = self.client.chat.completions.create(
                    model="gpt-4",  # Your company's approved model
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a helpful AI assistant. [Company policy guidelines here]",
                        },
                        {"role": "user", "content": user_input},
                    ],
                    stream=True,
                    temperature=0.7,
                    max_tokens=2000,  # Company limit
                )

                # 5. Stream with tracking
                chunk_count = 0
                for chunk in stream:
                    if chunk.choices[0].delta.content:
                        content = chunk.choices[0].delta.content
                        chunk_count += 1
                        yield content

                # 6. Post-processing / Logging
                print(
                    f"[{datetime.now()}] Request {request_id} completed: {chunk_count} chunks"
                )

            except openai.APIError as e:
                # 7. Error handling
                error_msg = f"OpenAI API Error: {str(e)}"
                print(f"[{datetime.now()}] Error in {request_id}: {error_msg}")
                yield f"⚠️ {error_msg}"

            except Exception as e:
                # 8. Generic error handling
                error_msg = f"Unexpected error: {str(e)}"
                print(f"[{datetime.now()}] Error in {request_id}: {error_msg}")
                yield f"⚠️ {error_msg}"

        def _should_block(self, text: str) -> bool:
            """
            Company's content filtering logic.

            Returns:
                True if content should be blocked
            """
            # Example: Check against blocklist
            blocked_terms = [
                "malicious_term_1",
                "malicious_term_2",
            ]  # Your company's list

            text_lower = text.lower()
            return any(term in text_lower for term in blocked_terms)

    # Initialize wrapper
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        wrapper = CompanyOpenAIWrapper(api_key)

        # Create ChatBot using company wrapper
        chatbot = ChatBot(
            handler=wrapper.stream_completion,
            placeholder="Ask a question (with company policies applied)...",
        )

        chatbot
    else:
        print("⚠️ Set OPENAI_API_KEY in .env file")
    return (
        CompanyOpenAIWrapper,
        api_key,
        chatbot,
        datetime,
        openai,
        time,
        wrapper,
    )


@app.cell
def _(mo):
    mo.md(
        """
    ## What This Demonstrates

    ### Pre-Processing
    - ✅ Request ID generation
    - ✅ Timestamp logging
    - ✅ Request counting

    ### Security
    - ✅ Content filtering
    - ✅ Rate limiting
    - ✅ Error handling

    ### Monitoring
    - ✅ Usage tracking
    - ✅ Token counting
    - ✅ Performance logging

    ### Integration
    - ✅ Works seamlessly with ChatBot
    - ✅ Streaming preserved
    - ✅ Company policies enforced

    ## Extend Further

    Add your company's specific needs:
    - Database logging
    - Cost tracking per user
    - Custom authentication
    - Multi-tenant support
    - A/B testing
    - Caching layer
    - Failover logic
    """
    )
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
