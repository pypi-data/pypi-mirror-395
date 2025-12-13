"""
PLS analysis for transcriptome gene contributions against FC deviations.

Provides reusable functions to select PLS components via CV, run PLS, compute
permutation p-values for weights, plotting utilities, and high-level pipeline.
"""
from typing import Tuple, Optional
from scipy.stats import zscore
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import logging
import os

from .utils import load_table_generic

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger(__name__)

try:
    from BrainNetAnno.utils import (
        select_optimal_components,
        permutation_explained_variance,
    )
except ModuleNotFoundError:
    import sys, os
    src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if src_dir not in sys.path:
        sys.path.append(src_dir)
    try:
        from utils import (
            select_optimal_components,
            permutation_explained_variance,
        )
    except ModuleNotFoundError:
        project_root = os.path.abspath(os.path.join(src_dir, '..'))
        if project_root not in sys.path:
            sys.path.append(project_root)
        from BrainNetAnno.utils import (
            select_optimal_components,
            permutation_explained_variance,
        )

# -----------------------------
# Data reading
# -----------------------------

def read_data_from_files(t_values_file: str, gene_expression_file: str) -> Tuple[pd.DataFrame, np.ndarray, np.ndarray, np.ndarray]:
    """Read FC deviation (t_values) and gene contribution matrices, align by Region_Pair.

    Parameters
    ----------
    t_values_file : str
        Path to CSV containing a square matrix of FC deviations (no header).
    gene_expression_file : str
        Path to CSV containing gene contributions with a 'Region_Pair' column.

    Returns
    -------
    Tuple[pd.DataFrame, np.ndarray, np.ndarray, np.ndarray]
        (df_pairs_values, t_values_vector, gene_matrix_aligned, gene_names_array)
    """
    t_values = load_table_generic(t_values_file, header=None)
    gene_df = load_table_generic(gene_expression_file)

    # Upper triangle non-zero entries from t_values
    coords = [(c, r) for r in range(t_values.shape[0]) for c in range(r + 1, t_values.shape[1]) if t_values.iat[r, c] != 0]
    formatted = [f"{r}-{c}" for c, r in coords]

    # Align gene_df by Region_Pair
    filtered = gene_df[gene_df["Region_Pair"].isin(formatted)].reset_index(drop=True)
    gene_names = filtered.columns.values
    gene_names = gene_names[gene_names != "Region_Pair"]
    gene_matrix = filtered.drop(columns=["Region_Pair"]).values

    df_pairs_values = pd.DataFrame([(f"{r}-{c}", t_values.at[r, c]) for c, r in coords], columns=["Region_Pair", "Value"])
    t_vector = df_pairs_values[["Value"]].values

    return df_pairs_values, t_vector, gene_matrix, gene_names

# -----------------------------
# Select component and genes
# -----------------------------

def select_best_component_and_genes(explained_variance_ratio: np.ndarray,
                                    p_values: np.ndarray,
                                    weights: np.ndarray,
                                    threshold: float = 0.05):
    """Select best component (prefer significant) and significant genes by simple z-score permutation.

    Parameters
    ----------
    explained_variance_ratio : np.ndarray
        Ratio of variance explained per component.
    p_values : np.ndarray
        P-values per component from permutation.
    weights : np.ndarray
        X weights matrix from PLS, shape (n_features, n_components).
    threshold : float, optional
        Significance threshold, by default 0.05.

    Returns
    -------
    Tuple[int, np.ndarray, np.ndarray, np.ndarray]
        best_component_index, best_genes_indices, z_scores_per_gene, p_values_per_gene
    """
    significant_components = np.where(p_values < threshold)[0]
    if len(significant_components) > 0:
        best_component = significant_components[np.argmax(explained_variance_ratio[significant_components])]
    else:
        best_component = int(np.argmax(explained_variance_ratio))

    best_weights = weights[:, best_component]
    z_scores = zscore(best_weights)
    p_values_genes = np.array([np.mean(np.random.permutation(z_scores) >= abs(z)) for z in z_scores])
    best_genes = np.where(p_values_genes < 0.05)[0]
    return best_component, best_genes, z_scores, p_values_genes

# -----------------------------
# Save and plot
# -----------------------------

def save_best_genes_to_csv(gene_names: np.ndarray,
                           best_genes: np.ndarray,
                           z_scores: np.ndarray,
                           p_values_genes: np.ndarray,
                           output_file: str) -> None:
    """Save significant genes info to CSV file."""
    results = {
        'Gene Index': gene_names[best_genes],
        'Original Z-Score': z_scores[best_genes],
        'P-Value': p_values_genes[best_genes]
    }
    results_df = pd.DataFrame(results)
    results_df.sort_values(by='P-Value', inplace=True)
    results_df.to_csv(output_file, index=False)

# -----------------------------
# High-level pipeline
# -----------------------------

def run_transcriptome_pls_pipeline(
    t_values_file_path: str,
    gene_expression_file_path: str,
    output_best_genes_path: str,
    mse_plot_path: Optional[str] = None,
    explained_variance_plot_path: Optional[str] = None,
    max_components: int = 15,
    cv_splits: int = 5,
    random_state: int = 42,
    n_permutations: int = 1000,
    n_components: Optional[int] = None,
) -> None:
    """Run PLS-based transcriptome analysis linking FC deviations to gene contributions.

    This pipeline reads FC deviation (t-values) and per-connection gene
    contribution matrices, aligns them by ``Region_Pair``, standardizes inputs,
    selects the optimal number of PLS components via cross-validated RMSE,
    estimates permutation-based significance for explained variance and feature
    weights, saves the significant genes to CSV, and plots RMSE and explained
    variance curves.

    Parameters
    ----------
    t_values_file : str
        Path to the CSV containing a square matrix of FC deviations (no header).
    gene_expression_file : str
        Path to the CSV containing per-connection gene contributions with a
        ``'Region_Pair'`` column.
    output_best_genes_csv : str
        Path to save the significant genes table. Parent directories are
        created automatically.
    fig_outputfile : Optional[str], optional
        Path to save plots (RMSE curve and explained variance). If ``None``,
        plots are saved next to ``output_best_genes_csv``. Default ``None``.
    max_components : int, optional
        Maximum number of components to consider in CV. Default ``15``.
    n_splits : int, optional
        Number of CV splits. Default ``5``.
    n_permutations : int, optional
        Number of permutations for significance testing. Default ``1000``.
    n_components : Optional[int], optional
        If provided, forces the number of components; otherwise chosen by CV.

    Returns
    -------
    None
        Saves outputs to disk and logs progress.

    Notes
    -----
    - Inputs are standardized before fitting.
    - Significant component selection prefers components with permutation
      p-values below the threshold; otherwise the component with highest
      explained variance is chosen.
    - Output directories are created automatically for CSV and figures.
    """
    logger.info(f"Loading t-values from: {t_values_file_path}")
    logger.info(f"Loading gene contributions from: {gene_expression_file_path}")
    df_pairs_values, t_values, gene_matrix, gene_names = read_data_from_files(t_values_file_path, gene_expression_file_path)
    df_pairs_values.to_csv(output_best_genes_path.replace('.csv', '_pairs_values.csv'), index=False)

    # Standardize
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    X = scaler.fit_transform(gene_matrix)
    Y = scaler.fit_transform(t_values)

    # CV errors and best components
    logger.info(f"Selecting optimal components (max={max_components}, splits={cv_splits})")
    best_n_comp, mse_scores = select_optimal_components(X, Y, max_components=max_components, cv_splits=cv_splits, random_state=random_state)

    logger.info(f"Best number of components selected: {best_n_comp}")

    # permutation test
    explained_variance_ratio, p_values, weights = permutation_explained_variance(X, Y, best_n_comp, n_permutations=n_permutations)
    best_component, best_genes, z_scores, p_values_genes = select_best_component_and_genes(explained_variance_ratio, p_values, weights)

    # Save significant genes
    save_best_genes_to_csv(gene_names, best_genes, z_scores, p_values_genes, output_best_genes_path)

    # Plot and save curves and data
    # Ensure directories exist only when paths are provided
    if mse_plot_path:
        mse_dir = os.path.dirname(mse_plot_path)
        if mse_dir:
            os.makedirs(mse_dir, exist_ok=True)

        # Save MSE data (CV errors per component)
        mse_csv = os.path.splitext(mse_plot_path)[0] + "_data.csv"
        pd.DataFrame({
            "Components": list(range(1, len(mse_scores) + 1)),
            "RMSE": mse_scores
        }).to_csv(mse_csv, index=False)

        # Plot MSE curve
        plt.figure(figsize=(6, 5))
        plt.plot(range(1, len(mse_scores) + 1), mse_scores, marker='o')
        plt.title('PLS CV MSE')
        plt.xlabel('Components')
        plt.ylabel('MSE')
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.tight_layout()
        plt.savefig(mse_plot_path, dpi=300)
        plt.close()
        logger.info(f"Saved SE curve to: {mse_plot_path}")
        logger.info(f"Saved SE data to: {mse_csv}")

    if explained_variance_plot_path:
        ev_dir = os.path.dirname(explained_variance_plot_path)
        if ev_dir:
            os.makedirs(ev_dir, exist_ok=True)
        # Save explained variance data (for X)
        ev_csv = os.path.splitext(explained_variance_plot_path)[0] + "_data.csv"
        pd.DataFrame({
            "Component": list(range(1, len(explained_variance_ratio) + 1)),
            "ExplainedVariance": explained_variance_ratio
        }).to_csv(ev_csv, index=False)
        # Plot explained variance
        plt.figure(figsize=(8, 5))
        plt.plot(range(1, len(explained_variance_ratio) + 1), explained_variance_ratio * 100,
                 marker='o', linestyle='-', color='b', label='Explained Variance (X)')
        plt.xlabel("PLS Component", fontsize=14)
        plt.ylabel("Explained Variance (%)", fontsize=14)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.legend(fontsize=12)
        plt.tight_layout()
        plt.savefig(explained_variance_plot_path, dpi=300)
        plt.close()
        logger.info(f"Saved explained variance plot to: {explained_variance_plot_path}")
        logger.info(f"Saved explained variance data to: {ev_csv}")

    # Ensure output directories exist for CSVs
    out_dir = os.path.dirname(output_best_genes_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    df_best = pd.DataFrame({
        'Gene Index': gene_names[best_genes],
        'Original Z-Score': z_scores[best_genes],
        'P-Value': p_values_genes[best_genes]
    })
    df_best.to_csv(output_best_genes_path, index=False)
    logger.info(f"Saved best genes CSV to: {output_best_genes_path}")

    logger.info("Transcriptome PLS pipeline completed successfully.")