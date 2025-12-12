from typing import Any, List, Union

from sayou.core.schemas import SayouNode, SayouOutput
from sayou.core.vocabulary import SayouAttribute, SayouClass, SayouPredicate

from ..interfaces.base_adapter import BaseAdapter


class DocumentChunkAdapter(BaseAdapter):
    """
    Standard Adapter for Sayou Chunking results.

    Converts `Chunk` objects (from sayou-chunking) into semantic `SayouNodes`.
    It maps metadata like 'semantic_type' to Ontology Classes (e.g., sayou:Topic)
    and preserves relationships like 'parent_id' as 'sayou:hasParent'.
    """

    component_name = "DocumentChunkAdapter"
    SUPPORTED_TYPES = ["document_chunk"]

    def _do_adapt(self, input_data: Union[List[Any], Any]) -> SayouOutput:
        """
        Convert chunks into a list of SayouNodes.

        Handles both Pydantic Chunk objects and dictionary representations.
        Generates deterministic URIs for nodes based on chunk IDs.

        Args:
            input_data (Union[List[Any], Any]): A single Chunk or list of Chunks.

        Returns:
            SayouOutput: The output containing the graph of nodes.
        """
        if not isinstance(input_data, list):
            input_data = [input_data]

        nodes = []

        for item in input_data:
            chunk_data = item.model_dump() if hasattr(item, "model_dump") else item

            if not isinstance(chunk_data, dict):
                self._log(f"Skipping invalid chunk data: {type(item)}", level="warning")
                continue

            content = chunk_data.get("content", "")
            meta = chunk_data.get("metadata", {})

            # 1. ID Mapping (Prefix 'sayou:doc:' added)
            raw_id = meta.get("chunk_id", "unknown")
            node_id = f"sayou:doc:{raw_id}"

            # 2. Node Class Decision (Semantic Type Mapping)
            sem_type = meta.get("semantic_type", "text")
            is_header = meta.get("is_header", False)

            if is_header:
                node_class = SayouClass.TOPIC
            elif sem_type == "table":
                node_class = SayouClass.TABLE
            elif sem_type == "code_block":
                node_class = SayouClass.CODE
            elif sem_type == "list_item":
                node_class = SayouClass.LIST_ITEM
            else:
                node_class = SayouClass.TEXT

            # 3. Attributes (Vocabulary 사용)
            attributes = {
                SayouAttribute.TEXT: content,
                SayouAttribute.SEMANTIC_TYPE: sem_type,
                SayouAttribute.PAGE_INDEX: meta.get("page_num"),
                SayouAttribute.PART_INDEX: meta.get("part_index"),
                SayouAttribute.SOURCE: meta.get("source"),
            }
            # 기타 메타데이터 보존
            for k, v in meta.items():
                if k not in ["chunk_id", "semantic_type", "parent_id", "is_header"]:
                    attributes[f"meta:{k}"] = v

            # 4. Relationships (Vocabulary 사용)
            relationships = {}
            parent_id = meta.get("parent_id")
            if parent_id:
                std_parent_id = f"sayou:doc:{parent_id}"
                relationships[SayouPredicate.HAS_PARENT] = [std_parent_id]

            # 5. Create Node
            node = SayouNode(
                node_id=node_id,
                node_class=node_class,
                friendly_name=f"DOC_NODE [{sem_type}] {raw_id}",
                attributes=attributes,
                relationships=relationships,
            )
            nodes.append(node)

        return SayouOutput(nodes=nodes, metadata={"source": "sayou-chunking"})
