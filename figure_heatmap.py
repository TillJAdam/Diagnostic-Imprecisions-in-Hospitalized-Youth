#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Figure: Heatmap of diagnostic misclassification and missed comorbidity.

Generates a two-panel figure (A: Misclassification, B: Missed Comorbidity)
showing n (%) per cell with FDR-corrected significance stars.

Inputs:
    - Figure_Data_Misclassification.csv (from script 8, Misclassification Matrices.Rmd)
    - Figure_Data_MissedComorbidity.csv  (from script 8, Misclassification Matrices.Rmd)
    Each CSV has columns: row_disorder, col_disorder, n, pct, p_value, p_fdr
    Falls back to hardcoded published values if CSVs are not found.

Outputs:
    - Figure_Heatmap.png
    - Figure_Heatmap.pdf
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# --- DISORDER LABELS ---
disorders = [
    "ADHD", "Schizophrenia-\nspectrum", "Bipolar-\nspectrum",
    "Depressive-\nspectrum", "Anxiety", "Obsessive/\ncompulsive",
    "Trauma/\nStress", "Feeding/\nEating",
    "Disruptive/\nConduct", "Substance\nuse", "Personality"
]

# Canonical order for mapping CSV row/col names to matrix indices
_disorder_keys = [
    "ADHD", "Schizophrenia-spectrum", "Bipolar-spectrum",
    "Depressive-spectrum", "Anxiety", "Obsessive/compulsive",
    "Trauma/Stress", "Feeding/Eating",
    "Disruptive/Conduct", "Substance use", "Personality"
]


def _p_fdr_to_stars(p):
    """Convert an FDR-corrected p-value to significance stars."""
    if pd.isna(p) or p >= 0.05:
        return ""
    if p < 0.001:
        return "***"
    if p < 0.01:
        return "**"
    return "*"


def _parse_csv(path):
    """Parse a CSV (from script 8) into 11x12 n, pct, and stars arrays.

    The 11x12 shape has a dummy first column (index 0) set to 0/"",
    matching the original hardcoded layout where column 0 was unused.
    """
    df = pd.read_csv(path)
    key_to_idx = {k: i for i, k in enumerate(_disorder_keys)}

    n_arr = np.zeros((11, 12), dtype=float)
    pct_arr = np.zeros((11, 12), dtype=float)
    stars_arr = np.full((11, 12), "", dtype=object)

    for _, row in df.iterrows():
        ri = key_to_idx.get(row["row_disorder"])
        ci = key_to_idx.get(row["col_disorder"])
        if ri is None or ci is None:
            continue
        cj = ci + 1  # shift right by 1 (column 0 is unused)
        n_arr[ri, cj] = row["n"]
        pct_arr[ri, cj] = row["pct"]
        stars_arr[ri, cj] = _p_fdr_to_stars(row.get("p_fdr", np.nan))

    return n_arr, pct_arr, stars_arr


def _load_data():
    """Load misclassification and comorbidity data from CSVs, or fall back to hardcoded values."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    mis_csv = os.path.join(script_dir, "Figure_Data_Misclassification.csv")
    com_csv = os.path.join(script_dir, "Figure_Data_MissedComorbidity.csv")

    try:
        mis_n, mis_pct, mis_stars = _parse_csv(mis_csv)
        com_n, com_pct, com_stars = _parse_csv(com_csv)
        print("Loaded data from CSVs.")
        return mis_n, mis_pct, mis_stars, com_n, com_pct, com_stars
    except Exception as e:
        print(f"CSV loading failed ({e}); using hardcoded published values.")

    # --- HARDCODED FALLBACK (published values) ---
    mis_n = np.array([
        [ 0,  0,  0, 11,  2,  0,  0,  1,  0,  0,  1,  2],
        [ 0,  2,  0, 17,  5,  4,  0,  2,  2,  0,  1,  4],
        [ 0,  0,  0,  0,  7,  1,  0,  0,  0,  0,  0,  0],
        [ 0,  2,  1, 52,  0,  1,  0,  2,  2,  0,  1,  3],
        [ 0,  1,  0, 18,  4,  0,  1,  4,  2,  0,  0,  0],
        [ 0,  1,  0,  4,  2,  0,  0,  0,  0,  1,  0,  0],
        [ 0,  2,  0, 10,  5,  2,  0,  0,  0,  2,  2,  2],
        [ 0,  0,  0,  1,  1,  0,  0,  2,  0,  0,  0,  0],
        [ 0,  1,  0, 17,  0,  3,  0,  1,  1,  0,  0,  4],
        [ 0,  0,  0,  9,  0,  0,  0,  1,  0,  0,  0,  0],
        [ 0,  0,  0, 12,  1,  2,  0,  1,  0,  0,  0,  0],
    ])
    mis_pct = np.array([
        [0, 0.0, 0.0, 2.9, 0.5, 0.0, 0.0, 0.3, 0.0, 0.0, 0.3, 0.5],
        [0, 0.5, 0.0, 4.4, 1.3, 1.0, 0.0, 0.5, 0.5, 0.0, 0.3, 1.0],
        [0, 0.0, 0.0, 0.0, 1.8, 0.3, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0, 0.5, 0.3,13.5, 0.0, 0.3, 0.0, 0.5, 0.5, 0.0, 0.3, 0.8],
        [0, 0.3, 0.0, 4.7, 1.0, 0.0, 0.3, 1.0, 0.5, 0.0, 0.0, 0.0],
        [0, 0.3, 0.0, 1.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.3, 0.0, 0.0],
        [0, 0.5, 0.0, 2.6, 1.3, 0.5, 0.0, 0.0, 0.0, 0.5, 0.5, 0.5],
        [0, 0.0, 0.0, 0.3, 0.3, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0],
        [0, 0.3, 0.0, 4.4, 0.0, 0.8, 0.0, 0.3, 0.3, 0.0, 0.0, 1.0],
        [0, 0.0, 0.0, 2.3, 0.0, 0.0, 0.0, 0.3, 0.0, 0.0, 0.0, 0.0],
        [0, 0.0, 0.0, 3.1, 0.3, 0.5, 0.0, 0.3, 0.0, 0.0, 0.0, 0.0],
    ])
    mis_stars = np.full((11, 12), "", dtype=object)
    mis_stars[3, 3] = "***"

    com_n = np.array([
        [ 0,  0,  1, 15, 17,  5,  0,  2,  1,  4,  4,  1],
        [ 0,  9,  0, 41, 47, 14,  2,  5,  4,  9,  6,  6],
        [ 0,  1,  1,  0,  0,  0,  0,  1,  2,  0,  1,  0],
        [ 0,  5,  2,  0,  0,  4,  0,  2,  2,  5,  2,  0],
        [ 0,  8,  1, 26, 47,  0,  1,  5,  5,  5,  6,  3],
        [ 0,  0,  1,  3,  5,  3,  0,  2,  0,  1,  1,  0],
        [ 0,  2,  2, 12, 26, 11,  0,  0,  1,  3,  5,  3],
        [ 0,  3,  0,  7,  8,  3,  0,  0,  0,  1,  2,  1],
        [ 0,  8,  2, 29, 19,  3,  1,  6,  3,  0,  9,  1],
        [ 0,  3,  2,  8, 10,  6,  0,  2,  1,  6,  0,  3],
        [ 0,  5,  0, 20, 17,  6,  1,  4,  3,  5,  5,  0],
    ])
    com_pct = np.array([
        [0, 0.0, 0.3, 3.9, 4.4, 1.3, 0.0, 0.5, 0.3, 1.0, 1.0, 0.3],
        [0, 2.3, 0.0,10.6,12.2, 3.6, 0.5, 1.3, 1.0, 2.3, 1.6, 1.6],
        [0, 0.3, 0.3, 0.0, 0.0, 0.0, 0.0, 0.3, 0.5, 0.0, 0.3, 0.0],
        [0, 1.3, 0.5, 0.0, 0.0, 1.0, 0.0, 0.5, 0.5, 1.3, 0.5, 0.0],
        [0, 2.1, 0.3, 6.8,12.2, 0.0, 0.3, 1.3, 1.3, 1.3, 1.6, 0.8],
        [0, 0.0, 0.3, 0.8, 1.3, 0.8, 0.0, 0.5, 0.0, 0.3, 0.3, 0.0],
        [0, 0.5, 0.5, 3.1, 6.8, 2.9, 0.0, 0.0, 0.3, 0.8, 1.3, 0.8],
        [0, 0.8, 0.0, 1.8, 2.1, 0.8, 0.0, 0.0, 0.0, 0.3, 0.5, 0.3],
        [0, 2.1, 0.5, 7.5, 4.9, 0.8, 0.3, 1.6, 0.8, 0.0, 2.3, 0.3],
        [0, 0.8, 0.5, 2.1, 2.6, 1.6, 0.0, 0.5, 0.3, 1.6, 0.0, 0.8],
        [0, 1.3, 0.0, 5.2, 4.4, 1.6, 0.3, 1.0, 0.8, 1.3, 1.3, 0.0],
    ])
    com_stars = np.full((11, 12), "", dtype=object)
    com_stars[0, 3]  = "**"
    com_stars[1, 3]  = "***"
    com_stars[1, 4]  = "***"
    com_stars[1, 5]  = "**"
    com_stars[4, 3]  = "***"
    com_stars[4, 4]  = "***"
    com_stars[6, 3]  = "*"
    com_stars[6, 4]  = "***"
    com_stars[8, 3]  = "***"
    com_stars[8, 4]  = "*"
    com_stars[10, 3] = "***"
    com_stars[10, 4] = "***"

    return mis_n, mis_pct, mis_stars, com_n, com_pct, com_stars


def draw_heatmap(ax, pct, n_vals, stars, title, disorders, show_xlab=True):
    """Draw one 11x11 heatmap panel (skip col 0 which is unused)."""
    pct11 = pct[:, 1:]
    n11 = n_vals[:, 1:]
    stars11 = stars[:, 1:]

    # Mask diagonal
    mask = np.eye(11, dtype=bool)
    data = np.ma.array(pct11, mask=mask)

    # Colormap: white -> light blue -> purple -> muted red
    cmap = mcolors.LinearSegmentedColormap.from_list(
        "custom", ["#FFFFFF", "#8CD3F5", "#8F5CCB", "#D96F76"], N=256
    )
    cmap.set_bad(color="#E8E8E8")  # diagonal

    im = ax.imshow(data, cmap=cmap, vmin=0, vmax=14, aspect="equal")

    # Cell annotations
    for i in range(11):
        for j in range(11):
            if i == j:
                ax.text(j, i, "\u2014", ha="center", va="center",
                        fontsize=7, color="#999999", fontweight="bold")
            else:
                n_val = int(n11[i, j])
                p_val = pct11[i, j]
                star = stars11[i, j]
                label = f"{n_val}\n({p_val:.1f}){star}"
                text_color = "white" if p_val > 7 else "black"
                ax.text(j, i, label, ha="center", va="center",
                        fontsize=5.5, color=text_color)

    # Axes
    ax.set_xticks(range(11))
    ax.set_yticks(range(11))
    ax.set_yticklabels(disorders, fontsize=7)

    if show_xlab:
        ax.set_xticklabels(disorders, fontsize=7, rotation=45, ha="right")
        ax.xaxis.set_ticks_position("bottom")
        ax.tick_params(axis="x", bottom=True, top=False)
    else:
        ax.set_xticklabels([])
        ax.tick_params(axis="x", bottom=False, top=False)

    ax.set_title(title, fontsize=10, fontweight="bold", pad=8)
    ax.set_ylabel("Structured Diagnostic Interview", fontsize=8, labelpad=6)

    # Grid lines
    for edge in range(12):
        ax.axhline(edge - 0.5, color="white", linewidth=0.5)
        ax.axvline(edge - 0.5, color="white", linewidth=0.5)

    # Outer border
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_color("black")
        spine.set_linewidth(0.8)

    return im


# --- MAIN ---
if __name__ == "__main__":
    mis_n, mis_pct, mis_stars, com_n, com_pct, com_stars = _load_data()

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 12.5), dpi=300,
                                    gridspec_kw={"hspace": 0.25})

    draw_heatmap(ax1, mis_pct, mis_n, mis_stars,
                 "A. Misclassification", disorders, show_xlab=False)
    im = draw_heatmap(ax2, com_pct, com_n, com_stars,
                      "B. Missed Comorbidity", disorders, show_xlab=True)

    ax2.set_xlabel("Clinical Diagnosis", fontsize=8, labelpad=8)

    # Shared colorbar
    cbar = fig.colorbar(im, ax=[ax1, ax2], shrink=0.4, aspect=25, pad=0.03)
    cbar.set_label("% of patients (n = 385)", fontsize=8)
    cbar.ax.tick_params(labelsize=7)

    # Footnotes
    fig.text(0.08, 0.02,
             "*P < .05;  **P < .01;  ***P < .001 (Benjamini-Hochberg-corrected)",
             fontsize=6.5, style="italic")

    plt.savefig("Figure_Heatmap.png", dpi=300, bbox_inches="tight", facecolor="white")
    plt.savefig("Figure_Heatmap.pdf", bbox_inches="tight", facecolor="white")

    print("Saved: Figure_Heatmap.png + .pdf")
