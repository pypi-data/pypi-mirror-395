import time
from typing import List

from sayou.core.schemas import SayouBlock, SayouChunk

from ..splitter.fixed_length_splitter import FixedLengthSplitter


class AuditedFixedLengthSplitter(FixedLengthSplitter):
    """
    Fixed Splitter with auditing.

    Inherits standard fixed splitting but adds an audit trail (timestamp,
    original length) to the metadata of each chunk.
    """

    component_name = "AuditedFixedLengthSplitter"
    SUPPORTED_TYPES = ["audited_fixed"]

    def _do_split(self, doc: SayouBlock) -> List[SayouChunk]:
        """
        Perform fixed splitting and inject audit info into metadata.
        """
        chunks = super()._do_split(doc)

        audit_info = {
            "processed_at": time.time(),
            "original_length": len(doc.content),
            "splitter_version": "1.0.0",
        }

        for chunk in chunks:
            chunk.update_metadata(audit=audit_info)

        return chunks
