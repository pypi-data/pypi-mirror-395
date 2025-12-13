from __future__ import annotations

import os
import time
from pathlib import Path
from typing import TYPE_CHECKING, Callable

import requests
from loguru import logger

from fused import context
from fused._options import StorageStr, _get_data_dir
from fused._options import options as OPTIONS

if TYPE_CHECKING:
    import fsspec


def data_path(storage: StorageStr = "auto") -> Path:
    if storage != "auto":
        return _get_data_dir(storage)
    return OPTIONS.data_directory


def filesystem(protocol: str, **storage_options) -> fsspec.AbstractFileSystem:
    """Get an fsspec filesystem for the given protocol.

    Args:
        protocol: Protocol part of the URL, such as "s3" or "gs".
        storage_options: Additional arguments to pass to the storage backend.

    Returns:
        An fsspec AbstractFileSystem.
    """

    import fsspec

    return fsspec.filesystem(protocol, **storage_options)


def _download_requests(url: str) -> bytes:
    # this function is shared
    response = requests.get(url, headers={"User-Agent": ""})
    response.raise_for_status()
    return response.content


def _download_signed(url: str) -> bytes:
    from fused.api._public_api import get_api

    api = get_api()
    return _download_requests(api.sign_url(url))


def _download_object(protocol: str, url: str) -> bytes:
    """

    Args:
        protocol: Protocol part of the URL, such as "s3" or "gs".
        url: Object URL with or without the protocol.

    Returns:
        The object's content in bytes
    """
    # Local needs to use signed URL to impersonal remote IAM role to download the file while remote can assume it has
    # direct access to S3 resources due to its IAM role.
    if not context.in_realtime() and not context.in_batch():
        logger.debug("Trying a signed URL")
        try:
            return _download_signed(url)
        except Exception as e:
            logger.debug(str(e))

    fs = filesystem(protocol)
    with fs.open(url, "rb") as f:
        return f.read()


def create_path(path: str, mkdir: bool = True) -> str:
    # Deprecated name...
    return file_path(file_path=path, mkdir=mkdir)


def file_path(file_path: str, mkdir: bool = True, storage: StorageStr = "auto") -> str:
    """Creates a directory in a predefined temporary directory.

    This gives users the ability to manage directories during the execution of a UDF.
    It takes a relative file_path, creates the corresponding directory structure,
    and returns its absolute path.

    This is useful for UDFs that temporarily store intermediate results as files,
    such as when writing intermediary files to disk when processing large datasets.
    `file_path` ensures that necessary directories exist.
    The directory is kept for 12h.

    Args:
        file_path: The relative file path to locate.
        mkdir: If True, create the directory if it doesn't already exist. Defaults to True.
        storage: Set where the cache data is stored. Supported values are "auto", "mount" and "local". Auto will
            automatically select the storage location defined in options (mount if it exists, otherwise local) and
            ensures that it exists and is writable. Mount gets shared across executions where local will only be shared
            within the same execution.

    Returns:
        The located file path.
    """
    # TODO: Move this onto the context object or use the context object
    global_path = data_path(storage)
    file_path = global_path / Path(file_path)

    if not file_path.suffix:
        folder = file_path
    else:
        folder = file_path.parent
    if mkdir:
        folder.mkdir(parents=True, exist_ok=True)
    return str(file_path)


def download(url: str, file_path: str, storage: StorageStr = "auto") -> str:
    """Download a file.

    May be called from multiple processes with the same inputs to get the same result.

    Fused runs UDFs from top to bottom each time code changes. This means objects in the UDF are recreated each time, which can slow down a UDF that downloads files from a remote server.

    💡 Downloaded files are written to a mounted volume shared across all UDFs in an organization. This means that a file downloaded by one UDF can be read by other UDFs.

    Fused addresses the latency of downloading files with the download utility function. It stores files in the mounted filesystem so they only download the first time.

    💡 Because a Tile UDF runs multiple chunks in parallel, the download function sets a signal lock during the first download attempt, to ensure the download happens only once.

    Args:
        url: The URL to download.
        file_path: The local path where to save the file.
        storage: Set where the cache data is stored. Supported values are "auto", "mount" and "local". Auto will
            automatically select the storage location defined in options (mount if it exists, otherwise local) and
            ensures that it exists and is writable. Mount gets shared across executions where local will only be shared
            within the same execution.

    Returns:
        The function downloads the file only on the first execution, and returns the file path.

    Examples:
        ```python
        @fused.udf
        def geodataframe_from_geojson():
            import geopandas as gpd
            url = "s3://sample_bucket/my_geojson.zip"
            path = fused.core.download(url, "tmp/my_geojson.zip")
            gdf = gpd.read_file(path)
            return gdf
        ```

    """
    from urllib.parse import urlparse

    from loguru import logger

    file_path = file_path.strip("/")

    # Cache in mounted drive if available & writable, else cache in /tmp
    base_path = data_path(storage)

    # Download directory
    file_full_path = Path(base_path) / file_path
    file_full_path.parent.mkdir(parents=True, exist_ok=True)

    def _download():
        parsed_url = urlparse(url)
        logger.debug(f"Downloading {url} -> {file_full_path}")

        if parsed_url.scheme in {"s3", "gs"}:
            content = _download_object(parsed_url.scheme, url)
        else:
            if parsed_url.scheme not in ["http", "https"]:
                logger.debug(f"Unexpected URL scheme {parsed_url.scheme}")
            content = _download_requests(url)

        with open(file_full_path, "wb") as file:
            file.write(content)

    _run_once(signal_name=file_path, fn=_download)

    return file_full_path


def _run_once(signal_name: str, fn: Callable) -> None:
    """Run a function once, waiting for another process to run it if in progress.

    Args:
        signal_key: A relative key for signalling done status. Files are written using `file_path` and this key to deduplicate runs.
        fn: A function that will be run once.
    """
    from loguru import logger

    path_in_progress = Path(file_path(signal_name + ".in_progress"))
    path_done = Path(file_path(signal_name + ".done"))
    path_error = Path(file_path(signal_name + ".error"))

    def _wait_for_file_done():
        logger.debug(f"Waiting for {signal_name}")
        while not path_done.exists() and not path_error.exists():
            time.sleep(1)
        if path_error.exists():
            os.remove(str(path_in_progress))
            os.remove(str(path_error))
            raise ValueError(f"{signal_name} failed in another chunk. Try again.")
        logger.info(f"already cached ({signal_name}).")

    if path_in_progress.is_file():
        _wait_for_file_done()
    else:
        try:
            with open(path_in_progress, "x") as file:
                file.write("requesting")
        except FileExistsError:
            _wait_for_file_done()
            return
        logger.debug(f"Running fn -> {signal_name}")

        try:
            fn()
        except:
            with open(path_error, "w") as file:
                file.write("done")
            raise

        with open(path_done, "w") as file:
            file.write("done")
        logger.info(f"waited successfully ({signal_name}).")
