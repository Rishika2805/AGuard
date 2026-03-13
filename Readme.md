# AGuard AI Agent – Complete Project Guide

![Python](https://img.shields.io/badge/Python-3.11-blue)
![LangGraph](https://img.shields.io/badge/LangGraph-Agent-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)


> **Goal:** Build an autonomous AI agent that filters noisy information from Gmail and Reddit, surfaces only relevant content, and notifies the user with explanations.

---

## 1. Problem Statement

Modern users are overwhelmed by emails and social content. Important signals are buried under promotions, rants, and low-value posts. Skimming manually is time-consuming and unreliable.

**Objective:** Reduce noise first, then apply intelligence. Notify only when content crosses a confidence threshold.

---

## 2. High-Level Architecture

**Pipeline:**

* Scheduler → Fetch → Preprocess → Hard Filters → LLM Gate → Relevance Scoring → Decision → Notify → Log & Memory

**Simple Architecture Diagram:**

```text
[Gmail API]      [Reddit RSS]
     |                |
     +------ Fetch ----+
               |
         Preprocess
               |
        Hard Rules Gate
         |            |
       Drop         Pass
                      |
             Vector Similarity
                      |
                 LLM Gate
               |         |
             Reject    Allow
                         |
                   Final Decision
                |      |      |
              Ignore Archive Notify
                       |      |
                     Email Telegram
```

**Sources (V1):**

* Gmail (official Gmail API, read-only)
* Reddit (official RSS feeds)

**Why RSS for Reddit (V1):**

* Official, read-only, no auth friction
* Stable and reliable
* Fetchers remain interchangeable for future API swap

---
# AGuard AI Agent

An AI-powered content triage pipeline that fetches data from Gmail and Reddit, filters low-value/noisy content, scores relevance with rule-based + vector + LLM signals, and sends actionable notifications.

---

## 1) Project Overview

AGuard is built as a multi-stage agent workflow using LangGraph. It ingests content from multiple sources, normalizes and preprocesses it, stores it in SQLite and ChromaDB, evaluates relevance with hard rules and LLM judgment, then routes results to Telegram and Email.

The core objective is to reduce information overload by surfacing only high-signal items.

---

## 2) Problem the Project Solves

Users receive too much content (emails, social posts, discussions) and cannot manually review everything efficiently. Important opportunities and updates are often missed.

This project solves that by:

- Automating multi-source ingestion.
- Removing obvious noise early with deterministic filtering.
- Using semantic memory and LLM scoring for better prioritization.
- Delivering concise summaries through notification channels.

---

## 3) Features

- **Multi-source ingestion**
  - Gmail via Gmail API (OAuth, read-only scope).
  - Reddit via subreddit RSS feeds.
- **Unified item schema** for source-agnostic processing.
- **Text preprocessing**
  - HTML stripping, normalization, boilerplate cleanup, metadata enrichment (`word_count`, `has_links`).
- **Hard-rule gate**
  - Keyword inclusion/exclusion logic from user preferences.
  - Minimum-content thresholding.
  - Duplicate-content blocking through content hash storage.
- **Vector memory (ChromaDB)**
  - Embedding generation with `sentence-transformers`.
  - Similarity search and average similarity scoring.
- **LLM relevance gate**
  - Structured JSON decision (`Allowed` / `Rejected`) with confidence and reason.
- **Final decision engine**
  - Weighted score fusion and outcome bands: `Notify`, `Archive`, `Ignore`.
- **Summary generation**
  - Short notification-ready summaries via LLM.
- **Notification delivery**
  - Telegram (interactive message with Ignore callback button).
  - Email (HTML + plain text fallback).
- **Persistent logging**
  - Content records and decision records in SQLite.

---

## 4) System Architecture / Workflow

The main runtime compiles a LangGraph pipeline with conditional branches:

1. **fetch_and_parse**
   - Collect Gmail + Reddit items.
   - Deduplicate and sort.
2. **preprocessor**
   - Build clean `full_text` and metadata features.
3. **store**
   - Insert content into SQLite (`content_items`) with content hash.
4. **hard_rules**
   - Score and classify as `PASS_TO_LLM` or `DROP`.
   - Log rule decision in `decisions` table.
   - If none pass, graph ends.
5. **vector**
   - Upsert embeddings to Chroma.
   - Query similarity and attach `similarity_score`.
6. **llm**
   - Run LLM structured evaluation.
   - Keep only `Allowed` items.
   - If none remain, graph ends.
7. **decision**
   - Compute final weighted score:

   final_score =
   0.25 * hard_rule_score +
   0.25 * similarity_score +
   0.50 * llm_score

   - Route to `Notify`, `Archive`, or `Ignore`.
8. **notify**
   - Telegram for notify items.
   - Email for archive items.

Each node is wrapped with a safety decorator to prevent full pipeline crashes on per-node exceptions.

---

## 5) Tech Stack

- **Language:** Python 3.11
- **Workflow orchestration:** LangGraph
- **LLM framework:** LangChain
- **LLM providers used in code:**
  - Groq (`llama-3.1-8b-instant`) for relevance evaluation
  - OpenAI (`gpt-4o-mini`) for summary generation
- **Vector database:** ChromaDB (persistent local store)
- **Embeddings:** `sentence-transformers` (`BAAI/bge-base-en-v1.5`)
- **Structured validation:** Pydantic
- **Data ingestion:**
  - Gmail API (`google-api-python-client`, OAuth)
  - Reddit RSS (`feedparser`)
- **Storage:** SQLite
- **Notifications:**
  - SMTP email (Gmail SMTP SSL)
  - Telegram Bot API
- **Config:** YAML + environment variables (`python-dotenv`)

---

## 6) Project Structure

```text
AGuard-AI-Agent/
├── main.py                          # Entry point — builds and runs LangGraph pipeline
├── requirements.txt                 # Python dependencies
├── .env                             # Environment variables (not committed)
│
├── agents/                          # Core processing logic
│   ├── fetch_data.py                # Gmail + Reddit collection, dedup, sort
│   ├── preprocessor.py              # Text cleaning and metadata enrichment
│   ├── hard_rules.py                # Deterministic scoring and filtering
│   ├── similarity.py                # Chroma cosine distance → similarity score
│   ├── llm_gate.py                  # Structured LLM relevance evaluation
│   ├── prompting.py                 # System + human prompts for the evaluator
│   ├── decision.py                  # Weighted score fusion and decision bands
│   └── summary_llm.py               # LLM-powered notification summary generation
│
├── graph/                           # LangGraph workflow definition
│   ├── graph.py                     # Node registration and edge/route topology
│   ├── nodes.py                     # Node function implementations
│   ├── langgraph_routes.py          # Conditional branch routing logic
│   ├── state.py                     # Typed pipeline state schema (TypedDict)
│   ├── safe_node.py                 # Exception-safe node decorator
│   └── logger.py                    # Centralised logging configuration
│
├── sources/                         # Data source connectors
│   ├── gmail/
│   │   ├── auth/auth.py             # Gmail OAuth2 flow and service creation
│   │   ├── fetcher.py               # Gmail message ID and payload fetching
│   │   └── parser.py                # Gmail payload → normalised item schema
│   └── reddit/
│       ├── fetcher.py               # Subreddit RSS feed retrieval
│       └── parser.py                # RSS entry → normalised item schema
│
├── database/                        # Persistence layer
│   ├── db.py                        # SQLite connection factory
│   ├── schema.py                    # Table definitions (content_items, decisions)
│   └── repos/
│       ├── content_repo.py          # Content insert with SHA-256 hash dedup
│       └── decision_repo.py         # Decision log repository
│
├── memory/                          # Vector memory (ChromaDB)
│   ├── embedder.py                  # SentenceTransformer model and encode helper
│   ├── chroma_client.py             # Persistent Chroma client setup
│   └── vector_repo.py               # Upsert embeddings and similarity search
│
├── notification/                    # Notification delivery channels
│   ├── email.py                     # SMTP/SSL email with HTML template
│   ├── telegram.py                  # Telegram bot with inline callback buttons
│   ├── console.py                   # Local console notifier
│   └── dispatcher.py                # Multi-channel dispatch helper
│
├── config/
│   ├── loader.py                    # YAML config loader
│   └── user_preferences.yaml        # Topics, keywords, senders, thresholds
│
├── scripts/                         # Local utility and debug scripts
│   ├── check_env.py                 # Verify environment variables are set
│   ├── check_email.py               # Test email notification delivery
│   ├── check_telegram.py            # Test Telegram notification delivery
│   └── test_embedding.py            # Verify embedding model output
│                    
└── utils/
    └── stream_utils.py              # Dedup, sort, and stream print helpers
```

---

## 7) Installation

### Prerequisites

- Python 3.11+
- Gmail API OAuth credentials (desktop app)
- Telegram bot (optional but recommended)
- API access keys for Groq and OpenAI

### Steps

1. **Clone repository**

```bash
git clone <your-repo-url>
cd AGuard-AI-Agent
```

2. **Create and activate virtual environment**

```bash
python -m venv .venv
```

Windows (PowerShell):

```bash
.\.venv\Scripts\Activate.ps1
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

> `requirements.txt` lists only the direct project dependencies grouped by purpose (orchestration, LLM, vector memory, ingestion, notifications, config).

4. **Set up Gmail OAuth files**

- Place your Google OAuth client file at:
  - `sources/gmail/auth/credential.json`
- On first run, token will be created at:
  - `sources/gmail/auth/token.json`

5. **Create database tables**

```bash
python -c "from database.schema import create_tables; create_tables()"
```

---

## 8) Environment Variables

Create a `.env` file in project root:

```env
# Email
EMAIL_SENDER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
EMAIL_RECEIVER=receiver_email@gmail.com

# Telegram
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_chat_id

# LLM Providers
GROQ_API_KEY=your_groq_api_key
OPENAI_API_KEY=your_openai_api_key
```

Used directly in code:

- `EMAIL_SENDER`, `EMAIL_PASSWORD`, `EMAIL_RECEIVER`
- `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`

Provider SDKs also require:

- `GROQ_API_KEY` (for `ChatGroq`)
- `OPENAI_API_KEY` (for `ChatOpenAI`)

---

## 9) Usage / Running the Project

### Run main pipeline

```bash
python main.py
```

### Alternative runner (debug)

```bash
python scripts/graph_execution.py
```

### Helpful validation scripts

```bash
python scripts/check_env.py
python scripts/check_email.py
python scripts/check_telegram.py
python scripts/test_embedding.py
```

---

## 10) Example Output / Behavior

During decision stage, the system prints per-item scoring:

```text
DECISION | <content_id> | rule=0.70 | vector=0.62 | llm=0.88 | final=0.77 | Notify
DECISION | <content_id> | rule=0.60 | vector=0.41 | llm=0.52 | final=0.51 | Archive
```

Then notifications are routed:

- `Notify` items -> Telegram alert (with a View link and Ignore button).
- `Archive` items -> Email summary alert.

If no actionable items exist:

```text
ℹ️ No items to notify
```

---

