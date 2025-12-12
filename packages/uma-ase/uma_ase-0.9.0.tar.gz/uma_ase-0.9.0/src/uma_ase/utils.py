"""Shared utilities for uma-ase workflows."""

from __future__ import annotations

import argparse
import logging
import os
import re
import shutil
import tempfile
import sys
from dataclasses import dataclass
from difflib import get_close_matches
from pathlib import Path
from typing import Iterable, Mapping, Optional

import numpy as np
from ase import Atoms

# for UMA Fairchem
try:
    from fairchem.core import FAIRChemCalculator, pretrained_mlip
except ModuleNotFoundError:  # pragma: no cover - environment dependent
    pretrained_mlip = None
    FAIRChemCalculator = None

try:  # FairChem >=1.0
    from fairchem.core.units.mlip_unit import load_predict_unit
except ModuleNotFoundError:  # pragma: no cover - fallback for old versions
    load_predict_unit = None


def Sum_of_atomic_energies(
    counts: Mapping[str, int],
    uma_checkpoint: str,
    uma_model: str,
    device: str,
    logger: Optional[logging.Logger] = None,
) -> float:
    """
    Compute the total energy by summing the energy of each atom type multiplied
    by its number of occurrences.

    Parameters
    ----------
    counts : dict[str, int]
        Dictionary mapping atom symbol -> number of occurrences.
    uma_checkpoint : str
        UMA checkpoint identifier.
    uma_model : str
        UMA task/model identifier.
    device : str
        Execution device (e.g. 'cpu', 'cuda').
    logger : logging.Logger, optional
        Logger used to report per-element energies.

    Returns
    -------
    float
        Total summed energy.
    """
    if pretrained_mlip is None or FAIRChemCalculator is None:
        raise RuntimeError("UMA FairChem libraries are unavailable; cannot compute atomic energies.")

    sum_atomic_energies = 0.0
    for atom_type, count in counts.items():
        # Generate a single-atom periodic cell inside the cutoff so the
        # calculator has neighbours to build the graph representation.
        # UMA default cutoff = 6.0, so a=5.0
        a = 5.0  # choose a < cutoff
        atom = Atoms(atom_type, positions=[[0, 0, 0]], cell=[a, a, a], pbc=True)
        atom.info["charge"] = 0
        atom.info["spin"] = 1

        try:
            predictor = get_predict_unit_with_local_fallback(
                uma_checkpoint,
                device=device,
                logger=logger,
            )
        except FileNotFoundError as exc:
            raise FileNotFoundError(str(exc)) from exc
        except KeyError as exc:
            raise KeyError(f"UMA checkpoint '{uma_checkpoint}' not found.") from exc
        atom.calc = FAIRChemCalculator(predictor, task_name=uma_model)
        energy = atom.get_total_energy()
        message = f"Atomic energy for atom type {atom_type}: {energy} eV"
        if logger:
            logger.info(message)
        else:
            print(message)
        sum_atomic_energies += energy * count
    return sum_atomic_energies


def sum_of_atomic_energies(
    counts: Mapping[str, int],
    uma_checkpoint: str,
    uma_model: str,
    device: str,
    logger: Optional[logging.Logger] = None,
) -> float:
    """PEP 8 alias for :func:`Sum_of_atomic_energies`."""
    return Sum_of_atomic_energies(counts, uma_checkpoint, uma_model, device, logger=logger)


class Tee:
    """
    A file-like object that writes simultaneously to a file and stdout.

    Usage:
        from log_utils import Tee
        tee = Tee("output.log")
        print("Hello", file=tee)
        tee.close()
    """
    def __init__(self, filename: str, mode: str = "w", stream=sys.stdout):
        """
        Args:
            filename (str): Path to the log file.
            mode (str): File open mode ('w' to overwrite, 'a' to append).
            stream: Output stream to duplicate (default: sys.stdout).
        """
        self.file = open(filename, mode)
        self.stream = stream

    def write(self, message: str) -> None:
        self.stream.write(message)
        self.file.write(message)

    def flush(self) -> None:
        self.stream.flush()
        self.file.flush()

    def close(self) -> None:
        """Close the underlying file."""
        self.file.close()


def rmsd_simple(atoms1: Atoms, atoms2: Atoms) -> float:
    """Compute RMSD between two ASE Atoms objects without alignment."""
    pos1 = atoms1.get_positions()
    pos2 = atoms2.get_positions()
    diff = pos1 - pos2
    return np.sqrt((diff ** 2).sum() / len(pos1))


def get_filename_only(filepath: str) -> str:
    """
    Given a file path like 'folder/filename.ext', return only 'filename'.

    Args:
        filepath (str): The full file name or path.

    Returns:
        str: The filename without its extension.
    """
    # Extract the base name (remove path)
    base = os.path.basename(filepath)
    # Split into (filename, extension)
    name, _ = os.path.splitext(base)
    return name


def delete_file_if_exists(filepath: str) -> bool:
    """
    Check if a file exists, and delete it if it does.

    Args:
        filepath (str): Path to the file to delete.

    Returns:
        bool: True if file existed and was deleted, False otherwise.
    """
    try:
        if os.path.isfile(filepath):
            os.remove(filepath)
            print(f"Deleted file: {filepath}")
            return True
        else:
            print(f"File not found: {filepath}")
            return False
    except PermissionError:
        print(f"Permission denied: {filepath}")
        return False
    except Exception as exc:
        print(f"Error deleting {filepath}: {exc}")
        return False


class ChargeAction(argparse.Action):
    """Track when the user explicitly provides -chg."""

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)
        setattr(namespace, "_chg_explicit", True)


class SpinAction(argparse.Action):
    """Track when the user explicitly provides -spin."""

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)
        setattr(namespace, "_spin_explicit", True)


@dataclass(frozen=True)
class XYZMetadata:
    comment: Optional[str]
    url: Optional[str]
    charge: Optional[int]
    spin: Optional[int]


_URL_PATTERN = re.compile(r"https?://\S+")
_SIGNED_INT_PATTERN = re.compile(r"(?<![\w.-])[+-]?\d+(?![\w.-])")


def parse_cli_args(argv: Optional[Iterable[str]] = None) -> argparse.Namespace:
    """
    Parse command-line arguments shared across UMA utilities.

    Required arguments
    ------------------
    - input : Path to the input geometry readable by ASE.

    Optional arguments
    ------------------
    - chg             : Total molecular charge (default 0; inferred from XYZ comment when present).
    - spin            : Spin multiplicity (default 1).
    - iter             : Maximum number of optimisation cycles (default 250).
    - grad             : Convergence threshold for maximum force (default 0.01).
    - mlff-chk         : UMA checkpoint identifier (default 'uma-s-1p1').
    - mlff-task        : UMA task/model identifier (default 'omol').
    - visualize        : Open the final trajectory in an interactive viewer.
    - optimizer        : ASE optimizer to use (default 'BFGS').
    - run-type         : Workflow to execute ('sp', 'geoopt', 'freqs', 'ts'; default 'sp').
    - cpu              : Force CPU execution even if CUDA is available.
    - temp             : Thermochemistry temperature in Kelvin (default 298.15).
    - press            : Thermochemistry pressure in Pascals (default 101325.0).
    """
    parser = argparse.ArgumentParser(
        prog="uma-ase",
        description=(
            "Provide the required -input value. Charge defaults to 0 or to the "
            "signed integer embedded in the XYZ comment line."
        ),
    )
    parser.set_defaults(_chg_explicit=False, _spin_explicit=False)

    # --- Required arguments ---
    parser.add_argument(
        "-input",
        type=str,
        required=True,
        help="Input geometry readable by ASE (XYZ comment may append the signed charge & spin).",
    )

    parser.add_argument(
        "-chg",
        type=int,
        action=ChargeAction,
        default=0,
        help="Charge (default 0; inferred from XYZ comment when present).",
    )

    # --- Optional arguments ---
    parser.add_argument(
        "-spin",
        type=int,
        action=SpinAction,
        default=1,
        help="Spin multiplicity (default 1; inferred from XYZ comment when present)"
    )

    parser.add_argument(
        "-run-type",
        nargs="+",
        choices=("sp", "geoopt", "freqs", "ts"),
        default=["sp"],
        help="Run type(s) to execute: 'sp', 'geoopt', 'freqs', 'ts', or any sequence thereof (default: sp).",
    )
    parser.add_argument(
        "-cpu",
        action="store_true",
        help="Force UMA calculations to run on CPU even when CUDA is available.",
    )
    parser.add_argument(
        "-iter",
        type=int,
        default=250,
        help="Max number of geometry optimization cycles. Default=250"
    )

    parser.add_argument(
        "-grad",
        type=float,
        default=0.01,
        help="Max grad for convergence. Default=0.01 eV/A"
    )

    parser.add_argument(
        "-optimizer",
        default="LBFGS",
        metavar="NAME",
        help="ASE optimizer (e.g. BFGS, LBFGS, FIRE, BFGSLineSearch,MDMin). Default='LBFGS'."
    )
    parser.add_argument(
        "--ts-displacement",
        type=float,
        default=0.1,
        help="Initial displacement (Å) applied along the selected mode before the dimer TS search.",
    )
    parser.add_argument(
        "--ts-dimer-separation",
        type=float,
        default=0.01,
        help="Separation (Å) between the two images in the dimer search.",
    )
    parser.add_argument(
        "--ts-trial-step",
        type=float,
        default=0.05,
        help="Trial translation step (Å) used by the dimer optimizer when curvature is negative.",
    )
    parser.add_argument(
        "--ts-max-step",
        type=float,
        default=0.2,
        help="Maximum translation step (Å) allowed per dimer iteration.",
    )
    parser.add_argument(
        "--ts-max-rot",
        type=int,
        default=5,
        help="Maximum number of rotational updates per dimer iteration.",
    )

    parser.add_argument(
        "-mlff-chk",
        default="uma-s-1p1",
        metavar="CHECKPOINT",
        help="UMA checkpoint. Default='uma-s-1p1'."
    )

    parser.add_argument(
        "-mlff-task",
        default="omol",
        metavar="TASK",
        help="UMA task/model. Default='omol'."
    )

    parser.add_argument(
        "-temp",
        "--temperature",
        dest="temp",
        type=float,
        metavar="T",
        default=298.15,
        help="Temperature in Kelvin for vibrational analysis (default 298.15 K).",
    )

    parser.add_argument(
        "-press",
        "--pressure",
        dest="press",
        type=float,
        metavar="P",
        default=101325.0,
        help="Pressure in Pascals for vibrational analysis (default 1 atm=101325.0 Pa).",
    )

    parser.add_argument(
        "-visualize",
        action="store_true",
        help="Open the trajectory of a geoopt run in the ASE interactive viewer."
    )
    args = parser.parse_args(argv)
    # Provide backward-compatible aliases for temperature/pressure fields.
    if not hasattr(args, "temp"):
        setattr(args, "temp", 298.15)
    if not hasattr(args, "press"):
        setattr(args, "press", 101325.0)
    setattr(args, "temperature", args.temp)
    setattr(args, "pressure", args.press)
    return args


def _resolve_custom_checkpoint_dir() -> Path:
    """
    Resolve the directory housing custom UMA checkpoints.
    """
    custom_dir = os.environ.get("UMA_CUSTOM_CHECKPOINT_DIR")
    if custom_dir:
        return Path(custom_dir).expanduser().resolve()
    return Path.home() / ".uma_ase" / "checkpoints"


def _locate_local_checkpoint(custom_root: Path, checkpoint: str) -> Optional[Path]:
    """
    Locate a checkpoint file under *custom_root* matching *checkpoint*.
    """
    expanded_root = custom_root.expanduser()
    if not expanded_root.exists():
        return None

    candidates = [
        expanded_root / checkpoint,
        expanded_root / f"{checkpoint}.pt",
    ]

    checkpoint_dir = expanded_root / checkpoint
    if checkpoint_dir.is_dir():
        candidates.extend(sorted(checkpoint_dir.glob("*.pt")))

    candidates.extend(sorted(expanded_root.glob(f"{checkpoint}*.pt")))

    seen: set[Path] = set()
    for candidate in candidates:
        candidate = candidate.expanduser()
        if candidate in seen:
            continue
        seen.add(candidate)
        if candidate.is_file():
            return candidate
    return None


def extract_xyz_comment(path: Path) -> Optional[str]:
    """
    Return the second-line comment from an XYZ file, if present.

    Parameters
    ----------
    path : Path
        Path to the candidate XYZ file.

    Returns
    -------
    str | None
        The stripped second line when available, otherwise ``None``.
    """
    metadata = extract_xyz_metadata(path)
    return metadata.comment


def extract_xyz_metadata(path: Path) -> XYZMetadata:
    """
    Extract comment, URL, charge, and spin metadata from an XYZ geometry.
    """
    default = XYZMetadata(comment=None, url=None, charge=None, spin=None)
    if path.suffix.lower() != ".xyz":
        return default

    try:
        with path.open("r", encoding="utf-8", errors="ignore") as handle:
            handle.readline()
            comment = handle.readline()
    except OSError:
        return default

    if comment is None:
        return default

    comment = comment.strip()
    if not comment:
        return default

    url_matches = list(_URL_PATTERN.finditer(comment))
    url = url_matches[0].group(0) if url_matches else None

    cleaned_comment = comment
    if url_matches:
        cleaned_comment = _URL_PATTERN.sub(" ", comment)

    numbers: list[int] = []
    for match in _SIGNED_INT_PATTERN.finditer(cleaned_comment):
        try:
            numbers.append(int(match.group(0)))
        except ValueError:
            continue

    charge = numbers[0] if numbers else None
    spin = numbers[1] if len(numbers) > 1 else None
    if spin is not None and spin <= 0:
        spin = None

    return XYZMetadata(
        comment=comment,
        url=url,
        charge=charge,
        spin=spin,
    )


def get_predict_unit_with_local_fallback(
    checkpoint: str,
    *,
    device: str,
    logger: Optional[logging.Logger] = None,
):
    """Load a UMA predictor, consulting local checkpoints when necessary."""
    if pretrained_mlip is None or FAIRChemCalculator is None:
        raise RuntimeError("UMA FairChem libraries are unavailable; cannot load checkpoints.")

    custom_root = _resolve_custom_checkpoint_dir()
    local_file = _locate_local_checkpoint(custom_root, checkpoint)
    local_error: Optional[Exception] = None

    if local_file is not None:
        try:
            return _load_predict_unit_from_resolved_local(
                checkpoint, local_file, device, logger
            )
        except Exception as exc:  # pragma: no cover - depends on FairChem
            local_error = exc
            if logger:
                logger.debug(
                    "Unable to load local UMA checkpoint '%s' from %s: %s",
                    checkpoint,
                    local_file,
                    exc,
                )

    try:
        return pretrained_mlip.get_predict_unit(checkpoint, device=device)
    except KeyError as exc:
        if local_file is None:
            raise FileNotFoundError(
                _format_missing_checkpoint_error(checkpoint, custom_root)
            ) from exc

        if local_error is not None:
            raise RuntimeError(
                f"UMA checkpoint '{checkpoint}' found at {local_file} but failed to load: {local_error}"
            ) from local_error

        # If we have a local file but no error recorded, ensure a final attempt.
        return _load_predict_unit_from_resolved_local(
            checkpoint, local_file, device, logger
        )
    except Exception as exc:
        if local_file is not None and local_error is None:
            try:
                return _load_predict_unit_from_resolved_local(
                    checkpoint, local_file, device, logger
                )
            except Exception as local_exc:  # pragma: no cover - fallback path
                if logger:
                    logger.debug(
                        "Secondary local load attempt for checkpoint '%s' failed: %s",
                        checkpoint,
                        local_exc,
                    )
                raise RuntimeError(
                    f"Remote UMA checkpoint load failed ({exc}) and local fallback failed ({local_exc})."
                ) from local_exc
        raise


def _load_predict_unit_from_resolved_local(
    checkpoint: str,
    local_file: Path,
    device: str,
    logger: Optional[logging.Logger],
):
    if logger:
        logger.debug("Loading local UMA checkpoint '%s' from %s", checkpoint, local_file)

    registry = getattr(pretrained_mlip, "MODEL_REGISTRY", None)
    model_dir_raw = getattr(pretrained_mlip, "MODEL_DIR", None)
    if registry is not None and model_dir_raw is not None:
        # Legacy FairChem version: mirror registry + model dir behaviour.
        entry = registry.get(checkpoint)
        if entry is None or entry.get("filename") != local_file.name:
            registry[checkpoint] = {
                "filename": local_file.name,
                "url": None,
                "md5": None,
                "license": "local",
            }

        model_dir = Path(model_dir_raw)
        model_dir.mkdir(parents=True, exist_ok=True)
        target = model_dir / local_file.name
        if target.exists():
            try:
                if os.path.samefile(target, local_file):
                    return pretrained_mlip.get_predict_unit(checkpoint, device=device)
            except OSError:
                pass
            try:
                target.unlink()
            except OSError:
                target.unlink(missing_ok=True)  # type: ignore[arg-type]
        try:
            target.symlink_to(local_file)
        except OSError:
            shutil.copy2(local_file, target)
        return pretrained_mlip.get_predict_unit(checkpoint, device=device)

    return _load_predict_unit_from_local_checkpoint(local_file, device, logger)


def _format_missing_checkpoint_error(checkpoint: str, custom_root: Path) -> str:
    """
    Build a descriptive error message including nearby identifiers and local files.
    """
    available_local = sorted(path.stem for path in custom_root.glob("*.pt"))

    available_registry_set: set[str] = set()
    registry = getattr(pretrained_mlip, "MODEL_REGISTRY", None)
    if isinstance(registry, dict):
        available_registry_set.update(registry.keys())

    model_ckpts = getattr(pretrained_mlip, "_MODEL_CKPTS", None)
    checkpoints = getattr(model_ckpts, "checkpoints", None)
    if isinstance(checkpoints, dict):
        available_registry_set.update(checkpoints.keys())

    builtin_models = getattr(pretrained_mlip, "available_models", ())
    if isinstance(builtin_models, (list, tuple, set)):
        available_registry_set.update(str(item) for item in builtin_models)

    available_registry = sorted(available_registry_set)

    message = (
        f"UMA checkpoint '{checkpoint}' not found in FairChem registry "
        f"or in '{custom_root}'."
    )

    suggestions = []
    for pool in (available_local, available_registry):
        suggestions.extend(get_close_matches(checkpoint, pool, n=1, cutoff=0.6))

    if suggestions:
        unique = []
        for item in suggestions:
            if item not in unique:
                unique.append(item)
        message += f" Did you mean: {', '.join(unique)}?"
    else:
        if available_local or available_registry:
            message += " Available options: "
            if available_local:
                message += f"local[{', '.join(available_local)}]"
            if available_registry:
                if available_local:
                    message += "; "
                message += f"registry[{', '.join(available_registry)}]"

    return message


def _load_predict_unit_from_local_checkpoint(
    local_file: Path,
    device: str,
    logger: Optional[logging.Logger],
):
    if load_predict_unit is None:
        raise RuntimeError(
            "Local checkpoint fallback unavailable; FairChem version lacks load_predict_unit."
        )

    try:
        return load_predict_unit(local_file, device=device)
    except Exception as exc:
        if "model_version" not in str(exc):
            raise

        predictor = _load_legacy_umamodel(local_file, device)
        if predictor is not None:
            if logger:
                logger.debug(
                    "Patched legacy UMA checkpoint '%s' by dropping unsupported keys.",
                    local_file.name,
                )
            return predictor
        raise


def _load_legacy_umamodel(local_file: Path, device: str):
    try:
        from torch.serialization import add_safe_globals
    except Exception:  # pragma: no cover - torch absent
        return None

    try:
        from fairchem.core.units.mlip_unit.api.inference import MLIPInferenceCheckpoint
    except ModuleNotFoundError:  # pragma: no cover
        return None

    add_safe_globals([MLIPInferenceCheckpoint])

    import torch  # local import to avoid hard dependency when unused

    checkpoint = torch.load(local_file, map_location="cpu", weights_only=False)
    backbone_cfg = None
    if isinstance(getattr(checkpoint, "model_config", None), dict):
        backbone_cfg = checkpoint.model_config.get("backbone")

    if not isinstance(backbone_cfg, dict) or "model_version" not in backbone_cfg:
        return None

    backbone_cfg.pop("model_version", None)

    with tempfile.NamedTemporaryFile(suffix=".pt", delete=False) as tmp_file:
        tmp_path = Path(tmp_file.name)

    torch.save(checkpoint, tmp_path)

    try:
        return load_predict_unit(tmp_path, device=device)
    finally:
        try:
            tmp_path.unlink()
        except OSError:
            pass
