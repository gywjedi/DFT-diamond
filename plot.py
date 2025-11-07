#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Plot precomputed ΔE/V₀ vs δ² for Hydro, Ortho, and Shear strain paths.
Uses LaTeX rendering for publication-quality figures.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ==============================
# USER PARAMETERS
# ==============================
use_latex = True          # Set False if no LaTeX installed
title_prefix = "Diamond"
save_format = "png"       # png or pdf

# File names (CSV with columns: delta, energy_density_GPa)
files = {
    "Hydro": "hydro.csv",
    "Ortho": "ortho.csv",
    "Shear": "shear.csv"
}

# ==============================
# MATPLOTLIB SETTINGS
# ==============================
if use_latex:
    plt.rcParams.update({
        "text.usetex": True,
        "font.family": "serif",
        "font.size": 12,
        "axes.labelsize": 11,
        "axes.titlesize": 11,
        "legend.fontsize": 11,
        "xtick.labelsize": 11,
        "ytick.labelsize": 11,
    })

# ==============================
# FUNCTION TO PLOT
# ==============================
def plot_curve(name, csv_file):
    df = pd.read_csv(csv_file)
    delta = df["delta"].to_numpy()
    energy = df["energy_density"].to_numpy()/1e9

    plt.figure(figsize=(3.2, 3.2))
    plt.plot(delta, energy, "o-", label=rf"{name} data")
    plt.xlabel(r"$\delta~[-]$")
    plt.ylabel(r"$\Delta E / V_0$ (GPa)")
    plt.title(rf"{title_prefix}: {name} strain")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{name.lower()}_energy_density.{save_format}", dpi=600)
    plt.close()

# ==============================
# MAIN
# ==============================
for name, file in files.items():
    print(f"Plotting {name} from {file} ...")
    plot_curve(name, file)

print("✅ Plots saved as hydro_energy_density.png, ortho_energy_density.png, shear_energy_density.png")

