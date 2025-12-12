from ase import units
import ase.io
from ase.io import read
from ase.io import Trajectory

from ase.md.langevin import Langevin
from ase.visualize import view
from fairchem.core import pretrained_mlip, FAIRChemCalculator

# Read the atoms object from ASE read-able file
atoms = ase.io.read('Mo132.geo_opt_gas.xyz')

# Set the total charge and spin multiplicity if using the OMol task
atoms.info["charge"] = -12
atoms.info["spin"] = 1
view(atoms)
print("Initial Geometry")

# Set up the calculator
predictor = pretrained_mlip.get_predict_unit('uma-sm', device='cpu')
atoms.calc = FAIRChemCalculator(predictor, task_name='omol')

#Initialize MD
dyn = Langevin(
    atoms,
    timestep=0.1 * units.fs,
    temperature_K=400,
    friction=0.000 / units.fs
)
trajectory = Trajectory("my_md.traj", "w", atoms)
dyn.attach(trajectory.write, interval=1)

print("Running MD")

dyn.run(steps=500)

print("MD Finished")
print("Trajectory in my_md.traj / Check results in output.log")

# Visualize the trajectory interactively
# Read trajectory file (supports formats like .traj, .xyz, .extxyz, etc.)
traj = read(filename="my_md.traj", index=':')  # ':' reads all frames
view(traj)
