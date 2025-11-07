from pathlib import Path

a0 = 3.552876161  
pseudopot = "C.pbesol-n-kjpaw_psl.1.0.0.UPF"
ecutwfc = 40   #incrase this by 1.3 when necessary
ecutrho = 325  #increase this by 1.3 when necessary
kmesh = (8,8,8)

deltas = [-0.010, -0.0075, -0.005, -0.0025, 0.0025, 0.005, 0.0075, 0.010]

base = Path("./diamond_elastic_inputs_relaxed")
(base / "hydro").mkdir(parents=True, exist_ok=True)
(base / "ortho").mkdir(parents=True, exist_ok=True)
(base / "shear").mkdir(parents=True, exist_ok=True)

header = f"""&CONTROL
  calculation   = 'relax',
  prefix        = 'diamond',
  outdir        = './out',
  pseudo_dir    = './PseudoPotential',
  tstress       = .true.,
  tprnfor       = .true.,
  verbosity     = 'high'
/
&SYSTEM
  ibrav    = 0,
  nat      = 8, 
  ntyp = 1,
  ecutwfc  = {ecutwfc},
  ecutrho  = {ecutrho},
  occupations = 'fixed'
/
&ELECTRONS
   electron_maxstep = 300
   mixing_beta      = 0.7
   scf_must_converge = .TRUE.
/
&IONS
  ion_dynamics = 'bfgs'
/
&CELL
  cell_dofree = 'none'   ! keep strained cell fixed; relax atoms only
/
ATOMIC_SPECIES
  C 12.011 {pseudopot}

K_POINTS automatic
  {kmesh[0]} {kmesh[1]} {kmesh[2]} 0 0 0
"""

atoms = [
               ( 0.8882191550,        0.8882191550,        0.8882191550),
               ( 0.0000000000,        0.0000000000,        0.0000000000),
               ( 0.8882191550,        2.6646570058,        2.6646570058),
               ( 0.0000000000,        1.7764380804,        1.7764380804),
               ( 2.6646570058,        0.8882191550,        2.6646570058),
               ( 1.7764380804,        0.0000000000,        1.7764380804),
               ( 2.6646570058,        2.6646570058,        0.8882191550),
               ( 1.7764380804,        1.7764380804,        0.0000000000),
]

def atoms_block():
    s = "ATOMIC_POSITIONS angstrom\n"
    for x,y,z in atoms:
        s += f"  C {x:10.10f} {y:10.10f} {z:10.10f}\n"
    return s

def write_input(path, cell, delta):
    cell_str = "CELL_PARAMETERS angstrom\n" + \
               f"  {cell[0][0]:.10f} {cell[0][1]:.10f} {cell[0][2]:.10f}\n" + \
               f"  {cell[1][0]:.10f} {cell[1][1]:.10f} {cell[1][2]:.10f}\n" + \
               f"  {cell[2][0]:.10f} {cell[2][1]:.10f} {cell[2][2]:.10f}\n"
    fname = path / f"in_relax_delta_{delta:+.4f}.in"
    with open(fname, "w") as f:
        f.write(header)
        f.write("\n")
        f.write(cell_str)
        f.write("\n")
        f.write(atoms_block())
    return fname

generated = []

for d in deltas:
    # Hydrostatic: scale all three
    s = 1.0 + d
    cell_h = [[s*a0, 0, 0],[0, s*a0, 0],[0,0,s*a0]]
    generated.append(write_input(base/"hydro", cell_h, d))

    # Orthorhombic: (1+d, 1-d, 1)
    cell_o = [[(1+d)*a0, 0, 0],[0,(1-d)*a0,0],[0,0,a0]]
    generated.append(write_input(base/"ortho", cell_o, d))

    # Shear xy: b' = b + d a
    cell_s = [[a0, 0, 0],[d*a0, a0, 0],[0,0,a0]]
    generated.append(write_input(base/"shear", cell_s, d))

# Helper README
readme = base / "README_relaxed.txt"
readme.write_text(f"""Diamond elastic constants by energy–strain (RELAXED-ION) in QE
=================================================================
- This set uses calculation='relax' with fixed strained cells (cell_dofree='none').
- After each run, take the FINAL total energy for the fitted curves.
- Create CSVs hydro.csv, ortho.csv, shear.csv with columns: delta,energy_ryd
  (energies per cell, in Ry), then use:
    python fit_elastic_constants.py --a0 {a0} --hydro hydro.csv --ortho ortho.csv --shear shear.csv
""")

(str(base), len(generated))

