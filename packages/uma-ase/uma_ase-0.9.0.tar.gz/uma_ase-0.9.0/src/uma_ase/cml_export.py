"""Utilities for exporting UMA ASE log files to the CML schema."""

from __future__ import annotations

import argparse
import ast
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Dict, Iterable, List, Optional, Sequence, Tuple
from xml.etree.ElementTree import Element, ElementTree, SubElement

try:  # pragma: no cover - fallback when running as a plain script
    from . import __version__
except ImportError:  # pragma: no cover - executed when module run directly
    __version__ = "unknown"


CML_NS = "http://www.xml-cml.org/schema"
UMA_NS = "http://www.iochem-bd.org/dictionary/uma/"


ROOT_NAMESPACE_ATTRS = {
    "xmlns": CML_NS,
    "xmlns:uma": UMA_NS,
    "xmlns:cc": "http://www.xml-cml.org/dictionary/compchem/",
    "xmlns:cml": CML_NS,
    "xmlns:cmlx": "http://www.xml-cml.org/schema/cmlx",
    "xmlns:convention": "http://www.xml-cml.org/convention/",
    "xmlns:nonsi": "http://www.xml-cml.org/unit/nonSi/",
    "xmlns:nonsi2": "http://www.iochem-bd.org/unit/nonSi2/",
    "xmlns:si": "http://www.xml-cml.org/unit/si/",
    "xmlns:xi": "http://www.w3.org/2001/XInclude",
    "xmlns:xsd": "http://www.w3.org/2001/XMLSchema",
}

CMLX_NS = ROOT_NAMESPACE_ATTRS["xmlns:cmlx"]
PLACEHOLDER_TEXT = "TODO"


def slugify(text: str, *, separator: str = "-") -> str:
    """Convert *text* to a lowercase slug suitable for identifiers."""

    slug = re.sub(r"[^0-9a-zA-Z]+", separator, text.lower()).strip(separator)
    return slug or "value"


def set_template_ref(element: Element, template: str) -> None:
    element.set(f"{{{CMLX_NS}}}templateRef", template)


def format_float(value: float) -> str:
    """Format floating point numbers with trimmed trailing zeros."""

    return ("{:.8f}".format(value)).rstrip("0").rstrip(".") or "0"


@dataclass
class AtomRecord:
    element: str
    x: float
    y: float
    z: float


@dataclass
class GeometryBlock:
    label: str
    atoms: List[AtomRecord] = field(default_factory=list)


@dataclass
class OptimizationStep:
    optimizer: str
    step: int
    time: str
    energy: float
    fmax: float


@dataclass
class NormalMode:
    index: int
    energy_mev: float
    wavenumber_cm1: float
    imaginary: bool = False


@dataclass
class NormalModeDisplacementRow:
    atom_index: int
    symbol: str
    component: str
    displacements: List[float]


@dataclass
class ThermoValue:
    label: str
    value: float
    unit: str


@dataclass
class EntropyComponent:
    label: str
    value: float
    value_unit: str
    ts_value: float
    ts_unit: str


@dataclass
class LogData:
    source: Path
    metadata: Dict[str, str]
    header_metadata: Dict[str, str]
    element_counts: Dict[str, int]
    run_types: List[str]
    geometries: Dict[str, GeometryBlock]
    energies: Dict[str, float]
    atomic_energies: Dict[str, float]
    sum_atomic_energies: Optional[float]
    bonding_energy_ev: Optional[float]
    bonding_energy_kcal: Optional[float]
    rmsd: Optional[float]
    optimization_steps: List[OptimizationStep]
    frequencies: List[NormalMode]
    zero_point_energy: Optional[float]
    enthalpy_components: List[ThermoValue]
    entropy_components: List[EntropyComponent]
    free_energy_components: List[ThermoValue]
    mode_displacements: List[NormalModeDisplacementRow]
    run_start: Optional[str]


class UmaLogParser:
    """Parser converting UMA ASE text logs into structured data."""

    ARGUMENT_LINE = re.compile(r"^\s{2}([\w]+)\s*:\s*(.+)$")
    HEADER_LINE = re.compile(r"^\*+\s*([^:]+):\s*(.+)$")
    ATOM_LINE = re.compile(
        r"^\s*([A-Za-z][A-Za-z0-9]*)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)"
    )
    OPT_LINE = re.compile(
        r"^(?P<optimizer>[A-Z0-9_]+):\s+(?P<step>\d+)\s+(?P<time>\d{2}:\d{2}:\d{2})\s+"
        r"(?P<energy>-?\d+\.\d+)\s+(?P<fmax>\d+\.\d+)"
    )
    ATOMIC_ENERGY_RE = re.compile(
        r"^Atomic energy for atom type ([A-Za-z0-9]+):\s+(-?\d+\.\d+)"
    )
    ENERGY_LINE = re.compile(r"^(Potential|Total) Energy:\s+(-?\d+\.\d+)")
    SUM_ATOMIC_RE = re.compile(r"^Sum of atomic energies:\s+(-?\d+\.\d+)")
    BONDING_RE = re.compile(r"^Bonding Energy:\s+(-?\d+\.\d+)\s+([\w./-]+)")
    RMSD_RE = re.compile(r"^RMSD .*:\s+(-?\d+\.\d+)")
    ZERO_POINT_RE = re.compile(r"^Zero-point energy:\s+(-?\d+\.\d+)")
    SINGLE_VALUE_RE = re.compile(
        r"^\s*([A-Za-z0-9_():<>\-+*/ ]+)\s+(-?\d+\.\d+)\s+([A-Za-z/\-*]+)"
    )
    DOUBLE_VALUE_RE = re.compile(
        r"^\s*([A-Za-z0-9_():<>\-+*/ ]+)\s+(-?\d+\.\d+)\s+([A-Za-z/\-*]+)\s+"
        r"(-?\d+\.\d+)\s+([A-Za-z/\-*]+)"
    )
    RUN_TIMESTAMP_RE = re.compile(
        r"^(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}(?:\.\d+)?)"
    )

    def __init__(self, path: Path):
        self.path = path
        self.lines = path.read_text(encoding="utf-8").splitlines()

    def parse(self) -> LogData:
        metadata = self._parse_arguments()
        header_metadata, element_counts = self._parse_header()
        run_types = self._parse_run_types(metadata)
        geometries = self._parse_geometries()
        energies = self._parse_energies()
        atomic_energies = self._parse_atomic_energies()
        sum_atomic = self._match_float(self.SUM_ATOMIC_RE)
        bonding_ev, bonding_kcal = self._parse_bonding()
        rmsd = self._match_float(self.RMSD_RE)
        optimization_steps = self._parse_optimization_steps()
        frequencies = self._parse_frequencies()
        displacement_rows = self._parse_mode_displacements()
        zero_point = self._match_float(self.ZERO_POINT_RE)
        enthalpy = self._parse_section("Enthalpy components", double=False)
        entropy = self._parse_entropy_section()
        free_energy = self._parse_section("Free energy components", double=False)
        run_start = self._parse_run_start()
        return LogData(
            source=self.path,
            metadata=metadata,
            header_metadata=header_metadata,
            element_counts=element_counts,
            run_types=run_types,
            geometries=geometries,
            energies=energies,
            atomic_energies=atomic_energies,
            sum_atomic_energies=sum_atomic,
            bonding_energy_ev=bonding_ev,
            bonding_energy_kcal=bonding_kcal,
            rmsd=rmsd,
            optimization_steps=optimization_steps,
            frequencies=frequencies,
            zero_point_energy=zero_point,
            enthalpy_components=[ThermoValue(*item) for item in enthalpy],
            entropy_components=entropy,
            free_energy_components=[ThermoValue(*item) for item in free_energy],
            mode_displacements=displacement_rows,
            run_start=run_start,
        )

    def _parse_arguments(self) -> Dict[str, str]:
        args: Dict[str, str] = {}
        in_block = False
        for line in self.lines:
            stripped = line.strip()
            if stripped.startswith("Parsed & Catch Arguments"):
                in_block = True
                continue
            if in_block:
                if not stripped:
                    in_block = False
                    continue
                match = self.ARGUMENT_LINE.match(line)
                if match:
                    key, value = match.groups()
                    args[key] = value.strip()
                continue
            inferred = re.match(r"^Charge inferred.*?:\s+(.+)$", stripped)
            if inferred:
                args.setdefault("inferred_charge", inferred.group(1).strip())
        return args

    def _parse_header(self) -> Tuple[Dict[str, str], Dict[str, int]]:
        header: Dict[str, str] = {}
        element_counts: Dict[str, int] = {}
        for line in self.lines:
            match = self.HEADER_LINE.match(line)
            if not match:
                continue
            key = slugify(match.group(1)).replace("-", "_")
            value = match.group(2).strip()
            header[key] = value
            if key == "element_counts":
                try:
                    parsed = ast.literal_eval(value)
                except (SyntaxError, ValueError):
                    parsed = {}
                if isinstance(parsed, dict):
                    element_counts = {
                        str(sym): int(count) for sym, count in parsed.items()
                    }
            elif key == "number_of_atoms":
                header[key] = value
            elif key in {"charge", "spin_multiplicity"}:
                header[key] = value
        return header, element_counts

    def _parse_run_types(self, metadata: Dict[str, str]) -> List[str]:
        raw = metadata.get("run_type")
        if not raw:
            return []
        try:
            parsed = ast.literal_eval(raw)
        except (SyntaxError, ValueError):
            parsed = [raw]
        if isinstance(parsed, (list, tuple)):
            return [str(item).lower() for item in parsed]
        return [str(parsed).lower()]

    def _parse_geometries(self) -> Dict[str, GeometryBlock]:
        geometries: Dict[str, GeometryBlock] = {}
        idx = 0
        while idx < len(self.lines):
            line = self.lines[idx].strip()
            if line.startswith("Initial geometry") or line.startswith("Final geometry") or line.startswith("Geometry for"):
                label = line.rsplit("(", 1)[0].strip()
                atoms: List[AtomRecord] = []
                idx += 1
                while idx < len(self.lines):
                    atom_line = self.lines[idx]
                    if not atom_line.strip():
                        break
                    atom_match = self.ATOM_LINE.match(atom_line)
                    if atom_match:
                        element, x, y, z = atom_match.groups()
                        atoms.append(AtomRecord(element, float(x), float(y), float(z)))
                        idx += 1
                        continue
                    break
                if atoms:
                    slug = slugify(label)
                    geometries[slug] = GeometryBlock(label=label, atoms=atoms)
                continue
            idx += 1
        return geometries

    def _parse_energies(self) -> Dict[str, float]:
        energies: Dict[str, float] = {}
        for line in self.lines:
            match = self.ENERGY_LINE.match(line)
            if match:
                label, value = match.groups()
                energies[label.lower()] = float(value)
        return energies

    def _parse_atomic_energies(self) -> Dict[str, float]:
        atomic: Dict[str, float] = {}
        for line in self.lines:
            match = self.ATOMIC_ENERGY_RE.match(line.strip())
            if match:
                symbol, value = match.groups()
                atomic[symbol] = float(value)
        return atomic

    def _match_float(self, pattern: re.Pattern[str]) -> Optional[float]:
        for line in self.lines:
            match = pattern.match(line.strip())
            if match:
                return float(match.group(1))
        return None

    def _parse_bonding(self) -> Tuple[Optional[float], Optional[float]]:
        ev_value: Optional[float] = None
        kcal_value: Optional[float] = None
        for line in self.lines:
            match = self.BONDING_RE.match(line.strip())
            if match:
                value, unit = match.groups()
                if unit.lower().startswith("kcal"):
                    kcal_value = float(value)
                else:
                    ev_value = float(value)
        return ev_value, kcal_value

    def _parse_optimization_steps(self) -> List[OptimizationStep]:
        steps: List[OptimizationStep] = []
        for line in self.lines:
            match = self.OPT_LINE.match(line.strip())
            if match:
                info = match.groupdict()
                steps.append(
                    OptimizationStep(
                        optimizer=info["optimizer"],
                        step=int(info["step"]),
                        time=info["time"],
                        energy=float(info["energy"]),
                        fmax=float(info["fmax"]),
                    )
                )
        return steps

    def _parse_frequencies(self) -> List[NormalMode]:
        frequencies: List[NormalMode] = []
        try:
            summary_idx = next(
                idx for idx, line in enumerate(self.lines) if line.strip().startswith("Vibrational summary")
            )
        except StopIteration:
            return frequencies
        header_idx = summary_idx
        while header_idx < len(self.lines) and not self.lines[header_idx].strip().startswith("#"):
            header_idx += 1
        data_idx = header_idx + 2
        for idx in range(data_idx, len(self.lines)):
            stripped = self.lines[idx].strip()
            if not stripped or stripped.startswith("-"):
                if stripped.startswith("-"):
                    break
                continue
            parts = stripped.split()
            if len(parts) < 3:
                continue
            mode_index = int(parts[0])
            meV_str = parts[1]
            cm_str = parts[2]
            imag = meV_str.endswith("i") or cm_str.endswith("i")
            meV_value = float(meV_str.rstrip("i"))
            cm_value = float(cm_str.rstrip("i"))
            frequencies.append(
                NormalMode(
                    index=mode_index,
                    energy_mev=meV_value,
                    wavenumber_cm1=cm_value,
                    imaginary=imag,
                )
            )
        return frequencies

    def _parse_mode_displacements(self) -> List[NormalModeDisplacementRow]:
        marker = "Normal mode displacement matrix"
        try:
            start_idx = next(idx for idx, line in enumerate(self.lines) if marker in line)
        except StopIteration:
            return []

        # Skip optional blank lines to reach the header describing mode columns
        header_idx = start_idx + 1
        while header_idx < len(self.lines) and not self.lines[header_idx].strip():
            header_idx += 1
        if header_idx >= len(self.lines):
            return []

        rows: List[NormalModeDisplacementRow] = []
        idx = header_idx + 1
        while idx < len(self.lines):
            line = self.lines[idx]
            stripped = line.strip()
            if not stripped:
                break
            if stripped.startswith("*") or stripped.startswith("Vibrational summary"):
                break
            parts = line.split()
            if len(parts) < 4:
                idx += 1
                continue
            try:
                atom_index = int(parts[0])
            except ValueError:
                idx += 1
                continue
            symbol = parts[1]
            component = parts[2]
            displacement_values = []
            for raw in parts[3:]:
                try:
                    displacement_values.append(float(raw))
                except ValueError:
                    displacement_values = []
                    break
            if displacement_values:
                rows.append(
                    NormalModeDisplacementRow(
                        atom_index=atom_index,
                        symbol=symbol,
                        component=component,
                        displacements=displacement_values,
                    )
                )
            idx += 1
        return rows

    def _parse_run_start(self) -> Optional[str]:
        for line in self.lines:
            match = self.RUN_TIMESTAMP_RE.match(line.strip())
            if match:
                return match.group("timestamp")
        return None

    def _parse_section(self, header: str, double: bool) -> List[Tuple[str, float, str]]:
        lines = self._extract_section_lines(header)
        entries: List[Tuple[str, float, str]] = []
        for line in lines:
            stripped = line.strip()
            if not stripped or set(stripped) == {"-"}:
                continue
            match = self.DOUBLE_VALUE_RE.match(line) if double else self.SINGLE_VALUE_RE.match(line)
            if match:
                if double:
                    label, v1, u1, _, _ = match.groups()
                    entries.append((label.strip(), float(v1), u1))
                else:
                    label, value, unit = match.groups()
                    entries.append((label.strip(), float(value), unit))
        return entries

    def _parse_entropy_section(self) -> List[EntropyComponent]:
        lines = self._extract_section_lines("Entropy components")
        components: List[EntropyComponent] = []
        for line in lines:
            stripped = line.strip()
            if not stripped or set(stripped) == {"-"}:
                continue
            match = self.DOUBLE_VALUE_RE.match(line)
            if match:
                label, value, unit, ts_value, ts_unit = match.groups()
                components.append(
                    EntropyComponent(
                        label=label.strip(),
                        value=float(value),
                        value_unit=unit,
                        ts_value=float(ts_value),
                        ts_unit=ts_unit,
                    )
                )
        return components

    def _extract_section_lines(self, header: str) -> List[str]:
        try:
            start = next(
                idx for idx, line in enumerate(self.lines) if line.strip().startswith(header)
            )
        except StopIteration:
            return []
        idx = start + 1
        while idx < len(self.lines) and not self.lines[idx].strip().startswith("="):
            idx += 1
        idx += 1
        section: List[str] = []
        while idx < len(self.lines):
            stripped = self.lines[idx].strip()
            if stripped.startswith("="):
                break
            section.append(self.lines[idx])
            idx += 1
        return section


VALUE_WITH_UNIT_RE = re.compile(
    r"^(-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)\s+([A-Za-z][A-Za-z0-9/\-]*)$"
)


UNIT_MAP = {
    "k": "si:K",
    "pa": "si:Pa",
    "ev": "nonsi:electronvolt",
    "mev": "uma:millielectronvolt",
    "ev/k": "uma:electronvoltPerKelvin",
    "angstrom": "nonsi:angstrom",
    "cm^-1": "nonsi:cm-1",
    "cm-1": "nonsi:cm-1",
    "kcal.mol-1": "nonsi2:kcal.mol-1",
    "kcal/mol": "nonsi2:kcal.mol-1",
}


def qualify_unit(unit: Optional[str]) -> Optional[str]:
    if not unit:
        return None
    if ":" in unit:
        return unit
    normalized = unit.strip()
    mapped = UNIT_MAP.get(normalized.lower())
    if mapped:
        return mapped
    return f"uma:{slugify(normalized)}"


def normalize_parameter_value(value: str | int | float) -> Tuple[str | int | float, Optional[str]]:
    """Best-effort conversion of parameter text into numeric value and unit."""

    if isinstance(value, (int, float)):
        return value, None
    text = str(value).strip()
    match = VALUE_WITH_UNIT_RE.match(text)
    if match:
        number = float(match.group(1))
        unit = match.group(2)
        return number, unit
    try:
        return int(text), None
    except ValueError:
        try:
            return float(text), None
        except ValueError:
            return text, None


def add_parameter(
    parent: Element,
    dict_ref: str,
    value: str | int | float,
    *,
    title: Optional[str] = None,
) -> Element:
    """Append a parameter/scalar pair under *parent* parameterList."""

    parameter = SubElement(parent, "parameter", {"dictRef": dict_ref})
    if title:
        parameter.set("title", title)
    coerced, unit = normalize_parameter_value(value)
    if isinstance(coerced, int):
        data_type = "xsd:integer"
        text = str(coerced)
    elif isinstance(coerced, float):
        data_type = "xsd:double"
        text = format_float(coerced)
    else:
        data_type = "xsd:string"
        text = str(coerced)
    scalar_attrs = {"dataType": data_type}
    if unit:
        scalar_attrs["units"] = qualify_unit(unit)
    scalar = SubElement(parameter, "scalar", scalar_attrs)
    scalar.text = text
    return parameter


def add_property(
    parent: Element,
    dict_ref: str,
    value: float | int | str,
    *,
    units: Optional[str] = None,
    title: Optional[str] = None,
    data_type: str = "xsd:double",
):
    prop = SubElement(parent, "property", {"dictRef": dict_ref})
    if title:
        prop.set("title", title)
    scalar_attrs: Dict[str, str] = {"dataType": data_type}
    if isinstance(value, str):
        scalar_attrs["dataType"] = "xsd:string"
        scalar_text = value
    else:
        numeric: float
        if isinstance(value, int):
            scalar_attrs["dataType"] = "xsd:integer" if data_type == "xsd:integer" else "xsd:double"
            numeric = float(value)
        else:
            numeric = float(value)
            scalar_attrs["dataType"] = data_type
        scalar_text = format_float(numeric) if scalar_attrs["dataType"] != "xsd:integer" else str(int(numeric))
    if units:
        scalar_attrs["units"] = qualify_unit(units)
    scalar = SubElement(prop, "scalar", scalar_attrs)
    scalar.text = scalar_text
    return prop


def add_molecule(parent: Element, molecule_id: str, geometry: GeometryBlock) -> None:
    molecule = SubElement(parent, "molecule", {"id": molecule_id})
    molecule.set("title", geometry.label)
    atom_array = SubElement(molecule, "atomArray")
    for idx, atom in enumerate(geometry.atoms, start=1):
        attrs = {
            "id": f"{molecule_id}-a{idx}",
            "elementType": atom.element,
            "x3": format_float(atom.x),
            "y3": format_float(atom.y),
            "z3": format_float(atom.z),
        }
        SubElement(atom_array, "atom", attrs)


def add_list_with_scalars(
    parent: Element,
    dict_ref: str,
    entries: Iterable[Tuple[str, float, str]],
    *,
    element_title: str,
    dict_ref_mapper: Optional[Callable[[str], Optional[str]]] = None,
) -> None:
    lst = SubElement(parent, "list", {"dictRef": dict_ref})
    for title, value, unit in entries:
        scalar_dict_ref = element_title
        if dict_ref_mapper:
            override = dict_ref_mapper(title)
            if override:
                scalar_dict_ref = override
        attrs = {
            "dictRef": scalar_dict_ref,
            "dataType": "xsd:double",
        }
        qualified_unit = qualify_unit(unit)
        if qualified_unit:
            attrs["units"] = qualified_unit
        scalar = SubElement(
            lst,
            "scalar",
            attrs,
        )
        scalar.set("title", title)
        scalar.text = format_float(value)


def add_entropy_list(parent: Element, components: Sequence[EntropyComponent]) -> None:
    if not components:
        return
    lst = SubElement(parent, "list", {"dictRef": "uma:entropyComponents"})
    for component in components:
        entry = SubElement(lst, "list", {"dictRef": "uma:entropyComponent"})
        val = SubElement(entry, "scalar", {
            "dictRef": "uma:S",
            "dataType": "xsd:double",
            "units": qualify_unit(component.value_unit),
            "title": component.label,
        })
        val.text = format_float(component.value)
        ts = SubElement(entry, "scalar", {
            "dictRef": "uma:TS",
            "dataType": "xsd:double",
            "units": qualify_unit(component.ts_unit),
            "title": component.label,
        })
        ts.text = format_float(component.ts_value)


def add_array(
    parent: Element,
    dict_ref: str,
    values: Sequence[object],
    *,
    data_type: str,
    units: Optional[str] = None,
) -> Element:
    """Append a cml:array with formatted values."""

    attrs = {
        "dictRef": dict_ref,
        "dataType": data_type,
        "size": str(len(values)),
    }
    qualified_units = qualify_unit(units)
    if qualified_units:
        attrs["units"] = qualified_units
    array = SubElement(parent, "array", attrs)
    def _format(value: object) -> str:
        if data_type == "xsd:double":
            return format_float(float(value))
        if data_type == "xsd:integer":
            return str(int(value))
        if data_type == "xsd:boolean":
            return "true" if bool(value) else "false"
        return str(value)
    array.text = " ".join(_format(v) for v in values)
    return array


def determine_job_title(data: LogData) -> str:
    """Generate a human readable title for the CompChem job module."""

    def normalize(entries: Iterable[Tuple[str, str]]) -> Dict[str, str]:
        normalized: Dict[str, str] = {}
        for key, value in entries:
            text = str(value).strip()
            if not text:
                continue
            normalized[key.lower()] = text
        return normalized

    metadata_lookup = normalize(data.metadata.items())
    header_lookup = normalize(data.header_metadata.items())
    candidate_keys = (
        "title",
        "name",
        "label",
        "job_name",
        "jobname",
        "job",
        "calculation",
        "calculation_type",
        "system",
        "molecule",
        "alias",
        "project",
    )
    for candidate in candidate_keys:
        lowered = candidate.lower()
        if lowered in metadata_lookup:
            return metadata_lookup[lowered]
        if lowered in header_lookup:
            return header_lookup[lowered]
    if data.run_types:
        unique_run_types = list(dict.fromkeys(data.run_types))
        run_label = ", ".join(rt.replace("_", " ") for rt in unique_run_types).strip()
        if run_label:
            return f"{run_label} job"
    source_label = data.source.stem.replace("_", " ").strip()
    if source_label:
        return f"{source_label} job"
    return "UMA ASE job"


def select_initial_geometry(geometries: Dict[str, GeometryBlock]) -> Optional[GeometryBlock]:
    """Pick a geometry block suitable for the initialization module."""

    if not geometries:
        return None
    for slug, geometry in geometries.items():
        if "initial" in slug.lower():
            return geometry
    return next(iter(geometries.values()))


FINAL_GEOMETRY_KEYWORDS = ("final", "optimized", "optimised", "opt", "geometry-for-frequencies")


def select_final_geometry(geometries: Dict[str, GeometryBlock]) -> Optional[GeometryBlock]:
    """Return the latest/optimized geometry using heuristic keyword matching."""

    if not geometries:
        return None
    items = list(geometries.items())
    for slug, geometry in reversed(items):
        lowered = slug.lower()
        if any(keyword in lowered for keyword in FINAL_GEOMETRY_KEYWORDS):
            return geometry
    return items[-1][1]


INITIALIZATION_KEY_ALIASES = {
    "chg": "charge",
    "inferred_charge": "charge",
    "multiplicity": "spin_multiplicity",
    "spin": "spin_multiplicity",
    "runtype": "run_type",
    "runtypes": "run_type",
    "basis_set": "basis",
    "basisset": "basis",
    "basis_sets": "basis",
}


INITIALIZATION_DICTREF_OVERRIDES = {
    "run_type": "cc:runtype",
    "task": "cc:task",
    "method": "cc:method",
    "functional": "cc:functional",
    "basis": "cc:basis",
    "charge": "cc:charge",
    "spin_multiplicity": "cc:spinMultiplicity",
    "temperature": "cc:temperature",
    "pressure": "cc:pressure",
    "optimizer": "cc:optimizer",
}


INITIALIZATION_MULTI_VALUE_KEYS = {"basis"}


def normalize_metadata_key(name: str) -> str:
    normalized = name.lower().replace("-", "_")
    return INITIALIZATION_KEY_ALIASES.get(normalized, normalized)


def initialization_dict_ref(normalized_key: str) -> str:
    override = INITIALIZATION_DICTREF_OVERRIDES.get(normalized_key)
    if override:
        return override
    slug = slugify(normalized_key).replace("-", "_")
    return f"uma:{slug or 'value'}"


def build_cml_document(data: LogData) -> ElementTree:
    root_attrs = {
        **ROOT_NAMESPACE_ATTRS,
        "id": f"{data.source.stem}-cml",
        "convention": "convention:compchem",
    }
    root = Element("module", root_attrs)
    job_list = SubElement(root, "module", {"dictRef": "cc:jobList", "id": "jobList1"})
    job_id = "job1"
    job_title = determine_job_title(data)
    job_attrs = {"dictRef": "cc:job", "id": job_id, "title": job_title}
    job = SubElement(job_list, "module", job_attrs)
    set_template_ref(job, "job")

    env_attrs = {
        "dictRef": "cc:environment",
        "id": f"{job_id}-environment",
        "title": f"{job_title} environment",
    }
    env = SubElement(job, "module", env_attrs)
    set_template_ref(env, "environment")
    env_params = SubElement(env, "parameterList")

    def lookup_metadata_value(target_key: str) -> Optional[str]:
        normalized_target = target_key.lower().replace("-", "_")
        for bucket in (data.metadata, data.header_metadata):
            for existing_key, value in bucket.items():
                normalized_existing = existing_key.lower().replace("-", "_")
                if normalized_existing == normalized_target:
                    text = str(value).strip()
                    if text:
                        return text
        return None

    def add_env_parameter(dict_ref: str, value: Optional[str]) -> None:
        text = value.strip() if isinstance(value, str) else value
        add_parameter(env_params, dict_ref, text or PLACEHOLDER_TEXT)

    add_env_parameter("cc:program", lookup_metadata_value("program") or "UMA-ASE")
    add_env_parameter("cc:programVersion", lookup_metadata_value("program_version") or __version__)
    add_env_parameter("cc:programSubversion", lookup_metadata_value("program_subversion"))
    add_env_parameter("cc:programDate", lookup_metadata_value("program_date"))
    add_env_parameter("cc:compileDate", lookup_metadata_value("compile_date"))
    flavour = lookup_metadata_value("program_flavour") or lookup_metadata_value("device")
    add_env_parameter("cc:programFlavour", flavour)
    add_env_parameter("cc:runDate", lookup_metadata_value("run_date") or data.run_start)
    add_env_parameter("cc:title", lookup_metadata_value("title") or job_title)

    init_attrs = {
        "dictRef": "cc:initialization",
        "id": f"{job_id}-initialization",
        "title": f"{job_title} initialization",
    }
    initialization = SubElement(job, "module", init_attrs)
    set_template_ref(initialization, "initialization")
    init_params = SubElement(initialization, "parameterList")
    add_parameter(init_params, "uma:jobIdentifier", job_id)

    consumed_metadata_keys: set[str] = set()

    def consume_key(key: str) -> None:
        consumed_metadata_keys.add(normalize_metadata_key(key))

    def get_core_value(key: str, *, default: Optional[str] = None) -> str:
        consume_key(key)
        return lookup_metadata_value(key) or default or PLACEHOLDER_TEXT

    if data.run_types:
        consume_key("run_type")
        for run_type in data.run_types:
            label = run_type.replace("_", " ").strip() or run_type
            add_parameter(init_params, "cc:runtype", label.upper())
    else:
        add_parameter(init_params, "cc:runtype", PLACEHOLDER_TEXT)

    add_parameter(init_params, "cc:method", get_core_value("method"))
    add_parameter(init_params, "cc:functional", get_core_value("functional"))

    basis_value = lookup_metadata_value("basis") or lookup_metadata_value("basis_set")
    if basis_value:
        consume_key("basis")
        for idx, entry in enumerate(re.split(r",\s*", basis_value)):
            if entry:
                add_parameter(init_params, "cc:basis", entry)
    else:
        add_parameter(init_params, "cc:basis", PLACEHOLDER_TEXT)

    add_parameter(init_params, "cc:charge", get_core_value("charge", default=str(data.header_metadata.get("charge", ""))))
    add_parameter(init_params, "cc:spinMultiplicity", get_core_value("spin_multiplicity", default=str(data.header_metadata.get("spin_multiplicity", ""))))
    add_parameter(init_params, "cc:optimizer", get_core_value("optimizer"))
    add_parameter(init_params, "cc:task", get_core_value("task"))
    add_parameter(init_params, "cc:temperature", get_core_value("temperature", default="298.15"))
    add_parameter(init_params, "cc:pressure", get_core_value("pressure", default="101325"))

    metadata_module = SubElement(
        initialization,
        "module",
        {
            "dictRef": "cc:userDefinedModule",
            "id": f"{job_id}-initialization-metadata",
        },
    )
    set_template_ref(metadata_module, "parameters")
    metadata_params = SubElement(metadata_module, "parameterList")

    def add_remaining_metadata(items: Dict[str, str]) -> None:
        for key, value in sorted(items.items()):
            normalized_key = normalize_metadata_key(key)
            if normalized_key in consumed_metadata_keys or normalized_key == "element_counts":
                continue
            if isinstance(value, str) and not value.strip():
                continue
            dict_ref = initialization_dict_ref(normalized_key)
            add_parameter(metadata_params, dict_ref, value)
            consumed_metadata_keys.add(normalized_key)

    add_remaining_metadata(data.metadata)
    add_remaining_metadata(data.header_metadata)

    if data.element_counts:
        counts_list = SubElement(initialization, "list", {"dictRef": "uma:elementCounts"})
        for element, count in sorted(data.element_counts.items()):
            scalar = SubElement(
                counts_list,
                "scalar",
                {
                    "dictRef": "uma:elementCount",
                    "title": element,
                    "dataType": "xsd:integer",
                },
            )
            scalar.text = str(count)

    initial_geometry = select_initial_geometry(data.geometries)
    final_geometry = select_final_geometry(data.geometries)
    if initial_geometry:
        add_molecule(initialization, f"{job_id}-init-geom", initial_geometry)

    calculation_attrs = {
        "dictRef": "cc:calculation",
        "id": f"{job_id}-calculation",
        "title": f"{job_title} calculation",
    }
    calculation = SubElement(job, "module", calculation_attrs)
    set_template_ref(calculation, "calculation")
    calc_user = SubElement(
        calculation,
        "module",
        {
            "dictRef": "cc:userDefinedModule",
            "id": f"{job_id}-calculation-results",
        },
    )
    set_template_ref(calc_user, "results")
    property_list = SubElement(calc_user, "propertyList")

    if data.run_types:
        run_list = SubElement(property_list, "property", {"dictRef": "uma:runTypes"})
        array = SubElement(run_list, "array", {"dataType": "xsd:string", "size": str(len(data.run_types))})
        array.text = " ".join(data.run_types)

    geom_index = 1
    for geometry in data.geometries.values():
        if final_geometry and geometry is final_geometry:
            continue
        molecule_id = f"geom{geom_index:02d}"
        geom_index += 1
        add_molecule(calc_user, molecule_id, geometry)

    if data.optimization_steps:
        history = SubElement(calc_user, "list", {"dictRef": "uma:optimizationHistory"})
        for step in data.optimization_steps:
            entry = SubElement(history, "list", {"dictRef": "uma:optimizationStep"})
            for dict_ref, value in (
                ("uma:optimizer", step.optimizer),
                ("uma:step", step.step),
                ("uma:time", step.time),
                ("uma:energy", step.energy),
                ("uma:fmax", step.fmax),
            ):
                scalar_attrs = {"dictRef": dict_ref}
                if isinstance(value, (int, float)):
                    scalar_attrs["dataType"] = "xsd:double" if isinstance(value, float) else "xsd:integer"
                    scalar = SubElement(entry, "scalar", scalar_attrs)
                    scalar.text = format_float(value) if isinstance(value, float) else str(value)
                else:
                    scalar_attrs["dataType"] = "xsd:string"
                    scalar = SubElement(entry, "scalar", scalar_attrs)
                    scalar.text = str(value)

    finalization_attrs = {
        "dictRef": "cc:finalization",
        "id": f"{job_id}-finalization",
        "title": f"{job_title} finalization",
    }
    finalization = SubElement(job, "module", finalization_attrs)
    set_template_ref(finalization, "finalization")
    if final_geometry:
        add_molecule(finalization, f"{job_id}-final-geom", final_geometry)
    final_property_list = SubElement(finalization, "propertyList")
    add_property(final_property_list, "cc:cputime", PLACEHOLDER_TEXT)
    add_property(final_property_list, "cc:systemtime", PLACEHOLDER_TEXT)
    add_property(final_property_list, "cc:elapsedtime", PLACEHOLDER_TEXT)
    if "potential" in data.energies:
        add_property(final_property_list, "cc:potentialEnergy", data.energies["potential"], units="eV")
    if "total" in data.energies:
        add_property(final_property_list, "cc:totalEnergy", data.energies["total"], units="eV")
    if data.sum_atomic_energies is not None:
        add_property(final_property_list, "uma:sumAtomicEnergy", data.sum_atomic_energies, units="eV")
    if data.bonding_energy_ev is not None:
        add_property(final_property_list, "uma:bondingEnergy", data.bonding_energy_ev, units="eV")
    if data.bonding_energy_kcal is not None:
        add_property(final_property_list, "uma:bondingEnergy", data.bonding_energy_kcal, units="kcal.mol-1")
    if data.rmsd is not None:
        add_property(final_property_list, "uma:rmsd", data.rmsd, units="angstrom")
    if data.zero_point_energy is not None:
        add_property(final_property_list, "uma:zeroPointEnergy", data.zero_point_energy, units="eV")

    for element, value in sorted(data.atomic_energies.items()):
        add_property(final_property_list, "uma:atomicEnergy", value, title=element, units="eV")

    if data.frequencies or data.mode_displacements:
        modes = SubElement(final_property_list, "list", {"dictRef": "cc:vibrationalSpectrum"})
        if data.frequencies:
            indices = [mode.index for mode in data.frequencies]
            energies = [mode.energy_mev for mode in data.frequencies]
            wavenumbers = [mode.wavenumber_cm1 for mode in data.frequencies]
            imaginaries = [mode.imaginary for mode in data.frequencies]
            add_array(modes, "uma:modeIndex", indices, data_type="xsd:integer")
            add_array(modes, "uma:energy", energies, data_type="xsd:double", units="meV")
            add_array(modes, "cc:frequency", wavenumbers, data_type="xsd:double", units="cm-1")
            add_array(modes, "uma:imaginary", imaginaries, data_type="xsd:boolean")
        if data.mode_displacements:
            element_types = [row.symbol for row in data.mode_displacements]
            flattened_displacements = [
                value for row in data.mode_displacements for value in row.displacements
            ]
            add_array(modes, "cc:elementType", element_types, data_type="xsd:string")
            add_array(
                modes,
                "cc:displacement",
                flattened_displacements,
                data_type="xsd:double",
                units="angstrom",
            )

    final_user_module = SubElement(
        finalization,
        "module",
        {
            "dictRef": "cc:userDefinedModule",
            "id": f"{job_id}-finalization-metadata",
        },
    )
    set_template_ref(final_user_module, "otherComponents")
    final_params = SubElement(final_user_module, "parameterList")
    add_parameter(final_params, "uma:sourceLog", str(data.source), title="Source log file")

    if data.enthalpy_components or data.entropy_components or data.free_energy_components:
        final_user_property_list = SubElement(final_user_module, "propertyList")
        if data.enthalpy_components:
            enthalpy_dict_map = {
                "E_pot": "cc:eener",
                "E_ZPE": "cc:zeropoint",
            }
            add_list_with_scalars(
                final_user_property_list,
                "uma:enthalpyComponents",
                [(c.label, c.value, c.unit) for c in data.enthalpy_components],
                element_title="uma:enthalpyTerm",
                dict_ref_mapper=lambda title: enthalpy_dict_map.get(title),
            )
        add_entropy_list(final_user_property_list, data.entropy_components)
        if data.free_energy_components:
            add_list_with_scalars(
                final_user_property_list,
                "uma:freeEnergyComponents",
                [(c.label, c.value, c.unit) for c in data.free_energy_components],
                element_title="uma:freeEnergyTerm",
            )

    indent(root)
    return ElementTree(root)


def indent(element: Element, level: int = 0) -> None:
    """Apply indentation to XML output for readability."""

    indent_str = "\n" + level * "  "
    if len(element):
        if not element.text or not element.text.strip():
            element.text = indent_str + "  "
        for child in element:
            indent(child, level + 1)
        if not element.tail or not element.tail.strip():
            element.tail = indent_str
    else:
        if level and (not element.tail or not element.tail.strip()):
            element.tail = indent_str


def convert_log(path: Path, output_path: Optional[Path] = None) -> Path:
    """Parse *path* and emit a CML file."""

    data = UmaLogParser(path).parse()
    tree = build_cml_document(data)
    destination = output_path or path.with_suffix(".xml")
    destination.parent.mkdir(parents=True, exist_ok=True)
    tree.write(destination, encoding="utf-8", xml_declaration=True)
    return destination


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Convert UMA ASE logs to CML XML files.")
    parser.add_argument("logs", nargs="+", help="Paths to UMA ASE log files")
    parser.add_argument("-o", "--output-dir", help="Directory where XML files will be written")
    args = parser.parse_args(argv)

    output_dir = Path(args.output_dir).expanduser() if args.output_dir else None
    status = 0
    for log_path_str in args.logs:
        log_path = Path(log_path_str).expanduser()
        if not log_path.is_file():
            print(f"[uma-ase-cml] Log file not found: {log_path}")
            status = 1
            continue
        destination = output_dir / f"{log_path.stem}.xml" if output_dir else log_path.with_suffix(".xml")
        try:
            convert_log(log_path, destination)
            print(f"[uma-ase-cml] Wrote {destination}")
        except Exception as exc:  # pragma: no cover - defensive
            print(f"[uma-ase-cml] Failed to convert {log_path}: {exc}")
            status = 1
    return status


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
