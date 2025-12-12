"""CLI helper to export ASE normal-mode displacement matrices."""

from __future__ import annotations

import argparse
import json
import sys
import zipfile
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Iterable, List, Optional, Sequence, Tuple

import numpy as np
from ase.atoms import Atoms
from ase.io import read

PhaseInfo = Tuple[int, float]


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="uma-ase-modes",
        description=(
            "Extract N_atoms x 3 displacement matrices for every normal mode "
            "stored in a uma-ase frequency output directory or ZIP archive."
        ),
    )
    parser.add_argument(
        "source",
        metavar="SRC",
        help="freqs directory (or <name>-FREQS-modes.zip) produced by uma-ase.",
    )
    parser.add_argument(
        "-o",
        "--output",
        dest="output",
        type=Path,
        help=(
            "Destination folder for .npy files (defaults to <SRC-stem>-modes "
            "under the current working directory)."
        ),
    )
    parser.add_argument(
        "--normalize",
        action="store_true",
        help="Rescale every mode so the maximum absolute displacement equals 1.",
    )
    return parser


def _parse_mode_index(path: Path) -> Optional[int]:
    """Best-effort extraction of the trailing integer in a mode filename."""
    for segment in reversed(path.stem.split(".")):
        if segment.isdigit():
            return int(segment)
    return None


def _collect_mode_files(root: Path) -> List[Path]:
    matched = list(root.rglob("*.xyz")) + list(root.rglob("*.traj"))
    return sorted(set(matched))


def _relative_to_root(path: Path, root: Path) -> Path:
    try:
        return path.relative_to(root)
    except ValueError:
        return path


def _sanitize_prefix(path: Path, root: Path) -> str:
    relative = _relative_to_root(path, root)
    parent = relative.parent.name if relative.parent != Path(".") else relative.stem
    candidate = parent or path.parent.name or "modes"
    return candidate.replace(" ", "_")


def _first_useful_phase(frames: Sequence[Atoms]) -> Tuple[np.ndarray, PhaseInfo]:
    if len(frames) < 2:
        raise ValueError("Need at least two frames per mode to reconstruct displacements.")
    equilibrium = frames[0].get_positions()
    nframes = len(frames)
    phases = np.linspace(0.0, 2.0 * np.pi, nframes, endpoint=False)
    for frame_index, phase in enumerate(phases[1:], start=1):
        scale = float(np.sin(phase))
        if abs(scale) < 1e-8:
            continue
        displaced = frames[frame_index].get_positions()
        return (displaced - equilibrium) / scale, (frame_index, scale)
    raise ValueError("Unable to recover displacement vectors; try regenerating modes with more frames.")


def _normalize_matrix(matrix: np.ndarray) -> np.ndarray:
    max_component = float(np.abs(matrix).max())
    if max_component == 0.0:
        return matrix
    return matrix / max_component


def _emit_metadata(
    output_dir: Path,
    summary: dict,
) -> None:
    metadata_path = output_dir / "modes.json"
    metadata_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")


def _prepare_output_dir(source: Path, explicit_output: Optional[Path]) -> Path:
    if explicit_output is not None:
        destination = explicit_output.expanduser()
    else:
        destination = Path.cwd() / f"{source.stem}-modes"
    destination.mkdir(parents=True, exist_ok=True)
    return destination


def _resolve_source_dir(source: Path) -> Tuple[Path, Optional[TemporaryDirectory]]:
    if source.is_dir():
        return source, None
    if source.is_file() and zipfile.is_zipfile(source):
        temp_area = TemporaryDirectory(prefix="uma_ase_modes_")
        with zipfile.ZipFile(source) as archive:
            archive.extractall(temp_area.name)
        return Path(temp_area.name), temp_area
    raise FileNotFoundError(f"{source} is neither a directory nor a ZIP archive")


def _unique_destination(output_dir: Path, basename: str) -> Path:
    destination = output_dir / f"{basename}.npy"
    counter = 1
    while destination.exists():
        destination = output_dir / f"{basename}-{counter}.npy"
        counter += 1
    return destination


def _save_mode_matrix(
    matrix: np.ndarray,
    destination: Path,
) -> None:
    np.save(destination, matrix)


def main(argv: Optional[Iterable[str]] = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    source = Path(args.source).expanduser().resolve()
    try:
        root, temp_area = _resolve_source_dir(source)
    except (FileNotFoundError, zipfile.BadZipFile) as exc:
        parser.error(str(exc))
        return 1

    output_dir = _prepare_output_dir(source, args.output)
    candidates = _collect_mode_files(root)
    if not candidates:
        message = f"No .xyz or .traj mode files found under {source}"
        if temp_area is not None:
            temp_area.cleanup()
        parser.error(message)
        return 1
    candidates.sort(key=lambda path: (str(path.parent), _parse_mode_index(path) or -1, path.name))

    metadata = {
        "source": str(source),
        "output_dir": str(output_dir),
        "normalize": bool(args.normalize),
        "modes": [],
    }
    failures = 0

    for path in candidates:
        mode_index = _parse_mode_index(path)
        if mode_index is None:
            continue
        try:
            frames = read(path, ":")
        except Exception as exc:  # pragma: no cover - depends on ASE readers
            print(f"[uma-ase-modes] Unable to read {path}: {exc}", file=sys.stderr)
            failures += 1
            continue
        try:
            matrix, (phase_frame, scale) = _first_useful_phase(frames)
        except ValueError as exc:
            print(f"[uma-ase-modes] {path}: {exc}", file=sys.stderr)
            failures += 1
            continue
        if args.normalize:
            matrix = _normalize_matrix(matrix)
        prefix = _sanitize_prefix(path, root)
        destination = _unique_destination(output_dir, f"{prefix}-mode-{mode_index:03d}")
        _save_mode_matrix(matrix, destination)
        metadata["modes"].append(
            {
                "mode_index": mode_index,
                "output": destination.name,
                "source": str(_relative_to_root(path, root)),
                "atoms": matrix.shape[0],
                "phase_frame": phase_frame,
                "phase_scale": scale,
                "frames": len(frames),
            }
        )

    _emit_metadata(output_dir, metadata)

    if temp_area is not None:
        temp_area.cleanup()

    if failures and len(metadata["modes"]) == 0:
        parser.error("Failed to convert any vibrational modes.")
        return 1
    if failures:
        print(f"[uma-ase-modes] Completed with {failures} failures.", file=sys.stderr)
        return 2

    print(f"[uma-ase-modes] Exported {len(metadata['modes'])} mode matrices to {output_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
