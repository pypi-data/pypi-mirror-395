from typing import List

from sayou.core.schemas import SayouBlock, SayouChunk

from ..interfaces.base_splitter import BaseSplitter


class AgenticSplitter(BaseSplitter):
    """
    LLM-based Splitter (Placeholder).

    Intended to use an LLM Agent to determine the most semantically
    meaningful breakpoints in the text.
    """

    component_name = "AgenticSplitter"
    SUPPORTED_TYPES = ["llm_agent"]

    def _do_split(self, doc: SayouBlock) -> List[SayouChunk]:
        """
        Delegate splitting logic to an LLM (Mock implementation).
        """
        # TODO: 실제 LLM Client 연동 필요
        self._log(
            "Agentic splitting is not fully implemented yet. Returning raw content."
        )

        return [SayouChunk(chunk_content=doc.content, metadata=doc.metadata)]
