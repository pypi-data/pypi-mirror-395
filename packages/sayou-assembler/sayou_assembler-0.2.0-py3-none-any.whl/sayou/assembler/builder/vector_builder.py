from typing import Any, Callable, Dict, List

from sayou.core.schemas import SayouOutput

from ..interfaces.base_builder import BaseBuilder


class VectorBuilder(BaseBuilder):
    """
    Builds Vector Payloads from SayouNodes.

    Extracts text content from nodes, computes embeddings using an injected function,
    and formats the data for Vector DBs (ID + Vector + Metadata).
    """

    component_name = "VectorBuilder"
    SUPPORTED_TYPES = ["vector"]

    def initialize(self, embedding_fn: Callable = None, **kwargs):
        """
        Inject the embedding function.

        Args:
            embedding_fn (Callable[[str], List[float]]): Function to generate vectors.
            **kwargs: Other arguments.
        """
        self.embedding_fn = embedding_fn

    def _do_build(self, data: SayouOutput) -> List[Dict[str, Any]]:
        """
        Generate a list of vector payloads.
        """
        payloads = []
        for node in data.nodes:
            text_content = node.attributes.get("schema:text", "")
            if not text_content:
                continue

            vector = []
            if self.embedding_fn:
                try:
                    vector = self.embedding_fn(text_content)
                except Exception as e:
                    self._log(f"Embedding error: {e}", level="warning")

            payload = {
                "id": node.node_id,
                "vector": vector,
                "text": text_content,
                "metadata": {
                    "node_class": node.node_class,
                    "friendly_name": node.friendly_name,
                    **node.attributes,
                },
            }
            payloads.append(payload)
        return payloads
