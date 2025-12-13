# Copyright (c) 2025 Microsoft Corporation.
# Licensed under the MIT License

"""
Elasticsearch Writer - Write operations for Elasticsearch.

Implements VectorDBWriterInterface from nlweb_dataload for uploading and
deleting documents in Elasticsearch indexes.
"""

import asyncio
import hashlib
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional

from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk

# Import the writer interface - but handle case where nlweb_dataload isn't installed
try:
    from nlweb_dataload.writer import VectorDBWriterInterface
    from nlweb_dataload.config import CONFIG
    _has_dataload = True
except ImportError:
    # Fallback: create minimal interface if nlweb_dataload not installed
    from abc import ABC, abstractmethod
    class VectorDBWriterInterface(ABC):
        @abstractmethod
        async def upload_documents(self, documents: List[Dict[str, Any]], **kwargs):
            pass
        @abstractmethod
        async def delete_documents(self, filter_criteria: Dict[str, Any], **kwargs):
            pass
    CONFIG = None
    _has_dataload = False


class ElasticsearchWriter(VectorDBWriterInterface):
    """Writer for Elasticsearch operations."""

    def __init__(self, endpoint_name: Optional[str] = None):
        """
        Initialize the Elasticsearch writer.

        Args:
            endpoint_name: Name of the endpoint to use (uses CONFIG.write_endpoint if not specified)
        """
        if not CONFIG:
            raise ValueError(
                "nlweb_dataload not configured. "
                "Call nlweb_dataload.init(config_path='config.yaml') first"
            )

        self.endpoint_name = endpoint_name or CONFIG.write_endpoint

        # Get endpoint configuration from dataload CONFIG
        self.endpoint_config = CONFIG.get_database_endpoint(self.endpoint_name)

        # Verify this is an Elasticsearch endpoint
        if self.endpoint_config.get('db_type') != "elasticsearch":
            raise ValueError(
                f"Endpoint {self.endpoint_name} is not an Elasticsearch endpoint "
                f"(type: {self.endpoint_config.get('db_type')})"
            )

        # Get API endpoint and key
        self.api_endpoint = self.endpoint_config.get('api_endpoint')
        if not self.api_endpoint:
            raise ValueError(f"api_endpoint not configured for {self.endpoint_name}")

        self.api_key = self.endpoint_config.get('api_key')
        if not self.api_key:
            raise ValueError(f"api_key not configured for {self.endpoint_name}")

        self.default_index_name = self.endpoint_config.get('index_name', 'embeddings')

    def _get_es_client(self) -> AsyncElasticsearch:
        """
        Get the Elasticsearch client.

        Returns:
            AsyncElasticsearch: The Elasticsearch client
        """
        return AsyncElasticsearch(
            hosts=self.api_endpoint,
            api_key=self.api_key
        )

    async def _ensure_index_exists(self, index_name: str, vector_dimensions: int = 1536):
        """
        Ensure the index exists, creating it if necessary.

        Args:
            index_name: Name of the index
            vector_dimensions: Dimension of the embedding vectors (default: 1536)
        """
        client = self._get_es_client()

        try:
            exists = await client.indices.exists(index=index_name)

            if not exists:
                # Create index with mappings
                mappings = {
                    "properties": {
                        "url": {"type": "keyword"},
                        "site": {"type": "keyword"},
                        "name": {"type": "text"},
                        "schema_json": {"type": "text"},
                        "timestamp": {"type": "date"},
                        "embedding": {
                            "type": "dense_vector",
                            "dims": vector_dimensions,
                            "index": True,
                            "similarity": "cosine"
                        }
                    }
                }

                await client.indices.create(index=index_name, mappings=mappings)

        finally:
            await client.close()

    def _generate_document_id(self, url: str, site: str) -> str:
        """
        Generate a unique document ID from URL and site.

        Args:
            url: Document URL
            site: Site identifier

        Returns:
            Unique document ID (hash)
        """
        # Use MD5 hash of URL + site for consistent IDs
        content = f"{url}:{site}"
        return hashlib.md5(content.encode()).hexdigest()

    async def upload_documents(
        self,
        documents: List[Dict[str, Any]],
        index_name: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Upload/index documents to Elasticsearch.

        Args:
            documents: List of document dicts with fields:
                - url (required)
                - name (required)
                - site (required)
                - schema_json (required): Document content/schema JSON
                - embedding (required): List of floats
                - timestamp (optional): ISO format timestamp
                - id (optional): If not provided, generated from URL + site
            index_name: Optional index name (defaults to configured index name)
            **kwargs: Additional parameters

        Returns:
            Dict with upload results
        """
        index_name = index_name or self.default_index_name

        # Ensure index exists (create if necessary)
        if documents:
            # Determine vector dimensions from first document's embedding
            vector_dimensions = len(documents[0]['embedding'])
            await self._ensure_index_exists(index_name, vector_dimensions)

        client = self._get_es_client()

        try:
            # Prepare documents for Elasticsearch
            actions = []
            for doc in documents:
                # Generate ID if not provided
                doc_id = doc.get('id') or self._generate_document_id(doc['url'], doc['site'])

                action = {
                    "_index": index_name,
                    "_id": doc_id,
                    "_source": {
                        "url": doc['url'],
                        "site": doc['site'],
                        "name": doc['name'],
                        "schema_json": doc['schema_json'],
                        "embedding": doc['embedding'],
                        "timestamp": doc.get('timestamp') or datetime.now(timezone.utc).isoformat()
                    }
                }
                actions.append(action)

            # Bulk index documents
            success, failed = await async_bulk(
                client,
                actions,
                raise_on_error=False,
                raise_on_exception=False
            )

            return {
                'success_count': success,
                'error_count': len(failed),
                'total': len(documents)
            }

        finally:
            await client.close()

    async def delete_documents(
        self,
        filter_criteria: Dict[str, Any],
        index_name: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Delete documents matching filter criteria.

        Args:
            filter_criteria: Filter dict (e.g., {"site": "example.com"})
            index_name: Optional index name
            **kwargs: Additional parameters

        Returns:
            Dict with deletion results
        """
        index_name = index_name or self.default_index_name
        client = self._get_es_client()

        try:
            # Build query from criteria
            must_clauses = []
            for key, value in filter_criteria.items():
                must_clauses.append({"term": {key: value}})

            query = {"bool": {"must": must_clauses}} if must_clauses else {"match_all": {}}

            # Delete by query
            response = await client.delete_by_query(
                index=index_name,
                query=query,
                conflicts='proceed'
            )

            deleted_count = response.get('deleted', 0)

            return {'deleted_count': deleted_count}

        finally:
            await client.close()

    async def delete_site(
        self,
        site: str,
        index_name: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Delete all documents for a specific site.

        Args:
            site: Site identifier
            index_name: Optional index name
            **kwargs: Additional parameters

        Returns:
            Dict with deletion results
        """
        return await self.delete_documents({'site': site}, index_name=index_name, **kwargs)
