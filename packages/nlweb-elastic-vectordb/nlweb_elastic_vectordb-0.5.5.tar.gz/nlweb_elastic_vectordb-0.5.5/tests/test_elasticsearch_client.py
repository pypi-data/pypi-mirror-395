# Copyright (c) 2025 Microsoft Corporation.
# Licensed under the MIT License

"""
Tests for Elasticsearch Client
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from typing import List, Dict, Any

from nlweb_elastic_vectordb.elasticsearch_client import ElasticsearchClient


@pytest.fixture
def mock_config():
    """Mock CONFIG object"""
    config = MagicMock()
    config.write_endpoint = "test_endpoint"
    
    # Mock endpoint config
    endpoint_config = MagicMock()
    endpoint_config.db_type = "elasticsearch"
    endpoint_config.api_endpoint = "https://test.elasticsearch.com"
    endpoint_config.api_key = "test_api_key"
    endpoint_config.index_name = "test_index"
    endpoint_config.vector_dimensions = 1536
    
    config.retrieval_endpoints = {"test_endpoint": endpoint_config}
    
    return config


@pytest.fixture
def mock_es_client():
    """Mock Elasticsearch client"""
    client = AsyncMock()
    client.info = AsyncMock(return_value={"version": "8.0.0"})
    client.indices = AsyncMock()
    client.indices.exists = AsyncMock(return_value=False)
    client.indices.create = AsyncMock()
    client.indices.delete = AsyncMock()
    client.search = AsyncMock()
    client.close = AsyncMock()
    return client


@pytest.fixture
def elasticsearch_client(mock_config):
    """Create ElasticsearchClient with mocked config"""
    with patch('nlweb_elastic_vectordb.elasticsearch_client.CONFIG', mock_config):
        client = ElasticsearchClient(endpoint_name="test_endpoint")
        return client


class TestElasticsearchClientInit:
    """Tests for ElasticsearchClient initialization"""

    def test_init_with_valid_config(self, mock_config):
        """Test initialization with valid configuration"""
        with patch('nlweb_elastic_vectordb.elasticsearch_client.CONFIG', mock_config):
            client = ElasticsearchClient(endpoint_name="test_endpoint")
            
            assert client.endpoint_name == "test_endpoint"
            assert client.api_endpoint == "https://test.elasticsearch.com"
            assert client.api_key == "test_api_key"
            assert client.default_index_name == "test_index"

    def test_init_without_endpoint_name(self, mock_config):
        """Test initialization without endpoint name uses default"""
        with patch('nlweb_elastic_vectordb.elasticsearch_client.CONFIG', mock_config):
            client = ElasticsearchClient()
            
            assert client.endpoint_name == "test_endpoint"

    def test_init_missing_api_endpoint(self, mock_config):
        """Test initialization fails with missing API endpoint"""
        mock_config.retrieval_endpoints["test_endpoint"].api_endpoint = None
        
        with patch('nlweb_elastic_vectordb.elasticsearch_client.CONFIG', mock_config):
            with pytest.raises(ValueError, match="API endpoint not configured"):
                ElasticsearchClient(endpoint_name="test_endpoint")

    def test_init_missing_api_key(self, mock_config):
        """Test initialization fails with missing API key"""
        mock_config.retrieval_endpoints["test_endpoint"].api_key = None
        
        with patch('nlweb_elastic_vectordb.elasticsearch_client.CONFIG', mock_config):
            with pytest.raises(ValueError, match="API key not configured"):
                ElasticsearchClient(endpoint_name="test_endpoint")

    def test_init_wrong_db_type(self, mock_config):
        """Test initialization fails with wrong database type"""
        mock_config.retrieval_endpoints["test_endpoint"].db_type = "azure_ai_search"
        
        with patch('nlweb_elastic_vectordb.elasticsearch_client.CONFIG', mock_config):
            with pytest.raises(ValueError, match="not an Elasticsearch endpoint"):
                ElasticsearchClient(endpoint_name="test_endpoint")

    def test_init_missing_endpoint_config(self, mock_config):
        """Test initialization fails with missing endpoint configuration"""
        mock_config.retrieval_endpoints = {}
        
        with patch('nlweb_elastic_vectordb.elasticsearch_client.CONFIG', mock_config):
            with pytest.raises(ValueError, match="No configuration found"):
                ElasticsearchClient(endpoint_name="test_endpoint")


class TestElasticsearchClientMethods:
    """Tests for ElasticsearchClient methods"""

    @pytest.mark.asyncio
    async def test_get_es_client(self, elasticsearch_client, mock_es_client):
        """Test getting Elasticsearch client"""
        with patch('nlweb_elastic_vectordb.elasticsearch_client.AsyncElasticsearch', return_value=mock_es_client):
            client = await elasticsearch_client._get_es_client()
            
            assert client == mock_es_client
            mock_es_client.info.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_es_client_caching(self, elasticsearch_client, mock_es_client):
        """Test that Elasticsearch client is cached"""
        with patch('nlweb_elastic_vectordb.elasticsearch_client.AsyncElasticsearch', return_value=mock_es_client):
            client1 = await elasticsearch_client._get_es_client()
            client2 = await elasticsearch_client._get_es_client()
            
            assert client1 == client2
            # info() should only be called once due to caching
            assert mock_es_client.info.call_count == 1

    @pytest.mark.asyncio
    async def test_create_index_if_not_exists_creates_index(self, elasticsearch_client, mock_es_client):
        """Test creating index when it doesn't exist"""
        mock_es_client.indices.exists = AsyncMock(return_value=False)
        
        with patch('nlweb_elastic_vectordb.elasticsearch_client.AsyncElasticsearch', return_value=mock_es_client):
            await elasticsearch_client._get_es_client()  # Initialize cache
            result = await elasticsearch_client.create_index_if_not_exists("new_index")
            
            assert result is True
            mock_es_client.indices.create.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_index_if_not_exists_exists(self, elasticsearch_client, mock_es_client):
        """Test when index already exists"""
        mock_es_client.indices.exists = AsyncMock(return_value=True)
        
        with patch('nlweb_elastic_vectordb.elasticsearch_client.AsyncElasticsearch', return_value=mock_es_client):
            await elasticsearch_client._get_es_client()  # Initialize cache
            result = await elasticsearch_client.create_index_if_not_exists("existing_index")
            
            assert result is False
            mock_es_client.indices.create.assert_not_called()

    @pytest.mark.asyncio
    async def test_delete_index(self, elasticsearch_client, mock_es_client):
        """Test deleting an index"""
        with patch('nlweb_elastic_vectordb.elasticsearch_client.AsyncElasticsearch', return_value=mock_es_client):
            await elasticsearch_client._get_es_client()  # Initialize cache
            result = await elasticsearch_client.delete_index("test_index")
            
            assert result is True
            mock_es_client.indices.delete.assert_called_once_with(
                index="test_index",
                ignore_unavailable=True
            )

    @pytest.mark.asyncio
    async def test_format_es_response(self, elasticsearch_client):
        """Test formatting Elasticsearch response"""
        mock_response = {
            "hits": {
                "hits": [
                    {
                        "_source": {
                            "url": "https://example.com/page1",
                            "schema_json": '{"title": "Page 1"}',
                            "name": "page1",
                            "site": "example.com"
                        }
                    },
                    {
                        "_source": {
                            "url": "https://example.com/page2",
                            "schema_json": '{"title": "Page 2"}',
                            "name": "page2",
                            "site": "example.com"
                        }
                    }
                ]
            }
        }
        
        results = await elasticsearch_client._format_es_response(mock_response)
        
        assert len(results) == 2
        assert results[0] == ["https://example.com/page1", '{"title": "Page 1"}', "page1", "example.com"]
        assert results[1] == ["https://example.com/page2", '{"title": "Page 2"}', "page2", "example.com"]

    @pytest.mark.asyncio
    async def test_search(self, elasticsearch_client, mock_es_client):
        """Test search functionality"""
        mock_embedding = [0.1] * 1536
        mock_search_response = {
            "hits": {
                "hits": [
                    {
                        "_source": {
                            "url": "https://example.com/page1",
                            "schema_json": '{"title": "Page 1"}',
                            "name": "page1",
                            "site": "example.com"
                        }
                    }
                ]
            }
        }
        
        mock_es_client.search = AsyncMock(return_value=mock_search_response)
        mock_es_client.indices.exists = AsyncMock(return_value=True)
        
        with patch('nlweb_elastic_vectordb.elasticsearch_client.AsyncElasticsearch', return_value=mock_es_client):
            with patch('nlweb_elastic_vectordb.elasticsearch_client.get_embedding', return_value=mock_embedding):
                await elasticsearch_client._get_es_client()  # Initialize cache
                results = await elasticsearch_client.search(
                    query="test query",
                    site="example.com",
                    num_results=10
                )
                
                assert len(results) == 1
                assert results[0][0] == "https://example.com/page1"
                mock_es_client.search.assert_called_once()

    @pytest.mark.asyncio
    async def test_search_multiple_sites(self, elasticsearch_client, mock_es_client):
        """Test search with multiple sites"""
        mock_embedding = [0.1] * 1536
        mock_search_response = {"hits": {"hits": []}}
        
        mock_es_client.search = AsyncMock(return_value=mock_search_response)
        mock_es_client.indices.exists = AsyncMock(return_value=True)
        
        with patch('nlweb_elastic_vectordb.elasticsearch_client.AsyncElasticsearch', return_value=mock_es_client):
            with patch('nlweb_elastic_vectordb.elasticsearch_client.get_embedding', return_value=mock_embedding):
                await elasticsearch_client._get_es_client()  # Initialize cache
                results = await elasticsearch_client.search(
                    query="test query",
                    site=["site1.com", "site2.com"],
                    num_results=10
                )
                
                assert results == []
                mock_es_client.search.assert_called_once()

    @pytest.mark.asyncio
    async def test_search_all_sites(self, elasticsearch_client, mock_es_client):
        """Test search across all sites"""
        mock_embedding = [0.1] * 1536
        mock_search_response = {"hits": {"hits": []}}
        
        mock_es_client.search = AsyncMock(return_value=mock_search_response)
        mock_es_client.indices.exists = AsyncMock(return_value=True)
        
        with patch('nlweb_elastic_vectordb.elasticsearch_client.AsyncElasticsearch', return_value=mock_es_client):
            with patch('nlweb_elastic_vectordb.elasticsearch_client.get_embedding', return_value=mock_embedding):
                await elasticsearch_client._get_es_client()  # Initialize cache
                results = await elasticsearch_client.search_all_sites(
                    query="test query",
                    num_results=10
                )
                
                assert results == []
                mock_es_client.search.assert_called_once()

    @pytest.mark.asyncio
    async def test_search_by_url(self, elasticsearch_client, mock_es_client):
        """Test searching by URL"""
        mock_search_response = {
            "hits": {
                "hits": [
                    {
                        "_source": {
                            "url": "https://example.com/page1",
                            "schema_json": '{"title": "Page 1"}',
                            "name": "page1",
                            "site": "example.com"
                        }
                    }
                ]
            }
        }
        
        mock_es_client.search = AsyncMock(return_value=mock_search_response)
        
        with patch('nlweb_elastic_vectordb.elasticsearch_client.AsyncElasticsearch', return_value=mock_es_client):
            await elasticsearch_client._get_es_client()  # Initialize cache
            result = await elasticsearch_client.search_by_url("https://example.com/page1")
            
            assert result == ["https://example.com/page1", '{"title": "Page 1"}', "page1", "example.com"]
            mock_es_client.search.assert_called_once()

    @pytest.mark.asyncio
    async def test_search_by_url_not_found(self, elasticsearch_client, mock_es_client):
        """Test searching by URL when not found"""
        mock_search_response = {"hits": {"hits": []}}
        
        mock_es_client.search = AsyncMock(return_value=mock_search_response)
        
        with patch('nlweb_elastic_vectordb.elasticsearch_client.AsyncElasticsearch', return_value=mock_es_client):
            await elasticsearch_client._get_es_client()  # Initialize cache
            result = await elasticsearch_client.search_by_url("https://example.com/notfound")
            
            assert result is None

    @pytest.mark.asyncio
    async def test_get_sites(self, elasticsearch_client, mock_es_client):
        """Test getting unique sites"""
        mock_agg_response = {
            "aggregations": {
                "unique_sites": {
                    "buckets": [
                        {"key": "site1.com"},
                        {"key": "site2.com"},
                        {"key": "site3.com"}
                    ]
                }
            }
        }
        
        mock_es_client.indices.exists = AsyncMock(return_value=True)
        mock_es_client.search = AsyncMock(return_value=mock_agg_response)
        
        with patch('nlweb_elastic_vectordb.elasticsearch_client.AsyncElasticsearch', return_value=mock_es_client):
            await elasticsearch_client._get_es_client()  # Initialize cache
            sites = await elasticsearch_client.get_sites()
            
            assert sites == ["site1.com", "site2.com", "site3.com"]
            mock_es_client.search.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_sites_index_not_exists(self, elasticsearch_client, mock_es_client):
        """Test getting sites when index doesn't exist"""
        mock_es_client.indices.exists = AsyncMock(return_value=False)
        
        with patch('nlweb_elastic_vectordb.elasticsearch_client.AsyncElasticsearch', return_value=mock_es_client):
            await elasticsearch_client._get_es_client()  # Initialize cache
            sites = await elasticsearch_client.get_sites()
            
            assert sites == []
            mock_es_client.search.assert_not_called()

    @pytest.mark.asyncio
    async def test_close(self, elasticsearch_client, mock_es_client):
        """Test closing client connections"""
        with patch('nlweb_elastic_vectordb.elasticsearch_client.AsyncElasticsearch', return_value=mock_es_client):
            await elasticsearch_client._get_es_client()  # Initialize cache
            await elasticsearch_client.close()
            
            mock_es_client.close.assert_called_once()
            assert elasticsearch_client._es_clients == {}

    @pytest.mark.asyncio
    async def test_context_manager(self, elasticsearch_client, mock_es_client):
        """Test async context manager"""
        with patch('nlweb_elastic_vectordb.elasticsearch_client.AsyncElasticsearch', return_value=mock_es_client):
            async with elasticsearch_client as client:
                assert client == elasticsearch_client
                await client._get_es_client()  # Initialize cache
            
            # Client should be closed after exiting context
            mock_es_client.close.assert_called_once()


class TestElasticsearchClientHelpers:
    """Tests for helper methods"""

    def test_create_client_params(self, elasticsearch_client):
        """Test creating client parameters"""
        params = elasticsearch_client._create_client_params()
        
        assert params["hosts"] == "https://test.elasticsearch.com"
        assert params["api_key"] == "test_api_key"

    def test_create_vector_properties(self, elasticsearch_client):
        """Test creating vector properties"""
        props = elasticsearch_client._create_vector_properties()
        
        assert props["dims"] == 1536
        assert props["index"] is True
        assert props["similarity"] == "cosine"

    def test_create_vector_properties_custom_dims(self, mock_config):
        """Test creating vector properties with custom dimensions"""
        mock_config.retrieval_endpoints["test_endpoint"].vector_dimensions = 768
        
        with patch('nlweb_elastic_vectordb.elasticsearch_client.CONFIG', mock_config):
            client = ElasticsearchClient(endpoint_name="test_endpoint")
            props = client._create_vector_properties()
            
            assert props["dims"] == 768
