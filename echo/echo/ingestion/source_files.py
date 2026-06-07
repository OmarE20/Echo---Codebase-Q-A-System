import os

from schema import Chunk, SourceType

SUPPORTED_EXTENSIONS = {
    ".py", ".js", ".ts", ".tsx", ".jsx", ".java", ".go", ".rs", ".cpp", ".c",
    ".h", ".cs", ".rb", ".php", ".swift", ".kt", ".scala", ".r", ".sql", ".sh",
    ".yaml", ".yml", ".toml", ".json", ".md",
}

IGNORED_DIRS = {
    ".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build",
    ".next", ".cache", "coverage", ".pytest_cache",
}


def ingest_source_files(repo_path: str, repo: str) -> list[Chunk]:
    chunks = []

    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]

        for filename in files:
            _, ext = os.path.splitext(filename)
            if ext not in SUPPORTED_EXTENSIONS:
                continue

            file_path = os.path.join(root, filename)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
            except (UnicodeDecodeError, OSError):
                continue

            if not content.strip():
                continue

            relative_path = os.path.relpath(file_path, repo_path).replace(os.sep, "/")
            line_count = content.count("\n") + 1

            chunks.append(Chunk(
                content=content,
                summary=f"Source file: {relative_path}",
                source_type=SourceType.SOURCE_FILE,
                repo=repo,
                file_path=relative_path,
                start_line=1,
                end_line=line_count,
            ))

    return chunks
