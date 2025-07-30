# Simple Extensible RAG System

A lightweight, extensible RAG (Retrieval-Augmented Generation) system designed for easy contribution and customization. Built with a modular architecture that makes it simple to add new data sources, embedding models, and vector databases.

## Features

- **Extensible Architecture**: Easy to add new parsers, embedders, and vector stores
- **CSV Support**: Built-in support for customer support tickets and other tabular data
- **Ollama Integration**: Local embeddings using Ollama
- **ChromaDB Support**: Persistent vector storage
- **Simple CLI**: Easy setup and management
- **Configuration-Driven**: JSON configuration files
- **Testing Framework**: Comprehensive tests included

## Quick Start

### Prerequisites

1. **Python 3.8+**
2. **Ollama** (for embeddings)

### macOS Installation

1. **Install Ollama**:
   ```bash
   # Method 1: Official installer
   curl -fsSL https://ollama.com/install.sh | sh
   
   # Method 2: Homebrew (alternative)
   brew install ollama
   ```

2. **Start Ollama and pull the embedding model**:
   ```bash
   # Start Ollama service
   ollama serve
   
   # In a new terminal, pull the embedding model
   ollama pull nomic-embed-text
   ```

3. **Install Python dependencies**:
   ```bash
   # Option 1: Direct installation
   pip install -r requirements.txt
   
   # Option 2: Use Python 3 explicitly
   python3 -m pip install -r requirements.txt
   
   # Option 3: Virtual environment (recommended)
   python3 -m venv rag_env
   source rag_env/bin/activate
   pip install -r requirements.txt
   ```

### Basic Usage

1. **Initialize configuration:**
   ```bash
   python cli.py init
   ```

2. **Test the system:**
   ```bash
   python cli.py test --test-file filtered-english-incident-tickets.csv
   ```

3. **Ingest your CSV data:**
   ```bash
   python cli.py ingest filtered-english-incident-tickets.csv
   ```

4. **Search the data:**
   ```bash
   python cli.py search "data breach security issue"
   python cli.py search "login problems"
   python cli.py search "password reset"
   ```

5. **Get collection info:**
   ```bash
   python cli.py info
   ```

### Alternative: Run the Example Script

```bash
python example.py
```

## Architecture

The system is built around four core components:

### 1. Parsers
Convert various data formats into the universal `Document` format.

- `CSVParser`: Generic CSV parser with configurable fields
- `CustomerSupportCSVParser`: Specialized for support ticket data

### 2. Embedders
Generate vector embeddings from text content.

- `OllamaEmbedder`: Uses local Ollama models

### 3. Vector Stores
Store and search document embeddings.

- `ChromaStore`: ChromaDB integration with persistence

### 4. Pipeline
Chains components together for end-to-end processing.

## Configuration

Configuration is JSON-based and includes three main sections:

```json
{
  "parser": {
    "type": "CustomerSupportCSVParser",
    "config": {
      "content_fields": ["subject", "body", "answer"],
      "metadata_fields": ["type", "priority", "language"]
    }
  },
  "embedder": {
    "type": "OllamaEmbedder",
    "config": {
      "model": "nomic-embed-text",
      "batch_size": 16
    }
  },
  "vector_store": {
    "type": "ChromaStore",
    "config": {
      "collection_name": "support_tickets",
      "persist_directory": "./chroma_db"
    }
  }
}
```

### Sample Configurations

- `config_examples/basic_config.json`: Basic local setup
- `config_examples/production_config.json`: Production deployment
- `config_examples/custom_csv_config.json`: Custom CSV format

## Adding New Components

### Adding a New Parser

1. **Create a new parser class:**

```python
from core.base import Parser, Document, ProcessingResult

class MyCustomParser(Parser):
    def parse(self, source: str) -> ProcessingResult:
        documents = []
        # Your parsing logic here
        return ProcessingResult(documents=documents)
```

2. **Register in CLI:**

Add to `create_pipeline_from_config()` in `cli.py`:

```python
elif parser_type == "MyCustomParser":
    parser = MyCustomParser(config=parser_config.get("config", {}))
```

### Adding a New Embedder

1. **Create embedder class:**

```python
from core.base import Embedder

class MyEmbedder(Embedder):
    def embed(self, texts: List[str]) -> List[List[float]]:
        # Your embedding logic here
        return embeddings
```

2. **Register in CLI and update configuration**

### Adding a New Vector Store

1. **Create store class:**

```python  
from core.base import VectorStore, Document

class MyVectorStore(VectorStore):
    def add_documents(self, documents: List[Document]) -> bool:
        # Storage logic
        pass
    
    def search(self, query: str, top_k: int = 10) -> List[Document]:
        # Search logic
        pass
```

2. **Register in CLI**

## Examples

### Programmatic Usage

```python
from core.base import Pipeline
from parsers.csv_parser import CustomerSupportCSVParser
from embedders.ollama_embedder import OllamaEmbedder
from stores.chroma_store import ChromaStore

# Create pipeline
pipeline = Pipeline("My RAG Pipeline")
pipeline.add_component(CustomerSupportCSVParser())
pipeline.add_component(OllamaEmbedder())
pipeline.add_component(ChromaStore())

# Process data
result = pipeline.run(source="my_data.csv")
```

### Custom CSV Format

For custom CSV formats, configure field mappings:

```json
{
  "parser": {
    "type": "CSVParser",
    "config": {
      "content_fields": ["title", "description", "solution"],
      "metadata_fields": ["category", "severity", "date"],
      "id_field": "ticket_number",
      "combine_content": true,
      "content_separator": "\\n\\n"
    }
  }
}
```

## Testing

Run the comprehensive test suite:

```bash
python test_system.py
```

This tests:
- CSV parsing functionality
- Ollama integration (if available)
- ChromaDB storage
- End-to-end pipeline

## File Structure

```
rag/
├── core/
│   ├── __init__.py
│   └── base.py              # Base classes
├── parsers/
│   ├── __init__.py
│   └── csv_parser.py        # CSV parsers
├── embedders/
│   ├── __init__.py
│   └── ollama_embedder.py   # Ollama integration
├── stores/
│   ├── __init__.py
│   └── chroma_store.py      # ChromaDB integration
├── config_examples/         # Sample configurations
├── cli.py                   # Command-line interface
├── example.py              # Usage example
├── test_system.py          # Test suite
├── requirements.txt        # Dependencies
└── README.md              # This file
```

## Contributing

This system is designed for easy extension. To contribute:

1. **Add new components** following the base class patterns
2. **Update CLI registration** for new component types
3. **Add tests** for new functionality
4. **Update documentation** with usage examples

### Component Guidelines

- Inherit from appropriate base classes (`Parser`, `Embedder`, `VectorStore`)
- Implement required abstract methods
- Include configuration validation
- Add error handling and logging
- Follow the established patterns

## Troubleshooting

### macOS-Specific Issues

#### Ollama Installation Problems
```bash
# If the curl install fails, try Homebrew
brew install ollama

# Start Ollama
ollama serve
```

#### Python/pip Issues
```bash
# Use Python 3 explicitly if needed
python3 cli.py init
python3 cli.py test

# Create virtual environment if you get permission errors
python3 -m venv rag_env
source rag_env/bin/activate
pip install -r requirements.txt
```

#### Check if Everything is Working
```bash
# Test Ollama connection
curl http://localhost:11434/api/tags

# Run comprehensive system tests
python test_system.py
```

### General Issues

#### Ollama Problems
- Ensure Ollama is running: `ollama serve`
- Check model availability: `ollama list`
- Pull required model: `ollama pull nomic-embed-text`

#### ChromaDB Issues
- Check permissions on persist directory
- Ensure disk space available
- Try deleting collection and recreating

#### Performance Tips
- Adjust batch sizes based on your hardware
- Use appropriate embedding models for your use case
- Consider chunking large CSV files

## License

This project is designed as a simple, extensible foundation for RAG systems. Feel free to use, modify, and extend as needed.