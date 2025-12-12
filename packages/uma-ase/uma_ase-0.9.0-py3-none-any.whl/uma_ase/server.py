"""Flask service exposing uma-ase workflows for web clients."""

from __future__ import annotations

import io
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import uuid
import zipfile
from collections import Counter
from contextlib import suppress
from dataclasses import dataclass
from datetime import datetime
from importlib import metadata as importlib_metadata
from importlib import resources
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple
from urllib.parse import urlparse
from xml.sax.saxutils import escape
import xml.etree.ElementTree as ET

import requests

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

try:
    from docx import Document

    DRIVER_DOCX_AVAILABLE = True
except ModuleNotFoundError:
    DRIVER_DOCX_AVAILABLE = False

from flask import Flask, Response, abort, after_this_request, jsonify, request, send_file
from werkzeug.utils import secure_filename

from ase.io import read, write, Trajectory
from ase import Atoms, units
from ase.geometry import cellpar_to_cell
from ase.md.langevin import Langevin
from ase.md.verlet import VelocityVerlet
from ase.md.nvtberendsen import NVTBerendsen
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution, Stationary, ZeroRotation

try:  # Optional engines that may not be present in older ASE releases.
    from ase.md.nose_hoover_chain import NoseHooverChainNVT, IsotropicMTKNPT, MTKNPT
except ModuleNotFoundError:  # pragma: no cover - depends on ASE version
    NoseHooverChainNVT = None
    IsotropicMTKNPT = None
    MTKNPT = None

try:
    from ase.md.bussi import Bussi
except ModuleNotFoundError:  # pragma: no cover
    Bussi = None

try:
    from ase.md.andersen import Andersen
except ModuleNotFoundError:  # pragma: no cover
    Andersen = None

try:
    from ase.md.nptberendsen import NPTBerendsen
except ModuleNotFoundError:  # pragma: no cover
    NPTBerendsen = None

try:
    from ase.md.langevinbaoab import LangevinBAOAB
except ModuleNotFoundError:  # pragma: no cover
    LangevinBAOAB = None

try:
    from ase.md.melchionna import MelchionnaNPT
except ModuleNotFoundError:  # pragma: no cover
    MelchionnaNPT = None

from py_iochem.RESTAPIManager import CollectionHandler

from .styled_rmsd_report import generate_report, _write_basic_docx as _write_basic_report_docx
from .utils import extract_xyz_metadata
from .workflows import (
    build_output_paths,
    select_device,
    TorchUnavailable,
    setup_calculated_atoms,
    configure_logging,
)

MD_ENGINE_LABELS = {
    "langevin": "Langevin (NVT)",
    "velocity_verlet": "VelocityVerlet (NVE)",
    "nvt_berendsen": "NVT Berendsen",
    "nose_hoover_chain": "Nosé-Hoover Chain (NVT)",
    "bussi": "Bussi (NVT)",
    "andersen": "Andersen (NVT)",
    "langevin_baoab_nvt": "Langevin-Hoover BAOAB (NVT)",
    "npt_berendsen": "NPT Berendsen",
    "isotropic_mtk_npt": "Isotropic MTK (NPT)",
    "mtk_npt": "Full MTK (NPT)",
    "langevin_baoab_npt": "Langevin-Hoover BAOAB (NPT)",
    "melchionna_npt": "Melchionna NPT",
}

README_BASENAME = "README.md"
_README_CONTENT_CACHE: Optional[str] = None


def _find_local_readme() -> Optional[Path]:
    current = Path(__file__).resolve()
    for parent in current.parents:
        candidate = parent / README_BASENAME
        if candidate.is_file():
            return candidate
    return None


def _load_readme_from_metadata() -> Optional[str]:
    package_name = "uma-ase"
    try:
        metadata = importlib_metadata.metadata(package_name)
    except importlib_metadata.PackageNotFoundError:
        return None
    description = metadata.get("Description")
    if description:
        return description
    return None


def _read_readme_text() -> str:
    global _README_CONTENT_CACHE
    if _README_CONTENT_CACHE is not None:
        return _README_CONTENT_CACHE
    readme_path = _find_local_readme()
    if readme_path is not None:
        _README_CONTENT_CACHE = readme_path.read_text(encoding="utf-8", errors="replace")
        return _README_CONTENT_CACHE
    metadata_text = _load_readme_from_metadata()
    if metadata_text:
        _README_CONTENT_CACHE = metadata_text
        return _README_CONTENT_CACHE
    raise FileNotFoundError("README.md content is unavailable.")


def _parse_float_field(
    form,
    field: str,
    default: Optional[float],
    *,
    label: str,
    min_value: Optional[float] = None,
    min_inclusive: bool = True,
    max_value: Optional[float] = None,
    max_inclusive: bool = True,
    required: bool = False,
) -> Optional[float]:
    raw = form.get(field)
    if raw is None or raw.strip() == "":
        if required:
            raise ValueError(f"{label} is required.")
        return float(default) if default is not None else None
    try:
        value = float(raw)
    except (TypeError, ValueError):
        raise ValueError(f"{label} must be a number.") from None
    if min_value is not None:
        if value < min_value or (not min_inclusive and value == min_value):
            comparator = "greater than" if not min_inclusive else "at least"
            raise ValueError(f"{label} must be {comparator} {min_value}.")
    if max_value is not None:
        if value > max_value or (not max_inclusive and value == max_value):
            comparator = "less than" if not max_inclusive else "at most"
            raise ValueError(f"{label} must be {comparator} {max_value}.")
    return value


def _parse_int_field(
    form,
    field: str,
    default: Optional[int],
    *,
    label: str,
    min_value: Optional[int] = None,
    min_inclusive: bool = True,
    required: bool = False,
) -> Optional[int]:
    raw = form.get(field)
    if raw is None or raw.strip() == "":
        if required:
            raise ValueError(f"{label} is required.")
        return int(default) if default is not None else None
    try:
        value = int(raw)
    except (TypeError, ValueError):
        raise ValueError(f"{label} must be an integer.") from None
    if min_value is not None:
        if value < min_value or (not min_inclusive and value == min_value):
            comparator = "greater than" if not min_inclusive else "at least"
            raise ValueError(f"{label} must be {comparator} {min_value}.")
    return value


def _normalize_iochem_handle(raw_handle: str) -> str:
    if raw_handle is None:
        raise ValueError("Handle is required.")
    handle = str(raw_handle).strip()
    if not handle:
        raise ValueError("Handle is required.")
    parsed = urlparse(handle)
    path = parsed.path or ""
    if parsed.netloc and not path:
        path = "/"
    target = path or handle
    lower_target = target.lower()
    if "handle/" in lower_target:
        idx = lower_target.index("handle/") + len("handle/")
        target = target[idx:]
    target = target.strip().strip("/").split("?", 1)[0].split("#", 1)[0]
    if not target:
        raise ValueError("Handle is required.")
    return target


def _build_iochem_source_url(handle: str, raw_handle: Optional[str] = None) -> str:
    base = None
    if raw_handle:
        parsed = urlparse(str(raw_handle).strip())
        if parsed.scheme and parsed.netloc:
            base = f"{parsed.scheme}://{parsed.netloc}".rstrip("/")
    if not base:
        base = "https://www.iochem-bd.org"
    return f"{base}/handle/{handle}"


def _resolve_iochem_rest_url(raw_handle: str) -> str:
    configured = str(app.config.get("IOCHEM_REST_URL") or IOCHEM_DEFAULT_REST_URL)
    handle_str = str(raw_handle or "").strip()
    parsed = urlparse(handle_str)
    if parsed.scheme and parsed.netloc:
        base = f"{parsed.scheme}://{parsed.netloc}".rstrip("/")
        if base.endswith("/rest"):
            return base
        return f"{base}/rest"
    return configured


def _safe_int_from_string(value: Optional[str], default: Optional[int] = None) -> Optional[int]:
    if value is None:
        return default
    text = str(value).strip()
    if not text:
        return default
    try:
        return int(round(float(text)))
    except (TypeError, ValueError):
        return default


def _find_scalar_value(node: ET.Element, dict_refs: Iterable[str]) -> Optional[str]:
    if node is None:
        return None
    for dict_ref in dict_refs:
        scalar = node.find(f".//cml:scalar[@dictRef='{dict_ref}']", CML_NAMESPACE)
        if scalar is not None:
            text = scalar.text.strip() if scalar.text else ""
            if text:
                return text
    return None


def _fetch_iochem_handle_metadata(handle: str, rest_url: str, *, verify: bool = True) -> Dict[str, Any]:
    normalized_base = rest_url.rstrip("/")
    url = f"{normalized_base}/handle/{handle}"
    try:
        resp = requests.get(url, headers={"Accept": "application/json"}, timeout=30, verify=verify)
    except requests.exceptions.SSLError as exc:
        raise ValueError(
            "TLS verification failed when contacting ioChem-BD. "
            "Set UMA_ASE_IOCHEM_VERIFY=0 to skip certificate checks."
        ) from exc
    except requests.RequestException as exc:
        raise ValueError("Unable to contact ioChem-BD REST endpoint.") from exc
    if resp.status_code >= 400:
        raise ValueError(f"ioChem-BD returned HTTP {resp.status_code} for handle lookup.")
    try:
        return resp.json()
    except ValueError as exc:
        raise ValueError("ioChem-BD returned an invalid response for the requested handle.") from exc


def _download_iochem_item_cml(rest_url: str, item_identifier: str, *, verify: bool = True) -> str:
    base_url = rest_url.rstrip("/")
    bitstreams_url = f"{base_url}/items/{item_identifier}/bitstreams"
    try:
        resp = requests.get(bitstreams_url, headers={"Accept": "application/json"}, timeout=30, verify=verify)
    except requests.exceptions.SSLError as exc:
        raise ValueError(
            "TLS verification failed when contacting ioChem-BD. "
            "Set UMA_ASE_IOCHEM_VERIFY=0 to skip certificate checks."
        ) from exc
    except requests.RequestException as exc:
        raise ValueError("Unable to list files for the requested ioChem-BD calculation.") from exc
    if resp.status_code >= 400:
        raise ValueError(f"Unable to list bitstreams for the requested calculation (HTTP {resp.status_code}).")
    try:
        entries = resp.json()
    except ValueError as exc:
        raise ValueError("ioChem-BD returned invalid bitstream metadata.") from exc
    if not isinstance(entries, list) or not entries:
        raise ValueError("The ioChem-BD handle has no files attached.")

    def is_output(entry: Dict[str, Any]) -> bool:
        name = (entry.get("name") or "").strip().lower()
        if name == "output.cml":
            return True
        format_name = entry.get("format") or entry.get("formatDescription")
        if isinstance(format_name, dict):
            format_name = format_name.get("description") or format_name.get("shortDescription")
        format_text = (format_name or "").strip().lower()
        return "output.cml" in format_text

    output_entry = next((entry for entry in entries if is_output(entry)), None)
    if output_entry is None:
        # If there is no explicit output.cml, fallback to the first entry.
        output_entry = entries[0]

    bitstream_id = output_entry.get("uuid") or output_entry.get("id")
    if not bitstream_id:
        raise ValueError("Unable to determine the bitstream identifier for the requested calculation.")

    retrieve_url = f"{base_url}/bitstreams/{bitstream_id}/retrieve"
    download_headers = {"Accept": "application/octet-stream"}
    try:
        resp = requests.get(retrieve_url, headers=download_headers, timeout=60, verify=verify)
    except requests.exceptions.SSLError as exc:
        raise ValueError(
            "TLS verification failed when contacting ioChem-BD. "
            "Set UMA_ASE_IOCHEM_VERIFY=0 to skip certificate checks."
        ) from exc
    except requests.RequestException as exc:
        raise ValueError("Unable to download the ioChem-BD output file.") from exc
    if resp.status_code >= 400:
        raise ValueError(f"Unable to download the calculation output (HTTP {resp.status_code}).")
    text = resp.text.strip()
    if not text:
        raise ValueError("The downloaded output.cml file is empty.")
    return resp.text


def _locate_cml_molecule(cml_text: str) -> ET.Element:
    try:
        root = ET.fromstring(cml_text.encode("utf-8"))
    except ET.ParseError as exc:
        raise ValueError("Downloaded CML content is invalid.") from exc
    molecules = root.findall(".//cml:molecule", CML_NAMESPACE)
    target_molecule = None
    for molecule in molecules:
        atom_array = molecule.find("cml:atomArray", CML_NAMESPACE)
        if atom_array is None:
            continue
        atoms = atom_array.findall("cml:atom", CML_NAMESPACE)
        if atoms and all(atom.get("x3") is not None for atom in atoms):
            target_molecule = molecule
    if target_molecule is None and molecules:
        target_molecule = molecules[-1]
    if target_molecule is None:
        raise ValueError("Unable to locate a molecule entry in the ioChem-BD file.")
    return target_molecule


def _extract_charge_spin_from_cml(cml_text: str) -> Tuple[int, int]:
    target_molecule = _locate_cml_molecule(cml_text)
    charge = _safe_int_from_string(target_molecule.get("formalCharge"), default=0)
    if charge is None:
        scalar_charge = _find_scalar_value(
            target_molecule,
            ("x:formalCharge", "g:charge", "a:charge", "cc:charge"),
        )
        charge = _safe_int_from_string(scalar_charge, default=0)
    spin = _safe_int_from_string(target_molecule.get("spinMultiplicity"), default=1)
    if spin is None or spin <= 0:
        scalar_spin = _find_scalar_value(
            target_molecule,
            ("x:multiplicity", "g:multiplicity", "a:multiplicity", "a:spin"),
        )
        spin = _safe_int_from_string(scalar_spin, default=1) or 1
    if spin <= 0:
        spin = 1
    return charge or 0, spin


def _atoms_from_cml_text(cml_text: str):
    target_molecule = _locate_cml_molecule(cml_text)
    atom_array = target_molecule.find("cml:atomArray", CML_NAMESPACE)
    if atom_array is None:
        raise ValueError("The ioChem-BD output lacks a valid atomic coordinate array.")
    symbols = []
    positions = []
    for atom in atom_array.findall("cml:atom", CML_NAMESPACE):
        symbol = atom.get("elementType")
        x3 = atom.get("x3")
        y3 = atom.get("y3")
        z3 = atom.get("z3")
        if not symbol or x3 is None or y3 is None or z3 is None:
            continue
        try:
            positions.append([float(x3), float(y3), float(z3)])
            symbols.append(symbol)
        except ValueError:
            continue
    if not symbols or len(symbols) != len(positions):
        raise ValueError("Unable to extract atomic coordinates from ioChem-BD output.")
    return Atoms(symbols=symbols, positions=positions)


def _atoms_to_xyz(atoms, source_url: str, charge: int, spin: int) -> str:
    symbols = atoms.get_chemical_symbols()
    positions = atoms.get_positions()
    if len(symbols) != len(positions):
        raise ValueError("Geometry is inconsistent.")
    header_parts = []
    if source_url:
        header_parts.append(source_url)
    header_parts.append(str(charge))
    header_parts.append(str(spin))
    comment = " ".join(part for part in header_parts if part) or "ioChem-BD geometry"
    lines = [str(len(symbols)), comment]
    for symbol, (x, y, z) in zip(symbols, positions):
        lines.append(f"{symbol:<3} {x: .10f} {y: .10f} {z: .10f}")
    return "\n".join(lines) + "\n"


def _download_iochem_cml(handler: CollectionHandler, item_id: str) -> str:
    try:
        file_url = handler.query_target_file_id(item_id, "output.cml")
    except KeyError as exc:
        raise ValueError("The provided handle does not expose an output.cml file.") from exc
    try:
        response = requests.get(
            file_url,
            headers=handler.headers.get("GET"),
            verify=getattr(handler, "verify", True),
            timeout=60,
        )
    except requests.exceptions.SSLError as exc:
        raise ValueError(
            "TLS verification failed when contacting ioChem-BD. "
            "Set UMA_ASE_IOCHEM_VERIFY=0 to skip certificate checks."
        ) from exc
    except requests.RequestException as exc:
        raise ValueError("Unable to download the ioChem-BD output file.") from exc
    if response.status_code >= 400:
        raise ValueError(f"Unable to download output.cml (HTTP {response.status_code}).")
    text = response.text.strip()
    if not text:
        raise ValueError("ioChem-BD returned an empty output.cml file.")
    return response.text


def _download_iochem_geometry(raw_handle: str) -> IoChemGeometry:
    handle = _normalize_iochem_handle(raw_handle)
    rest_url = _resolve_iochem_rest_url(raw_handle)
    verify_ssl = bool(app.config.get("IOCHEM_VERIFY", True))
    try:
        handle_metadata = _fetch_iochem_handle_metadata(handle, rest_url, verify=verify_ssl)
    except Exception as exc:
        raise ValueError("Unable to query ioChem-BD REST API.") from exc

    # Determine whether the handle points to a collection (with numberItems) or to an individual calculation.
    is_collection = isinstance(handle_metadata, dict) and ("numberItems" in handle_metadata)

    if is_collection:
        try:
            handler = CollectionHandler(rest_url, handle, token="", service="browse", verify=verify_ssl)
            items = handler.get_items()
        except Exception as exc:  # pragma: no cover - network dependency
            raise ValueError("Unable to query ioChem-BD REST API.") from exc
        if not items:
            raise ValueError(f"No calculations found for handle '{handle}'.")
        target = items[0]
        item_id = target.get(handler.idField)
        if not item_id:
            raise ValueError("Unable to determine the calculation identifier for this handle.")
        cml_text = _download_iochem_cml(handler, item_id)
    else:
        item_identifier = handle_metadata.get("uuid") or handle_metadata.get("id")
        if not item_identifier:
            raise ValueError("The ioChem-BD handle response is missing an identifier for the calculation.")
        cml_text = _download_iochem_item_cml(rest_url, str(item_identifier), verify=verify_ssl)
    charge, spin = _extract_charge_spin_from_cml(cml_text)
    atoms = _atoms_from_cml_text(cml_text)
    atoms.info["charge"] = charge
    atoms.info["spin"] = spin
    source_url = _build_iochem_source_url(handle, raw_handle=raw_handle)
    xyz_content = _atoms_to_xyz(atoms, source_url, charge, spin)
    formula = atoms.get_chemical_formula()
    num_atoms = len(atoms)
    element_counts = dict(Counter(atoms.get_chemical_symbols()))
    filename = f"ioChem_{handle.replace('/', '_')}.xyz"
    return IoChemGeometry(
        handle=handle,
        source_url=source_url,
        filename=filename,
        xyz_content=xyz_content,
        charge=charge,
        spin=spin,
        formula=formula,
        num_atoms=num_atoms,
        element_counts=element_counts,
    )


def _parse_bool_field(form, field: str, default: bool = False) -> bool:
    raw = form.get(field)
    if raw is None:
        return default
    return raw.strip().lower() in ("1", "true", "yes", "on")


def _missing_engine_builder(engine_key: str, module_hint: str):
    def _builder(*_):
        raise RuntimeError(
            f"The '{engine_key}' MD engine requires {module_hint}, but it is not available in the installed ASE. "
            "Update ASE or choose a different engine."
        )

    return _builder


def _build_md_builder_params(md_options: Dict[str, Any]) -> SimpleNamespace:
    temperature = md_options.get("temperature", 300.0)
    timestep = md_options.get("timestep_fs", 0.5) * units.fs
    friction_coeff = max(0.0, md_options.get("friction", 0.0)) / units.fs
    relax_fs = max(1e-12, md_options.get("relax_fs", 100.0))
    relax_time = relax_fs * units.fs
    pressure_bar = md_options.get("pressure_bar", 1.0)
    compressibility_bar = md_options.get("compressibility_bar", 0.0)
    compressibility_au = compressibility_bar / units.bar if compressibility_bar and compressibility_bar > 0 else None
    barostat_relax = max(1e-12, md_options.get("barostat_relax_fs", 1000.0)) * units.fs
    nose_tdamp = max(1e-12, md_options.get("nose_tdamp_fs", relax_fs)) * units.fs
    bussi_taut = max(1e-12, md_options.get("bussi_taut_fs", relax_fs)) * units.fs
    baoab_ttau = max(1e-12, md_options.get("baoab_ttau_fs", 50.0)) * units.fs
    baoab_ptau = max(1e-12, md_options.get("baoab_ptau_fs", 1000.0)) * units.fs
    melchionna_ttime = max(0.0, md_options.get("melchionna_ttime_fs", 25.0)) * units.fs
    melchionna_ptime = max(0.0, md_options.get("melchionna_ptime_fs", 75.0)) * units.fs
    return SimpleNamespace(
        temperature=temperature,
        timestep=timestep,
        friction=friction_coeff,
        relax=relax_time,
        pressure_bar=pressure_bar,
        pressure_au=pressure_bar * units.bar,
        compressibility_au=compressibility_au,
        barostat_relax=barostat_relax,
        nose_tdamp=nose_tdamp,
        nose_tchain=int(md_options.get("nose_tchain", 3)),
        nose_tloop=int(md_options.get("nose_tloop", 1)),
        bussi_taut=bussi_taut,
        andersen_prob=float(md_options.get("andersen_prob", 0.0)),
        mtk_tdamp=max(1e-12, md_options.get("mtk_tdamp_fs", 100.0)) * units.fs,
        mtk_pdamp=max(1e-12, md_options.get("mtk_pdamp_fs", 1000.0)) * units.fs,
        mtk_tchain=int(md_options.get("mtk_tchain", 3)),
        mtk_pchain=int(md_options.get("mtk_pchain", 3)),
        mtk_tloop=int(md_options.get("mtk_tloop", 1)),
        mtk_ploop=int(md_options.get("mtk_ploop", 1)),
        baoab_ttau=baoab_ttau,
        baoab_ptau=baoab_ptau,
        baoab_pmass=md_options.get("baoab_pmass"),
        baoab_pmass_factor=md_options.get("baoab_pmass_factor", 1.0),
        baoab_hydrostatic=bool(md_options.get("baoab_hydrostatic")),
        melchionna_ttime=melchionna_ttime if melchionna_ttime > 0 else None,
        melchionna_ptime=melchionna_ptime if melchionna_ptime > 0 else None,
        melchionna_bulk=md_options.get("melchionna_bulk_gpa", 0.0) * units.GPa,
        melchionna_mask=md_options.get("melchionna_mask"),
    )


MD_ENGINE_BUILDERS: Dict[str, Callable[[Any, SimpleNamespace], Any]] = {
    "langevin": lambda atoms, p: Langevin(
        atoms,
        p.timestep,
        temperature_K=p.temperature,
        friction=p.friction,
    ),
    "velocity_verlet": lambda atoms, p: VelocityVerlet(atoms, p.timestep),
    "nvt_berendsen": lambda atoms, p: NVTBerendsen(
        atoms,
        p.timestep,
        temperature_K=p.temperature,
        taut=p.relax,
    ),
}

MD_ENGINE_BUILDERS["bussi"] = (
    (lambda atoms, p: Bussi(atoms, p.timestep, temperature_K=p.temperature, taut=p.bussi_taut))
    if Bussi is not None
    else _missing_engine_builder("bussi", "ase.md.bussi.Bussi")
)

MD_ENGINE_BUILDERS["andersen"] = (
    (lambda atoms, p: Andersen(atoms, p.timestep, temperature_K=p.temperature, andersen_prob=p.andersen_prob))
    if Andersen is not None
    else _missing_engine_builder("andersen", "ase.md.andersen.Andersen")
)

MD_ENGINE_BUILDERS["npt_berendsen"] = (
    (
        lambda atoms, p: NPTBerendsen(
            atoms,
            p.timestep,
            temperature_K=p.temperature,
            pressure_au=p.pressure_au,
            taut=p.relax,
            taup=p.barostat_relax,
            compressibility_au=p.compressibility_au,
        )
    )
    if NPTBerendsen is not None
    else _missing_engine_builder("npt_berendsen", "ase.md.nptberendsen.NPTBerendsen")
)

MD_ENGINE_BUILDERS["nose_hoover_chain"] = (
    (
        lambda atoms, p: NoseHooverChainNVT(
            atoms,
            p.timestep,
            temperature_K=p.temperature,
            tdamp=p.nose_tdamp,
            tchain=p.nose_tchain,
            tloop=p.nose_tloop,
        )
    )
    if NoseHooverChainNVT is not None
    else _missing_engine_builder("nose_hoover_chain", "ase.md.nose_hoover_chain.NoseHooverChainNVT")
)

MD_ENGINE_BUILDERS["isotropic_mtk_npt"] = (
    (
        lambda atoms, p: IsotropicMTKNPT(
            atoms,
            p.timestep,
            temperature_K=p.temperature,
            pressure_au=p.pressure_au,
            tdamp=p.mtk_tdamp,
            pdamp=p.mtk_pdamp,
            tchain=p.mtk_tchain,
            pchain=p.mtk_pchain,
            tloop=p.mtk_tloop,
            ploop=p.mtk_ploop,
        )
    )
    if IsotropicMTKNPT is not None
    else _missing_engine_builder("isotropic_mtk_npt", "ase.md.nose_hoover_chain.IsotropicMTKNPT")
)

MD_ENGINE_BUILDERS["mtk_npt"] = (
    (
        lambda atoms, p: MTKNPT(
            atoms,
            p.timestep,
            temperature_K=p.temperature,
            pressure_au=p.pressure_au,
            tdamp=p.mtk_tdamp,
            pdamp=p.mtk_pdamp,
            tchain=p.mtk_tchain,
            pchain=p.mtk_pchain,
            tloop=p.mtk_tloop,
            ploop=p.mtk_ploop,
        )
    )
    if MTKNPT is not None
    else _missing_engine_builder("mtk_npt", "ase.md.nose_hoover_chain.MTKNPT")
)

MD_ENGINE_BUILDERS["langevin_baoab_nvt"] = (
    (
        lambda atoms, p: LangevinBAOAB(
            atoms,
            p.timestep,
            temperature_K=p.temperature,
            T_tau=p.baoab_ttau,
        )
    )
    if LangevinBAOAB is not None
    else _missing_engine_builder("langevin_baoab_nvt", "ase.md.langevinbaoab.LangevinBAOAB")
)

MD_ENGINE_BUILDERS["langevin_baoab_npt"] = (
    (
        lambda atoms, p: LangevinBAOAB(
            atoms,
            p.timestep,
            temperature_K=p.temperature,
            externalstress=-p.pressure_au,
            hydrostatic=p.baoab_hydrostatic,
            T_tau=p.baoab_ttau,
            P_tau=p.baoab_ptau,
            P_mass=p.baoab_pmass if p.baoab_pmass else None,
            P_mass_factor=p.baoab_pmass_factor,
        )
    )
    if LangevinBAOAB is not None
    else _missing_engine_builder("langevin_baoab_npt", "ase.md.langevinbaoab.LangevinBAOAB")
)

MD_ENGINE_BUILDERS["melchionna_npt"] = (
    (
        lambda atoms, p: MelchionnaNPT(
            atoms,
            p.timestep,
            temperature_K=p.temperature,
            externalstress=-p.pressure_au,
            ttime=p.melchionna_ttime,
            pfactor=(p.melchionna_ptime**2 * (p.melchionna_bulk or 0.0)) if p.melchionna_ptime else None,
            mask=p.melchionna_mask,
        )
    )
    if MelchionnaNPT is not None
    else _missing_engine_builder("melchionna_npt", "ase.md.melchionna.MelchionnaNPT")
)

STATIC_HTML = "uma-ase.html"
app = Flask(__name__)
IOCHEM_DEFAULT_REST_URL = os.environ.get("UMA_ASE_IOCHEM_REST_URL", "https://www.iochem-bd.org/rest")
IOCHEM_DEFAULT_VERIFY = os.environ.get("UMA_ASE_IOCHEM_VERIFY", "1").strip().lower() not in (
    "0",
    "false",
    "no",
    "off",
)
app.config.setdefault("IOCHEM_REST_URL", IOCHEM_DEFAULT_REST_URL)
app.config.setdefault("IOCHEM_VERIFY", IOCHEM_DEFAULT_VERIFY)
app.config.setdefault("UMA_RESULTS_DIR", Path.home() / ".uma_ase" / "results")
ANALYZE_REPORT_ROOT = Path(app.config["UMA_RESULTS_DIR"]) / "analyze_reports"
ANALYZE_REPORT_ROOT.mkdir(parents=True, exist_ok=True)

CML_NAMESPACE = {"cml": "http://www.xml-cml.org/schema"}


@dataclass
class IoChemGeometry:
    handle: str
    source_url: str
    filename: str
    xyz_content: str
    charge: int
    spin: int
    formula: str
    num_atoms: int
    element_counts: Dict[str, int]


@dataclass
class JobRecord:
    job_id: str
    job_dir: Path
    charge: int
    spin: int
    grad: float
    iterations: int
    run_types: List[str]
    status: str = "running"
    message: Optional[str] = None
    log_path: Optional[Path] = None
    traj_path: Optional[Path] = None
    opt_path: Optional[Path] = None
    freq_archive_path: Optional[Path] = None
    freq_folder: Optional[Path] = None
    log_url: Optional[str] = None
    traj_url: Optional[str] = None
    opt_url: Optional[str] = None
    freq_archive_url: Optional[str] = None
    traj_visual_path: Optional[Path] = None
    relative_path: Optional[Path] = None
    job_kind: str = "workflow"
    md_options: Optional[Dict[str, Any]] = None
    md_multi_xyz: Optional[Path] = None
    md_multi_xyz_url: Optional[str] = None
    cancel_event: Optional[threading.Event] = None
    worker: Optional[threading.Thread] = None
    process: Optional[subprocess.Popen] = None


JOBS: Dict[str, JobRecord] = {}
JOB_LOCK = threading.Lock()


class JobCancelled(Exception):
    """Raised internally when a running job is cancelled by the user."""


def _get_job(job_id: str) -> JobRecord:
    with JOB_LOCK:
        record = JOBS.get(job_id)
    if record is None:
        abort(404)
    return record


def _build_cli_args(
    input_path: Path,
    run_types: Iterable[str],
    charge: str,
    spin: str,
    optimizer: str,
    grad: str,
    iterations: str,
    temperature: str,
    pressure: str,
    mlff_checkpoint: str | None,
    mlff_task: str | None,
    ts_displacement: str | None = None,
    ts_dimer_separation: str | None = None,
    ts_trial_step: str | None = None,
    ts_max_step: str | None = None,
    ts_max_rot: str | None = None,
) -> List[str]:
    args: List[str] = [
        "-input",
        str(input_path),
        "-chg",
        charge,
        "-spin",
        spin,
        "-optimizer",
        optimizer,
        "-grad",
        grad,
        "-iter",
        iterations,
        "-temp",
        temperature,
        "-press",
        pressure,
    ]
    if run_types:
        args.extend(["-run-type", *run_types])
    if mlff_checkpoint:
        args.extend(["-mlff-chk", mlff_checkpoint])
    if mlff_task:
        args.extend(["-mlff-task", mlff_task])
    ts_requested = any(rt == "ts" for rt in run_types or [])
    if ts_requested:
        if ts_displacement:
            args.extend(["--ts-displacement", ts_displacement])
        if ts_dimer_separation:
            args.extend(["--ts-dimer-separation", ts_dimer_separation])
        if ts_trial_step:
            args.extend(["--ts-trial-step", ts_trial_step])
        if ts_max_step:
            args.extend(["--ts-max-step", ts_max_step])
        if ts_max_rot:
            args.extend(["--ts-max-rot", ts_max_rot])
    return args


def _initialise_md_velocities(atoms, temperature: float, logger):
    if temperature <= 0:
        logger.info("Temperature %.2f K <= 0. Skipping velocity initialisation.", temperature)
        return
    MaxwellBoltzmannDistribution(atoms, temperature_K=temperature)
    Stationary(atoms)
    ZeroRotation(atoms)
    logger.info("Initial velocities sampled at %.2f K.", temperature)


def _create_md_dynamics(engine: str, atoms, *, md_options: Dict[str, Any]):
    params = _build_md_builder_params(md_options)
    builder = MD_ENGINE_BUILDERS.get(engine)
    if builder is None:
        raise ValueError(
            "Unsupported MD engine "
            f"'{engine}'. Available: {', '.join(MD_ENGINE_LABELS)}"
        )
    return builder(atoms, params)


def _collect_log(temp_dir: Path) -> str:
    logs = sorted(temp_dir.glob("*.log"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not logs:
        return "No log file generated."
    return logs[0].read_text(encoding="utf-8", errors="replace")


def _safe_save_upload(storage, base_dir: Path) -> Path:
    filename = storage.filename or getattr(storage, "name", None)
    if not filename:
        raise ValueError("Uploaded file missing name.")
    relative_parts = [secure_filename(part) for part in Path(filename).parts if part not in ("", ".", "..")]
    if not relative_parts:
        relative_parts = [secure_filename(filename)]
    destination = base_dir.joinpath(*relative_parts)
    destination.parent.mkdir(parents=True, exist_ok=True)
    storage.save(destination)
    return destination


def _build_analyze_url(token: str, path: Path | None) -> str | None:
    if not path:
        return None
    return f"/api/uma-ase/analyze/{token}/{path.name}"


def _sanitize_relative_path(relpath: str | None) -> Path | None:
    if not relpath:
        return None
    parts = [
        secure_filename(part)
        for part in Path(relpath).parts
        if part not in ("", ".", "..")
    ]
    cleaned = [part for part in parts if part]
    if not cleaned:
        return None
    return Path(*cleaned)


def _display_label_for_upload(raw_name: str | None, saved_path: Path) -> str:
    sanitized = _sanitize_relative_path(raw_name)
    if sanitized:
        return sanitized.as_posix()
    if raw_name:
        simplified = secure_filename(Path(raw_name).name)
        if simplified:
            return simplified
    return saved_path.name


def _extract_zip_members(zip_path: Path, base_label: str) -> List[Tuple[Path, str]]:
    extract_root = zip_path.parent / f"{zip_path.stem}_unzipped"
    if extract_root.exists():
        shutil.rmtree(extract_root, ignore_errors=True)
    extract_root.mkdir(parents=True, exist_ok=True)
    extracted: List[Tuple[Path, str]] = []
    try:
        with zipfile.ZipFile(zip_path) as archive:
            for info in archive.infolist():
                if info.is_dir():
                    continue
                sanitized = _sanitize_relative_path(info.filename)
                if not sanitized:
                    continue
                destination = extract_root / sanitized
                destination.parent.mkdir(parents=True, exist_ok=True)
                with archive.open(info) as source, destination.open("wb") as target:
                    shutil.copyfileobj(source, target)
                rel_label = sanitized.as_posix()
                label = f"{base_label}/{rel_label}" if rel_label else base_label
                extracted.append((destination, label))
    except zipfile.BadZipFile as exc:
        raise ValueError(f"{zip_path.name} is not a valid ZIP archive.") from exc
    if not extracted:
        raise ValueError(f"{zip_path.name} did not contain any files.")
    return extracted


def _expand_geometry_inputs(files: List[Tuple[Path, str]]) -> Tuple[List[Tuple[Path, str]], List[Dict[str, str]]]:
    candidates: List[Tuple[Path, str]] = []
    skipped: List[Dict[str, str]] = []
    for path, label in files:
        if path.suffix.lower() == ".zip":
            try:
                extracted = _extract_zip_members(path, label)
            except ValueError as exc:
                skipped.append({"label": label, "reason": str(exc)})
                continue
            candidates.extend(extracted)
        else:
            candidates.append((path, label))
    return candidates, skipped


def _load_first_structure(path: Path):
    try:
        atoms = read(path)
        if atoms is not None:
            return atoms
    except Exception:
        pass
    with suppress(Exception):
        frames = read(path, ":")
        if isinstance(frames, list) and frames:
            return frames[0]
    if path.suffix.lower() == ".traj":
        with suppress(Exception):
            with Trajectory(path) as traj:
                if len(traj):
                    return traj[0]
    return None


def _pair_label(symbol_a: str, symbol_b: str) -> str:
    first = (symbol_a or "X").strip() or "X"
    second = (symbol_b or "X").strip() or "X"
    ordered = sorted((first, second))
    return f"{ordered[0]}-{ordered[1]}"


def _build_simple_geometry_summary(
    structures: List[Dict[str, Any]],
    pair_series: List[Dict[str, Any]],
    total_pairs: int,
    skipped: List[Dict[str, str]],
) -> str:
    timestamp = datetime.utcnow().replace(microsecond=0).isoformat()
    lines: List[str] = [
        "Simple Geometry Analysis Report",
        f"Generated at {timestamp} UTC",
        "",
        f"Structures processed: {len(structures)}",
        f"Unique pair types: {len(pair_series)}",
        f"Total interatomic pairs: {total_pairs}",
        "",
    ]
    if structures:
        lines.append("Structures")
        lines.append("----------")
        for index, entry in enumerate(structures, start=1):
            label = entry.get("label") or f"Structure {index}"
            formula = entry.get("formula") or "Unknown formula"
            atom_count = entry.get("atom_count") or "-"
            lines.append(f"{index}. {label} — {formula} ({atom_count} atoms)")
        lines.append("")
    if pair_series:
        lines.append("Pair Distance Statistics (Å)")
        lines.append("-----------------------------")
        for entry in pair_series:
            label = entry.get("label") or "Pair"
            count = entry.get("count") or 0
            minimum = entry.get("min")
            maximum = entry.get("max")
            mean_value = entry.get("mean")
            min_text = f"{minimum:.4f}" if isinstance(minimum, (int, float)) else "-"
            max_text = f"{maximum:.4f}" if isinstance(maximum, (int, float)) else "-"
            mean_text = f"{mean_value:.4f}" if isinstance(mean_value, (int, float)) else "-"
            lines.append(f"- {label}: count={count}, min={min_text}, max={max_text}, avg={mean_text}")
        lines.append("")
    if skipped:
        lines.append("Skipped files")
        lines.append("-------------")
        for entry in skipped:
            label = entry.get("label") or "Unknown file"
            reason = entry.get("reason") or "Unknown reason"
            lines.append(f"- {label}: {reason}")
        lines.append("")
    if not pair_series:
        lines.append("No interatomic distance pairs were detected.")
    lines.append("")
    lines.append("End of report.")
    return "\n".join(lines)


def _freqs_ready(record: JobRecord) -> bool:
    if record.freq_archive_path and record.freq_archive_path.exists():
        return True
    folder = record.freq_folder
    if not folder:
        return False
    if folder.exists():
        for path in folder.rglob("*"):
            if path.is_file():
                return True
    return False


def _convert_traj_tree_to_xyz(root: Path) -> int:
    """Convert any *.traj files under *root* to multi-frame XYZ."""

    converted = 0
    for traj_file in root.rglob("*.traj"):
        xyz_path = traj_file.with_suffix(".xyz")
        try:
            frames = read(traj_file, ":")
            write(xyz_path, frames, format="xyz")
            traj_file.unlink()
            converted += 1
        except Exception as exc:  # pragma: no cover - best effort
            app.logger.warning("Unable to convert %s to XYZ: %s", traj_file, exc)
    return converted


_MINMODE_LINE = re.compile(
    r"MinModeTranslate:\s*(\d+)\s+\d+:\d+:\d+\s+([+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[Ee][+-]?\d+)?)"
)


def _extract_minmode_energies(log_path: Optional[Path]) -> Dict[int, float]:
    if log_path is None or not log_path.exists():
        return {}
    energies: Dict[int, float] = {}
    try:
        for line in log_path.read_text(encoding="utf-8", errors="ignore").splitlines():
            match = _MINMODE_LINE.search(line)
            if match:
                step = int(match.group(1))
                energy = float(match.group(2))
                energies[step] = energy
    except OSError:
        return {}
    return energies


def _export_traj_for_visualization(source: Path, *, log_path: Optional[Path] = None) -> Optional[Path]:
    """Convert an ASE trajectory to multi-frame XYZ with metadata."""
    if source is None or not source.exists():
        return None
    destination = source.with_suffix(".xyz")
    try:
        frames = read(str(source), ":")
    except Exception as exc:
        app.logger.warning("Unable to read trajectory %s: %s", source, exc)
        return None

    if not frames:
        return None

    energy_by_step = _extract_minmode_energies(log_path)

    try:
        with destination.open("w", encoding="utf-8") as handle:
            for index, atoms in enumerate(frames):
                symbols = atoms.get_chemical_symbols()
                positions = atoms.get_positions()
                comment_parts = [f"step={index}"]

                energy = energy_by_step.get(index)
                if energy is None:
                    calc = getattr(atoms, "calc", None)
                    if calc is not None:
                        energy = calc.results.get("energy") or calc.results.get("free_energy")
                    if energy is None:
                        energy = atoms.info.get("energy_ev")
                    if energy is None:
                        energy = atoms.info.get("energy")
                    if energy is None:
                        with suppress(Exception):
                            energy = atoms.get_potential_energy()
                if energy is not None:
                    with suppress(Exception):
                        comment_parts.append(f"energy_ev={float(energy):.8f}")

                if "time_fs" in atoms.info:
                    with suppress(Exception):
                        comment_parts.append(f"time_fs={float(atoms.info['time_fs']):.4f}")

                existing = atoms.info.get("comment") or atoms.info.get("uma_comment")
                if existing:
                    comment_parts.append(str(existing).strip())

                comment_line = " ".join(part for part in comment_parts if part).strip()
                handle.write(f"{len(symbols)}\n")
                handle.write(f"{comment_line}\n")
                for symbol, (x_coord, y_coord, z_coord) in zip(symbols, positions):
                    handle.write(f"{symbol:2s} {x_coord: .10f} {y_coord: .10f} {z_coord: .10f}\n")
        return destination
    except Exception as exc:
        app.logger.warning("Unable to export %s to XYZ: %s", source, exc)
        return None


def _extract_xyz_frames(path: Path, start_index: int, limit: int) -> tuple[list[str], int]:
    """Read multi-frame XYZ data and return frame strings plus total count."""

    frames: list[str] = []
    total = 0

    if not path or not path.exists():
        return frames, total

    start_index = max(0, start_index)
    limit = max(1, limit)

    with path.open("r", encoding="utf-8", errors="ignore") as handle:
        while True:
            header_line = handle.readline()
            if not header_line:
                break
            stripped = header_line.strip()
            if not stripped:
                continue
            try:
                atom_count = int(stripped)
            except ValueError:
                continue
            comment_line = handle.readline()
            if comment_line == "":
                break
            atom_lines: list[str] = []
            incomplete = False
            for _ in range(atom_count):
                atom_line = handle.readline()
                if atom_line == "":
                    incomplete = True
                    break
                atom_lines.append(atom_line.rstrip("\n"))
            if incomplete:
                break
            if total >= start_index and len(frames) < limit:
                frame_text = "\n".join(
                    [
                        str(atom_count),
                        comment_line.rstrip("\n"),
                        *atom_lines,
                    ]
                )
                frames.append(frame_text)
            total += 1
    return frames, total


def _write_text_pdf(text: str, pdf_path: Path) -> Path | None:
    try:
        lines = text.splitlines() or [""]
        lines_per_page = 55
        with PdfPages(pdf_path) as pdf:
            for start in range(0, len(lines), lines_per_page):
                chunk = lines[start : start + lines_per_page]
                fig = plt.figure(figsize=(8.27, 11.69))
                fig.patch.set_facecolor("white")
                plt.axis("off")
                fig.text(
                    0.03,
                    0.97,
                    "\n".join(chunk),
                    family="monospace",
                    fontsize=8,
                    va="top",
                    ha="left",
                )
                pdf.savefig(fig, bbox_inches="tight")
                plt.close(fig)
        return pdf_path
    except Exception:
        if pdf_path.exists():
            pdf_path.unlink(missing_ok=True)  # type: ignore[arg-type]
        return None


def _write_text_latex(text: str, tex_path: Path, title: str) -> Path | None:
    try:
        latex = "\n".join(
            [
                r"\documentclass{article}",
                r"\usepackage[margin=1in]{geometry}",
                r"\usepackage{fancyvrb}",
                r"\begin{document}",
                rf"\section*{{{title}}}",
                r"\begin{Verbatim}[fontsize=\small]",
                text,
                r"\end{Verbatim}",
                r"\end{document}",
                "",
            ]
        )
        tex_path.write_text(latex, encoding="utf-8")
        return tex_path
    except OSError:
        return None


def _write_text_docx(text: str, docx_path: Path) -> Path | None:
    if DRIVER_DOCX_AVAILABLE:
        try:
            document = Document()
            for line in text.splitlines():
                document.add_paragraph(line)
            document.save(docx_path)
            return docx_path
        except Exception:
            pass

    lines = text.splitlines() or [""]
    fallback = _write_basic_report_docx(lines, docx_path)
    if fallback:
        return fallback
    if docx_path.exists():
        docx_path.unlink(missing_ok=True)  # type: ignore[arg-type]
    return None


def _run_driver_analysis(xyz_root: Path, output_dir: Path) -> Dict[str, Path | str | int]:
    xyz_files = [
        path
        for path in xyz_root.rglob("*")
        if path.is_file() and path.suffix.lower() == ".xyz"
    ]
    if not xyz_files:
        raise ValueError("Upload at least one XYZ file in the selected folder.")

    def _is_opt_variant(path: Path) -> bool:
        stem = path.stem.lower()
        return "opt" in stem or "sp-opt" in stem

    def _matches_base(base: Path, candidate: Path) -> bool:
        base_key = base.stem.lower()
        cand_key = candidate.stem.lower()
        if cand_key == base_key:
            return False
        prefix = f"{base_key}-"
        if not cand_key.startswith(prefix):
            return False
        suffix = cand_key[len(prefix) :]
        return "opt" in suffix or "sp-opt" in suffix

    by_parent: Dict[Path, Dict[str, Path]] = {}
    for path in xyz_files:
        by_parent.setdefault(path.parent, {})[path.name.lower()] = path

    file_pairs: List[tuple[Path, Path]] = []
    for folder_files in by_parent.values():
        bases = {name: path for name, path in folder_files.items() if not _is_opt_variant(path)}
        variants = {name: path for name, path in folder_files.items() if _is_opt_variant(path)}
        for base_name, base_path in bases.items():
            prefix = f"{base_name}"
            matches = [
                variants[name]
                for name in variants
                if name.startswith(f"{base_name[:-4]}-") and _matches_base(base_path, variants[name])
            ]
            for match in matches:
                file_pairs.append((base_path, match))

    if not file_pairs:
        raise ValueError("No XYZ/-geoopt-OPT pairs found. Ensure optimized counterparts are present.")

    scripts_root = resources.files("uma_ase").joinpath("scripts-to-share_v2")
    with resources.as_file(scripts_root) as resolved_root:
        root_path = Path(resolved_root)
        rmsd_script = root_path / "rmsd.py"
        hetero_script = root_path / "rmsd_dist-angles_ranking_hetero-cutoff.py"
        if not rmsd_script.exists() or not hetero_script.exists():
            raise RuntimeError("Driver scripts are unavailable in this installation.")

        def _run_tool(tool_path: Path, file_a: Path, file_b: Path) -> str:
            result = subprocess.run(
                [sys.executable, str(tool_path), str(file_a), str(file_b)],
                capture_output=True,
                text=True,
                cwd=str(root_path),
            )
            if result.returncode != 0:
                stderr = (result.stderr or "").strip()
                stdout = (result.stdout or "").strip()
                details = stderr or stdout or f"Exited with status {result.returncode}"
                return f"Error running {tool_path.name}: {details}\n"
            return result.stdout

        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / "compiled_rmsd_results.txt"
        with output_path.open("w", encoding="utf-8", buffering=1024 * 1024) as handle:
            handle.write("=== RMSD Analysis Results ===\n\n")
            for index, (file_a, file_b) in enumerate(file_pairs, start=1):
                handle.write(f"[{index}] File pair: {file_a.name}  vs  {file_b.name}\n")
                handle.write("-" * 60 + "\n")
                handle.write("--- rmsd.py output ---\n")
                handle.write(_run_tool(rmsd_script, file_a, file_b))
                handle.write("\n--- rmsd_dist-angles_ranking_hetero-cutoff.py output ---\n")
                handle.write(_run_tool(hetero_script, file_a, file_b))
                handle.write("\n" + "=" * 80 + "\n\n")
            handle.flush()

    preview_text = output_path.read_text(encoding="utf-8", errors="replace")
    preview_limit = 200_000
    trimmed_preview = (
        preview_text if len(preview_text) <= preview_limit else f"{preview_text[:preview_limit]}\n...\n"
    )
    pdf_path = _write_text_pdf(preview_text, output_dir / "compiled_rmsd_results.pdf")
    tex_path = _write_text_latex(preview_text, output_dir / "compiled_rmsd_results.tex", "Compiled RMSD Results")
    docx_path = _write_text_docx(preview_text, output_dir / "compiled_rmsd_results.docx")

    return {
        "text_path": output_path,
        "pdf_path": pdf_path,
        "latex_path": tex_path,
        "docx_path": docx_path,
        "pairs": len(file_pairs),
        "preview": trimmed_preview,
    }


@app.route("/")
def index() -> Response:
    """Serve the single-page frontend bundled with the package."""
    html_path = resources.files("uma_ase").joinpath("static", STATIC_HTML)
    return Response(html_path.read_bytes(), mimetype="text/html")


@app.route("/assets/<path:asset>")
def serve_static_asset(asset: str):
    """Serve packaged static assets (e.g. logo.svg) referenced from the frontend."""
    candidate = resources.files("uma_ase").joinpath("static", asset)
    if not candidate.is_file():
        abort(404)
    with resources.as_file(candidate) as fs_path:
        return send_file(fs_path)


@app.route("/screenshot<int:index>.png")
def serve_readme_screenshot(index: int):
    """Expose README screenshot assets referenced by relative paths."""
    if index < 1:
        abort(404)
    filename = f"screenshot{index}.png"
    candidate = resources.files("uma_ase").joinpath("static", "screenshots", filename)
    if not candidate.is_file():
        abort(404)
    with resources.as_file(candidate) as fs_path:
        return send_file(fs_path)


@app.route("/assets/")
def serve_static_root():
    """Provide a no-op response for tools that probe the asset root (e.g. JSmol)."""
    return Response(status=204)


@app.route("/api/uma-ase/readme", methods=["GET"])
def fetch_readme():
    try:
        content = _read_readme_text()
    except FileNotFoundError as exc:
        return jsonify({"status": "error", "message": str(exc)}), 404
    return jsonify({"status": "ok", "content": content})


@app.route("/api/uma-ase/analyze", methods=["POST"])
def analyze_logs():
    uploads = request.files.getlist("files")
    if not uploads:
        return jsonify({"status": "error", "message": "Upload at least one log file or folder."}), 400

    with tempfile.TemporaryDirectory() as tmpdir:
        logs_root = Path(tmpdir) / "logs"
        logs_root.mkdir(parents=True, exist_ok=True)
        saved = 0
        for storage in uploads:
            if not storage or not storage.filename:
                continue
            try:
                _safe_save_upload(storage, logs_root)
                saved += 1
            except ValueError:
                continue

        if not saved:
            return jsonify({"status": "error", "message": "No valid files uploaded."}), 400

        token = secure_filename(uuid.uuid4().hex)
        output_dir = ANALYZE_REPORT_ROOT / token
        output_dir.mkdir(parents=True, exist_ok=True)
        try:
            outputs = generate_report(logs_root, output_dir)
        except ValueError as exc:
            shutil.rmtree(output_dir, ignore_errors=True)
            return jsonify({"status": "error", "message": str(exc)}), 400
        pdf_path = outputs.get("pdf")
        if not pdf_path or not pdf_path.exists():
            shutil.rmtree(output_dir, ignore_errors=True)
            return jsonify({"status": "error", "message": "Report generation failed."}), 500
        payload = {
            "status": "ok",
            "token": token,
            "text_url": _build_analyze_url(token, outputs.get("text")),
            "pdf_url": _build_analyze_url(token, pdf_path),
            "latex_url": _build_analyze_url(token, outputs.get("latex")),
            "docx_url": _build_analyze_url(token, outputs.get("docx")),
        }
        return jsonify(payload)


@app.route("/api/uma-ase/analyze/driver", methods=["POST"])
def analyze_xyz_pairs():
    uploads = request.files.getlist("files")
    if not uploads:
        return jsonify({"status": "error", "message": "Upload at least one XYZ file or folder."}), 400

    with tempfile.TemporaryDirectory() as tmpdir:
        xyz_root = Path(tmpdir) / "xyz"
        xyz_root.mkdir(parents=True, exist_ok=True)
        saved = 0
        for storage in uploads:
            if not storage or not storage.filename:
                continue
            try:
                _safe_save_upload(storage, xyz_root)
                saved += 1
            except ValueError:
                continue

        if not saved:
            return jsonify({"status": "error", "message": "No valid files uploaded."}), 400

        token = secure_filename(f"drv-{uuid.uuid4().hex}")
        output_dir = ANALYZE_REPORT_ROOT / token
        output_dir.mkdir(parents=True, exist_ok=True)
        try:
            result = _run_driver_analysis(xyz_root, output_dir)
        except ValueError as exc:
            shutil.rmtree(output_dir, ignore_errors=True)
            return jsonify({"status": "error", "message": str(exc)}), 400
        except RuntimeError as exc:
            shutil.rmtree(output_dir, ignore_errors=True)
            return jsonify({"status": "error", "message": str(exc)}), 500

    text_path = result.get("text_path")
    payload = {
        "status": "ok",
        "token": token,
        "pairs": result.get("pairs", 0),
        "preview": result.get("preview"),
        "results_url": _build_analyze_url(token, text_path),
        "pdf_url": _build_analyze_url(token, result.get("pdf_path")),
        "latex_url": _build_analyze_url(token, result.get("latex_path")),
        "docx_url": _build_analyze_url(token, result.get("docx_path")),
        "message": f"Processed {result.get('pairs', 0)} file pairs." if result.get("pairs") else "Analysis complete.",
    }
    return jsonify(payload)


@app.route("/api/uma-ase/analyze/simple-geometry", methods=["POST"])
def analyze_simple_geometry():
    uploads = request.files.getlist("files")
    if not uploads:
        return jsonify({"status": "error", "message": "Upload at least one geometry file or folder."}), 400

    with tempfile.TemporaryDirectory() as tmpdir:
        geom_root = Path(tmpdir) / "geometry"
        geom_root.mkdir(parents=True, exist_ok=True)
        saved_files: List[Tuple[Path, str]] = []
        for storage in uploads:
            if not storage or not storage.filename:
                continue
            try:
                destination = _safe_save_upload(storage, geom_root)
            except ValueError:
                continue
            label = _display_label_for_upload(storage.filename, destination)
            saved_files.append((destination, label))

        if not saved_files:
            return jsonify({"status": "error", "message": "No valid geometry files uploaded."}), 400

        candidates, skipped = _expand_geometry_inputs(saved_files)
        if not candidates:
            return jsonify({
                "status": "error",
                "message": "No geometry files found inside the uploaded selection.",
                "skipped": skipped,
            }), 400

        pair_map: Dict[str, List[float]] = {}
        structures: List[Dict[str, Any]] = []
        processed = 0

        for path, label in candidates:
            if not path.is_file():
                continue
            atoms = _load_first_structure(path)
            if atoms is None:
                skipped.append({"label": label, "reason": "Unsupported geometry format."})
                continue
            atom_count = len(atoms)
            if atom_count == 0:
                skipped.append({"label": label, "reason": "Structure does not contain atoms."})
                continue
            try:
                mic = bool(atoms.pbc.any()) if hasattr(atoms, "pbc") else False
            except Exception:
                mic = False
            try:
                distances = atoms.get_all_distances(mic=mic)
            except Exception as exc:
                skipped.append({"label": label, "reason": f"Unable to compute distances: {exc}"})
                continue
            symbols = atoms.get_chemical_symbols()
            matrix_list = []
            for row in distances.tolist():
                matrix_row = []
                for value in row:
                    try:
                        numeric_value = float(value)
                    except (TypeError, ValueError):
                        matrix_row.append(None)
                        continue
                    if math.isfinite(numeric_value):
                        matrix_row.append(round(numeric_value, 6))
                    else:
                        matrix_row.append(None)
                matrix_list.append(matrix_row)

            for i in range(atom_count):
                for j in range(i + 1, atom_count):
                    try:
                        numeric = float(distances[i][j])
                    except (TypeError, ValueError):
                        continue
                    if not math.isfinite(numeric):
                        continue
                    pair_label = _pair_label(symbols[i], symbols[j])
                    pair_map.setdefault(pair_label, []).append(numeric)

            structure_entry = {
                "id": len(structures),
                "label": label,
                "formula": atoms.get_chemical_formula(),
                "atom_count": atom_count,
                "symbols": symbols,
                "distance_matrix": matrix_list,
            }
            structures.append(structure_entry)
            processed += 1

    if not structures:
        return jsonify({
            "status": "error",
            "message": "No valid geometries were detected.",
            "skipped": skipped,
        }), 400

    pair_series = []
    total_pairs = 0
    for pair_label in sorted(pair_map):
        distances = pair_map[pair_label]
        if not distances:
            continue
        distances.sort()
        total_pairs += len(distances)
        mean_value = sum(distances) / len(distances)
        pair_series.append({
            "label": pair_label,
            "count": len(distances),
            "min": round(distances[0], 6),
            "max": round(distances[-1], 6),
            "mean": round(mean_value, 6),
            "distances": [round(value, 6) for value in distances],
        })

    token = secure_filename(f"geo-{uuid.uuid4().hex}")
    output_dir = ANALYZE_REPORT_ROOT / token
    output_dir.mkdir(parents=True, exist_ok=True)
    summary_text = _build_simple_geometry_summary(structures, pair_series, total_pairs, skipped)
    text_path: Optional[Path] = output_dir / "simple_geometry_results.txt"
    try:
        text_path.write_text(summary_text, encoding="utf-8")
    except OSError:
        text_path = None
    pdf_path = _write_text_pdf(summary_text, output_dir / "simple_geometry_results.pdf")
    latex_path = _write_text_latex(summary_text, output_dir / "simple_geometry_results.tex", "Simple Geometry Analysis")
    docx_path = _write_text_docx(summary_text, output_dir / "simple_geometry_results.docx")

    payload = {
        "status": "ok",
        "token": token,
        "structures": structures,
        "pair_series": pair_series,
        "total_pairs": total_pairs,
        "processed": processed,
        "skipped": skipped,
        "text_url": _build_analyze_url(token, text_path) if text_path else None,
        "pdf_url": _build_analyze_url(token, pdf_path),
        "latex_url": _build_analyze_url(token, latex_path),
        "docx_url": _build_analyze_url(token, docx_path),
    }
    return jsonify(payload)


@app.route("/api/uma-ase/analyze/<token>/<path:filename>")
def download_analyze_file(token: str, filename: str):
    safe_token = secure_filename(token)
    base_dir = (ANALYZE_REPORT_ROOT / safe_token).resolve()
    if not base_dir.exists():
        abort(404)
    target = (base_dir / filename).resolve()
    try:
        target.relative_to(base_dir)
    except ValueError:
        abort(404)
    if not target.is_file():
        abort(404)
    return send_file(target)


@app.route("/api/uma-ase/run", methods=["POST"])
def run_job():
    geometry = request.files.get("geometry")
    if geometry is None or geometry.filename == "":
        return jsonify({"status": "error", "message": "Geometry file is required."}), 400

    try:
        charge_val = int(request.form.get("charge", "0"))
    except (TypeError, ValueError):
        return jsonify({"status": "error", "message": "Charge must be an integer."}), 400

    try:
        spin_val = int(request.form.get("spin", "1"))
    except (TypeError, ValueError):
        return jsonify({"status": "error", "message": "Spin multiplicity must be an integer."}), 400

    try:
        grad_val = float(request.form.get("grad", "0.01"))
    except (TypeError, ValueError):
        return jsonify({"status": "error", "message": "Grad must be a number."}), 400
    if grad_val <= 0:
        return jsonify({"status": "error", "message": "Grad must be positive."}), 400

    try:
        iter_val = int(request.form.get("iter", "250"))
    except (TypeError, ValueError):
        return jsonify({"status": "error", "message": "Max iterations must be an integer."}), 400
    if iter_val <= 0:
        return jsonify({"status": "error", "message": "Max iterations must be positive."}), 400

    optimizer = request.form.get("optimizer", "LBFGS")
    temperature = request.form.get("temperature", "298.15")
    pressure = request.form.get("pressure", "101325.0")
    run_types_raw = request.form.get("run_type", "sp").split()
    run_types = [item.lower() for item in run_types_raw] or ["sp"]
    mlff_checkpoint_raw = request.form.get("mlff_checkpoint", "uma-s-1p1")
    mlff_checkpoint = mlff_checkpoint_raw.strip() or "uma-s-1p1"
    mlff_task_raw = request.form.get("mlff_task", "omol")
    mlff_task = mlff_task_raw.strip() or "omol"
    ts_displacement_raw = (request.form.get("ts_displacement") or "").strip()
    if ts_displacement_raw:
        try:
            ts_displacement_val = float(ts_displacement_raw)
        except (TypeError, ValueError):
            return jsonify({"status": "error", "message": "TS displacement must be a number."}), 400
        if ts_displacement_val < 0:
            return jsonify({"status": "error", "message": "TS displacement must be non-negative."}), 400
    else:
        ts_displacement_val = 0.1

    ts_dimer_sep_raw = (request.form.get("ts_dimer_separation") or "").strip()
    if ts_dimer_sep_raw:
        try:
            ts_dimer_sep_val = float(ts_dimer_sep_raw)
        except (TypeError, ValueError):
            return jsonify({"status": "error", "message": "Dimer separation must be a number."}), 400
        if ts_dimer_sep_val <= 0:
            return jsonify({"status": "error", "message": "Dimer separation must be positive."}), 400
    else:
        ts_dimer_sep_val = 0.01

    ts_trial_step_raw = (request.form.get("ts_trial_step") or "").strip()
    if ts_trial_step_raw:
        try:
            ts_trial_step_val = float(ts_trial_step_raw)
        except (TypeError, ValueError):
            return jsonify({"status": "error", "message": "Trial translation must be a number."}), 400
        if ts_trial_step_val <= 0:
            return jsonify({"status": "error", "message": "Trial translation must be positive."}), 400
    else:
        ts_trial_step_val = 0.05

    ts_max_step_raw = (request.form.get("ts_max_step") or "").strip()
    if ts_max_step_raw:
        try:
            ts_max_step_val = float(ts_max_step_raw)
        except (TypeError, ValueError):
            return jsonify({"status": "error", "message": "Max translation must be a number."}), 400
        if ts_max_step_val <= 0:
            return jsonify({"status": "error", "message": "Max translation must be positive."}), 400
    else:
        ts_max_step_val = 0.2

    ts_max_rot_raw = (request.form.get("ts_max_rot") or "").strip()
    if ts_max_rot_raw:
        try:
            ts_max_rot_val = int(ts_max_rot_raw)
        except (TypeError, ValueError):
            return jsonify({"status": "error", "message": "Max rotations must be an integer."}), 400
        if ts_max_rot_val <= 0:
            return jsonify({"status": "error", "message": "Max rotations must be positive."}), 400
    else:
        ts_max_rot_val = 5

    ts_displacement = str(ts_displacement_val)
    ts_dimer_separation = str(ts_dimer_sep_val)
    ts_trial_step = str(ts_trial_step_val)
    ts_max_step = str(ts_max_step_val)
    ts_max_rot = str(ts_max_rot_val)

    results_root = Path(app.config["UMA_RESULTS_DIR"])
    results_root.mkdir(parents=True, exist_ok=True)

    job_id = f"{datetime.now().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:6]}"
    filename = secure_filename(geometry.filename) or "input.xyz"
    relative_field = request.form.get("relative_path") or request.form.get("source_path")
    sanitized_relative = _sanitize_relative_path(relative_field)
    folder_root_raw = request.form.get("multi_root")
    folder_root = secure_filename(folder_root_raw) if folder_root_raw else None
    multi_root_dir = results_root / "multi_runs"
    job_dir: Path
    if sanitized_relative:
        multi_root_dir.mkdir(parents=True, exist_ok=True)
        rel_parent = sanitized_relative.parent if sanitized_relative.parent != Path(".") else Path()
        base_name = sanitized_relative.stem or Path(filename).stem or "geometry"
        if folder_root:
            rel_parent = Path(folder_root) / rel_parent
        base_dir = multi_root_dir.joinpath(rel_parent, base_name)
        job_dir = base_dir
        attempt = 1
        while job_dir.exists():
            job_dir = base_dir.parent / f"{base_name}_{attempt}"
            attempt += 1
        job_dir.mkdir(parents=True, exist_ok=True)
    else:
        if folder_root:
            multi_root_dir.mkdir(parents=True, exist_ok=True)
            base_name = Path(filename).stem or "geometry"
            base_dir = multi_root_dir / folder_root / base_name
            job_dir = base_dir
            attempt = 1
            while job_dir.exists():
                job_dir = base_dir.parent / f"{base_name}_{attempt}"
                attempt += 1
            job_dir.mkdir(parents=True, exist_ok=True)
        else:
            job_dir = results_root / job_id
            job_dir.mkdir(parents=True, exist_ok=True)

    input_path = job_dir / filename
    geometry.save(input_path)

    record = JobRecord(
        job_id=job_id,
        job_dir=job_dir,
        charge=charge_val,
        spin=spin_val,
        grad=grad_val,
        iterations=iter_val,
        run_types=run_types,
        relative_path=sanitized_relative,
    )
    record.cancel_event = threading.Event()
    record.job_kind = "workflow"

    with JOB_LOCK:
        JOBS[job_id] = record

    worker = threading.Thread(
        target=_execute_job,
        args=(
            record,
            filename,
            optimizer,
            temperature,
            pressure,
            mlff_checkpoint,
            mlff_task,
            sanitized_relative,
            ts_displacement,
            ts_dimer_separation,
            ts_trial_step,
            ts_max_step,
            ts_max_rot,
        ),
        daemon=True,
    )
    record.worker = worker
    worker.start()

    return jsonify({"job_id": job_id})



@app.route("/api/uma-ase/md/run", methods=["POST"])
def run_md_job():
    geometry = request.files.get("geometry")
    if geometry is None or geometry.filename == "":
        return jsonify({"status": "error", "message": "Geometry file is required."}), 400

    form = request.form
    engine = (form.get("md_engine") or "langevin").lower()

    try:
        charge_val = _parse_int_field(form, "charge", 0, label="Charge")
        spin_val = _parse_int_field(form, "spin", 1, label="Spin multiplicity", min_value=0, min_inclusive=False)
        steps_val = _parse_int_field(form, "md_steps", 500, label="MD steps", min_value=0, min_inclusive=False)
        timestep_fs = _parse_float_field(form, "md_timestep_fs", 0.5, label="Timestep", min_value=0.0, min_inclusive=False)
        temperature_val = _parse_float_field(form, "md_temperature", 300.0, label="Temperature", min_value=0.0, min_inclusive=False)
        friction_val = _parse_float_field(form, "md_friction", 0.002, label="Friction", min_value=0.0)
        traj_interval = _parse_int_field(form, "md_traj_interval", 10, label="Trajectory interval", min_value=0, min_inclusive=False)
        log_interval = _parse_int_field(form, "md_log_interval", 10, label="Log interval", min_value=0, min_inclusive=False)
        relax_fs = _parse_float_field(form, "md_relax_fs", 100.0, label="Thermostat relaxation time", min_value=0.0, min_inclusive=False)
        pressure_bar = _parse_float_field(form, "md_pressure_bar", 1.0, label="Pressure", min_value=0.0)
        compressibility_bar = _parse_float_field(form, "md_compressibility_bar", 4.57e-5, label="Compressibility", min_value=0.0)
        barostat_relax_fs = _parse_float_field(form, "md_barostat_relax_fs", 1000.0, label="Barostat relaxation time", min_value=0.0, min_inclusive=False)
        nose_tdamp_fs = _parse_float_field(form, "md_nose_tdamp_fs", relax_fs, label="Nosé-Hoover damping", min_value=0.0, min_inclusive=False)
        nose_tchain = _parse_int_field(form, "md_nose_tchain", 3, label="Nosé-Hoover chain length", min_value=0, min_inclusive=False)
        nose_tloop = _parse_int_field(form, "md_nose_tloop", 1, label="Nosé-Hoover sub-steps", min_value=0, min_inclusive=False)
        bussi_taut_fs = _parse_float_field(form, "md_bussi_taut_fs", relax_fs, label="Bussi time constant", min_value=0.0, min_inclusive=False)
        andersen_prob = _parse_float_field(form, "md_andersen_prob", 0.001, label="Andersen collision probability", min_value=0.0)
        if andersen_prob is None or not 0 <= andersen_prob <= 1:
            raise ValueError("Andersen collision probability must be between 0 and 1.")
        mtk_tdamp_fs = _parse_float_field(form, "md_mtk_tdamp_fs", 100.0, label="MTK thermostat damping", min_value=0.0, min_inclusive=False)
        mtk_pdamp_fs = _parse_float_field(form, "md_mtk_pdamp_fs", 1000.0, label="MTK barostat damping", min_value=0.0, min_inclusive=False)
        mtk_tchain = _parse_int_field(form, "md_mtk_tchain", 3, label="MTK thermostat chain length", min_value=0, min_inclusive=False)
        mtk_pchain = _parse_int_field(form, "md_mtk_pchain", 3, label="MTK barostat chain length", min_value=0, min_inclusive=False)
        mtk_tloop = _parse_int_field(form, "md_mtk_tloop", 1, label="MTK thermostat sub-steps", min_value=0, min_inclusive=False)
        mtk_ploop = _parse_int_field(form, "md_mtk_ploop", 1, label="MTK barostat sub-steps", min_value=0, min_inclusive=False)
        baoab_ttau_fs = _parse_float_field(form, "md_baoab_ttau_fs", 50.0, label="BAOAB thermostat time", min_value=0.0, min_inclusive=False)
        baoab_ptau_fs = _parse_float_field(form, "md_baoab_ptau_fs", 1000.0, label="BAOAB barostat time", min_value=0.0, min_inclusive=False)
        baoab_pmass = _parse_float_field(form, "md_baoab_pmass", None, label="BAOAB cell mass", min_value=0.0, min_inclusive=False)
        baoab_pmass_factor = _parse_float_field(form, "md_baoab_pmass_factor", 1.0, label="BAOAB mass factor", min_value=0.0, min_inclusive=False)
        melchionna_ttime_fs = _parse_float_field(form, "md_melchionna_ttime_fs", 25.0, label="Melchionna thermostat time", min_value=0.0)
        melchionna_ptime_fs = _parse_float_field(form, "md_melchionna_ptime_fs", 75.0, label="Melchionna barostat time", min_value=0.0)
        melchionna_bulk_gpa = _parse_float_field(form, "md_melchionna_bulk_gpa", 100.0, label="Melchionna bulk modulus", min_value=0.0)
    except ValueError as exc:
        return jsonify({"status": "error", "message": str(exc)}), 400

    melchionna_mask_raw = (form.get("md_melchionna_mask") or "").strip()
    melchionna_mask: Optional[List[int]] = None
    if melchionna_mask_raw:
        try:
            mask_values = []
            for entry in melchionna_mask_raw.split(","):
                entry_clean = entry.strip()
                if entry_clean == "":
                    continue
                value = 1 if int(round(float(entry_clean))) > 0 else 0
                mask_values.append(value)
            if mask_values:
                mask_values = (mask_values + [1, 1, 1])[:3]
                melchionna_mask = mask_values
        except (TypeError, ValueError):
            return jsonify({"status": "error", "message": "Melchionna mask must be comma separated integers."}), 400

    baoab_hydrostatic = _parse_bool_field(form, "md_baoab_hydrostatic", False)
    use_pbc = _parse_bool_field(form, "md_use_pbc", False)
    cell_parameters: Optional[List[float]] = None
    if use_pbc:
        try:
            cell_a = _parse_float_field(form, "md_cell_a", None, label="Cell a", min_value=0.0, min_inclusive=False, required=True)
            cell_b = _parse_float_field(form, "md_cell_b", None, label="Cell b", min_value=0.0, min_inclusive=False, required=True)
            cell_c = _parse_float_field(form, "md_cell_c", None, label="Cell c", min_value=0.0, min_inclusive=False, required=True)
            cell_alpha = _parse_float_field(
                form,
                "md_cell_alpha",
                None,
                label="Cell alpha",
                min_value=0.0,
                min_inclusive=False,
                max_value=180.0,
                max_inclusive=False,
                required=True,
            )
            cell_beta = _parse_float_field(
                form,
                "md_cell_beta",
                None,
                label="Cell beta",
                min_value=0.0,
                min_inclusive=False,
                max_value=180.0,
                max_inclusive=False,
                required=True,
            )
            cell_gamma = _parse_float_field(
                form,
                "md_cell_gamma",
                None,
                label="Cell gamma",
                min_value=0.0,
                min_inclusive=False,
                max_value=180.0,
                max_inclusive=False,
                required=True,
            )
            cell_parameters = [cell_a, cell_b, cell_c, cell_alpha, cell_beta, cell_gamma]  # type: ignore[list-item]
        except ValueError as exc:
            return jsonify({"status": "error", "message": str(exc)}), 400

    mlff_checkpoint_raw = request.form.get("mlff_checkpoint", "uma-s-1p1")
    mlff_checkpoint = mlff_checkpoint_raw.strip() or "uma-s-1p1"
    mlff_task_raw = request.form.get("mlff_task", "omol")
    mlff_task = mlff_task_raw.strip() or "omol"

    results_root = Path(app.config["UMA_RESULTS_DIR"])
    results_root.mkdir(parents=True, exist_ok=True)

    job_id = f"{datetime.now().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:6]}"
    filename = secure_filename(geometry.filename) or "input.xyz"
    job_dir = results_root / job_id
    job_dir.mkdir(parents=True, exist_ok=True)

    input_path = job_dir / filename
    geometry.save(input_path)

    log_path = job_dir / f"{Path(filename).stem}-MD.log"
    traj_path = job_dir / f"{Path(filename).stem}-MD.traj"
    snapshot_path = job_dir / f"{Path(filename).stem}-MD-final.xyz"
    multi_xyz_path = job_dir / f"{Path(filename).stem}-MD.xyz"

    md_options = {
        "engine": engine,
        "steps": steps_val,
        "timestep_fs": timestep_fs,
        "temperature": temperature_val,
        "friction": friction_val,
        "traj_interval": traj_interval,
        "log_interval": log_interval,
        "relax_fs": relax_fs,
        "pressure_bar": pressure_bar,
        "compressibility_bar": compressibility_bar,
        "barostat_relax_fs": barostat_relax_fs,
        "nose_tdamp_fs": nose_tdamp_fs,
        "nose_tchain": nose_tchain,
        "nose_tloop": nose_tloop,
        "bussi_taut_fs": bussi_taut_fs,
        "andersen_prob": andersen_prob,
        "mtk_tdamp_fs": mtk_tdamp_fs,
        "mtk_pdamp_fs": mtk_pdamp_fs,
        "mtk_tchain": mtk_tchain,
        "mtk_pchain": mtk_pchain,
        "mtk_tloop": mtk_tloop,
        "mtk_ploop": mtk_ploop,
        "baoab_ttau_fs": baoab_ttau_fs,
        "baoab_ptau_fs": baoab_ptau_fs,
        "baoab_pmass": baoab_pmass,
        "baoab_pmass_factor": baoab_pmass_factor,
        "baoab_hydrostatic": baoab_hydrostatic,
        "melchionna_ttime_fs": melchionna_ttime_fs,
        "melchionna_ptime_fs": melchionna_ptime_fs,
        "melchionna_bulk_gpa": melchionna_bulk_gpa,
        "melchionna_mask": melchionna_mask,
        "use_pbc": use_pbc,
        "cell_parameters": cell_parameters,
        "mlff_checkpoint": mlff_checkpoint,
        "mlff_task": mlff_task,
        "multi_xyz": multi_xyz_path,
    }

    record = JobRecord(
        job_id=job_id,
        job_dir=job_dir,
        charge=charge_val,
        spin=spin_val,
        grad=0.0,
        iterations=steps_val,
        run_types=["md"],
        status="running",
        log_path=log_path,
        traj_path=traj_path,
        opt_path=snapshot_path,
        md_options=md_options,
        md_multi_xyz=multi_xyz_path,
    )
    record.cancel_event = threading.Event()
    record.job_kind = "md"

    with JOB_LOCK:
        JOBS[job_id] = record

    worker = threading.Thread(
        target=_execute_md_job,
        args=(record, filename, md_options),
        daemon=True,
    )
    record.worker = worker
    worker.start()

    return jsonify({"job_id": job_id})


def _execute_job(
    record: JobRecord,
    filename: str,
    optimizer: str,
    temperature: str,
    pressure: str,
    mlff_checkpoint: Optional[str],
    mlff_task: Optional[str],
    relative_path: Optional[Path],
    ts_displacement: Optional[str],
    ts_dimer_separation: Optional[str],
    ts_trial_step: Optional[str],
    ts_max_step: Optional[str],
    ts_max_rot: Optional[str],
):
    job_dir = record.job_dir
    cancel_event = record.cancel_event
    if cancel_event is None:
        cancel_event = threading.Event()
        record.cancel_event = cancel_event
    if relative_path:
        record.relative_path = relative_path
    if cancel_event.is_set():
        with JOB_LOCK:
            record.status = "cancelled"
            record.message = "Job cancelled by user."
        return

    input_path = job_dir / filename
    run_sequence = record.run_types or ["sp"]

    try:
        paths = build_output_paths(input_path, run_sequence)
        record.log_path = paths.log
        record.traj_path = paths.trajectory
        record.opt_path = paths.final_geometry
        record.freq_archive_path = paths.freq_archive
        record.freq_folder = record.job_dir / "freqs" / Path(filename).stem
        record.freq_archive_path = paths.freq_archive

        argv = _build_cli_args(
            input_path,
            record.run_types,
            str(record.charge),
            str(record.spin),
            optimizer,
            str(record.grad),
            str(record.iterations),
            temperature,
            pressure,
            mlff_checkpoint,
            mlff_task,
            ts_displacement,
            ts_dimer_separation,
            ts_trial_step,
            ts_max_step,
            ts_max_rot,
        )

        cmd = [sys.executable, "-m", "uma_ase.cli", *argv]
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            cwd=str(job_dir),
        )
        with JOB_LOCK:
            record.process = process

        stdout_data, _ = process.communicate()
        exit_code = process.returncode
        with JOB_LOCK:
            record.process = None

        cancelled = cancel_event.is_set()
        error_message: Optional[str] = None
        if cancelled:
            error_message = "Job cancelled by user."
        elif exit_code != 0:
            tail = (stdout_data or "").strip().splitlines()
            detail = tail[-1] if tail else ""
            error_message = f"uma-ase exited with status {exit_code}."
            if detail:
                error_message = f"{error_message} {detail}"
        else:
            if record.opt_path and record.opt_path.exists():
                try:
                    atoms_opt = read(str(record.opt_path))
                    formula_opt = atoms_opt.get_chemical_formula()
                    comment = " ".join(
                        part
                        for part in [
                            formula_opt,
                            f"charge={record.charge}",
                            f"spin={record.spin}",
                        ]
                        if part
                    )
                    write(str(record.opt_path), atoms_opt, format="xyz", comment=comment)
                except Exception as exc:
                    error_message = f"Optimized geometry rewrite failed: {exc}"

        visual_traj = None
        if record.traj_path and record.traj_path.exists():
            visual_traj = _export_traj_for_visualization(record.traj_path, log_path=record.log_path)

        with JOB_LOCK:
            if cancelled:
                record.status = "cancelled"
                record.message = "Job cancelled by user."
            elif error_message:
                record.status = "error"
                record.message = error_message
            else:
                record.status = "completed"

            if record.log_path and record.log_path.exists():
                record.log_url = f"/api/uma-ase/job/{record.job_id}/log"
            if visual_traj is not None and visual_traj.exists():
                record.traj_visual_path = visual_traj
            if record.traj_path and record.traj_path.exists():
                record.traj_url = f"/api/uma-ase/job/{record.job_id}/trajectory"
            if record.opt_path and record.opt_path.exists():
                record.opt_url = f"/api/uma-ase/job/{record.job_id}/optimized"
            if record.freq_archive_path is None:
                fallback_zip = next(
                    (path for path in record.job_dir.glob("*-FREQS-modes.zip") if path.is_file()),
                    None,
                )
                if fallback_zip:
                    record.freq_archive_path = fallback_zip
            if _freqs_ready(record):
                record.freq_archive_url = f"/api/uma-ase/job/{record.job_id}/frequencies"
            record.worker = None

    except Exception as exc:
        with JOB_LOCK:
            record.status = "error" if not cancel_event.is_set() else "cancelled"
            record.message = "Job cancelled by user." if cancel_event.is_set() else str(exc)
            record.worker = None


def _execute_md_job(
    record: JobRecord,
    filename: str,
    md_options: Dict[str, Any],
):
    job_dir = record.job_dir
    input_path = job_dir / filename
    stem = Path(filename).stem or "input"
    log_path = record.log_path or job_dir / f"{stem}-MD.log"
    traj_path = record.traj_path or job_dir / f"{stem}-MD.traj"
    final_path = record.opt_path or job_dir / f"{stem}-MD-final.xyz"
    multi_xyz_path = job_dir / f"{stem}-MD.xyz"
    md_steps = md_options.get("steps", 0)
    traj_interval = max(1, int(md_options.get("traj_interval", 10)))
    log_interval = max(1, int(md_options.get("log_interval", 10)))
    engine = md_options.get("engine", "langevin")
    label = MD_ENGINE_LABELS.get(engine, engine)
    temperature = md_options.get("temperature", 300.0)
    timestep_fs = md_options.get("timestep_fs", 0.5)
    friction = md_options.get("friction", 0.0)
    relax_fs = md_options.get("relax_fs", 100.0)
    checkpoint = md_options.get("mlff_checkpoint")
    task = md_options.get("mlff_task")
    use_pbc = bool(md_options.get("use_pbc"))
    cell_parameters = md_options.get("cell_parameters")
    cancel_event = record.cancel_event
    if cancel_event is None:
        cancel_event = threading.Event()
        record.cancel_event = cancel_event

    if record.md_options is None:
        record.md_options = {}
    record.md_options.setdefault("multi_xyz", multi_xyz_path)
    record.md_multi_xyz = multi_xyz_path

    success = False
    error_message: Optional[str] = None
    trajectory = None
    try:
        with configure_logging(log_path) as logger:
            args = SimpleNamespace(
                input=str(input_path),
                chg=record.charge,
                spin=record.spin,
                optimizer="",
                grad=0.0,
                iter=md_steps,
                run_type=["md"],
                mlff_chk=checkpoint,
                mlff_task=task,
                temp=temperature,
                press=0.0,
                cpu=False,
                visualize=False,
                _chg_explicit=True,
                _spin_explicit=True,
            )
            status, context = setup_calculated_atoms(args, logger)
            if status != 0 or context is None:
                raise RuntimeError("UMA calculator setup failed; see log for details.")

            if cancel_event.is_set():
                logger.info("Cancellation requested before MD start.")
                raise JobCancelled("MD job cancelled by user.")

            logger.info("*****************************************************************************")
            logger.info("*                        Molecular Dynamics Run                             *")
            logger.info("*****************************************************************************")
            logger.info("* Engine          : %s", label)
            logger.info("* Steps           : %s", md_steps)
            logger.info("* Timestep (fs)   : %.4f", timestep_fs)
            logger.info("* Temperature (K) : %.2f", temperature)
            logger.info("* Friction (1/fs) : %.4f", friction)
            logger.info("* Traj interval   : %d", traj_interval)
            logger.info("* Log interval    : %d", log_interval)
            logger.info("* Checkpoint      : %s", checkpoint)
            logger.info("* Task            : %s", task)
            logger.info("* Periodic BC     : %s", "enabled" if use_pbc else "disabled")
            if use_pbc and cell_parameters:
                logger.info(
                    "* Cell (Å | °)    : a=%.3f b=%.3f c=%.3f | α=%.2f β=%.2f γ=%.2f",
                    cell_parameters[0],
                    cell_parameters[1],
                    cell_parameters[2],
                    cell_parameters[3],
                    cell_parameters[4],
                    cell_parameters[5],
                )
            if engine in {"npt_berendsen", "isotropic_mtk_npt", "mtk_npt", "langevin_baoab_npt", "melchionna_npt"}:
                logger.info("* Pressure (bar)  : %.6f", md_options.get("pressure_bar", 0.0))
            if engine in {"nvt_berendsen", "npt_berendsen"}:
                logger.info("* Thermostat tau  : %.4f fs", relax_fs)
            if engine == "npt_berendsen":
                logger.info("* Barostat tau    : %.4f fs", md_options.get("barostat_relax_fs", 1000.0))
                logger.info("* Compressibility : %.6e 1/bar", md_options.get("compressibility_bar", 0.0))
            if engine == "nose_hoover_chain":
                logger.info(
                    "* Nosé-Hoover     : tdamp=%.4f fs | chain=%d | tloop=%d",
                    md_options.get("nose_tdamp_fs", relax_fs),
                    md_options.get("nose_tchain", 3),
                    md_options.get("nose_tloop", 1),
                )
            if engine == "bussi":
                logger.info("* Bussi taut      : %.4f fs", md_options.get("bussi_taut_fs", relax_fs))
            if engine == "andersen":
                logger.info("* Andersen prob   : %.6f", md_options.get("andersen_prob", 0.0))
            if engine in {"isotropic_mtk_npt", "mtk_npt"}:
                logger.info(
                    "* MTK params      : tdamp=%.4f fs | pdamp=%.4f fs | tchain=%d | pchain=%d",
                    md_options.get("mtk_tdamp_fs", 100.0),
                    md_options.get("mtk_pdamp_fs", 1000.0),
                    md_options.get("mtk_tchain", 3),
                    md_options.get("mtk_pchain", 3),
                )
            if engine.startswith("langevin_baoab"):
                logger.info(
                    "* BAOAB params    : T_tau=%.4f fs | P_tau=%.4f fs | hydrostatic=%s",
                    md_options.get("baoab_ttau_fs", 50.0),
                    md_options.get("baoab_ptau_fs", 1000.0),
                    md_options.get("baoab_hydrostatic", False),
                )
            if engine == "melchionna_npt":
                logger.info(
                    "* Melchionna      : ttime=%.4f fs | ptime=%.4f fs | bulk=%.3f GPa",
                    md_options.get("melchionna_ttime_fs", 25.0),
                    md_options.get("melchionna_ptime_fs", 75.0),
                    md_options.get("melchionna_bulk_gpa", 100.0),
                )
            logger.info("*****************************************************************************")

            atoms = context.atoms
            if use_pbc:
                if cell_parameters:
                    try:
                        cell_matrix = cellpar_to_cell(cell_parameters)
                    except Exception as exc:
                        raise RuntimeError(f"Invalid cell parameters: {exc}") from exc
                    atoms.set_cell(cell_matrix, scale_atoms=True)
                atoms.set_pbc(True)
                cell_vectors = atoms.get_cell()
                logger.info("Cell matrix (Å):")
                axis_labels = ("a", "b", "c")
                for axis_label, vector in zip(axis_labels, cell_vectors):
                    logger.info("  %s = [%.6f %.6f %.6f]", axis_label, vector[0], vector[1], vector[2])
            else:
                atoms.set_pbc(False)
            _initialise_md_velocities(atoms, temperature, logger)
            dynamics = _create_md_dynamics(
                engine,
                atoms,
                md_options=md_options,
            )
            trajectory = Trajectory(str(traj_path), "w", atoms)

            def log_step():
                step = dynamics.nsteps
                potential = atoms.get_potential_energy()
                kinetic = atoms.get_kinetic_energy()
                total = potential + kinetic
                inst_temp = atoms.get_temperature()
                logger.info(
                    "Step %d/%d | E_pot=%.6f eV | E_kin=%.6f eV | E_tot=%.6f eV | T=%.2f K",
                    step,
                    md_steps,
                    potential,
                    kinetic,
                    total,
                    inst_temp,
                )

            dynamics.attach(log_step, interval=log_interval)
            dynamics.attach(trajectory.write, interval=traj_interval)
            def record_xyz_frame():
                step = dynamics.nsteps
                try:
                    potential = atoms.get_potential_energy()
                except Exception:
                    potential = float("nan")
                time_fs = step * timestep_fs
                comment = f"step={step} time_fs={time_fs:.6f} energy_ev={potential:.8f}"
                write(
                    multi_xyz_path,
                    atoms,
                    format="xyz",
                    append=True,
                    comment=comment,
                )

            dynamics.attach(record_xyz_frame, interval=traj_interval)

            logger.info(
                "Starting %s dynamics for %d steps (dt=%.4f fs).",
                label,
                md_steps,
                timestep_fs,
            )
            chunk = max(1, min(100, traj_interval, log_interval))
            completed = 0
            while completed < md_steps:
                if cancel_event.is_set():
                    logger.info("Cancellation requested. Halting MD integration.")
                    raise JobCancelled("MD job cancelled by user.")
                steps_this_round = min(chunk, md_steps - completed)
                dynamics.run(steps_this_round)
                completed += steps_this_round
            logger.info("Molecular dynamics finished successfully.")

            if not cancel_event.is_set():
                try:
                    write(
                        str(final_path),
                        atoms,
                        format="xyz",
                        comment=f"MD final snapshot | charge={record.charge} spin={record.spin}",
                    )
                    logger.info("Final files saved to %s", final_path)
                except Exception as exc:
                    logger.warning("Unable to write final files: %s", exc)

        success = True
    except JobCancelled as exc:
        error_message = str(exc)
        logger = app.logger
        logger.info("MD job %s cancelled by user.", record.job_id)
    except Exception as exc:
        error_message = str(exc)
        app.logger.exception("MD job %s failed", record.job_id)
    finally:
        if trajectory is not None:
            with suppress(Exception):
                trajectory.close()

        with JOB_LOCK:
            if cancel_event.is_set():
                record.status = "cancelled"
                record.message = error_message or "MD job cancelled by user."
            elif success:
                record.status = "completed"
                record.message = None
            else:
                record.status = "error"
                record.message = error_message or "MD job failed."

            if log_path.exists():
                record.log_url = f"/api/uma-ase/job/{record.job_id}/log"
            if traj_path.exists():
                record.traj_url = f"/api/uma-ase/job/{record.job_id}/trajectory"
            if final_path.exists():
                record.opt_url = f"/api/uma-ase/job/{record.job_id}/optimized"
            if multi_xyz_path.exists():
                record.md_multi_xyz = multi_xyz_path
                record.md_multi_xyz_url = f"/api/uma-ase/job/{record.job_id}/md_xyz"
            if multi_xyz_path.exists():
                record.md_options["multi_xyz"] = multi_xyz_path
            record.worker = None


def _send_job_file(path: Optional[Path], mimetype: str = "text/plain"):
    if path is None or not path.exists():
        abort(404)
    return send_file(
        path,
        mimetype=mimetype,
        as_attachment=True,
        download_name=path.name,
    )


@app.route("/api/uma-ase/job/<job_id>", methods=["GET"])
def job_status(job_id: str):
    record = _get_job(job_id)
    if _freqs_ready(record):
        record.freq_archive_url = f"/api/uma-ase/job/{record.job_id}/frequencies"
    log_text = ""
    if record.log_path and record.log_path.exists():
        try:
            log_text = record.log_path.read_text(encoding="utf-8")
        except OSError:
            log_text = ""
    return jsonify(
        {
            "status": record.status,
            "message": record.message,
            "log": log_text,
            "log_download": record.log_url,
            "traj_download": record.traj_url,
            "opt_download": record.opt_url,
            "md_xyz_download": f"/api/uma-ase/job/{record.job_id}/md_xyz" if record.md_multi_xyz and record.md_multi_xyz.exists() else None,
            "freqs_download": record.freq_archive_url,
        }
    )


@app.route("/api/uma-ase/job/<job_id>/cancel", methods=["POST"])
def cancel_job(job_id: str):
    record = _get_job(job_id)
    with JOB_LOCK:
        if record.status not in ("running",):
            return jsonify({"status": "error", "message": "Job is not running."}), 400
        cancel_event = record.cancel_event
        if cancel_event is None:
            cancel_event = threading.Event()
            record.cancel_event = cancel_event
        already_set = cancel_event.is_set()
        cancel_event.set()
        process = record.process
        job_kind = record.job_kind
        record.message = "Cancellation requested..."
    if already_set:
        return jsonify({"status": "ok"})
    if job_kind == "workflow" and process and process.poll() is None:
        try:
            process.terminate()
        except Exception:
            pass
    return jsonify({"status": "ok"})


@app.route("/api/uma-ase/job/<job_id>/log", methods=["GET"])
def download_job_log(job_id: str):
    record = _get_job(job_id)
    return _send_job_file(record.log_path, "text/plain")


@app.route("/api/uma-ase/job/<job_id>/trajectory", methods=["GET"])
def download_job_trajectory(job_id: str):
    record = _get_job(job_id)
    if record.traj_visual_path and record.traj_visual_path.exists():
        return _send_job_file(record.traj_visual_path, "text/plain")
    return _send_job_file(record.traj_path, "application/octet-stream")


@app.route("/api/uma-ase/job/<job_id>/optimized", methods=["GET"])
def download_job_optimized(job_id: str):
    record = _get_job(job_id)
    return _send_job_file(record.opt_path, "text/plain")


@app.route("/api/uma-ase/job/<job_id>/md_xyz", methods=["GET"])
def download_job_md_xyz(job_id: str):
    record = _get_job(job_id)
    return _send_job_file(record.md_multi_xyz, "text/plain")


@app.route("/api/uma-ase/md/job/<job_id>/frames", methods=["GET"])
def fetch_md_job_frames(job_id: str):
    record = _get_job(job_id)
    start_raw = request.args.get("start", "0")
    limit_raw = request.args.get("limit", "25")
    try:
        start_index = max(0, int(start_raw))
    except (TypeError, ValueError):
        return jsonify({"status": "error", "message": "start must be an integer."}), 400
    try:
        limit_val = int(limit_raw)
    except (TypeError, ValueError):
        return jsonify({"status": "error", "message": "limit must be an integer."}), 400
    limit_val = max(1, min(limit_val, 200))

    multi_xyz_path = record.md_multi_xyz
    if multi_xyz_path is None and record.md_options:
        candidate = record.md_options.get("multi_xyz")
        if isinstance(candidate, Path):
            multi_xyz_path = candidate
        elif isinstance(candidate, str):
            multi_xyz_path = Path(candidate)

    available = multi_xyz_path is not None and multi_xyz_path.exists()
    if not available:
        return jsonify(
            {
                "frames": [],
                "next_index": start_index,
                "total_frames": 0,
                "job_status": record.status,
                "available": False,
            }
        )

    frames, total_frames = _extract_xyz_frames(multi_xyz_path, start_index, limit_val)
    next_index = start_index + len(frames)
    return jsonify(
        {
            "frames": frames,
            "next_index": next_index,
            "total_frames": total_frames,
            "job_status": record.status,
            "available": True,
            "has_more": next_index < total_frames or record.status == "running",
        }
    )


@app.route("/api/uma-ase/md/traj/convert", methods=["POST"])
def convert_md_traj_to_xyz():
    trajectory_file = request.files.get("trajectory")
    if trajectory_file is None or trajectory_file.filename == "":
        return jsonify({"status": "error", "message": "Trajectory file is required."}), 400

    max_frames_raw = request.form.get("max_frames")
    max_frames = 500
    if max_frames_raw not in (None, ""):
        try:
            max_frames = max(1, min(int(max_frames_raw), 2000))
        except (TypeError, ValueError):
            return jsonify({"status": "error", "message": "max_frames must be an integer."}), 400

    with tempfile.TemporaryDirectory(prefix="uma_traj_convert_") as temp_dir_str:
        temp_dir = Path(temp_dir_str)
        temp_path = temp_dir / (secure_filename(trajectory_file.filename) or "trajectory.traj")
        trajectory_file.save(temp_path)
        try:
            images = read(temp_path, ":")
        except Exception as exc:  # pragma: no cover - depends on input formats
            return jsonify({"status": "error", "message": f"Unable to parse trajectory: {exc}"}), 400

    frames: list[str] = []
    for index, atoms in enumerate(images):
        if index >= max_frames:
            break
        buffer = io.StringIO()
        try:
            potential = atoms.get_potential_energy()
        except Exception:
            potential = None
        time_value = atoms.info.get("time_fs")
        if time_value is None:
            time_value = atoms.info.get("time")
        try:
            time_value = float(time_value)
        except (TypeError, ValueError):
            time_value = None
        comment_parts = [f"step={index}"]
        if time_value is not None and math.isfinite(time_value):
            comment_parts.append(f"time_fs={time_value:.6f}")
        if potential is not None and math.isfinite(potential):
            comment_parts.append(f"energy_ev={float(potential):.8f}")
        write(buffer, atoms, format="xyz", comment=" ".join(comment_parts))
        frames.append(buffer.getvalue().strip())

    total_frames = len(images)
    return jsonify(
        {
            "status": "ok",
            "frames": frames,
            "total_frames": total_frames,
            "returned_frames": len(frames),
            "truncated": len(frames) < total_frames,
        }
    )


@app.route("/api/uma-ase/job/<job_id>/frequencies", methods=["GET"])
def download_job_frequencies(job_id: str):
    record = _get_job(job_id)
    freq_folder = record.freq_folder or (record.job_dir / "freqs")
    if freq_folder.exists():
        converted = _convert_traj_tree_to_xyz(freq_folder)
        if converted:
            app.logger.info("Converted %d normal mode trajectories under %s", converted, freq_folder)

    if record.freq_archive_path and record.freq_archive_path.exists():
        return _send_job_file(record.freq_archive_path, "application/zip")
    if not freq_folder.exists():
        abort(404)
    files = [path for path in freq_folder.rglob("*") if path.is_file()]
    if not files:
        abort(404)
    freq_base = freq_folder.name or Path(record.opt_path or record.job_dir).stem
    temp_dir = Path(tempfile.mkdtemp(prefix="uma_freqs_"))
    archive_path = temp_dir / f"{freq_base}-FREQS-modes.zip"
    try:
        with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as archive:
            for file_path in files:
                try:
                    arcname = file_path.relative_to(freq_folder.parent)
                except ValueError:
                    arcname = file_path.name
                archive.write(file_path, str(arcname))
    except Exception:
        shutil.rmtree(temp_dir, ignore_errors=True)
        raise

    @after_this_request
    def cleanup(response):  # pragma: no cover
        shutil.rmtree(temp_dir, ignore_errors=True)
        return response

    return send_file(
        archive_path,
        mimetype="application/zip",
        as_attachment=True,
        download_name=f"{freq_base}-FREQS-modes.zip",
    )


@app.route("/api/uma-ase/clean", methods=["POST"])
def clean_results_root():
    base_dir = Path.home() / ".uma_ase"
    try:
        if base_dir.exists():
            shutil.rmtree(base_dir)
        results_root = Path(app.config["UMA_RESULTS_DIR"])
        results_root.mkdir(parents=True, exist_ok=True)
        ANALYZE_REPORT_ROOT.mkdir(parents=True, exist_ok=True)
        return jsonify({"status": "ok"})
    except OSError as exc:
        return jsonify({"status": "error", "message": str(exc)}), 500


@app.route("/api/uma-ase/multi/logs/<path:folder>", methods=["GET"])
def download_multi_logs(folder: str):
    safe_folder = secure_filename(folder)
    if not safe_folder:
        abort(404)
    multi_root = (Path(app.config["UMA_RESULTS_DIR"]) / "multi_runs").resolve()
    target_dir = (multi_root / safe_folder).resolve()
    try:
        target_dir.relative_to(multi_root)
    except ValueError:
        abort(404)
    if not target_dir.exists():
        abort(404)
    produced_files = [path for path in target_dir.rglob("*") if path.is_file()]
    if not produced_files:
        abort(404)

    extra_freq_entries = []
    for freq_dir in target_dir.glob("**/freqs"):
        if not freq_dir.is_dir():
            continue
        try:
            rel_freq_dir = freq_dir.relative_to(target_dir)
        except ValueError:
            continue
        parts = rel_freq_dir.parts
        if parts and parts[0] == "freqs":
            continue
        try:
            rel_parent = freq_dir.parent.relative_to(target_dir)
        except ValueError:
            continue
        arc_prefix = Path("freqs") / rel_parent
        for file_path in freq_dir.rglob("*"):
            if file_path.is_file():
                arcname = arc_prefix / file_path.relative_to(freq_dir)
                extra_freq_entries.append((file_path, arcname))

    temp_dir = Path(tempfile.mkdtemp(prefix="uma_logs_"))
    archive_path = temp_dir / f"{safe_folder}_files.zip"
    try:
        with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as archive:
            for file_path in produced_files:
                archive.write(file_path, file_path.relative_to(target_dir))
            for src_path, arcname in extra_freq_entries:
                archive.write(src_path, str(arcname))
    except Exception:
        shutil.rmtree(temp_dir, ignore_errors=True)
        raise

    @after_this_request
    def cleanup(response):  # pragma: no cover
        shutil.rmtree(temp_dir, ignore_errors=True)
        return response

    return send_file(
        archive_path,
        mimetype="application/zip",
        as_attachment=True,
        download_name=f"{safe_folder}_files.zip",
    )




@app.route("/api/uma-ase/iochem/fetch", methods=["POST"])
def fetch_iochem_geometry():
    payload = request.get_json(silent=True) or {}
    raw_handle = payload.get("handle") or request.form.get("handle")
    if raw_handle is None or not str(raw_handle).strip():
        return jsonify({"status": "error", "message": "Handle is required."}), 400
    try:
        geometry = _download_iochem_geometry(str(raw_handle))
    except ValueError as exc:
        app.logger.warning("ioChem-BD fetch failed for %s: %s", raw_handle, exc)
        return jsonify({"status": "error", "message": str(exc)}), 400
    except Exception as exc:  # pragma: no cover - defensive logging
        app.logger.exception("Unexpected ioChem-BD error: %s", exc)
        return jsonify({"status": "error", "message": "Unable to download ioChem-BD geometry."}), 502

    return jsonify(
        {
            "status": "ok",
            "handle": geometry.handle,
            "source_url": geometry.source_url,
            "filename": geometry.filename,
            "geometry": geometry.xyz_content,
            "charge": geometry.charge,
            "spin": geometry.spin,
            "formula": geometry.formula,
            "num_atoms": geometry.num_atoms,
            "element_counts": geometry.element_counts,
        }
    )


@app.route("/api/uma-ase/preview", methods=["POST"])
def preview_structure():
    geometry = request.files.get("geometry")
    if geometry is None or geometry.filename == "":
        return jsonify({"status": "error", "message": "Geometry file is required."}), 400

    charge_raw = request.form.get("charge")
    spin_raw = request.form.get("spin")
    spin_val = 1

    with tempfile.TemporaryDirectory(prefix="uma_preview_") as temp_dir_str:
        temp_dir = Path(temp_dir_str)
        filename = secure_filename(geometry.filename) or "input.xyz"
        input_path = temp_dir / filename
        geometry.save(input_path)

        metadata = extract_xyz_metadata(input_path)

        if charge_raw is None or charge_raw.strip() == "":
            charge_val = metadata.charge if metadata.charge is not None else 0
        else:
            try:
                charge_val = int(charge_raw)
            except (TypeError, ValueError):
                return jsonify({"status": "error", "message": "Charge must be an integer."}), 400

        if spin_raw is None or spin_raw.strip() == "":
            if metadata.spin is not None and metadata.spin > 0:
                spin_val = metadata.spin
            else:
                spin_val = 1
        else:
            try:
                spin_val = int(spin_raw)
            except (TypeError, ValueError):
                return jsonify({"status": "error", "message": "Spin multiplicity must be an integer."}), 400
            if spin_val <= 0:
                return jsonify({"status": "error", "message": "Spin multiplicity must be positive."}), 400

        try:
            atoms = read(str(input_path))
        except Exception as exc:  # pragma: no cover - depends on external IO
            return jsonify({"status": "error", "message": f"Unable to read geometry: {exc}"}), 400

        atoms.info["charge"] = charge_val
        atoms.info["spin"] = spin_val
        xyz_comment = metadata.comment
        if xyz_comment:
            atoms.info.setdefault("uma_comment", xyz_comment)
        if metadata.url:
            atoms.info.setdefault("uma_comment_url", metadata.url)

        counts = Counter(atoms.get_chemical_symbols())
        num_atoms = len(atoms)
        formula = atoms.get_chemical_formula()
        element_counts = dict(counts)

        # Decide device availability using fairchem rules
        try:
            device = select_device()
        except TorchUnavailable:
            device = "cpu"

    summary_lines = [
        f"Number of atoms: {num_atoms}",
        f"Formula: {formula}",
        f"Element counts: {element_counts}",
        f"Device: {device}",
    ]
    summary_lines.insert(0, f"Spin multiplicity: {spin_val}")
    summary_lines.insert(0, f"Charge: {charge_val}")
    if xyz_comment:
        summary_lines.insert(0, f"Comment: {xyz_comment}")
    if metadata.url:
        summary_lines.insert(0, f"Source URL: {metadata.url}")

    return jsonify(
        {
            "status": "ok",
            "initial_geometry": filename,
            "num_atoms": num_atoms,
            "formula": formula,
            "element_counts": element_counts,
            "charge": charge_val,
            "spin": spin_val,
            "device": device,
            "comment": xyz_comment,
            "lines": summary_lines,
        }
    )
def create_app() -> Flask:
    """Factory for embedding in external WSGI servers."""
    return app


def main() -> None:
    """Run the development server."""
    app.run(debug=True, port=8000)


if __name__ == "__main__":  # pragma: no cover
    main()
