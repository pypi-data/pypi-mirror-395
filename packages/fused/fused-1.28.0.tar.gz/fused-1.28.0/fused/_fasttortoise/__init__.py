"""Fast Tortoise - Efficient parquet row group reconstruction from metadata."""

from typing import Any, Dict, List, Optional

from fused._options import options as OPTIONS

# Keep the API helpers in fused-py since they're just API clients
from ._api import find_dataset, get_row_groups_for_dataset, register_dataset


def _get_metadata_url(base_url: Optional[str] = None) -> str:
    """
    Get the metadata URL, using current environment's base URL if not specified.

    Args:
        base_url: Optional base URL override

    Returns:
        Full metadata endpoint URL
    """
    if base_url is None:
        base_url = OPTIONS.base_url

    return f"{base_url}/file-metadata"


def read_parquet_row_group(
    parquet_path: str,
    row_group_index: int,
    base_url: Optional[str] = None,
    columns=None,
):
    """
    Reconstruct and read a single row group from a parquet file.

    Args:
        parquet_path: S3 or HTTP path to parquet file
        row_group_index: Index of row group to read (0-based)
        base_url: Base URL for API (e.g., "https://www.fused.io/server/v1"). If None, uses current environment.
        columns: Optional list of column names to read

    Returns:
        PyArrow Table containing the row group data

    This function imports the implementation from job2 at runtime,
    similar to how raster_to_h3 works.

    Example:
        table = read_parquet_row_group(path, 0)
        df = table.to_pandas()
    """
    metadata_url = _get_metadata_url(base_url)

    try:
        from job2.fasttortoise import read_parquet_row_group as _read_parquet_row_group

        return _read_parquet_row_group(
            parquet_path=parquet_path,
            row_group_index=row_group_index,
            metadata_url=metadata_url,
            columns=columns,
        )
    except ImportError as e:
        raise RuntimeError(
            "The fasttortoise reconstruction functionality requires the job2 module. "
            "This is typically only available in the Fused execution environment."
        ) from e


async def async_read_parquet_row_group(
    parquet_path: str,
    row_group_index: int,
    base_url: Optional[str] = None,
    columns=None,
):
    """
    Reconstruct and read a single row group from a parquet file (async version).

    Args:
        parquet_path: S3 or HTTP path to parquet file
        row_group_index: Index of row group to read (0-based)
        base_url: Base URL for API (e.g., "https://www.fused.io/server/v1"). If None, uses current environment.
        columns: Optional list of column names to read

    Returns:
        PyArrow Table containing the row group data

    This function imports the implementation from job2 at runtime,
    similar to how raster_to_h3 works.

    Example:
        table = await async_read_parquet_row_group(path, 0)
        df = table.to_pandas()
    """
    metadata_url = _get_metadata_url(base_url)

    try:
        from job2.fasttortoise import (
            async_read_parquet_row_group as _async_read_parquet_row_group,
        )

        return await _async_read_parquet_row_group(
            parquet_path=parquet_path,
            row_group_index=row_group_index,
            metadata_url=metadata_url,
            columns=columns,
        )
    except ImportError as e:
        raise RuntimeError(
            "The fasttortoise reconstruction functionality requires the job2 module. "
            "This is typically only available in the Fused execution environment."
        ) from e


async def async_fetch_row_group_metadata(
    parquet_path: str,
    row_group_index: int,
    base_url: Optional[str] = None,
    session: Optional[Any] = None,
) -> Dict[str, Any]:
    """
    Fetch row group metadata and extract byte offset information.

    This fetches the metadata from the API and parses it to get the byte offsets
    needed for combined downloads.

    Args:
        parquet_path: S3 or HTTP path to parquet file
        row_group_index: Index of row group to read (0-based)
        base_url: Base URL for API. If None, uses current environment.
        session: Optional aiohttp ClientSession. If None, uses shared session.

    Returns:
        Dict with keys:
            - 'path': The parquet file path
            - 'row_group_index': The row group index
            - 'start_offset': Starting byte offset in the file
            - 'end_offset': Ending byte offset in the file (exclusive)
            - 'size': Size of the row group data in bytes
            - 'api_metadata': Full unwrapped metadata dict (for reconstruction)
    """
    metadata_url = _get_metadata_url(base_url)

    try:
        from job2.fasttortoise._reconstruction import (
            _parse_row_group_from_metadata,
            _unwrap_api_metadata,
        )
    except ImportError as e:
        raise RuntimeError(
            "The fasttortoise reconstruction functionality requires the job2 module. "
            "This is typically only available in the Fused execution environment."
        ) from e

    import aiohttp

    from fused import context
    from fused.core._realtime_ops import _realtime_raise_for_status_async

    # Get authentication headers from the execution context
    auth_headers = context._get_auth_header(missing_ok=True)

    params = {"path": parquet_path, "row_group_index": row_group_index}

    # Use provided session or fall back to shared session
    if session is None:
        from fused.core._realtime_ops import _get_shared_session

        session = await _get_shared_session()

    async with session.get(
        url=metadata_url,
        params=params,
        headers=auth_headers,
        timeout=aiohttp.ClientTimeout(total=OPTIONS.metadata_request_timeout),
    ) as response:
        await _realtime_raise_for_status_async(response)

        # Handle 202 status (metadata still being processed)
        if response.status == 202:
            error_msg = "Metadata is still being processed by the server"
            try:
                response_json = await response.json()
                if "message" in response_json:
                    error_msg = response_json["message"]
                elif "detail" in response_json:
                    error_msg = response_json["detail"]
            except Exception:
                pass
            raise RuntimeError(f"Metadata not ready: {error_msg}")

        api_response = await response.json()

    # Unwrap metadata
    metadata = _unwrap_api_metadata(api_response)

    # Extract byte offsets from the row group
    target_row_group, num_rows, start_offset, end_offset = (
        _parse_row_group_from_metadata(metadata)
    )

    return {
        "path": parquet_path,
        "row_group_index": row_group_index,
        "start_offset": start_offset,
        "end_offset": end_offset,
        "size": end_offset - start_offset,
        "api_metadata": metadata,
    }


async def async_fetch_row_group_metadata_batch(
    requests: List[Dict[str, Any]],
    base_url: Optional[str] = None,
    session: Optional[Any] = None,
) -> List[Dict[str, Any]]:
    """
    Fetch metadata for multiple row groups in a single API call.

    This reduces API overhead by batching multiple requests together.
    The batch size is controlled by the metadata_batch_size parameter in read_hex_table.

    Args:
        requests: List of dicts with 'path' and 'row_group_index' keys
        base_url: Base URL for API. If None, uses current environment.
        session: Optional aiohttp ClientSession. If None, uses shared session.

    Returns:
        List of metadata dicts (same format as async_fetch_row_group_metadata)
        in the same order as input requests.

    Raises:
        RuntimeError: If the batch request fails or metadata is still being processed
    """
    metadata_url = _get_metadata_url(base_url)
    batch_url = f"{metadata_url}/batch"

    try:
        from job2.fasttortoise._reconstruction import (
            _parse_row_group_from_metadata,
            _unwrap_api_metadata,
        )
    except ImportError as e:
        raise RuntimeError(
            "The fasttortoise reconstruction functionality requires the job2 module."
        ) from e

    import aiohttp

    from fused import context
    from fused.core._realtime_ops import _realtime_raise_for_status_async

    auth_headers = context._get_auth_header(missing_ok=True)

    if session is None:
        from fused.core._realtime_ops import _get_shared_session

        session = await _get_shared_session()

    async with session.post(
        url=batch_url,
        json=requests,
        headers=auth_headers,
        timeout=aiohttp.ClientTimeout(total=OPTIONS.metadata_request_timeout),
    ) as response:
        await _realtime_raise_for_status_async(response)

        if response.status == 202:
            raise RuntimeError("Metadata is still being processed by the server")

        batch_response = await response.json()
        results = batch_response.get("results", [])

    # Process results and convert to same format as individual calls
    processed_results = []
    for i, result in enumerate(results):
        if "error" in result:
            # Propagate error
            error = result["error"]
            raise RuntimeError(
                f"Metadata fetch failed for row group {requests[i]['row_group_index']} "
                f"in {requests[i]['path']}: {error.get('detail', 'Unknown error')}"
            )

        # Unwrap and parse metadata (same as individual call)
        api_response = {
            "metadata": result.get("metadata", ""),
            "row_group_bytes": result.get("row_group_bytes", ""),
        }
        metadata = _unwrap_api_metadata(api_response)

        target_row_group, num_rows, start_offset, end_offset = (
            _parse_row_group_from_metadata(metadata)
        )

        processed_results.append(
            {
                "path": requests[i]["path"],
                "row_group_index": requests[i]["row_group_index"],
                "start_offset": start_offset,
                "end_offset": end_offset,
                "size": end_offset - start_offset,
                "api_metadata": metadata,
            }
        )

    return processed_results


async def async_read_combined_row_groups(
    path: str,
    row_group_metadata_list: List[Dict[str, Any]],
    base_url: Optional[str] = None,
    columns: Optional[List[str]] = None,
) -> List[Any]:
    """
    Read multiple consecutive row groups with a single combined download.

    Downloads the byte range spanning all row groups in one request,
    then reconstructs each row group's table from the combined data.

    Args:
        path: S3 or HTTP path to parquet file
        row_group_metadata_list: List of metadata dicts from async_fetch_row_group_metadata
                                 (must be consecutive row groups from the same file)
        base_url: Base URL for API. If None, uses current environment.
        columns: Optional list of column names to read

    Returns:
        List of PyArrow Tables, one per row group in the same order as input
    """
    import pyarrow.parquet as pq

    if not row_group_metadata_list:
        return []

    try:
        from job2.fasttortoise._reconstruction import (
            _async_read_file_range,
            _build_parquet_buffer_from_data,
            _parse_row_group_from_metadata,
        )
    except ImportError as e:
        raise RuntimeError(
            "The fasttortoise reconstruction functionality requires the job2 module. "
            "This is typically only available in the Fused execution environment."
        ) from e

    # Calculate the combined byte range
    start_offset = min(rg["start_offset"] for rg in row_group_metadata_list)
    end_offset = max(rg["end_offset"] for rg in row_group_metadata_list)
    data_size = end_offset - start_offset

    # Download the combined byte range
    combined_data = await _async_read_file_range(path, start_offset, data_size)

    # Reconstruct each row group from the combined data
    tables = []
    for rg_meta in row_group_metadata_list:
        metadata = rg_meta["api_metadata"]

        # Parse the row group metadata again to get the thrift object
        target_row_group, num_rows, rg_start, rg_end = _parse_row_group_from_metadata(
            metadata
        )

        # Extract this row group's data from the combined buffer
        # The offset is relative to our combined download start
        relative_start = rg_start - start_offset
        relative_end = rg_end - start_offset
        row_group_data = combined_data[relative_start:relative_end]

        # Build the minimal parquet file
        parquet_buffer = _build_parquet_buffer_from_data(
            row_group_data,
            target_row_group,
            metadata,
            rg_start,
            num_rows,
        )

        try:
            # Parse with PyArrow
            parquet_file = pq.ParquetFile(parquet_buffer)
            table = parquet_file.read_row_group(0, columns=columns)
            tables.append(table)
        finally:
            parquet_buffer.close()

    return tables


__all__ = [
    "async_fetch_row_group_metadata",
    "async_fetch_row_group_metadata_batch",
    "async_read_combined_row_groups",
    "async_read_parquet_row_group",
    "find_dataset",
    "get_row_groups_for_dataset",
    "get_row_groups_for_dataset_with_metadata",
    "read_parquet_row_group",
    "register_dataset",
]
