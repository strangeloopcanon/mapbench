#!/usr/bin/env python3
"""Validate MapBench's public artifacts, provenance, and score arithmetic."""

from __future__ import annotations

import csv
import hashlib
import json
import statistics
import struct
import sys
from collections import Counter
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
IDS = [f"MB{index:03d}" for index in range(1, 41)]
WEIGHTS = {"spatial": 8, "factual": 5, "coverage": 3, "legibility": 4}
MEDIA_SUFFIXES = {"image/png": ".png", "image/jpeg": ".jpg"}


class ValidationError(RuntimeError):
    """A public release invariant did not hold."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def read_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as error:
        raise ValidationError(f"cannot read valid JSON from {path}: {error}") from error


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    try:
        lines = path.read_text().splitlines()
    except OSError as error:
        raise ValidationError(f"cannot read {path}: {error}") from error
    for line_number, line in enumerate(lines, 1):
        if not line.strip():
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError as error:
            raise ValidationError(f"invalid JSON at {path}:{line_number}: {error}") from error
    return records


def rounded(value: float) -> float:
    return float(Decimal(str(value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def release_path(relative_path: str) -> Path:
    path = (ROOT / relative_path).resolve()
    require(path.is_relative_to(ROOT), f"path escapes repository: {relative_path}")
    require(path.is_file(), f"missing release file: {relative_path}")
    return path


def image_info(path: Path) -> tuple[str, int, int]:
    with path.open("rb") as handle:
        signature = handle.read(8)
        if signature == b"\x89PNG\r\n\x1a\n":
            require(handle.read(4) == b"\x00\x00\x00\r", f"bad PNG IHDR length: {path}")
            require(handle.read(4) == b"IHDR", f"missing PNG IHDR: {path}")
            width, height = struct.unpack(">II", handle.read(8))
            require(width > 0 and height > 0, f"invalid PNG dimensions: {path}")
            return "image/png", width, height

        handle.seek(0)
        require(handle.read(2) == b"\xff\xd8", f"unsupported image encoding: {path}")
        while True:
            byte = handle.read(1)
            while byte != b"\xff":
                require(bool(byte), f"truncated JPEG: {path}")
                byte = handle.read(1)
            marker = handle.read(1)
            while marker == b"\xff":
                marker = handle.read(1)
            require(bool(marker), f"truncated JPEG marker: {path}")
            marker_value = marker[0]
            if marker_value in {0xD8, 0xD9} or 0xD0 <= marker_value <= 0xD7:
                continue
            length_bytes = handle.read(2)
            require(len(length_bytes) == 2, f"truncated JPEG segment: {path}")
            segment_length = struct.unpack(">H", length_bytes)[0]
            require(segment_length >= 2, f"invalid JPEG segment length: {path}")
            if marker_value in {
                0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
                0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF,
            }:
                require(len(handle.read(1)) == 1, f"truncated JPEG precision: {path}")
                dimensions = handle.read(4)
                require(len(dimensions) == 4, f"truncated JPEG dimensions: {path}")
                height, width = struct.unpack(">HH", dimensions)
                require(width > 0 and height > 0, f"invalid JPEG dimensions: {path}")
                return "image/jpeg", width, height
            handle.seek(segment_length - 2, 1)


def band(score: float) -> str:
    if score >= 90:
        return "excellent"
    if score >= 75:
        return "good"
    if score >= 60:
        return "usable_draft"
    if score >= 40:
        return "misleading"
    if score >= 21:
        return "substantive_failure"
    return "not_usable"


def validate_tasks() -> dict[str, dict[str, Any]]:
    records = read_jsonl(ROOT / "benchmark/tasks.jsonl")
    require([record.get("id") for record in records] == IDS, "task IDs must be MB001-MB040")
    tasks = {record["id"]: record for record in records}
    for record in records:
        require(record.get("reference_supplied_to_generator") is False, f"reference flag set for {record['id']}")
        prompt_path = release_path(record["prompt_file"])
        require(prompt_path.name.startswith(f"{record['id']}-"), f"prompt filename mismatch for {record['id']}")
        prompt = prompt_path.read_text()
        require(record["subject"].casefold() in prompt.casefold(), f"task subject missing from prompt for {record['id']}")
        require("no reference image is provided" in prompt, f"no-reference clause missing for {record['id']}")
    return tasks


def validate_manifest(path: Path, expected_prefix: str) -> list[dict[str, Any]]:
    records = read_jsonl(path)
    require([record.get("id") for record in records] == IDS, f"manifest IDs out of order: {path}")
    require(len({record.get("image_sha256") for record in records}) == 40, f"duplicate image hashes: {path}")
    forbidden = {"conversation_id", "trace_file", "permission_mode"}

    for record in records:
        item_id = record["id"]
        require(not (forbidden & set(record)), f"private execution fields in {path.name}:{item_id}")
        require(record["file"].startswith(expected_prefix), f"wrong output prefix for {item_id}")
        image_path = release_path(record["file"])
        prompt_path = release_path(record["prompt_file"])
        require(sha256(image_path) == record["image_sha256"], f"image hash mismatch for {item_id}")
        require(sha256(prompt_path) == record["prompt_sha256"], f"prompt hash mismatch for {item_id}")
        require(record.get("reference_image_supplied") is False, f"reference supplied for {item_id}")
        require(record.get("generation_calls") == 1, f"generation call count is not one for {item_id}")
        require(record.get("corrective_iterations") == 0, f"corrective iteration recorded for {item_id}")
        media_type, width, height = image_info(image_path)
        require(record.get("media_type") == media_type, f"media type mismatch for {item_id}")
        require(image_path.suffix.lower() == MEDIA_SUFFIXES[media_type], f"extension mismatch for {item_id}")
        require((width, height) == (record["width"], record["height"]), f"dimension mismatch for {item_id}")
    return records


def validate_score_record(record: dict[str, Any], allow_half_points: bool) -> None:
    item_id = record.get("id", "unknown")
    require(set(record.get("scores", {})) == set(WEIGHTS), f"score dimensions wrong for {item_id}")
    for key, score in record["scores"].items():
        require(isinstance(score, (int, float)) and 0 <= score <= 5, f"{key} score out of range for {item_id}")
        multiplier = 2 if allow_half_points else 1
        require(float(score * multiplier).is_integer(), f"unsupported score precision for {item_id}:{key}")
    raw_total = rounded(sum(WEIGHTS[key] * record["scores"][key] for key in WEIGHTS))
    require(record.get("raw_total") == raw_total, f"raw score arithmetic wrong for {item_id}")
    require(record.get("cap") in {20, 39, 59, 74, 100}, f"invalid cap for {item_id}")
    require(record.get("total") == min(raw_total, record["cap"]), f"final score arithmetic wrong for {item_id}")
    errors = record.get("material_errors")
    require(isinstance(errors, list), f"material errors missing for {item_id}")
    require(all(error.get("dimension") in WEIGHTS and error.get("description", "").strip() for error in errors), f"bad material error for {item_id}")
    if record["cap"] == 100:
        require(not errors, f"uncapped record contains material errors for {item_id}")
    elif record["cap"] == 74:
        require(len(errors) == 1, f"one-error cap does not have one error for {item_id}")
    elif record["cap"] == 59:
        require(len(errors) >= 2, f"multiple-error cap lacks multiple errors for {item_id}")
    else:
        require(bool(errors), f"failure cap lacks a material error for {item_id}")
    if "band" in record:
        require(record["band"] == band(record["total"]), f"band mismatch for {item_id}")


def validate_summary(aggregate: dict[str, Any], records: list[dict[str, Any]]) -> None:
    summary = aggregate["summary"]
    totals = [record["total"] for record in records]
    raw_totals = [record["raw_total"] for record in records]
    require(summary["final_mean"] == rounded(statistics.mean(totals)), "final mean mismatch")
    require(summary["final_median"] == rounded(statistics.median(totals)), "final median mismatch")
    require(summary["raw_mean"] == rounded(statistics.mean(raw_totals)), "raw mean mismatch")
    require(summary["maps_with_material_errors"] == sum(bool(record["material_errors"]) for record in records), "map error count mismatch")
    require(summary["material_error_count"] == sum(len(record["material_errors"]) for record in records), "material error total mismatch")
    expected_by_dimension = {
        key: sum(error["dimension"] == key for record in records for error in record["material_errors"])
        for key in WEIGHTS
    }
    require(summary["material_errors_by_dimension"] == expected_by_dimension, "material errors by dimension mismatch")
    expected_bands = dict(Counter(band(record["total"]) for record in records))
    require(summary["band_counts"] == expected_bands, "band counts mismatch")
    dimension_means = {
        key: rounded(statistics.mean(record["scores"][key] for record in records)) for key in WEIGHTS
    }
    published_dimensions = aggregate.get("dimension_means", summary.get("dimension_means"))
    require(published_dimensions == dimension_means, "dimension means mismatch")


def validate_aggregate(path: Path, allow_half_points: bool) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    aggregate = read_json(path)
    records = aggregate.get("ranking", [])
    require(aggregate.get("map_count") == 40 and len(records) == 40, f"aggregate map count wrong: {path}")
    require(len({record.get("id") for record in records}) == 40, f"duplicate aggregate IDs: {path}")
    for record in records:
        validate_score_record(record, allow_half_points)
    expected = sorted(records, key=lambda record: (-record["total"], -record["raw_total"], record["id"]))
    require([record["id"] for record in records] == [record["id"] for record in expected], f"ranking order wrong: {path}")
    require([record.get("rank") for record in records] == list(range(1, 41)), f"rank numbers wrong: {path}")
    validate_summary(aggregate, records)
    return aggregate, records


def validate_codex_judges(records: list[dict[str, Any]]) -> None:
    judge_directory = ROOT / "results/codex-image/judges"
    cohorts = (
        (
            IDS[:20],
            judge_directory / "baseline-sol-medium.jsonl",
            judge_directory / "baseline-terra-high.jsonl",
            judge_directory / "baseline-adjudication-sol-high.jsonl",
        ),
        (
            IDS[20:],
            judge_directory / "extension-sol-medium.jsonl",
            judge_directory / "extension-terra-high.jsonl",
            judge_directory / "extension-adjudication-sol-high.jsonl",
        ),
    )
    sol_records: dict[str, dict[str, Any]] = {}
    terra_records: dict[str, dict[str, Any]] = {}
    adjudications: dict[str, dict[str, Any]] = {}

    for expected_ids, sol_path, terra_path, adjudication_path in cohorts:
        sol_cohort = read_jsonl(sol_path)
        terra_cohort = read_jsonl(terra_path)
        adjudication_cohort = read_jsonl(adjudication_path)
        require([record.get("id") for record in sol_cohort] == expected_ids, f"judge IDs out of order: {sol_path}")
        require([record.get("id") for record in terra_cohort] == expected_ids, f"judge IDs out of order: {terra_path}")
        require(
            all(record.get("id") in expected_ids for record in adjudication_cohort),
            f"adjudication ID outside cohort: {adjudication_path}",
        )
        for record in sol_cohort + terra_cohort + adjudication_cohort:
            validate_score_record(record, allow_half_points=False)
        sol_records.update({record["id"]: record for record in sol_cohort})
        terra_records.update({record["id"]: record for record in terra_cohort})
        adjudications.update({record["id"]: record for record in adjudication_cohort})

    require(len(adjudications) == 30, "Codex adjudication count must be 30")
    for record in records:
        item_id = record["id"]
        sol = sol_records[item_id]
        terra = terra_records[item_id]
        expected_judge_scores = {"sol_medium": sol["total"], "terra_high": terra["total"]}
        expected_judge_raw_scores = {"sol_medium": sol["raw_total"], "terra_high": terra["raw_total"]}
        require(record["initial_final_gap"] == abs(sol["total"] - terra["total"]), f"initial final gap mismatch for {item_id}")
        require(record["initial_raw_gap"] == abs(sol["raw_total"] - terra["raw_total"]), f"initial raw gap mismatch for {item_id}")

        if record["final_source"] == "sol-high-adjudication":
            require(item_id in adjudications, f"missing adjudication for {item_id}")
            adjudication = adjudications[item_id]
            expected_judge_scores["sol_high_adjudicator"] = adjudication["total"]
            expected_judge_raw_scores["sol_high_adjudicator"] = adjudication["raw_total"]
            for key in ("scores", "raw_total", "cap", "cap_reason", "total", "material_errors", "summary"):
                require(record[key] == adjudication[key], f"adjudication/aggregate drift for {item_id}:{key}")
        elif record["final_source"] == "two-judge-mean":
            require(item_id not in adjudications, f"unused adjudication present for {item_id}")
            require(sol["cap"] == terra["cap"] == record["cap"], f"non-adjudicated cap disagreement for {item_id}")
            require(
                len(sol["material_errors"]) == len(terra["material_errors"]) == len(record["material_errors"]),
                f"non-adjudicated material-error count disagreement for {item_id}",
            )
            expected_scores = {key: (sol["scores"][key] + terra["scores"][key]) / 2 for key in WEIGHTS}
            require(record["scores"] == expected_scores, f"two-judge mean mismatch for {item_id}")
            if item_id >= "MB021":
                require(record["cap"] == 100 and not record["material_errors"], f"hard-extension mean violates protocol for {item_id}")
        else:
            raise ValidationError(f"unknown Codex final source for {item_id}")

        require(record["judge_scores"] == expected_judge_scores, f"judge final-score projection mismatch for {item_id}")
        require(record["judge_raw_scores"] == expected_judge_raw_scores, f"judge raw-score projection mismatch for {item_id}")

    require(set(adjudications) == {record["id"] for record in records if record["final_source"] == "sol-high-adjudication"}, "adjudication set does not match aggregate sources")


def as_number(value: str) -> float:
    return float(value)


def validate_csv(path: Path, records: list[dict[str, Any]], system: str) -> None:
    with path.open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    require(len(rows) == 40, f"CSV row count wrong: {path}")
    require([row["id"] for row in rows] == [record["id"] for record in records], f"CSV IDs do not match ranking: {path}")
    final_key, raw_key = ("final_score", "raw_score") if system == "codex" else ("gemini_final", "gemini_raw")
    for row, record in zip(rows, records):
        require(int(row["rank"]) == record["rank"], f"CSV rank mismatch for {record['id']}")
        require(as_number(row[final_key]) == record["total"], f"CSV final score mismatch for {record['id']}")
        require(as_number(row[raw_key]) == record["raw_total"], f"CSV raw score mismatch for {record['id']}")
        require(row["band"] == band(record["total"]), f"CSV band mismatch for {record['id']}")
        require(int(row["material_error_count"]) == len(record["material_errors"]), f"CSV error count mismatch for {record['id']}")
        for key in WEIGHTS:
            require(as_number(row[key]) == record["scores"][key], f"CSV {key} mismatch for {record['id']}")


def validate_reference_manifest() -> None:
    records = read_jsonl(ROOT / "sources/reference-manifest.jsonl")
    require([record.get("id") for record in records] == IDS, "reference manifest IDs must be MB001-MB040")
    for record in records:
        item_id = record["id"]
        require(record.get("source_page", "").startswith("https://"), f"bad reference URL for {item_id}")
        require(record.get("normalized_width", record.get("width", 0)) > 0, f"missing reference width for {item_id}")
        require(record.get("normalized_height", record.get("height", 0)) > 0, f"missing reference height for {item_id}")
        digest = record.get("normalized_sha256", "")
        require(len(digest) == 64 and all(character in "0123456789abcdef" for character in digest), f"bad reference hash for {item_id}")
        require("not supplied to generator" in record.get("use", ""), f"bad reference-use declaration for {item_id}")


def validate_contact_sheets() -> None:
    for relative_path in (
        "results/codex-image/contact-sheet.jpg",
        "results/gemini-agent-image/contact-sheet.png",
    ):
        path = release_path(relative_path)
        media_type, width, height = image_info(path)
        require(path.suffix == MEDIA_SUFFIXES[media_type], f"contact-sheet extension mismatch: {relative_path}")
        require(width >= 1000 and height >= 1000, f"contact sheet unexpectedly small: {relative_path}")


def validate_public_claims(codex: dict[str, Any], gemini: dict[str, Any]) -> None:
    readme = (ROOT / "README.md").read_text()
    codex_mean = f"{codex['summary']['final_mean']:.2f}"
    gemini_mean = f"{gemini['summary']['final_mean']:.2f}"
    require(codex_mean in readme and gemini_mean in readme, "README headline scores are stale")
    require("exploratory diagnostics, not a controlled model ranking" in readme, "README comparison caveat missing")
    gemini_report = (ROOT / "results/gemini-agent-image/report.md").read_text()
    require("exploratory" in gemini_report.casefold(), "Gemini comparison caveat missing")


def main() -> None:
    validate_tasks()
    validate_manifest(ROOT / "results/codex-image/manifest.jsonl", "results/codex-image/generated/")
    validate_manifest(ROOT / "results/gemini-agent-image/manifest.jsonl", "results/gemini-agent-image/generated/")
    codex, codex_records = validate_aggregate(ROOT / "results/codex-image/aggregate.json", allow_half_points=True)
    gemini, gemini_records = validate_aggregate(ROOT / "results/gemini-agent-image/aggregate.json", allow_half_points=False)
    validate_codex_judges(codex_records)

    gemini_evaluations = read_jsonl(ROOT / "results/gemini-agent-image/evaluations.jsonl")
    require([record.get("id") for record in gemini_evaluations] == IDS, "Gemini evaluation IDs out of order")
    for record in gemini_evaluations:
        validate_score_record(record, allow_half_points=False)
    aggregate_by_id = {record["id"]: record for record in gemini_records}
    for record in gemini_evaluations:
        aggregate_record = aggregate_by_id[record["id"]]
        for key in ("scores", "raw_total", "material_errors", "cap", "total", "summary"):
            require(record[key] == aggregate_record[key], f"Gemini evaluation/aggregate drift for {record['id']}:{key}")

    validate_csv(ROOT / "results/codex-image/per-map.csv", codex_records, "codex")
    validate_csv(ROOT / "results/gemini-agent-image/per-map.csv", gemini_records, "gemini")
    validate_reference_manifest()
    validate_contact_sheets()
    validate_public_claims(codex, gemini)
    print("MapBench release validation passed: 40 tasks and two complete generation runs.")


if __name__ == "__main__":
    try:
        main()
    except (ValidationError, OSError, KeyError, TypeError, ValueError) as error:
        print(f"MapBench release validation failed: {error}", file=sys.stderr)
        raise SystemExit(1) from error
