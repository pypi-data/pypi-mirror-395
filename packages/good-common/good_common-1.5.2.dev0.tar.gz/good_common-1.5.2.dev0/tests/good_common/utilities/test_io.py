"""Tests for good_common.utilities.io module."""

import datetime
import tempfile
import zipfile
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from good_common.utilities.io import (
    create_retry_decorator,
    decompress_tempfile,
    get_file_metadata,
    get_url_headers,
    is_cloudfront_response,
    is_cloudfront_url,
    safely_remove_file,
    set_file_timestamp,
    should_download_file,
)


class TestGetUrlHeaders:
    """Test get_url_headers function."""

    @pytest.mark.asyncio
    async def test_get_url_headers_success(self):
        """Test successful header retrieval."""
        mock_response = MagicMock()
        mock_response.headers = {
            "content-type": "text/html",
            "last-modified": "Wed, 21 Oct 2024 07:28:00 GMT",
            "content-length": "1234",
            "date": "Wed, 21 Oct 2024 07:28:00 GMT",
        }

        with patch("httpx.AsyncClient") as mock_client:
            mock_async_client = AsyncMock()
            mock_async_client.head.return_value = mock_response
            mock_client.return_value.__aenter__.return_value = mock_async_client

            headers = await get_url_headers("https://example.com")

            assert "content-type" in headers
            assert headers["content-type"] == "text/html"
            assert "last-modified" in headers
            # last-modified doesn't have "date" in the key name, so it won't be parsed
            assert headers["last-modified"] == "Wed, 21 Oct 2024 07:28:00 GMT"
            # But 'date' field should be parsed
            assert isinstance(headers["date"], datetime.datetime)

    @pytest.mark.asyncio
    async def test_get_url_headers_with_date_parsing(self):
        """Test that date headers are parsed correctly."""
        mock_response = MagicMock()
        mock_response.headers = {
            "date": "Wed, 21 Oct 2024 07:28:00 GMT",
            "last-modifiedtime": "2024-10-21T07:28:00Z",
        }

        with patch("httpx.AsyncClient") as mock_client:
            mock_async_client = AsyncMock()
            mock_async_client.head.return_value = mock_response
            mock_client.return_value.__aenter__.return_value = mock_async_client

            headers = await get_url_headers("https://example.com")

            assert isinstance(headers["date"], datetime.datetime)
            assert isinstance(headers["last-modifiedtime"], datetime.datetime)


class TestDecompressTempfile:
    """Test decompress_tempfile function."""

    @pytest.mark.asyncio
    async def test_decompress_tempfile_basic(self, tmp_path):
        """Test basic decompression of a zip file."""
        # Create a test zip file
        zip_path = tmp_path / "test.zip"
        test_content = b"Test file content"
        
        with zipfile.ZipFile(zip_path, "w") as zf:
            zf.writestr("test_file.txt", test_content)

        # Decompress
        result = await decompress_tempfile(zip_path)

        assert result.exists()
        assert result.is_dir()
        assert (result / "test_file.txt").exists()
        assert (result / "test_file.txt").read_bytes() == test_content

    @pytest.mark.asyncio
    async def test_decompress_tempfile_with_destination(self, tmp_path):
        """Test decompression to a specific destination."""
        zip_path = tmp_path / "test.zip"
        dest_path = tmp_path / "custom_dest"
        
        with zipfile.ZipFile(zip_path, "w") as zf:
            zf.writestr("file.txt", b"content")

        result = await decompress_tempfile(zip_path, destination=dest_path)

        assert result == dest_path
        assert dest_path.exists()
        assert (dest_path / "file.txt").exists()

    @pytest.mark.asyncio
    async def test_decompress_tempfile_clear_destination(self, tmp_path):
        """Test clearing destination before decompression."""
        zip_path = tmp_path / "test.zip"
        dest_path = tmp_path / "dest"
        
        # Create existing file in destination
        dest_path.mkdir()
        (dest_path / "existing.txt").write_text("old content")
        
        with zipfile.ZipFile(zip_path, "w") as zf:
            zf.writestr("new.txt", b"new content")

        result = await decompress_tempfile(
            zip_path, destination=dest_path, clear_destination=True
        )

        assert result == dest_path
        assert not (dest_path / "existing.txt").exists()
        assert (dest_path / "new.txt").exists()


class TestCloudFrontChecks:
    """Test CloudFront-related functions."""

    def test_is_cloudfront_url_true(self):
        """Test identifying CloudFront URLs."""
        cf_urls = [
            "https://d1234567890.cloudfront.net/file.pdf",
            "http://dxxxxxxx.cloudfront.net/path/to/file",
            "https://d2bu9v0mnxvlol.cloudfront.net/",
        ]
        
        for url in cf_urls:
            assert is_cloudfront_url(url) is True

    def test_is_cloudfront_url_false(self):
        """Test non-CloudFront URLs."""
        non_cf_urls = [
            "https://example.com/file.pdf",
            "https://cdn.example.com/file",
            "https://amazonaws.com/file",
        ]
        
        for url in non_cf_urls:
            assert is_cloudfront_url(url) is False

    def test_is_cloudfront_response(self):
        """Test identifying CloudFront responses."""
        # CloudFront response
        cf_response = MagicMock(spec=httpx.Response)
        cf_response.headers = {"x-amz-cf-id": "some-cf-id"}
        assert is_cloudfront_response(cf_response) is True

        # Non-CloudFront response
        regular_response = MagicMock(spec=httpx.Response)
        regular_response.headers = {"content-type": "text/html"}
        assert is_cloudfront_response(regular_response) is False


class TestFileMetadata:
    """Test file metadata functions."""

    @pytest.mark.asyncio
    async def test_get_file_metadata_success(self):
        """Test successful file metadata retrieval."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {
            "content-length": "1024",
            "last-modified": "Wed, 21 Oct 2024 07:28:00 GMT",
        }

        mock_client = AsyncMock()
        mock_client.head.return_value = mock_response

        response, last_modified = await get_file_metadata(
            mock_client, "https://example.com/file.pdf", retry_count=3
        )

        assert response == mock_response
        # last_modified should be parsed datetime
        assert isinstance(last_modified, datetime.datetime)

    @pytest.mark.asyncio
    async def test_get_file_metadata_no_content_length(self):
        """Test metadata retrieval when content-length is missing."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {}

        mock_client = AsyncMock()
        mock_client.head.return_value = mock_response

        response, last_modified = await get_file_metadata(
            mock_client, "https://example.com/file.pdf", retry_count=3
        )

        assert response == mock_response
        assert last_modified is None

    def test_should_download_file_no_local_file(self, tmp_path):
        """Test should_download_file when local file doesn't exist."""
        non_existent = tmp_path / "nonexistent.txt"
        assert should_download_file(non_existent, None, False) is True

    def test_should_download_file_overwrite(self, tmp_path):
        """Test should_download_file with overwrite flag."""
        existing_file = tmp_path / "existing.txt"
        existing_file.write_text("content")
        
        assert should_download_file(existing_file, None, True) is True

    def test_should_download_file_no_overwrite_existing(self, tmp_path):
        """Test should_download_file with existing file and no overwrite."""
        existing_file = tmp_path / "existing.txt"
        existing_file.write_text("content")
        
        # File exists and no timestamp - don't download
        assert should_download_file(existing_file, None, False) is False


class TestSafelyRemoveFile:
    """Test safely_remove_file function."""

    def test_safely_remove_existing_file(self, tmp_path, caplog):
        """Test removing an existing file."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")
        
        with caplog.at_level("INFO"):
            safely_remove_file(test_file, "Test")
        
        assert not test_file.exists()
        assert "Test: Removing existing file" in caplog.text

    def test_safely_remove_nonexistent_file(self, tmp_path, caplog):
        """Test removing a non-existent file."""
        test_file = tmp_path / "nonexistent.txt"
        
        with caplog.at_level("INFO"):
            safely_remove_file(test_file, "Test")
        
        assert "Test: No existing file to remove" in caplog.text

    def test_safely_remove_permission_error(self, tmp_path, caplog):
        """Test handling permission errors."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")  # Create the file so it exists
        
        with caplog.at_level("WARNING"):
            with patch("pathlib.Path.unlink", side_effect=PermissionError("No permission")):
                safely_remove_file(test_file, "Test")
            
        assert "Test: Failed to remove file" in caplog.text
        assert "No permission" in caplog.text


class TestSetFileTimestamp:
    """Test set_file_timestamp function."""

    def test_set_file_timestamp(self, tmp_path):
        """Test setting file timestamp."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")
        
        # Set specific timestamp
        new_time = datetime.datetime(2024, 1, 1, 12, 0, 0)
        set_file_timestamp(test_file, new_time)
        
        # Verify timestamp was set
        stat = test_file.stat()
        file_time = datetime.datetime.fromtimestamp(stat.st_mtime)
        
        # Allow small difference due to filesystem precision
        assert abs((file_time - new_time).total_seconds()) < 1


class TestRetryDecorator:
    """Test create_retry_decorator function."""

    def test_create_retry_decorator_basic(self):
        """Test basic retry decorator creation."""
        decorator = create_retry_decorator(3)
        
        # Mock function that fails twice then succeeds
        call_count = {"count": 0}
        
        @decorator
        def flaky_function():
            call_count["count"] += 1
            if call_count["count"] < 3:
                raise httpx.ConnectError("Connection failed")
            return "success"
        
        result = flaky_function()
        assert result == "success"
        assert call_count["count"] == 3

    def test_create_retry_decorator_max_attempts(self):
        """Test retry decorator reaches max attempts."""
        decorator = create_retry_decorator(2)
        
        @decorator
        def always_fails():
            raise httpx.ConnectError("Connection failed")
        
        with pytest.raises(httpx.ConnectError):
            always_fails()


class TestDownloadUrlToFile:
    """Test download_url_to_file function."""

    @pytest.mark.skip(reason="Test requires network access - should be converted to integration test")
    @pytest.mark.asyncio
    async def test_download_url_to_file_basic(self, tmp_path):
        """Test basic file download."""
        # This test requires actual network access or a more complex mock setup
        # Skip for now to avoid network dependencies in unit tests
        pass


# Integration test fixtures
@pytest.fixture
def mock_httpx_client():
    """Fixture for mocking httpx.AsyncClient."""
    with patch("httpx.AsyncClient") as mock:
        yield mock


@pytest.fixture
def temp_dir():
    """Fixture for temporary directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)