Diamond elastic constants by energy–strain (RELAXED-ION) in QE
=================================================================
- This set uses calculation='relax' with fixed strained cells (cell_dofree='none').
- After each run, take the FINAL total energy for the fitted curves.
- Create CSVs hydro.csv, ortho.csv, shear.csv with columns: delta,energy_ryd
  (energies per cell, in Ry), then use:
    python fit_elastic_constants.py --a0 3.552876161 --hydro hydro.csv --ortho ortho.csv --shear shear.csv
