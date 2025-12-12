import subprocess
import glob
import os
import sys

if len(sys.argv) != 2:
    print("Usage: python3 driver.py /path/to/xyz_files_directory")
    sys.exit(1)

xyz_dir = sys.argv[1]

if not os.path.isdir(xyz_dir):
    print(f"Error: {xyz_dir} is not a valid directory")
    sys.exit(1)

# Find all XYZ files in the directory
files = glob.glob(os.path.join(xyz_dir, "*.xyz"))

# Pair files with their corresponding "-geoopt-OPT.xyz"
file_pairs = []
for f in files:
    if "-geoopt-OPT" not in f:
        basename = os.path.basename(f)
        opt_file = os.path.join(xyz_dir, basename.replace(".xyz", "-geoopt-OPT.xyz"))
        if opt_file in files:
            file_pairs.append((f, opt_file))

if not file_pairs:
    print("No valid file pairs found in the directory.")
    sys.exit(1)

output_file = "compiled_rmsd_results.txt"

with open(output_file, "w") as out:
    out.write("=== RMSD Analysis Results ===\n\n")

    for f1, f2 in file_pairs:
        out.write(f"File pair: {os.path.basename(f1)}  vs  {os.path.basename(f2)}\n")
        out.write("-" * 60 + "\n")

        # Run rmsd.py
        out.write("--- rmsd.py output ---\n")
        try:
            result_rmsd = subprocess.run(
                ["python3", "rmsd.py", f1, f2],
                capture_output=True, text=True, check=True
            )
            out.write(result_rmsd.stdout + "\n")
        except subprocess.CalledProcessError as e:
            out.write(f"Error running rmsd.py: {e}\n\n")

        # Run rmsd_dist-angles_ranking_hetero-cutoff.py
        out.write("--- rmsd_dist-angles_ranking_hetero-cutoff.py output ---\n")
        try:
            result_hetero = subprocess.run(
                ["python3", "rmsd_dist-angles_ranking_hetero-cutoff.py", f1, f2],
                capture_output=True, text=True, check=True
            )
            out.write(result_hetero.stdout + "\n")
        except subprocess.CalledProcessError as e:
            out.write(f"Error running rmsd_dist-angles_ranking_hetero-cutoff.py: {e}\n\n")

        out.write("\n" + "="*80 + "\n\n")

print(f"Compiled RMSD results written to {output_file}")


