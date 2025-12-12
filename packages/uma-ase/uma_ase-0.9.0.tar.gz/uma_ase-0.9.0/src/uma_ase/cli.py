"""Command-line interface for running uma-ase workflows."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Iterable, Optional

from .utils import parse_cli_args
from .workflows import (
    WorkflowPaths,
    build_output_paths,
    configure_logging,
    remove_if_exists,
    run_geometry_optimization,
    run_single_point,
    prepare_atoms_for_vibrations,
    run_vibrational_analysis,
    run_transition_state_search,
)


def _ensure_input(path: Path) -> bool:
    if not path.is_file():
        print(f"Input geometry not found: {path}", file=sys.stderr)
        return False
    return True


def _clean_outputs(paths: WorkflowPaths) -> None:
    remove_if_exists(
        tuple(
            path
            for path in (
                paths.trajectory,
                paths.log,
                paths.final_geometry,
                paths.freq_archive,
            )
            if path is not None
        )
    )


def _rollover_existing_log(log_path: Path) -> None:
    """Rename existing log file to a numbered backup before overwriting."""
    if not log_path.exists():
        return
    counter = 1
    while True:
        candidate = log_path.with_name(f"{log_path.stem}.{counter:02d}{log_path.suffix}")
        if not candidate.exists():
            log_path.rename(candidate)
            break
        counter += 1


def main(argv: Optional[Iterable[str]] = None) -> int:
    args = parse_cli_args(argv)

    input_path = Path(args.input).expanduser()
    if not _ensure_input(input_path):
        return 1
    args.input = str(input_path)

    run_sequence_raw = args.run_type
    if isinstance(run_sequence_raw, str):
        run_sequence_raw = [run_sequence_raw]
    run_sequence = [step.lower() for step in run_sequence_raw] or ["sp"]

    log_sequence = run_sequence.copy()

    paths = build_output_paths(input_path, log_sequence)
    _rollover_existing_log(paths.log)
    _clean_outputs(paths)

    with configure_logging(paths.log) as logger:
        context = None
        status = 0

        for step in run_sequence:
            if step == "sp":
                status, context = run_single_point(args, paths, logger)
            elif step == "geoopt":
                status, context = run_geometry_optimization(args, paths, logger)
            elif step == "freqs":
                if context is None:
                    status, context = prepare_atoms_for_vibrations(args, logger)
                    if status != 0:
                        break
                status, _ = run_vibrational_analysis(
                    context,
                    logger,
                    input_path,
                    args.temp,
                    args.press,
                    paths.freq_archive,
                )
            elif step == "ts":
                status, context = run_transition_state_search(
                    args,
                    paths,
                    logger,
                    input_path,
                    context,
                )
            else:
                logger.error("Unknown run-type '%s'", step)
                status = 1

            if status != 0:
                break

        return status


if __name__ == "__main__":
    sys.exit(main())
