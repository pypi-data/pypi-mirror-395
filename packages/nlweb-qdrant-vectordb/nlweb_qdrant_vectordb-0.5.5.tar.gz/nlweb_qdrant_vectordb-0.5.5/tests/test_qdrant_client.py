# Copyright (c) 2025 Microsoft Corporation.
# Licensed under the MIT License

"""
Tests for Qdrant Client
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from typing import List

from nlweb_qdrant_vectordb.qdrant_client import QdrantClient


@pytest.fixture
def mock_config():
    """Mock CONFIG object"""
    config = MagicMock()
    config.write_endpoint = "test_endpoint"
    
    # Mock endpoint config
    endpoint_config = MagicMock()
    endpoint_config.db_type = "qdrant"
    endpoint_config.api_endpoint = "https://test.qdrant.tech"
    endpoint_config.api_key = "test_api_key"
    endpoint_config.database_path = None
    endpoint_config.index_name = "test_collection"
    
    config.retrieval_endpoints = {"test_endpoint": endpoint_config}
    
    return config


@pytest.fixture
def mock_qdrant_client():
    """Mock Qdrant client"""
    client = AsyncMock()
    
    # Mock collections response
    collections_response = MagicMock()
    collections_response.collections = []
    client.get_collections = AsyncMock(return_value=collections_response)
    
    client.collection_exists = AsyncMock(return_value=False)
    client.create_collection = AsyncMock()
    client.search = AsyncMock(return_value=[])
    client.scroll = AsyncMock(return_value=([], None))
    client.close = AsyncMock()
    
    return client


@pytest.fixture
def qdrant_client(mock_config):
    """Create QdrantClient with mocked config"""
    with patch('nlweb_qdrant_vectordb.qdrant_client.CONFIG', mock_config):
        client = QdrantClient(endpoint_name="test_endpoint")
        return client


class TestQdrantClientInit:
    """Tests for QdrantClient initialization"""

    def test_init_with_valid_config(self, mock_config):
        """Test initialization with valid configuration"""
        with patch('nlweb_qdrant_vectordb.qdrant_client.CONFIG', mock_config):
            client = QdrantClient(endpoint_name="test_endpoint")
            
            assert client.endpoint_name == "test_endpoint"
            assert client.api_endpoint == "https://test.qdrant.tech"
            assert client.api_key == "test_api_key"
            assert client.default_collection_name == "test_collection"

    def test_init_without_endpoint_name(self, mock_config):
        """Test initialization without endpoint name uses default"""
        with patch('nlweb_qdrant_vectordb.qdrant_client.CONFIG', mock_config):
            client = QdrantClient()
            
            assert client.endpoint_name == "test_endpoint"

    def test_init_with_local_path(self, mock_config):
        """Test initialization with local database path"""
        mock_config.retrieval_endpoints["test_endpoint"].api_endpoint = None
        mock_config.retrieval_endpoints["test_endpoint"].database_path = "./data/qdrant"
        
        with patch('nlweb_qdrant_vectordb.qdrant_client.CONFIG', mock_config):
            client = QdrantClient(endpoint_name="test_endpoint")
            
            assert client.database_path == "./data/qdrant"
            assert client.api_endpoint is None

    def test_init_wrong_db_type(self, mock_config):
        """Test initialization fails with wrong database type"""
        mock_config.retrieval_endpoints["test_endpoint"].db_type = "elasticsearch"
        
        with patch('nlweb_qdrant_vectordb.qdrant_client.CONFIG', mock_config):
            with pytest.raises(ValueError, match="not a Qdrant endpoint"):
                QdrantClient(endpoint_name="test_endpoint")

    def test_init_missing_endpoint_config(self, mock_config):
        """Test initialization fails with missing endpoint configuration"""
        mock_config.retrieval_endpoints = {}
        
        with patch('nlweb_qdrant_vectordb.qdrant_client.CONFIG', mock_config):
            with pytest.raises(ValueError, match="No configuration found"):
                QdrantClient(endpoint_name="test_endpoint")


class TestQdrantClientMethods:
    """Tests for QdrantClient methods"""

    @pytest.mark.asyncio
    async def test_get_qdrant_client(self, qdrant_client, mock_qdrant_client):
        """Test getting Qdrant client"""
        with patch('nlweb_qdrant_vectordb.qdrant_client.AsyncQdrantClient', return_value=mock_qdrant_client):
            client = await qdrant_client._get_qdrant_client()
            
            assert client == mock_qdrant_client
            mock_qdrant_client.get_collections.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_qdrant_client_caching(self, qdrant_client, mock_qdrant_client):
        """Test that Qdrant client is cached"""
        with patch('nlweb_qdrant_vectordb.qdrant_client.AsyncQdrantClient', return_value=mock_qdrant_client):
            client1 = await qdrant_client._get_qdrant_client()
            client2 = await qdrant_client._get_qdrant_client()
            
            assert client1 == client2
            # get_collections() should only be called once due to caching
            assert mock_qdrant_client.get_collections.call_count == 1

    @pytest.mark.asyncio
    async def test_collection_exists_true(self, qdrant_client, mock_qdrant_client):
        """Test checking if collection exists (returns true)"""
        mock_qdrant_client.collection_exists = AsyncMock(return_value=True)
        
        with patch('nlweb_qdrant_vectordb.qdrant_client.AsyncQdrantClient', return_value=mock_qdrant_client):
            await qdrant_client._get_qdrant_client()  # Initialize cache
            exists = await qdrant_client.collection_exists("test_collection")
            
            assert exists is True

    @pytest.mark.asyncio
    async def test_collection_exists_false(self, qdrant_client, mock_qdrant_client):
        """Test checking if collection exists (returns false)"""
        mock_qdrant_client.collection_exists = AsyncMock(return_value=False)
        
        with patch('nlweb_qdrant_vectordb.qdrant_client.AsyncQdrantClient', return_value=mock_qdrant_client):
            await qdrant_client._get_qdrant_client()  # Initialize cache
            exists = await qdrant_client.collection_exists("nonexistent")
            
            assert exists is False

    @pytest.mark.asyncio
    async def test_collection_exists_error(self, qdrant_client, mock_qdrant_client):
        """Test collection_exists returns False on error"""
        mock_qdrant_client.collection_exists = AsyncMock(side_effect=Exception("Connection error"))
        
        with patch('nlweb_qdrant_vectordb.qdrant_client.AsyncQdrantClient', return_value=mock_qdrant_client):
            await qdrant_client._get_qdrant_client()  # Initialize cache
            exists = await qdrant_client.collection_exists("test_collection")
            
            assert exists is False

    @pytest.mark.asyncio
    async def test_create_collection_success(self, qdrant_client, mock_qdrant_client):
        """Test creating a collection successfully"""
        mock_qdrant_client.collection_exists = AsyncMock(return_value=False)
        
        with patch('nlweb_qdrant_vectordb.qdrant_client.AsyncQdrantClient', return_value=mock_qdrant_client):
            await qdrant_client._get_qdrant_client()  # Initialize cache
            result = await qdrant_client.create_collection("new_collection", 1536)
            
            assert result is True
            mock_qdrant_client.create_collection.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_collection_already_exists(self, qdrant_client, mock_qdrant_client):
        """Test creating a collection that already exists"""
        mock_qdrant_client.collection_exists = AsyncMock(return_value=True)
        
        with patch('nlweb_qdrant_vectordb.qdrant_client.AsyncQdrantClient', return_value=mock_qdrant_client):
            await qdrant_client._get_qdrant_client()  # Initialize cache
            result = await qdrant_client.create_collection("existing_collection", 1536)
            
            assert result is False
            mock_qdrant_client.create_collection.assert_not_called()

    @pytest.mark.asyncio
    async def test_ensure_collection_exists_creates(self, qdrant_client, mock_qdrant_client):
        """Test ensure_collection_exists creates collection"""
        mock_qdrant_client.collection_exists = AsyncMock(return_value=False)
        
        with patch('nlweb_qdrant_vectordb.qdrant_client.AsyncQdrantClient', return_value=mock_qdrant_client):
            await qdrant_client._get_qdrant_client()  # Initialize cache
            result = await qdrant_client.ensure_collection_exists("test_collection", 1536)
            
            assert result is True
            mock_qdrant_client.create_collection.assert_called_once()

    @pytest.mark.asyncio
    async def test_ensure_collection_exists_already_exists(self, qdrant_client, mock_qdrant_client):
        """Test ensure_collection_exists when collection exists"""
        mock_qdrant_client.collection_exists = AsyncMock(return_value=True)
        
        with patch('nlweb_qdrant_vectordb.qdrant_client.AsyncQdrantClient', return_value=mock_qdrant_client):
            await qdrant_client._get_qdrant_client()  # Initialize cache
            result = await qdrant_client.ensure_collection_exists("test_collection", 1536)
            
            assert result is False
            mock_qdrant_client.create_collection.assert_not_called()

    def test_create_site_filter_single_site(self, qdrant_client):
        """Test creating site filter for single site"""
        site_filter = qdrant_client._create_site_filter("example.com")
        
        assert site_filter is not None

    def test_create_site_filter_multiple_sites(self, qdrant_client):
        """Test creating site filter for multiple sites"""
        site_filter = qdrant_client._create_site_filter(["site1.com", "site2.com"])
        
        assert site_filter is not None

    def test_create_site_filter_all(self, qdrant_client):
        """Test creating site filter for 'all'"""
        site_filter = qdrant_client._create_site_filter("all")
        
        assert site_filter is None

    def test_create_site_filter_list_with_all(self, qdrant_client):
        """Test creating site filter with 'all' in list"""
        site_filter = qdrant_client._create_site_filter(["site1.com", "all"])
        
        # Should filter out "all"
        assert site_filter is not None

    def test_format_results(self, qdrant_client):
        """Test formatting search results"""
        mock_point = MagicMock()
        mock_point.payload = {
            "url": "https://example.com/page1",
            "schema_json": '{"title": "Page 1"}',
            "name": "page1",
            "site": "example.com"
        }
        
        results = qdrant_client._format_results([mock_point])
        
        assert len(results) == 1
        assert results[0] == [
            "https://example.com/page1",
            '{"title": "Page 1"}',
            "page1",
            "example.com"
        ]

    @pytest.mark.asyncio
    async def test_search(self, qdrant_client, mock_qdrant_client):
        """Test search functionality"""
        mock_embedding = [0.1] * 1536
        
        mock_point = MagicMock()
        mock_point.payload = {
            "url": "https://example.com/page1",
            "schema_json": '{"title": "Page 1"}',
            "name": "page1",
            "site": "example.com"
        }
        
        mock_qdrant_client.collection_exists = AsyncMock(return_value=True)
        mock_qdrant_client.search = AsyncMock(return_value=[mock_point])
        
        with patch('nlweb_qdrant_vectordb.qdrant_client.AsyncQdrantClient', return_value=mock_qdrant_client):
            with patch('nlweb_qdrant_vectordb.qdrant_client.get_embedding', return_value=mock_embedding):
                await qdrant_client._get_qdrant_client()  # Initialize cache
                results = await qdrant_client.search(
                    query="test query",
                    site="example.com",
                    num_results=10
                )
                
                assert len(results) == 1
                assert results[0][0] == "https://example.com/page1"
                mock_qdrant_client.search.assert_called_once()

    @pytest.mark.asyncio
    async def test_search_creates_collection(self, qdrant_client, mock_qdrant_client):
        """Test search creates collection if it doesn't exist"""
        mock_embedding = [0.1] * 1536
        
        mock_qdrant_client.collection_exists = AsyncMock(return_value=False)
        
        with patch('nlweb_qdrant_vectordb.qdrant_client.AsyncQdrantClient', return_value=mock_qdrant_client):
            with patch('nlweb_qdrant_vectordb.qdrant_client.get_embedding', return_value=mock_embedding):
                await qdrant_client._get_qdrant_client()  # Initialize cache
                results = await qdrant_client.search(
                    query="test query",
                    site="example.com",
                    num_results=10
                )
                
                # Should return empty results when collection is created
                assert results == []
                mock_qdrant_client.create_collection.assert_called_once()

    @pytest.mark.asyncio
    async def test_search_all_sites(self, qdrant_client, mock_qdrant_client):
        """Test search across all sites"""
        mock_embedding = [0.1] * 1536
        
        mock_qdrant_client.collection_exists = AsyncMock(return_value=True)
        mock_qdrant_client.search = AsyncMock(return_value=[])
        
        with patch('nlweb_qdrant_vectordb.qdrant_client.AsyncQdrantClient', return_value=mock_qdrant_client):
            with patch('nlweb_qdrant_vectordb.qdrant_client.get_embedding', return_value=mock_embedding):
                await qdrant_client._get_qdrant_client()  # Initialize cache
                results = await qdrant_client.search_all_sites(
                    query="test query",
                    num_results=10
                )
                
                assert results == []
                mock_qdrant_client.search.assert_called_once()

    @pytest.mark.asyncio
    async def test_search_by_url_found(self, qdrant_client, mock_qdrant_client):
        """Test searching by URL when found"""
        mock_point = MagicMock()
        mock_point.payload = {
            "url": "https://example.com/page1",
            "schema_json": '{"title": "Page 1"}',
            "name": "page1",
            "site": "example.com"
        }
        
        mock_qdrant_client.scroll = AsyncMock(return_value=([mock_point], None))
        
        with patch('nlweb_qdrant_vectordb.qdrant_client.AsyncQdrantClient', return_value=mock_qdrant_client):
            await qdrant_client._get_qdrant_client()  # Initialize cache
            result = await qdrant_client.search_by_url("https://example.com/page1")
            
            assert result == [
                "https://example.com/page1",
                '{"title": "Page 1"}',
                "page1",
                "example.com"
            ]

    @pytest.mark.asyncio
    async def test_search_by_url_not_found(self, qdrant_client, mock_qdrant_client):
        """Test searching by URL when not found"""
        mock_qdrant_client.scroll = AsyncMock(return_value=([], None))
        
        with patch('nlweb_qdrant_vectordb.qdrant_client.AsyncQdrantClient', return_value=mock_qdrant_client):
            await qdrant_client._get_qdrant_client()  # Initialize cache
            result = await qdrant_client.search_by_url("https://example.com/notfound")
            
            assert result is None

    @pytest.mark.asyncio
    async def test_search_by_url_collection_not_found(self, qdrant_client, mock_qdrant_client):
        """Test searching by URL when collection doesn't exist"""
        mock_qdrant_client.scroll = AsyncMock(side_effect=Exception("Collection not found"))
        
        with patch('nlweb_qdrant_vectordb.qdrant_client.AsyncQdrantClient', return_value=mock_qdrant_client):
            await qdrant_client._get_qdrant_client()  # Initialize cache
            result = await qdrant_client.search_by_url("https://example.com/page1")
            
            assert result is None

    @pytest.mark.asyncio
    async def test_get_sites(self, qdrant_client, mock_qdrant_client):
        """Test getting unique sites"""
        mock_point1 = MagicMock()
        mock_point1.payload = {"site": "site1.com"}
        mock_point2 = MagicMock()
        mock_point2.payload = {"site": "site2.com"}
        mock_point3 = MagicMock()
        mock_point3.payload = {"site": "site1.com"}  # Duplicate
        
        mock_qdrant_client.collection_exists = AsyncMock(return_value=True)
        mock_qdrant_client.scroll = AsyncMock(
            return_value=([mock_point1, mock_point2, mock_point3], None)
        )
        
        with patch('nlweb_qdrant_vectordb.qdrant_client.AsyncQdrantClient', return_value=mock_qdrant_client):
            await qdrant_client._get_qdrant_client()  # Initialize cache
            sites = await qdrant_client.get_sites()
            
            assert sites == ["site1.com", "site2.com"]  # Deduplicated and sorted

    @pytest.mark.asyncio
    async def test_get_sites_collection_not_exists(self, qdrant_client, mock_qdrant_client):
        """Test getting sites when collection doesn't exist"""
        mock_qdrant_client.collection_exists = AsyncMock(return_value=False)
        
        with patch('nlweb_qdrant_vectordb.qdrant_client.AsyncQdrantClient', return_value=mock_qdrant_client):
            await qdrant_client._get_qdrant_client()  # Initialize cache
            sites = await qdrant_client.get_sites()
            
            assert sites == []

    @pytest.mark.asyncio
    async def test_get_sites_pagination(self, qdrant_client, mock_qdrant_client):
        """Test getting sites with pagination"""
        mock_point1 = MagicMock()
        mock_point1.payload = {"site": "site1.com"}
        mock_point2 = MagicMock()
        mock_point2.payload = {"site": "site2.com"}
        
        mock_qdrant_client.collection_exists = AsyncMock(return_value=True)
        # First call returns one point with offset, second call returns another point with no offset
        mock_qdrant_client.scroll = AsyncMock(side_effect=[
            ([mock_point1], "offset1"),
            ([mock_point2], None)
        ])
        
        with patch('nlweb_qdrant_vectordb.qdrant_client.AsyncQdrantClient', return_value=mock_qdrant_client):
            await qdrant_client._get_qdrant_client()  # Initialize cache
            sites = await qdrant_client.get_sites()
            
            assert len(sites) == 2
            assert mock_qdrant_client.scroll.call_count == 2


class TestQdrantClientHelpers:
    """Tests for helper methods"""

    def test_resolve_path_absolute(self, qdrant_client):
        """Test resolving absolute path"""
        path = "/absolute/path/to/db"
        resolved = qdrant_client._resolve_path(path)
        
        assert resolved == path

    def test_resolve_path_relative(self, qdrant_client):
        """Test resolving relative path"""
        path = "../data/db"
        resolved = qdrant_client._resolve_path(path)
        
        assert isinstance(resolved, str)
        assert len(resolved) > len(path)  # Should be expanded

    def test_create_client_params_url(self, qdrant_client):
        """Test creating client parameters with URL"""
        params = qdrant_client._create_client_params()
        
        assert "url" in params
        assert params["url"] == "https://test.qdrant.tech"
        assert params["api_key"] == "test_api_key"

    def test_create_client_params_local_path(self, mock_config):
        """Test creating client parameters with local path"""
        mock_config.retrieval_endpoints["test_endpoint"].api_endpoint = None
        mock_config.retrieval_endpoints["test_endpoint"].database_path = "./data/qdrant"
        
        with patch('nlweb_qdrant_vectordb.qdrant_client.CONFIG', mock_config):
            client = QdrantClient(endpoint_name="test_endpoint")
            params = client._create_client_params()
            
            assert "path" in params
            assert "url" not in params
