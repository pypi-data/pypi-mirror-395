# TODO: This file is no longer the most recent -- use fused.core.run_* instead
# This file is only for running non-saved (code included) UDFs
from __future__ import annotations

import json
import time
from dataclasses import dataclass
from typing import TYPE_CHECKING

from loguru import logger

from fused._options import default_serialization_format
from fused._options import options as OPTIONS
from fused._request import session_with_retries
from fused.api.api import FusedAPI, resolve_udf_server_url
from fused.context import get_user_email
from fused.core._realtime_ops import (
    _process_response,
    _process_response_async,
    serialize_realtime_params,
)
from fused.models import AnyJobStepConfig
from fused.models.udf._eval_result import UdfEvaluationResult

from ..core._realtime_ops import _realtime_raise_for_status_async, get_recursion_factor

if TYPE_CHECKING:
    import pandas as pd


@dataclass
class RequestInfo:
    udf_server_url: str
    url: str
    body: dict
    headers: dict
    params: dict


def _prepare_request(
    step_config: AnyJobStepConfig | None,
    params: dict[str, str] | None,
    xyz: tuple[float, float, float] | None,
    client_id: str | None,
    cache_max_age: int | None,
    format: str | None,
    _profile: bool,
    run_id: str | None,
):
    # We need to get the auth headers from the FusedAPI. Don't enable set_global_api
    # to avoid messing up the user's environment.
    api = FusedAPI(set_global_api=False)

    udf_server_url = resolve_udf_server_url(client_id)

    assert step_config is not None
    # Apply parameters, if we want to step_config that's returned to have this,
    # overwrite step_config.
    step_config_with_params = step_config.set_udf(
        udf=step_config.udf, parameters=serialize_realtime_params(params)
    )

    # Note: Custom UDF uses the json POST attribute.
    if xyz is None:
        url = f"{udf_server_url}/api/v1/run/udf"
    else:
        x, y, z = xyz
        url = f"{udf_server_url}/api/v1/run/udf/tiles/{z}/{x}/{y}"

    # Payload
    # This is the body for when step_config_with_params.type == "udf".
    body = {
        "step_config": step_config_with_params.model_dump_json(),
        "format": format or default_serialization_format(),
        "profile": _profile,
    }

    # Headers
    recursion_factor = get_recursion_factor()
    headers = api._generate_headers(
        {
            "Content-Type": "application/json",
            **(OPTIONS.default_run_headers or {}),
        }
    )
    headers["Fused-Recursion"] = f"{recursion_factor}"
    if run_id is not None:
        headers["Fused-Run-Id"] = run_id
    if user_email := get_user_email():
        headers["Fused-Share-User-Email"] = user_email

    # Params
    req_params = {
        **({"cache_max_age": int(cache_max_age)} if cache_max_age is not None else {}),
    }

    return step_config_with_params, RequestInfo(
        udf_server_url=udf_server_url,
        url=url,
        body=body,
        headers=headers,
        params=req_params,
    )


def run_tile(
    x: float,
    y: float,
    z: float,
    step_config: AnyJobStepConfig | None = None,
    params: dict[str, str] | None = None,
    *,
    client_id: str | None = None,
    cache_max_age: int | None = None,
    format: str | None = None,
    _profile: bool = False,
    run_id: str | None = None,
) -> UdfEvaluationResult:
    return run(
        step_config=step_config,
        params=params,
        xyz=(x, y, z),
        client_id=client_id,
        cache_max_age=cache_max_age,
        format=format,
        _profile=_profile,
        run_id=run_id,
    )


def run(
    step_config: AnyJobStepConfig | None = None,
    params: dict[str, str] | None = None,
    xyz: tuple[float, float, float] | None = None,
    *,
    client_id: str | None = None,
    cache_max_age: int | None = None,
    format: str | None = None,
    _profile: bool = False,
    run_id: str | None = None,
) -> pd.DataFrame:
    """Run a UDF.

    Args:
        step_config: AnyJobStepConfig.
        params: Additional parameters to pass to the UDF. Must be JSON serializable.
    """
    time_start = time.perf_counter()

    # Prepare request body/headers/parameters
    step_config_with_params, request = _prepare_request(
        step_config=step_config,
        params=params,
        xyz=xyz,
        client_id=client_id,
        cache_max_age=cache_max_age,
        format=format,
        _profile=_profile,
        run_id=run_id,
    )

    # Make request
    start = time.time()

    with session_with_retries() as session:
        logger.debug(f"{run_id=} | Starting request")
        r = session.request(
            method="POST",
            url=request.url,
            params=request.params,
            json=request.body,
            headers=request.headers,
            timeout=OPTIONS.run_timeout,
        )

    end = time.time()
    logger.info(f"{run_id=} | Time in request: {end - start}")

    time_end = time.perf_counter()
    time_taken_seconds = time_end - time_start

    return _process_response(
        r,
        step_config=step_config_with_params,
        time_taken_seconds=time_taken_seconds,
        profile=_profile,
    )


def run_polling(
    step_config: AnyJobStepConfig | None = None,
    params: dict[str, str] | None = None,
    *,
    xyz: tuple[float, float, float] | None = None,
    client_id: str | None = None,
    cache_max_age: int | None = None,
    format: str | None = None,
    _profile: bool = False,
    run_id: str | None = None,
) -> UdfEvaluationResult:
    time_start = time.perf_counter()

    # Prepare request body/headers/parameters
    step_config_with_params, request = _prepare_request(
        step_config=step_config,
        params=params,
        xyz=xyz,
        client_id=client_id,
        cache_max_age=cache_max_age,
        format=format,
        _profile=_profile,
        run_id=run_id,
    )

    if xyz is None:
        url = f"{request.udf_server_url}/api/v1/run/udf/start"
    else:
        x, y, z = xyz
        url = f"{request.udf_server_url}/api/v1/run/udf/start/tiles/{z}/{x}/{y}"

    # Make request
    start = time.time()

    # use request_timeout instead of run_timeout since the request does not
    # connect for the entirety of the UDF run
    timeout = OPTIONS.request_timeout

    with session_with_retries() as session:
        logger.debug(f"{run_id=} | Starting request")
        r = session.request(
            method="POST",
            url=url,
            params=request.params,
            json=request.body,
            headers=request.headers,
            timeout=timeout,
        )

        if r.status_code == 202:
            logger.debug(f"{run_id=} | Start polling")

            n_retries = 0
            while (time.time() - start) < OPTIONS.run_timeout:
                r = session.get(
                    f"{request.udf_server_url}/api/v1/run/udf/get/{run_id}",
                    headers=request.headers,
                    timeout=timeout,
                )
                if r.status_code != 202:
                    break
                if n_retries > 1:
                    time.sleep(1)
                n_retries += 1

    if r.status_code == 202:
        # TODO: Add a better error message
        raise Exception(f"UDF run {run_id} timed out")

    end = time.time()
    logger.info(f"{run_id=} | Time in request: {end - start}")

    time_end = time.perf_counter()
    time_taken_seconds = time_end - time_start

    return _process_response(
        r,
        step_config=step_config_with_params,
        time_taken_seconds=time_taken_seconds,
        profile=_profile,
    )


async def run_tile_async(
    x: float,
    y: float,
    z: float,
    step_config: AnyJobStepConfig | None = None,
    params: dict[str, str] | None = None,
    *,
    client_id: str | None = None,
    cache_max_age: int | None = None,
    format: str | None = None,
    run_id: str | None = None,
) -> UdfEvaluationResult:
    return await run_async(
        step_config=step_config,
        params=params,
        xyz=(x, y, z),
        client_id=client_id,
        cache_max_age=cache_max_age,
        format=format,
        run_id=run_id,
    )


async def run_async(
    step_config: AnyJobStepConfig | None = None,
    params: dict[str, str] | None = None,
    *,
    xyz: tuple[float, float, float] | None = None,
    client_id: str | None = None,
    cache_max_age: int | None = None,
    format: str | None = None,
    run_id: str | None = None,
) -> UdfEvaluationResult:
    """Run a UDF over a DataFrame.

    Args:
        step_config: AnyJobStepConfig.
        params: Additional parameters to pass to the UDF. Must be JSON serializable.

    """
    time_start = time.perf_counter()

    # Prepare request body/headers/parameters
    step_config_with_params, request = _prepare_request(
        step_config=step_config,
        params=params,
        xyz=xyz,
        client_id=client_id,
        cache_max_age=cache_max_age,
        format=format,
        _profile=False,
        run_id=run_id,
    )

    # Make request
    start = time.time()

    if OPTIONS.pyodide_async_requests:
        import pyodide.http
        import yarl

        str_params = {key: str(value) for key, value in request.params.items()}
        url_with_params = yarl.URL(request.url, encoded=True).with_query(str_params)
        r = await pyodide.http.pyfetch(
            str(url_with_params),
            method="POST",
            headers=request.headers,
            body=json.dumps(request.body),
            # TODO: timeout
        )
        end = time.time()
        logger.info(f"Time in request: {end - start}")

        await _realtime_raise_for_status_async(r)
        time_end = time.perf_counter()
        time_taken_seconds = time_end - time_start

        return await _process_response_async(
            r,
            step_config=step_config_with_params,
            time_taken_seconds=time_taken_seconds,
        )
    else:
        from fused.core._realtime_ops import _get_shared_session

        # Use shared session for connection pooling and reuse
        # TODO: Retry mechanism
        session = await _get_shared_session()
        async with session.post(
            url=request.url,
            params=request.params,
            json=request.body,
            headers=request.headers,
            # retry=default_retry_strategy,
            # TODO: timeout
        ) as r:
            end = time.time()
            logger.info(f"Time in request: {end - start}")

            await _realtime_raise_for_status_async(r)
            time_end = time.perf_counter()
            time_taken_seconds = time_end - time_start

            return await _process_response_async(
                r,
                step_config=step_config_with_params,
                time_taken_seconds=time_taken_seconds,
            )


async def run_polling_async(
    step_config: AnyJobStepConfig | None = None,
    params: dict[str, str] | None = None,
    *,
    xyz: tuple[float, float, float] | None = None,
    client_id: str | None = None,
    cache_max_age: int | None = None,
    format: str | None = None,
    _profile: bool = False,
    run_id: str | None = None,
) -> UdfEvaluationResult:
    time_start = time.perf_counter()

    # Prepare request body/headers/parameters
    step_config_with_params, request = _prepare_request(
        step_config=step_config,
        params=params,
        xyz=xyz,
        client_id=client_id,
        cache_max_age=cache_max_age,
        format=format,
        _profile=_profile,
        run_id=run_id,
    )
    if xyz is None:
        url = f"{request.udf_server_url}/api/v1/run/udf/start"
    else:
        x, y, z = xyz
        url = f"{request.udf_server_url}/api/v1/run/udf/start/tiles/{z}/{x}/{y}"

    # Make request
    start = time.time()

    if OPTIONS.pyodide_async_requests:
        import pyodide.http
        import yarl

        logger.debug(f"{run_id=} | Starting request")
        str_params = {key: str(value) for key, value in request.params.items()}
        url_with_params = yarl.URL(url, encoded=True).with_query(str_params)
        r = await pyodide.http.pyfetch(
            str(url_with_params),
            method="POST",
            headers=request.headers,
            body=json.dumps(request.body),
            # TODO: timeout
        )
        if r.status == 202:
            logger.debug(f"{run_id=} | Start polling")

            url = yarl.URL(
                f"{request.udf_server_url}/api/v1/run/udf/get/{run_id}", encoded=True
            )

            n_retries = 0
            while (time.time() - start) < OPTIONS.run_timeout:
                r = await pyodide.http.pyfetch(
                    str(url),
                    method="GET",
                    headers=request.headers,
                )
                if r.status != 202:
                    break
                if n_retries > 1:
                    time.sleep(1)
                n_retries += 1

        result_content = await r.bytes()

    else:
        from fused.core._realtime_ops import _get_shared_session

        logger.debug(f"{run_id=} | Starting request")
        result_content: bytes | None = None
        session = await _get_shared_session()
        async with session.post(
            url=url,
            params=request.params,
            json=request.body,
            headers=request.headers,
        ) as r:
            if r.status == 202:
                logger.debug(f"{run_id=} | Start polling")

                n_retries = 0
                while (time.time() - start) < OPTIONS.run_timeout:
                    async with session.get(
                        url=f"{request.udf_server_url}/api/v1/run/udf/get/{run_id}",
                        headers=request.headers,
                    ) as r:
                        if r.status != 202:
                            result_content = await r.read()
                            break
                        if n_retries > 1:
                            time.sleep(1)
                        n_retries += 1
            else:
                result_content = await r.read()

    if r.status == 202:
        # TODO: Add a better error message
        raise Exception(f"UDF run {run_id} timed out")

    end = time.time()
    logger.info(f"{run_id=} | Time in request: {end - start}")

    time_end = time.perf_counter()
    time_taken_seconds = time_end - time_start

    return await _process_response_async(
        r,
        step_config=step_config_with_params,
        time_taken_seconds=time_taken_seconds,
        result_content=result_content,
    )
