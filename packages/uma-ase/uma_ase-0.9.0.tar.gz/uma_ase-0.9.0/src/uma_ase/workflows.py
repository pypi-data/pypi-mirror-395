from __future__ import annotations

from argparse import Namespace
from collections import Counter
from contextlib import contextmanager, suppress
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable, Optional, Tuple
import logging
import sys
import shutil
import inspect
import io
import zipfile
import uuid

import numpy as np
from ase.io import read, write
from ase.optimize import BFGS, BFGSLineSearch, FIRE, LBFGS, MDMin
from ase.mep import DimerControl, MinModeAtoms, MinModeTranslate
from ase.vibrations import Vibrations
from ase.vibrations.data import VibrationsData
from ase.thermochemistry import IdealGasThermo
from ase.visualize import view
from ase import Atoms, units

try:
    from fairchem.core import pretrained_mlip, FAIRChemCalculator
except ModuleNotFoundError as exc:  # pragma: no cover - environment dependent
    pretrained_mlip = None
    FAIRChemCalculator = None
    FAIR_CHEM_IMPORT_ERROR = exc
else:  # pragma: no cover - environment dependent
    FAIR_CHEM_IMPORT_ERROR = None

from .utils import (
    Sum_of_atomic_energies,
    extract_xyz_metadata,
    get_predict_unit_with_local_fallback,
    rmsd_simple,
)


@dataclass(frozen=True)
class WorkflowPaths:
    """Collection of standard output artifacts emitted by a run."""

    trajectory: Path
    log: Path
    final_geometry: Path
    freq_archive: Optional[Path] = None


@dataclass
class AtomContext:
    """Container bundling an ASE atoms object with metadata for downstream steps."""

    atoms: Atoms
    counts: Counter
    device: str


def capture_stdout(func, *args, **kwargs):
    """Capture stdout emitted by *func* and replay it to the original stream."""
    buffer = io.StringIO()
    original_stdout = sys.stdout
    try:
        sig = inspect.signature(func)
        if "log" in sig.parameters and "log" not in kwargs:
            kwargs["log"] = buffer
            result = func(*args, **kwargs)
        else:
            sys.stdout = buffer
            result = func(*args, **kwargs)
    finally:
        sys.stdout = original_stdout
    output = buffer.getvalue()
    if output:
        original_stdout.write(output)
        original_stdout.flush()
    return result, output


class LoggerWriter:
    """Adapter that lets ASE optimizers log through a standard logger."""

    def __init__(self, logger: logging.Logger):
        self._logger = logger

    def write(self, message: str) -> None:
        message = message.strip()
        if message:
            self._logger.info(message)

    def flush(self) -> None:  # pragma: no cover - interface requirement
        pass

    def close(self) -> None:  # pragma: no cover - interface requirement
        pass


class TorchUnavailable(RuntimeError):
    """Lightweight exception indicating torch is not present."""


OPTIMIZER_CLASSES = {
    "BFGS": BFGS,
    "LBFGS": LBFGS,
    "BFGS_LINESEARCH": BFGSLineSearch,
    "FIRE": FIRE,
    "MDMIN": MDMin,
}

RUN_LABELS = {
    "sp": "SP",
    "geoopt": "OPT",
    "freqs": "FREQS",
    "ts": "TS",
}


def build_output_paths(
    input_path: Path,
    run_sequence: Optional[Iterable[str]] = None,
    explicit_geoopt: bool = True,
) -> WorkflowPaths:
    """Generate canonical output filenames derived from the input geometry."""
    parent = input_path.parent
    stem = input_path.stem
    sequence = list(run_sequence) if run_sequence else ["geoopt"]
    normalized = [
        item.lower() if isinstance(item, str) else str(item).lower()
        for item in sequence
    ]
    if set(normalized) == {"freqs"}:
        labels = ["FREQS"]
    else:
        labels = []
        for item in normalized:
            label = RUN_LABELS.get(item, item.upper())
            if label not in labels:
                labels.append(label)
    log_suffix = "-".join(labels)
    log_name = f"{stem}-{log_suffix}.log"
    freq_archive = None
    if any(item in {"freqs", "ts"} for item in normalized):
        freq_archive = parent / f"{stem}-FREQS-modes.zip"
    return WorkflowPaths(
        trajectory=parent / f"{stem}-{log_suffix}.traj",
        log=parent / log_name,
        final_geometry=parent / f"{stem}-geoopt-{log_suffix}.xyz",
        freq_archive=freq_archive,
    )


def remove_if_exists(paths: Iterable[Path]) -> None:
    """Delete pre-existing files or directories produced by earlier runs."""
    for path in paths:
        if path.is_dir():
            shutil.rmtree(path, ignore_errors=True)
        elif path.exists():
            path.unlink()


def _convert_traj_to_xyz(traj_file: Path, destination: Path, logger: logging.Logger) -> bool:
    """Convert an ASE trajectory to multi-frame XYZ, deleting the original."""

    try:
        frames = read(traj_file, ":")
    except Exception as exc:
        logger.warning("Unable to read vibrational trajectory %s: %s", traj_file, exc)
        return False
    try:
        destination.parent.mkdir(parents=True, exist_ok=True)
        write(destination, frames, format="xyz")
    except OSError as exc:
        logger.warning("Unable to write %s: %s", destination, exc)
        return False
    try:
        traj_file.unlink()
    except OSError:
        pass
    return True


def _cleanup_vibration_cache(cache_dir: Path, target_dir: Path, logger: logging.Logger) -> None:
    """Move trajectory files to target dir and remove cache artifacts."""
    if not cache_dir.exists():
        return

    moved = 0
    for traj_file in cache_dir.glob("*.traj"):
        destination = target_dir / f"{traj_file.stem}.xyz"
        if _convert_traj_to_xyz(traj_file, destination, logger):
            moved += 1

    removed = 0
    for cache_file in cache_dir.glob("cache*.json"):
        try:
            cache_file.unlink()
            removed += 1
        except OSError as exc:
            logger.warning("Unable to delete %s: %s", cache_file, exc)

    try:
        shutil.rmtree(cache_dir)
    except OSError as exc:
        logger.warning("Unable to remove cache directory %s: %s", cache_dir, exc)

    if moved:
        logger.info("Moved %d normal mode components to %s", moved, target_dir)
    if removed:
        logger.info("Removed %d temporary cache files", removed)


def _package_vibrational_data(
    source_dir: Path,
    archive_path: Path,
    logger: logging.Logger,
) -> Optional[Path]:
    """Create a ZIP archive containing the vibrational trajectories."""

    converted = 0
    for traj_file in source_dir.rglob("*.traj"):
        xyz_path = traj_file.with_suffix(".xyz")
        if _convert_traj_to_xyz(traj_file, xyz_path, logger):
            converted += 1
    if converted:
        logger.info("Converted %d normal mode trajectories to XYZ", converted)

    files = [path for path in source_dir.rglob("*") if path.is_file()]
    if not files:
        logger.warning("No vibrational files found to package in %s", source_dir)
        return None
    try:
        archive_path.parent.mkdir(parents=True, exist_ok=True)
        if archive_path.exists():
            archive_path.unlink()
        with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as archive:
            for file_path in files:
                try:
                    relative = file_path.relative_to(source_dir.parent)
                except ValueError:
                    relative = file_path.name
                archive.write(file_path, str(relative))
    except OSError as exc:
        logger.warning("Unable to package vibrational data into %s: %s", archive_path, exc)
        return None
    logger.info("Packaged vibrational data into %s", archive_path)
    return archive_path


def _log_normal_mode_matrices(
    vib_data: VibrationsData,
    atoms: Atoms,
    logger: logging.Logger,
) -> None:
    """Emit formatted displacement matrices for every normal mode."""
    try:
        mode_matrices = np.asarray(vib_data.get_modes(all_atoms=True)).real
    except Exception as exc:  # pragma: no cover - ASE internals may vary
        logger.warning("Unable to extract normal-mode displacement matrices: %s", exc)
        return

    n_modes, n_atoms, _ = mode_matrices.shape
    symbols = atoms.get_chemical_symbols()
    component_labels = ("dx", "dy", "dz")
    col_width = 13
    chunk_size = 6

    logger.info(
        "Normal mode displacement matrix (columns = modes, rows = atom component dx/dy/dz)."
    )
    for start in range(0, n_modes, chunk_size):
        end = min(start + chunk_size, n_modes)
        header = "Atom Sym Comp" + "".join(
            f"{f'Mode {mode_index}':>{col_width}}"
            for mode_index in range(start, end)
        )
        logger.info(header)

        for atom_index in range(n_atoms):
            symbol = symbols[atom_index] if atom_index < len(symbols) else "?"
            for comp_index, label in enumerate(component_labels):
                row_label = f"{atom_index + 1:4d} {symbol:>3} {label:>4}"
                values = "".join(
                    f"{mode_matrices[mode_index, atom_index, comp_index]:{col_width}.6f}"
                    for mode_index in range(start, end)
                )
                logger.info("%s%s", row_label, values)
        logger.info("")


@contextmanager
def configure_logging(log_path: Path):
    """Context manager that emits log messages to stdout and a logfile."""
    logger = logging.Logger(f"uma_workflow.{uuid.uuid4().hex}")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    formatter = logging.Formatter("%(message)s")
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    file_handler = logging.FileHandler(log_path, mode="w")
    file_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)

    try:
        yield logger
    finally:
        for handler in logger.handlers[:]:
            handler.close()
            logger.removeHandler(handler)


def select_device(force_cpu: bool = False) -> str:
    """Return the preferred execution device based on torch availability."""
    if force_cpu:
        return "cpu"
    try:
        import torch
    except ModuleNotFoundError as exc:  # pragma: no cover - environment dependent
        raise TorchUnavailable("PyTorch is required to determine execution device.") from exc
    try:
        return "cuda" if torch.cuda.is_available() else "cpu"
    except Exception as exc:
        raise TorchUnavailable("Failed to query torch CUDA availability.") from exc


def log_header(logger: logging.Logger) -> None:
    """Print a static banner summarising the workflow."""
    try:
        from . import __version__
    except Exception:  # pragma: no cover
        __version__ = "unknown"

    banner = [
        "*****************************************************************************",
        f"*                        U M A - A S E   v{__version__:>8}                          *",
        "*        Universal Model for Atoms - Atomistic Simulation Environment       *",
        "*****************************************************************************",
    ]
    for line in banner:
        logger.info(line)


def log_arguments(args: Namespace, logger: logging.Logger, device: str) -> None:
    """Echo the parsed CLI arguments to aid reproducibility."""
    logger.info("Parsed & Catch Arguments:")
    logger.info("  input      : %s", args.input)
    logger.info("  chg        : %s", args.chg)
    logger.info("  spin       : %s", args.spin)
    logger.info("  iter       : %s", getattr(args, "iter", "-"))
    logger.info("  grad       : %s", getattr(args, "grad", "-"))
    logger.info("  optimizer  : %s", getattr(args, "optimizer", "-"))
    logger.info("  run_type   : %s", args.run_type)
    logger.info("  checkpoint : %s", args.mlff_chk)
    logger.info("  task       : %s", args.mlff_task)
    logger.info("  visualize  : %s", args.visualize)
    logger.info("  cpu_only   : %s", getattr(args, "cpu", False))
    logger.info("  temperature: %.4f K", getattr(args, "temp", 0.0))
    logger.info("  pressure   : %.2f Pa", getattr(args, "press", 0.0))
    logger.info("  device     : %s", device)


def summarise_structure(
    args: Namespace,
    atoms: Atoms,
    logger: logging.Logger,
    *,
    comment: Optional[str] = None,
) -> Counter:
    """Log structural information about the current Atoms object."""
    counts = Counter(atoms.get_chemical_symbols())
    log_header(logger)
    logger.info("*          Initial Geometry %s loaded", args.input)
    logger.info("*          Number of atoms: %s", len(atoms))
    logger.info("*          Formula: %s", atoms.get_chemical_formula())
    logger.info("*          Element counts: %s", dict(counts))
    logger.info("*          Charge: %s", args.chg)
    logger.info("*          Spin Multiplicity: %s", args.spin)
    if comment:
        logger.info("*          XYZ comment: %s", comment)
    logger.info("*")
    return counts


def log_geometry(logger: logging.Logger, atoms: Atoms, title: str) -> None:
    """Log atomic coordinates of *atoms* with a descriptive *title*."""
    logger.info(title)
    symbols = atoms.get_chemical_symbols()
    positions = atoms.get_positions()
    for symbol, (x_coord, y_coord, z_coord) in zip(symbols, positions):
        logger.info("  %3s %12.6f %12.6f %12.6f", symbol, x_coord, y_coord, z_coord)
    logger.info("")


def setup_calculated_atoms(
    args: Namespace,
    logger: logging.Logger,
) -> Tuple[int, Optional[AtomContext]]:
    """Create an ASE atoms object wired with the requested UMA calculator."""
    if FAIR_CHEM_IMPORT_ERROR is not None:
        logger.error("UMA FairChem libraries unavailable: %s", FAIR_CHEM_IMPORT_ERROR)
        return 1, None

    try:
        device = select_device(force_cpu=getattr(args, "cpu", False))
    except TorchUnavailable as exc:
        logger.error(str(exc))
        return 1, None

    if device == "cpu" and not getattr(args, "cpu", False):
        logger.info("CUDA device unavailable; running on CPU.")

    input_path = Path(args.input)
    metadata = extract_xyz_metadata(input_path)

    chg_explicit = bool(getattr(args, "_chg_explicit", False))
    if metadata.charge is not None and not chg_explicit:
        args.chg = metadata.charge
        logger.info("Charge inferred from XYZ metadata: %s", args.chg)
    elif metadata.charge is not None and chg_explicit and metadata.charge != args.chg:
        logger.debug(
            "XYZ metadata charge %s ignored because CLI provided charge %s.",
            metadata.charge,
            args.chg,
        )

    spin_explicit = bool(getattr(args, "_spin_explicit", False))
    if metadata.spin is not None and not spin_explicit:
        args.spin = metadata.spin
        logger.info("Spin multiplicity inferred from XYZ metadata: %s", args.spin)
    elif metadata.spin is not None and spin_explicit and metadata.spin != args.spin:
        logger.debug(
            "XYZ metadata spin %s ignored because CLI provided spin %s.",
            metadata.spin,
            args.spin,
        )

    log_arguments(args, logger, device)

    atoms = read(args.input)
    atoms.info["charge"] = args.chg
    atoms.info["spin"] = args.spin

    xyz_comment = metadata.comment
    if xyz_comment:
        atoms.info.setdefault("uma_comment", xyz_comment)
    if metadata.url:
        atoms.info.setdefault("uma_comment_url", metadata.url)

    counts = summarise_structure(args, atoms, logger, comment=xyz_comment)

    try:
        predictor = get_predict_unit_with_local_fallback(
            args.mlff_chk,
            device=device,
            logger=logger,
        )
    except FileNotFoundError as exc:
        logger.error(str(exc))
        return 1, None
    except KeyError:
        logger.error(
            "UMA checkpoint '%s' not found. Please provide a valid identifier.",
            args.mlff_chk,
        )
        return 1, None
    except Exception as exc:
        logger.error("Failed to load UMA checkpoint '%s': %s", args.mlff_chk, exc)
        return 1, None

    try:
        atoms.calc = FAIRChemCalculator(predictor, task_name=args.mlff_task)
    except Exception as exc:
        logger.error("Failed to initialise UMA calculator for task '%s': %s", args.mlff_task, exc)
        return 1, None

    logger.info("*          UMA Checkpoint: %s", args.mlff_chk)
    logger.info("*          UMA model: %s", args.mlff_task)
    logger.info("*")

    return 0, AtomContext(atoms=atoms, counts=counts, device=device)


def prepare_atoms_for_vibrations(
    args: Namespace,
    logger: logging.Logger,
) -> Tuple[int, Optional[AtomContext]]:
    """Set up atoms for vibrational analysis without running an optimisation."""
    status, context = setup_calculated_atoms(args, logger)
    if status != 0 or context is None:
        return status, None
    return 0, context


def _optimizer_converged(optimizer, run_result) -> bool:
    """Determine whether an ASE optimizer reported convergence."""
    converged: Optional[bool] = None
    if run_result is not None:
        with suppress(Exception):
            converged = bool(run_result)

    if converged is None:
        converged_attr = getattr(optimizer, "converged", None)
        if callable(converged_attr):
            gradient = None
            optimizable = getattr(optimizer, "optimizable", None)
            if optimizable is not None and hasattr(optimizable, "get_gradient"):
                with suppress(Exception):
                    gradient = optimizable.get_gradient()
            if gradient is None:
                atoms_obj = getattr(optimizer, "atoms", None)
                if atoms_obj is not None and hasattr(atoms_obj, "get_forces"):
                    with suppress(Exception):
                        gradient = atoms_obj.get_forces().ravel()
            if gradient is not None:
                with suppress(TypeError, AttributeError, AssertionError):
                    converged = converged_attr(gradient)
            else:
                with suppress(TypeError, AttributeError):
                    converged = converged_attr()
        elif isinstance(converged_attr, bool):
            converged = converged_attr

    if converged is None:
        converged = False
    return converged

def _resolve_optimizer(name: str):
    """Map a user-supplied optimiser name to an ASE optimiser class."""
    key = name.replace("-", "_").upper()
    return OPTIMIZER_CLASSES.get(key)


def run_geometry_optimization(
    args: Namespace,
    paths: WorkflowPaths,
    logger: logging.Logger,
) -> Tuple[int, Optional[AtomContext]]:
    """Execute a geometry optimisation and capture derived metrics."""
    status, context = setup_calculated_atoms(args, logger)
    if status != 0 or context is None:
        return status, None

    optimizer_cls = _resolve_optimizer(args.optimizer)
    if optimizer_cls is None:
        logger.error(
            "Unknown optimizer '%s'. Available options: %s",
            args.optimizer,
            ", ".join(sorted(OPTIMIZER_CLASSES)),
        )
        return 1, None

    logger.info("*          Optimizer: %s", optimizer_cls.__name__)
    logger.info("*")

    optimizer = optimizer_cls(
        context.atoms,
        trajectory=str(paths.trajectory),
        logfile=LoggerWriter(logger),
    )

    start_time = datetime.now()
    logger.info("*****************************************************************************",)
    logger.info("*                         Geometry optimization                             *",)
    logger.info("*****************************************************************************",)
    logger.info("*")
    logger.info("%s Running GeoOpt using device %s", start_time, context.device)
    logger.info("*")
    logger.info("Target fmax %s eV/A. Max number of iterations %s", args.grad, args.iter)
    logger.info("*")

    log_geometry(logger, context.atoms, "Initial geometry for GeoOpt (Å):")

    try:
        run_result = optimizer.run(fmax=args.grad, steps=args.iter)
    except Exception as exc:
        logger.error("Optimizer failed: %s", exc)
        return 1, None

    finish_time = datetime.now()
    converged = _optimizer_converged(optimizer, run_result)

    if converged:
        logger.info("%s Optimization Finished", finish_time)
    else:
        logger.error(
            "%s GeoOpt stopped: maximum iterations reached without convergence.",
            finish_time,
        )
        return 1, None
    logger.info("")
    logger.info("*****************************************************************************",)
    logger.info("*                          Final GeoOpt Results                              *")
    logger.info("*****************************************************************************",)
    logger.info("*")
    log_geometry(logger, context.atoms, "Final geometry (Å):")
    logger.info("*")

    potential_energy = context.atoms.get_potential_energy()
    total_energy = context.atoms.get_total_energy()

    logger.info("Potential Energy: %s eV", potential_energy)
    logger.info("Total Energy:     %s eV", total_energy)
    logger.info("*")

    try:
        atomic_sum = Sum_of_atomic_energies(
            context.counts,
            args.mlff_chk,
            args.mlff_task,
            context.device,
            logger=logger,
        )
    except Exception as exc:
        logger.error("Failed to compute sum of atomic energies: %s", exc)
        return 1, None

    bonding_energy = total_energy - atomic_sum
    logger.info("*")
    logger.info("Sum of atomic energies: %s eV", atomic_sum)
    logger.info("Bonding Energy: %s eV", bonding_energy)
    logger.info("Bonding Energy: %s kcal.mol-1", bonding_energy*23.0609)
    logger.info("*")

    trajectory = read(filename=str(paths.trajectory), index=":")
    rmsd_value = rmsd_simple(trajectory[0], trajectory[-1])
    logger.info("RMSD between first (initial) and last(optimized) geometries: %.6f Å", rmsd_value)
    logger.info("*")

    write(str(paths.final_geometry), context.atoms)
    logger.info("Final geometry in %s", str(paths.final_geometry))
    logger.info("Check results in %s", str(paths.log))
    logger.info("GeoOpt movie in %s", str(paths.trajectory))
    logger.info("*")
    logger.info("End of GeoOpt")

    if args.visualize:
        view(trajectory)

    return 0, context


def run_single_point(
    args: Namespace,
    paths: WorkflowPaths,
    logger: logging.Logger,
) -> Tuple[int, Optional[AtomContext]]:
    """Compute single-point energies and bonding energy."""
    status, context = setup_calculated_atoms(args, logger)
    if status != 0 or context is None:
        return status, None

    atoms = context.atoms
    logger.info("*****************************************************************************",)
    logger.info("*                      Single Point Energy Calculation                      *",)
    logger.info("*****************************************************************************",)
    logger.info("*")

    logger.info("*")
    logger.info("%s Single-point energy calculation", datetime.now())
    logger.info("*")

    log_geometry(logger, atoms, "Initial geometry for Single Point (Å):")
    logger.info("*")

    potential_energy = atoms.get_potential_energy()
    total_energy = atoms.get_total_energy()

    logger.info("Potential Energy: %s eV", potential_energy)
    logger.info("Total Energy:     %s eV", total_energy)
    logger.info(" ")

    try:
        atomic_sum = Sum_of_atomic_energies(
            context.counts,
            args.mlff_chk,
            args.mlff_task,
            context.device,
            logger=logger,
        )
    except Exception as exc:
        logger.error("Failed to compute sum of atomic energies: %s", exc)
        return 1, None

    bonding_energy = total_energy - atomic_sum
    logger.info("*")
    logger.info("Sum of atomic energies: %s eV", atomic_sum)
    logger.info("Bonding Energy: %s eV", bonding_energy)
    logger.info("Bonding Energy: %s kcal.mol-1", bonding_energy*23.0609)
    logger.info("*")
    logger.info("%s End of Single Point", datetime.now())

    return 0, context


def run_vibrational_analysis(
    context: AtomContext,
    logger: logging.Logger,
    base_path: Path,
    temperature: float,
    pressure: float,
    freq_archive: Optional[Path] = None,
    *,
    skip_thermochemistry: bool = False,
) -> Tuple[int, Optional[VibrationsData]]:
    """Compute vibrational frequencies, thermochemistry (optional), and archive normal modes."""

    start_time = datetime.now()
    logger.info("*****************************************************************************",)
    logger.info("*                          Vibrational Analysis                             *",)
    logger.info("*****************************************************************************",)
    logger.info("*")
 
    logger.info(
        "%s Starting vibrational analysis on device %s (T=%.4f K, P=%.2f Pa)",
        start_time,
        context.device,
        temperature,
        pressure,
    )

    log_geometry(logger, context.atoms, "Geometry for Frequencies (Å):")
    logger.info("*")
    freq_root = base_path.parent / "freqs"
    freq_root.mkdir(parents=True, exist_ok=True)
    base_name = base_path.stem
    target_dir = freq_root / base_name
    target_dir.mkdir(parents=True, exist_ok=True)
    cache_dir = target_dir / "cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    archive_destination = freq_archive or (base_path.parent / f"{base_name}-FREQS-modes.zip")
    freq_packaged = False

    def finalize_modes() -> None:
        nonlocal freq_packaged
        if freq_packaged:
            return
        _cleanup_vibration_cache(cache_dir, target_dir, logger)
        _package_vibrational_data(target_dir, archive_destination, logger)
        freq_packaged = True

    vib_prefix = cache_dir / base_name
    vib = Vibrations(context.atoms, name=str(vib_prefix))
    vib.clean()
    vib_data: Optional[VibrationsData] = None

    original_displacements = vib.displacements

    def wrapped_displacements():
        raw_disp = list(original_displacements())
        total = len(raw_disp)
        start = datetime.now()
        for index, disp in enumerate(raw_disp, start=1):
            if disp.name != "eq":
                logger.info(
                    "%s Vibrational displacement %s/%s (%s) in progress.",
                    datetime.now(),
                    index,
                    total,
                    disp.name,
                )
            yield disp
        logger.info(
            "%s Completed vibrational displacements (%s entries) in %s.",
            datetime.now(),
            total,
            datetime.now() - start,
        )

    vib.displacements = wrapped_displacements  # type: ignore[assignment]

    try:
        vib.run()
    except Exception as exc:
        logger.error("Failed to compute vibrational modes: %s", exc)
        _cleanup_vibration_cache(cache_dir, target_dir, logger)
        return 1, None
    finally:
        vib.displacements = original_displacements

    try:
        vib_data = vib.get_vibrations()
    except Exception as exc:  # pragma: no cover - ASE internals may vary
        logger.warning("Unable to cache VibrationsData for mode inspection: %s", exc)
        vib_data = None

    end_time = datetime.now()
    logger.info("%s Vibrational analysis completed. Normal modes stored under %s", end_time, target_dir)
    if vib_data is not None:
        _log_normal_mode_matrices(vib_data, context.atoms, logger)
    logger.info("*")

    raw_energies: Optional[np.ndarray] = None
    try:
        if vib_data is not None:
            raw_energies = vib_data.get_energies()
        else:
            raw_energies = vib.get_energies()
    except ValueError as exc:
        logger.error("Unable to retrieve vibrational energies: %s", exc)
        finalize_modes()
        return 1, vib_data

    try:
        vib_energies = _sanitize_vibrational_energies(raw_energies, logger)
    except ValueError as exc:
        logger.error("Imaginary vibrational energies are present: %s", exc)
        finalize_modes()
        return 1, vib_data

    try:
        _, summary_output = capture_stdout(vib.summary)
        if summary_output:
            logger.info("Vibrational summary:\n%s", summary_output.rstrip())
        else:
            logger.info("Vibrational summary: <no output>")
    except Exception as exc:  # pragma: no cover - ASE behaviour varies
        logger.warning("Unable to print vibration summary: %s", exc)

    try:
        vib.write_mode()
    except Exception as exc:  # pragma: no cover - optional
        logger.warning("Unable to write vibrational modes: %s", exc)
    finally:
        finalize_modes()
    if skip_thermochemistry:
        logger.info("Thermochemistry analysis skipped for transition-state preparation.")
        logger.info("*")
        logger.info("%s End of Vibrational Analysis", datetime.now())
        return 0, vib_data

    potential_energy = context.atoms.get_potential_energy()
    try:
        thermo = IdealGasThermo(
            vib_energies=vib_energies,
            potentialenergy=potential_energy,
            atoms=context.atoms,
            geometry="nonlinear",
            symmetrynumber=1,
            spin=0,
        )
    except ValueError:
        logger.error("ValueError: Imaginary vibrational energies prevent further Thermochemistry analysis")
        finalize_modes()
        return 1, vib_data
    if hasattr(thermo, "summary"):
        try:
            _, thermo_output = capture_stdout(
                thermo.summary,
                temperature=temperature,
                pressure=pressure,
                verbose=True,
            )
            if thermo_output:
                logger.info("Thermochemistry summary (IdealGasThermo):\n%s", thermo_output.rstrip())
        except Exception as exc:  # pragma: no cover - optional
            logger.warning("IdealGasThermo.summary failed: %s", exc)
    else:
        property_specs = []
        recorded_lines = []
        for label, method_name, kwargs, unit in property_specs:
            method = getattr(thermo, method_name, None)
            if callable(method):
                try:
                    value, prop_output = capture_stdout(method, **kwargs)
                except Exception as exc:  # pragma: no cover - optional
                    logger.warning("Unable to evaluate %s: %s", label.lower(), exc)
                else:
                    if prop_output:
                        logger.info(prop_output.rstrip())
                    recorded_lines.append(f"  {label}: {value} {unit}")
        if recorded_lines:
            logger.info("Thermochemistry (IdealGasThermo):\n%s", "\n".join(recorded_lines))

    try:
        gibbs, gibbs_output = capture_stdout(
            thermo.get_gibbs_energy,
            temperature=temperature,
            pressure=pressure,
        )
        if gibbs_output:
            logger.info("IdealGasThermo main output:\n%s", gibbs_output.rstrip())
    except Exception as exc:
        logger.warning("Unable to compute Gibbs free energy: %s", exc)
        finalize_modes()
        return 1, vib_data
    logger.info("*")
    finish_timestamp = datetime.now()
    logger.info("%s End of Vibrational Analysis", finish_timestamp)

    finalize_modes()
    return 0, vib_data


def _select_lowest_curvature_mode(
    vib_data: VibrationsData,
    logger: logging.Logger,
) -> Tuple[Optional[np.ndarray], Optional[int], Optional[float], Optional[float]]:
    """Return the normalized displacement vector of the softest vibrational mode."""
    try:
        energies, modes = vib_data.get_energies_and_modes()
    except Exception as exc:  # pragma: no cover - ASE internals
        logger.error("Unable to access vibrational modes: %s", exc)
        return None, None, None, None

    if energies is None or len(energies) == 0 or modes is None or len(modes) == 0:
        logger.error("Vibrational calculation did not produce any modes.")
        return None, None, None, None

    energy_array = np.asarray(energies)
    if energy_array.size == 0:
        logger.error("Unable to identify lowest curvature mode.")
        return None, None, None, None

    freq_complex = energy_array / units.invcm if units.invcm else energy_array
    imag_component = np.abs(np.imag(freq_complex))
    real_component = np.real(freq_complex)
    curvature_cm_values = np.where(imag_component > 1e-6, -imag_component, real_component)

    mode_index = int(np.argmin(curvature_cm_values))
    curvature_cm = float(curvature_cm_values[mode_index])
    curvature = curvature_cm * units.invcm if units.invcm else float(energy_array[mode_index].real)

    mode_candidate = np.array(modes)[mode_index]
    mode_candidate = np.array(mode_candidate, dtype=float)
    norm = float(np.linalg.norm(mode_candidate))
    if not np.isfinite(norm) or norm == 0.0:
        logger.error("Selected eigenmode %d has invalid norm.", mode_index)
        return None, None, None, None

    return mode_candidate / norm, mode_index, curvature, curvature_cm


def _sanitize_vibrational_energies(
    energies: Iterable[complex],
    logger: logging.Logger,
    threshold_cm: float = 100.0,
) -> np.ndarray:
    """Convert near-zero imaginary frequencies into positive reals for thermochemistry."""
    array = np.asarray(list(energies), dtype=complex)
    if array.size == 0:
        return np.array([], dtype=float)

    sanitized = np.empty_like(array, dtype=float)
    adjustments: list[tuple[int, float]] = []
    sizable_imag: list[tuple[int, float]] = []
    tol_cm = 1e-3

    for idx, value in enumerate(array):
        freq_cm = value / units.invcm if units.invcm else value
        freq_real = float(np.real(freq_cm))
        freq_imag = float(np.imag(freq_cm))

        if not np.isfinite(freq_imag) or not np.isfinite(freq_real):
            sizable_imag.append((idx, freq_imag))
            continue

        if abs(freq_imag) <= tol_cm:
            sanitized[idx] = abs(freq_real) * units.invcm
            continue

        if abs(freq_imag) <= threshold_cm:
            sanitized[idx] = abs(freq_imag) * units.invcm
            adjustments.append((idx, freq_imag))
        else:
            sanitized[idx] = freq_cm.real * units.invcm
            sizable_imag.append((idx, freq_imag))

    if len(sizable_imag) > 1:
        details = ", ".join(f"mode {idx} ({value:.2f} cm^-1)" for idx, value in sizable_imag)
        raise ValueError(f"Imaginary vibrational modes exceed tolerance: {details}")
    if len(sizable_imag) == 1:
        idx, value = sizable_imag[0]
        logger.info(
            "Single significant imaginary mode retained for TS validation: mode %d (%.2f cm^-1).",
            idx,
            value,
        )

    if adjustments:
        logger.info(
            "Converted %d near-zero imaginary modes (<%.1f cm^-1) to real frequencies: %s",
            len(adjustments),
            threshold_cm,
            ", ".join(f"mode {idx} ({value:.2f} cm^-1)" for idx, value in adjustments),
        )

    return sanitized


def run_transition_state_search(
    args: Namespace,
    paths: WorkflowPaths,
    logger: logging.Logger,
    base_path: Path,
    context: Optional[AtomContext],
) -> Tuple[int, Optional[AtomContext]]:
    """Locate a transition state using a freshly computed vibrational analysis plus dimer search."""
    if context is None:
        status, context = setup_calculated_atoms(args, logger)
        if status != 0 or context is None:
            return status, None

    logger.info("*****************************************************************************")
    logger.info("*                         Transition State Search                           *")
    logger.info("*****************************************************************************")
    logger.info("* Plan: (1) preconditioning frequency run (thermochemistry skipped),")
    logger.info("*       (2) dimer-based TS search,")
    logger.info("*       (3) final frequency/thermochemistry validation on the saddle point.")
    logger.info("*")

    logger.info("************  Phase 1: Initial Vibrational Analysis (TS seed)  *************")

    freq_status, vib_data = run_vibrational_analysis(
        context,
        logger,
        base_path,
        args.temp,
        args.press,
        paths.freq_archive,
        skip_thermochemistry=True,
    )
    if freq_status != 0:
        return freq_status, None

    if vib_data is None:
        logger.error("Vibrational data unavailable; cannot seed dimer search.")
        return 1, None

    logger.info("*")
    logger.info("***************  Phase 2: Transition State Search (Dimer)  *****************")
    logger.info(
        "Running dimer TS search with fmax %.4f eV/Å and up to %d steps.",
        args.grad,
        args.iter,
    )
    logger.info("*")

    eigenmode, mode_index, curvature, curvature_cm = _select_lowest_curvature_mode(vib_data, logger)
    if eigenmode is None or mode_index is None or curvature is None:
        logger.error("Unable to select a vibrational eigenmode for the TS search.")
        return 1, None

    if curvature_cm is not None:
        logger.info(
            "Using vibrational mode #%d with curvature %.2f cm^-1 (%.6f eV) to initialize the dimer search.",
            mode_index,
            curvature_cm,
            curvature,
        )
    else:
        logger.info(
            "Using vibrational mode #%d with curvature %.6f eV to initialize the dimer search.",
            mode_index,
            curvature,
        )

    control_log = LoggerWriter(logger)
    dimer_control = DimerControl(
        logfile=control_log,
        eigenmode_logfile=control_log,
        dimer_separation=args.ts_dimer_separation,
        trial_trans_step=args.ts_trial_step,
        maximum_translation=args.ts_max_step,
        max_num_rot=args.ts_max_rot,
    )

    dimer_atoms = MinModeAtoms(context.atoms, control=dimer_control)
    try:
        dimer_atoms.initialize_eigenmodes(eigenmodes=[eigenmode])
    except Exception as exc:
        logger.error("Failed to initialise dimer eigenmode: %s", exc)
        return 1, None

    displacement = getattr(args, "ts_displacement", 0.1)
    if displacement > 0:
        displacement_vector = (eigenmode * displacement).tolist()
        try:
            full_mask = [True] * len(context.atoms)
            dimer_atoms.displace(
                displacement_vector=displacement_vector,
                method="vector",
                mask=full_mask,
            )
        except Exception as exc:
            logger.warning("Unable to displace along the selected eigenmode: %s", exc)

    optimizer = MinModeTranslate(
        dimer_atoms,
        logfile=LoggerWriter(logger),
        trajectory=str(paths.trajectory),
    )

    start_time = datetime.now()
    try:
        run_result = optimizer.run(fmax=args.grad, steps=args.iter)
    except Exception as exc:
        logger.error("Dimer optimizer failed: %s", exc)
        return 1, None

    finish_time = datetime.now()
    converged = _optimizer_converged(optimizer, run_result)
    final_curvature = float(dimer_atoms.get_curvature())
    if not converged or final_curvature >= 0.0:
        logger.error(
            "%s TS search stopped without convergence (curvature %.6f eV).",
            finish_time,
            final_curvature,
        )
        return 1, None

    logger.info("*")
    logger.info("%s Transition state search converged.", finish_time)
    context.atoms = dimer_atoms.get_atoms()
    logger.info("*")
    logger.info("Final dimer curvature: %.6f eV", final_curvature)
    log_geometry(logger, context.atoms, "Transition state geometry (Å):")

    potential_energy = context.atoms.get_potential_energy()
    total_energy = context.atoms.get_total_energy()
    logger.info("Transition state potential energy: %s eV", potential_energy)
    logger.info("Transition state total energy    : %s eV", total_energy)

    try:
        atomic_sum = Sum_of_atomic_energies(
            context.counts,
            args.mlff_chk,
            args.mlff_task,
            context.device,
            logger=logger,
        )
    except Exception as exc:
        logger.error("Failed to compute sum of atomic energies: %s", exc)
        return 1, None

    bonding_energy = total_energy - atomic_sum
    logger.info("*")
    logger.info("Sum of atomic energies: %s eV", atomic_sum)
    logger.info("Relative bonding energy: %s eV", bonding_energy)
    logger.info("Relative bonding energy: %s kcal.mol-1", bonding_energy * 23.0609)
    logger.info("*")

    write(str(paths.final_geometry), context.atoms)
    logger.info("Transition state geometry stored in %s", str(paths.final_geometry))
    logger.info("Dimer trajectory written to %s", str(paths.trajectory))
    logger.info("*")

    logger.info("***************  Phase 3: Final Vibrational Validation  ********************")
    logger.info("Initiating post-TS vibrational analysis to validate the saddle point.")
    freq_dir = base_path.parent / "freqs" / base_path.stem
    cleanup_targets = [freq_dir]
    if paths.freq_archive is not None:
        cleanup_targets.append(paths.freq_archive)
    remove_if_exists(cleanup_targets)

    final_freq_status, _ = run_vibrational_analysis(
        context,
        logger,
        base_path,
        args.temp,
        args.press,
        paths.freq_archive,
    )
    if final_freq_status != 0:
        logger.error("Post-TS vibrational analysis failed.")
        return final_freq_status, None

    logger.info("End of TS search")

    if args.visualize:
        try:
            frames = read(paths.trajectory, ":")
        except Exception:  # pragma: no cover - optional viewer
            frames = None
        if frames is not None:
            view(frames)

    return 0, context
