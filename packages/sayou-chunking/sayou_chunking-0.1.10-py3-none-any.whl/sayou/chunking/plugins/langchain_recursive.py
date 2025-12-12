from typing import List

from sayou.core.schemas import SayouBlock, SayouChunk

from ..splitter.recursive_splitter import RecursiveSplitter

try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
except ImportError:
    RecursiveCharacterTextSplitter = None


class LangChainRecursiveSplitter(RecursiveSplitter):
    """
    Adapter for LangChain's RecursiveCharacterTextSplitter.
    Uses LangChain's logic instead of Sayou's internal TextSegmenter.
    """

    component_name = "LangChainRecursiveSplitter"
    SUPPORTED_TYPES = ["langchain_recursive"]

    def _do_split(self, doc: SayouBlock) -> List[SayouChunk]:
        """
        Delegate the splitting process to LangChain's splitter.
        """
        if RecursiveCharacterTextSplitter is None:
            raise ImportError("langchain-text-splitters is required for this plugin.")

        config = doc.metadata.get("config", {})
        chunk_size = config.get("chunk_size", 1000)
        chunk_overlap = config.get("chunk_overlap", 100)
        separators = config.get("separators", ["\n\n", "\n", " ", ""])

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap, separators=separators
        )

        texts = splitter.split_text(doc.content)

        return [SayouChunk(content=t, metadata=doc.metadata) for t in texts]
