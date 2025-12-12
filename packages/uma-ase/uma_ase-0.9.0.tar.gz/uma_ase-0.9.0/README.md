# uma-ase

uma-ase bundles UMA (Universal Model for Atoms (https://huggingface.co/facebook/UMA) machine-learned force-field (MLFF) with the Atomic Simulation Environment (ASE) methods (https://ase-lib.org/). It supports basic single-point energy calculations, geometry optimisation, vibrational/thermochemical analysis, and transition-state searches via ASE's dimer algorithm from a single command-line entry point or an optional web GUI service. The Webapp GUI provides wide support for running Molecular Dynamics simulations and visualization. 

## Requirements

The project currently ships and has been validated with Python 3.12. The runtime stack is:

- Python ≥ 3.10 (tested with 3.12)
- ASE ≥ 3.26.0
- numpy ≥ 2.2
- torch ≥ 2.6
- fairchem-core ≥ 2.10 for UMA checkpoints and calculators
- flask ≥ 3.0 when you want the optional web GUI

Install these packages with:

```bash
pip install -r requirements.txt
```

If you build your own environment, make sure `fairchem` is present—all calculations rely on it to compute per-atom reference energies. On Apple Silicon you may also want to limit OpenMP threads when driving torch (e.g. `export OMP_NUM_THREADS=1`) to avoid shared-memory warnings.

## Installation

### Released package
```bash
pip install uma-ase[server]
```
The `server` extra installs the optional GUI web interface. Omit it when you only need the command-line tooling. Afterwards, install FairChem explicitly if your environment does not already ship it:

```bash
pip install fairchem-core
```
FairChem is repidly evolving. Check version changes and compatibility with uma-ase.

### From source
```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install -e ".[server]"
```
The editable install registers the `uma-ase` and `uma-ase-server` console scripts for local development.

## Configuration

Some environment variables you may consider to set up:

- FairChem’s UMA models can be loaded directly from the official distribution (see the FairChem/UMA website). You can download the checkpoint files yourself for extra stability and keep them wherever you prefer. Point the shell environment variable `UMA_CUSTOM_CHECKPOINT_DIR` at your directory so `-mlff-chk uma-s-1p1` and similar shortcuts resolve against your local files.
If the variable is unset, uma-ase looks for online HuggingFace access or checkpoints under `~/.uma_ase/checkpoints`.
- When using the Webapp, each run stores the returned log & files under `~/.uma_ase/results/` (configurable via `UMA_RESULTS_DIR`). The web interface enables a *Download Log* button once a job finishes. The CLI writes all files in the same place where the input file resides.



## Command-line (CLI) usage


- **Installed via pip (PyPI, wheel, or editable install)**
  ```bash
  # Set up where your local checkpoint UMA MLFF files are located.  
  export UMA_CUSTOM_CHECKPOINT_DIR=/abs/path/to/checkpoints
  (include this your .bashrc or .bash_profile conf files).

  # Single run
  uma-ase -input geometry.xyz -chg 0 -spin 1 -run-type sp
  ```

- **Working from a cloned repository without installing**
  ```bash
  export PYTHONPATH=src
  python -m uma_ase.py -input geometry.xyz -chg 0 -spin 1 -run-type geoopt
  ```

The CLI always emits a consolidated log (e.g. `molecule-SP-OPT.log`), a trajectory (`*.traj`), an optimised XYZ (`*-geoopt-OPT.xyz`), and vibrational normal modes outputs. Run `uma-ase -h` (or `python -m uma_ase.cli -h`) for the full reference.

**IMPORTANT NOTE**

When an XYZ comment line embeds an string and two signed integers (e.g. `https://… -1 2`), uma-ase reads them before invoking ASE and uses the first as the default charge and the optional second one as the default spin multiplicity, unless you supplied `-chg`/`-spin` explicitly.

**CLI option summary**
- `-input` *(required)*: input geometry file readable by ASE, typically `.xyz`. A standard XYZ can omit `-chg`/`-spin` when the second-line comment ends with signed integers (optionally alongside a source URL), e.g.  
  ```
  199
  https://iochem-bd.iciq.es/browse/handle/100/69781 -1 2
  O  0.0 0.0 0.0
  H  0.0 0.0 0.96
  H  0.0 0.75 -0.48
  C .....
  ```
  uma-ase reads the charge `-1` and spin `2` before invoking ASE and adopts them as defaults.
- `-chg` *(default 0)*: total molecular charge; omitted values default to 0 or to the signed integer embedded in the XYZ comment line if present.
- `-spin` *(default 1)*: spin multiplicity; omitted values default to 1 or to the second signed integer embedded in the XYZ comment line when present.
- `-run-type` *(default sp)*: workflow steps to run; choose any sequence of `sp`, `geoopt`, `freqs`, `ts`. A `ts` run first executes a frequency calculation (discarding thermochemistry) to extract the largest negative mode "#0", launches ASE’s dimer method seeded with that mode, and finally recomputes full vibrational data on the converged saddle point.
- `-cpu`: force CPU execution even when CUDA is available (helpful on shared HPC nodes or to avoid GPU startup costs).
- `-iter` *(default 250)*: maximum geometry optimisation cycles.
- `-grad` *(default 0.01 eV/Å)*: convergence threshold on the maximum force component.
- `-optimizer` *(default LBFGS)*: ASE optimiser to use (BFGS, LBFGS, FIRE, BFGSLineSearch, MDMin).
- `--ts-displacement` / `--ts-dimer-separation` / `--ts-trial-step` / `--ts-max-step` / `--ts-max-rot`: tune the initial mode displacement and dimer parameters used by the `ts` workflow. These settings also control the preparatory and final frequency calculations, so every TS run delivers both the dimer trajectory and the validated saddle-point frequencies in a single invocation.
- `-mlff-chk` *(default uma-s-1p1)*: UMA checkpoint identifier.
- `-mlff-task` *(default omol)*: UMA task/model name passed to the calculator.
- `-temp`/`--temperature` *(default 298.15 K)*: vibrational/thermochemistry temperature.
- `-press`/`--pressure` *(default 101325 Pa)*: vibrational/thermochemistry pressure.
- `-visualize`: open the geoopt trajectory in ASE’s viewer after completion.

**CLI help (`uma-ase -h`)**
```text
usage: uma-ase [-h] -input INPUT [-chg CHG] [-spin SPIN]
               [-run-type {sp,geoopt,freqs,ts} [{sp,geoopt,freqs,ts} ...]] [-cpu]
               [-iter ITER] [-grad GRAD] [-optimizer NAME]
               [-mlff-chk CHECKPOINT] [-mlff-task TASK] [-temp T]
               [-press P] [-visualize]

Provide the required -input value. Charge defaults to 0 (or the first signed
integer embedded in the XYZ comment line) and spin defaults to 1 (or the second
integer when present).

options:
  -h, --help            show this help message and exit
  -input INPUT          Input geometry readable by ASE (XYZ comment may append
                        signed charge/spin metadata).
  -chg CHG              Molecular charge override (default 0; inferred from
                        XYZ comment when present).
  -spin SPIN            Spin multiplicity (default 1; inferred from XYZ comment
                        when a second integer is present).
  -run-type {sp,geoopt,freqs,ts} [{sp,geoopt,freqs,ts} ...]
                        Run type(s) to execute: 'sp', 'geoopt', 'freqs',
                        'ts', or any sequence thereof (default: sp).
  -cpu                  Force UMA calculations to run on CPU even when CUDA is
                        available.
  -iter ITER            Max number of geometry optimization cycles.
                        Default=250
  -grad GRAD            Max grad for convergence. Default=0.01 eV/A
  -optimizer NAME       ASE optimizer (e.g. BFGS, LBFGS, FIRE,
                        BFGSLineSearch,MDMin). Default='LBFGS'.
  -mlff-chk CHECKPOINT  UMA checkpoint identifier. Default='uma-s-1p1'.
  -mlff-task TASK       UMA task/model identifier. Default='omol'.
  -temp   T             Temperature in Kelvin for vibrational analysis
                        (default 298.15 K).
  -press   P            Pressure in Pascals for vibrational analysis (default
                        101325.0 Pa).
  -visualize            Open the trajectory of a geoopt run in an interactive
                        viewer.
```

## Webapp interface

If your pip installed the package, launch the command:

```bash
uma-ase-server
```
If working directly from the source tree without installing, then prefix the module path:

```bash
# export PYTHONPATH once,
export PYTHONPATH=src
# then:
python -m uma_ase.server
```

Once the server is up and running, then visit <http://127.0.0.1:8000> using your preferred web browser (tested with Safari, Firefox & Chrome). A webapp is bundled with the package and allows submitting jobs and visualize results. The backend stores each uploaded geometry in a temporary directory, delegates to the CLI, returns the generated log, and removes temporary files automatically. The Webapp page focuses on jobs submission, visualization and analysis, showing live summary of the calculations. CAUTION: Dealing with very big files can cause troubles. Reload the page to reset fields and memory usage.



![uma-ase web interface](./screenshot1.png)
- **Load file tab.** Load a geometry file (`.xyz`, `.pdb`, `.mol`, etc.) from disk or paste an ioChem-BD handle/URL—when you provide a handle, the UI downloads the referenced calculation, parses the XYZ comment line, and pre-populates the charge and spin multiplicity so subsequent tabs inherit the right settings automatically.

![uma-ase web interface](./screenshot2.png)
- **Single Run tab.** Upload one geometry, set charge/spin/run types (sp, geoopt, freqs, ts) and launch a job. The panel streams the full stdout/stderr log, exposes download buttons for log/trajectory/optimized XYZ/FREQS bundles, and once a GeoOpt/TS calculation finishes it automatically switches to the Visualize tab and loads the produced `*.traj` (falling back to the final XYZ if the trajectory is unavailable) so the optimization pathway is ready to inspect without touching the Load File tab.

![uma-ase web interface](./screenshot3.png)
- **Simulate tab.** Reuse the same UMA checkpoints to launch ASE MD jobs by choosing steps, timestep, target temperature, ensemble-specific knobs, and sampling intervals. The UI mirrors the Single Run layout, streams the MD log in real time, and exposes downloads for the trajectory, multi-frame XYZ, and final snapshot once the simulation completes.

![uma-ase web interface](./screenshot4.png)
- **Visualize tab.** Opens first by default so you can inspect structures immediately. The bundled JSmol canvas synchronises with every geometry you upload in Single Run, keeps charge/spin indicators aligned, and still lets you drag-and-drop alternate files straight into the viewer panel. The tab now shares space with a dedicated 3Dmol.js Trajectory Viewer: drag in any `.traj/.xyz/.xyz.gz` file (or let the Single Run workflow auto-load the GeoOpt/TS trajectory when a job ends) and scrub through frames, play/pause, adjust FPS, or capture live MD runs. A *Vibrational Normal Modes* panel accepts the packaged `<input>-FREQS-modes.zip` plus its log file, parses the “Vibrational Summary”, and builds a selector that animates each normal mode as a multi-frame trajectory (palindrome loop) complete with a stop button. When a freqs/TS job finishes, the server auto-downloads the ZIP + log, populates the selectors, reloads the relevant geometry in the viewer, and jumps straight into the Trajectory tab so you can inspect the modes without manual uploads.

![uma-ase web interface](./screenshot5.png)
- **Multi Run tab.** Point at a folder containing multiple `.xyz` files (non-OPT/geoopt names) and the UI builds a summary table with the detected charge/spin for each entry. Choose the shared run settings once, then fan out to as many jobs as needed. The Results panel shows the complete output of every job (including inline download links per file) and a “Download Files” button bundles every artifact from the batch into a single ZIP.

![uma-ase web interface](./screenshot6.png)
- **Analyze tab.** Post-process folders of uma-ase results directly in the browser.
  - *RMSD Report* reads uma-ase `.log` files and generates PDF/LaTeX/DOCX artifacts plus an inline PDF preview powered by `styled_rmsd_report.py`.
  - *XYZ Pair Analysis* drives `scripts-to-share_v2/driver.py`, matching `.xyz` files with their `-geoopt-OPT` counterparts, collecting TXT/PDF/LaTeX/DOCX outputs, and exposing download buttons for each format.

![uma-ase web interface](./screenshot7.png)
![uma-ase web interface](./screenshot8.png)
![uma-ase web interface](./screenshot9.png)

![uma-ase web interface](./screenshot10.png)
- **<About tab>** Point at a folder containing multiple `.xyz` files (non-OPT/geoopt names) and the UI builds a summary table with the detected charge/spin for each entry. Choose the shared run settings once, then fan out to as many jobs as needed. The Results panel shows the complete output of every job (including inline download links per file) and a “Download Files” button bundles every artifact from the batch into a single ZIP.

### Simulate tab (Molecular Dynamics)

The Simulate tab is a front-end for ASE’s molecular dynamics drivers coupled to UMA MLFF calculators. It consumes whichever structure is currently loaded in the Visualize tab and lets you tweak every relevant thermostat/barostat parameter without touching Python. Controls are grouped as follows.

| Section | Options |
| --- | --- |
| **System** | Charge, spin multiplicity, UMA checkpoint (`uma-s-1p1` default), UMA task (`omol` default). |
| **Integrator** | Dynamics engine selector covering `Langevin (NVT)`, `VelocityVerlet (NVE)`, `NVT Berendsen`, `Nosé-Hoover Chain`, `Bussi`, `Andersen`, `Langevin-Hoover BAOAB (NVT/NPT)`, `NPT Berendsen`, `Isotropic MTK`, `Full MTK`, and `Melchionna NPT`. |
| **Core MD settings** | Steps, timestep (fs), target temperature (K), per-engine extras (friction for Langevin, thermostat relaxation for Berendsen). |
| **NPT controls** | Pressure (bar), compressibility (1/bar), barostat relaxation (fs), MTK damping and chain lengths, BAOAB `T_tau`/`P_tau`/cell-mass factor/hydrostatic toggle, Melchionna thermostat time, barostat time, bulk modulus, and mask vector. |
| **PBC / cell** | Checkbox to enable periodic boundary conditions and numeric fields for cell lengths `a/b/c` (Å) plus angles `α/β/γ` (°). When enabled the app scales the uploaded geometry into that lattice before the run. |
| **Sampling** | Trajectory write interval, log interval. |

Each control only appears when relevant (e.g., MTK sliders only unlock when you pick an MTK engine), mirroring ASE’s own API. During a run the Simulate output panel shows a live tail of the job log, and once the job finishes the full log stays visible while the JSmol viewer auto-loads `md-final.xyz`. Download buttons become active for the MD log, ASE `.traj`, multi-frame `.xyz`, and the final snapshot. Any backend error (for example, picking BAOAB when your ASE build predates `ase.md.langevinbaoab`) gets surfaced inline with the current log.

## Package layout

```
src/uma_ase/
├── __init__.py          # Version metadata
├── __main__.py          # Enables `python -m uma_ase`
├── cli.py               # Console entry point
├── server.py            # Flask application (optional)
├── utils.py             # CLI parser and helper utilities
├── workflows.py         # Core UMA/ASE workflow orchestration
└── static/uma-ase.html  # Single-page frontend served by the Flask app
```

## Development workflow

1. Create a virtual environment and install the package in editable mode (`pip install -e .[server]`).
2. Run unit or integration tests as desired (add your preferred framework).
3. Build distributions for publishing:
   ```bash
   python -m build
   ```
4. Upload to a package index:
   - **GitLab Package Registry** (replace `<project-id>` and token accordingly):
     ```bash
     python -m twine upload \
       --repository-url "https://gitlab.com/api/v4/projects/<project-id>/packages/pypi" \
       dist/*
     ```
   - **PyPI**:
     ```bash
     python -m twine upload dist/*
     ```

## License

Copyright (c) Carles Bo. Portions of this code were generated by the ChatGPT Codex agent under the supervision of Carles Bo. The project is distributed under the GNU General Public License v3.0 - see `LICENSE` for details.
 
