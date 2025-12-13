"""API client helpers for dataset queries."""

from typing import Any, Dict, List, Optional

from fused import context
from fused._global_api import get_api
from fused._options import options as OPTIONS
from fused._request import session_with_retries


def register_dataset(
    dataset_path: str,
    base_url: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Register a dataset for indexed queries.

    This function registers a directory in your file storage as a dataset,
    enabling fast geospatial queries using H3 indexing.

    Args:
        dataset_path: Path to the dataset directory. The path should point to
                     a directory containing parquet files.
        base_url: Base URL for API. If None, uses current environment.

    Returns:
        Dictionary with registration results:
            - dataset_id: ID of the created/updated dataset
            - location: Normalized URL of the dataset
            - visit_status: Status of the dataset visit (success/timeout/error)
            - items_discovered: Total number of items found
            - new_items: Number of new items added

    Raises:
        requests.HTTPError: If the API request fails

    Example:
        # Register a dataset from your storage
        result = fused.register_dataset("s3://my-bucket/my-data/buildings/")
        print(f"Registered dataset with ID: {result['dataset_id']}")
        print(f"Found {result['items_discovered']} files")

    Note:
        - Regular users can use any storage paths they have access to
        - Datasets are registered as private (only accessible to your team)
        - Files are automatically queued for metadata extraction
    """

    # Use current environment's base URL if not specified
    if base_url is None:
        base_url = OPTIONS.base_url

    # Build query parameters
    params: Dict[str, Any] = {
        "url": dataset_path,
    }

    # Make API request with auth headers
    url = f"{base_url}/datasets/register-from-url"
    with session_with_retries() as session:
        response = session.post(
            url,
            params=params,
            headers=get_api()._generate_headers(),
            timeout=OPTIONS.request_timeout,
        )
        response.raise_for_status()

    return response.json()


def find_dataset(
    location: str,
    base_url: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Find the dataset that contains a specific location URL.

    Uses hierarchical prefix matching: if the exact path isn't registered,
    searches progressively shorter prefixes to find the containing dataset.

    Args:
        location: Full URL to search for (s3://, gs://, http://, etc.).
                 Can be a file, partition, or directory path.
        base_url: Base URL for API. If None, uses current environment.

    Returns:
        Dataset dict with keys: id, location, description, storage_type,
        owner, public, created_at, updated_at, etc.

    Raises:
        requests.HTTPError: If dataset not found (404) or request fails

    Example:
        # Find dataset containing a file
        dataset = fused.find_dataset("s3://bucket/data/year=2024/file.parquet")
        print(f"Found dataset: {dataset['location']}")
    """
    # Use current environment's base URL if not specified
    if base_url is None:
        base_url = OPTIONS.base_url

    # Build query parameters
    params: Dict[str, Any] = {
        "location": location,
    }

    # Make API request with auth headers from execution context
    url = f"{base_url}/datasets/find-by-location"
    with session_with_retries() as session:
        response = session.get(
            url,
            params=params,
            headers=context._get_auth_header(missing_ok=True),
            timeout=OPTIONS.request_timeout,
        )
        response.raise_for_status()

    return response.json()


def get_row_groups_for_dataset(
    dataset_path: str,
    geographical_regions: List[Dict[str, str]],
    h3_resolution: Optional[int] = None,
    base_url: Optional[str] = None,
    include_signed_urls: bool = False,
) -> List[Dict[str, Any]]:
    """
    Query dataset to find files and row groups for given H3 spatial ranges.

    Args:
        dataset_path: S3 path to dataset (e.g., "s3://bucket/dataset/"). Can include
                     subdirectories to filter results (e.g., "s3://bucket/dataset/year=2024/").
        geographical_regions: List of H3 ranges like [{"min": "8928...", "max": "8928..."}]
        h3_resolution: Optional H3 resolution level to filter results. If provided,
                      only items with that resolution are returned (optimization).
                      If not provided, returns row groups from all resolutions.
        base_url: Base URL for API (e.g., "https://www.fused.io/server/v1"). If None, uses current environment.
        include_signed_urls: If True, include presigned URLs for accessing files (valid for 1 hour).

    Returns:
        List of dicts with 'path', 'row_group_index', and optionally 'signed_url' keys

    Example:
        regions = [{"min": "8928308280fffff", "max": "89283082a1bffff"}]
        items = get_row_groups_for_dataset(
            "s3://my-bucket/my-dataset/",
            regions,
        )
        # Returns: [
        #   {"path": "s3://my-bucket/my-dataset/file1.parquet", "row_group_index": 0},
        #   {"path": "s3://my-bucket/my-dataset/file1.parquet", "row_group_index": 3},
        #   {"path": "s3://my-bucket/my-dataset/file2.parquet", "row_group_index": 1},
        # ]

        # With signed URLs
        items = get_row_groups_for_dataset(
            "s3://my-bucket/my-dataset/",
            regions,
            include_signed_urls=True
        )
        # Returns: [
        #   {
        #       "path": "s3://my-bucket/my-dataset/file1.parquet",
        #       "row_group_index": 0,
        #       "signed_url": "https://s3.amazonaws.com/bucket/file.parquet?..."
        #   },
        #   ...
        # ]
    """
    # Use current environment's base URL if not specified
    if base_url is None:
        base_url = OPTIONS.base_url

    # Build request body for POST
    body: Dict[str, Any] = {
        "dataset_path": dataset_path,
        "geographical_regions": geographical_regions,
        "include_signed_urls": include_signed_urls,
    }

    if h3_resolution is not None:
        body["h3_resolution"] = h3_resolution

    # Make API request with auth headers from execution context
    url = f"{base_url}/datasets/items"
    with session_with_retries() as session:
        response = session.post(
            url,
            json=body,
            headers=context._get_auth_header(missing_ok=True),
        )
        response.raise_for_status()

    # Parse response
    data = response.json()
    items = data.get("items", [])

    # Flatten into list of {path, row_group_index, signed_url?} dicts
    result = []
    for item in items:
        relative_path = item.get("relative_path", "")
        row_groups = item.get("row_groups", [])
        signed_url = item.get("signed_url")

        # Construct full path - handle empty relative_path to avoid trailing slash
        if relative_path:
            full_path = dataset_path.rstrip("/") + "/" + relative_path.lstrip("/")
        else:
            full_path = dataset_path.rstrip("/")

        # Add each row group
        for rg_index in row_groups:
            row_group_dict = {"path": full_path, "row_group_index": rg_index}
            # Include signed URL if available
            if signed_url:
                row_group_dict["signed_url"] = signed_url
            result.append(row_group_dict)

    return result


def get_row_groups_for_dataset_with_metadata(
    dataset_path: str,
    geographical_regions: List[Dict[str, str]],
    h3_resolution: Optional[int] = None,
    base_url: Optional[str] = None,
    include_signed_urls: bool = False,
    include_full_metadata: bool = True,
) -> List[Dict[str, Any]]:
    """
    Query dataset to find files and row groups with metadata (offsets and optionally full metadata).

    This is an optimized version that returns byte offsets (and optionally full reconstruction
    metadata) in a single call, eliminating the need for separate metadata batch API calls.

    Args:
        dataset_path: S3 path to dataset (e.g., "s3://bucket/dataset/"). Can include
                     subdirectories to filter results (e.g., "s3://bucket/dataset/year=2024/").
        geographical_regions: List of H3 ranges like [{"min": "8928...", "max": "8928..."}]
        h3_resolution: Optional H3 resolution level to filter results. If provided,
                      only items with that resolution are returned (optimization).
                      If not provided, returns row groups from all resolutions.
        base_url: Base URL for API (e.g., "https://www.fused.io/server/v1"). If None, uses current environment.
        include_signed_urls: If True, include presigned URLs for accessing files (valid for 1 hour).
        include_full_metadata: If True, include metadata_json and row_group_bytes for reconstruction.
                              If False, only include offsets (allows earlier S3 downloads).

    Returns:
        List of dicts with 'path', 'row_group_index', 'start_offset', 'end_offset', and optionally
        'metadata_json' and 'row_group_bytes' keys

    Example:
        regions = [{"min": "8928308280fffff", "max": "89283082a1bffff"}]
        items = get_row_groups_for_dataset_with_metadata(
            "s3://my-bucket/my-dataset/",
            regions,
            include_full_metadata=True
        )
        # Returns: [
        #   {
        #       "path": "s3://my-bucket/my-dataset/file1.parquet",
        #       "row_group_index": 0,
        #       "start_offset": 1234,
        #       "end_offset": 5678,
        #       "metadata_json": "...",
        #       "row_group_bytes": "..."
        #   },
        #   ...
        # ]
    """
    # Use current environment's base URL if not specified
    if base_url is None:
        base_url = OPTIONS.base_url

    # Build request body for POST
    body: Dict[str, Any] = {
        "dataset_path": dataset_path,
        "geographical_regions": geographical_regions,
        "include_signed_urls": include_signed_urls,
        "include_full_metadata": include_full_metadata,
    }

    if h3_resolution is not None:
        body["h3_resolution"] = h3_resolution

    # Make API request with auth headers from execution context
    url = f"{base_url}/datasets/items-with-metadata"
    with session_with_retries() as session:
        response = session.post(
            url,
            json=body,
            headers=context._get_auth_header(missing_ok=True),
        )
        response.raise_for_status()

    # Parse response
    data = response.json()
    items = data.get("items", [])

    # Flatten into list of {path, row_group_index, start_offset, end_offset, ...} dicts
    result = []
    for item in items:
        relative_path = item.get("relative_path", "")
        row_groups = item.get("row_groups", [])
        signed_url = item.get("signed_url")

        # Construct full path - handle empty relative_path to avoid trailing slash
        if relative_path:
            full_path = dataset_path.rstrip("/") + "/" + relative_path.lstrip("/")
        else:
            full_path = dataset_path.rstrip("/")

        # Add each row group with its metadata
        for rg in row_groups:
            row_group_dict = {
                "path": full_path,
                "row_group_index": rg.get("row_group_index"),
                "start_offset": rg.get("start_offset"),
                "end_offset": rg.get("end_offset"),
            }
            # Include signed URL if available
            if signed_url:
                row_group_dict["signed_url"] = signed_url
            # Include full metadata if present
            if "metadata_json" in rg:
                row_group_dict["metadata_json"] = rg.get("metadata_json")
            if "row_group_bytes" in rg:
                row_group_dict["row_group_bytes"] = rg.get("row_group_bytes")
            result.append(row_group_dict)

    return result
