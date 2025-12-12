import re
from typing import List


class TextSegmenter:
    """
    (Utility) A stateless engine for regex-based text segmentation.

    Provides core logic for recursive splitting while respecting 'protected'
    blocks (like tables or code snippets) that should not be fragmented.
    """

    @staticmethod
    def split_with_protection(
        text: str,
        separators: List[str],
        protected_patterns: List[str],
        chunk_size: int,
        chunk_overlap: int,
    ) -> List[str]:
        """
        Split text while preserving specific patterns intact.

        1. Identifies blocks matching `protected_patterns` (e.g., Tables).
        2. Isolates them so they are not split.
        3. Recursively splits the remaining text using `separators`.

        Args:
            text (str): The text to split.
            separators (List[str]): List of separators in order of precedence.
            protected_patterns (List[str]): Regex patterns to protect from splitting.
            chunk_size (int): Target size for each chunk.
            chunk_overlap (int): Number of overlapping characters.

        Returns:
            List[str]: A list of text segments.
        """
        if not text:
            return []

        final_chunks = []

        if not protected_patterns:
            return TextSegmenter.recursive_split(
                text, separators, chunk_size, chunk_overlap
            )

        combined_pattern = f"({'|'.join(protected_patterns)})"
        parts = re.split(combined_pattern, text, flags=re.MULTILINE | re.DOTALL)

        for part in parts:
            if not part:
                continue

            is_protected = False
            for pat in protected_patterns:
                if re.fullmatch(pat, part, flags=re.MULTILINE | re.DOTALL):
                    is_protected = True
                    break

            if is_protected:
                final_chunks.append(part)
            else:
                sub_chunks = TextSegmenter.recursive_split(
                    part, separators, chunk_size, chunk_overlap
                )
                final_chunks.extend(sub_chunks)

        return final_chunks

    @staticmethod
    def recursive_split(
        text: str, separators: List[str], chunk_size: int, chunk_overlap: int
    ) -> List[str]:
        """
        Recursively split text using a list of separators.

        Tries to split by the first separator. If chunks are still too large,
        it moves to the next separator in the list.

        Args:
            text (str): The text to split.
            separators (List[str]): Separators (e.g., ["\n\n", "\n", " "]).
            chunk_size (int): Maximum size of a chunk.
            chunk_overlap (int): Overlap size.

        Returns:
            List[str]: A list of text segments.
        """
        final_chunks = []

        if not separators:
            return [text]

        separator = separators[0]
        next_separators = separators[1:]

        if separator == "":
            return list(text)

        try:
            splits = re.split(f"({separator})", text)
        except:
            splits = [text]

        current_doc = []
        total_len = 0

        for split in splits:
            if not split:
                continue
            if split == separator:
                if current_doc:
                    current_doc[-1] += split
                continue

            if total_len + len(split) > chunk_size:
                if current_doc:
                    final_chunks.append("".join(current_doc))
                    current_doc = []
                    total_len = 0

                if len(split) > chunk_size:
                    final_chunks.extend(
                        TextSegmenter.recursive_split(
                            split, next_separators, chunk_size, chunk_overlap
                        )
                    )
                else:
                    current_doc.append(split)
                    total_len += len(split)
            else:
                current_doc.append(split)
                total_len += len(split)

        if current_doc:
            final_chunks.append("".join(current_doc))

        return final_chunks
