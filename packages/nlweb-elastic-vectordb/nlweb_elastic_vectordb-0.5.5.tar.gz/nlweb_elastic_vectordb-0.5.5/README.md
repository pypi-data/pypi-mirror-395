# nlweb-elastic-vectordb

Elasticsearch provider for NLWeb.

## Overview

This package provides Elasticsearch vector database support for NLWeb, demonstrating how to create third-party provider packages.

## Installation

```bash
pip install nlweb-core nlweb-elastic-vectordb
```

For LLM and embedding, you'll also need a model provider:
```bash
pip install nlweb-azure-models
```

Or use the bundle packages:
```bash
pip install nlweb-core nlweb-retrieval nlweb-models
```

## Configuration

Create `config.yaml`:

```yaml
retrieval:
  provider: elasticsearch
  import_path: nlweb_elastic_vectordb.elasticsearch_client
  class_name: ElasticsearchClient
  api_endpoint_env: ELASTICSEARCH_ENDPOINT
  api_key_env: ELASTICSEARCH_API_KEY
  index_name: my-index
```

### Authentication

Set environment variables:
```bash
export ELASTICSEARCH_ENDPOINT=https://your-cluster.elasticsearch.com
export ELASTICSEARCH_API_KEY=your_api_key_here
```

## Usage

```python
import nlweb_core

# Initialize
nlweb_core.init(config_path="./config.yaml")

# Search
from nlweb_core import retriever

results = await retriever.search(
    query="example query",
    site="example.com",
    num_results=10
)
```

## Features

- Vector similarity search with Elasticsearch
- KNN search with filtering
- Configurable index names
- API key authentication
- Compatible with NLWeb Protocol v0.5

## Creating Your Own Provider Package

Use this package as a template:

1. **Create package structure**:
   ```
   nlweb-yourprovider/
   ├── pyproject.toml
   ├── README.md
   └── nlweb_yourprovider/
       ├── __init__.py
       └── your_client.py
   ```

2. **Implement VectorDBClientInterface**:
   ```python
   from nlweb_core.retriever import VectorDBClientInterface

   class YourClient(VectorDBClientInterface):
       async def search(self, query, site, num_results, **kwargs):
           # Your implementation
           pass
   ```

3. **Declare dependencies** in `pyproject.toml`:
   ```toml
   dependencies = [
       "nlweb-core>=0.5.0",
       "your-provider-sdk>=1.0.0",
   ]
   ```

4. **Publish to PyPI**:
   ```bash
   python -m build
   twine upload dist/*
   ```

## License

MIT License - Copyright (c) 2025 Microsoft Corporation
