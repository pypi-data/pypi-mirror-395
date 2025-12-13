# Copyright (c) 2025 Microsoft Corporation.
# Licensed under the MIT License

"""
Tests for Qdrant Writer
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime, timezone

from nlweb_qdrant_vectordb.qdrant_writer import QdrantWriter


@pytest.fixture
def mock_config():
    """Mock CONFIG object for dataload"""
    config = MagicMock()
    config.write_endpoint = "test_endpoint"
    
    endpoint_config = {
        'db_type': 'qdrant',
        'api_endpoint': 'https://test.qdrant.tech',
        'api_key': 'test_api_key',
        'database_path': None,
        'index_name': 'test_collection'
    }
    
    config.get_database_endpoint = MagicMock(return_value=endpoint_config)
    
    return config


@pytest.fixture
def mock_qdrant_client():
    """Mock Qdrant client"""
    client = AsyncMock()
    client.collection_exists = AsyncMock(return_value=False)
    client.create_collection = AsyncMock()
    client.upsert = AsyncMock()
    client.delete = AsyncMock(return_value=True)
    client.close = AsyncMock()
    return client


@pytest.fixture
def qdrant_writer(mock_config):
    """Create QdrantWriter with mocked config"""
    with patch('nlweb_qdrant_vectordb.qdrant_writer.CONFIG', mock_config):
        writer = QdrantWriter(endpoint_name="test_endpoint")
        return writer


class TestQdrantWriterInit:
    """Tests for QdrantWriter initialization"""

    def test_init_with_valid_config(self, mock_config):
        """Test initialization with valid configuration"""
        with patch('nlweb_qdrant_vectordb.qdrant_writer.CONFIG', mock_config):
            writer = QdrantWriter(endpoint_name="test_endpoint")
            
            assert writer.endpoint_name == "test_endpoint"
            assert writer.api_endpoint == "https://test.qdrant.tech"
            assert writer.api_key == "test_api_key"
            assert writer.default_collection_name == "test_collection"

    def test_init_without_endpoint_name(self, mock_config):
        """Test initialization without endpoint name uses default"""
        with patch('nlweb_qdrant_vectordb.qdrant_writer.CONFIG', mock_config):
            writer = QdrantWriter()
            
            assert writer.endpoint_name == "test_endpoint"

    def test_init_no_config(self):
        """Test initialization fails when CONFIG is None"""
        with patch('nlweb_qdrant_vectordb.qdrant_writer.CONFIG', None):
            with pytest.raises(ValueError, match="nlweb_dataload not configured"):
                QdrantWriter(endpoint_name="test_endpoint")

    def test_init_wrong_db_type(self, mock_config):
        """Test initialization fails with wrong database type"""
        mock_config.get_database_endpoint.return_value = {
            'db_type': 'elasticsearch',
            'api_endpoint': 'https://test.qdrant.tech',
            'api_key': 'test_api_key',
            'index_name': 'test_collection'
        }
        
        with patch('nlweb_qdrant_vectordb.qdrant_writer.CONFIG', mock_config):
            with pytest.raises(ValueError, match="not a Qdrant endpoint"):
                QdrantWriter(endpoint_name="test_endpoint")

    def test_init_with_local_path(self, mock_config):
        """Test initialization with local database path"""
        mock_config.get_database_endpoint.return_value = {
            'db_type': 'qdrant',
            'api_endpoint': None,
            'api_key': None,
            'database_path': './data/qdrant',
            'index_name': 'test_collection'
        }
        
        with patch('nlweb_qdrant_vectordb.qdrant_writer.CONFIG', mock_config):
            writer = QdrantWriter(endpoint_name="test_endpoint")
            
            assert writer.database_path == './data/qdrant'
            assert writer.api_endpoint is None


class TestQdrantWriterMethods:
    """Tests for QdrantWriter methods"""

    def test_get_qdrant_client_url(self, qdrant_writer):
        """Test getting Qdrant client with URL"""
        with patch('nlweb_qdrant_vectordb.qdrant_writer.AsyncQdrantClient') as mock_client:
            client = qdrant_writer._get_qdrant_client()
            
            mock_client.assert_called_once()
            call_kwargs = mock_client.call_args.kwargs
            assert 'url' in call_kwargs
            assert call_kwargs['url'] == 'https://test.qdrant.tech'

    def test_get_qdrant_client_local(self, mock_config):
        """Test getting Qdrant client with local path"""
        mock_config.get_database_endpoint.return_value = {
            'db_type': 'qdrant',
            'api_endpoint': None,
            'api_key': None,
            'database_path': './data/qdrant',
            'index_name': 'test_collection'
        }
        
        with patch('nlweb_qdrant_vectordb.qdrant_writer.CONFIG', mock_config):
            writer = QdrantWriter(endpoint_name="test_endpoint")
            
            with patch('nlweb_qdrant_vectordb.qdrant_writer.AsyncQdrantClient') as mock_client:
                client = writer._get_qdrant_client()
                
                call_kwargs = mock_client.call_args.kwargs
                assert 'path' in call_kwargs

    def test_generate_document_id(self, qdrant_writer):
        """Test generating document ID"""
        doc_id = qdrant_writer._generate_document_id(
            "https://example.com/page1",
            "example.com"
        )
        
        assert isinstance(doc_id, str)
        # UUID5 format
        assert len(doc_id) == 36  # UUID string length
        
        # Same inputs should produce same ID
        doc_id2 = qdrant_writer._generate_document_id(
            "https://example.com/page1",
            "example.com"
        )
        assert doc_id == doc_id2

    @pytest.mark.asyncio
    async def test_ensure_collection_exists_creates(self, qdrant_writer, mock_qdrant_client):
        """Test ensuring collection exists creates it when needed"""
        mock_qdrant_client.collection_exists = AsyncMock(return_value=False)
        
        with patch('nlweb_qdrant_vectordb.qdrant_writer.AsyncQdrantClient', return_value=mock_qdrant_client):
            await qdrant_writer._ensure_collection_exists("test_collection", 1536)
            
            mock_qdrant_client.create_collection.assert_called_once()
            mock_qdrant_client.close.assert_called_once()

    @pytest.mark.asyncio
    async def test_ensure_collection_exists_already_exists(self, qdrant_writer, mock_qdrant_client):
        """Test ensuring collection exists when it already exists"""
        mock_qdrant_client.collection_exists = AsyncMock(return_value=True)
        
        with patch('nlweb_qdrant_vectordb.qdrant_writer.AsyncQdrantClient', return_value=mock_qdrant_client):
            await qdrant_writer._ensure_collection_exists("test_collection", 1536)
            
            mock_qdrant_client.create_collection.assert_not_called()
            mock_qdrant_client.close.assert_called_once()

    @pytest.mark.asyncio
    async def test_upload_documents_success(self, qdrant_writer, mock_qdrant_client):
        """Test successfully uploading documents"""
        documents = [
            {
                'url': 'https://example.com/page1',
                'site': 'example.com',
                'name': 'page1',
                'schema_json': '{"title": "Page 1"}',
                'embedding': [0.1] * 1536
            },
            {
                'url': 'https://example.com/page2',
                'site': 'example.com',
                'name': 'page2',
                'schema_json': '{"title": "Page 2"}',
                'embedding': [0.2] * 1536
            }
        ]
        
        mock_qdrant_client.collection_exists = AsyncMock(return_value=True)
        
        with patch('nlweb_qdrant_vectordb.qdrant_writer.AsyncQdrantClient', return_value=mock_qdrant_client):
            result = await qdrant_writer.upload_documents(documents)
            
            assert result['success_count'] == 2
            assert result['error_count'] == 0
            assert result['total'] == 2
            mock_qdrant_client.upsert.assert_called_once()

    @pytest.mark.asyncio
    async def test_upload_documents_with_custom_id(self, qdrant_writer, mock_qdrant_client):
        """Test uploading documents with custom IDs"""
        documents = [
            {
                'id': 'custom_id_1',
                'url': 'https://example.com/page1',
                'site': 'example.com',
                'name': 'page1',
                'schema_json': '{"title": "Page 1"}',
                'embedding': [0.1] * 1536
            }
        ]
        
        mock_qdrant_client.collection_exists = AsyncMock(return_value=True)
        
        with patch('nlweb_qdrant_vectordb.qdrant_writer.AsyncQdrantClient', return_value=mock_qdrant_client):
            result = await qdrant_writer.upload_documents(documents)
            
            assert result['success_count'] == 1
            # Verify custom ID was used
            call_args = mock_qdrant_client.upsert.call_args
            points = call_args.kwargs['points']
            assert points[0].id == 'custom_id_1'

    @pytest.mark.asyncio
    async def test_upload_documents_with_timestamp(self, qdrant_writer, mock_qdrant_client):
        """Test uploading documents with custom timestamp"""
        timestamp = datetime.now(timezone.utc).isoformat()
        documents = [
            {
                'url': 'https://example.com/page1',
                'site': 'example.com',
                'name': 'page1',
                'schema_json': '{"title": "Page 1"}',
                'embedding': [0.1] * 1536,
                'timestamp': timestamp
            }
        ]
        
        mock_qdrant_client.collection_exists = AsyncMock(return_value=True)
        
        with patch('nlweb_qdrant_vectordb.qdrant_writer.AsyncQdrantClient', return_value=mock_qdrant_client):
            result = await qdrant_writer.upload_documents(documents)
            
            # Verify timestamp was used
            call_args = mock_qdrant_client.upsert.call_args
            points = call_args.kwargs['points']
            assert points[0].payload['timestamp'] == timestamp

    @pytest.mark.asyncio
    async def test_upload_documents_creates_collection(self, qdrant_writer, mock_qdrant_client):
        """Test uploading documents creates collection if needed"""
        documents = [
            {
                'url': 'https://example.com/page1',
                'site': 'example.com',
                'name': 'page1',
                'schema_json': '{"title": "Page 1"}',
                'embedding': [0.1] * 1536
            }
        ]
        
        mock_qdrant_client.collection_exists = AsyncMock(return_value=False)
        
        with patch('nlweb_qdrant_vectordb.qdrant_writer.AsyncQdrantClient', return_value=mock_qdrant_client):
            result = await qdrant_writer.upload_documents(documents)
            
            mock_qdrant_client.create_collection.assert_called_once()

    @pytest.mark.asyncio
    async def test_upload_documents_skip_without_embedding(self, qdrant_writer, mock_qdrant_client):
        """Test uploading documents skips items without embeddings"""
        documents = [
            {
                'url': 'https://example.com/page1',
                'site': 'example.com',
                'name': 'page1',
                'schema_json': '{"title": "Page 1"}',
                'embedding': None  # No embedding
            },
            {
                'url': 'https://example.com/page2',
                'site': 'example.com',
                'name': 'page2',
                'schema_json': '{"title": "Page 2"}',
                'embedding': [0.2] * 1536
            }
        ]
        
        mock_qdrant_client.collection_exists = AsyncMock(return_value=True)
        
        with patch('nlweb_qdrant_vectordb.qdrant_writer.AsyncQdrantClient', return_value=mock_qdrant_client):
            result = await qdrant_writer.upload_documents(documents)
            
            # Only one document should be uploaded
            call_args = mock_qdrant_client.upsert.call_args
            points = call_args.kwargs['points']
            assert len(points) == 1

    @pytest.mark.asyncio
    async def test_upload_documents_batch_processing(self, qdrant_writer, mock_qdrant_client):
        """Test uploading documents in batches"""
        # Create more documents than batch size
        documents = [
            {
                'url': f'https://example.com/page{i}',
                'site': 'example.com',
                'name': f'page{i}',
                'schema_json': f'{{"title": "Page {i}"}}',
                'embedding': [0.1] * 1536
            }
            for i in range(150)  # More than batch size of 100
        ]
        
        mock_qdrant_client.collection_exists = AsyncMock(return_value=True)
        
        with patch('nlweb_qdrant_vectordb.qdrant_writer.AsyncQdrantClient', return_value=mock_qdrant_client):
            result = await qdrant_writer.upload_documents(documents)
            
            # Should be called twice (100 + 50)
            assert mock_qdrant_client.upsert.call_count == 2

    @pytest.mark.asyncio
    async def test_upload_documents_empty_list(self, qdrant_writer, mock_qdrant_client):
        """Test uploading empty document list"""
        with patch('nlweb_qdrant_vectordb.qdrant_writer.AsyncQdrantClient', return_value=mock_qdrant_client):
            result = await qdrant_writer.upload_documents([])
            
            assert result['success_count'] == 0
            assert result['error_count'] == 0
            assert result['total'] == 0

    @pytest.mark.asyncio
    async def test_upload_documents_batch_error(self, qdrant_writer, mock_qdrant_client):
        """Test uploading documents with batch error"""
        documents = [
            {
                'url': f'https://example.com/page{i}',
                'site': 'example.com',
                'name': f'page{i}',
                'schema_json': f'{{"title": "Page {i}"}}',
                'embedding': [0.1] * 1536
            }
            for i in range(150)
        ]
        
        mock_qdrant_client.collection_exists = AsyncMock(return_value=True)
        # First batch succeeds, second fails
        mock_qdrant_client.upsert = AsyncMock(side_effect=[None, Exception("Upload error")])
        
        with patch('nlweb_qdrant_vectordb.qdrant_writer.AsyncQdrantClient', return_value=mock_qdrant_client):
            result = await qdrant_writer.upload_documents(documents)
            
            # Should have partial success
            assert result['success_count'] == 100
            assert result['error_count'] == 50

    @pytest.mark.asyncio
    async def test_upload_documents_custom_collection(self, qdrant_writer, mock_qdrant_client):
        """Test uploading documents to custom collection"""
        documents = [
            {
                'url': 'https://example.com/page1',
                'site': 'example.com',
                'name': 'page1',
                'schema_json': '{"title": "Page 1"}',
                'embedding': [0.1] * 1536
            }
        ]
        
        mock_qdrant_client.collection_exists = AsyncMock(return_value=True)
        
        with patch('nlweb_qdrant_vectordb.qdrant_writer.AsyncQdrantClient', return_value=mock_qdrant_client):
            result = await qdrant_writer.upload_documents(
                documents,
                collection_name="custom_collection"
            )
            
            call_args = mock_qdrant_client.upsert.call_args
            assert call_args.kwargs['collection_name'] == 'custom_collection'

    @pytest.mark.asyncio
    async def test_delete_documents(self, qdrant_writer, mock_qdrant_client):
        """Test deleting documents by filter criteria"""
        filter_criteria = {'site': 'example.com'}
        
        with patch('nlweb_qdrant_vectordb.qdrant_writer.AsyncQdrantClient', return_value=mock_qdrant_client):
            result = await qdrant_writer.delete_documents(filter_criteria)
            
            assert result['deleted_count'] == 1
            mock_qdrant_client.delete.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_documents_multiple_criteria(self, qdrant_writer, mock_qdrant_client):
        """Test deleting documents with multiple filter criteria"""
        filter_criteria = {'site': 'example.com', 'name': 'page1'}
        
        with patch('nlweb_qdrant_vectordb.qdrant_writer.AsyncQdrantClient', return_value=mock_qdrant_client):
            result = await qdrant_writer.delete_documents(filter_criteria)
            
            mock_qdrant_client.delete.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_documents_custom_collection(self, qdrant_writer, mock_qdrant_client):
        """Test deleting documents from custom collection"""
        filter_criteria = {'site': 'example.com'}
        
        with patch('nlweb_qdrant_vectordb.qdrant_writer.AsyncQdrantClient', return_value=mock_qdrant_client):
            result = await qdrant_writer.delete_documents(
                filter_criteria,
                collection_name="custom_collection"
            )
            
            call_args = mock_qdrant_client.delete.call_args
            assert call_args.kwargs['collection_name'] == 'custom_collection'

    @pytest.mark.asyncio
    async def test_delete_documents_empty_criteria(self, qdrant_writer, mock_qdrant_client):
        """Test deleting documents with empty criteria"""
        filter_criteria = {}
        
        with patch('nlweb_qdrant_vectordb.qdrant_writer.AsyncQdrantClient', return_value=mock_qdrant_client):
            result = await qdrant_writer.delete_documents(filter_criteria)
            
            # Should not delete anything
            assert result['deleted_count'] == 0
            mock_qdrant_client.delete.assert_not_called()

    @pytest.mark.asyncio
    async def test_delete_site(self, qdrant_writer, mock_qdrant_client):
        """Test deleting all documents for a site"""
        with patch('nlweb_qdrant_vectordb.qdrant_writer.AsyncQdrantClient', return_value=mock_qdrant_client):
            result = await qdrant_writer.delete_site("example.com")
            
            assert result['deleted_count'] == 1
            mock_qdrant_client.delete.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_site_custom_collection(self, qdrant_writer, mock_qdrant_client):
        """Test deleting site from custom collection"""
        with patch('nlweb_qdrant_vectordb.qdrant_writer.AsyncQdrantClient', return_value=mock_qdrant_client):
            result = await qdrant_writer.delete_site(
                "example.com",
                collection_name="custom_collection"
            )
            
            call_args = mock_qdrant_client.delete.call_args
            assert call_args.kwargs['collection_name'] == 'custom_collection'


class TestQdrantWriterIntegration:
    """Integration-style tests"""

    @pytest.mark.asyncio
    async def test_full_workflow(self, qdrant_writer, mock_qdrant_client):
        """Test complete upload and delete workflow"""
        documents = [
            {
                'url': 'https://example.com/page1',
                'site': 'example.com',
                'name': 'page1',
                'schema_json': '{"title": "Page 1"}',
                'embedding': [0.1] * 1536
            }
        ]
        
        mock_qdrant_client.collection_exists = AsyncMock(return_value=True)
        
        with patch('nlweb_qdrant_vectordb.qdrant_writer.AsyncQdrantClient', return_value=mock_qdrant_client):
            # Upload documents
            upload_result = await qdrant_writer.upload_documents(documents)
            assert upload_result['success_count'] == 1
            
            # Delete documents
            delete_result = await qdrant_writer.delete_site("example.com")
            assert delete_result['deleted_count'] == 1
