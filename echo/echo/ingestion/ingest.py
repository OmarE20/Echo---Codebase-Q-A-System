from collections import Counter
from typing import Optional

from schema import Chunk
from echo.ingestion.commits import ingest_commits
from echo.ingestion.github_prs import ingest_github_prs
from echo.ingestion.source_files import ingest_source_files


def ingest_repo(repo_path: str, repo_name: str, github_token: Optional[str] = None) -> list[Chunk]:
    chunks = []

    chunks.extend(ingest_source_files(repo_path, repo_name))
    chunks.extend(ingest_commits(repo_path, repo_name))
    chunks.extend(ingest_github_prs(repo_name, github_token))

    counts = Counter(chunk.source_type.value for chunk in chunks)
    breakdown = ", ".join(f"{source_type}={count}" for source_type, count in counts.items())
    print(f"Ingested {len(chunks)} total chunks from {repo_name} ({breakdown})")

    return chunks
