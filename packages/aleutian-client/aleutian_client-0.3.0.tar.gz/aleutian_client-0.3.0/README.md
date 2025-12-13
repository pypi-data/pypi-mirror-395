# Aleutian Client (Python SDK)

[![PyPI version](https://badge.fury.io/py/aleutian-client.svg)](https://badge.fury.io/py/aleutian-client)
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)

The official Python client SDK for the **[AleutianLocal MLOps platform](https://github.com/jinterlante1206/AleutianLocal)**.

This package allows developers, data scientists, and applications to programmatically interact with a running AleutianLocal stack to perform:
* Retrieval-Augmented Generation (RAG) queries
* Direct-to-LLM chat sessions
* Timeseries forecasting
* Session management
* And more, all through a simple Python API.

---

## Prerequisites

**This package is a client library.** It **requires** the full **[AleutianLocal](https://github.com/jinterlante1206/AleutianLocal)** stack to be installed and running on your local machine.

Before using this package, please ensure you have:
1.  Installed the `aleutian` CLI (see the [main project for instructions](https://github.com/jinterlante1206/AleutianLocal#installation)).
2.  Started the Aleutian stack:

    ```bash
    # Make sure your Podman machine and Ollama are running
    aleutian stack start
    ```

The `AleutianClient` will connect to the `orchestrator` service, which runs on `http://localhost:12210` by default.

## Installation

You can install the client using `pip`:

```bash
pip install aleutian-client
````

## Quickstart & Usage

The client is designed to be used with a context manager (the `with` statement), which automatically handles opening and closing the connection.

Here is a complete example showing the most common operations.

```python
import sys
from aleutian_client import AleutianClient, Message
from aleutian_client import AleutianConnectionError, AleutianApiError

def main():
    try:
        # 1. Connect to the running Aleutian stack
        # Defaults to host="http://localhost", port=12210
        with AleutianClient() as client:

            # 2. Run a health check to verify connection
            health = client.health_check()
            print(f"Successfully connected to Aleutian: {health.get('status')}")

            # -------------------------------------------------
            # Example 1: Direct Ask (No RAG)
            # This sends the query directly to the configured LLM.
            # -------------------------------------------------
            print("\n--- 1. Direct LLM Ask (no RAG) ---")
            try:
                # Use no_rag=True to bypass RAG
                response_ask = client.ask(
                    query="What is the capital of France?", 
                    no_rag=True
                )
                print(f"LLM Answer: {response_ask.answer}")
            except AleutianApiError as e:
                print(f"API Error: {e}")


            # -------------------------------------------------
            # Example 2: RAG-Powered Ask
            # Assumes you have already populated data, e.g.:
            # aleutian populate vectordb ./my_documents
            # -------------------------------------------------
            print("\n--- 2. RAG-Powered Query ---")
            try:
                # no_rag=False (default) uses the 'reranking' pipeline
                response_rag = client.ask(
                    query="What is AleutianLocal?",
                    pipeline="reranking" # or "standard"
                )
                print(f"RAG Answer: {response_rag.answer}")
                
                if response_rag.sources:
                    sources = [s.source for s in response_rag.sources]
                    print(f"Sources: {sources}")
                else:
                    print("No sources found. (Is data populated?)")
            
            except AleutianApiError as e:
                print(f"API Error: {e}")


            # -------------------------------------------------
            # Example 3: Direct Chat Session
            # This uses the /v1/chat/direct endpoint.
            # -------------------------------------------------
            print("\n--- 3. Direct Chat Session ---")
            try:
                # The chat method takes a list of Message objects
                messages = [
                    Message(role="user", content="Hello! Please introduce yourself briefly.")
                ]
                response_chat = client.chat(messages=messages)
                print(f"Chat Answer: {response_chat.answer}")
            
            except AleutianApiError as e:
                print(f"API Error: {e}")


    except AleutianConnectionError:
        print("\nError: Could not connect to AleutianLocal stack.", file=sys.stderr)
        print("Please ensure the stack is running with 'aleutian stack start'.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

```

## License

This project is licensed under the GNU Affero General Public License v3.0.
