import numpy as np
import itertools

def read_xyz(filename):
    """Reads atom types and coordinates from an XYZ file."""
    with open(filename, 'r') as f:
        lines = f.readlines()[2:]  # skip first two lines (count + comment)
    atoms, coords = [], []
    for line in lines:
        parts = line.split()
        if len(parts) >= 4:
            atoms.append(parts[0])
            coords.append([float(parts[1]), float(parts[2]), float(parts[3])])
    return atoms, np.array(coords)

def distance(a, b):
    return np.linalg.norm(a - b)

def angle(a, b, c):
    """Return angle (in radians) between vectors ba and bc."""
    v1 = a - b
    v2 = c - b
    cosang = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
    cosang = np.clip(cosang, -1.0, 1.0)
    return np.arccos(cosang)

def find_bonds(coords, atoms):
    """Find bonded pairs using element-dependent distance cutoffs."""
    special = {"P", "Si", "Al", "Sn", "Sb", "W", "Mo", "V", "Te", "Mn", "Zn"}
    bonds = []
    n = len(coords)
    for i in range(n):
        for j in range(i + 1, n):
            cutoff = 2.8 if atoms[i] in special or atoms[j] in special else 1.6
            if distance(coords[i], coords[j]) <= cutoff:
                bonds.append((i, j))
    return bonds

def find_angles(bonds):
    """Find triplets (i, j, k) where j is central atom bonded to i and k."""
    neighbors = {}
    for i, j in bonds:
        neighbors.setdefault(i, []).append(j)
        neighbors.setdefault(j, []).append(i)
    angles = []
    for j, neigh in neighbors.items():
        for i, k in itertools.combinations(neigh, 2):
            angles.append((i, j, k))
    return angles

def rms(values1, values2):
    diff = np.array(values1) - np.array(values2)
    return np.sqrt(np.mean(diff**2))

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python rms_bonds_angles.py file1.xyz file2.xyz")
        sys.exit(1)

    atoms1, coords1 = read_xyz(sys.argv[1])
    atoms2, coords2 = read_xyz(sys.argv[2])

    if coords1.shape != coords2.shape:
        print("Error: files have different number of atoms.")
        sys.exit(1)

    # Bond detection with heterogeneous cutoffs
    bonds = find_bonds(coords1, atoms1)
    angles = find_angles(bonds)

    print(f"Found {len(bonds)} bonds and {len(angles)} angles (bonded triplets only).")

    # Distances
    dist1 = [distance(coords1[i], coords1[j]) for i, j in bonds]
    dist2 = [distance(coords2[i], coords2[j]) for i, j in bonds]
    dist_diff = np.abs(np.array(dist1) - np.array(dist2))
    dist_rms = rms(dist1, dist2)

    # Angles
    ang1 = [angle(coords1[i], coords1[j], coords1[k]) for i, j, k in angles]
    ang2 = [angle(coords2[i], coords2[j], coords2[k]) for i, j, k in angles]
    ang_diff = np.abs(np.array(ang1) - np.array(ang2))
    ang_rms = rms(ang1, ang2)

    print(f"\nDistance RMSD: {dist_rms:.4f} Å")
    print(f"Angle RMSD: {np.degrees(ang_rms):.4f} degrees\n")

    # Sort and extract top 10 most divergent bonds and angles
    top_bonds_idx = np.argsort(-dist_diff)[:10]
    top_angles_idx = np.argsort(-ang_diff)[:10]

    # Print top 10 divergent bonds
    print("=== Top 10 Most Divergent Bonds ===")
    print("i   j   atoms(i-j)   dist1(Å)   dist2(Å)   Δ(Å)")
    print("-" * 60)
    for idx in top_bonds_idx:
        i, j = bonds[idx]
        print(f"{i+1:<3} {j+1:<3} {atoms1[i]}-{atoms1[j]:<6} "
              f"{dist1[idx]:8.4f} {dist2[idx]:8.4f} {dist_diff[idx]:8.4f}")

    # Print top 10 divergent angles
    print("\n=== Top 10 Most Divergent Angles ===")
    print("i   j   k   atoms(i-j-k)   angle1(°)   angle2(°)   Δ(°)")
    print("-" * 75)
    for idx in top_angles_idx:
        i, j, k = angles[idx]
        print(f"{i+1:<3} {j+1:<3} {k+1:<3} "
              f"{atoms1[i]}-{atoms1[j]}-{atoms1[k]:<8} "
              f"{np.degrees(ang1[idx]):8.2f} {np.degrees(ang2[idx]):8.2f} "
              f"{np.degrees(ang_diff[idx]):8.2f}")
