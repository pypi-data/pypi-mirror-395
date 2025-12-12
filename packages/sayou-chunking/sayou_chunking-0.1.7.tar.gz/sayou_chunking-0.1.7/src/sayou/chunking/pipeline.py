from typing import Any, Dict, List, Optional

from sayou.core.base_component import BaseComponent
from sayou.core.decorators import safe_run
from sayou.core.schemas import SayouChunk

from .core.exceptions import SplitterError
from .interfaces.base_splitter import BaseSplitter
from .splitter.agentic_splitter import AgenticSplitter
from .splitter.fixed_length_splitter import FixedLengthSplitter
from .splitter.parent_document_splitter import ParentDocumentSplitter
from .splitter.recursive_splitter import RecursiveSplitter
from .splitter.semantic_splitter import SemanticSplitter
from .splitter.structure_splitter import StructureSplitter


class ChunkingPipeline(BaseComponent):
    """
    Orchestrates the text chunking process.

    This pipeline acts as a factory and dispatcher, routing the input data
    to the specific splitter strategy (e.g., recursive, markdown, semantic)
    requested by the user.
    """

    component_name = "ChunkingPipeline"

    def __init__(self, extra_splitters: Optional[List[BaseSplitter]] = None):
        """
        Initialize the pipeline with default and optional custom splitters.

        Args:
            extra_splitters (List[BaseSplitter], optional): Custom splitters to register.
        """
        super().__init__()
        self.splitters: Dict[str, BaseSplitter] = {}

        default_splitters = [
            AgenticSplitter(),
            RecursiveSplitter(),
            FixedLengthSplitter(),
            StructureSplitter(),
            SemanticSplitter(),
            ParentDocumentSplitter(),
        ]

        self._register(default_splitters)
        if extra_splitters:
            print("======")
            self._register(extra_splitters)

    def _register(self, splitters: List[BaseSplitter]):
        """
        Register a list of splitters into the internal strategy map.

        Args:
            splitters (List[BaseSplitter]): Splitter instances to register.
        """
        for s in splitters:
            for t in getattr(s, "SUPPORTED_TYPES", []):
                self.splitters[t] = s

    @safe_run(default_return=None)
    def initialize(self, **kwargs):
        """
        Initialize all registered splitters.

        Passes global configuration (e.g., default chunk_size) to all splitters.
        """
        for s in set(self.splitters.values()):
            s.initialize(**kwargs)
        self._log(
            f"ChunkingPipeline initialized. Strategies: {list(self.splitters.keys())}"
        )

    def run(self, input_data: Any, strategy: str = "default") -> List[SayouChunk]:
        """
        Execute the chunking strategy on the input data.

        Args:
            input_data (Any): Text string, Dict, or InputDocument object.
            strategy (str): The splitting strategy to use (default: 'default').

        Returns:
            List[SayouChunk]: A list of generated Chunk objects.

        Raises:
            SplitterError: If the strategy is unknown or execution fails.
        """
        splitter = self.splitters.get(strategy)
        if not splitter:
            raise SplitterError(
                f"Unknown strategy '{strategy}'. Available: {list(self.splitters.keys())}"
            )

        return splitter.split(input_data)
