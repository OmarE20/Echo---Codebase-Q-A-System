from typing import Optional

import requests

from schema import Chunk, SourceType

API_BASE = "https://api.github.com"
PER_PAGE = 100


def _fetch_all_issues(repo_name: str, github_token: Optional[str] = None) -> list[dict]:
    headers = {"Accept": "application/vnd.github+json"}
    if github_token:
        headers["Authorization"] = f"Bearer {github_token}"

    items = []
    url = f"{API_BASE}/repos/{repo_name}/issues"
    params = {"state": "all", "per_page": PER_PAGE, "page": 1}

    while url:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        items.extend(response.json())

        next_url = response.links.get("next", {}).get("url")
        url = next_url
        params = None

    return items


def ingest_github_prs(repo_name: str, github_token: Optional[str] = None) -> list[Chunk]:
    chunks = []

    items = _fetch_all_issues(repo_name, github_token)

    for item in items:
        body = item.get("body")
        if not body:
            continue

        title = item.get("title") or ""
        author = (item.get("user") or {}).get("login")
        is_pr = "pull_request" in item

        chunks.append(Chunk(
            content=f"{title}\n\n{body}",
            summary=title,
            source_type=SourceType.PULL_REQUEST if is_pr else SourceType.ISSUE,
            repo=repo_name,
            pr_number=item.get("number"),
            author=author,
            timestamp=item.get("created_at"),
        ))

    print(f"Ingested {len(chunks)} issues/pull requests from {repo_name}")

    return chunks
