
# Local RAG: Enterprise Policy Search

A fully local **Retrieval-Augmented Generation (RAG)** application built to query internal business documents without sending data to the cloud.

This project demonstrates how to build a scalable AI search engine using **Ollama** for local LLM inference, **ChromaDB** for vector storage, and **LangChain** for orchestration—all running efficiently on a standard CPU.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Ollama](https://img.shields.io/badge/AI-Ollama-orange)
![ChromaDB](https://img.shields.io/badge/Vector%20DB-Chroma-green)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-red)

## Features

*   **100% Local Privacy:** No data leaves your machine. No API keys required.
*   **CPU Optimized:** Uses `llama3.2` (3B) and `nomic-embed-text` for fast performance on non-GPU hardware.
*   **Scalable Architecture:** Capable of ingesting and searching through 500+ markdown documents.
*   **Modern Stack:** Managed with `uv` for lightning-fast dependency resolution.
*   **Interactive UI:** Clean chat interface built with Streamlit.

## Tech Stack

*   **LLM:** Llama 3.2 (via Ollama)
*   **Embeddings:** Nomic Embed Text
*   **Vector Database:** ChromaDB (Persistent storage)
*   **Framework:** LangChain & LangChain Community
*   **Frontend:** Streamlit
*   **Package Manager:** UV

## Prerequisites

1.  **Install UV:** (Fast Python package manager)
    *   Mac/Linux: `curl -LsSf https://astral.sh/uv/install.sh | sh`
    *   Windows: `powershell -c "irm https://astral.sh/uv/install.ps1 | iex"`

2.  **Install Ollama:** [Download here](https://ollama.com/).

3.  **Pull Required Models:**
    Run these commands in your terminal to download the models locally:
    ```bash
    ollama pull nomic-embed-text
    ollama pull llama3.2
    ```

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/local-rag-project.git
    cd local-rag-project
    ```

2.  **Initialize environment & Install dependencies:**
    ```bash
    uv init
    uv sync
    ```

## Usage Guide

### 1. Generate Dummy Data (Optional)
If you don't have your own markdown files, generate 500 realistic corporate policy documents to test scalability.
```bash
uv run python generate_data.py
```

### 2. Ingest Documents
Process the markdown files, chunk them into smaller pieces, generate embeddings, and store them in ChromaDB.
```bash
uv run python ingest_scaled.py
```
*Note: On a CPU, processing 500 files may take a few minutes. You only need to run this once.*

### 3. Launch the Application
Start the Streamlit interface.
```bash
uv run streamlit run app_scaled.py
```

## How It Works (Architecture)

1.  **Ingestion:**
    *   Documents are loaded from the `/data` directory.
    *   Text is split into chunks (1000 chars) with overlap to preserve context.
    *   Chunks are converted into vector embeddings using `nomic-embed-text`.
    *   Vectors are stored locally in `./chroma_db`.

2.  **Retrieval & Generation:**
    *   User asks a question via Streamlit.
    *   The question is embedded into a vector.
    *   ChromaDB finds the top 5 most similar document chunks.
    *   These chunks + the user question are sent to `llama3.2`.
    *   The LLM generates an accurate answer based *only* on the provided context.

## Project Structure

```
├── data/                  # Source markdown files
├── chroma_db/             # Vector database storage (created after ingestion)
├── app_scaled.py          # Main Streamlit application
├── ingest_scaled.py       # Logic for loading and vectorizing documents
├── generate_data.py       # Script to create dummy dataset
├── pyproject.toml         # Dependency definitions (UV)
└── README.md              # Project documentation
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
