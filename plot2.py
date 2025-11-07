#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Fit ΔE/V₀ vs δ² for Hydro, Ortho, and Shear to extract C11, C12, C44 (in GPa).
Each CSV must contain: delta, energy_density_GPa
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ==============================
# USER SETTINGS
# ==============================
use_latex = True       # Set False if no LaTeX install
title_prefix = "Diamond"
save_format = "png"    # png or pdf

files = {
    "Hydro": "hydro.csv",
    "Ortho": "ortho.csv",
    "Shear": "shear.csv"
}

# ==============================
# MATPLOTLIB CONFIG
# ==============================
if use_latex:
    plt.rcParams.update({
        "text.usetex": True,
        "font.family": "serif",
        "font.size": 11,
        "axes.labelsize": 11,
        "axes.titlesize": 11,
        "legend.fontsize": 11,
        "xtick.labelsize": 11,
        "ytick.labelsize": 11,
    })

# ==============================
# FUNCTION TO LOAD AND FIT
# ==============================
def load_and_fit(name, csv_file):
    df = pd.read_csv(csv_file,sep=r"\s+")
    delta = df["delta"].to_numpy()
    d2 = delta**2
    energy = df["energy_density"].to_numpy()*1e-9

    # Linear fit through origin (ΔE/V₀ = A δ²)
    A, *_ = np.polyfit(delta, energy, 2)
    fit_energy = A * (np.linspace(-0.01,0.01,200))**2

    plt.figure(figsize=(3.2, 3.2))
    plt.plot(delta, energy, "o", label=rf"{name} DFT")
    plt.plot(np.linspace(-0.01,0.01,200), fit_energy, "-", label=rf"Fit")
    plt.xlabel(r"$\delta^2$")
    plt.ylabel(r"$\Delta E / V_0$ (GPa)")
    plt.title(rf"{title_prefix}: {name} strain")
    plt.legend(frameon=False)
    plt.tight_layout()
    plt.savefig(f"{name.lower()}_fit.{save_format}", dpi=600)
    plt.close()

    return A

# ==============================
# MAIN
# ==============================
Ah = load_and_fit("Hydro", files["Hydro"])
Ao = load_and_fit("Ortho", files["Ortho"])
As = load_and_fit("Shear", files["Shear"])

# Calculate elastic constants
C11 = (Ah + 2*Ao) / 3.0
C12 = (Ah - Ao) / 3.0
C44 = 2.0 * As

# ==============================
# PRINT AND SAVE RESULTS
# ==============================
with open("elastic_constants_from_fit.txt", "w") as f:
    f.write(f"A_hydro = {Ah:.2f} GPa\n")
    f.write(f"A_ortho = {Ao:.2f} GPa\n")
    f.write(f"A_shear = {As:.2f} GPa\n\n")
    f.write(f"C11 = {C11:.2f} GPa\n")
    f.write(f"C12 = {C12:.2f} GPa\n")
    f.write(f"C44 = {C44:.2f} GPa\n")

print("✅ Fitted constants (GPa):")
print(f"A_hydro = {Ah:.2f},  A_ortho = {Ao:.2f},  A_shear = {As:.2f}")
print(f"C11 = {C11:.2f},  C12 = {C12:.2f},  C44 = {C44:.2f}")
print("Results saved to elastic_constants_from_fit.txt")

