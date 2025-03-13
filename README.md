# langgraph-agent-template

**LangGraph Agent Template** is a production-ready boilerplate designed to help you quickly build and deploy AI agents using the [LangGraph framework](https://www.langchain.com/langgraph). It comes pre-configured with Dockerized infrastructure, including **PostgreSQL** for state and history storage and **Qdrant** as a vector database for semantic search and retrieval.

In this template, you will find:
- A basic **LangGraph workflow** that demonstrates the core principles of agent orchestration.
- An integrated **vector search example** using Qdrant and OpenAI embeddings.
- Support for **LangSmith tracing** to monitor token usage, prompts, messages, and agent decisions during execution.

> ℹ️ To enable LangSmith tracing, make sure to provide your `LANGSMITH_API_KEY` and other related environment variables in the `.env` file. Once enabled, you will get detailed traces of agent execution, token usage, and message flow in your LangSmith dashboard.

> 📎 Don't forget: before running the project, create a `.env` file based on `.env.sample` and fill in all required keys (e.g., OpenAI, LangSmith, PostgreSQL connection string).

## 📚 Vector Search & Embedding Example (Qdrant)

This project includes a simple example to demonstrate how you can use vector search with Qdrant to retrieve semantically similar content and summarize it using a language model.

**Path:** `examples/vector_summary_workflow.py`

This example simulates a short user conversation, stores the messages in a vector database using OpenAI embeddings, then performs similarity search and runs a summarization over the retrieved content.

### Steps:
1. Simulate a short conversation.
2. Clean and embed each message using OpenAI's `text-embedding-ada-002` model.
3. Store embeddings in Qdrant.
4. Query Qdrant with a new message and retrieve semantically similar messages.
5. Generate a summary of the retrieved content using an LLM.

### 💡 What is RAG?

**RAG (Retrieval-Augmented Generation)** is an approach where a language model (LLM) is combined with a vector database to retrieve relevant information before generating a response.

This allows the model to work with **external knowledge or historical context**, improving accuracy and grounding.

> In simple terms: instead of asking the LLM to "remember everything", you retrieve relevant documents/messages first — and then let the model respond based on that content.

In this template, you already have the building blocks for a basic RAG pipeline:
- Embeddings
- Vector DB (Qdrant)
- Semantic retrieval
- Summarization or generation based on retrieved content

---

## 🐳 Running Local Infrastructure (PostgreSQL + Qdrant)

This template separates infrastructure (databases) from the application logic, allowing you to run your code locally while keeping vector and relational databases containerized.

### 📦 Step 1: Start infrastructure using Docker Compose

Start the PostgreSQL and Qdrant containers using the provided development configuration:

```bash
docker-compose -f docker-compose.development.yml up -d
```

This will spin up:
- **PostgreSQL** (on port `5432`) — used for storing state and checkpoints.
- **Qdrant** (on port `6333`) — used for semantic search and vector storage.

Both services are automatically initialized and mounted to local Docker volumes.

### 🔍 Step 2: Verify running containers

You can verify that the services are running using:

```bash
docker ps
```

You should see two containers: `postgres_langgraph` and `qdrant`.

### ⚙️ Step 3: Initialize PostgreSQL checkpointing tables

Before using the LangGraph workflow with PostgreSQL checkpointing, you must run the setup script once to create the necessary tables:

```bash
python scripts/setup_checkpointer.py
```

This will initialize the database with the required tables for storing workflow checkpoints.

### 💡 Step 4: Stop and remove infrastructure

When you're done, stop the containers with:

```bash
docker-compose -f docker-compose.development.yml down
```

To also remove volumes (if needed):

```bash
docker-compose -f docker-compose.development.yml down -v
```

