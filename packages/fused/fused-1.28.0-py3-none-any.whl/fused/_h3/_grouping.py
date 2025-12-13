"""Size-based grouping logic for row group downloads."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class RowGroupMetadata:
    """Metadata for a single row group with byte offset information.

    Attributes:
        path: File path (S3 or HTTP URL)
        row_group_index: Index of the row group in the file (0-based)
        start_offset: Starting byte offset in the file
        end_offset: Ending byte offset in the file (exclusive)
        size: Size of the row group data in bytes (end_offset - start_offset)
        api_metadata: Full metadata dict from API (needed for reconstruction)
    """

    path: str
    row_group_index: int
    start_offset: int
    end_offset: int
    api_metadata: Dict[str, Any]

    @property
    def size(self) -> int:
        """Size of the row group data in bytes."""
        return self.end_offset - self.start_offset


@dataclass
class DownloadGroup:
    """A group of consecutive row groups from the same file to download together.

    Attributes:
        path: File path (S3 or HTTP URL)
        row_groups: List of RowGroupMetadata objects (must be consecutive indices)
        start_offset: Starting byte offset for the combined download
        end_offset: Ending byte offset for the combined download (exclusive)
        total_size: Total size of all row groups in this group
    """

    path: str
    row_groups: List[RowGroupMetadata] = field(default_factory=list)

    @property
    def start_offset(self) -> int:
        """Starting byte offset for the combined download."""
        if not self.row_groups:
            return 0
        return min(rg.start_offset for rg in self.row_groups)

    @property
    def end_offset(self) -> int:
        """Ending byte offset for the combined download (exclusive)."""
        if not self.row_groups:
            return 0
        return max(rg.end_offset for rg in self.row_groups)

    @property
    def total_size(self) -> int:
        """Total size of all row groups in this group."""
        return self.end_offset - self.start_offset

    @property
    def row_group_indices(self) -> List[int]:
        """List of row group indices in this group."""
        return [rg.row_group_index for rg in self.row_groups]

    def add_row_group(self, rg: RowGroupMetadata) -> None:
        """Add a row group to this download group.

        Args:
            rg: RowGroupMetadata to add

        Raises:
            ValueError: If row group is from a different file or not consecutive
        """
        if rg.path != self.path:
            raise ValueError(
                f"Cannot add row group from {rg.path} to group for {self.path}"
            )
        if self.row_groups:
            last_index = self.row_groups[-1].row_group_index
            if rg.row_group_index != last_index + 1:
                raise ValueError(
                    f"Row group {rg.row_group_index} is not consecutive with "
                    f"last index {last_index}"
                )
        self.row_groups.append(rg)


def group_row_groups_by_file(
    row_group_items: List[Dict[str, Any]],
) -> Dict[str, List[int]]:
    """Group row group items by file path.

    Args:
        row_group_items: List of dicts with 'path' and 'row_group_index' keys

    Returns:
        Dict mapping file path to list of row group indices (sorted)
    """
    by_file: Dict[str, List[int]] = {}
    for item in row_group_items:
        path = item["path"]
        rg_index = item["row_group_index"]
        if path not in by_file:
            by_file[path] = []
        by_file[path].append(rg_index)

    # Sort indices for each file
    for path in by_file:
        by_file[path].sort()

    return by_file


def find_consecutive_runs(indices: List[int]) -> List[List[int]]:
    """Find runs of consecutive integers in a sorted list.

    Args:
        indices: Sorted list of integers

    Returns:
        List of lists, where each inner list contains consecutive integers.

    Examples:
        >>> find_consecutive_runs([0, 1, 2, 3])
        [[0, 1, 2, 3]]
        >>> find_consecutive_runs([0, 2, 4, 6])
        [[0], [2], [4], [6]]
        >>> find_consecutive_runs([0, 1, 5, 6, 7, 10])
        [[0, 1], [5, 6, 7], [10]]
        >>> find_consecutive_runs([])
        []
        >>> find_consecutive_runs([5])
        [[5]]
    """
    if not indices:
        return []

    runs: List[List[int]] = [[indices[0]]]

    for idx in indices[1:]:
        if idx == runs[-1][-1] + 1:
            # Consecutive - extend current run
            runs[-1].append(idx)
        else:
            # Gap - start new run
            runs.append([idx])

    return runs


def create_size_based_groups(
    row_group_metadata: List[RowGroupMetadata],
    target_size: int,
) -> List[DownloadGroup]:
    """Create download groups from row group metadata based on cumulative size.

    Groups consecutive row groups until the cumulative size reaches the target.
    Row groups that are already larger than the target stay as single groups.
    Gaps in row group indices force new groups.

    Args:
        row_group_metadata: List of RowGroupMetadata (should be from the same file
                           and sorted by row_group_index)
        target_size: Target size in bytes for each group

    Returns:
        List of DownloadGroup objects

    Examples:
        With 3 row groups of sizes [10KB, 15KB, 20KB] and target 32KB:
        - Group 1: [rg0, rg1] = 25KB (adding rg2 would exceed 32KB)
        - Group 2: [rg2] = 20KB
    """
    if not row_group_metadata:
        return []

    # All metadata should be for the same file
    path = row_group_metadata[0].path

    # Sort by row group index
    sorted_metadata = sorted(row_group_metadata, key=lambda rg: rg.row_group_index)

    groups: List[DownloadGroup] = []
    current_group: Optional[DownloadGroup] = None

    for rg in sorted_metadata:
        # Check if we need to start a new group
        start_new_group = False

        if current_group is None:
            start_new_group = True
        elif current_group.row_groups:
            last_index = current_group.row_groups[-1].row_group_index
            # Non-consecutive indices force a new group
            if rg.row_group_index != last_index + 1:
                start_new_group = True
            # Check if adding this row group would exceed the target
            # We want batches to stay under the target size
            elif current_group.total_size + rg.size > target_size:
                start_new_group = True

        if start_new_group:
            if current_group is not None and current_group.row_groups:
                groups.append(current_group)
            current_group = DownloadGroup(path=path)

        current_group.add_row_group(rg)

    # Don't forget the last group
    if current_group is not None and current_group.row_groups:
        groups.append(current_group)

    return groups


def create_download_groups_from_metadata(
    metadata_by_file: Dict[str, List[RowGroupMetadata]],
    target_size: int,
) -> List[DownloadGroup]:
    """Create download groups from all files based on cumulative size.

    Args:
        metadata_by_file: Dict mapping file path to list of RowGroupMetadata
        target_size: Target size in bytes for each group

    Returns:
        List of DownloadGroup objects from all files
    """
    all_groups: List[DownloadGroup] = []

    for path, metadata_list in metadata_by_file.items():
        groups = create_size_based_groups(metadata_list, target_size)
        all_groups.extend(groups)

    return all_groups
