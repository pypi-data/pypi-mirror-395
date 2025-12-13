from __future__ import annotations

import fsspec


def ls_or_empty(fs: fsspec.AbstractFileSystem, path, **kwargs):
    """Calls fs.ls, working around a change in the fsspec implementation,
    where listing non-existant paths throws."""
    try:
        return fs.ls(path, **kwargs)
    except FileNotFoundError:
        return []


def is_empty_dir(fs: fsspec.AbstractFileSystem, path, **kwargs):
    """Checks if a directory is empty, dealing with S3 peculiarities."""
    contents = ls_or_empty(fs, path, **kwargs)
    if len(contents) > 1:
        return False
    if len(contents) == 1:
        # a single file with the name of the path as a dir placeholder
        # considered as a directory by info()
        try:
            return contents[0] in path and fs.info(contents[0])["type"] == "directory"
        except Exception:
            return False
    return True


def is_non_empty_dir(url: str, fs: fsspec.AbstractFileSystem | None = None) -> bool:
    if fs is not None:
        fs.invalidate_cache()
        if fs.exists(url) and not is_empty_dir(fs, url, refresh=True):
            return True

    elif url.startswith("s3://"):
        import s3fs

        s3 = s3fs.S3FileSystem()
        s3.invalidate_cache()
        if s3.exists(url) and not is_empty_dir(s3, url, refresh=True):
            return True

    elif url.startswith("gs://"):
        import gcsfs

        gcs = gcsfs.GCSFileSystem()
        gcs.invalidate_cache()
        if gcs.exists(url) and not is_empty_dir(gcs, url, refresh=True):
            return True

    elif url.startswith("file:///"):
        from pathlib import Path

        path = Path(url.replace("file://", ""))

        if path.exists() and any(path.iterdir()):
            return True

    return False
