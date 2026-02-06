# AGuard AI Agent – Complete Project Guide

> **Goal:** Build an autonomous AI agent that filters noisy information from Gmail and Reddit, surfaces only relevant content, and notifies the user with explanations.

---

## 1. Problem Statement

Modern users are overwhelmed by emails and social content. Important signals are buried under promotions, rants, and low-value posts. Skimming manually is time-consuming and unreliable.

**Objective:** Reduce noise first, then apply intelligence. Notify only when content crosses a confidence threshold.

---

## 2. High-Level Architecture

**Pipeline:**

* Scheduler → Fetch → Preprocess → Hard Filters → LLM Gate → Relevance Scoring → Decision → Notify → Log & Memory

**Sources (V1):**

* Gmail (official Gmail API, read-only)
* Reddit (official RSS feeds)

**Why RSS for Reddit (V1):**

* Official, read-only, no auth friction
* Stable and reliable
* Fetchers remain interchangeable for future API swap

---

## 3. Agent Responsibilities

### Scheduler

* Time-based trigger (e.g., every 30 minutes)
* Respects quiet hours

### Fetchers

* **Gmail Fetcher:** Uses Gmail API to list recent/unread messages
* **Reddit Fetcher:** Uses subreddit RSS feeds for new posts
* Fetchers are intentionally dumb (no intelligence)

### Preprocessor

* Clean text (strip signatures, HTML, emojis)
* Normalize fields into a common schema

### Hard Filters (Rule-Based)

* Fast, deterministic, ruthless
* Remove 60–80% noise before AI

### LLM Gate (Lightweight)

* Single question: informational vs noise
* No decisions, only classification

### Relevance Scoring

* Weighted combination of rules, LLM understanding, memory, and context

### Decision Engine

* Threshold-based outcomes: Notify / Batch / Ignore

### Logger & Memory

* Log every decision with reason
* Store content memory, interaction memory, preference memory, pattern memory

---

## 4. Normalized Content Schema

All sources convert to the same shape:

```
{
  id,
  source,
  title,
  body,
  timestamp,
  link,
  metadata
}
```

---

## 5. Hard Filter Rules

### Gmail Hard Filters

Apply in order:

1. Duplicate message ID → drop
2. Category noise (Promotions/Social/Forums) → drop
3. Sender blacklist (no-reply, marketing) → drop
4. Age > X days → drop
5. Empty or very short subject → drop
6. Attachment-only emails → drop (optional v1)

**Result:** ~100 → 15–25 emails

### Reddit Hard Filters (RSS)

1. Duplicate post ID → drop
2. Title length < 15 chars → drop
3. Rant/vent keywords → drop
4. Low-signal summaries → drop
5. Repetitive threads (daily/weekly/megathread) → drop

**Result:** ~50 → 8–12 posts

---

## 6. LLM Gate (Minimal)

* Input: cleaned title + body
* Output: {type: informational | noise, confidence}
* Reject if noise or confidence below threshold

---

## 7. Relevance Scoring Logic

Final relevance score (0–1) is computed as:

```
Rule Score
+ LLM Understanding Score
+ Memory Adjustment
+ Context Adjustment
```

**Guidelines:**

* Rules: 30–40%
* LLM: 30–40%
* Memory: 20–30%
* Context: small but important

**Thresholds:**

* ≥ 0.6 → Notify
* 0.4–0.6 → Batch
* < 0.4 → Ignore

---

## 8. Decision Explainability

Every decision must generate a human-readable reason, e.g.:

> “Notified because it matched your interest in internships and similar posts were clicked before.”

---

## 9. Memory Design

### Content Memory

* Prevent duplicates
* Enable similarity checks

### Interaction Memory

* Track clicks/ignores
* Behavior beats opinion

### Preference Memory

* Explicit user rules (topics, sources)

### Pattern Memory

* Derived stats (topic click rate, source ignore rate)

---

## 10. Project Structure

```
attention_guardian/
├── main.py
├── config/
│   └── user_preferences.yaml
├── agents/
│   ├── scheduler.py
│   ├── fetcher_gmail.py
│   ├── fetcher_reddit_rss.py
│   ├── preprocessor.py
│   ├── hard_filters.py
│   ├── llm_gate.py
│   ├── scoring.py
│   ├── decision.py
│   └── notifier.py
├── storage/
│   ├── db.py
│   └── vector_store.py
├── logs/
│   └── decisions.log
└── README.md
```

---

## 11. Gmail API Setup (Summary)

* Create Google Cloud project
* Enable Gmail API
* Configure OAuth consent (External, gmail.readonly)
* Create OAuth Client ID (Desktop)
* Use credentials.json for app identity
* token.json stores user permission

---

## 12. Reddit Ingestion (V1)

* Use official subreddit RSS feeds
* No authentication required
* Replaceable with API-based fetcher later

---

## 13. Logging & Evaluation

* Log every rejection and decision
* Store stage and reason
* Enables tuning, debugging, and trust

---

## 14. README Talking Points (Interview-Ready)

* Real user pain: attention overload
* System-first design, not chatbot
* Noise reduction before intelligence
* Explainable decisions
* Cloud-agnostic, deployable later

---

## 15. Roadmap

* V1: Local run, Gmail + Reddit RSS
* V2: Cloud deployment (serverless)
* V3: Additional sources (LinkedIn, GitHub)

---

**Principle to remember:**

> Great agents reduce workload before they increase intelligence.
