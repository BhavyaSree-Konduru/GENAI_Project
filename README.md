# Local RAG Assistant

A retrieval-augmented generation (RAG) app that indexes a PDF into Chroma,
retrieves relevant chunks, and uses a local Ollama model to answer questions.

## Requirements

- Python 3.10 or newer
- Ollama installed and running locally
- The `llama3.2` Ollama model

## Setup (Windows PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
ollama pull llama3.2
```

Place the PDF at `data/genai_notes.pdf`, then create or refresh its Chroma index:

```powershell
python ingest.py
```

Start the chat app:

```powershell
streamlit run app.py
```

Alternatively, run the command-line chat with `python rag.py`.

The index is generated in `db/` and is intentionally excluded from version
control. Run `python ingest.py` again after changing the PDF; it replaces the
existing chunks for that PDF.

## Tests

```powershell
python -m unittest discover -s tests
```
