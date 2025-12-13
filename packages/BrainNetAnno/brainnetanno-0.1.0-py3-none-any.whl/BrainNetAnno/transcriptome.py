"""
Transcriptome analysis utilities for computing CGE vs. distance relationships
and per-connection gene contribution scores using NumPy/SciPy on CPU.

"""
from typing import Tuple, Sequence, Optional
import os
import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger(__name__)

# Import shared utilities with robust fallback for script execution
try:
    from .utils import (
        load_coordinates_adaptive,
        load_gene_expression,
        zscore_rows,
        compute_distance_matrix,
        exponential_decay,
        fit_exponential_decay,
        compute_expected_matrix,
        compute_cge,
    )
except ImportError:
    import os, sys
    # Add the parent directory of this file (i.e., the package root's parent) to sys.path
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from BrainNetAnno.utils import (
        load_coordinates_adaptive,
        load_gene_expression,
        zscore_rows,
        compute_distance_matrix,
        exponential_decay,
        fit_exponential_decay,
        compute_expected_matrix,
        compute_cge,
    )

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# -----------------------------
# Core computations (module-specific)
# -----------------------------

def compute_gene_contribution(z_gene_expression: np.ndarray,
                              expected_matrix: np.ndarray,
                              upper_tri_indices: Tuple[np.ndarray, np.ndarray],
                              gene_names: Sequence[str]) -> pd.DataFrame:
    """Compute per-connection gene contribution scores.

    For each connection (i, j), contribution score for gene g is:
        z[i, g] * z[j, g] - expected[i, j]

    Parameters
    ----------
    z_gene_expression : np.ndarray
        Z-scored gene expression matrix of shape (n_regions, n_genes).
    expected_matrix : np.ndarray
        Expected CGE matrix of shape (n_regions, n_regions).
    upper_tri_indices : Tuple[np.ndarray, np.ndarray]
        Indices (rows, cols) of the upper triangle (k=1) of the matrices.
    gene_names : Sequence[str]
        Names of genes corresponding to columns in z_gene_expression.

    Returns
    -------
    pd.DataFrame
        DataFrame of shape (n_connections, n_genes + 1) with a 'Region_Pair' column
        and per-gene contribution scores.
    """
    rows, cols = upper_tri_indices
    n_connections = rows.shape[0]
    n_genes = z_gene_expression.shape[1]

    out = pd.DataFrame(np.zeros((n_connections, n_genes)), columns=gene_names)
    region_pairs = [f"{int(i)}-{int(j)}" for i, j in zip(rows, cols)]

    for idx, (i, j) in enumerate(zip(rows, cols)):
        product_z = z_gene_expression[i] * z_gene_expression[j]
        out.iloc[idx, :] = product_z - expected_matrix[i, j]

    out.insert(0, "Region_Pair", region_pairs)
    return out

# -----------------------------
# Visualization
# -----------------------------

def plot_fit(distances: np.ndarray, correlations: np.ndarray, params: Tuple[float, float, float]) -> None:
    """Plot empirical CGE vs. distance and fitted exponential decay curve.

    Parameters
    ----------
    distances : np.ndarray
        1D array of pairwise distances (upper triangle entries).
    correlations : np.ndarray
        1D array of CGE values matching distances.
    params : Tuple[float, float, float]
        Fitted parameters (A, n, B).
    """
    A, n, B = params
    plt.figure(figsize=(8, 6))
    plt.scatter(distances, correlations, s=1, color='gray', alpha=0.5, label='Data')
    order = np.argsort(distances)
    plt.plot(distances[order], exponential_decay(distances[order], A, n, B),
             color='red', linewidth=2, label='Fitted Curve')
    plt.xlabel("Distance between regions (mm)")
    plt.ylabel("Correlated gene expression (CGE)")
    plt.title("CGE vs. Distance with Fitted Exponential Decay")
    plt.legend()

# -----------------------------
# High-level pipeline
# -----------------------------

def run_transcriptome_pipeline(coordinates_path: str,
                 gene_expression_path: str,
                 output_contribution_path: str,
                 initial_params: Sequence[float] = (0.64, 90.4, -0.19),
                 save_plot: bool = False,
                 plot_path: Optional[str] = None) -> Tuple[Tuple[float, float, float], pd.DataFrame]:
    """Run transcriptome-based CGE analysis and optionally save per-connection gene contributions.

    This high-level pipeline loads region MNI coordinates and a transcriptome
    expression matrix, computes pairwise distances and a precision-based
    connection measure, fits an exponential distance-decay model to the
    connection values, builds an expected connection matrix, and derives per-
    connection gene contribution scores. Results can be saved to CSV and an
    optional plot of the fitted decay can be saved.

    Parameters
    ----------
    coordinates_csv : str
        Path to the CSV containing region coordinates with columns such as
        ``'MNI_X'``, ``'MNI_Y'``, ``'MNI_Z'``.
    gene_expression_csv : str
        Path to the CSV containing gene expression (rows=regions, columns=genes).
    output_contribution_csv : str
        Path to save the per-connection gene contribution scores as CSV.
        Parent directories are created automatically.
    initial_params : Sequence[float], optional
        Initial guess for the exponential decay parameters ``(A, n, B)``.
        Default is ``(0.64, 90.4, -0.19)``.
    save_plot : bool, optional
        Whether to save the fitted distance-decay plot. Default is ``False``.
    plot_path : Optional[str], optional
        Path to save the plot when ``save_plot=True``. If ``None``, a file next
        to ``output_contribution_csv`` is used.

    Returns
    -------
    Tuple[Tuple[float, float, float], pd.DataFrame]
        The fitted decay parameters ``(A, n, B)`` and the contribution DataFrame
        with a ``'Region_Pair'`` column followed by per-gene scores.

    Notes
    -----
    - Rows of the expression matrix are z-scored prior to model fitting.
    - Precision matrix is estimated via Ledoit–Wolf shrinkage on gene features.
    - The expected connection matrix is built from the fitted decay model.
    - Parent directories for ``output_contribution_csv`` are created
      automatically when saving results.
    """
    logger.info(f"Loading coordinates from: {coordinates_path}")
    coords = load_coordinates_adaptive(coordinates_path)
    logger.info(f"Coordinates loaded. Shape: {coords.shape}")

    logger.info(f"Loading gene expression CSV from: {gene_expression_path}")
    matrix, gene_names = load_gene_expression(gene_expression_path)
    logger.info(f"Gene expression loaded. Shape: {matrix.shape}; genes: {len(gene_names)}")

    logger.info("Computing distance matrix and z-scoring rows")
    dist_mat = compute_distance_matrix(coords)
    z_mat = zscore_rows(matrix)

    logger.info("Computing correlated gene expression (CGE)")
    cge_mat = compute_cge(z_mat)

    upper = np.triu_indices(dist_mat.shape[0], k=1)
    distances = dist_mat[upper]
    correlations = cge_mat[upper]

    logger.info(f"Fitting exponential decay with initial params: {tuple(initial_params)}")
    params = fit_exponential_decay(distances, correlations, initial_params=initial_params)
    A, n, B = params
    logger.info(f"Fitted decay params: A={A:.4f}, n={n:.4f}, B={B:.4f}")

    logger.info("Building expected connection matrix from decay model")
    expected = compute_expected_matrix(dist_mat, A, n, B)

    logger.info("Computing per-connection gene contribution scores")
    contrib_df = compute_gene_contribution(z_mat, expected, upper, gene_names)

    logger.info(f"Saving contributions to: {output_contribution_path}")
    d = os.path.dirname(output_contribution_path)
    if d:
        os.makedirs(d, exist_ok=True)
    contrib_df.to_csv(output_contribution_path, index=False)
    logger.info(f"Saved contributions to: {output_contribution_path}")

    if save_plot:
        if plot_path is None:
            plot_path = os.path.splitext(output_contribution_path)[0] + "_decay_plot.tif"
        pds = os.path.dirname(plot_path)
        if pds:
            os.makedirs(pds, exist_ok=True)

        plot_data_csv = os.path.splitext(plot_path)[0] + "_data.csv"
        plot_df = pd.DataFrame({
            "Distance": distances,
            "CGE": correlations,
            "Fitted": exponential_decay(distances, A, n, B),
        })
        plot_df.to_csv(plot_data_csv, index=False)
        # Generate and save the plot
        plt.figure(figsize=(8, 6))
        order = np.argsort(distances)
        plt.scatter(distances, correlations, s=3, color='gray', alpha=0.5)
        plt.plot(distances[order], exponential_decay(distances[order], A, n, B), color='red', linewidth=2)
        plt.xlabel("Distance between regions (mm)")
        plt.ylabel("Connection strength (precision)")
        plt.title("CGE vs. Distance with Fitted Exponential Decay")
        plt.savefig(plot_path, dpi=300)
        plt.close()
        logger.info(f"Saved decay plot to: {plot_path}")
        logger.info(f"Saved plot data to: {plot_data_csv}")

    return params, contrib_df
