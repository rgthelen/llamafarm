"""Ollama-based embedding generator."""

import requests
import json
from typing import List, Dict, Any

from core.base import Embedder


class OllamaEmbedder(Embedder):
    """Embedder using Ollama API for local embeddings."""

    def __init__(self, name: str = "OllamaEmbedder", config: Dict[str, Any] = None):
        super().__init__(name, config)
        config = config or {}
        self.model = config.get("model", "nomic-embed-text")
        self.base_url = config.get("base_url", "http://localhost:11434")
        self.batch_size = config.get("batch_size", 32)
        self.timeout = config.get("timeout", 60)

    def validate_config(self) -> bool:
        """Validate configuration and check Ollama availability."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code != 200:
                raise ValueError(f"Ollama not available at {self.base_url}")

            # Check if response has proper JSON structure
            response_data = response.json()
            if response_data is None:
                raise ValueError("Invalid response from Ollama API")

            # Check if model is available
            models = response_data.get("models", [])
            model_names = [m.get("name", "") for m in models if isinstance(m, dict)]
            # Check for exact match or partial match (e.g., "nomic-embed-text" matches "nomic-embed-text:latest")
            model_available = any(
                self.model == name or name.startswith(f"{self.model}:")
                for name in model_names
            )
            if not model_available:
                self.logger.warning(
                    f"Model {self.model} not found. Available models: {model_names}"
                )
                self.logger.info(f"Will attempt to pull {self.model} when first used")

            return True
        except Exception as e:
            raise ValueError(f"Failed to connect to Ollama: {e}")

    def embed(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings using Ollama."""
        embeddings = []

        # Process in batches
        for i in range(0, len(texts), self.batch_size):
            batch = texts[i : i + self.batch_size]
            batch_embeddings = self._embed_batch(batch)
            embeddings.extend(batch_embeddings)

        return embeddings

    def _embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Embed a batch of texts."""
        embeddings = []

        for text in texts:
            try:
                response = requests.post(
                    f"{self.base_url}/api/embeddings",
                    json={"model": self.model, "prompt": text},
                    timeout=self.timeout,
                )

                if response.status_code == 200:
                    result = response.json()
                    embedding = result.get("embedding")
                    if embedding:
                        embeddings.append(embedding)
                    else:
                        self.logger.error(
                            f"No embedding returned for text: {text[:50]}..."
                        )
                        embeddings.append([])
                else:
                    self.logger.error(
                        f"Ollama API error {response.status_code}: {response.text}"
                    )
                    embeddings.append([])

            except Exception as e:
                self.logger.error(f"Failed to get embedding for text: {e}")
                embeddings.append([])

        return embeddings

    def pull_model(self) -> bool:
        """Pull the embedding model if not available."""
        try:
            self.logger.info(f"Pulling model {self.model}...")
            response = requests.post(
                f"{self.base_url}/api/pull",
                json={"name": self.model},
                timeout=300,  # 5 minutes for model download
            )

            if response.status_code == 200:
                self.logger.info(f"Model {self.model} pulled successfully")
                return True
            else:
                self.logger.error(f"Failed to pull model: {response.text}")
                return False

        except Exception as e:
            self.logger.error(f"Error pulling model: {e}")
            return False
