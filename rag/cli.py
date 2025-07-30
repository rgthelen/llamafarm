#!/usr/bin/env python3
"""Simple CLI for the RAG system."""

import argparse
import logging
import json
import sys
import time
from pathlib import Path
from typing import Dict, Any
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

from core.base import Pipeline
from core.enhanced_pipeline import EnhancedPipeline
from parsers.csv_parser import CSVParser, CustomerSupportCSVParser
from embedders.ollama_embedder import OllamaEmbedder
from stores.chroma_store import ChromaStore
from utils.progress import LlamaProgressTracker, create_enhanced_progress_bar


def setup_logging(level: str = "INFO"):
    """Setup logging configuration."""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def load_config(config_path: str) -> Dict[str, Any]:
    """Load configuration from JSON file."""
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Config file not found: {config_path}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON in config file: {e}")
        sys.exit(1)


def create_sample_config():
    """Create a sample configuration file."""
    config = {
        "parser": {
            "type": "CustomerSupportCSVParser",
            "config": {
                "content_fields": ["subject", "body", "answer"],
                "metadata_fields": ["type", "queue", "priority", "language"],
                "combine_content": True,
                "content_separator": "\n\n---\n\n"
            }
        },
        "embedder": {
            "type": "OllamaEmbedder",
            "config": {
                "model": "nomic-embed-text",
                "base_url": "http://localhost:11434",
                "batch_size": 16,
                "timeout": 60
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
    
    config_path = Path("rag_config.json")
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"Sample configuration created: {config_path}")
    print("Edit this file to customize your RAG setup.")


def create_pipeline_from_config(config: Dict[str, Any], enhanced: bool = False) -> Pipeline:
    """Create pipeline from configuration."""
    # Create parser
    parser_config = config.get("parser", {})
    parser_type = parser_config.get("type", "CustomerSupportCSVParser")
    
    if parser_type == "CustomerSupportCSVParser":
        parser = CustomerSupportCSVParser(config=parser_config.get("config", {}))
    elif parser_type == "CSVParser":
        parser = CSVParser(config=parser_config.get("config", {}))
    else:
        raise ValueError(f"Unknown parser type: {parser_type}")
    
    # Create embedder
    embedder_config = config.get("embedder", {})
    embedder_type = embedder_config.get("type", "OllamaEmbedder")
    
    if embedder_type == "OllamaEmbedder":
        embedder = OllamaEmbedder(config=embedder_config.get("config", {}))
    else:
        raise ValueError(f"Unknown embedder type: {embedder_type}")
    
    # Create vector store
    store_config = config.get("vector_store", {})
    store_type = store_config.get("type", "ChromaStore")
    
    if store_type == "ChromaStore":
        store = ChromaStore(config=store_config.get("config", {}))
    else:
        raise ValueError(f"Unknown vector store type: {store_type}")
    
    # Create pipeline
    if enhanced:
        pipeline = EnhancedPipeline("🦙 Enhanced RAG Pipeline")
    else:
        pipeline = Pipeline("RAG Pipeline")
    
    pipeline.add_component(parser)
    pipeline.add_component(embedder)
    pipeline.add_component(store)
    
    return pipeline


def ingest_command(args):
    """Handle the ingest command."""
    setup_logging(args.log_level)
    tracker = LlamaProgressTracker()
    
    # Load configuration
    try:
        config = load_config(args.config)
    except Exception as e:
        tracker.print_error(f"Failed to load configuration: {e}")
        sys.exit(1)
    
    # Create enhanced pipeline
    try:
        pipeline = create_pipeline_from_config(config, enhanced=True)
    except Exception as e:
        tracker.print_error(f"Failed to create pipeline: {e}")
        sys.exit(1)
    
    # Run ingestion with enhanced progress tracking
    try:
        if hasattr(pipeline, 'run_with_progress'):
            result = pipeline.run_with_progress(source=args.source)
        else:
            # Fallback to regular pipeline
            tracker.print_info(f"📂 Processing documents from: {args.source}")
            result = pipeline.run(source=args.source)
            tracker.print_success("Processing completed!")
        
        # Show final summary
        print(f"\n📊 Final Results:")
        tracker.print_success(f"Documents processed: {len(result.documents)}")
        
        if result.errors:
            tracker.print_warning(f"Errors encountered: {len(result.errors)}")
            if args.log_level.upper() in ["DEBUG", "INFO"]:
                print("\n🔍 Error Details:")
                for i, error in enumerate(result.errors[:5], 1):
                    print(f"   {i}. {error}")
                if len(result.errors) > 5:
                    print(f"   ... and {len(result.errors) - 5} more errors")
        else:
            tracker.print_success("Zero errors - perfect execution! 🎯")
                
    except KeyboardInterrupt:
        tracker.print_warning("\n⏸️  Processing interrupted by user. No prob-llama!")
        sys.exit(0)
    except Exception as e:
        tracker.print_error(f"Ingestion failed: {e}")
        sys.exit(1)


def search_command(args):
    """Handle the search command."""
    setup_logging(args.log_level)
    tracker = LlamaProgressTracker()
    
    # Load configuration
    config = load_config(args.config)
    
    # Create embedder for query
    embedder_config = config.get("embedder", {})
    embedder_type = embedder_config.get("type", "OllamaEmbedder")
    
    if embedder_type == "OllamaEmbedder":
        embedder = OllamaEmbedder(config=embedder_config.get("config", {}))
    else:
        print(f"Unknown embedder type: {embedder_type}")
        sys.exit(1)
    
    # Create vector store
    store_config = config.get("vector_store", {})
    store_type = store_config.get("type", "ChromaStore")
    
    if store_type == "ChromaStore":
        store = ChromaStore(config=store_config.get("config", {}))
    else:
        print(f"Unknown vector store type: {store_type}")
        sys.exit(1)
    
    # Perform search with llama flair
    tracker.print_header(f"🔍 Searching the Llama-sphere! 🔍")
    tracker.print_info(f"🎯 Query: '{args.query}'")
    tracker.print_info(f"🦙 {tracker.get_random_pun()}")
    
    try:
        # Embed the query
        print("🧠 Converting your query into llama-friendly embeddings...")
        query_embedding = embedder.embed([args.query])[0]
        tracker.print_success("Query embedded successfully!")
        
        # Search using the query embedding
        print("🔍 Searching through the knowledge pasture...")
        results = store.search(query_embedding=query_embedding, top_k=args.top_k)
        
        if results:
            tracker.print_success(f"Found {len(results)} llama-nificent matches!")
            print(f"\n📋 Search Results:")
            
            for i, doc in enumerate(results, 1):
                print(f"\n{Fore.CYAN}{'='*50}")
                print(f"🏆 Result #{i} - Document: {doc.id}")
                print(f"{'='*50}{Style.RESET_ALL}")
                
                print(f"📝 Content Preview:")
                print(f"   {doc.content[:300]}{'...' if len(doc.content) > 300 else ''}")
                
                if "similarity_score" in doc.metadata:
                    score = doc.metadata['similarity_score']
                    if score > -100:
                        print(f"🎯 Similarity: {score:.3f} (Excellent match!)")
                    elif score > -300:
                        print(f"🎯 Similarity: {score:.3f} (Good match)")
                    else:
                        print(f"🎯 Similarity: {score:.3f} (Partial match)")
                
                if "priority" in doc.metadata:
                    priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(doc.metadata['priority'], "⚪")
                    print(f"{priority_emoji} Priority: {doc.metadata['priority']}")
                
                if "tags" in doc.metadata:
                    print(f"🏷️  Tags: {doc.metadata['tags']}")
        else:
            tracker.print_warning("No results found. The llamas are still grazing in other pastures! 🌾")
            print("\n💡 Tips for better results:")
            print("   • Try different keywords")
            print("   • Use more specific terms")
            print("   • Check if your data has been ingested")
            
    except Exception as e:
        tracker.print_error(f"Search failed: {e}")
        sys.exit(1)


def info_command(args):
    """Handle the info command."""
    setup_logging(args.log_level)
    
    # Load configuration
    config = load_config(args.config)
    
    # Create vector store
    store_config = config.get("vector_store", {})
    store_type = store_config.get("type", "ChromaStore")
    
    if store_type == "ChromaStore":
        store = ChromaStore(config=store_config.get("config", {}))
    else:
        print(f"Unknown vector store type: {store_type}")
        sys.exit(1)
    
    # Get info
    try:
        info = store.get_collection_info()
        print("Vector Store Information:")
        for key, value in info.items():
            print(f"  {key}: {value}")
    except Exception as e:
        print(f"Failed to get info: {e}")
        sys.exit(1)


def test_command(args):
    """Handle the test command."""
    setup_logging(args.log_level)
    
    print("Testing RAG system components...")
    
    # Test Ollama connection
    print("\n1. Testing Ollama connection...")
    try:
        embedder = OllamaEmbedder()
        embedder.validate_config()
        print("   ✓ Ollama is available")
        
        # Test embedding
        test_texts = ["Hello world", "This is a test"]
        embeddings = embedder.embed(test_texts)
        if embeddings and all(emb for emb in embeddings):
            print(f"   ✓ Embeddings generated (dimension: {len(embeddings[0])})")
        else:
            print("   ✗ Failed to generate embeddings")
    except Exception as e:
        print(f"   ✗ Ollama test failed: {e}")
    
    # Test ChromaDB
    print("\n2. Testing ChromaDB...")
    try:
        store = ChromaStore(config={"collection_name": "test_collection"})
        store.validate_config()
        print("   ✓ ChromaDB is available")
        
        # Clean up test collection
        store.delete_collection()
        print("   ✓ Test collection cleaned up")
    except Exception as e:
        print(f"   ✗ ChromaDB test failed: {e}")
    
    # Test CSV parsing
    print("\n3. Testing CSV parsing...")
    try:
        if args.test_file:
            parser = CustomerSupportCSVParser()
            result = parser.parse(args.test_file)
            print(f"   ✓ Parsed {len(result.documents)} documents")
            if result.errors:
                print(f"   ⚠ {len(result.errors)} parsing errors")
        else:
            print("   ⚠ No test file provided (use --test-file)")
    except Exception as e:
        print(f"   ✗ CSV parsing test failed: {e}")
    
    print("\nTest completed!")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Simple RAG System CLI")
    parser.add_argument("--config", "-c", default="rag_config.json",
                       help="Configuration file path")
    parser.add_argument("--log-level", default="INFO",
                       choices=["DEBUG", "INFO", "WARNING", "ERROR"],
                       help="Logging level")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Config command
    config_parser = subparsers.add_parser("init", help="Create sample configuration")
    
    # Ingest command
    ingest_parser = subparsers.add_parser("ingest", help="Ingest documents")
    ingest_parser.add_argument("source", help="Source file or directory")
    
    # Search command
    search_parser = subparsers.add_parser("search", help="Search documents")
    search_parser.add_argument("query", help="Search query")
    search_parser.add_argument("--top-k", type=int, default=5,
                              help="Number of results to return")
    
    # Info command
    info_parser = subparsers.add_parser("info", help="Show vector store info")
    
    # Test command
    test_parser = subparsers.add_parser("test", help="Test system components")
    test_parser.add_argument("--test-file", help="CSV file to test parsing")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    if args.command == "init":
        create_sample_config()
    elif args.command == "ingest":
        ingest_command(args)
    elif args.command == "search":
        search_command(args)
    elif args.command == "info":
        info_command(args)
    elif args.command == "test":
        test_command(args)


if __name__ == "__main__":
    main()