# 💼 FinCon & Financial Regulatory Intelligence Assistant

**An AI-powered Hierarchical Hybrid RAG System for Financial Controlling and Regulatory Compliance**

FinCon RAG is an intelligent document question-answering system designed to help users retrieve and understand financial controlling information, accounting standards, and regulatory requirements.

The system combines **Query Expansion, Named Entity Recognition, Hybrid Retrieval, Hierarchical Parent-Child Indexing, Cross-Encoder Reranking, and LLM-based Answer Generation** to deliver relevant, context-grounded answers with source attribution.

---

## 🌟 Key Features

### 1. Hierarchical Parent-Child Indexing

The system uses a hierarchical document structure to balance retrieval precision and contextual completeness.

- Documents are parsed and split into Parent Chunks and Child Chunks.
- Child Chunks are used for precise retrieval.
- Retrieved Child Chunks are mapped back to their corresponding Parent Chunks.
- Parent contexts are passed to the LLM to provide more complete information.

This approach helps avoid losing important context when retrieving small text segments.

### 2. Persistent Vector Database – ChromaDB

- Uses ChromaDB for dense vector storage and semantic retrieval.
- Uses `PersistentClient` to persist indexed data locally.
- Allows previously generated embeddings and indexed chunks to be reused instead of rebuilding the vector database every time.
- Supports collection-based document storage and retrieval.

### 3. Hybrid Search (Dense + Sparse Retrieval)

The retrieval layer combines two complementary approaches:

- **Dense Retrieval (ChromaDB):** Finds semantically related content using vector embeddings.
- **Sparse Retrieval (BM25):** Finds relevant documents based on exact keywords, financial terminology, and regulatory references.

The results are combined using **Reciprocal Rank Fusion (RRF)** to produce a unified candidate ranking.

### 4. Pre-Retrieval Query Expansion & NER

Before retrieving documents, the system enriches the original query.

- **Named Entity Recognition (NER):** Extracts financial entities using spaCy.
- **Query Expansion:** Adds relevant financial and domain-specific terminology.
- The expanded query is used for retrieval, while the original query is retained for reranking.

This helps improve retrieval when users ask questions using different terminology.

### 5. Cross-Encoder Reranking

The retrieved candidate chunks are passed through:

`BAAI/bge-reranker-base`

The Cross-Encoder evaluates the relevance of each candidate against the original query and reorders the results.

This improves the quality of the final retrieved context before generation.

### 6. Grounded Answer Generation

- Uses Groq-powered LLM generation through LangChain's `ChatGroq`.
- Combines the original question with retrieved Parent Chunk contexts.
- Uses financial-domain prompts to guide answer generation.
- Provides source attribution based on retrieved document metadata.

### 7. RAG Evaluation Suite

The project includes a RAG evaluation pipeline based on **RAGAS**.

Evaluation uses a golden benchmark dataset containing **30 questions** and measures:

| Metric | Purpose |
|---|---|
| Faithfulness | Measures whether the answer is supported by the retrieved context. |
| Answer Relevancy | Measures how relevant the generated answer is to the question. |
| Context Precision | Measures how relevant the retrieved context is. |
| Context Recall | Measures how much of the required ground-truth information was retrieved. |

The evaluation LLM uses Groq's `openai/gpt-oss-120b` model.

Evaluation results are saved in JSON format for further analysis.

---

## 🏗️ System Architecture

```text
                    User Question
                          |
                          v
                Query Expansion + NER
                          |
                          v
                 Expanded Query
                          |
                          v
                  Hybrid Retrieval
                   /           \
                  /             \
          Dense Search        BM25 Search
           ChromaDB             Sparse
                  \             /
                   \           /
                          |
                          v
                   RRF Fusion
                          |
                          v
                  Candidate Chunks
                          |
                          v
                 Cross-Encoder Reranker
                          |
                          v
                 Top-K Child Chunks
                          |
                          v
                Parent Context Expansion
                          |
                          v
                   Grounded Prompt
                          |
                          v
                    Groq LLM
                          |
                          v
                 Answer + Sources
```

---

## 📊 Ingestion Statistics

A successful ingestion run produced the following dataset statistics:

| Component | Count |
|---|---:|
| Parsed Documents | 75,029 |
| Parent Chunks | 89,581 |
| Child Chunks | 369,503 |

**Storage:**
- Parent documents are persisted in `data/parent_docstore.json`.
- Child embeddings are stored in the persistent ChromaDB database.
- Sparse retrieval data is maintained by the retrieval indexing component.

*These figures represent the observed ingestion run and may change when the source dataset changes.*

---

## 🚀 Installation & Quickstart

### 1. Clone the Repository

```bash
git clone https://github.com/AsmaaSalem246/Fincon_Rag.git
cd Fincon_Rag
```

### 2. Create a Conda Environment

```bash
conda create -n fincon-rag python=3.11 -y
conda activate fincon-rag
```

### 3. Install Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create your `.env` file based on `.env.example` and configure the required API credentials and model settings.

**Important:** Never commit your actual `.env` file or expose API keys.

### 5. Ingest Financial Documents

Run the ingestion pipeline from the project root:

```bash
python -m src.ingestion.run_ingestion
```

This processes the raw documents, generates hierarchical chunks, builds the retrieval indexes, and persists the generated data.

**Note:** If the persistent indexes already exist and are compatible with the current configuration, reuse them rather than rebuilding them unnecessarily.

### 6. Run the Streamlit Application

```bash
streamlit run ui/streamlit_app.py
```

The application provides:
- Financial question input.
- Configurable Top-K reranking.
- Generated answers.
- Recognized financial entities.
- Expanded queries.
- Source attributions.
- Retrieved Child Chunk inspection.
- Cross-Encoder and RRF scores.
- Full Parent Context inspection.

### 7. Launch the FastAPI Backend

```bash
uvicorn api.app:app --host 0.0.0.0 --port 8000 --reload
```

API documentation:

`http://localhost:8000/docs`

### 8. Run RAG Evaluation

```bash
python -m src.evaluation.evaluate_rag
```

The evaluation pipeline uses the golden evaluation dataset and calculates the four RAGAS metrics.

Results are saved to:

```text
data/ragas_evaluation_results.json
```

---

## 📁 Project Structure

```text
Fincon_Rag/
│
├── api/
│   └── app.py
│
├── data/
│   ├── raw/
│   ├── golden_eval_set.json
│   ├── parent_docstore.json
│   └── ragas_evaluation_results.json
│
├── src/
│   ├── config.py
│   │
│   ├── ingestion/
│   │   ├── parser.py
│   │   ├── hierarchical.py
│   │   ├── indexer.py
│   │   ├── load_baai_dataset.py
│   │   └── run_ingestion.py
│   │
│   ├── retrieval/
│   │   ├── hybrid_search.py
│   │   ├── query_expansion.py
│   │   └── reranker.py
│   │
│   ├── generation/
│   │   ├── chain.py
│   │   └── prompts.py
│   │
│   └── evaluation/
│       └── evaluate_rag.py
│
├── ui/
│   └── streamlit_app.py
│
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .gitignore
└── README.md
```

---

## 🛠️ Technology Stack

| Category | Technologies |
|---|---|
| Language | Python |
| LLM Integration | Groq, LangChain |
| Vector Database | ChromaDB |
| Dense Embeddings | Sentence Transformers |
| Sparse Retrieval | BM25 |
| Retrieval Fusion | Reciprocal Rank Fusion (RRF) |
| Reranking | BAAI/bge-reranker-base |
| NLP & NER | spaCy |
| RAG Evaluation | RAGAS |
| Frontend | Streamlit |
| Backend | FastAPI |
| Deployment & Containerization | Docker, Docker Compose |

---

## 🎯 Project Objectives

- Build a scalable financial document retrieval system.
- Improve retrieval quality through hybrid search and reranking.
- Preserve document context using hierarchical indexing.
- Generate grounded answers from financial and regulatory documentation.
- Evaluate retrieval and generation quality using established RAG metrics.
- Provide an interactive interface for financial question answering.

---

