from typing import Any, Dict, List
from ddgs import DDGS
from agents import function_tool  # your agent SDK decorator

_ddg = DDGS()

@function_tool
def ddg_search(
    query: str,
    max_results: int = 10,
    region: str = "us-en",
    safesearch: str = "moderate",
) -> List[Dict[str, Any]]:
    """Run a DuckDuckGo search and return a list of dicts with title, url, snippet."""
    hits = _ddg.text(
        query=query,
        max_results=max_results,
        region=region,
        safesearch=safesearch,
        verbose=True,
    )
    results: List[Dict[str, Any]] = []
    for h in hits:
        url = h.get("href") or h.get("url") or ""
        if not url.startswith("http"):
            continue
        results.append(
            {
                "title": h.get("title", "") or "",
                "url": url,
                "snippet": h.get("body") or h.get("snippet") or "",
            }
        )
    return results