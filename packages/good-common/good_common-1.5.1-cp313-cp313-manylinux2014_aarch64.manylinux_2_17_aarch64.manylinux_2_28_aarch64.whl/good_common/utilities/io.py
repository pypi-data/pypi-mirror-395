import asyncio
import datetime
import logging
import os
import re
import shutil
import tempfile
import zipfile
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any, AsyncGenerator, Awaitable, Callable, Dict, Optional, Tuple, cast

import dateparser
import httpx
import tqdm
from loguru import logger
from tenacity import (
    RetryError,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

# Create a standard logger for functions that need pytest caplog compatibility
standard_logger = logging.getLogger(__name__)


async def get_url_headers(url: str):
    async with httpx.AsyncClient(timeout=30, follow_redirects=True) as client:
        r = await client.head(url)
        headers: Dict[str, Any] = dict(r.headers)
        for k, v in headers.items():
            if any([x in k for x in ("date", "modifiedtime")]):
                parsed_date = dateparser.parse(v)
                headers[k] = parsed_date if parsed_date else v
        return headers


async def decompress_tempfile(
    tempfile: Path, destination: Path | None = None, clear_destination: bool = False
) -> Path:
    """
    Takes a Path object to a compressed file and returns a Path object to the
    decompressed archive folder.
    """
    with zipfile.ZipFile(tempfile, "r") as archive:
        if not destination:
            destination = tempfile.parent / tempfile.stem
        if clear_destination:
            logger.info(f"Clearing destination folder {destination}")
            try:
                shutil.rmtree(destination)
            except FileNotFoundError:
                pass

        destination.mkdir(parents=True, exist_ok=True)
        archive.extractall(destination)
    return destination


async def download_url_to_file(
    url: str,
    directory: Path,
    filename: str | None = None,
    display_progress: bool = True,
    overwrite: bool = False,
    max_threads: int = 4,
) -> Path:
    async with download_url_to_temp_file(
        url,
        directory,
        filename,
        display_progress=display_progress,
        cleanup=False,
        overwrite=overwrite,
        max_threads=max_threads,
    ) as file:
        return file


# Custom exceptions
class IncompleteDownloadError(Exception):
    """Raised when a download is incomplete."""

    pass


class FileDoesNotExist(Exception):
    """Raised when a file doesn't exist at the specified URL."""

    pass


class RangeNotSatisfiableError(Exception):
    """Raised when a server cannot fulfill a range request (HTTP 416)."""

    pass


def create_retry_decorator(retry_count: int):
    """Create a retry decorator with the specified number of attempts."""
    return retry(
        retry=retry_if_exception_type(
            (httpx.ConnectError, httpx.ConnectTimeout, ValueError, OSError)
        ),
        stop=stop_after_attempt(retry_count),
        wait=wait_exponential(multiplier=1.2, min=2, max=60),
        before_sleep=lambda retry_state: logger.warning(
            f"Connection failed, retrying in {retry_state.next_action.sleep if retry_state.next_action else 'unknown'} seconds: "
            f"{str(retry_state.outcome.exception()) if retry_state.outcome else 'unknown error'}"
        ),
        reraise=True,
    )


def is_cloudfront_url(url: str) -> bool:
    """Check if a URL is likely being served by CloudFront."""
    cloudfront_patterns = [r"\.cloudfront\.net", r"\.amazonaws\.com"]

    return any(
        re.search(pattern, url, re.IGNORECASE) for pattern in cloudfront_patterns
    )


def is_cloudfront_response(response: httpx.Response) -> bool:
    """Check if a response is coming from CloudFront based on headers."""
    # Check for CloudFront-specific headers
    if "x-amz-cf-id" in response.headers:
        return True
    if "via" in response.headers and "cloudfront" in response.headers["via"].lower():
        return True
    if response.headers.get("server", "").lower() == "cloudfront":
        return True
    return False


async def get_file_metadata(
    client: httpx.AsyncClient, url: str, retry_count: int
) -> Tuple[Optional[httpx.Response], Optional[datetime.datetime]]:
    """
    Get metadata about a file from the server using HEAD request.
    Returns a tuple of (response, timestamp).
    """
    retry_decorator = create_retry_decorator(retry_count)

    @retry_decorator
    async def check_head():
        try:
            return await client.head(url)
        except ValueError as e:
            # Handle the specific ValueError from anyio
            if "second argument (exceptions) must be a non-empty sequence" in str(e):
                raise httpx.ConnectError(
                    f"Connection to {url} failed with network error"
                ) from e
            raise

    try:
        head_response = await check_head()

        if not head_response.is_success and not head_response.has_redirect_location:
            raise FileDoesNotExist(f"File not found at {url}")

        # Check if the response is from CloudFront
        if is_cloudfront_response(head_response):
            logger.debug(f"Detected CloudFront response for {url}")

        # Get timestamp from headers (headers are case-insensitive)
        file_timestamp = None
        headers_dict = {k.lower(): v for k, v in head_response.headers.items()}
        if "last-modified" in headers_dict:
            file_timestamp = dateparser.parse(headers_dict["last-modified"])
        elif "date" in headers_dict:
            file_timestamp = dateparser.parse(headers_dict["date"])

        return head_response, file_timestamp

    except RetryError as e:
        # If HEAD request fails persistently, we'll fall back to GET
        logger.warning(
            f"HEAD request failed after {retry_count} attempts: {str(e.last_attempt.exception())}"
        )
        return None, None


def should_download_file(
    filepath: Path, file_timestamp: Optional[datetime.datetime], overwrite: bool
) -> bool:
    """
    Determine if we need to download the file based on local existence and timestamps.
    """
    if not filepath.exists() or overwrite:
        return True

    # File exists and overwrite is False
    if file_timestamp:
        # Get local file's modified time
        file_mtime = datetime.datetime.fromtimestamp(
            filepath.stat().st_mtime, tz=datetime.timezone.utc
        )

        # Skip download if server file is not newer
        if file_timestamp <= file_mtime:
            logger.info(f"Skipping {filepath.name} - file is up to date")
            return False
        # Download if server file is newer
        return True

    # File exists, no timestamp, and overwrite is False - don't download
    return False


async def download_single_threaded(
    client: httpx.AsyncClient,
    url: str,
    filepath: Path,
    display_progress: bool,
    retry_count: int,
) -> int:
    """
    Download a file using a single connection.
    Returns the total bytes downloaded.
    """
    retry_decorator = create_retry_decorator(retry_count)

    async def _perform_download() -> tuple[int, int]:
        total_downloaded: int = 0

        with open(filepath, "wb") as download_file:
            async with client.stream("GET", url) as response:
                if not response.is_success:
                    raise httpx.HTTPStatusError(
                        f"HTTP Error {response.status_code}",
                        request=response.request,
                        response=response,
                    )

                total = int(response.headers.get("Content-Length", 0))
                with tqdm.tqdm(
                    total=total,
                    unit_scale=True,
                    unit_divisor=1024,
                    unit="B",
                    disable=not display_progress,
                ) as progress:
                    num_bytes_downloaded = response.num_bytes_downloaded
                    async for chunk in response.aiter_bytes():
                        download_file.write(chunk)
                        total_downloaded += len(chunk)
                        progress.update(
                            response.num_bytes_downloaded - num_bytes_downloaded
                        )
                        num_bytes_downloaded = response.num_bytes_downloaded

                # Return tuple of (total_downloaded, expected_size)
                return total_downloaded, int(response.headers.get("Content-Length", 0))

    perform_download = cast(
        Callable[[], Awaitable[tuple[int, int]]],
        retry_decorator(_perform_download),
    )

    try:
        total_downloaded, expected_size = await perform_download()

        # Verify the download is complete if content length was provided
        if expected_size > 0 and total_downloaded != expected_size:
            raise IncompleteDownloadError(
                f"File download incomplete. Expected {expected_size} bytes, got {total_downloaded} bytes."
            )

        return total_downloaded
    except (RetryError, httpx.HTTPError) as e:
        # Clean up the partial file
        safely_remove_file(filepath, "Download error cleanup: ")

        if isinstance(e, RetryError):
            # Unwrap the original exception from RetryError
            original_exception = e.last_attempt.exception()
            if original_exception and isinstance(original_exception, BaseException):
                raise original_exception from e
        raise


async def test_range_support(
    client: httpx.AsyncClient, url: str, content_length: int
) -> bool:
    """
    Test if server truly supports range requests by making a small range request.
    Returns True if range requests are supported, False otherwise.
    """
    # Test with a very small range from the beginning of the file
    test_end = min(
        1023, content_length - 1
    )  # Request at most 1KB or less if file is smaller
    headers = {"Range": f"bytes=0-{test_end}"}

    try:
        async with client.stream("GET", url, headers=headers) as response:
            # Check if this is a CloudFront response
            is_cloudfront = is_cloudfront_response(response)

            if response.status_code == 206:  # Partial Content - what we want
                # For CloudFront, verify content length matches what we expect
                if is_cloudfront:
                    expected_content_length = test_end + 1
                    actual_content_length = int(
                        response.headers.get("Content-Length", 0)
                    )

                    if actual_content_length != expected_content_length:
                        logger.warning(
                            f"CloudFront range length mismatch: expected {expected_content_length}, "
                            f"got {actual_content_length}. Disabling range requests."
                        )
                        return False

                # Consume and discard the body
                async for _ in response.aiter_bytes(1024):
                    pass
                # logger.debug(f"Range requests confirmed to work for {url}")
                return True
            else:
                if is_cloudfront:
                    logger.warning(
                        f"CloudFront range request failed with status {response.status_code}. "
                        f"Disabling multi-threaded downloads."
                    )
                else:
                    logger.warning(
                        f"Range requests test failed for {url}: got status code {response.status_code}"
                    )
                return False
    except httpx.HTTPError as e:
        if is_cloudfront_url(url) or "cloudfront" in str(e).lower():
            logger.warning(
                f"CloudFront range request failed: {str(e)}. Disabling multi-threaded downloads."
            )
        else:
            logger.warning(f"Range requests test failed for {url}: {str(e)}")
        return False


async def download_chunk(
    client: httpx.AsyncClient,
    url: str,
    chunk_id: int,
    start_byte: int,
    end_byte: int,
    chunk_file: Path,
    progress: Optional[tqdm.tqdm],
    semaphore: asyncio.Semaphore,
    retry_count: int,
) -> Path:
    """Download a single chunk of a file with range headers."""
    retry_decorator = create_retry_decorator(retry_count)

    # Skip if chunk has zero or negative size
    chunk_size = end_byte - start_byte + 1
    if chunk_size <= 0:
        logger.warning(
            f"Skipping chunk {chunk_id} with invalid size: {chunk_size} bytes"
        )
        # Create an empty file so the chunk merger doesn't fail
        chunk_file.touch()
        return chunk_file

    async with semaphore:  # Limit concurrent connections
        headers = {"Range": f"bytes={start_byte}-{end_byte}"}

        async def _get_chunk() -> Path:
            try:
                async with client.stream("GET", url, headers=headers) as response:
                    # Check for 416 Range Not Satisfiable
                    if response.status_code == 416:
                        raise RangeNotSatisfiableError(
                            f"Server cannot fulfill range request for chunk {chunk_id} ({start_byte}-{end_byte})"
                        )

                    # Check for any non-206 response
                    if response.status_code != 206:  # 206 Partial Content
                        # Special handling for CloudFront errors
                        if is_cloudfront_response(response):
                            logger.error(
                                f"CloudFront error for chunk {chunk_id}: status {response.status_code}"
                            )
                            error_content = await response.aread()
                            if (
                                len(error_content) < 200
                            ):  # Only log if it's small enough
                                preview = error_content.decode(
                                    "utf-8", errors="replace"
                                )
                                logger.error(f"CloudFront error content: {preview}")
                            raise RangeNotSatisfiableError(
                                f"CloudFront error for range request ({start_byte}-{end_byte})"
                            )
                        else:
                            raise httpx.HTTPStatusError(
                                f"Expected 206 Partial Content, got {response.status_code} for chunk {chunk_id}",
                                request=response.request,
                                response=response,
                            )

                    with open(chunk_file, "wb") as f:
                        downloaded = 0
                        expected_size = end_byte - start_byte + 1
                        async for data in response.aiter_bytes():
                            f.write(data)
                            downloaded += len(data)
                            if progress:
                                progress.update(len(data))

                    # Verify chunk size matches expected
                    if downloaded != expected_size:
                        raise IncompleteDownloadError(
                            f"Chunk {chunk_id} download incomplete. Expected {expected_size} bytes, got {downloaded} bytes."
                        )
            except httpx.HTTPStatusError as e:
                # Check if it's a 416 error from the response
                if e.response.status_code == 416:
                    raise RangeNotSatisfiableError(
                        f"Server cannot fulfill range request for chunk {chunk_id} ({start_byte}-{end_byte})"
                    ) from e

                # Check if it's a CloudFront error
                if is_cloudfront_response(e.response):
                    logger.error(
                        f"CloudFront error for chunk {chunk_id}: status {e.response.status_code}"
                    )
                    raise RangeNotSatisfiableError(
                        f"CloudFront error for range request ({start_byte}-{end_byte})"
                    ) from e
                raise

            return chunk_file

        get_chunk = cast(Callable[[], Awaitable[Path]], retry_decorator(_get_chunk))

        try:
            return await get_chunk()
        except RetryError as e:
            # Unwrap the original exception from RetryError
            original_exception = e.last_attempt.exception()
            if original_exception and isinstance(original_exception, BaseException):
                raise original_exception from e
            raise


async def download_multi_threaded(
    client: httpx.AsyncClient,
    url: str,
    filepath: Path,
    content_length: int,
    max_threads: int,
    display_progress: bool,
    retry_count: int,
) -> None:
    """
    Download a file using multiple concurrent connections.
    """
    # Immediate check for CloudFront URL to prevent unnecessary tests
    if is_cloudfront_url(url):
        logger.warning(
            f"CloudFront URL detected: {url} - checking range support carefully"
        )

    # Test if server truly supports range requests properly
    range_support_confirmed = await test_range_support(client, url, content_length)

    if not range_support_confirmed:
        raise RangeNotSatisfiableError(
            f"Server does not properly support range requests for {url}"
        )

    # Create temporary directory for chunks
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir_path = Path(temp_dir)

        # Define minimum chunk size (16KB)
        MIN_CHUNK_SIZE = 16 * 1024

        # For CloudFront, use larger chunks and fewer connections
        if is_cloudfront_url(url):
            MIN_CHUNK_SIZE = 1024 * 1024  # 1MB minimum
            max_threads = min(max_threads, 4)  # Limit to 4 threads for CloudFront
            # logger.debug(
            #     f"CloudFront detected: using larger chunks and {max_threads} threads"
            # )

        # Calculate number of chunks based on content length and minimum chunk size
        max_possible_chunks = content_length // MIN_CHUNK_SIZE
        num_chunks = min(
            max(max_threads * 2, 8), max_possible_chunks
        )  # Limit chunks to prevent too small chunks

        # If file is too small for chunking, fall back to fewer chunks
        if num_chunks < 2:
            logger.info(
                f"File too small ({content_length} bytes) for multi-threaded download, using single chunk"
            )
            num_chunks = 1

        chunk_size = content_length // num_chunks

        # Ensure chunk size is at least MIN_CHUNK_SIZE (except potentially the last chunk)
        if chunk_size < MIN_CHUNK_SIZE and num_chunks > 1:
            num_chunks = content_length // MIN_CHUNK_SIZE
            if num_chunks < 1:
                num_chunks = 1
            chunk_size = content_length // num_chunks

        # logger.debug(
        #     f"Downloading with {num_chunks} chunks of ~{chunk_size} bytes each"
        # )

        chunks = []
        for i in range(num_chunks):
            start_byte = i * chunk_size
            end_byte = (
                (i + 1) * chunk_size - 1 if i < num_chunks - 1 else content_length - 1
            )
            chunks.append((i, start_byte, end_byte))

        # Create progress bar if enabled
        progress = (
            tqdm.tqdm(
                total=content_length,
                unit_scale=True,
                unit_divisor=1024,
                unit="B",
                disable=not display_progress,
            )
            if display_progress
            else None
        )

        # Create a semaphore to limit concurrent downloads
        semaphore = asyncio.Semaphore(max_threads)

        # Track all chunk files for cleanup
        all_chunk_files = {temp_dir_path / f"chunk_{i}" for i, _, _ in chunks}

        # Create tasks for all chunks
        tasks = [
            download_chunk(
                client,
                url,
                i,
                start,
                end,
                temp_dir_path / f"chunk_{i}",
                progress,
                semaphore,
                retry_count,
            )
            for i, start, end in chunks
        ]

        # Wait for all chunks to download (semaphore will limit concurrency)
        try:
            chunk_files = await asyncio.gather(*tasks)

            # Combine chunks into final file - only if all chunks downloaded successfully
            with open(filepath, "wb") as outfile:
                for chunk_file in sorted(
                    chunk_files, key=lambda x: int(x.name.split("_")[1])
                ):
                    with open(chunk_file, "rb") as infile:
                        outfile.write(infile.read())

            # Verify final file size matches expected content length
            final_size = filepath.stat().st_size
            if final_size != content_length:
                raise IncompleteDownloadError(
                    f"File download incomplete. Expected {content_length} bytes, got {final_size} bytes."
                )

        except (asyncio.CancelledError, Exception) as e:
            # Handle cancellation and other errors
            logger.warning(f"Download was interrupted: {str(e)}")

            # Clean up any partial chunks
            for chunk_file in all_chunk_files:
                safely_remove_file(chunk_file, "Chunk cleanup: ")

            # Clean up the partial download file
            safely_remove_file(filepath, "Multi-threaded download cleanup: ")

            raise
        finally:
            # Close progress bar
            if progress:
                progress.close()


def safely_remove_file(filepath: Path, log_prefix: str = ""):
    """Safely delete a file with error handling."""
    if filepath.exists():
        standard_logger.info(f"{log_prefix}: Removing existing file")
        try:
            filepath.unlink()
        except (OSError, PermissionError) as e:
            standard_logger.warning(
                f"{log_prefix}: Failed to remove file {filepath}: {str(e)}"
            )
    else:
        standard_logger.info(f"{log_prefix}: No existing file to remove")


def set_file_timestamp(filepath: Path, timestamp: datetime.datetime):
    """Set the access and modification times of a file."""
    if filepath.exists() and timestamp:
        try:
            os_timestamp = timestamp.timestamp()
            os.utime(filepath, (os_timestamp, os_timestamp))
        except OSError as e:
            logger.warning(f"Failed to set timestamp for {filepath}: {str(e)}")


@asynccontextmanager
async def download_url_to_temp_file(
    url: str,
    directory: Path,
    filename: str | None = None,
    display_progress: bool = True,
    cleanup: bool = False,
    overwrite: bool = False,
    max_threads: int = 4,
    retry_count: int = 3,
    disable_multi_threaded: bool = False,  # Added option to disable multi-threaded entirely
) -> AsyncGenerator[Path, None]:
    """
    Download a file from a URL to a local directory.

    Args:
        url: The URL to download from
        directory: The directory to save the file to
        filename: The filename to save as (defaults to the URL's filename)
        display_progress: Whether to display a progress bar
        cleanup: Whether to remove the file after the context manager exits
        overwrite: Whether to overwrite existing files
        max_threads: Maximum number of concurrent download connections
        retry_count: Number of times to retry failed connections
        disable_multi_threaded: Set to True to force single-threaded downloads

    Yields:
        The path to the downloaded file

    Raises:
        FileDoesNotExist: If the file is not found at the URL
        IncompleteDownloadError: If the download is incomplete
        ConnectionError: If connection to the server fails
        httpx.HTTPError: For HTTP protocol errors
    """
    if filename is None:
        filename = Path(url).name

    filepath = directory / filename

    # Flag to track if we should delete the file on cleanup
    downloaded_this_session = False

    # Ensure the output directory exists
    directory.mkdir(parents=True, exist_ok=True)

    # Check if this is a CloudFront URL
    cf_url = is_cloudfront_url(url)
    if cf_url:
        # logger.debug(f"CloudFront URL detected: {url}")
        # Consider disabling multi-threaded for CloudFront by default
        if max_threads > 4:
            # logger.debug(
            #     f"Limiting max_threads to 4 for CloudFront URL (was {max_threads})"
            # )
            max_threads = 4

    # Create HTTP client with extended timeout for CloudFront
    timeout = 600
    # if cf_url else 300  # Use longer timeout for CloudFront
    async with httpx.AsyncClient(
        timeout=timeout,
        follow_redirects=True,
    ) as client:
        try:
            # Get file metadata
            head_response, file_timestamp = await get_file_metadata(
                client, url, retry_count
            )

            # Check if we need to download the file
            should_download = should_download_file(filepath, file_timestamp, overwrite)

            if should_download:
                # Set flag to indicate we're downloading in this session
                downloaded_this_session = True

                # Remove existing file if it exists
                safely_remove_file(filepath, "Pre-download cleanup: ")

                # Get range support and content length from headers
                supports_range = False
                content_length = 0

                if head_response:
                    supports_range = (
                        head_response.headers.get("Accept-Ranges") == "bytes"
                    )
                    content_length = int(head_response.headers.get("Content-Length", 0))

                    # Log the Accept-Ranges header for debugging
                    # logger.debug(
                    #     f"Server Accept-Ranges header: {head_response.headers.get('Accept-Ranges', 'None')}"
                    # )

                    # # Check for CloudFront in the response
                    # if is_cloudfront_response(head_response):
                    #     logger.debug("CloudFront detected in response headers")

                # Try multi-threaded download if conditions are met and it's not explicitly disabled
                if (
                    supports_range
                    and content_length > 1024 * 1024
                    and max_threads > 1
                    and not disable_multi_threaded
                ):
                    # logger.debug(
                    #     f"Attempting to download {filename} with {max_threads} concurrent connections"
                    # )
                    try:
                        await download_multi_threaded(
                            client,
                            url,
                            filepath,
                            content_length,
                            max_threads,
                            display_progress,
                            retry_count,
                        )
                    except RangeNotSatisfiableError:
                        # If range requests fail, fall back to single-threaded
                        # logger.warning(
                        #     f"Range request failed: {str(e)}. Falling back to single-threaded download."
                        # )
                        safely_remove_file(filepath, "Range error cleanup: ")

                        # Do single-threaded download
                        logger.debug(f"Downloading {filename} with single thread")
                        await download_single_threaded(
                            client, url, filepath, display_progress, retry_count
                        )
                else:
                    # Log why we're using single-threaded download
                    # if disable_multi_threaded:
                    #     logger.debug("Multi-threaded downloads explicitly disabled")
                    # elif not supports_range:
                    #     logger.debug(
                    #         f"Server does not support range requests, using single-threaded download"
                    #     )
                    # elif content_length <= 1024 * 1024:
                    #     logger.debug(
                    #         f"File too small ({content_length} bytes) for multi-threaded download"
                    #     )
                    # elif max_threads <= 1:
                    #     logger.debug(
                    #         f"Multi-threaded download disabled by configuration"
                    #     )

                    # Regular single-threaded download
                    # logger.debug(f"Downloading {filename} with single thread")
                    await download_single_threaded(
                        client, url, filepath, display_progress, retry_count
                    )

                # Set file timestamps if available
                if file_timestamp:
                    set_file_timestamp(filepath, file_timestamp)

            # Yield the filepath to the caller
            yield filepath

        except Exception as e:
            # Handle all errors
            logger.opt(exception=e).error(f"Download error for {url}: {str(e)}")
            # Clean up any partial download if it was from this session
            if filepath.exists() and downloaded_this_session:
                safely_remove_file(filepath, "Error cleanup: ")
            raise
        finally:
            # Final cleanup if requested
            if cleanup and filepath.exists() and downloaded_this_session:
                safely_remove_file(filepath, "Final cleanup: ")
