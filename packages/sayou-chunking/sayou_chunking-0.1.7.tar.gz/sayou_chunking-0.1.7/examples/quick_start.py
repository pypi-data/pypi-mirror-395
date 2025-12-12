import json
import logging

from sayou.chunking.pipeline import ChunkingPipeline
from sayou.chunking.plugins.audited_fixed_length_splitter import (
    AuditedFixedLengthSplitter,
)
from sayou.chunking.plugins.markdown_splitter import MarkdownSplitter

logging.basicConfig(level=logging.INFO, format="%(message)s")


def run_demo():
    print(">>> Initializing Sayou Chunking Pipeline...")

    markdown_plugin = MarkdownSplitter()
    audited_plugin = AuditedFixedLengthSplitter()
    pipeline = ChunkingPipeline(extra_splitters=[markdown_plugin, audited_plugin])
    pipeline.initialize()

    md_content = """
# Sayou Chunking Demo

This is an example markdown file.

## Section 1: Introduction
Chunking is crucial for RAG. It splits large texts into smaller pieces.

## Section 2: Features
- Recursive Splitting
- Markdown Awareness
- **Semantic Analysis**

| Feature | Support |
| :--- | :--- |
| Text | Yes |
| Table | Yes |
    """.strip()

    # --- Scenario 1: Markdown Strategy ---
    print("\n=== [1] Markdown Chunking ===")
    request_md = {
        "content": md_content,
        "metadata": {"source": "dummy.md"},
        "config": {"chunk_size": 100},
    }

    chunks = pipeline.run(request_md, strategy="markdown")

    for i, chunk in enumerate(chunks):
        print(
            f"[{i}] Type: {chunk.metadata.get('semantic_type')} | Len: {len(chunk.chunk_content)}"
        )
        print(f"    Content: {chunk.chunk_content[:50]}...")

    print("\n=== [2] Audited Fixed Chunking ===")
    request_fixed = {
        "content": "A" * 150,
        "metadata": {"source": "generated"},
        "config": {"chunk_size": 50, "chunk_overlap": 0},
    }

    chunks_audit = pipeline.run(request_fixed, strategy="audited_fixed")

    for i, chunk in enumerate(chunks_audit):
        audit_info = chunk.metadata.get("audit", {})
        print(f"[{i}] Content: {chunk.chunk_content}")
        print(f"    Audit Info: {audit_info}")

    output_data = [c.model_dump() for c in chunks]
    with open("chunks_output.json", "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    print("\n✅ Saved results to chunks_output.json")


if __name__ == "__main__":
    run_demo()
