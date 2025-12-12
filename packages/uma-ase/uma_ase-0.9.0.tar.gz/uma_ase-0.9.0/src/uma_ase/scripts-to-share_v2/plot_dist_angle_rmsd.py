#!/usr/bin/env python3
import re
import sys
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pathlib import Path

# === INPUT FILES ===
if len(sys.argv) > 1:
    files = sys.argv[1:]
else:
    files = [
        "compiled_rmsd_results_fire.txt",
        "compiled_rmsd_results_lbfgs.txt"
    ]

print(f"📂 Input files: {files}")

# === OUTPUT DIRECTORY ===
output_dir = Path("rmsd_plots")
output_dir.mkdir(exist_ok=True)

data = []
algorithms_order = []

# === PARSE FILES ===
for filename in files:
    if not Path(filename).exists():
        print(f"⚠️ File not found: {filename}")
        continue

    # Detect algorithm name but keep display style
    if re.search(r"fire", filename, flags=re.IGNORECASE):
        algo = "uma-s-1p1 | FIRE"
    elif re.search(r"lbfgs", filename, flags=re.IGNORECASE):
        algo = "uma-s-1p1 | LBFGS"
    else:
        algo = Path(filename).stem

    if algo not in algorithms_order:
        algorithms_order.append(algo)

    print(f"\n📄 Parsing {filename} (algorithm = {algo})")
    text = Path(filename).read_text(errors="ignore")

    sections = re.split(r"File pair:\s*", text, flags=re.IGNORECASE)
    if len(sections) <= 1:
        print("⚠️ No 'File pair:' sections found.")
        continue

    for sec in sections[1:]:
        # Extract first file name before "vs"
        m_name = re.search(r"^(.*?)\.xyz\s+vs", sec, flags=re.IGNORECASE | re.MULTILINE)
        if not m_name:
            continue
        mol_file = m_name.group(1).strip()
        mol = Path(mol_file).stem

        # Distance and Angle RMSD
        m_dist = re.search(r"Distance RMSD:\s*([\d.]+)", sec, flags=re.IGNORECASE)
        m_ang = re.search(r"Angle RMSD:\s*([\d.]+)", sec, flags=re.IGNORECASE)

        if m_dist and m_ang:
            dist_rmsd = float(m_dist.group(1))
            ang_rmsd = float(m_ang.group(1))
            print(f"  ✓ {mol}: Distance={dist_rmsd}, Angle={ang_rmsd}")

            data.append({
                "File": mol,
                "Algorithm": algo,
                "Distance RMSD (Å)": dist_rmsd,
                "Angle RMSD (°)": ang_rmsd
            })
        else:
            print(f"  ⚠️ Skipped {mol} — RMSD values not found")

# === MAKE DATAFRAME ===
df = pd.DataFrame(data)
if df.empty:
    raise ValueError("No data extracted — check your file format and regex patterns!")

# === ALIGN DATA (so molecule order matches across algorithms) ===
dist_pivot = df.pivot_table(index="File", columns="Algorithm", values="Distance RMSD (Å)", aggfunc="first")
ang_pivot = df.pivot_table(index="File", columns="Algorithm", values="Angle RMSD (°)", aggfunc="first")

# Align columns to preserve algorithm order
algos_present = [a for a in algorithms_order if a in dist_pivot.columns or a in ang_pivot.columns]
dist_pivot = dist_pivot.reindex(columns=algos_present)
ang_pivot = ang_pivot.reindex(columns=algos_present)

# Align all file names (union)
files_sorted = sorted(set(dist_pivot.index).union(ang_pivot.index))
dist_pivot = dist_pivot.reindex(index=files_sorted)
ang_pivot = ang_pivot.reindex(index=files_sorted)

# === WARN ABOUT MISSING DATA ===
for algo in algos_present:
    missing_files = dist_pivot.index[dist_pivot[algo].isna() | ang_pivot[algo].isna()]
    if len(missing_files) > 0:
        print(f"⚠️ Missing data for {algo}: {list(missing_files)}")

# === PLOTS ===
bar_width = 0.35
x = np.arange(len(files_sorted))

# --- Distance RMSD ---
plt.figure(figsize=(8, 5))
for i, algo in enumerate(algos_present):
    values = dist_pivot[algo].fillna(0).values
    plt.bar(x + i * bar_width, values, width=bar_width, label=algo)
plt.xticks(x + bar_width / 2, files_sorted, rotation=45, ha="right")
plt.ylabel("Distance RMSD (Å)")
plt.title("Distance RMSD Comparison by Algorithm")
plt.legend()
plt.tight_layout()
distance_plot_path = output_dir / "distance_rmsd_comparison.png"
plt.savefig(distance_plot_path, dpi=300)
plt.close()
print(f"📊 Saved distance RMSD plot to {distance_plot_path}")

# --- Angle RMSD ---
plt.figure(figsize=(8, 5))
for i, algo in enumerate(algos_present):
    values = ang_pivot[algo].fillna(0).values
    plt.bar(x + i * bar_width, values, width=bar_width, label=algo)
plt.xticks(x + bar_width / 2, files_sorted, rotation=45, ha="right")
plt.ylabel("Angle RMSD (°)")
plt.title("Angle RMSD Comparison by Algorithm")
plt.legend()
plt.tight_layout()
angle_plot_path = output_dir / "angle_rmsd_comparison.png"
plt.savefig(angle_plot_path, dpi=300)
plt.close()
print(f"📊 Saved angle RMSD plot to {angle_plot_path}")

print("\n✅ Done — plots aligned and styled like the original version.")


