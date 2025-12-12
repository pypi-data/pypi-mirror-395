import re
from typing import List

from sayou.core.schemas import SayouBlock, SayouChunk

from ..splitter.recursive_splitter import RecursiveSplitter
from ..utils.text_segmenter import TextSegmenter


class StructureSplitter(RecursiveSplitter):
    """
    Regex-based Structure Splitter.

    Uses a user-defined regex pattern (e.g., 'Article \d+') to identify
    structural boundaries in the document and splits along those lines first.
    """

    component_name = "StructureSplitter"
    SUPPORTED_TYPES = ["structure"]

    def _do_split(self, doc: SayouBlock) -> List[SayouChunk]:
        """
        Split by structure regex first, then fall back to recursive splitting
        for sections larger than `chunk_size`.
        """
        config = doc.metadata.get("config", {})
        chunk_size = config.get("chunk_size", 1000)

        structure_pattern = config.get("structure_pattern", r"\n\n")

        try:
            split_regex = f"(?m)(?={structure_pattern})"
            sections = re.split(split_regex, doc.content)
        except Exception:
            sections = doc.content.split("\n\n")

        final_chunks = []

        for section in sections:
            section = section.strip()
            if not section:
                continue

            if len(section) > chunk_size:
                sub_parts = TextSegmenter.split_with_protection(
                    section,
                    config.get("separators", self.DEFAULT_SEPARATORS),
                    config.get("protected_patterns", []),
                    chunk_size,
                    config.get("chunk_overlap", 50),
                )
                for part in sub_parts:
                    final_chunks.append(
                        SayouChunk(chunk_content=part, metadata=doc.metadata)
                    )
            else:
                final_chunks.append(
                    SayouChunk(chunk_content=section, metadata=doc.metadata)
                )

        return final_chunks
