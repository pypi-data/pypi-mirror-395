"""Core harmonization workflow functions.

'why': unify sync/async paths via a single async implementation
"""
from __future__ import annotations

import asyncio
import json
import logging
import time
from urllib.parse import urlparse
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Callable, Final, Literal, TypeAlias, cast

import httpx

from ._errors import NetriasAPIUnavailable
from ._http import build_harmonize_payload, fetch_job_status, submit_harmonize_job
from ._io import stream_download_to_file
from ._models import HarmonizationResult, Settings
from ._validators import validate_cde_map_path, validate_output_path, validate_source_path

JSONPrimitive: TypeAlias = str | int | float | bool | None
JSONValue: TypeAlias = JSONPrimitive | Mapping[str, "JSONValue"] | Sequence["JSONValue"]
JOB_POLL_INTERVAL_SECONDS: Final[float] = 3.0
_MESSAGE_KEYS: Final[tuple[str, ...]] = (
    "message",
    "detail",
    "error",
    "description",
    "statusMessage",
)


class HarmonizationJobError(RuntimeError):
    """Raised when the harmonization job fails before producing a result."""


async def _harmonize_async(
    settings: Settings,
    source_path: Path,
    cde_map: Path | Mapping[str, object],
    output_path: Path | None = None,
    cde_map_output_path: Path | None = None,
    logger: logging.Logger | None = None,
    job_callback: Callable[[str], None] | None = None,
    skip_cache: bool = False,
) -> HarmonizationResult:
    """Execute harmonization using the asynchronous job API."""

    logger = logger or logging.getLogger("netrias_client")
    csv_path = validate_source_path(source_path)
    cde_map_input = _resolve_cde_map(cde_map, cde_map_output_path)
    dest = validate_output_path(output_path, source_name=csv_path.stem, allow_versioning=True)

    started = time.perf_counter()
    status_label = "error"
    job_id: str | None = None
    logger.info("harmonize start: file=%s", csv_path)

    try:
        payload = build_harmonize_payload(csv_path, cde_map_input, use_cache=not skip_cache)
        job_payload = await _submit_job_response(
            base_url=settings.harmonization_url,
            api_key=settings.api_key,
            timeout=settings.timeout,
            payload=payload,
            csv_path=csv_path,
            logger=logger,
        )
        logger.info("Payload received: %s", job_payload)
        job_id = _require_job_id(job_payload, csv_path, logger)
        if job_callback:
            job_callback(job_id)
        logger.info("harmonize job queued: file=%s job_id=%s", csv_path, job_id)
        final_payload = await _resolve_final_payload(
            base_url=settings.harmonization_url,
            api_key=settings.api_key,
            job_id=job_id,
            timeout=settings.timeout,
            csv_path=csv_path,
            logger=logger,
        )
        final_url, manifest_url = _require_result_urls(final_payload, csv_path, logger)
    except HarmonizationJobError as exc:
        status_label = "failed"
        return HarmonizationResult(
            file_path=dest,
            manifest_path=None,
            status="failed",
            description=str(exc),
            job_id=job_id,
        )
    else:
        result = await _download_outputs(
            final_url,
            manifest_url,
            dest,
            settings.timeout,
            csv_path,
            logger,
            job_id,
        )
        status_label = result.status
        return result
    finally:
        elapsed = time.perf_counter() - started
        logger.info(
            "harmonize finished: file=%s status=%s duration=%.2fs",
            csv_path,
            status_label,
            elapsed,
        )


def harmonize(
    settings: Settings,
    source_path: Path,
    cde_map: Path | Mapping[str, object],
    output_path: Path | None = None,
    cde_map_output_path: Path | None = None,
    logger: logging.Logger | None = None,
    job_callback: Callable[[str], None] | None = None,
    skip_cache: bool = False,
) -> HarmonizationResult:
    """Sync wrapper: run the async harmonize workflow and block until completion."""

    return asyncio.run(
        _harmonize_async(
            settings=settings,
            source_path=source_path,
            cde_map=cde_map,
            output_path=output_path,
            cde_map_output_path=cde_map_output_path,
            logger=logger,
            job_callback=job_callback,
            skip_cache=skip_cache,
        )
    )


async def harmonize_async(
    settings: Settings,
    source_path: Path,
    cde_map: Path | Mapping[str, object],
    output_path: Path | None = None,
    cde_map_output_path: Path | None = None,
    logger: logging.Logger | None = None,
    job_callback: Callable[[str], None] | None = None,
    skip_cache: bool = False,
) -> HarmonizationResult:
    """Async counterpart to `harmonize` with identical validation and result semantics."""

    return await _harmonize_async(
        settings=settings,
        source_path=source_path,
        cde_map=cde_map,
        output_path=output_path,
        cde_map_output_path=cde_map_output_path,
        logger=logger,
        job_callback=job_callback,
        skip_cache=skip_cache,
    )


def _resolve_cde_map(
    cde_map: Path | Mapping[str, object], cde_map_output_path: Path | None
) -> Path | Mapping[str, object]:
    if isinstance(cde_map, Path):
        return _cde_map_from_path(cde_map, cde_map_output_path)
    return _cde_map_from_mapping(cde_map, cde_map_output_path)


def _cde_map_from_path(
    cde_map_path: Path, cde_map_output_path: Path | None
) -> Path:
    validated = validate_cde_map_path(cde_map_path)
    if cde_map_output_path is None or cde_map_output_path == validated:
        return validated
    cde_map_output_path.parent.mkdir(parents=True, exist_ok=True)
    _ = cde_map_output_path.write_text(
        validated.read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    return cde_map_output_path


def _cde_map_from_mapping(
    cde_map: Mapping[str, object], cde_map_output_path: Path | None
) -> Path | Mapping[str, object]:
    normalized = _normalize_cde_map(cde_map)
    if cde_map_output_path is None:
        return normalized
    cde_map_output_path.parent.mkdir(parents=True, exist_ok=True)
    _ = cde_map_output_path.write_text(
        json.dumps(normalized, indent=2),
        encoding="utf-8",
    )
    return cde_map_output_path


def _normalize_cde_map(cde_map: Mapping[str, object]) -> dict[str, object]:
    try:
        serialized = json.dumps(cde_map)
    except TypeError as exc:  # pragma: no cover - guarded by tests
        raise ValueError("cde_map mapping must be JSON-serializable") from exc
    return cast(dict[str, object], json.loads(serialized))


async def _submit_job_response(
    base_url: str,
    api_key: str,
    timeout: float,
    payload: bytes,
    csv_path: Path,
    logger: logging.Logger,
) -> Mapping[str, JSONValue]:
    response = await _submit_job_http(
        base_url=base_url,
        api_key=api_key,
        timeout=timeout,
        payload=payload,
        csv_path=csv_path,
        logger=logger,
    )
    _ensure_submit_success(response, csv_path, logger)
    payload_mapping = _json_mapping(response)
    if not payload_mapping:
        logger.error("harmonize submit response was not JSON: file=%s", csv_path)
        raise HarmonizationJobError("harmonization job response was not JSON")
    logger.info("harmonize submit payload: file=%s body=%s", csv_path, _formatted_body(payload_mapping))
    return payload_mapping


async def _submit_job_http(
    base_url: str,
    api_key: str,
    timeout: float,
    payload: bytes,
    csv_path: Path,
    logger: logging.Logger,
) -> httpx.Response:
    try:
        return await submit_harmonize_job(
            base_url=base_url,
            api_key=api_key,
            payload_gz=payload,
            timeout=timeout,
        )
    except httpx.TimeoutException as exc:
        logger.error("harmonize submit timeout: file=%s err=%s", csv_path, exc)
        raise HarmonizationJobError("harmonization submit request timed out") from exc
    except httpx.HTTPError as exc:
        logger.error("harmonize submit transport error: file=%s err=%s", csv_path, exc)
        raise NetriasAPIUnavailable(f"transport error: {exc}") from exc


def _ensure_submit_success(response: httpx.Response, csv_path: Path, logger: logging.Logger) -> None:
    if response.status_code < 400:
        return
    message, payload_for_log = _error_description(
        status=response.status_code,
        body_text=response.text,
        default="harmonization submit failed",
    )
    logger.error(
        "harmonize submit failed: file=%s status=%s body=%s",
        csv_path,
        response.status_code,
        _formatted_body(payload_for_log),
    )
    raise HarmonizationJobError(message)


def _require_job_id(
    payload: Mapping[str, JSONValue],
    csv_path: Path,
    logger: logging.Logger,
) -> str:
    job_id = _string_field(payload, "job_id")
    if job_id:
        return job_id
    logger.error("harmonize submit response missing job_id: file=%s body=%s", csv_path, payload)
    raise HarmonizationJobError("harmonization job response missing job_id")


async def _resolve_final_payload(
    base_url: str,
    api_key: str,
    job_id: str,
    timeout: float,
    csv_path: Path,
    logger: logging.Logger,
) -> Mapping[str, JSONValue]:
    started = time.monotonic()
    deadline = started + timeout
    poll_interval = max(1.0, min(JOB_POLL_INTERVAL_SECONDS, timeout / 60 if timeout else JOB_POLL_INTERVAL_SECONDS))

    while time.monotonic() < deadline:
        elapsed = time.monotonic() - started
        response = await _job_status_http(
            base_url=base_url,
            api_key=api_key,
            job_id=job_id,
            timeout=timeout,
            csv_path=csv_path,
            logger=logger,
        )

        payload = _interpret_job_status(response, csv_path, logger)
        if payload is None:
            logger.info(
                "harmonize job polling: file=%s job_id=%s status=pending elapsed=%.2fs",
                csv_path,
                job_id,
                elapsed,
            )
            await asyncio.sleep(poll_interval)
            continue
        logger.info(
            "harmonize job polling: file=%s job_id=%s status=%s elapsed=%.2fs",
            csv_path,
            job_id,
            payload.get("status"),
            elapsed,
        )
        return payload

    total_elapsed = time.monotonic() - started
    logger.error("harmonize job polling timed out: file=%s elapsed=%.2fs", csv_path, total_elapsed)
    raise HarmonizationJobError("harmonization job polling timed out")


async def _job_status_http(
    base_url: str,
    api_key: str,
    job_id: str,
    timeout: float,
    csv_path: Path,
    logger: logging.Logger,
) -> httpx.Response:
    try:
        return await fetch_job_status(
            base_url=base_url,
            api_key=api_key,
            job_id=job_id,
            timeout=timeout,
        )
    except httpx.TimeoutException as exc:
        logger.error("harmonize job status timeout: file=%s err=%s", csv_path, exc)
        raise HarmonizationJobError("harmonization job status timed out") from exc
    except httpx.HTTPError as exc:
        logger.error("harmonize job status transport error: file=%s err=%s", csv_path, exc)
        raise NetriasAPIUnavailable(f"transport error: {exc}") from exc


def _interpret_job_status(response: httpx.Response, csv_path: Path, logger: logging.Logger) -> Mapping[str, JSONValue] | None:
    if response.status_code == 404:
        return None

    payload = _validated_status_payload(response, csv_path, logger)
    state = _job_state(payload)
    if state == "FAILED":
        message = _job_failure_message(payload)
        logger.error("harmonize job failed: file=%s message=%s", csv_path, message)
        raise HarmonizationJobError(message)
    if state == "SUCCEEDED":
        return payload
    return None


def _validated_status_payload(response: httpx.Response, csv_path: Path, logger: logging.Logger) -> Mapping[str, JSONValue]:
    if response.status_code >= 400:
        message, payload_for_log = _error_description(
            status=response.status_code,
            body_text=response.text,
            default="harmonization job status failed",
        )
        logger.error(
            "harmonize job status failed: file=%s status=%s body=%s",
            csv_path,
            response.status_code,
            _formatted_body(payload_for_log),
        )
        raise HarmonizationJobError(message)

    payload = _json_mapping(response)
    if not payload:
        logger.error("harmonize job status response was not JSON: file=%s", csv_path)
        raise HarmonizationJobError("harmonization job status response was not JSON")
    return payload


def _job_state(payload: Mapping[str, JSONValue]) -> str:
    status_value = (_string_field(payload, "status") or "").upper()
    if status_value == "SUCCEEDED":
        return "SUCCEEDED"
    if status_value == "FAILED":
        return "FAILED"
    return "PENDING"


def _require_result_urls(
    payload: Mapping[str, JSONValue],
    csv_path: Path,
    logger: logging.Logger,
) -> tuple[str, str | None]:

    final_url = _string_field(payload, "final_url")
    manifest_url = _string_field(payload, "manifest_url")
    if final_url:
        return final_url, manifest_url
    logger.error("harmonize job missing final_url: file=%s payload=%s", csv_path, payload)
    raise HarmonizationJobError("harmonization job completed without a download URL")


def _manifest_destination(harmonized_dest: Path, manifest_url: str | None) -> Path | None:
    if manifest_url is None:
        return None
    parsed = urlparse(manifest_url)
    file_name = Path(parsed.path).name or f"{harmonized_dest.stem}_manifest.parquet"
    return harmonized_dest.parent / file_name


async def _download_outputs(
    final_url: str,
    manifest_url: str | None,
    dest: Path,
    timeout: float,
    csv_path: Path,
    logger: logging.Logger,
    job_id: str | None,
) -> HarmonizationResult:
    manifest_dest = _manifest_destination(dest, manifest_url)
    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(timeout)) as client:
            return await _download_csv_and_manifest(
                client, final_url, manifest_url, dest, manifest_dest, csv_path, logger, job_id
            )
    except httpx.HTTPError as exc:
        logger.error("harmonize download transport error: file=%s err=%s", csv_path, exc)
        raise NetriasAPIUnavailable(f"transport error: {exc}") from exc


async def _download_csv_and_manifest(
    client: httpx.AsyncClient,
    final_url: str,
    manifest_url: str | None,
    dest: Path,
    manifest_dest: Path | None,
    csv_path: Path,
    logger: logging.Logger,
    job_id: str | None,
) -> HarmonizationResult:
    """Download CSV and optionally manifest, returning appropriate result."""

    status, description = await _download_artifact(
        client=client,
        url=final_url,
        dest=dest,
        csv_path=csv_path,
        logger=logger,
        label="harmonized CSV",
    )
    if status != "succeeded":
        return HarmonizationResult(
            file_path=dest,
            manifest_path=manifest_dest,
            status=status,
            description=description,
            job_id=job_id,
        )

    if manifest_url and manifest_dest:
        manifest_status, manifest_description = await _download_artifact(
            client=client,
            url=manifest_url,
            dest=manifest_dest,
            csv_path=csv_path,
            logger=logger,
            label="manifest parquet",
        )
        if manifest_status != "succeeded":
            return HarmonizationResult(
                file_path=dest,
                manifest_path=manifest_dest,
                status=manifest_status,
                description=manifest_description,
                job_id=job_id,
            )

    logger.info(
        "harmonize complete: file=%s -> %s manifest=%s",
        csv_path,
        dest,
        manifest_dest if manifest_dest else "none",
    )
    return HarmonizationResult(
        file_path=dest,
        manifest_path=manifest_dest,
        status="succeeded",
        description="harmonization succeeded",
        job_id=job_id,
    )


async def _download_artifact(
    client: httpx.AsyncClient,
    url: str,
    dest: Path,
    csv_path: Path,
    logger: logging.Logger,
    label: str,
) -> tuple[Literal["succeeded", "failed", "timeout"], str]:
    try:
        async with client.stream("GET", url) as response:
            if 200 <= response.status_code < 300:
                _ = await stream_download_to_file(response, dest)
                logger.info("download complete: %s file=%s -> %s", label, csv_path, dest)
                return "succeeded", "harmonization succeeded"

            body_bytes = await response.aread()
            description = _download_error_message(response.status_code, body_bytes)
            logger.error(
                "harmonize download failed: artifact=%s file=%s status=%s body=%s",
                label,
                csv_path,
                response.status_code,
                _formatted_body(_payload_for_logging(body_bytes)),
            )
            return "failed", description
    except httpx.TimeoutException as exc:
        logger.error("harmonize download timeout: artifact=%s file=%s err=%s", label, csv_path, exc)
        return "timeout", "download timed out"
    except httpx.HTTPError as exc:
        logger.error("harmonize download transport error: artifact=%s file=%s err=%s", label, csv_path, exc)
        raise NetriasAPIUnavailable(f"transport error: {exc}") from exc


def _error_description(status: int, body_text: str, default: str) -> tuple[str, JSONValue | str]:
    parsed = _try_parse_json(body_text)
    message = _message_from_mapping(parsed if isinstance(parsed, Mapping) else None)
    if not message:
        hint = _failure_hint(status)
        if hint:
            message = hint
    description = message or default
    payload_for_log: JSONValue | str = parsed if parsed is not None else body_text
    return description, payload_for_log


def _json_mapping(response: httpx.Response) -> Mapping[str, JSONValue]:
    try:
        data = cast(object, response.json())
    except (json.JSONDecodeError, ValueError):
        return {}
    if isinstance(data, Mapping):
        return cast(Mapping[str, JSONValue], data)
    return {}


def _string_field(payload: Mapping[str, JSONValue], key: str) -> str | None:
    value = payload.get(key)
    if isinstance(value, str):
        stripped = value.strip()
        if stripped:
            return stripped
    return None


def _job_failure_message(payload: Mapping[str, JSONValue]) -> str:
    direct = _message_from_mapping(payload)
    if direct:
        return direct
    for key in ("statusReason", "failureReason", "errorMessage"):
        text = _string_field(payload, key)
        if text:
            return text
    return "harmonization job failed"


def _download_error_message(status: int, body: bytes) -> str:
    payload = _payload_for_logging(body)
    message = _message_from_mapping(payload if isinstance(payload, Mapping) else None)
    if message:
        return message
    hint = _failure_hint(status)
    if hint:
        return hint
    return f"harmonization download failed (HTTP {status})"


def _message_from_mapping(payload: Mapping[str, JSONValue] | None) -> str | None:
    direct = _direct_message(payload)
    if direct:
        return direct
    return _message_from_body_field(payload)


def _direct_message(payload: Mapping[str, JSONValue] | None) -> str | None:
    if payload is None:
        return None
    for key in _MESSAGE_KEYS:
        text = _coerce_message(payload.get(key))
        if text:
            return text
    return None


def _message_from_body_field(payload: Mapping[str, JSONValue] | None) -> str | None:
    body_mapping = _body_mapping(payload)
    if body_mapping is None:
        return None
    return _message_from_mapping(body_mapping)


def _coerce_message(value: JSONValue | None) -> str | None:
    if isinstance(value, str):
        stripped = value.strip()
        if stripped:
            return stripped
    return None


def _body_mapping(payload: Mapping[str, JSONValue] | None) -> Mapping[str, JSONValue] | None:
    if payload is None:
        return None
    body = payload.get("body")
    if isinstance(body, str):
        parsed = _try_parse_json(body)
        return parsed if isinstance(parsed, Mapping) else None
    if isinstance(body, Mapping):
        return cast(Mapping[str, JSONValue], body)
    return None


def _payload_for_logging(body: bytes) -> JSONValue | str:
    text = body.decode("utf-8", errors="replace")
    parsed = _try_parse_json(text)
    return parsed if parsed is not None else text


def _failure_hint(status: int) -> str | None:
    if status in {401, 403}:
        return "harmonization request was rejected (check API credentials and permissions)"
    if status == 404:
        return "harmonization endpoint not found (confirm base URL/path)"
    if 500 <= status < 600:
        return "harmonization service encountered an internal error"
    return None


def _formatted_body(payload: JSONValue | str) -> str:
    if isinstance(payload, str):
        return _formatted_string_body(payload)
    if isinstance(payload, (dict, list)):
        return _render_json(payload)
    return _truncate(str(payload))


def _formatted_string_body(raw: str) -> str:
    parsed = _try_parse_json(raw)
    if isinstance(parsed, (dict, list)):
        return _render_json(parsed)
    return _truncate(raw)


def _try_parse_json(raw: str) -> JSONValue | None:
    try:
        return cast(JSONValue, json.loads(raw))
    except Exception:
        return None


def _render_json(data: Mapping[str, JSONValue] | Sequence[JSONValue]) -> str:
    return _truncate(json.dumps(data, indent=2, sort_keys=True))


def _truncate(text: str, limit: int = 2000) -> str:
    if len(text) <= limit:
        return text
    return f"{text[: limit - 1]}…"
