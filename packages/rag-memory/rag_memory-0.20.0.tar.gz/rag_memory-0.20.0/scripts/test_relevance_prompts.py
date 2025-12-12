#!/usr/bin/env python3
"""
Test different relevance scoring prompts without redeploying MCP server.

Usage:
    python scripts/test_relevance_prompts.py

This script:
1. Crawls a test URL to get real page data
2. Tests multiple prompt variations against the same pages
3. Compares results side-by-side
4. Helps iterate on prompt engineering without rebuild cycles
"""

import asyncio
import json
import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from openai import OpenAI
from src.ingestion.web_crawler import WebCrawler


# =============================================================================
# PROMPT VARIATIONS TO TEST
# =============================================================================

# Current (loose) prompt
PROMPT_V1_LOOSE = {
    "name": "V1: Current (Loose)",
    "system": """You are a relevance scoring assistant. Given a user's topic and a list of web pages,
score each page's relevance to the topic on a scale of 0.0 to 1.0.

Scoring guidelines:
- 0.9-1.0: Directly about the topic, essential content
- 0.7-0.89: Closely related, useful context or examples
- 0.5-0.69: Tangentially related, might be useful
- 0.3-0.49: Loosely related, probably not needed
- 0.0-0.29: Unrelated to the topic

Respond with a JSON array where each element has:
- "index": the page index
- "relevance_score": float 0.0-1.0
- "relevance_summary": 1 sentence explaining why (max 100 chars)
- "recommendation": "ingest" if score >= 0.5, else "skip"

Only output valid JSON, no markdown formatting."""
}

# Conservative prompt - err on side of caution
PROMPT_V2_CONSERVATIVE = {
    "name": "V2: Conservative (Evidence-Based)",
    "system": """You are a strict relevance scoring assistant for a knowledge base ingestion system.
Your job is to PREVENT low-quality content from polluting the user's knowledge base.

IMPORTANT: Err on the side of CAUTION. It's better to skip a potentially useful page than to
ingest irrelevant content. The user can always override your recommendations.

Scoring RULES (not guidelines):
- 0.9-1.0: Title explicitly contains topic keywords AND content has substantial topic coverage
- 0.7-0.89: Title or content clearly discusses the topic with specific details/examples
- 0.5-0.69: Topic is mentioned but page is primarily about something else
- 0.3-0.49: Topic mentioned in passing OR page is generic overview/index page
- 0.0-0.29: No clear evidence of topic relevance

EVIDENCE REQUIRED for scores >= 0.7:
- Topic keywords appear in the page title, OR
- Topic is discussed in detail (not just mentioned), OR
- Code examples or tutorials specifically about the topic

AUTOMATIC DOWNGRADES:
- Generic "overview" or "home" pages: cap at 0.7 unless topic is explicitly in title
- Index/navigation pages: cap at 0.5
- Installation/setup pages: cap at 0.5 unless topic is about installation
- Contributing/community pages: cap at 0.3

When uncertain, score LOWER and recommend "skip". The user can override.

Respond with a JSON array where each element has:
- "index": the page index
- "relevance_score": float 0.0-1.0
- "relevance_summary": 1 sentence citing specific evidence found (or lack thereof)
- "recommendation": "ingest" if score >= 0.6, else "skip"

Only output valid JSON, no markdown formatting."""
}

# Even stricter with explicit evidence citation
PROMPT_V3_STRICT_EVIDENCE = {
    "name": "V3: Strict Evidence Citation",
    "system": """You are a strict content relevance evaluator. Your goal is to PROTECT the user's
knowledge base from irrelevant content. When in doubt, exclude.

TASK: For each page, look for CONCRETE EVIDENCE that it covers the user's topic.

EVIDENCE TYPES (cite these in your summary):
- [TITLE_MATCH]: Topic keywords appear in page title
- [HEADING_MATCH]: Topic keywords in H1/H2 headings
- [CODE_EXAMPLE]: Code snippets demonstrating the topic
- [TUTORIAL]: Step-by-step instructions about the topic
- [DEEP_COVERAGE]: Multiple paragraphs discussing the topic in depth
- [MENTION_ONLY]: Topic mentioned but not the focus
- [NO_EVIDENCE]: No clear topic relevance found

SCORING MATRIX:
- 0.9-1.0: [TITLE_MATCH] + ([CODE_EXAMPLE] or [DEEP_COVERAGE])
- 0.7-0.89: [TITLE_MATCH] or ([HEADING_MATCH] + [DEEP_COVERAGE])
- 0.5-0.69: [HEADING_MATCH] or [TUTORIAL] without title match
- 0.3-0.49: [MENTION_ONLY] or generic related content
- 0.0-0.29: [NO_EVIDENCE]

HARD RULES:
- Homepage/landing pages: max 0.5 unless [TITLE_MATCH]
- Installation pages: max 0.4 unless topic IS installation
- Contributing/changelog: max 0.2
- If you're unsure, score LOW

Output JSON array with:
- "index": page index
- "relevance_score": float 0.0-1.0
- "evidence": list of evidence tags found (e.g., ["TITLE_MATCH", "CODE_EXAMPLE"])
- "relevance_summary": 1 sentence with evidence citation
- "recommendation": "ingest" if score >= 0.6, else "skip"

Only output valid JSON."""
}

# Balanced approach - conservative but not paranoid
PROMPT_V4_BALANCED = {
    "name": "V4: Balanced (Conservative + Reasonable)",
    "system": """You are a relevance evaluator helping users build focused knowledge bases.
Your goal is to recommend high-quality, relevant pages while filtering obvious noise.

PHILOSOPHY: Better to skip marginally relevant pages than pollute the knowledge base.
But DO NOT reject pages that clearly discuss the topic just because the title is generic.

EVIDENCE TO LOOK FOR:
- Topic keywords in title or headings
- Code examples related to the topic
- Detailed explanations or tutorials about the topic
- The topic being the PRIMARY focus (not just mentioned)

SCORING GUIDE:
- 0.9-1.0: Page is PRIMARILY about the topic (title match + substantial content)
- 0.7-0.89: Topic is a MAJOR focus (detailed coverage, examples, or tutorial)
- 0.5-0.69: Topic is DISCUSSED but page has broader scope
- 0.3-0.49: Topic only MENTIONED in passing
- 0.0-0.29: No meaningful topic coverage

AUTOMATIC SCORE CAPS (apply AFTER initial scoring):
- Generic homepages without topic in title: max 0.4
- Pure navigation/index pages: max 0.3
- Contributing/changelog/license pages: max 0.2
- Installation pages (unless topic IS installation): max 0.4

RECOMMENDATION THRESHOLD: 0.5
- Score >= 0.5: recommend "ingest"
- Score < 0.5: recommend "skip"

The user can always override your recommendations - you're advising, not deciding.

Output JSON array:
- "index": page index
- "relevance_score": float 0.0-1.0
- "relevance_summary": 1 sentence explaining evidence found (max 100 chars)
- "recommendation": "ingest" or "skip"

Only output valid JSON, no markdown."""
}

# Final version - evidence-based with clear boundary handling
PROMPT_V5_FINAL = {
    "name": "V5: Evidence-Based Final",
    "system": """You are a relevance evaluator helping users build focused knowledge bases.
Your goal: recommend pages that genuinely cover the user's topic, filter noise.

PHILOSOPHY: Err on the side of caution. Better to skip a marginally useful page than pollute
the knowledge base with irrelevant content. The user can always override your recommendations.

EVIDENCE TO LOOK FOR:
- Topic keywords in page title or H1/H2 headings
- Code examples demonstrating the topic
- Tutorials or detailed explanations about the topic
- The topic being a PRIMARY focus, not just mentioned

SCORING RULES:
- 0.85-1.0: Topic is the PRIMARY focus (title match AND substantial content)
- 0.65-0.84: Topic is a MAJOR focus (detailed coverage, code examples, or tutorial)
- 0.45-0.64: Topic is DISCUSSED meaningfully but page has broader scope
- 0.25-0.44: Topic only MENTIONED in passing or tangentially related
- 0.0-0.24: No meaningful topic coverage

AUTOMATIC SCORE CAPS (apply these AFTER scoring):
- Generic homepages/landing pages: max 0.35
- Navigation-only or index pages: max 0.30
- Contributing/changelog/license pages: max 0.20
- Installation/setup pages (unless topic IS installation): max 0.40

RECOMMENDATION RULES:
- Score >= 0.50: recommend "ingest" - page has meaningful topic coverage
- Score 0.40-0.49: recommend "review" - borderline, user should decide
- Score < 0.40: recommend "skip" - insufficient topic coverage

Output JSON array with:
- "index": page index
- "relevance_score": float 0.0-1.0
- "relevance_summary": 1 sentence explaining what evidence you found (max 100 chars)
- "recommendation": "ingest", "review", or "skip"

Only output valid JSON, no markdown."""
}

# V6: Semantic matching variant
PROMPT_V6_SEMANTIC = {
    "name": "V6: Semantic Matching",
    "system": """You are a relevance evaluator helping users build focused knowledge bases.
Your goal: recommend pages that genuinely cover the user's topic, filter noise.

PHILOSOPHY: Err on the side of caution. Better to skip a marginally useful page than pollute
the knowledge base with irrelevant content. The user can always override your recommendations.

EVIDENCE TO LOOK FOR:
- Topic keywords OR semantic equivalents in page title or headings
  (don't require literal matches - look for conceptual overlap)
- Code examples demonstrating the topic
- Tutorials or detailed explanations about the topic
- The topic being a PRIMARY focus, not just mentioned

SEMANTIC MATCHING - consider these equivalent:
- "installation" ↔ "setup", "getting started", "quickstart"
- "commands" ↔ "CLI reference", "terminal", "flags", "options"
- "permissions" ↔ "security", "access control", "allowlist"
- "settings" ↔ "configuration", "options", "preferences"
- "tools" ↔ "integrations", "plugins", "extensions", "MCP"

SCORING RULES:
- 0.85-1.0: Topic is the PRIMARY focus (title match AND substantial content)
- 0.65-0.84: Topic is a MAJOR focus (detailed coverage, code examples, or tutorial)
- 0.45-0.64: Topic is DISCUSSED meaningfully but page has broader scope
- 0.25-0.44: Topic only MENTIONED in passing or tangentially related
- 0.0-0.24: No meaningful topic coverage

AUTOMATIC SCORE CAPS (apply these AFTER scoring):
- Generic homepages/landing pages: max 0.35
- Navigation-only or index pages: max 0.30
- Contributing/changelog/license pages: max 0.20
- Legal/compliance/data policy pages: max 0.25

RECOMMENDATION RULES:
- Score >= 0.50: recommend "ingest" - page has meaningful topic coverage
- Score 0.40-0.49: recommend "review" - borderline, user should decide
- Score < 0.40: recommend "skip" - insufficient topic coverage

Output JSON array with:
- "index": page index
- "relevance_score": float 0.0-1.0
- "relevance_summary": 1 sentence explaining what evidence you found (max 100 chars)
- "recommendation": "ingest", "review", or "skip"

Only output valid JSON, no markdown."""
}

ALL_PROMPTS = [PROMPT_V5_FINAL, PROMPT_V6_SEMANTIC]


# =============================================================================
# TEST EXECUTION
# =============================================================================

async def crawl_test_pages(url: str, max_pages: int = 10) -> list:
    """Crawl pages and return them in scoring format."""
    print(f"\n📥 Crawling {url} (max {max_pages} pages)...")

    crawler = WebCrawler(headless=True, verbose=False)
    results = await crawler.crawl_with_depth(url, max_depth=1, max_pages=max_pages)

    pages = []
    for r in results:
        if r.success:
            pages.append({
                "url": r.url,
                "title": r.metadata.get("title", r.url),
                "content": r.content[:2000],  # Same truncation as production
            })

    print(f"✅ Crawled {len(pages)} pages successfully")
    return pages


def score_with_prompt(pages: list, topic: str, prompt_config: dict, model: str = "gpt-4o-mini") -> dict:
    """Score pages using a specific prompt configuration."""

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not set")

    client = OpenAI(api_key=api_key)

    # Build pages for scoring
    pages_for_scoring = []
    for i, page in enumerate(pages):
        pages_for_scoring.append({
            "index": i,
            "url": page["url"],
            "title": page["title"],
            "preview": page["content"][:2000],
        })

    user_prompt = f"""Topic: {topic}

Pages to evaluate:
{json.dumps(pages_for_scoring, indent=2)}

Score each page's relevance to the topic."""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": prompt_config["system"]},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.1,
        max_tokens=3000,
    )

    response_text = response.choices[0].message.content.strip()

    # Handle markdown code blocks
    if response_text.startswith("```"):
        lines = response_text.split("\n")
        response_text = "\n".join(lines[1:-1])

    try:
        scores = json.loads(response_text)
    except json.JSONDecodeError as e:
        print(f"❌ JSON parse error: {e}")
        print(f"Response was: {response_text[:500]}")
        return {"error": str(e), "raw": response_text}

    return {
        "prompt_name": prompt_config["name"],
        "scores": scores,
        "model": model,
    }


def print_comparison(results: list, pages: list):
    """Print side-by-side comparison of different prompt results."""

    print("\n" + "=" * 100)
    print("COMPARISON: Side-by-Side Results")
    print("=" * 100)

    # Build a map of scores by URL for each prompt
    prompt_scores = {}
    for result in results:
        if "error" in result:
            continue
        prompt_name = result["prompt_name"]
        prompt_scores[prompt_name] = {}
        for score in result["scores"]:
            idx = score["index"]
            if idx < len(pages):
                url = pages[idx]["url"]
                prompt_scores[prompt_name][url] = score

    # Print header
    prompt_names = list(prompt_scores.keys())
    print(f"\n{'URL':<60} | " + " | ".join(f"{p[:15]:<15}" for p in prompt_names))
    print("-" * (62 + len(prompt_names) * 18))

    # Print each page's scores across prompts
    for page in pages:
        url = page["url"]
        short_url = url[-57:] + "..." if len(url) > 60 else url

        scores_str = []
        for prompt_name in prompt_names:
            if url in prompt_scores.get(prompt_name, {}):
                score_data = prompt_scores[prompt_name][url]
                score = score_data.get("relevance_score", 0)
                rec = score_data.get("recommendation", "?")[0].upper()
                scores_str.append(f"{score:.1f} ({rec})")
            else:
                scores_str.append("N/A")

        print(f"{short_url:<60} | " + " | ".join(f"{s:<15}" for s in scores_str))

    # Print summary statistics
    print("\n" + "-" * 100)
    print("SUMMARY STATISTICS")
    print("-" * 100)

    for prompt_name in prompt_names:
        scores = [s.get("relevance_score", 0) for s in prompt_scores.get(prompt_name, {}).values()]
        if scores:
            avg = sum(scores) / len(scores)
            ingest_count = sum(1 for s in prompt_scores.get(prompt_name, {}).values()
                             if s.get("recommendation") == "ingest")
            skip_count = len(scores) - ingest_count
            print(f"{prompt_name}: avg={avg:.2f}, ingest={ingest_count}, skip={skip_count}")


def print_detailed_results(results: list, pages: list):
    """Print detailed results for each prompt."""

    for result in results:
        if "error" in result:
            print(f"\n❌ {result.get('prompt_name', 'Unknown')}: Error - {result['error']}")
            continue

        print(f"\n{'=' * 80}")
        print(f"📊 {result['prompt_name']}")
        print(f"{'=' * 80}")

        for score in sorted(result["scores"], key=lambda x: x.get("relevance_score", 0), reverse=True):
            idx = score.get("index", 0)
            if idx < len(pages):
                title = pages[idx]["title"][:50]
                url = pages[idx]["url"]
            else:
                title = "Unknown"
                url = "Unknown"

            rel_score = score.get("relevance_score", 0)
            summary = score.get("relevance_summary", "")[:60]
            rec = score.get("recommendation", "?")
            evidence = score.get("evidence", [])

            icon = "✅" if rec == "ingest" else "⏭️"
            print(f"\n{icon} [{rel_score:.1f}] {title}")
            print(f"   URL: {url}")
            print(f"   Summary: {summary}")
            if evidence:
                print(f"   Evidence: {evidence}")


async def main():
    """Main test runner."""

    print("=" * 80)
    print("RELEVANCE PROMPT A/B TESTING")
    print("=" * 80)

    # Test configuration
    test_cases = [
        {
            "url": "https://code.claude.com/docs/en/overview",
            "topic": "Claude Code usage: getting started, installation, setup, slash commands, security settings, tool permissions",
            "max_pages": 20,
        },
    ]

    for test in test_cases:
        print(f"\n{'#' * 80}")
        print(f"TEST: {test['topic']}")
        print(f"URL: {test['url']}")
        print(f"{'#' * 80}")

        # Crawl pages
        pages = await crawl_test_pages(test["url"], test["max_pages"])

        if not pages:
            print("❌ No pages crawled, skipping")
            continue

        # Test each prompt
        results = []
        for prompt_config in ALL_PROMPTS:
            print(f"\n🔄 Testing: {prompt_config['name']}...")
            try:
                result = score_with_prompt(pages, test["topic"], prompt_config)
                results.append(result)
                print(f"   ✅ Completed")
            except Exception as e:
                print(f"   ❌ Error: {e}")
                results.append({"prompt_name": prompt_config["name"], "error": str(e)})

        # Print comparison
        print_comparison(results, pages)
        print_detailed_results(results, pages)

    print("\n" + "=" * 80)
    print("TESTING COMPLETE")
    print("=" * 80)
    print("\nTo test your own prompt, edit ALL_PROMPTS in this script and re-run.")


if __name__ == "__main__":
    asyncio.run(main())
