# Copyright (c) 2025 Microsoft Corporation.
# Licensed under the MIT License

"""
Qdrant Writer - Write operations for Qdrant.

Implements VectorDBWriterInterface from nlweb_dataload for uploading and
deleting documents in Qdrant collections.
"""

import asyncio
import hashlib
import uuid
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional

from qdrant_client import AsyncQdrantClient
from qdrant_client.http import models

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


class QdrantWriter(VectorDBWriterInterface):
    """Writer for Qdrant operations."""

    def __init__(self, endpoint_name: Optional[str] = None):
        """
        Initialize the Qdrant writer.

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

        # Verify this is a Qdrant endpoint
        if self.endpoint_config.get('db_type') != "qdrant":
            raise ValueError(
                f"Endpoint {self.endpoint_name} is not a Qdrant endpoint "
                f"(type: {self.endpoint_config.get('db_type')})"
            )

        # Get connection parameters
        self.api_endpoint = self.endpoint_config.get('api_endpoint')
        self.api_key = self.endpoint_config.get('api_key')
        self.database_path = self.endpoint_config.get('database_path')
        self.default_collection_name = self.endpoint_config.get('index_name', 'nlweb_collection')

    def _get_qdrant_client(self) -> AsyncQdrantClient:
        """
        Get the Qdrant client.

        Returns:
            AsyncQdrantClient: The Qdrant client
        """
        params = {}

        # Check for URL-based connection
        if self.api_endpoint and self.api_endpoint.startswith(("http://", "https://")):
            params["url"] = self.api_endpoint
            if self.api_key:
                params["api_key"] = self.api_key
        elif self.database_path:
            params["path"] = self.database_path
        else:
            # Default to a local path
            params["path"] = "./data/qdrant"

        return AsyncQdrantClient(**params)

    async def _ensure_collection_exists(
        self,
        collection_name: str,
        vector_dimensions: int = 1536
    ):
        """
        Ensure the collection exists, creating it if necessary.

        Args:
            collection_name: Name of the collection
            vector_dimensions: Dimension of the embedding vectors (default: 1536)
        """
        client = self._get_qdrant_client()

        try:
            exists = await client.collection_exists(collection_name)

            if not exists:
                # Create collection
                await client.create_collection(
                    collection_name=collection_name,
                    vectors_config=models.VectorParams(
                        size=vector_dimensions,
                        distance=models.Distance.COSINE
                    ),
                )

        finally:
            await client.close()

    def _generate_document_id(self, url: str, site: str) -> str:
        """
        Generate a unique document ID from URL and site.

        Args:
            url: Document URL
            site: Site identifier

        Returns:
            Unique document ID (UUID string)
        """
        # Use UUID5 with URL namespace for consistent IDs
        content = f"{url}:{site}"
        return str(uuid.uuid5(uuid.NAMESPACE_URL, content))

    async def upload_documents(
        self,
        documents: List[Dict[str, Any]],
        collection_name: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Upload/upsert documents to Qdrant.

        Args:
            documents: List of document dicts with fields:
                - url (required)
                - name (required)
                - site (required)
                - schema_json (required): Document content/schema JSON
                - embedding (required): List of floats
                - timestamp (optional): ISO format timestamp
                - id (optional): If not provided, generated from URL + site
            collection_name: Optional collection name (defaults to configured name)
            **kwargs: Additional parameters

        Returns:
            Dict with upload results
        """
        collection_name = collection_name or self.default_collection_name

        client = self._get_qdrant_client()

        try:
            # Prepare documents for Qdrant
            points = []
            vector_dimensions = None
            
            for doc in documents:
                # Skip documents without embeddings
                if "embedding" not in doc or not doc["embedding"]:
                    continue
                
                # Determine vector dimensions from first valid document
                if vector_dimensions is None:
                    vector_dimensions = len(doc['embedding'])
                    # Ensure collection exists with the correct dimensions
                    await self._ensure_collection_exists(collection_name, vector_dimensions)

                # Generate ID if not provided
                doc_id = doc.get('id') or self._generate_document_id(doc['url'], doc['site'])

                points.append(models.PointStruct(
                    id=doc_id,
                    vector=doc['embedding'],
                    payload={
                        "url": doc['url'],
                        "name": doc['name'],
                        "site": doc['site'],
                        "schema_json": doc['schema_json'],
                        "timestamp": doc.get('timestamp') or datetime.now(timezone.utc).isoformat()
                    }
                ))

            if points:
                # Upload in batches
                batch_size = 100  # Smaller batch size for stability
                total_uploaded = 0

                for i in range(0, len(points), batch_size):
                    batch = points[i:i+batch_size]
                    try:
                        await client.upsert(collection_name=collection_name, points=batch)
                        total_uploaded += len(batch)
                    except Exception as e:
                        # Log error but continue with next batch
                        pass

                return {
                    'success_count': total_uploaded,
                    'error_count': len(points) - total_uploaded,
                    'total': len(documents)
                }
            else:
                return {
                    'success_count': 0,
                    'error_count': 0,
                    'total': 0
                }

        finally:
            await client.close()

    async def delete_documents(
        self,
        filter_criteria: Dict[str, Any],
        collection_name: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Delete documents matching filter criteria.

        Args:
            filter_criteria: Filter dict (e.g., {"site": "example.com"})
            collection_name: Optional collection name
            **kwargs: Additional parameters

        Returns:
            Dict with deletion results
        """
        collection_name = collection_name or self.default_collection_name
        client = self._get_qdrant_client()

        try:
            # Build filter from criteria
            must_conditions = []
            for key, value in filter_criteria.items():
                must_conditions.append(
                    models.FieldCondition(
                        key=key,
                        match=models.MatchValue(value=value)
                    )
                )

            filter_condition = models.Filter(must=must_conditions) if must_conditions else None

            # Delete points matching filter
            if filter_condition:
                result = await client.delete(
                    collection_name=collection_name,
                    points_selector=models.FilterSelector(filter=filter_condition)
                )

                # The result status indicates success
                deleted_count = 1 if result else 0  # Qdrant doesn't return count directly
            else:
                deleted_count = 0

            return {'deleted_count': deleted_count}

        finally:
            await client.close()

    async def delete_site(
        self,
        site: str,
        collection_name: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Delete all documents for a specific site.

        Args:
            site: Site identifier
            collection_name: Optional collection name
            **kwargs: Additional parameters

        Returns:
            Dict with deletion results
        """
        return await self.delete_documents({'site': site}, collection_name=collection_name, **kwargs)
