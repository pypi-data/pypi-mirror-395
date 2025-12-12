# URL Relevance Filtering Options for ingest_url

**Date**: 2024-12-02
**Status**: Brainstorming / Option 2 selected for implementation

## Problem Statement

When agents use `ingest_url` with `follow_links=True`, they often ingest pages that aren't relevant to the user's actual topic. Example: User wanted LangChain LCEL Pipelines docs, but the crawl picked up 50 linked pages mostly unrelated to LCEL.

The core issue: **link discovery is structural, not semantic**. A page about LCEL might link to 50 unrelated LangChain pages.

## Research Findings (2024-2025)

### What Others Are Doing

1. **Focused Crawlers with LLM Classification** (arxiv.org/html/2505.06972v1) - May 2025
   - Uses LLMs to classify pages as "relevant to topic" vs not, before crawling

2. **Craw4LLM** (arxiv.org/abs/2502.13347) - Feb 2025
   - Uses LLM pretraining influence as priority score for crawl scheduling

3. **Crawl4AI** (github.com/unclecode/crawl4ai) - Current library
   - Has `BM25` filtering and `cosine_similarity` for relevance
   - Applied *post-crawl* for chunking, not *pre-ingest*

4. **Watercrawl** (watercrawl.dev) - Commercial
   - Claims "semantic ranking" built-in

**Key insight**: Nobody has solved "dry run preview" exactly as described. Most solutions filter *during* or *after* crawl, not before.

---

## Brainstormed Options

### Option 1: Dry Run with Title/Meta Preview (Lightweight)

**How**: Crawl pages but only extract `<title>`, `<meta description>`, and first ~500 chars

**Returns**: List of `{url, title, description, preview}` for agent review

**Cost**: Low (no embeddings, no ingestion)

**Pros**:
- Fast
- Minimal context pollution

**Cons**:
- Titles can be misleading
- Agent must still decide

```python
async def preview_crawl(url, follow_links=True, max_pages=20):
    # Crawl pages, extract only title + first 500 chars
    return [{"url": ..., "title": ..., "preview": ...}]
```

---

### Option 2: Dry Run with LLM Relevance Scoring (Smarter) ✅ SELECTED

**How**: Crawl + extract content, then use cheap LLM (e.g., GPT-4o-mini) to score relevance to user's topic

**Returns**: `{url, title, relevance_score, brief_summary}` sorted by relevance

**Cost**: ~$0.01-0.05 per 20 pages (cheap model)

**Pros**:
- Actually semantic - understands topic relevance
- Agent gets actionable scores
- Clear UX for user decision

**Cons**:
- Adds latency (~10-30s for 20 pages)
- Requires topic as input

```python
async def preview_crawl_with_relevance(url, topic: str, follow_links=True, max_pages=20):
    # Returns URLs sorted by relevance to topic
    return [{"url": ..., "relevance": 0.92, "summary": "LCEL pipe composition"}]
```

**Implementation approach**: Add `dry_run: bool = False` and `topic: str = None` to existing `ingest_url` tool.

---

### Option 3: Topic-Constrained Crawling (Smart Crawl)

**How**: As you crawl, score each page against topic *before* following its links

**Returns**: Only pages above relevance threshold get ingested

**Cost**: Similar to Option 2

**Pros**:
- Automatic - no agent decision needed

**Cons**:
- More complex
- Harder to debug why pages were excluded

---

### Option 4: Embedding-Based URL Filtering (Fast Semantic)

**How**: Generate embedding for topic, then for each page's title+preview, compute cosine similarity

**Returns**: URLs above threshold

**Cost**: Very cheap (~$0.002 for 20 pages via existing embedder)

**Pros**:
- Fast
- Uses existing embedding infrastructure

**Cons**:
- Titles alone might not capture relevance well

---

## Decision

**Selected Option 2** for implementation because:
- Clear UX: agent gets explicit scores to present to user
- Semantic: actually understands topic relevance
- Cheap: GPT-4o-mini at ~$0.15/1M tokens means 20 pages costs cents
- Debuggable: user sees why pages were scored low/high

## Future Considerations

- Option 3 could be added later as an "auto" mode
- Option 4 could be a fast fallback if LLM is unavailable
- Consider caching relevance scores by URL+topic hash
