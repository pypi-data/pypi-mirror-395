"""
PLS analysis for mitochondrial contributions against FC deviations.

Provides reusable functions to select PLS components via CV, run PLS, compute
permutation p-values for weights, and plotting utilities suitable for packaging.
"""
from typing import Tuple, Optional
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import logging
import os
from .utils import load_table_generic

try:
    from BrainNetAnno.utils import (
        select_optimal_components,
        run_pls,
        permutation_pvalues,
        plot_mse_curve,
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
            run_pls,
            permutation_pvalues,
            plot_mse_curve,
            permutation_explained_variance,
        )
    except ModuleNotFoundError:
        project_root = os.path.abspath(os.path.join(src_dir, '..'))
        if project_root not in sys.path:
            sys.path.append(project_root)
        from BrainNetAnno.utils import (
            select_optimal_components,
            run_pls,
            permutation_pvalues,
            plot_mse_curve,
            permutation_explained_variance,
        )

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger(__name__)

def run_mitochondrial_pls_pipeline(fc_matrix_path: str,
                 nt_contrib_path: str,
                 top_k: int = 500,
                 mse_plot_path: Optional[str] = None,
                 explained_variance_plot_path: Optional[str] = None,
                 output_weights_path: Optional[str] = None,
                 max_components: int = 6,
                 cv_splits: int = 5,
                 random_state: int = 42,
                 n_permutations: int = 1000) -> Tuple[int, pd.DataFrame]:
    """Run PLS analysis linking FC weights to mitochondrial contributions.

    This pipeline loads an FC weights matrix and a per-connection mitochondrial
    contribution table, aligns by ``Region_Pair``, selects the optimal number of
    PLS components via cross-validated MSE, fits the PLS model, computes
    permutation p-values for feature weights, saves results, and optionally
    saves plots of MSE and explained variance.

    Parameters
    ----------
    fc_matrix_path : str
        Path to the CSV containing a square FC weights matrix (no header).
    nt_contrib_csv : str
        Path to the CSV containing mitochondrial contributions with a
        ``'Region_Pair'`` column.
    top_k : int, optional
        Number of top absolute FC entries to keep. Default ``500``.
    mse_plot_path : Optional[str], optional
        Path to save the CV MSE curve plot. Default ``None``.
    explained_variance_plot_path : Optional[str], optional
        Path to save the explained-variance plot for X scores. Default ``None``.
    output_weights_csv : Optional[str], optional
        Path to save weights and p-values CSV. Default ``None``.
    max_components : int, optional
        Maximum number of components considered in CV. Default ``6``.
    cv_splits : int, optional
        Number of CV splits. Default ``5``.
    random_state : int, optional
        Random seed for CV. Default ``42``.
    n_permutations : int, optional
        Number of permutations for p-values. Default ``1000``.

    Returns
    -------
    Tuple[int, pd.DataFrame]
        Best number of components and a DataFrame with neurotransmitter weights and p-values.

    Notes
    -----
    - Output directories for plots and CSVs are created automatically when
      paths are provided.
    - The explained variance is computed from X scores relative to total X
      variance.
    """
    logger.info(f"Loading FC matrix from: {fc_matrix_path}")
    try:
        fc_matrix = load_table_generic(fc_matrix_path, header=None).values
    except Exception as e:
        logger.error(f"Failed to read FC matrix: {e}")
        raise
    logger.info(f"FC matrix loaded. Shape: {fc_matrix.shape}")

    row_idx, col_idx = np.triu_indices_from(fc_matrix, k=1)
    nonzero_mask = fc_matrix[row_idx, col_idx] != 0

    region_pairs = [f"{r}-{c}" for r, c in zip(row_idx[nonzero_mask], col_idx[nonzero_mask])]
    fc_values = fc_matrix[row_idx[nonzero_mask], col_idx[nonzero_mask]]

    logger.info(f"Selecting top {top_k} FC entries by absolute value")
    top_idx = np.argsort(np.abs(fc_values))[-top_k:]
    fc_df = pd.DataFrame({"Region_Pair": np.array(region_pairs)[top_idx], "FC_Value": fc_values[top_idx]})

    logger.info(f"Merging FC with mitochondrial contributions from: {nt_contrib_path}")
    try:
        nt_df = load_table_generic(nt_contrib_path)
    except Exception as e:
        logger.error(f"Failed to read contributions CSV: {e}")
        raise
    merged_df = pd.merge(fc_df, nt_df, on="Region_Pair")
    logger.info(f"Merged dataset shape: {merged_df.shape}; features: {merged_df.shape[1]-2}")

    Y = merged_df["FC_Value"].values
    X = merged_df.drop(columns=["Region_Pair", "FC_Value"]).values
    mitochondrial = merged_df.drop(columns=["Region_Pair", "FC_Value"]).columns

    logger.info(f"Running CV to select optimal PLS components (max={max_components}, splits={cv_splits}, seed={random_state})")
    best_n_comp, mse_scores = select_optimal_components(X, Y, max_components=max_components, cv_splits=cv_splits, random_state=random_state)
    logger.info(f"Best number of components selected: {best_n_comp}")

    if mse_plot_path:
        from os import path, makedirs
        d = path.dirname(mse_plot_path)
        if d:
            makedirs(d, exist_ok=True)
        mse_csv = path.splitext(mse_plot_path)[0] + "_data.csv"
        pd.DataFrame({"Components": list(range(1, len(mse_scores)+1)), "MSE": mse_scores}).to_csv(mse_csv, index=False)
        plot_mse_curve(mse_scores, mse_plot_path)
        logger.info(f"Saved MSE curve to: {mse_plot_path}")
        logger.info(f"Saved MSE data to: {mse_csv}")

    pls, x_weights, x_scores, y_scores = run_pls(X, Y, best_n_comp)
    logger.info("PLS model fitted. Computing explained variance via permutation.")

    pls, x_weights, x_scores, y_scores = run_pls(X, Y, best_n_comp)

    total_var_X = np.var(X, axis=0).sum()
    explained_var_X = np.var(x_scores, axis=0) / total_var_X
    explained_var_Y = np.var(y_scores, axis=0) / np.var(Y)

    if explained_variance_plot_path:
        from os import path, makedirs
        d = path.dirname(explained_variance_plot_path)
        if d:
            makedirs(d, exist_ok=True)
        ev_csv = path.splitext(explained_variance_plot_path)[0] + "_data.csv"
        pd.DataFrame({
            "Component": list(range(1, len(explained_var_X)+1)),
            "ExplainedVariance_X": explained_var_X,
            "ExplainedVariance_Y": explained_var_Y
        }).to_csv(ev_csv, index=False)
        plt.figure(figsize=(8, 5))
        plt.plot(range(1, len(explained_var_X) + 1), explained_var_X * 100, 
                 marker='o', linestyle='-', color='b', label='Explained Variance (X)')
        plt.xlabel("PLS Component", fontsize=14)
        plt.ylabel("Explained Variance (%)", fontsize=14)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.legend(fontsize=12)
        plt.savefig(explained_variance_plot_path, dpi=300)
        plt.close()
        logger.info(f"Saved explained variance plot to: {explained_variance_plot_path}")

    optimal_component_index = int(np.argmax(explained_var_X))
    logger.info(f"Computing permutation p-values (n={n_permutations}) for component index {optimal_component_index}")
    p_values = permutation_pvalues(X, Y, best_n_comp, optimal_component_index, n_permutations=n_permutations)

    logger.info("Assembling result DataFrame with weights and p-values")
    result_df = pd.DataFrame({
        "Mitochondrial": mitochondrial,
        "Weight": x_weights[:, optimal_component_index],
        "P_value": p_values,
    }).sort_values(by="Weight", key=np.abs, ascending=False)

    import os
    for p in [output_weights_path]:
        if p:
            d = os.path.dirname(p)
            if d:
                os.makedirs(d, exist_ok=True)
    if output_weights_path:
        result_df.to_csv(output_weights_path, index=False)
        logger.info(f"Saved weights and p-values to: {output_weights_path}")

    logger.info("Mitochondrial PLS pipeline completed successfully.")
    return best_n_comp, result_df