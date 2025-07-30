"""ChromaDB vector store implementation."""

from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings

from core.base import VectorStore, Document


class ChromaStore(VectorStore):
    """ChromaDB vector store implementation."""
    
    def __init__(self, name: str = "ChromaStore", config: Dict[str, Any] = None):
        super().__init__(name, config)
        self.collection_name = config.get("collection_name", "documents")
        self.persist_directory = config.get("persist_directory", "./chroma_db")
        self.host = config.get("host")
        self.port = config.get("port")
        
        # Initialize ChromaDB client
        if self.host and self.port:
            # HTTP client
            self.client = chromadb.HttpClient(host=self.host, port=self.port)
        else:
            # Persistent client
            self.client = chromadb.PersistentClient(path=self.persist_directory)
        
        self.collection = None
        self._setup_collection()
    
    def validate_config(self) -> bool:
        """Validate configuration."""
        try:
            # Test connection
            self.client.heartbeat()
            return True
        except Exception as e:
            raise ValueError(f"Failed to connect to ChromaDB: {e}")
    
    def _setup_collection(self):
        """Setup or get collection."""
        try:
            self.collection = self.client.get_collection(name=self.collection_name)
            self.logger.info(f"Using existing collection: {self.collection_name}")
        except Exception:
            # Collection doesn't exist, create it
            self.collection = self.client.create_collection(name=self.collection_name)
            self.logger.info(f"Created new collection: {self.collection_name}")
    
    def add_documents(self, documents: List[Document]) -> bool:
        """Add documents to ChromaDB."""
        try:
            # Prepare data for ChromaDB
            ids = []
            embeddings = []
            metadatas = []
            documents_content = []
            
            for doc in documents:
                if not doc.embeddings:
                    self.logger.warning(f"Document {doc.id} has no embeddings, skipping")
                    continue
                
                ids.append(doc.id)
                embeddings.append(doc.embeddings)
                documents_content.append(doc.content)
                
                # ChromaDB metadata must be JSON serializable
                metadata = self._serialize_metadata(doc.metadata)
                metadatas.append(metadata)
            
            if not ids:
                self.logger.warning("No documents with embeddings to add")
                return False
            
            # Add to collection
            self.collection.add(
                ids=ids,
                embeddings=embeddings,
                documents=documents_content,
                metadatas=metadatas
            )
            
            self.logger.info(f"Added {len(ids)} documents to collection")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to add documents: {e}")
            return False
    
    def search(self, query: str = None, query_embedding: List[float] = None, 
               top_k: int = 10, where: Dict[str, Any] = None) -> List[Document]:
        """Search for similar documents."""
        try:
            if query_embedding is None and query is None:
                raise ValueError("Either query or query_embedding must be provided")
            
            # Prepare search parameters
            search_params = {
                "n_results": top_k
            }
            
            if query_embedding:
                search_params["query_embeddings"] = [query_embedding]
            else:
                search_params["query_texts"] = [query]
            
            if where:
                search_params["where"] = where
            
            # Search
            results = self.collection.query(**search_params)
            
            # Convert results to Document objects
            documents = []
            if results["ids"] and results["ids"][0]:  # Check if we got any results
                for i, doc_id in enumerate(results["ids"][0]):
                    doc = Document(
                        id=doc_id,
                        content=results["documents"][0][i],
                        metadata=results["metadatas"][0][i] or {},
                        embeddings=results["embeddings"][0][i] if results.get("embeddings") else None
                    )
                    
                    # Add distance/similarity score if available
                    if results.get("distances") and len(results["distances"][0]) > i:
                        doc.metadata["similarity_score"] = 1 - results["distances"][0][i]  # Convert distance to similarity
                    
                    documents.append(doc)
            
            return documents
            
        except Exception as e:
            self.logger.error(f"Search failed: {e}")
            return []
    
    def delete_collection(self) -> bool:
        """Delete the collection."""
        try:
            self.client.delete_collection(name=self.collection_name)
            self.logger.info(f"Deleted collection: {self.collection_name}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to delete collection: {e}")
            return False
    
    def get_collection_info(self) -> Dict[str, Any]:
        """Get collection information."""
        try:
            count = self.collection.count()
            return {
                "name": self.collection_name,
                "count": count,
                "client_type": type(self.client).__name__
            }
        except Exception as e:
            self.logger.error(f"Failed to get collection info: {e}")
            return {}
    
    def _serialize_metadata(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Serialize metadata for ChromaDB storage."""
        serialized = {}
        for key, value in metadata.items():
            if isinstance(value, (str, int, float, bool)):
                serialized[key] = value
            elif isinstance(value, list):
                # Convert lists to comma-separated strings
                serialized[key] = ",".join(map(str, value))
            else:
                # Convert other types to string
                serialized[key] = str(value)
        
        return serialized