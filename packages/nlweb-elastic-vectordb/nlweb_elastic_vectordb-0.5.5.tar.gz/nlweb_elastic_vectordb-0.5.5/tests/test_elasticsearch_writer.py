# Copyright (c) 2025 Microsoft Corporation.
# Licensed under the MIT License

"""
Tests for Elasticsearch Writer
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime, timezone

from nlweb_elastic_vectordb.elasticsearch_writer import ElasticsearchWriter


@pytest.fixture
def mock_config():
    """Mock CONFIG object for dataload"""
    config = MagicMock()
    config.write_endpoint = "test_endpoint"
    
    endpoint_config = {
        'db_type': 'elasticsearch',
        'api_endpoint': 'https://test.elasticsearch.com',
        'api_key': 'test_api_key',
        'index_name': 'test_index'
    }
    
    config.get_database_endpoint = MagicMock(return_value=endpoint_config)
    
    return config


@pytest.fixture
def mock_es_client():
    """Mock Elasticsearch client"""
    client = AsyncMock()
    client.indices = AsyncMock()
    client.indices.exists = AsyncMock(return_value=False)
    client.indices.create = AsyncMock()
    client.delete_by_query = AsyncMock(return_value={'deleted': 5})
    client.close = AsyncMock()
    return client


@pytest.fixture
def elasticsearch_writer(mock_config):
    """Create ElasticsearchWriter with mocked config"""
    with patch('nlweb_elastic_vectordb.elasticsearch_writer.CONFIG', mock_config):
        writer = ElasticsearchWriter(endpoint_name="test_endpoint")
        return writer


class TestElasticsearchWriterInit:
    """Tests for ElasticsearchWriter initialization"""

    def test_init_with_valid_config(self, mock_config):
        """Test initialization with valid configuration"""
        with patch('nlweb_elastic_vectordb.elasticsearch_writer.CONFIG', mock_config):
            writer = ElasticsearchWriter(endpoint_name="test_endpoint")
            
            assert writer.endpoint_name == "test_endpoint"
            assert writer.api_endpoint == "https://test.elasticsearch.com"
            assert writer.api_key == "test_api_key"
            assert writer.default_index_name == "test_index"

    def test_init_without_endpoint_name(self, mock_config):
        """Test initialization without endpoint name uses default"""
        with patch('nlweb_elastic_vectordb.elasticsearch_writer.CONFIG', mock_config):
            writer = ElasticsearchWriter()
            
            assert writer.endpoint_name == "test_endpoint"

    def test_init_no_config(self):
        """Test initialization fails when CONFIG is None"""
        with patch('nlweb_elastic_vectordb.elasticsearch_writer.CONFIG', None):
            with pytest.raises(ValueError, match="nlweb_dataload not configured"):
                ElasticsearchWriter(endpoint_name="test_endpoint")

    def test_init_wrong_db_type(self, mock_config):
        """Test initialization fails with wrong database type"""
        mock_config.get_database_endpoint.return_value = {
            'db_type': 'qdrant',
            'api_endpoint': 'https://test.elasticsearch.com',
            'api_key': 'test_api_key',
            'index_name': 'test_index'
        }
        
        with patch('nlweb_elastic_vectordb.elasticsearch_writer.CONFIG', mock_config):
            with pytest.raises(ValueError, match="not an Elasticsearch endpoint"):
                ElasticsearchWriter(endpoint_name="test_endpoint")

    def test_init_missing_api_endpoint(self, mock_config):
        """Test initialization fails with missing API endpoint"""
        mock_config.get_database_endpoint.return_value = {
            'db_type': 'elasticsearch',
            'api_endpoint': None,
            'api_key': 'test_api_key',
            'index_name': 'test_index'
        }
        
        with patch('nlweb_elastic_vectordb.elasticsearch_writer.CONFIG', mock_config):
            with pytest.raises(ValueError, match="api_endpoint not configured"):
                ElasticsearchWriter(endpoint_name="test_endpoint")

    def test_init_missing_api_key(self, mock_config):
        """Test initialization fails with missing API key"""
        mock_config.get_database_endpoint.return_value = {
            'db_type': 'elasticsearch',
            'api_endpoint': 'https://test.elasticsearch.com',
            'api_key': None,
            'index_name': 'test_index'
        }
        
        with patch('nlweb_elastic_vectordb.elasticsearch_writer.CONFIG', mock_config):
            with pytest.raises(ValueError, match="api_key not configured"):
                ElasticsearchWriter(endpoint_name="test_endpoint")


class TestElasticsearchWriterMethods:
    """Tests for ElasticsearchWriter methods"""

    def test_get_es_client(self, elasticsearch_writer):
        """Test getting Elasticsearch client"""
        with patch('nlweb_elastic_vectordb.elasticsearch_writer.AsyncElasticsearch') as mock_es:
            client = elasticsearch_writer._get_es_client()
            
            mock_es.assert_called_once_with(
                hosts="https://test.elasticsearch.com",
                api_key="test_api_key"
            )

    def test_generate_document_id(self, elasticsearch_writer):
        """Test generating document ID"""
        doc_id = elasticsearch_writer._generate_document_id(
            "https://example.com/page1",
            "example.com"
        )
        
        assert isinstance(doc_id, str)
        assert len(doc_id) == 32  # MD5 hash length
        
        # Same inputs should produce same ID
        doc_id2 = elasticsearch_writer._generate_document_id(
            "https://example.com/page1",
            "example.com"
        )
        assert doc_id == doc_id2

    @pytest.mark.asyncio
    async def test_ensure_index_exists_creates_index(self, elasticsearch_writer, mock_es_client):
        """Test ensuring index exists creates it when needed"""
        mock_es_client.indices.exists = AsyncMock(return_value=False)
        
        with patch('nlweb_elastic_vectordb.elasticsearch_writer.AsyncElasticsearch', return_value=mock_es_client):
            await elasticsearch_writer._ensure_index_exists("test_index", 1536)
            
            mock_es_client.indices.create.assert_called_once()
            mock_es_client.close.assert_called_once()

    @pytest.mark.asyncio
    async def test_ensure_index_exists_already_exists(self, elasticsearch_writer, mock_es_client):
        """Test ensuring index exists when it already exists"""
        mock_es_client.indices.exists = AsyncMock(return_value=True)
        
        with patch('nlweb_elastic_vectordb.elasticsearch_writer.AsyncElasticsearch', return_value=mock_es_client):
            await elasticsearch_writer._ensure_index_exists("test_index", 1536)
            
            mock_es_client.indices.create.assert_not_called()
            mock_es_client.close.assert_called_once()

    @pytest.mark.asyncio
    async def test_upload_documents_success(self, elasticsearch_writer, mock_es_client):
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
        
        mock_es_client.indices.exists = AsyncMock(return_value=True)
        
        with patch('nlweb_elastic_vectordb.elasticsearch_writer.AsyncElasticsearch', return_value=mock_es_client):
            with patch('nlweb_elastic_vectordb.elasticsearch_writer.async_bulk', return_value=(2, [])):
                result = await elasticsearch_writer.upload_documents(documents)
                
                assert result['success_count'] == 2
                assert result['error_count'] == 0
                assert result['total'] == 2

    @pytest.mark.asyncio
    async def test_upload_documents_with_custom_id(self, elasticsearch_writer, mock_es_client):
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
        
        mock_es_client.indices.exists = AsyncMock(return_value=True)
        
        with patch('nlweb_elastic_vectordb.elasticsearch_writer.AsyncElasticsearch', return_value=mock_es_client):
            with patch('nlweb_elastic_vectordb.elasticsearch_writer.async_bulk', return_value=(1, [])) as mock_bulk:
                result = await elasticsearch_writer.upload_documents(documents)
                
                # Verify custom ID was used
                call_args = mock_bulk.call_args
                actions = call_args[0][1]
                assert actions[0]['_id'] == 'custom_id_1'

    @pytest.mark.asyncio
    async def test_upload_documents_with_timestamp(self, elasticsearch_writer, mock_es_client):
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
        
        mock_es_client.indices.exists = AsyncMock(return_value=True)
        
        with patch('nlweb_elastic_vectordb.elasticsearch_writer.AsyncElasticsearch', return_value=mock_es_client):
            with patch('nlweb_elastic_vectordb.elasticsearch_writer.async_bulk', return_value=(1, [])) as mock_bulk:
                result = await elasticsearch_writer.upload_documents(documents)
                
                # Verify timestamp was used
                call_args = mock_bulk.call_args
                actions = call_args[0][1]
                assert actions[0]['_source']['timestamp'] == timestamp

    @pytest.mark.asyncio
    async def test_upload_documents_creates_index(self, elasticsearch_writer, mock_es_client):
        """Test uploading documents creates index if needed"""
        documents = [
            {
                'url': 'https://example.com/page1',
                'site': 'example.com',
                'name': 'page1',
                'schema_json': '{"title": "Page 1"}',
                'embedding': [0.1] * 1536
            }
        ]
        
        mock_es_client.indices.exists = AsyncMock(return_value=False)
        
        with patch('nlweb_elastic_vectordb.elasticsearch_writer.AsyncElasticsearch', return_value=mock_es_client):
            with patch('nlweb_elastic_vectordb.elasticsearch_writer.async_bulk', return_value=(1, [])):
                result = await elasticsearch_writer.upload_documents(documents)
                
                mock_es_client.indices.create.assert_called_once()

    @pytest.mark.asyncio
    async def test_upload_documents_empty_list(self, elasticsearch_writer, mock_es_client):
        """Test uploading empty document list"""
        with patch('nlweb_elastic_vectordb.elasticsearch_writer.AsyncElasticsearch', return_value=mock_es_client):
            with patch('nlweb_elastic_vectordb.elasticsearch_writer.async_bulk', return_value=(0, [])):
                result = await elasticsearch_writer.upload_documents([])
                
                assert result['success_count'] == 0
                assert result['error_count'] == 0
                assert result['total'] == 0

    @pytest.mark.asyncio
    async def test_upload_documents_with_failures(self, elasticsearch_writer, mock_es_client):
        """Test uploading documents with some failures"""
        documents = [
            {
                'url': 'https://example.com/page1',
                'site': 'example.com',
                'name': 'page1',
                'schema_json': '{"title": "Page 1"}',
                'embedding': [0.1] * 1536
            }
        ]
        
        mock_es_client.indices.exists = AsyncMock(return_value=True)
        failed_items = [{'index': {'error': 'some error'}}]
        
        with patch('nlweb_elastic_vectordb.elasticsearch_writer.AsyncElasticsearch', return_value=mock_es_client):
            with patch('nlweb_elastic_vectordb.elasticsearch_writer.async_bulk', return_value=(0, failed_items)):
                result = await elasticsearch_writer.upload_documents(documents)
                
                assert result['success_count'] == 0
                assert result['error_count'] == 1
                assert result['total'] == 1

    @pytest.mark.asyncio
    async def test_upload_documents_custom_index(self, elasticsearch_writer, mock_es_client):
        """Test uploading documents to custom index"""
        documents = [
            {
                'url': 'https://example.com/page1',
                'site': 'example.com',
                'name': 'page1',
                'schema_json': '{"title": "Page 1"}',
                'embedding': [0.1] * 1536
            }
        ]
        
        mock_es_client.indices.exists = AsyncMock(return_value=True)
        
        with patch('nlweb_elastic_vectordb.elasticsearch_writer.AsyncElasticsearch', return_value=mock_es_client):
            with patch('nlweb_elastic_vectordb.elasticsearch_writer.async_bulk', return_value=(1, [])) as mock_bulk:
                result = await elasticsearch_writer.upload_documents(documents, index_name="custom_index")
                
                call_args = mock_bulk.call_args
                actions = call_args[0][1]
                assert actions[0]['_index'] == 'custom_index'

    @pytest.mark.asyncio
    async def test_delete_documents(self, elasticsearch_writer, mock_es_client):
        """Test deleting documents by filter criteria"""
        filter_criteria = {'site': 'example.com'}
        
        with patch('nlweb_elastic_vectordb.elasticsearch_writer.AsyncElasticsearch', return_value=mock_es_client):
            result = await elasticsearch_writer.delete_documents(filter_criteria)
            
            assert result['deleted_count'] == 5
            mock_es_client.delete_by_query.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_documents_multiple_criteria(self, elasticsearch_writer, mock_es_client):
        """Test deleting documents with multiple filter criteria"""
        filter_criteria = {'site': 'example.com', 'name': 'page1'}
        
        with patch('nlweb_elastic_vectordb.elasticsearch_writer.AsyncElasticsearch', return_value=mock_es_client):
            result = await elasticsearch_writer.delete_documents(filter_criteria)
            
            mock_es_client.delete_by_query.assert_called_once()
            call_args = mock_es_client.delete_by_query.call_args
            assert 'query' in call_args.kwargs

    @pytest.mark.asyncio
    async def test_delete_documents_custom_index(self, elasticsearch_writer, mock_es_client):
        """Test deleting documents from custom index"""
        filter_criteria = {'site': 'example.com'}
        
        with patch('nlweb_elastic_vectordb.elasticsearch_writer.AsyncElasticsearch', return_value=mock_es_client):
            result = await elasticsearch_writer.delete_documents(
                filter_criteria,
                index_name="custom_index"
            )
            
            call_args = mock_es_client.delete_by_query.call_args
            assert call_args.kwargs['index'] == 'custom_index'

    @pytest.mark.asyncio
    async def test_delete_documents_empty_criteria(self, elasticsearch_writer, mock_es_client):
        """Test deleting documents with empty criteria (match all)"""
        filter_criteria = {}
        
        with patch('nlweb_elastic_vectordb.elasticsearch_writer.AsyncElasticsearch', return_value=mock_es_client):
            result = await elasticsearch_writer.delete_documents(filter_criteria)
            
            mock_es_client.delete_by_query.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_site(self, elasticsearch_writer, mock_es_client):
        """Test deleting all documents for a site"""
        with patch('nlweb_elastic_vectordb.elasticsearch_writer.AsyncElasticsearch', return_value=mock_es_client):
            result = await elasticsearch_writer.delete_site("example.com")
            
            assert result['deleted_count'] == 5
            mock_es_client.delete_by_query.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_site_custom_index(self, elasticsearch_writer, mock_es_client):
        """Test deleting site from custom index"""
        with patch('nlweb_elastic_vectordb.elasticsearch_writer.AsyncElasticsearch', return_value=mock_es_client):
            result = await elasticsearch_writer.delete_site("example.com", index_name="custom_index")
            
            call_args = mock_es_client.delete_by_query.call_args
            assert call_args.kwargs['index'] == 'custom_index'


class TestElasticsearchWriterIntegration:
    """Integration-style tests"""

    @pytest.mark.asyncio
    async def test_full_workflow(self, elasticsearch_writer, mock_es_client):
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
        
        mock_es_client.indices.exists = AsyncMock(return_value=True)
        
        with patch('nlweb_elastic_vectordb.elasticsearch_writer.AsyncElasticsearch', return_value=mock_es_client):
            # Upload documents
            with patch('nlweb_elastic_vectordb.elasticsearch_writer.async_bulk', return_value=(1, [])):
                upload_result = await elasticsearch_writer.upload_documents(documents)
                assert upload_result['success_count'] == 1
            
            # Delete documents
            delete_result = await elasticsearch_writer.delete_site("example.com")
            assert delete_result['deleted_count'] == 5
