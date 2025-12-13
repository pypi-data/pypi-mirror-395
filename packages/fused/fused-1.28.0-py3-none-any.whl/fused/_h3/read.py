"""Read H3-indexed tables by hex ranges."""

from __future__ import annotations

import asyncio
import time
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from fused._fasttortoise import async_read_combined_row_groups
from fused._h3._grouping import (
    DownloadGroup,
    RowGroupMetadata,
    create_size_based_groups,
    group_row_groups_by_file,
)

if TYPE_CHECKING:
    import pyarrow as pa

# Check for nest_asyncio availability
try:
    import nest_asyncio

    HAS_NEST_ASYNCIO = True
except ImportError:
    HAS_NEST_ASYNCIO = False


def read_hex_table_slow(
    dataset_path: str,
    hex_ranges_list: List[List[int]],
    columns: Optional[List[str]] = None,
    base_url: Optional[str] = None,
    verbose: bool = False,
    return_timing_info: bool = False,
    metadata_batch_size: int = 50,
) -> "pa.Table" | tuple["pa.Table", Dict[str, Any]]:
    """
    Read data from an H3-indexed dataset by querying hex ranges.

    This function queries the dataset index for row groups that match the given
    H3 hex ranges, downloads them in parallel with optimized batching, and returns
    a concatenated table.

    Adjacent row groups from the same file are combined into single downloads
    for better S3 performance. The batch size is controlled by
    `fused.options.row_group_batch_size` (default: 32KB).

    Args:
        dataset_path: Path to the H3-indexed dataset (e.g., "s3://bucket/dataset/")
        hex_ranges_list: List of [min_hex, max_hex] pairs as integers.
            Example: [[622236719905341439, 622246719905341439]]
        columns: Optional list of column names to read. If None, reads all columns.
        base_url: Base URL for API. If None, uses current environment.
        verbose: If True, print progress information. Default is False.
        return_timing_info: If True, return a tuple of (table, timing_info) instead of just the table.
            Default is False for backward compatibility.
        metadata_batch_size: Maximum number of row group metadata requests to batch together
            in a single API call. Larger batches reduce API overhead. Default is 50.
            Consider MongoDB's 16KB document limit when adjusting this value.

    Returns:
        PyArrow Table containing the concatenated data from all matching row groups.
        If return_timing_info is True, returns a tuple of (table, timing_info dict).

    Example:
        import fused

        # Read data for a specific H3 hex range
        table = fused.h3.read_hex_table_slow(
            dataset_path="s3://my-bucket/my-h3-dataset/",
            hex_ranges_list=[[622236719905341439, 622246719905341439]]
        )
        df = table.to_pandas()
    """
    import pyarrow as pa

    from fused._fasttortoise._api import get_row_groups_for_dataset
    from fused._options import options as OPTIONS

    # Use current environment's base URL if not specified
    if base_url is None:
        base_url = OPTIONS.base_url

    if not hex_ranges_list:
        return pa.table({})

    # Convert integer hex ranges to the format expected by get_row_groups_for_dataset
    geographical_regions = []
    for hex_range in hex_ranges_list:
        if len(hex_range) != 2:
            raise ValueError(
                f"Each hex range must be a list of [min, max], got {hex_range}"
            )
        min_hex, max_hex = hex_range
        geographical_regions.append({"min": f"{min_hex:x}", "max": f"{max_hex:x}"})

    # Query the dataset index to find matching row groups
    t0 = time.perf_counter()
    row_groups = get_row_groups_for_dataset(
        dataset_path=dataset_path,
        geographical_regions=geographical_regions,
        base_url=base_url,
    )
    t_api = time.perf_counter()

    if verbose:
        print(f"  API query: {(t_api - t0) * 1000:.1f}ms")
        print(f"  Found {len(row_groups)} row groups matching geo query")

    if not row_groups:
        # No matching row groups for the given hex ranges
        # This is normal - just return an empty table
        return pa.table({})

    # Get the batch size from options
    batch_size = OPTIONS.row_group_batch_size

    if verbose:
        print(f"  Using batch size: {batch_size} bytes")
        print(f"  Using metadata batch size: {metadata_batch_size}")

    # Run the pipelined fetch and download
    tables, timing_info = _run_async(
        _fetch_with_combining(
            row_groups, base_url, columns, batch_size, verbose, metadata_batch_size
        )
    )
    t_fetch = time.perf_counter()

    if verbose:
        print(f"  Metadata + download: {(t_fetch - t_api) * 1000:.1f}ms")
        if timing_info:
            print(
                f"    Metadata fetch: {timing_info.get('metadata_wall_ms', 0):.1f}ms wall-clock, "
                f"{timing_info.get('metadata_ms', 0):.1f}ms cumulative"
            )
            print(
                f"      Longest metadata fetch: {timing_info.get('longest_metadata_fetch_ms', 0):.1f}ms"
            )
            print(
                f"    Data download: {timing_info.get('download_wall_ms', 0):.1f}ms wall-clock, "
                f"{timing_info.get('download_ms', 0):.1f}ms cumulative"
            )
            print(
                f"      Longest download: {timing_info.get('longest_download_ms', 0):.1f}ms"
            )
            print(f"    Download groups: {timing_info.get('num_groups', 0)}")

    # Concatenate all tables into one
    if not tables:
        return pa.table({})
    if len(tables) == 1:
        return tables[0]

    t_concat_start = time.perf_counter()
    # Use promote_options to handle schema mismatches (e.g., float vs double)
    # "permissive" allows type promotion like float->double
    result = pa.concat_tables(tables, promote_options="permissive")
    t_concat = time.perf_counter()

    if verbose:
        print(f"  Concat tables: {(t_concat - t_concat_start) * 1000:.1f}ms")

    if return_timing_info:
        return result, timing_info
    return result


def _run_async(coro):
    """Run an async coroutine, handling existing event loops."""

    async def _run_with_cleanup():
        """Run coroutine and clean up shared S3 client afterwards.

        Only cleans up when we own the event loop (not when nested via nest_asyncio).
        Note: We no longer clean up the aiohttp session here because _fetch_with_combining
        creates and manages its own session.
        """
        try:
            return await coro
        finally:
            # Clean up shared S3 client (job2) to prevent "Unclosed" warnings
            # This is safe because we own this event loop
            try:
                import asyncio

                from job2.fasttortoise._reconstruction import (
                    _async_s3_client_loop,
                    _shared_async_s3_client,
                )

                # Only clean up if the client belongs to this event loop
                current_loop = asyncio.get_running_loop()
                if (
                    _shared_async_s3_client is not None
                    and _async_s3_client_loop is current_loop
                ):
                    await _shared_async_s3_client.__aexit__(None, None, None)
            except Exception:
                pass

    # Handle running inside an existing event loop (e.g., Jupyter, UDF runner)
    try:
        asyncio.get_running_loop()
        # We're inside an event loop - apply nest_asyncio if available
        if HAS_NEST_ASYNCIO:
            nest_asyncio.apply()
            # DON'T clean up here - the outer loop owns the session
            return asyncio.run(coro)
        else:
            # Fallback: create a new thread to run the async code
            # Clean up since we own this isolated event loop
            import concurrent.futures

            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(asyncio.run, _run_with_cleanup())
                return future.result()
    except RuntimeError:
        # No event loop running - use asyncio.run directly
        # Clean up since we own this event loop
        return asyncio.run(_run_with_cleanup())


def read_hex_table(
    dataset_path: str,
    hex_ranges_list: List[List[int]],
    columns: Optional[List[str]] = None,
    base_url: Optional[str] = None,
    verbose: bool = False,
    return_timing_info: bool = False,
    batch_size: Optional[int] = None,
    max_concurrent_downloads: Optional[int] = None,
) -> "pa.Table" | tuple["pa.Table", Dict[str, Any]]:
    """
    Read data from an H3-indexed dataset by querying hex ranges.

    This is an optimized version that assumes the server always provides full metadata
    (start_offset, end_offset, metadata_json, and row_group_bytes) for all row groups.
    If any row group is missing required metadata, this function will raise an error
    indicating that the dataset needs to be re-indexed.

    This function eliminates all metadata API calls by using prefetched metadata from
    the /datasets/items-with-metadata endpoint.

    This function imports the implementation from job2 at runtime,
    similar to how read_parquet_row_group works.

    Args:
        dataset_path: Path to the H3-indexed dataset (e.g., "s3://bucket/dataset/")
        hex_ranges_list: List of [min_hex, max_hex] pairs as integers.
            Example: [[622236719905341439, 622246719905341439]]
        columns: Optional list of column names to read. If None, reads all columns.
        base_url: Base URL for API. If None, uses current environment.
        verbose: If True, print progress information. Default is False.
        return_timing_info: If True, return a tuple of (table, timing_info) instead of just the table.
            Default is False for backward compatibility.
        batch_size: Target size in bytes for combining row groups. If None, uses
            `fused.options.row_group_batch_size` (default: 32KB).
        max_concurrent_downloads: Maximum number of simultaneous download operations. If None,
            uses a default based on the number of files. Default is None.

    Returns:
        PyArrow Table containing the concatenated data from all matching row groups.
        If return_timing_info is True, returns a tuple of (table, timing_info dict).

    Raises:
        ValueError: If any row group is missing required metadata (start_offset, end_offset,
            metadata_json, or row_group_bytes). This indicates the dataset needs to be re-indexed.

    Example:
        import fused

        # Read data for a specific H3 hex range
        table = fused.h3.read_hex_table(
            dataset_path="s3://my-bucket/my-h3-dataset/",
            hex_ranges_list=[[622236719905341439, 622246719905341439]]
        )
        df = table.to_pandas()
    """
    try:
        from job2.fasttortoise import (
            read_hex_table as _read_hex_table,
        )
    except ImportError:
        raise ImportError(
            "read_hex_table requires job2. This function is only available "
            "in the Fused execution environment."
        ) from None

    return _read_hex_table(
        dataset_path=dataset_path,
        hex_ranges_list=hex_ranges_list,
        columns=columns,
        base_url=base_url,
        verbose=verbose,
        return_timing_info=return_timing_info,
        batch_size=batch_size,
        max_concurrent_downloads=max_concurrent_downloads,
    )


async def _fetch_with_combining(
    row_groups: List[Dict[str, Any]],
    base_url: str,
    columns: Optional[List[str]],
    batch_size: int,
    verbose: bool = False,
    metadata_batch_size: int = 50,
) -> tuple:
    """
    Fetch row groups with pipelined metadata fetch and combined downloads.

    This implements a producer-consumer pattern:
    1. Group row groups by file
    2. For each file, fetch metadata for all row groups in parallel (batched)
    3. As metadata arrives, form size-based download groups
    4. Download groups are processed as they become ready

    Args:
        row_groups: List of dicts with 'path' and 'row_group_index' keys
        base_url: Base URL for API
        columns: Optional list of column names to read
        batch_size: Target size in bytes for combining row groups
        verbose: If True, print progress information
        metadata_batch_size: Maximum number of row group metadata requests to batch together

    Returns:
        Tuple of (List of PyArrow Tables, timing_info dict)
    """
    import aiohttp

    from fused._h3._grouping import (
        find_consecutive_runs,
    )
    from fused._options import options as OPTIONS

    # Create our own aiohttp session for this operation
    # This ensures proper cleanup and doesn't interfere with shared sessions
    connector = aiohttp.TCPConnector(
        limit=100,  # Reasonable limit for concurrent requests
        ttl_dns_cache=300,
        use_dns_cache=True,
    )
    session = aiohttp.ClientSession(
        connector=connector,
        timeout=aiohttp.ClientTimeout(total=OPTIONS.request_timeout),
    )

    try:
        # Timing tracking - cumulative (sum of all operations)
        metadata_total_ms = 0.0
        download_total_ms = 0.0
        num_groups = 0

        # Wall-clock timing - first start to last end
        metadata_first_start: Optional[float] = None
        metadata_last_end: Optional[float] = None
        download_first_start: Optional[float] = None
        download_last_end: Optional[float] = None

        # Track longest individual operations
        longest_metadata_fetch_ms = 0.0
        longest_download_ms = 0.0

        # Group row groups by file path
        by_file = group_row_groups_by_file(row_groups)

        if verbose:
            print(f"  Row groups span {len(by_file)} files")

        # Queue for download groups ready to be fetched
        download_queue: asyncio.Queue[Optional[DownloadGroup]] = asyncio.Queue()

        # Results collection (protected by lock for thread safety)
        results: List["pa.Table"] = []
        results_lock = asyncio.Lock()

        # Track how many producers are still running
        num_producers = len(by_file)
        producers_done = asyncio.Event()

        # Track timing
        timing_lock = asyncio.Lock()

        async def metadata_producer(file_path: str, rg_indices: List[int]) -> None:
            """Fetch metadata for all row groups in a file and create download groups."""
            nonlocal num_producers, metadata_total_ms, num_groups
            nonlocal metadata_first_start, metadata_last_end, longest_metadata_fetch_ms

            try:
                # Find consecutive runs first
                runs = find_consecutive_runs(rg_indices)

                for run in runs:
                    # Batch metadata requests to reduce API overhead
                    for batch_start in range(0, len(run), metadata_batch_size):
                        batch_indices = run[
                            batch_start : batch_start + metadata_batch_size
                        ]

                        t_meta_start = time.perf_counter()

                        # Use batched API call
                        from fused._fasttortoise import (
                            async_fetch_row_group_metadata_batch,
                        )

                        batch_requests = [
                            {"path": file_path, "row_group_index": idx}
                            for idx in batch_indices
                        ]
                        metadata_results = await async_fetch_row_group_metadata_batch(
                            batch_requests, base_url=base_url, session=session
                        )

                        t_meta_end = time.perf_counter()

                        async with timing_lock:
                            metadata_fetch_ms = (t_meta_end - t_meta_start) * 1000
                            metadata_total_ms += metadata_fetch_ms
                            # Track longest individual metadata fetch
                            if metadata_fetch_ms > longest_metadata_fetch_ms:
                                longest_metadata_fetch_ms = metadata_fetch_ms
                            # Track wall-clock: first start to last end
                            if (
                                metadata_first_start is None
                                or t_meta_start < metadata_first_start
                            ):
                                metadata_first_start = t_meta_start
                            if (
                                metadata_last_end is None
                                or t_meta_end > metadata_last_end
                            ):
                                metadata_last_end = t_meta_end

                        # Convert to RowGroupMetadata objects
                        rg_metadata_list = [
                            RowGroupMetadata(
                                path=m["path"],
                                row_group_index=m["row_group_index"],
                                start_offset=m["start_offset"],
                                end_offset=m["end_offset"],
                                api_metadata=m["api_metadata"],
                            )
                            for m in metadata_results
                        ]

                        # Create size-based groups from this batch
                        groups = create_size_based_groups(rg_metadata_list, batch_size)

                        async with timing_lock:
                            num_groups += len(groups)

                        # Enqueue each group for download
                        for group in groups:
                            await download_queue.put(group)

            finally:
                # Mark this producer as done
                num_producers -= 1
                if num_producers == 0:
                    producers_done.set()

        async def download_consumer() -> None:
            """Download groups from the queue as they become available."""
            nonlocal download_total_ms
            nonlocal download_first_start, download_last_end, longest_download_ms

            while True:
                # Wait for either a group or all producers to be done
                try:
                    # Use a timeout to periodically check if producers are done
                    group = await asyncio.wait_for(download_queue.get(), timeout=0.1)
                except asyncio.TimeoutError:
                    if producers_done.is_set() and download_queue.empty():
                        break
                    continue

                if group is None:
                    break

                # Download and reconstruct all row groups in this group
                metadata_list = [
                    {
                        "path": rg.path,
                        "row_group_index": rg.row_group_index,
                        "start_offset": rg.start_offset,
                        "end_offset": rg.end_offset,
                        "api_metadata": rg.api_metadata,
                    }
                    for rg in group.row_groups
                ]

                t_dl_start = time.perf_counter()
                tables = await async_read_combined_row_groups(
                    path=group.path,
                    row_group_metadata_list=metadata_list,
                    base_url=base_url,
                    columns=columns,
                )
                t_dl_end = time.perf_counter()

                async with timing_lock:
                    download_ms = (t_dl_end - t_dl_start) * 1000
                    download_total_ms += download_ms
                    # Track longest individual download
                    if download_ms > longest_download_ms:
                        longest_download_ms = download_ms
                    # Track wall-clock: first start to last end
                    if (
                        download_first_start is None
                        or t_dl_start < download_first_start
                    ):
                        download_first_start = t_dl_start
                    if download_last_end is None or t_dl_end > download_last_end:
                        download_last_end = t_dl_end

                async with results_lock:
                    results.extend(tables)

                download_queue.task_done()

        # Start all producers and a consumer
        producer_tasks = [
            asyncio.create_task(metadata_producer(path, indices))
            for path, indices in by_file.items()
        ]

        # Start multiple consumers for better parallelism
        num_consumers = min(len(by_file), 8)  # At most 8 concurrent downloads
        consumer_tasks = [
            asyncio.create_task(download_consumer()) for _ in range(num_consumers)
        ]

        # Wait for all producers to finish
        await asyncio.gather(*producer_tasks)

        # Wait for all items to be processed
        await download_queue.join()

        # Signal consumers to stop (they'll exit when queue is empty and producers done)
        # Cancel remaining consumer tasks
        for task in consumer_tasks:
            task.cancel()

        # Wait for consumers to finish (ignore cancellation errors)
        await asyncio.gather(*consumer_tasks, return_exceptions=True)

        # Calculate wall-clock times
        metadata_wall_ms = 0.0
        if metadata_first_start is not None and metadata_last_end is not None:
            metadata_wall_ms = (metadata_last_end - metadata_first_start) * 1000

        download_wall_ms = 0.0
        if download_first_start is not None and download_last_end is not None:
            download_wall_ms = (download_last_end - download_first_start) * 1000

        timing_info = {
            "metadata_ms": metadata_total_ms,  # Cumulative
            "metadata_wall_ms": metadata_wall_ms,  # Wall-clock (first to last)
            "longest_metadata_fetch_ms": longest_metadata_fetch_ms,  # Longest individual metadata fetch
            "download_ms": download_total_ms,  # Cumulative
            "download_wall_ms": download_wall_ms,  # Wall-clock (first to last)
            "longest_download_ms": longest_download_ms,  # Longest individual download
            "num_groups": num_groups,
        }

        return results, timing_info
    finally:
        # Always close our session to prevent "Unclosed" warnings
        if not session.closed:
            await session.close()
