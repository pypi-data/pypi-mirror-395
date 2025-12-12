import re
import os
import pandas as pd
import matplotlib.pyplot as plt
import sys


def normalize_bond(atom_pair):
    a, b = atom_pair.split('-')
    return '-'.join(sorted([a, b]))


def normalize_angle(angle_triplet):
    parts = angle_triplet.split('-')
    if len(parts) != 3:
        return angle_triplet
    a, b, c = parts
    if a == c:
        return f"{a}-{b}-{c}"
    return f"{a}-{b}-{c}" if (a, b, c) <= (c, b, a) else f"{c}-{b}-{a}"


def parse_rmsd_report(filename):
    with open(filename, "r") as f:
        text = f.read()

    # Split by file pair blocks
    blocks = re.split(r'File pair:\s*', text)[1:]

    bond_records, angle_records = [], []

    for block in blocks:
        # Get file pair name
        m_pair = re.match(r'([^\n]+?)\s+vs\s+([^\n]+)', block)
        if not m_pair:
            continue
        file_pair = f"{m_pair.group(1).strip()} vs {m_pair.group(2).strip()}"

        # --- Bonds ---
        bond_match = re.search(r"=== Top 10 Most Divergent Bonds ===(.*?)=== Top 10 Most Divergent Angles ===", block, re.S)
        if bond_match:
            lines = [l.strip() for l in bond_match.group(1).splitlines() if l.strip()]
            for l in lines:
                # Skip headers
                if l.startswith("i") or l.startswith("-"):
                    continue
                cols = re.split(r"\s+", l)
                if len(cols) >= 6:
                    atom_pair = cols[2]
                    try:
                        delta = float(cols[-1])
                    except ValueError:
                        continue
                    bond_records.append({
                        "file_pair": file_pair,
                        "bond_type": normalize_bond(atom_pair),
                        "delta": delta
                    })

        # --- Angles ---
        angle_match = re.search(r"=== Top 10 Most Divergent Angles ===(.*?)(?:=+|$)", block, re.S)
        if angle_match:
            lines = [l.strip() for l in angle_match.group(1).splitlines() if l.strip()]
            for l in lines:
                if l.startswith("i") or l.startswith("-"):
                    continue
                cols = re.split(r"\s+", l)
                if len(cols) >= 7:
                    atom_triplet = cols[3]
                    try:
                        delta = float(cols[-1])
                    except ValueError:
                        continue
                    angle_records.append({
                        "file_pair": file_pair,
                        "angle_type": normalize_angle(atom_triplet),
                        "delta": delta
                    })

    return pd.DataFrame(bond_records), pd.DataFrame(angle_records)


# -----------------------
# Helper: clean label text
# -----------------------
def clean_filename(file_pair):
    """Return the first file name (without .xyz extension) from a file pair string."""
    first_file = file_pair.split(" vs ")[0].strip()
    base = os.path.basename(first_file)
    return base.replace(".xyz", "")


def make_plots(bonds_df, angles_df):
    # --- Top 25 bonds ---
    top_bonds = bonds_df.sort_values("delta", ascending=False).head(25)
    bond_labels = top_bonds.apply(
        lambda row: f"{row['bond_type']} ({clean_filename(row['file_pair'])})", axis=1
    )

    plt.figure(figsize=(12, max(8, len(top_bonds) * 0.4)))  # dynamic height
    plt.barh(range(len(top_bonds)), top_bonds["delta"], color="steelblue")
    plt.yticks(range(len(top_bonds)), bond_labels, fontsize=9)
    plt.xlabel("Δ (Å)")
    plt.ylabel("Bond (File)")
    plt.title("Top 25 Most Divergent Bonds (Global)")
    plt.gca().invert_yaxis()
    plt.subplots_adjust(left=0.35, right=0.95, top=0.9, bottom=0.05)
    plt.savefig("top25_bonds.png", dpi=300)
    plt.close()

    # --- Top 25 angles ---
    top_angles = angles_df.sort_values("delta", ascending=False).head(25)
    angle_labels = top_angles.apply(
        lambda row: f"{row['angle_type']} ({clean_filename(row['file_pair'])})", axis=1
    )

    plt.figure(figsize=(12, max(8, len(top_angles) * 0.4)))
    plt.barh(range(len(top_angles)), top_angles["delta"], color="darkorange")
    plt.yticks(range(len(top_angles)), angle_labels, fontsize=9)
    plt.xlabel("Δ (°)")
    plt.ylabel("Angle (File)")
    plt.title("Top 25 Most Divergent Angles (Global)")
    plt.gca().invert_yaxis()
    plt.subplots_adjust(left=0.35, right=0.95, top=0.9, bottom=0.05)
    plt.savefig("top25_angles.png", dpi=300)
    plt.close()

    # --- Bond histogram ---
    plt.figure(figsize=(10, 6))
    bonds_df["bond_type"].value_counts().plot(kind="bar")
    plt.xlabel("Bond Type")
    plt.ylabel("Count")
    plt.title("Bond Type Occurrences")
    plt.tight_layout()
    plt.savefig("bond_type_histogram.png", dpi=300)
    plt.close()

    # --- Angle histogram ---
    plt.figure(figsize=(10, 6))
    angles_df["angle_type"].value_counts().plot(kind="bar")
    plt.xlabel("Angle Type")
    plt.ylabel("Count")
    plt.title("Angle Type Occurrences")
    plt.tight_layout()
    plt.savefig("angle_type_histogram.png", dpi=300)
    plt.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python rmsd_parser_and_plots.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    bonds_df, angles_df = parse_rmsd_report(input_file)

    print(f"✅ Parsed {len(bonds_df)} bond lines and {len(angles_df)} angle lines")
    make_plots(bonds_df, angles_df)
    print("✅ Plots saved: top25_bonds.png, top25_angles.png, bond_type_histogram.png, angle_type_histogram.png")

