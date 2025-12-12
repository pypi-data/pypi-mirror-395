import numpy as np

def read_xyz(filename):
    """Reads coordinates from an XYZ file (ignores atom types)."""
    with open(filename, 'r') as f:
        lines = f.readlines()[2:]  # skip first two lines (count + comment)
    coords = []
    for line in lines:
        parts = line.split()
        if len(parts) >= 4:
            coords.append([float(parts[1]), float(parts[2]), float(parts[3])])
    return np.array(coords)

def kabsch(P, Q):
    """
    Perform the Kabsch algorithm to find the optimal rotation matrix
    that minimizes RMSD between P and Q.
    P and Q must be centered (mean removed).
    """
    C = np.dot(P.T, Q)
    V, S, W = np.linalg.svd(C)
    d = (np.linalg.det(V) * np.linalg.det(W)) < 0.0
    if d:
        V[:, -1] = -V[:, -1]
    return np.dot(V, W)

def rmsd(P, Q):
    """Compute RMSD between two sets of points after optimal superposition."""
    P = np.array(P)
    Q = np.array(Q)
    # Center coordinates
    P -= P.mean(axis=0)
    Q -= Q.mean(axis=0)
    # Optimal rotation
    U = kabsch(P, Q)
    P_rot = np.dot(P, U)
    diff = P_rot - Q
    return np.sqrt((diff * diff).sum() / len(P))

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python rmsd.py file1.xyz file2.xyz")
        sys.exit(1)

    xyz1 = read_xyz(sys.argv[1])
    xyz2 = read_xyz(sys.argv[2])

    if xyz1.shape != xyz2.shape:
        print("Error: files have different number of atoms.")
        sys.exit(1)

    value = rmsd(xyz1, xyz2)
    print(f"RMSD: {value:.4f} Å")

