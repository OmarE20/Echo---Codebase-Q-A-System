from datetime import timezone

from git import Repo

from schema import Chunk, SourceType


def ingest_commits(repo_path: str, repo_name: str) -> list[Chunk]:
    chunks = []

    repo = Repo(repo_path)

    try:
        commits = list(repo.iter_commits())
    except ValueError:
        commits = []

    for commit in commits:
        message = commit.message
        if isinstance(message, bytes):
            message = message.decode("utf-8", errors="replace")
        message = message.strip()

        if not message:
            continue

        subject = message.splitlines()[0]
        timestamp = commit.committed_datetime.astimezone(timezone.utc).isoformat()

        chunks.append(Chunk(
            content=message,
            summary=subject,
            source_type=SourceType.COMMIT,
            repo=repo_name,
            commit_sha=commit.hexsha,
            author=commit.author.name,
            timestamp=timestamp,
        ))

    print(f"Ingested {len(chunks)} commits from {repo_name}")

    return chunks
