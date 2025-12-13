from __future__ import annotations

import argparse
import importlib
import json
import os
import sys
from collections.abc import Mapping, Sequence
from contextlib import suppress
from pathlib import Path
from types import SimpleNamespace
from typing import IO, Protocol, cast

if __package__ in {None, ""}:  # pragma: no cover - executed when run as a script
    sys.path.append(str(Path(__file__).resolve().parent.parent))

from x_make_common_x.json_contracts import validate_payload
from x_make_yahw_x.json_contracts import ERROR_SCHEMA, INPUT_SCHEMA, OUTPUT_SCHEMA
from x_make_yahw_x.projection import (
    ExecutionPolicy,
    ProjectionDataBundle,
    ProjectionEdge,
    ProjectionNetwork,
    ProjectionNode,
    ProjectionOrigin,
    ProjectionResources,
    ProjectionSnapshot,
    ProjectionTelemetry,
    write_snapshot,
)


class _SchemaValidationError(Exception):
    message: str
    path: tuple[object, ...]
    schema_path: tuple[object, ...]


class _JsonSchemaModule(Protocol):
    ValidationError: type[_SchemaValidationError]


def _load_validation_error() -> type[_SchemaValidationError]:
    module = cast("_JsonSchemaModule", importlib.import_module("jsonschema"))
    return module.ValidationError


ValidationErrorType: type[_SchemaValidationError] = _load_validation_error()


RUN_DIR_ENV_VAR = "RUN_ALL_RUN_DIR"
_SMOKE_PLAN_NAMES = {"yahw_smoke", "astral_demo"}


class XClsMakeYahwX:
    def __init__(self, ctx: object | None = None) -> None:
        # store optional orchestrator context for backward-compatible upgrades
        self._ctx = ctx

    def run(self) -> str:
        return "Hello world!"


def main() -> str:
    return XClsMakeYahwX().run()


SCHEMA_VERSION = "x_make_yahw_x.run/1.0"


def _failure_payload(
    message: str, *, details: Mapping[str, object] | None = None
) -> dict[str, object]:
    payload: dict[str, object] = {"status": "failure", "message": message}
    if details:
        payload["details"] = dict(details)
    with suppress(ValidationErrorType):
        validate_payload(payload, ERROR_SCHEMA)
    return payload


def _build_context(
    ctx: object | None, overrides: Mapping[str, object] | None
) -> object | None:
    if not overrides:
        return ctx
    namespace = SimpleNamespace(**{str(key): value for key, value in overrides.items()})
    if ctx is not None:
        namespace.parent_ctx = ctx
    return namespace


def _maybe_generate_projection(
    context_mapping: Mapping[str, object] | None,
) -> tuple[Path, str] | None:
    if not context_mapping:
        return None
    plan_obj = context_mapping.get("plan")
    plan_raw = str(plan_obj).strip() if isinstance(plan_obj, str) else None
    plan_value = plan_raw.lower() if plan_raw else None
    if not plan_value:
        return None

    canonical_plan = None
    for known in _SMOKE_PLAN_NAMES:
        if (
            plan_value == known
            or plan_value.endswith(f"/{known}")
            or known in plan_value
        ):
            canonical_plan = known
            break
    if canonical_plan is None:
        return None

    run_dir_raw = os.environ.get(RUN_DIR_ENV_VAR)
    if not run_dir_raw or not Path(run_dir_raw).exists():
        return None
    run_dir = Path(run_dir_raw)
    try:
        snapshot = _build_demo_snapshot(canonical_plan)
        snapshot_path = run_dir / f"astral_projection_{canonical_plan}.json"
        write_snapshot(snapshot, snapshot_path)
    except (OSError, RuntimeError, ValueError):  # pragma: no cover - demo best-effort
        return None
    return snapshot_path, canonical_plan


def _build_demo_snapshot(plan_name: str) -> ProjectionSnapshot:
    begin = ProjectionNode(
        id="seed",
        form="Form_1",
        operation="emit_seed",
        module="x_make_yahw_x.demo",
        parameters={"count": 3},
        traits=("stateless",),
    )
    worker = ProjectionNode(
        id="amplifier",
        form="Form_2",
        operation="amplify",
        module="x_make_yahw_x.demo",
        parameters={"factor": 2},
    )
    collector = ProjectionNode(
        id="collector",
        form="Form_3",
        operation="collect",
        module="x_make_yahw_x.demo",
    )

    network = ProjectionNetwork(
        nodes=(begin, worker, collector),
        edges=(
            ProjectionEdge(source="seed", target="amplifier", channel="sequence"),
            ProjectionEdge(source="amplifier", target="collector", channel="results"),
        ),
        entrypoints=("seed",),
        sinks=("collector",),
        execution_policy=ExecutionPolicy(batch_size=8, concurrency="sequential"),
    )

    origin = ProjectionOrigin(
        workspace_root=str(Path.cwd()),
        orchestrator="x_0_run_all_x",
        git_revision=None,
        extras={"plan": plan_name},
    )

    resources = ProjectionResources(
        python_requirements=("x_make_yahw_x",),
        data_bundles=(
            ProjectionDataBundle(
                id="demo_payload",
                bundle_type="json",
                description="Synthetic payload captured during YAHW smoke plan",
            ),
        ),
    )

    telemetry = ProjectionTelemetry(events=True, metrics=True, log_level="INFO")

    snapshot_id = f"yahw_demo_{plan_name}".replace("-", "_")
    description = "Demo astral snapshot emitted by YAHW smoke run"
    return ProjectionSnapshot(
        id=snapshot_id,
        origin=origin,
        network=network,
        resources=resources,
        telemetry=telemetry,
        description=description,
    )


def main_json(
    payload: Mapping[str, object], *, ctx: object | None = None
) -> dict[str, object]:
    try:
        validate_payload(payload, INPUT_SCHEMA)
    except ValidationErrorType as exc:
        return _failure_payload(
            "input payload failed validation",
            details={
                "error": exc.message,
                "path": [str(part) for part in exc.path],
                "schema_path": [str(part) for part in exc.schema_path],
            },
        )

    parameters_obj = payload.get("parameters", {})
    parameters = cast("Mapping[str, object]", parameters_obj)
    context_obj = parameters.get("context")
    context_mapping = cast(
        "Mapping[str, object] | None",
        context_obj if isinstance(context_obj, Mapping) else None,
    )

    runtime_ctx = _build_context(ctx, context_mapping)

    try:
        runner = XClsMakeYahwX(ctx=runtime_ctx)
        message = runner.run()
    except Exception as exc:  # noqa: BLE001
        return _failure_payload(
            "yahw execution failed",
            details={"error": str(exc)},
        )

    if not isinstance(message, str) or not message.strip():
        return _failure_payload(
            "yahw returned an empty message",
            details={"result": message},
        )

    metadata: dict[str, object] = {}
    if context_mapping:
        context_keys = tuple(sorted(str(key) for key in context_mapping))
        metadata["context_keys"] = list(context_keys)
        metadata["context_entries"] = len(context_keys)
    projection_result = _maybe_generate_projection(context_mapping)
    if projection_result is not None:
        snapshot_path, plan_name = projection_result
        metadata["projection_snapshot"] = str(snapshot_path)
        metadata["projection_plan"] = plan_name
        existing_notes = metadata.get("notes")
        if isinstance(existing_notes, Sequence) and not isinstance(
            existing_notes, (str, bytes)
        ):
            notes = [str(entry) for entry in cast("Sequence[object]", existing_notes)]
            notes.append("Auto-generated demo astral snapshot")
        else:
            notes = ["Auto-generated demo astral snapshot"]
        metadata["notes"] = notes
    if runtime_ctx is not ctx and runtime_ctx is not None and ctx is not None:
        metadata["parent_ctx_attached"] = True

    result_payload: dict[str, object] = {
        "status": "success",
        "schema_version": SCHEMA_VERSION,
        "message": message,
    }
    if metadata:
        result_payload["metadata"] = metadata

    try:
        validate_payload(result_payload, OUTPUT_SCHEMA)
    except ValidationErrorType as exc:
        return _failure_payload(
            "generated output failed schema validation",
            details={
                "error": exc.message,
                "path": [str(part) for part in exc.path],
                "schema_path": [str(part) for part in exc.schema_path],
            },
        )

    return result_payload


def _load_json_payload(file_path: str | None) -> Mapping[str, object]:
    def _load(handle: IO[str]) -> Mapping[str, object]:
        payload_obj: object = json.load(handle)
        if not isinstance(payload_obj, dict):
            message = "JSON payload must be an object"
            raise TypeError(message)
        return cast("dict[str, object]", payload_obj)

    if file_path:
        with Path(file_path).open("r", encoding="utf-8") as handle:
            return _load(handle)
    return _load(sys.stdin)


def _run_json_cli(args: Sequence[str]) -> None:
    parser = argparse.ArgumentParser(description="x_make_yahw_x JSON runner")
    parser.add_argument(
        "--json", action="store_true", help="Read JSON payload from stdin"
    )
    parser.add_argument("--json-file", type=str, help="Path to JSON payload file")
    parsed = parser.parse_args(args)
    json_flag_obj = cast("object", getattr(parsed, "json", False))
    json_flag = bool(json_flag_obj)
    json_file_obj = cast("object", getattr(parsed, "json_file", None))
    json_file = json_file_obj if isinstance(json_file_obj, str) else None

    if not (json_flag or json_file):
        parser.error("JSON input required. Use --json for stdin or --json-file <path>.")

    payload = _load_json_payload(json_file if json_file else None)
    result = main_json(payload)
    json.dump(result, sys.stdout, indent=2)
    sys.stdout.write("\n")


x_cls_make_yahw_x = XClsMakeYahwX

__all__ = ["XClsMakeYahwX", "main", "main_json", "x_cls_make_yahw_x"]


if __name__ == "__main__":
    _run_json_cli(sys.argv[1:])
