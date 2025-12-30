import os
from typing import Dict, Any, List

from pymilvus import MilvusClient

from src.domain.ports.vector_db_port import VectorDBPort


class MilvusVectorDBService(VectorDBPort):
    def __init__(self) -> None:
        self.client = self._init_client()

    @staticmethod
    def _init_client() -> MilvusClient:
        host = os.getenv("MILVUS_HOST")
        token = os.getenv("MILVUS_TOKEN")
        user = os.getenv("MILVUS_USER")
        password = os.getenv("MILVUS_PASSWORD")

        if not host:
            raise ValueError("MILVUS_HOST is not set")

        if token:
            return MilvusClient(uri=host, token=token)

        if user and password:
            return MilvusClient(uri=host, user=user, password=password)

        raise ValueError("Either MILVUS_TOKEN or both MILVUS_USER and MILVUS_PASSWORD must be set")

    def get(self, collection_name: str, query: str, output_fields: List[str], top_k: int = 10) -> List[Dict[str, Any]]:
        """
        Metadata / filtered query (NO embeddings)
        """
        # Direct synchronous call to Milvus
        return self.client.query(collection_name=collection_name, filter=query, output_fields=output_fields,
                                 limit=top_k)

    def search_similar(self, collection_name: str, embeddings: List[float], output_fields: List[str], top_k: int = 10,
                       embedding_field: str = "embedding") -> List[Dict[str, Any]]:
        """
        Vector similarity search
        """
        # Direct synchronous call to Milvus
        res = self.client.search(collection_name=collection_name, data=[embeddings], anns_field=embedding_field,
                                 limit=top_k, output_fields=output_fields,
                                 search_params={"metric_type": "IP", "params": {"ef": 64}})

        # MilvusClient returns List[List[Dict]] (one list per query vector)
        flattened_results = []
        for hits in res:
            for hit in hits:
                item = {field: hit.get(field) for field in output_fields}
                flattened_results.append(item)

        return flattened_results
