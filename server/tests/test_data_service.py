"""
Tests for DataService.

This module contains comprehensive tests for the DataService class,
including unit tests for all public methods and edge cases.
"""

from unittest.mock import AsyncMock, Mock, mock_open, patch

import pytest
from fastapi import UploadFile

from config.datamodel import (
    Dataset,
    LlamaFarmConfig,
    Prompt,
    Provider,
    Runtime,
    Version,
)
from services.data_service import (
    DataService,
    FileExistsInAnotherDatasetError,
    MetadataFileContent,
)

# Configure pytest for async tests
pytest_plugins = ("pytest_asyncio",)


class TestDataService:
    """Test cases for DataService class."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.test_namespace = "test_namespace"
        self.test_project = "test_project"
        self.test_data_dir = "/test/data/dir"

        # Mock file data
        self.test_file_content = b"test file content"
        self.test_file_hash = (
            "a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3"
        )

        # Mock metadata
        self.mock_metadata = MetadataFileContent(
            original_file_name="test.pdf",
            resolved_file_name="test_1640995200.0.pdf",
            size=len(self.test_file_content),
            mime_type="application/pdf",
            hash=self.test_file_hash,
            timestamp=1640995200.0,
        )

        # Mock project with datasets
        self.mock_project = Mock()
        self.mock_project.config = LlamaFarmConfig(
            version=Version.v1,
            name="test_project",
            namespace=self.test_namespace,
            prompts=[
                Prompt(
                    role="system",
                    content="You are a helpful assistant.",
                )
            ],
            rag={
                "strategies": [
                    {
                        "name": "default",
                        "description": "Default strategy configuration",
                        "components": {
                            "parser": {"type": "CSVParser", "config": {}},
                            "extractors": [],
                            "embedder": {
                                "type": "OllamaEmbedder",
                                "config": {"model": "nomic-embed-text"},
                            },
                            "vector_store": {"type": "ChromaStore", "config": {}},
                            "retrieval_strategy": {
                                "type": "BasicSimilarityStrategy",
                                "config": {},
                            },
                        },
                    }
                ]
            },
            datasets=[
                Dataset(
                    name="dataset1", rag_strategy="auto", files=[self.test_file_hash]
                ),
                Dataset(name="dataset2", rag_strategy="auto", files=["other_hash"]),
            ],
            runtime=Runtime(
                provider=Provider.openai,
                model="llama3.1:8b",
                api_key="ollama",
                base_url="http://localhost:11434/v1",
                model_api_parameters={
                    "temperature": 0.5,
                },
            ),
        )

    @patch("services.data_service.os.makedirs")
    @patch("services.data_service.ProjectService.get_project_dir")
    def test_get_data_dir_creates_directories(
        self, mock_get_project_dir, mock_makedirs
    ):
        """Test that get_data_dir creates all necessary directories."""
        mock_get_project_dir.return_value = "/project/dir"

        result = DataService.get_data_dir(self.test_namespace, self.test_project)

        expected_data_dir = "/project/dir/lf_data"
        assert result == expected_data_dir
        mock_get_project_dir.assert_called_once_with(
            self.test_namespace, self.test_project
        )

        # Verify all directories are created
        expected_calls = [
            (("/project/dir/lf_data",), {"exist_ok": True}),
            (("/project/dir/lf_data/meta",), {"exist_ok": True}),
            (("/project/dir/lf_data/raw",), {"exist_ok": True}),
            (("/project/dir/lf_data/index/by_name",), {"exist_ok": True}),
        ]
        assert mock_makedirs.call_count == 4
        for call in expected_calls:
            assert call in [
                (args, kwargs) for args, kwargs in mock_makedirs.call_args_list
            ]

    def test_hash_data(self):
        """Test data hashing functionality."""
        test_data = b"hello world"
        expected_hash = (
            "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9"
        )

        result = DataService.hash_data(test_data)

        assert result == expected_hash

    @patch("services.data_service.datetime")
    def test_append_collision_timestamp(self, mock_datetime):
        """Test timestamp appending for collision resolution."""
        mock_datetime.now.return_value.timestamp.return_value = 1640995200.0

        # Test with extension
        result = DataService.append_collision_timestamp("test.pdf")
        assert result == "test_1640995200.0.pdf"

        # Test without extension
        result = DataService.append_collision_timestamp("test")
        assert result == "test_1640995200.0"

    @patch.object(DataService, "get_data_dir")
    @patch.object(DataService, "hash_data")
    @patch.object(DataService, "append_collision_timestamp")
    @patch("builtins.open", new_callable=mock_open)
    @patch("os.symlink")
    @patch("services.data_service.logger")
    @pytest.mark.asyncio
    async def test_add_data_file_success(
        self,
        mock_logger,
        mock_symlink,
        mock_file_open,
        mock_append_timestamp,
        mock_hash_data,
        mock_get_data_dir,
    ):
        """Test successfully adding a data file."""
        # Setup mocks
        mock_get_data_dir.return_value = self.test_data_dir
        mock_hash_data.return_value = self.test_file_hash
        mock_append_timestamp.return_value = "test_1640995200.0.pdf"

        # Create mock upload file
        mock_upload_file = Mock(spec=UploadFile)
        mock_upload_file.filename = "test.pdf"
        mock_upload_file.content_type = "application/pdf"
        mock_upload_file.read = AsyncMock(return_value=self.test_file_content)

        # Execute
        result = await DataService.add_data_file(
            self.test_namespace, self.test_project, mock_upload_file
        )

        # Verify result
        assert isinstance(result, MetadataFileContent)
        assert result.original_file_name == "test.pdf"
        assert result.resolved_file_name == "test_1640995200.0.pdf"
        assert result.size == len(self.test_file_content)
        assert result.mime_type == "application/pdf"
        assert result.hash == self.test_file_hash

        # Verify file operations
        mock_upload_file.read.assert_called_once()
        mock_hash_data.assert_called_once_with(self.test_file_content)
        mock_append_timestamp.assert_called_once_with("test.pdf")

        # Verify file writes
        assert mock_file_open.call_count == 2  # metadata and raw file
        mock_symlink.assert_called_once()
        mock_logger.info.assert_called_once()

    @patch.object(DataService, "get_data_dir")
    @patch("builtins.open", new_callable=mock_open, read_data=b"test file content")
    def test_read_data_file_success(self, mock_file_open, mock_get_data_dir):
        """Test successfully reading a data file."""
        mock_get_data_dir.return_value = self.test_data_dir

        result = DataService.read_data_file(
            self.test_namespace, self.test_project, self.test_file_hash
        )

        assert result == b"test file content"
        mock_get_data_dir.assert_called_once_with(
            self.test_namespace, self.test_project
        )
        mock_file_open.assert_called_once_with(
            f"{self.test_data_dir}/raw/{self.test_file_hash}", "rb"
        )

    @patch.object(DataService, "get_data_dir")
    @patch("builtins.open", new_callable=mock_open)
    def test_read_data_file_not_found(self, mock_file_open, mock_get_data_dir):
        """Test reading a non-existent data file."""
        mock_get_data_dir.return_value = self.test_data_dir
        mock_file_open.side_effect = FileNotFoundError("File not found")

        with pytest.raises(FileNotFoundError):
            DataService.read_data_file(
                self.test_namespace, self.test_project, "nonexistent_hash"
            )

    @patch.object(DataService, "get_data_dir")
    @patch("builtins.open", new_callable=mock_open)
    def test_get_data_file_metadata_by_hash_success(
        self, mock_file_open, mock_get_data_dir
    ):
        """Test successfully getting metadata by hash."""
        mock_get_data_dir.return_value = self.test_data_dir
        mock_file_open.return_value.read.return_value = (
            self.mock_metadata.model_dump_json()
        )

        result = DataService.get_data_file_metadata_by_hash(
            self.test_namespace, self.test_project, self.test_file_hash
        )

        assert isinstance(result, MetadataFileContent)
        assert result.original_file_name == self.mock_metadata.original_file_name
        assert result.hash == self.mock_metadata.hash

        mock_get_data_dir.assert_called_once_with(
            self.test_namespace, self.test_project
        )
        mock_file_open.assert_called_once_with(
            f"{self.test_data_dir}/meta/{self.test_file_hash}.json"
        )

    @patch.object(DataService, "get_data_dir")
    @patch("builtins.open", new_callable=mock_open)
    def test_get_data_file_metadata_by_hash_not_found(
        self, mock_file_open, mock_get_data_dir
    ):
        """Test getting metadata for non-existent file."""
        mock_get_data_dir.return_value = self.test_data_dir
        mock_file_open.side_effect = FileNotFoundError("Metadata not found")

        with pytest.raises(FileNotFoundError):
            DataService.get_data_file_metadata_by_hash(
                self.test_namespace, self.test_project, "nonexistent_hash"
            )

    @patch("services.data_service.os.remove")
    @patch("services.data_service.logger")
    @patch.object(DataService, "get_data_dir")
    @patch("services.data_service.ProjectService.get_project")
    def test_delete_data_file_success(
        self, mock_get_project, mock_get_data_dir, mock_logger, mock_remove
    ):
        """Test successfully deleting a data file."""
        mock_get_data_dir.return_value = self.test_data_dir

        # Mock project with datasets where no other dataset exists
        mock_project = Mock()
        mock_project.config = LlamaFarmConfig(
            version=Version.v1,
            name="test_project",
            namespace=self.test_namespace,
            prompts=[
                Prompt(
                    role="system",
                    content="You are a helpful assistant.",
                )
            ],
            rag={
                "strategies": [
                    {
                        "name": "default",
                        "description": "Default strategy configuration",
                        "components": {
                            "parser": {"type": "CSVParser", "config": {}},
                            "extractors": [],
                            "embedder": {
                                "type": "OllamaEmbedder",
                                "config": {"model": "nomic-embed-text"},
                            },
                            "vector_store": {"type": "ChromaStore", "config": {}},
                            "retrieval_strategy": {
                                "type": "BasicSimilarityStrategy",
                                "config": {},
                            },
                        },
                    }
                ]
            },
            datasets=[
                Dataset(
                    name="target_dataset",
                    rag_strategy="auto",
                    files=[self.test_file_hash],
                )
            ],
            runtime=Runtime(
                provider=Provider.openai,
                model="llama3.1:8b",
                api_key="ollama",
                base_url="http://localhost:11434/v1",
                model_api_parameters={
                    "temperature": 0.5,
                },
            ),
        )
        mock_get_project.return_value = mock_project

        # Execute
        DataService.delete_data_file(
            self.test_namespace, self.test_project, "target_dataset", self.mock_metadata
        )

        # Verify file removals
        expected_calls = [
            f"{self.test_data_dir}/meta/{self.test_file_hash}.json",
            f"{self.test_data_dir}/raw/{self.test_file_hash}",
            f"{self.test_data_dir}/index/by_name/{self.mock_metadata.resolved_file_name}",
        ]
        assert mock_remove.call_count == 3
        for expected_path in expected_calls:
            mock_remove.assert_any_call(expected_path)

        mock_logger.info.assert_called_once()

    @patch.object(DataService, "get_data_dir")
    @patch("services.data_service.ProjectService.get_project")
    def test_delete_data_file_in_use_by_another_dataset(
        self, mock_get_project, mock_get_data_dir
    ):
        """Test deleting a file that's in use by another dataset."""
        mock_get_data_dir.return_value = self.test_data_dir

        # Mock project with datasets where another dataset exists
        # Note: Current logic just checks if ANY other dataset exists, not if file is in use
        mock_project = Mock()
        mock_project.config = LlamaFarmConfig(
            version=Version.v1,
            name="test_project",
            namespace=self.test_namespace,
            prompts=[
                Prompt(
                    role="system",
                    content="You are a helpful assistant.",
                )
            ],
            rag={
                "strategies": [
                    {
                        "name": "default",
                        "description": "Default strategy configuration",
                        "components": {
                            "parser": {"type": "CSVParser", "config": {}},
                            "extractors": [],
                            "embedder": {
                                "type": "OllamaEmbedder",
                                "config": {"model": "nomic-embed-text"},
                            },
                            "vector_store": {"type": "ChromaStore", "config": {}},
                            "retrieval_strategy": {
                                "type": "BasicSimilarityStrategy",
                                "config": {},
                            },
                        },
                    }
                ]
            },
            datasets=[
                Dataset(
                    name="target_dataset",
                    rag_strategy="auto",
                    files=[self.test_file_hash],
                ),
                Dataset(
                    name="other_dataset",
                    rag_strategy="auto",
                    files=["other_hash", self.test_file_hash],
                ),
            ],
            runtime=Runtime(
                provider=Provider.openai,
                model="llama3.1:8b",
                api_key="ollama",
                base_url="http://localhost:11434/v1",
                model_api_parameters={
                    "temperature": 0.5,
                },
            ),
        )
        mock_get_project.return_value = mock_project

        # Execute and verify exception
        with pytest.raises(FileExistsInAnotherDatasetError) as exc_info:
            DataService.delete_data_file(
                self.test_namespace,
                self.test_project,
                "target_dataset",
                self.mock_metadata,
            )

        assert "is in use by dataset 'other_dataset'" in str(exc_info.value)

    @patch.object(DataService, "get_data_dir")
    @patch("services.data_service.ProjectService.get_project")
    def test_delete_data_file_no_other_datasets(
        self, mock_get_project, mock_get_data_dir
    ):
        """Test deleting a file when no other datasets exist."""
        mock_get_data_dir.return_value = self.test_data_dir

        # Mock project with only the target dataset
        mock_project = Mock()
        mock_project.config = LlamaFarmConfig(
            version=Version.v1,
            name="test_project",
            namespace=self.test_namespace,
            prompts=[
                Prompt(
                    role="system",
                    content="You are a helpful assistant.",
                )
            ],
            rag={
                "strategies": [
                    {
                        "name": "default",
                        "description": "Default strategy configuration",
                        "components": {
                            "parser": {"type": "CSVParser", "config": {}},
                            "extractors": [],
                            "embedder": {
                                "type": "OllamaEmbedder",
                                "config": {"model": "nomic-embed-text"},
                            },
                            "vector_store": {"type": "ChromaStore", "config": {}},
                            "retrieval_strategy": {
                                "type": "BasicSimilarityStrategy",
                                "config": {},
                            },
                        },
                    }
                ]
            },
            datasets=[
                Dataset(
                    name="target_dataset",
                    rag_strategy="auto",
                    files=[self.test_file_hash],
                )
            ],
            runtime=Runtime(
                provider=Provider.openai,
                model="llama3.1:8b",
                api_key="ollama",
                base_url="http://localhost:11434/v1",
                model_api_parameters={
                    "temperature": 0.5,
                },
            ),
        )
        mock_get_project.return_value = mock_project

        with (
            patch("services.data_service.os.remove") as mock_remove,
            patch("services.data_service.logger") as mock_logger,
        ):
            # Should not raise an exception
            DataService.delete_data_file(
                self.test_namespace,
                self.test_project,
                "target_dataset",
                self.mock_metadata,
            )

            # Verify files were removed
            assert mock_remove.call_count == 3
            mock_logger.info.assert_called_once()


# Integration tests
class TestDataServiceIntegration:
    """Integration tests for DataService workflows."""

    @patch.object(DataService, "get_data_dir")
    def test_file_hash_consistency(self, mock_get_data_dir):
        """Test that the same data always produces the same hash."""
        test_data1 = b"consistent test data"
        test_data2 = b"consistent test data"
        test_data3 = b"different test data"

        hash1 = DataService.hash_data(test_data1)
        hash2 = DataService.hash_data(test_data2)
        hash3 = DataService.hash_data(test_data3)

        assert hash1 == hash2  # Same data, same hash
        assert hash1 != hash3  # Different data, different hash
        assert len(hash1) == 64  # SHA256 hex length

    def test_collision_timestamp_format(self):
        """Test that collision timestamp produces valid file names."""
        with patch("services.data_service.datetime") as mock_datetime:
            mock_datetime.now.return_value.timestamp.return_value = 1640995200.5

            # Test various file name formats
            test_cases = [
                ("file.pdf", "file_1640995200.5.pdf"),
                ("file.tar.gz", "file.tar_1640995200.5.gz"),
                ("no_extension", "no_extension_1640995200.5"),
                ("multiple.dots.in.name.txt", "multiple.dots.in.name_1640995200.5.txt"),
            ]

            for input_name, expected_output in test_cases:
                result = DataService.append_collision_timestamp(input_name)
                assert result == expected_output

    def test_metadata_serialization_roundtrip(self):
        """Test that metadata can be serialized and deserialized correctly."""
        original_metadata = MetadataFileContent(
            original_file_name="test.pdf",
            resolved_file_name="test_1640995200.0.pdf",
            size=1024,
            mime_type="application/pdf",
            hash="abcd1234",
            timestamp=1640995200.0,
        )

        # Serialize to JSON
        json_data = original_metadata.model_dump_json()

        # Deserialize back
        restored_metadata = MetadataFileContent.model_validate_json(json_data)

        # Verify all fields match
        assert (
            restored_metadata.original_file_name == original_metadata.original_file_name
        )
        assert (
            restored_metadata.resolved_file_name == original_metadata.resolved_file_name
        )
        assert restored_metadata.size == original_metadata.size
        assert restored_metadata.mime_type == original_metadata.mime_type
        assert restored_metadata.hash == original_metadata.hash
