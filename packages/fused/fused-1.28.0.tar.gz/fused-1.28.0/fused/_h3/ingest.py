import uuid

import fused
from fused.core._fs_utils import is_non_empty_dir


@fused.udf(cache_max_age=0)
def udf_extract(
    src_path: str,
    chunk_id: int,
    x_chunks: int,
    y_chunks: int,
    tmp_path: str,
    res: int,
    k_ring: int,
    res_offset: int,
    file_res: int,
    chunk_name: str | None = None,
):
    # define UDF that imports the helper function inside the UDF
    from job2.partition.raster_to_h3 import udf_extract as run_udf_extract

    run_udf_extract(
        src_path,
        chunk_id,
        x_chunks,
        y_chunks,
        tmp_path,
        res=res,
        k_ring=k_ring,
        res_offset=res_offset,
        file_res=file_res,
        chunk_name=chunk_name,
    )


def run_extract(
    submit_params: list[dict],
    tmp_path: str,
    res: int = 11,
    k_ring: int = 1,
    res_offset: int = 1,
    file_res: int = 2,
    **kwargs,
):
    params = {
        "tmp_path": tmp_path,
        "res": res,
        "k_ring": k_ring,
        "res_offset": res_offset,
        "file_res": file_res,
    }

    pool = fused.submit(udf_extract, submit_params, **params, collect=False, **kwargs)
    return pool


@fused.udf(cache_max_age=0)
def udf_partition(
    file_id: int,
    tmp_path: str,
    output_path: str,
    metrics: list[str],
    groupby_cols: list[str] = ["hex", "data"],
    window_cols: list[str] = ["hex"],
    additional_cols: list[str] = [],
    chunk_res: int = 3,
    overview_res: list = [3, 4, 5, 6],
    max_rows_per_chunk: int = 0,
    include_source_url: bool = True,
):
    # define UDF that imports the helper function inside the UDF
    from job2.partition.raster_to_h3 import udf_partition as run_udf_partition

    run_udf_partition(
        file_id,
        tmp_path,
        output_path,
        metrics=metrics,
        groupby_cols=groupby_cols,
        window_cols=window_cols,
        additional_cols=additional_cols,
        chunk_res=chunk_res,
        overview_res=overview_res,
        max_rows_per_chunk=max_rows_per_chunk,
        include_source_url=include_source_url,
    )


def run_partition(
    tmp_path: str,
    file_ids: list[str],
    output_path: str,
    metrics: list[str] = ["cnt"],
    groupby_cols: list[str] = ["hex", "data"],
    window_cols: list[str] = ["hex"],
    additional_cols: list[str] = [],
    chunk_res: int = 3,
    overview_res: list = [3, 4, 5, 6],
    max_rows_per_chunk: int = 0,
    include_source_url: bool = True,
    debug_mode: bool = False,
    **kwargs,
):
    """
    Combine chunks per file_id H3 cell and recalculate data.

    Parameters
    ----------
    tmp_path : str
        Path where the intermediate files to combine are stored.
    output_path : str
        Path for the resulting Parquet dataset.
    chunk_res : int
        The H3 resolution to chunk the row groups within each file of the Parquet dataset
    overview_res : list of int
        The H3 resolutions for which to create overview files.

    """
    params = {
        "tmp_path": tmp_path,
        "output_path": output_path,
        #
        "metrics": metrics,
        "groupby_cols": groupby_cols,
        "window_cols": window_cols,
        "additional_cols": additional_cols,
        "chunk_res": chunk_res,
        "overview_res": overview_res,
        "max_rows_per_chunk": max_rows_per_chunk,
        "include_source_url": include_source_url,
    }
    submit_params = [{"file_id": i} for i in file_ids]

    if debug_mode:
        submit_params = submit_params[:2]

    pool = fused.submit(
        udf_partition,
        submit_params,
        **params,
        collect=False,
        **kwargs,
    )
    return pool


@fused.udf(cache_max_age=0)
def udf_overview(
    tmp_path: str, output_path: str, res: int, chunk_res: int, max_rows_per_chunk: int
):
    from job2.partition.raster_to_h3 import udf_overview as run_udf_overview

    return run_udf_overview(
        tmp_path,
        output_path,
        res=res,
        chunk_res=chunk_res,
        max_rows_per_chunk=max_rows_per_chunk,
    )


def run_overview(
    tmp_path: str,
    output_path: str,
    overview_res: list[int],
    overview_chunk_res: list[int],
    max_rows_per_chunk: int = 0,
    **kwargs,
):
    params = {
        "tmp_path": tmp_path,
        "output_path": output_path,
        "max_rows_per_chunk": max_rows_per_chunk,
    }
    submit_params = [
        {"res": res, "chunk_res": chunk_res}
        for res, chunk_res in zip(overview_res, overview_chunk_res)
    ]

    pool = fused.submit(
        udf_overview,
        submit_params,
        **params,
        collect=False,
        **kwargs,
    )
    return pool


def _submit_with_fallback(
    step: str, run_function, run_kwargs: dict, submit_kwargs: dict, update_callback=None
):
    if not (
        submit_kwargs.get("engine", None) == "local" or "instance_type" in submit_kwargs
    ):
        # default logic: try realtime and fallback to large instance
        submit_kwargs["instance_type"] = "realtime"
        result = run_function(
            **run_kwargs,
            **submit_kwargs,
        )
        result.wait()
        if not result.all_succeeded():
            errors = result.errors()
            error_msg = str(next(iter(errors.values())))
            error_msg = error_msg.removeprefix(
                "The UDF returned the following error:\n"
            )
            if "Out of Memory Error: failed to offload data block of size" in error_msg:
                # reduce verbosity of long duckdb OOM error
                error_msg = "Out of Memory Error (duckdb)"
            print(
                f"-- {step} step failed on realtime instances retrying failed runs "
                "on large instances\n"
                f"   ({len(errors)} out of {result.n_jobs} runs, first error: {error_msg})"
            )
            update_callback(run_kwargs, errors)
            submit_kwargs["instance_type"] = "large"
            result = run_function(
                **run_kwargs,
                **submit_kwargs,
            )
    else:
        # otherwise run once with user provided configuration
        result = run_function(
            **run_kwargs,
            **submit_kwargs,
        )
    return result


def _print_batch_jobs(result):
    if isinstance(result, fused._submit.BatchJobPool):
        print(f"-- started {len(result._jobs)} instances:")
        for job in result._jobs:
            print(f"   - {job.logs_url}")


def _create_tmp_path(src_path: str, output_path: str) -> str:
    cache_id = uuid.uuid4().hex[:10]
    src_path_part = (
        src_path.replace("/", "_").replace(":", "_").replace(".", "_").replace(" ", "_")
    )
    if output_path.startswith("file:///"):
        # create local tmp path
        import tempfile

        local_tmp_dir = tempfile.gettempdir()
        tmp_path = f"file://{local_tmp_dir}/fused-tmp/tmp/{src_path_part}-{cache_id}/"
    else:
        api = fused.api.FusedAPI()
        tmp_path = api._resolve(f"fd://fused-tmp/tmp/{src_path_part}-{cache_id}/")

    if is_non_empty_dir(tmp_path):
        raise ValueError(
            f"Temporary path {tmp_path} is not empty. Please re-run to resolve "
            "the issue."
        )

    return tmp_path


def _cleanup_tmp_files(tmp_path: str, remove_tmp_files: bool):
    if remove_tmp_files:
        try:
            _delete_path(tmp_path)
        except Exception:
            print("-- Warning: failed to remove temporary files")


def _delete_path(path: str):
    if path.startswith("file://"):
        import shutil

        shutil.rmtree(path.replace("file://", ""), ignore_errors=True)
    else:
        orig = fused.options.request_timeout
        fused.options.request_timeout = 30
        fused.api.delete(path)
        fused.options.request_timeout = orig


def _list_files(path: str):
    if path.startswith("file://"):
        from pathlib import Path

        path = Path(path.replace("file://", ""))
        if path.is_file():
            return [str(path)]
        return [str(p) for p in path.iterdir() if p.is_file()]
    else:
        orig = fused.options.request_timeout
        fused.options.request_timeout = 10
        files = [
            path.url
            for path in fused.api.list(path, details=True)
            if not path.is_directory
        ]
        fused.options.request_timeout = orig
        return files


def _list_tmp_file_ids(tmp_path: str):
    if tmp_path.startswith("file://"):
        from pathlib import Path

        path = Path(tmp_path.replace("file://", ""))
        file_ids = [
            p.name for p in path.iterdir() if p.is_dir() and not p.name.startswith("_")
        ]
    else:
        orig = fused.options.request_timeout
        fused.options.request_timeout = 10
        file_ids = [path.strip("/").split("/")[-1] for path in fused.api.list(tmp_path)]
        file_ids = [fid for fid in file_ids if not fid.startswith("_")]
        fused.options.request_timeout = orig
    return file_ids


def infer_defaults(
    src_path: str,
    res: int | None = None,
    file_res: int | None = None,
    chunk_res: int | None = None,
    k_ring: int = 1,
    res_offset: int = 1,
):
    import math

    import h3.api.basic_int as h3
    import pyproj
    import rasterio

    if res is None:
        with rasterio.open(src_path) as src:
            src_crs = pyproj.CRS(src.crs)
            # estimate target resolution based on pixel size
            # -> use resolution where 7 cells would roughly cover one pixel
            if src_crs.is_projected:
                pixel_area = (
                    (src.bounds.right - src.bounds.left)
                    / src.width
                    * (src.bounds.top - src.bounds.bottom)
                    / src.height
                )
            else:
                # approximate pixel area in m^2 at center of raster
                transformer = pyproj.Transformer.from_crs(
                    src_crs, "EPSG:3857", always_xy=True
                )
                x_center = (src.bounds.right + src.bounds.left) / 2
                y_center = (src.bounds.top + src.bounds.bottom) / 2
                x1, y1 = transformer.transform(x_center, y_center)
                x2, y2 = transformer.transform(
                    x_center + (src.bounds.right - src.bounds.left) / src.width,
                    y_center + (src.bounds.top - src.bounds.bottom) / src.height,
                )
                pixel_area = abs((x2 - x1) * (y2 - y1))

            n_cells = max(7 * k_ring, 1)
            # get lat/lng of center
            transformer = pyproj.Transformer.from_crs(
                src_crs, "EPSG:4326", always_xy=True
            )
            lng, lat = transformer.transform(
                (src.bounds.right + src.bounds.left) / 2,
                (src.bounds.top + src.bounds.bottom) / 2,
            )

            for res in range(15, 0, -1):
                if h3.cell_area(h3.latlng_to_cell(lat, lng, res), "m^2") > (
                    pixel_area / n_cells
                ):
                    break

        res = res - res_offset

    if file_res is None:
        # target is to have files around 100MB up to 1 GB in size:
        # with the current compression and typical dataset with the
        # `hex, data, cnt, cnt_total` columns, a rought estimate is that
        # we have 1 byte per row.
        # (and assuming a minimum of one value for each cell in the target
        # resolution)
        file_res = res - math.ceil(math.log(100_000_000, 7))
        file_res = max(file_res, 0)

    if chunk_res is None:
        # choose a chunk_res such that each row group has
        # at least 1,000,000 rows, assuming we have one value for each cell
        # in the target resolution
        # (typical recommendation of 100,000 rows gives to small row groups
        # with our files with few columns)
        chunk_res = res - math.floor(math.log(1_000_000, 7))
        # with a minimum of +2 compared to the file resolution,
        # to ensure we have multiple (10+) row groups per file
        chunk_res = max(chunk_res, file_res + 2)

    return res, file_res, chunk_res


def run_ingest_raster_to_h3(
    src_path: str | list[str],
    output_path: str,
    metrics: str | list[str] = "cnt",
    res: int | None = None,
    k_ring: int = 1,
    res_offset: int = 1,
    chunk_res: int | None = None,
    file_res: int | None = None,
    overview_res: list[int] | None = None,
    overview_chunk_res: int | list[int] | None = None,
    max_rows_per_chunk: int = 0,
    include_source_url: bool = True,
    target_chunk_size: int | None = None,
    debug_mode: bool = False,
    remove_tmp_files: bool = True,
    tmp_path: str | None = None,
    overwrite: bool = False,
    extract_kwargs={},
    partition_kwargs={},
    overview_kwargs={},
    **kwargs,
):
    """
    Run the raster to H3 ingestion process.

    This process involves multiple steps:
    - extract pixels values and assign to H3 cells in chunks (extract step)
    - combine the chunks per partition (file) and prepare metadata (partition step)
    - create the metadata `_sample` file and overviews files

    Args:
        src_path (str, list): Path(s) to the input raster data.
            When this is a single path, the file is chunked up for processing
            based on `target_chunk_size`. When this is a list of paths, each
            file is processed as one chunk.
        output_path (str): Path for the resulting Parquet dataset.
        metrics (str or list of str): The metrics to compute per H3 cell.
            Supported metrics are either "cnt" or a list containing any of
            "avg", "min", "max", "stddev", "mode" (i.e. most common value),
            and "sum".
        res (int): The resolution of the H3 cells in the output data.
            The pixel values are assigned to H3 cells at resolution
            `res + res_offset` and then aggregated to `res`.
            By default, this is inferred based on the resolution of the
            input data ensuring the H3 cell size is close to the pixel size
            (e.g. for a raster with pixel size of 30x30m, a resolution of 11
            is inferred).
        k_ring (int): The k-ring distance at resolution `res + res_offset`
            to which the pixel value is assigned (in addition to the center
            cell). Defaults to 1.
        res_offset (int): Offset to child resolution (relative to `res`) at
            which to assign the raw pixel values to H3 cells.
        file_res (int): The H3 resolution to chunk the resulting files of the
            Parquet dataset. By default will be inferred based on the target
            resolution `res`. You can specify `file_res=-1` to have a single
            output file.
        chunk_res (int): The H3 resolution to chunk the row groups within
            each file of the Parquet dataset (ignored when `max_rows_per_chunk`
            is specified). By default will be inferred based on the target
            resolution `res`.
        overview_res (list of int): The H3 resolutions for which to create
            overview files. By default, overviews are created for resolutions 3
            to 7 (or capped at a lower value if the `res` of the output dataset
            is lower).
        overview_chunk_res (int or list of int): The H3 resolution(s) to chunk
            the row groups within each overview file of the Parquet dataset. By
            default, each overview file is chunked at the overview resolution
            minus 5 (clamped between 0 and the `res` of the output dataset).
        max_rows_per_chunk (int): The maximum number of rows per chunk in the
            resulting data and overview files. If 0 (the default), `chunk_res`
            and `overview_chunk_res` are used to determine the chunking.
        include_source_url (bool): If True, include a `"source_url"` column in
            the output dataset that contains a list of source URLs that
            contributed data to each H3 cell. Defaults to True, set to False
            to omit this column.
        target_chunk_size (int): The approximate number of pixel values to
            process per chunk in the first "extract" step. Defaults to
            10,000,000 for ingesting a single file or a few files. If ingesting
            more than 20 files, each file is processed as a single chunk by
            default, but you can override this by specifying a specific
            `target_chunk_size` value, or by specifying `target_chunk_size=0` to
            always process each file as a single chunk.
        debug_mode (bool): If True, run only the first two chunks for
            debugging purposes. Defaults to False.
        remove_tmp_files (bool): If True, remove the temporary files after
            ingestion is complete. Defaults to True.
        tmp_path (str): Optional path to use for the temporary files.
            If specified, the extract step is skipped and it is assumed that
            the temporary files are already present at this path.
        overwrite (bool): If True, overwrite the output path if it already
            exists, by first removing the existing content before writing the
            new files. Defaults to False, in which case an error is raised if
            the `output_path` is not empty.
        extract_kwargs (dict): Additional keyword arguments to pass to
            `fused.submit` for the extract step.
        partition_kwargs (dict): Additional keyword arguments to pass to
            `fused.submit` for the partition step.
        overview_kwargs (dict): Additional keyword arguments to pass to
            `fused.submit` for the overview step.
        **kwargs
            Additional keyword arguments to pass to `fused.submit` for each of
            the extract, partition, and overview steps. Keys specified here are
            further overridden by those in `extract_kwargs`, `partition_kwargs`,
            and `overview_kwargs` respectively.
            Typical keywords include `engine`, `instance_type`, `max_workers`,
            and `n_processes_per_worker`.

    The extract, partition and overview steps are run in parallel using
    `fused.submit()`. By default, the function will first attempt to run this using
    "realtime" instances, and retry any failed runs using "large" instances.

    You can override this behavior by specifying the `engine`, `instance_type`,
    `max_workers`, `n_processes_per_worker`, etc parameters as additional
    keyword arguments to this function (`**kwargs`). If you want to specify
    those per step, use `extract_kwargs`, `partition_kwargs`, and `overview_kwargs`.
    For example, to run everything locally on the same machine where this
    function runs, use:

        run_ingest_raster_to_h3(..., engine="local")

    To run the extract step on realtime and the partition step on medium
    instance, you could do:

        run_ingest_raster_to_h3(...,
            extract_kwargs={"instance_type": "realtime", "max_workers": 256, "max_retry": 1},
            partition_kwargs={"instance_type": "medium", "max_workers": 5, "n_processes_per_worker": 2},
        )
    """
    import datetime

    import numpy as np
    import rasterio

    try:
        from job2.partition.raster_to_h3 import udf_sample
    except ImportError:
        raise RuntimeError(
            "The ingestion functionality can only be run using the remote engine"
        )

    result_extract = None
    result_partition = None

    print("Starting ingestion process\n")
    start_time = datetime.datetime.now()

    # Validate and preprocess input src path
    if isinstance(src_path, str):
        # single file or directory input
        src_files = _list_files(src_path)
        if not src_files:
            raise ValueError(f"No input files found at {src_path}")
    else:
        src_files = src_path

    print(
        f"-- Processing {len(src_files)} file(s) at {src_files[0] if len(src_files) == 1 else src_files[0].rsplit('/', maxsplit=1)[0]}"
    )

    # Validate output path and verify that it is empty
    output_path = str(output_path)
    if not output_path.endswith("/"):
        output_path += "/"
    if is_non_empty_dir(output_path):
        if overwrite:
            print(f"-- Overwriting existing output path {output_path}")
            _delete_path(output_path)
        else:
            raise ValueError(
                f"Output path {output_path} is not empty. If you want to remove "
                "existing files, specify `overwrite=True`."
            )

    # Construct path for intermediate results
    skip_extract = False
    if tmp_path is not None:
        print(f"-- Using user-specified temporary path: {tmp_path}")
        skip_extract = True
    else:
        tmp_path = _create_tmp_path(src_files[0], output_path)
        print(f"-- Using {tmp_path=}")

    res, file_res, chunk_res = infer_defaults(
        src_files[0],
        res,
        file_res,
        chunk_res,
        k_ring=k_ring,
        res_offset=res_offset,
    )
    if res + res_offset > 15:
        raise ValueError(
            f"The combination of `res={res}` and `res_offset={res_offset}` "
            f"results in a resolution higher than 15 ({res} + {res_offset} = "
            f"{res + res_offset}), which is not supported. "
            "Provide either a lower res or res_offset."
        )
    print(f"\n-- Using {res=}, {file_res=}, {chunk_res=}")

    if isinstance(metrics, str):
        metrics = [metrics]
    else:
        metrics = list(metrics)
        if len(metrics) > 1 and "cnt" in metrics:
            raise ValueError("The 'cnt' metric cannot be combined with other metrics")

    if "sum" in metrics and k_ring != 1 and res_offset != 1:
        raise NotImplementedError(
            "The 'sum' metric is currently only supported for k_ring=1 and res_offset=1"
        )

    if overview_res is None:
        max_overview_res = min(res - 1, 7)
        overview_res = list(range(3, max_overview_res + 1))
    elif max(overview_res) >= res:
        raise ValueError(
            "Overview resolutions must be lower than the target resolution `res`"
        )
    if overview_chunk_res is None:
        overview_chunk_res = [max(r - 5, 0) for r in overview_res]
    elif isinstance(overview_chunk_res, int):
        overview_chunk_res = [overview_chunk_res] * len(overview_res)

    ###########################################################################
    # Step one: extracting pixel values and converting to hex divided in chunks

    if not skip_extract:
        print("\nRunning extract step")
        start_extract_time = datetime.datetime.now()

        if target_chunk_size is None:
            if len(src_files) > 20:
                print(
                    "-- processing each file as a single chunk by default (specify "
                    "'target_chunk_size' to override this)"
                )
                target_chunk_size = 0
            else:
                target_chunk_size = 10_000_000

        if target_chunk_size > 0:
            # determine number of chunks based on target chunk size
            x_chunks = []
            y_chunks = []
            for src_file in src_files:
                with rasterio.open(src_file) as src:
                    meta = src.meta

                x_chunks.append(
                    max(round(meta["width"] / np.sqrt(target_chunk_size)), 1)
                )
                y_chunks.append(
                    max(round(meta["height"] / np.sqrt(target_chunk_size)), 1)
                )
        else:
            # allow to process each file as a single chunk
            x_chunks = [1] * len(src_files)
            y_chunks = [1] * len(src_files)

        n_chunks_per_file = [x * y for x, y in zip(x_chunks, y_chunks)]

        if debug_mode:
            # avoid creating huge submit_params list in case of tiny target_chunk_size
            src_path = src_path[:1]
            x_chunks = x_chunks[:1]
            y_chunks = y_chunks[:1]
            n_chunks_per_file = [min(n_chunks_per_file[0], 2)]

        # repeat variables per input file chunks
        submit_params = [
            {
                "src_path": p,
                "x_chunks": x,
                "y_chunks": y,
                "chunk_id": chunk_id,
                "chunk_name": f"{p.split('/')[-1].rsplit('.', maxsplit=1)[0]}_{chunk_id}",
            }
            for p, x, y, n in zip(src_files, x_chunks, y_chunks, n_chunks_per_file)
            for chunk_id in range(n)
        ]

        extract_run_kwargs = dict(
            submit_params=submit_params,
            tmp_path=tmp_path,
            res=res,
            k_ring=k_ring,
            res_offset=res_offset,
            file_res=file_res,
        )
        extract_submit_kwargs = {"max_retry": 0} | kwargs | extract_kwargs

        # Run the actual extract step
        print(f"-- processing {len(submit_params)} chunks")
        result_extract = _submit_with_fallback(
            "Extract",
            run_extract,
            extract_run_kwargs,
            extract_submit_kwargs,
            update_callback=lambda run_kwargs, errors: run_kwargs.update(
                {"submit_params": [submit_params[i] for i in errors.keys()]}
            ),
        )
        _print_batch_jobs(result_extract)
        result_extract.wait()
        end_extract_time = datetime.datetime.now()
        if not result_extract.all_succeeded():
            print("\nExtract step failed!")
            _cleanup_tmp_files(tmp_path, remove_tmp_files)
            return result_extract, result_partition
        print(f"-- Done extract! (took {end_extract_time - start_extract_time})")
    else:
        print("\nSkipping extract step")
        end_extract_time = datetime.datetime.now()

    ###########################################################################
    # Step two: combining the chunks per file (resolution 2) and preparing
    # metadata and overviews

    print("\nRunning partition step")

    # list available file_ids from the previous step
    file_ids = _list_tmp_file_ids(tmp_path)
    print(f"-- processing {len(file_ids)} file_ids")

    partition_run_kwargs = dict(
        tmp_path=tmp_path,
        file_ids=file_ids,
        output_path=output_path,
        metrics=metrics,
        chunk_res=chunk_res,
        overview_res=overview_res,
        max_rows_per_chunk=max_rows_per_chunk,
        include_source_url=include_source_url,
    )
    partition_submit_kwargs = {"max_retry": 0} | kwargs | partition_kwargs

    # Run the actual partition step
    result_partition = _submit_with_fallback(
        "Partition",
        run_partition,
        partition_run_kwargs,
        partition_submit_kwargs,
        update_callback=lambda run_kwargs, errors: run_kwargs.update(
            {"file_ids": [file_ids[i] for i in errors.keys()]}
        ),
    )
    _print_batch_jobs(result_partition)
    result_partition.wait()
    end_partition_time = datetime.datetime.now()
    if not result_partition.all_succeeded():
        print("\nPartition step failed!")
        _cleanup_tmp_files(tmp_path, remove_tmp_files)
        return result_extract, result_partition
    print(f"-- Done partition! (took {end_partition_time - end_extract_time})")

    ###########################################################################
    # Step 3: combining the metadata and overview tmp files

    print("\nRunning sample step")

    @fused.udf(cache_max_age=0)
    def udf_sample(tmp_path: str, output_path: str):
        from job2.partition.raster_to_h3 import udf_sample as run_udf_sample

        return run_udf_sample(tmp_path, output_path)

    sample_file = fused.run(
        udf_sample,
        tmp_path=tmp_path,
        output_path=output_path,
        verbose=False,
        engine=kwargs.get("engine", None),
    )
    end_sample_time = datetime.datetime.now()
    print(f"-- Written: {sample_file}")
    print(f"-- Done sample! (took {end_sample_time - end_partition_time})")

    print("\nRunning overview step")
    overview_run_kwargs = dict(
        tmp_path=tmp_path,
        output_path=output_path,
        overview_res=overview_res,
        overview_chunk_res=overview_chunk_res,
        max_rows_per_chunk=max_rows_per_chunk,
    )
    overview_submit_kwargs = {"max_retry": 0} | kwargs | overview_kwargs

    result_overview = _submit_with_fallback(
        "Overview",
        run_overview,
        overview_run_kwargs,
        overview_submit_kwargs,
        update_callback=lambda run_kwargs, errors: run_kwargs.update(
            {
                "overview_res": [overview_res[i] for i in errors.keys()],
                "overview_chunk_res": [overview_chunk_res[i] for i in errors.keys()],
            }
        ),
    )
    _print_batch_jobs(result_overview)
    result_overview.wait()

    end_overview_time = datetime.datetime.now()
    if not result_overview.all_succeeded():
        print("\nOverview step failed!")
        _cleanup_tmp_files(tmp_path, remove_tmp_files)
        return result_extract, result_partition

    for i, overview_file in enumerate(result_overview.results()):
        print(
            f"-- Written: {overview_file} (res={overview_res[i]}, chunk_res={overview_chunk_res[i]})"
        )

    print(f"-- Done overview! (took {end_overview_time - end_sample_time})")

    # remove tmp files
    _cleanup_tmp_files(tmp_path, remove_tmp_files)

    print(f"\nIngestion process done! (took {datetime.datetime.now() - start_time})")

    return result_extract, result_partition


@fused.udf(cache_max_age=0)
def udf_divide(src_path: str, tmp_path: str, chunk_name: str, file_res: int = 2):
    # define UDF that imports the helper function inside the UDF
    from job2.partition.raster_to_h3 import write_by_file_res

    write_by_file_res(
        src_path,
        tmp_path,
        chunk_name,
        file_res=file_res,
    )


def run_divide(src_files: list[str], tmp_path: str, file_res: int, **kwargs):
    params = {
        "tmp_path": tmp_path,
        "file_res": file_res,
    }
    submit_params = [
        {"src_path": p, "chunk_name": str(i)} for i, p in enumerate(src_files)
    ]
    pool = fused.submit(
        udf_divide,
        submit_params,
        **params,
        collect=False,
        **kwargs,
    )
    return pool


def run_partition_to_h3(
    src_path,
    output_path: str,
    metrics: str | list[str] = "cnt",
    groupby_cols: list[str] = ["hex", "data"],
    window_cols: list[str] = ["hex"],
    additional_cols: list[str] = [],
    res: int | None = None,
    # k_ring: int = 1,
    # parent_offset: int = 1,
    chunk_res: int | None = None,
    file_res: int | None = None,
    overview_res: list[int] | None = None,
    overview_chunk_res: int | list[int] | None = None,
    max_rows_per_chunk: int = 0,
    # debug_mode: bool = False,
    remove_tmp_files: bool = True,
    overwrite: bool = False,
    extract_kwargs={},
    partition_kwargs={},
    overview_kwargs={},
    **kwargs,
):
    """
    Run the H3 partitioning process.

    This pipeline assumes that the input data already has a ``"hex"`` column
    with H3 cell IDs at the target resolution. It will then repartition
    the data spatially and add overview files.

    Args:
        src_path (str, list): Path(s) to the input data.
            Can be a path to file or directory, or list of file paths). The
            first step of the processing is parallelized per input file.
        output_path (str): Path for the resulting Parquet dataset.
        metrics (str or list of str): The metrics to compute per H3 cell.
            Supported metrics are either "cnt" or a list containing any of
            "avg", "min", "max", "stddev", and "sum".
        groupby_cols (list): The columns indicating the groups for which
            the aggregated metrics are calculated. By default, this is ``["hex",
            "data"]`` (for the default "cnt" metric, this means counts are
            calculated (summed) per unique combination of "hex" and "data").
            The list must always include ``"hex"``.
            This only applies when the "cnt" metric is specified.
        window_cols (list): The columns for which to calculate total counts
            over using a window function. This will add an additional column to
            the output (one for each of the columns in this list) with the total
            counts per unique value of the specified column.
            By default, this is only done for the "hex" column.
            This only applies when the "cnt" metric is specified.
        additional_cols (list): Additional columns from the input data to
            include in the output dataset. These columns are assumed to have a
            unique value per group defined by the `groupby_cols`. If this is not
            the case, the output will contain arbitrary values from one of the
            rows in each group.
            By default, this is empty.
            This only applies when the "cnt" metric is specified.
        res (int): The resolution at which to assign the pixel values to H3 cells.
        file_res (int): The H3 resolution to chunk the resulting files of the
            Parquet dataset. By default will be inferred based on the target
            resolution `res`. You can specify `file_res=-1` to have a single
            output file.
        chunk_res (int): The H3 resolution to chunk the row groups within
            each file of the Parquet dataset (ignored when `max_rows_per_chunk`
            is specified). By default will be inferred based on the target
            resolution `res`.
        overview_res (list of int): The H3 resolutions for which to create
            overview files. By default, overviews are created for resolutions 3
            to 7 (or capped at a lower value if the `res` of the output dataset
            is lower).
        overview_chunk_res (int or list of int): The H3 resolution(s) to chunk
            the row groups within each overview file of the Parquet dataset. By
            default, each overview file is chunked at the overview resolution
            minus 5 (clamped between 0 and the `res` of the output dataset).
        max_rows_per_chunk (int): The maximum number of rows per chunk in the
            resulting data and overview files. If 0 (the default), `chunk_res`
            and `overview_chunk_res` are used to determine the chunking.
        remove_tmp_files (bool): If True, remove the temporary files after
            ingestion is complete. Defaults to True.
        overwrite (bool): If True, overwrite the output path if it already
            exists, by first removing the existing content before writing the
            new files. Defaults to False, in which case an error is raised if
            the `output_path` is not empty.
        extract_kwargs (dict): Additional keyword arguments to pass to
            `fused.submit` for the extract step.
        partition_kwargs (dict): Additional keyword arguments to pass to
            `fused.submit` for the partition step.
        overview_kwargs (dict): Additional keyword arguments to pass to
            `fused.submit` for the overview step.
        **kwargs
            Additional keyword arguments to pass to `fused.submit` for each of
            the extract, partition, and overview steps. Keys specified here are
            further overridden by those in `extract_kwargs`, `partition_kwargs`,
            and `overview_kwargs` respectively.

    See the docstring of `run_ingest_raster_to_h3` for more details on
    the processing steps and how to configure the execution.
    """
    import datetime

    try:
        from job2.partition.raster_to_h3 import udf_sample
    except ImportError:
        raise RuntimeError(
            "The ingestion functionality can only be run using the remote engine"
        )

    result_extract = None
    result_partition = None

    if not isinstance(src_path, (str, list)):
        raise NotImplementedError

    is_single_file = isinstance(src_path, str)
    # use single file for inferring defaults and creating paths
    src_path_file = src_path if is_single_file else src_path[0]

    print(
        f"Starting partitioning process for {src_path_file}{' ({} files)'.format(len(src_path)) if not is_single_file else ''}\n"
    )
    start_time = datetime.datetime.now()

    # Validate output path and verify that it is empty
    output_path = str(output_path)
    if not output_path.endswith("/"):
        output_path += "/"
    if is_non_empty_dir(output_path):
        if overwrite:
            print(f"-- Overwriting existing output path {output_path}")
            _delete_path(output_path)
        else:
            raise ValueError(
                f"Output path {output_path} is not empty. If you want to remove "
                "existing files, specify `overwrite=True`."
            )

    # Construct path for intermediate results
    tmp_path = _create_tmp_path(src_path_file, output_path)
    print(f"-- Using {tmp_path=}")

    if res is None:
        raise ValueError("res must be specified for now")

    res, file_res, chunk_res = infer_defaults(
        None,
        res,
        file_res,
        chunk_res,
    )
    print(f"\n-- Using {res=}, {file_res=}, {chunk_res=}")

    if isinstance(metrics, str):
        metrics = [metrics]
    else:
        metrics = list(metrics)
        if len(metrics) > 1 and "cnt" in metrics:
            raise ValueError("The 'cnt' metric cannot be combined with other metrics")

    if "hex" not in groupby_cols:
        raise ValueError("groupby_cols must contain 'hex'")

    if overview_res is None:
        max_overview_res = min(res - 1, 7)
        overview_res = list(range(3, max_overview_res + 1))
    elif max(overview_res) >= res:
        raise ValueError(
            "Overview resolutions must be lower than the target resolution `res`"
        )
    if overview_chunk_res is None:
        overview_chunk_res = [max(r - 5, 0) for r in overview_res]
    elif isinstance(overview_chunk_res, int):
        overview_chunk_res = [overview_chunk_res] * len(overview_res)

    ###########################################################################
    # Step one: splitting data per file

    print("\nRunning extract step")
    start_extract_time = datetime.datetime.now()

    if isinstance(src_path, str):
        # single file or directory input
        files = _list_files(src_path)
    else:
        files = src_path
    print(f"-- processing {len(files)} chunks")

    divide_run_kwargs = dict(
        src_files=files,
        tmp_path=tmp_path,
        file_res=file_res,
    )
    divide_submit_kwargs = {"max_retry": 0} | kwargs | extract_kwargs

    # Run the actual extract (divide) step
    result_extract = _submit_with_fallback(
        "Extract",
        run_divide,
        divide_run_kwargs,
        divide_submit_kwargs,
        update_callback=lambda run_kwargs, errors: run_kwargs.update(
            {
                "src_path": [files[i] for i in errors.keys()],
                "chunk_name": [str(i) for i in errors.keys()],
            }
        ),
    )
    result_extract.wait()
    end_extract_time = datetime.datetime.now()
    if not result_extract.all_succeeded():
        print("\nExtract step failed!")
        try:
            _cleanup_tmp_files(tmp_path, remove_tmp_files)
        except Exception:
            pass
        return result_extract, result_partition
    print(f"-- Done extract! (took {end_extract_time - start_extract_time})")

    ###########################################################################
    # Step two: combining the chunks per file (resolution 2) and preparing
    # metadata and overviews

    print("\nRunning partition step")

    # list available file_ids from the previous step
    file_ids = _list_tmp_file_ids(tmp_path)
    print(f"-- processing {len(file_ids)} file_ids")

    partition_run_kwargs = dict(
        tmp_path=tmp_path,
        file_ids=file_ids,
        output_path=output_path,
        metrics=metrics,
        groupby_cols=groupby_cols,
        window_cols=window_cols,
        additional_cols=additional_cols,
        chunk_res=chunk_res,
        overview_res=overview_res,
        max_rows_per_chunk=max_rows_per_chunk,
    )
    partition_submit_kwargs = {"max_retry": 0} | kwargs | partition_kwargs

    # Run the actual partition step
    result_partition = _submit_with_fallback(
        "Partition",
        run_partition,
        partition_run_kwargs,
        partition_submit_kwargs,
        update_callback=lambda run_kwargs, errors: run_kwargs.update(
            {"file_ids": [file_ids[i] for i in errors.keys()]}
        ),
    )
    result_partition.wait()
    end_partition_time = datetime.datetime.now()
    if not result_partition.all_succeeded():
        print("\nPartition step failed!")
        _cleanup_tmp_files(tmp_path, remove_tmp_files)
        return result_extract, result_partition
    print(f"-- Done partition! (took {end_partition_time - end_extract_time})")

    ###########################################################################
    # Step 3: combining the metadata and overview tmp files

    print("\nRunning sample step")

    @fused.udf(cache_max_age=0)
    def udf_sample(tmp_path: str, output_path: str):
        from job2.partition.raster_to_h3 import udf_sample as run_udf_sample

        return run_udf_sample(tmp_path, output_path)

    sample_file = fused.run(
        udf_sample,
        tmp_path=tmp_path,
        output_path=output_path,
        verbose=False,
        engine=kwargs.get("engine", None),
    )
    end_sample_time = datetime.datetime.now()
    print(f"-- Written: {sample_file}")
    print(f"-- Done sample! (took {end_sample_time - end_partition_time})")

    print("\nRunning overview step")
    overview_run_kwargs = dict(
        tmp_path=tmp_path,
        output_path=output_path,
        overview_res=overview_res,
        overview_chunk_res=overview_chunk_res,
        max_rows_per_chunk=max_rows_per_chunk,
    )
    overview_submit_kwargs = {"max_retry": 0} | kwargs | overview_kwargs

    result_overview = _submit_with_fallback(
        "Overview",
        run_overview,
        overview_run_kwargs,
        overview_submit_kwargs,
        update_callback=lambda run_kwargs, errors: run_kwargs.update(
            {
                "overview_res": [overview_res[i] for i in errors.keys()],
                "overview_chunk_res": [overview_chunk_res[i] for i in errors.keys()],
            }
        ),
    )
    result_overview.wait()

    end_overview_time = datetime.datetime.now()
    if not result_overview.all_succeeded():
        print("\nOverview step failed!")
        _cleanup_tmp_files(tmp_path, remove_tmp_files)
        return result_extract, result_partition

    for i, overview_file in enumerate(result_overview.results()):
        print(
            f"-- Written: {overview_file} (res={overview_res[i]}, chunk_res={overview_chunk_res[i]})"
        )

    print(f"-- Done overview! (took {end_overview_time - end_sample_time})")

    # remove tmp files
    _cleanup_tmp_files(tmp_path, remove_tmp_files)

    print(f"\nIngestion process done! (took {datetime.datetime.now() - start_time})")

    return result_extract, result_partition
