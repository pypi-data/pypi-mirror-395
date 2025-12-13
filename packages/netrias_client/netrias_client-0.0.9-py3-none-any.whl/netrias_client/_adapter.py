"""Translate discovery results into harmonization CDE maps.

'why': bridge API recommendations to harmonization CDE maps while respecting confidence bounds
"""
from __future__ import annotations

import json
import logging
from collections.abc import Iterable, Mapping
from pathlib import Path
from typing import Final, cast

from ._models import MappingDiscoveryResult, MappingRecommendationOption, MappingSuggestion



def build_column_mapping_payload(
    result: MappingDiscoveryResult,
    threshold: float,
    logger: logging.Logger | None = None,
) -> dict[str, dict[str, dict[str, object]]]:
    """Convert discovery output into the CDE map structure expected by harmonization."""

    active_logger = logger or logging.getLogger("netrias_client")
    strongest = strongest_targets(result, threshold=threshold, logger=active_logger)
    return {"column_mappings": _column_entries(strongest, active_logger)}


_COLUMN_METADATA: Final[dict[str, dict[str, object]]] = {
    "therapeutic_agents": {
      "route": "sagemaker:therapeutic_agents",
      "targetField": "therapeutic_agents",
      "cdeId": 1,
      "cde_id": 1
    },
    "primary_diagnosis": {
      "route": "sagemaker:primary",
      "targetField": "primary_diagnosis",
      "cdeId": 2,
      "cde_id": 2
    },
    "morphology": {
      "route": "sagemaker:morphology",
      "targetField": "morphology",
      "cdeId": 3,
      "cde_id": 3
    },
    "sample_anatomic_site": {
      "route": "sagemaker:sample_anatomic_site",
      "targetField": "sample_anatomic_site",
      "cdeId": 5,
      "cde_id": 5
    },
    "tissue_or_organ_of_origin": {
      "route": "sagemaker:tissue_or_organ_of_origin",
      "targetField": "tissue_or_organ_of_origin",
      "cdeId": 4,
      "cde_id": 4
    }
}
    # "study_name": {"route": "api:passthrough", "targetField": "study_name"},
    # "number_of_participants": {"route": "api:passthrough", "targetField": "number_of_participants"},
    # "number_of_samples": {"route": "api:passthrough", "targetField": "number_of_samples"},
    # "study_data_types": {
    #     "route": "api:passthrough",
    #     "targetField": "study_data_types",
    #     "cdeId": 12_571_096,
    #     "cde_id": 12_571_096,
    # },
    # "participant_id": {"route": "api:passthrough", "targetField": "participant_id"},
    # "sample_id": {"route": "api:passthrough", "targetField": "sample_id"},
    # "file_name": {"route": "api:passthrough", "targetField": "file_name"},
    # "primary_diagnosis": {
    #     "route": "sagemaker:primary",
    #     "targetField": "primary_diagnosis",
    #     "cdeId": -200,
    #     "cde_id": -200,
    # },
    # "therapeutic_agents": {
    #     "route": "sagemaker:therapeutic_agents",
    #     "targetField": "therapeutic_agents",
    #     "cdeId": -203,
    #     "cde_id": -203,
    # },
    # "morphology": {
    #     "route": "sagemaker:morphology",
    #     "targetField": "morphology",
    #     "cdeId": -201,
    #     "cde_id": -201,
    # },
    # "tissue_or_organ_of_origin": {
    #     "route": "sagemaker:tissue_origin",
    #     "targetField": "tissue_or_organ_of_origin",
    #     "cdeId": -204,
    #     "cde_id": -204,
    # },
    # "site_of_resection_or_biopsy": {
    #     "route": "sagemaker:sample_anatomic_site",
    #     "targetField": "site_of_resection_or_biopsy",
    #     "cdeId": -202,
    #     "cde_id": -202,
    # },
# }


def strongest_targets(
    result: MappingDiscoveryResult,
    threshold: float,
    logger: logging.Logger,
) -> dict[str, str]:
    """Return the highest-confidence target per column, filtered by threshold."""

    if result.suggestions:
        all_targets, all_confidences = _from_suggestions_unfiltered(result.suggestions)
        selected, confidences = _from_suggestions(result.suggestions, threshold)
    else:
        all_targets, all_confidences = _from_raw_payload_unfiltered(result.raw)
        selected, confidences = _from_raw_payload(result.raw, threshold)

    _log_target_selection(logger, all_targets, all_confidences, selected, confidences, threshold)
    return selected


def _log_target_selection(
    logger: logging.Logger,
    all_targets: dict[str, str],
    all_confidences: dict[str, float],
    selected: dict[str, str],
    confidences: dict[str, float],
    threshold: float,
) -> None:
    """Log all discovered mappings, filtered results, and what was filtered out."""

    if all_targets:
        all_with_scores = {col: f"{target} (confidence: {all_confidences.get(col, 'N/A')})"
                          for col, target in all_targets.items()}
        logger.info("adapter all discovered mappings (pre-filter): %s", all_with_scores)

    if selected:
        targets_with_scores = {col: f"{target} (confidence: {confidences.get(col, 'N/A')})"
                               for col, target in selected.items()}
        logger.info("adapter strongest targets (threshold >= %.2f): %s", threshold, targets_with_scores)
    else:
        logger.warning("adapter strongest targets empty after filtering (threshold=%.2f)", threshold)

    filtered_out = {col: f"{all_targets[col]} (confidence: {all_confidences.get(col, 'N/A')})"
                   for col in all_targets if col not in selected}
    if filtered_out:
        logger.info("adapter filtered out (below threshold): %s", filtered_out)


def _column_entries(
    strongest: Mapping[str, str],
    logger: logging.Logger,
) -> dict[str, dict[str, object]]:
    entries: dict[str, dict[str, object]] = {}
    missing_cde: list[str] = []
    recognized_mappings: dict[str, int] = {}

    for source, target in strongest.items():
        entry = _initial_entry(source, target)
        _track_cde_status(entry, source, missing_cde, recognized_mappings)
        entries[source] = entry

    _apply_metadata_defaults(entries)
    _log_cde_tracking(logger, recognized_mappings, missing_cde)
    return entries


def _track_cde_status(
    entry: dict[str, object],
    source: str,
    missing_cde: list[str],
    recognized_mappings: dict[str, int],
) -> None:
    """Track whether entry has a CDE id or is unresolved."""

    if _needs_cde(entry):
        missing_cde.append(source)
    else:
        cde_id = entry.get("cdeId") or entry.get("cde_id")
        if isinstance(cde_id, int):
            recognized_mappings[source] = cde_id


def _log_cde_tracking(
    logger: logging.Logger,
    recognized_mappings: dict[str, int],
    missing_cde: list[str],
) -> None:
    """Log recognized and unresolved CDE mappings."""

    if recognized_mappings:
        logger.info("adapter recognized mappings (column -> CDE id): %s", recognized_mappings)
    if missing_cde:
        logger.info("adapter unresolved targets (no CDE id mapping): %s", missing_cde)


def _initial_entry(source: str, target: str) -> dict[str, object]:
    metadata = _COLUMN_METADATA.get(source)
    if metadata is None:
        return {"targetField": target}
    # Preserve configured targetField when metadata defines it.
    return dict(metadata)


def _needs_cde(entry: Mapping[str, object]) -> bool:
    return "cdeId" not in entry


def _apply_metadata_defaults(entries: dict[str, dict[str, object]]) -> None:
    for source, metadata in _COLUMN_METADATA.items():
        if source not in entries:
            entries[source] = dict(metadata)


def _from_suggestions_unfiltered(
    suggestions: Iterable[MappingSuggestion]
) -> tuple[dict[str, str], dict[str, float]]:
    """Get all recommendations without filtering by threshold."""
    strongest: dict[str, str] = {}
    confidences: dict[str, float] = {}
    for suggestion in suggestions:
        option = _top_option_unfiltered(suggestion.options)
        if option is None or option.target is None:
            continue
        strongest[suggestion.source_column] = option.target
        if option.confidence is not None:
            confidences[suggestion.source_column] = option.confidence
    return strongest, confidences


def _from_suggestions(
    suggestions: Iterable[MappingSuggestion], threshold: float
) -> tuple[dict[str, str], dict[str, float]]:
    strongest: dict[str, str] = {}
    confidences: dict[str, float] = {}
    for suggestion in suggestions:
        option = _top_option(suggestion.options, threshold)
        if option is None or option.target is None:
            continue
        strongest[suggestion.source_column] = option.target
        if option.confidence is not None:
            confidences[suggestion.source_column] = option.confidence
    return strongest, confidences


def _from_raw_payload_unfiltered(payload: Mapping[str, object]) -> tuple[dict[str, str], dict[str, float]]:
    """Get all recommendations from raw payload without filtering by threshold."""
    strongest: dict[str, str] = {}
    confidences: dict[str, float] = {}
    for column, value in payload.items():
        options = _coerce_options(value)
        option = _top_option_unfiltered(options)
        if option is None or option.target is None:
            continue
        strongest[column] = option.target
        if option.confidence is not None:
            confidences[column] = option.confidence
    return strongest, confidences


def _from_raw_payload(payload: Mapping[str, object], threshold: float) -> tuple[dict[str, str], dict[str, float]]:
    strongest: dict[str, str] = {}
    confidences: dict[str, float] = {}
    for column, value in payload.items():
        options = _coerce_options(value)
        option = _top_option(options, threshold)
        if option is None or option.target is None:
            continue
        strongest[column] = option.target
        if option.confidence is not None:
            confidences[column] = option.confidence
    return strongest, confidences


def _coerce_options(value: object) -> tuple[MappingRecommendationOption, ...]:
    if not isinstance(value, list):
        return ()
    return tuple(_option_iterator(cast(list[object], value)))


def _option_iterator(items: list[object]) -> Iterable[MappingRecommendationOption]:
    for item in items:
        if not isinstance(item, Mapping):
            continue
        option = _option_from_mapping(cast(Mapping[str, object], item))
        if option is not None:
            yield option


def _option_from_mapping(item: Mapping[str, object]) -> MappingRecommendationOption | None:
    target = item.get("target")
    if not isinstance(target, str):
        return None
    similarity = item.get("similarity")
    score: float | None = None
    if isinstance(similarity, (float, int)):
        score = float(similarity)
    return MappingRecommendationOption(target=target, confidence=score, raw=item)


def _top_option_unfiltered(
    options: Iterable[MappingRecommendationOption]
) -> MappingRecommendationOption | None:
    """Return the highest-confidence option without filtering by threshold."""
    options_list = list(options)
    if not options_list:
        return None
    return max(options_list, key=lambda opt: opt.confidence or float("-inf"))


def _top_option(
    options: Iterable[MappingRecommendationOption], threshold: float
) -> MappingRecommendationOption | None:
    eligible = [opt for opt in options if _meets_threshold(opt, threshold)]
    if not eligible:
        return None
    return max(eligible, key=lambda opt: opt.confidence or float("-inf"))


def _meets_threshold(option: MappingRecommendationOption, threshold: float) -> bool:
    score = option.confidence
    if score is None:
        return False
    return score >= threshold

def normalize_cde_map(
    cde_map: Path | Mapping[str, object] | None,
) -> dict[str, int]:
    """Normalize CDE map column→CDE entries for harmonization payloads."""

    if cde_map is None:
        return {}
    raw = _load_cde_map_raw(cde_map)
    mapping = _mapping_dict(raw)
    normalized: dict[str, int] = {}
    for field, value in mapping.items():
        _apply_cde_entry(normalized, field, value)
    return normalized


def _load_cde_map_raw(cde_map: Path | Mapping[str, object]) -> Mapping[str, object]:
    if isinstance(cde_map, Path):
        content = cde_map.read_text(encoding="utf-8")
        try:
            return cast(Mapping[str, object], json.loads(content))
        except json.JSONDecodeError as exc:
            raise ValueError(f"cde_map must be valid JSON: {exc}") from exc
    return cde_map


def _mapping_dict(raw: Mapping[str, object]) -> dict[str, object]:
    mapping = _dict_if_str_mapping(raw)
    if mapping is None:
        return {}
    candidate = _dict_if_str_mapping(mapping.get("column_mappings"))
    return candidate if candidate is not None else mapping


def _dict_if_str_mapping(value: object) -> dict[str, object] | None:
    if isinstance(value, Mapping):
        typed = cast(Mapping[str, object], value)
        return dict(typed)
    return None


def _apply_cde_entry(destination: dict[str, int], field: object, value: object) -> None:
    name = _clean_field(field)
    cde_id = _coerce_cde_id(value)
    if name is None or cde_id is None:
        return
    destination[name] = cde_id


def _clean_field(field: object) -> str | None:
    if not isinstance(field, str):
        return None
    name = field.strip()
    return name or None


def _coerce_cde_id(value: object) -> int | None:
    candidate = _cde_candidate(value)
    if candidate is None:
        return None
    return _int_from_candidate(candidate)


def _cde_candidate(value: object) -> object | None:
    mapping = _dict_if_str_mapping(value)
    if mapping is not None:
        return mapping.get("cdeId") or mapping.get("cde_id")
    return value


def _int_from_candidate(candidate: object) -> int | None:
    if isinstance(candidate, bool):
        return int(candidate)
    if isinstance(candidate, (int, float)):
        return _int_from_number(candidate)
    if isinstance(candidate, str):
        return _int_from_string(candidate)
    return None


def _int_from_number(value: int | float) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _int_from_string(value: str) -> int | None:
    stripped = value.strip()
    if not stripped:
        return None
    try:
        return int(stripped)
    except ValueError:
        return None
