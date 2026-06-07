import shutil
import tempfile
from collections import Counter

from git import Repo

from echo.ingestion.ingest import ingest_repo

REPO_URL = "https://github.com/pallets/flask"
REPO_NAME = "pallets/flask"


def main():
    temp_dir = tempfile.mkdtemp(prefix="echo-smoke-")

    try:
        print(f"Cloning {REPO_URL} into {temp_dir}...")
        Repo.clone_from(REPO_URL, temp_dir)

        chunks = ingest_repo(temp_dir, REPO_NAME)

        counts = Counter(chunk.source_type.value for chunk in chunks)
        breakdown = ", ".join(f"{source_type}={count}" for source_type, count in counts.items())
        print(f"\nTotal chunks: {len(chunks)}")
        print(f"Breakdown by source_type: {breakdown}")

        print("\nFirst 3 chunks:")
        for chunk in chunks[:3]:
            print("---")
            print(chunk.to_dict())
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


if __name__ == "__main__":
    main()
