"""
Common utilities for molecular network analyses (NumPy/SciPy/Scikit-learn, CPU).

This module centralizes shared functions to avoid redundancy across submodules.
It provides:
- Robust table loaders for CSV/Excel
- Coordinate, expression loaders and z-score preprocessing
- Distance/CGE computations and exponential decay fitting
- Shared PLS helpers (CV component selection, permutation tests, plotting)

All functions aim to have stable I/O contracts and clear error messages.
"""
from typing import Tuple, Sequence, Optional
from scipy.spatial.distance import pdist, squareform
from scipy.optimize import curve_fit
from scipy.stats import zscore
import numpy as np
import pandas as pd
import os

# -----------------------------
# Data loading and preprocessing
# -----------------------------

def _is_excel(path: str) -> bool:
    """Return True if file extension indicates an Excel file.

    Parameters
    ----------
    path : str
        File path.

    Returns
    -------
    bool
        Whether the path ends with .xlsx or .xls (case-insensitive).
    """
    ext = os.path.splitext(path)[1].lower()
    return ext in {'.xlsx', '.xls'}


def load_table_generic(path: str, **read_kwargs) -> pd.DataFrame:
    """Load a tabular file (CSV or Excel) adaptively based on file extension.

    Parameters
    ----------
    path : str
        File path ending with .csv, .xlsx, or .xls.
    **read_kwargs : dict
        Extra keyword arguments passed to pandas reader (e.g., sheet_name for Excel).

    Returns
    -------
    pd.DataFrame
        Loaded DataFrame.

    Raises
    ------
    FileNotFoundError
        If the file does not exist.
    ValueError
        If the file extension is unsupported.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    if _is_excel(path):
        return pd.read_excel(path, **read_kwargs)
    ext = os.path.splitext(path)[1].lower()
    if ext == '.csv':
        return pd.read_csv(path, **read_kwargs)
    raise ValueError(f"Unsupported file extension: {ext}. Expected .csv/.xlsx/.xls")


def load_coordinates_adaptive(path: str) -> np.ndarray:
    """Load coordinates from CSV or Excel adaptively.

    Expects columns 'MNI_X','MNI_Y','MNI_Z'.

    Parameters
    ----------
    path : str
        Path to CSV/Excel containing coordinate columns.

    Returns
    -------
    np.ndarray
        Array of shape (n_regions, 3) with xyz coordinates.

    Raises
    ------
    ValueError
        If required coordinate columns are missing.
    """
    df = load_table_generic(path)
    required = ["MNI_X", "MNI_Y", "MNI_Z"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing coordinate columns: {missing} in {path}")
    return df[["MNI_X", "MNI_Y", "MNI_Z"]].values


def load_gene_expression(path: str, drop_columns: Sequence[str] = ("label",)) -> Tuple[np.ndarray, pd.Index]:
    """Load gene expression from CSV or Excel adaptively.

    Parameters
    ----------
    path : str
        File path (.csv, .xlsx, .xls) containing rows=regions, columns=genes.
    drop_columns : Sequence[str], optional
        Column names to drop (e.g., labels), by default ("label",).

    Returns
    -------
    Tuple[np.ndarray, pd.Index]
        Matrix (n_regions, n_genes) and gene names index.

    Notes
    -----
    - Non-feature columns listed in ``drop_columns`` are removed if present.
    - Returned matrix preserves the original row order.
    """
    df = load_table_generic(path)
    for col in drop_columns:
        if col in df.columns:
            df = df.drop(columns=[col])
    return df.values, df.columns

# Backward-compatible wrappers delegate to adaptive loaders

def load_coordinates(csv_path: str) -> np.ndarray:
    """Backward-compatible wrapper for ``load_coordinates_adaptive``."""
    return load_coordinates_adaptive(csv_path)


def load_gene_expression_csv(csv_path: str, drop_columns: Sequence[str] = ("label",)) -> Tuple[np.ndarray, pd.Index]:
    """Backward-compatible wrapper for ``load_gene_expression``."""
    return load_gene_expression(csv_path, drop_columns)


def load_neurotransmitter_expression(xlsx_path: str, drop_columns: Sequence[str] = ("label",)) -> Tuple[np.ndarray, pd.Index]:
    """Load neurotransmitter expression from Excel/CSV adaptively.

    Parameters
    ----------
    xlsx_path : str
        Path to the file containing rows=regions, columns=neurotransmitters.
    drop_columns : Sequence[str], optional
        Column names to drop (e.g., labels), by default ("label",).

    Returns
    -------
    Tuple[np.ndarray, pd.Index]
        Matrix (n_regions, n_neurotransmitters) and names index.
    """
    df = load_table_generic(xlsx_path)
    # Drop any specified non-feature columns if present
    for col in drop_columns:
        if col in df.columns:
            df = df.drop(columns=[col])
    return df.values, df.columns


def load_mitochondrial_expression(xlsx_path: str, drop_columns: Sequence[str] = ("label",)) -> Tuple[np.ndarray, pd.Index]:
    """Load mitochondrial expression from Excel/CSV adaptively.

    Parameters
    ----------
    xlsx_path : str
        Path to the file containing rows=regions, columns=mitochondrial genes/features.
    drop_columns : Sequence[str], optional
        Column names to drop (e.g., labels), by default ("label",).

    Returns
    -------
    Tuple[np.ndarray, pd.Index]
        Matrix (n_regions, n_features) and names index.
    """
    df = load_table_generic(xlsx_path)
    for col in drop_columns:
        if col in df.columns:
            df = df.drop(columns=[col])
    return df.values, df.columns


def zscore_rows(matrix: np.ndarray) -> np.ndarray:
    """Apply z-score along rows to standardize each region's gene expression vector.

    Parameters
    ----------
    matrix : np.ndarray
        Gene expression matrix of shape (n_regions, n_genes).

    Returns
    -------
    np.ndarray
        Z-scored matrix with same shape, standardized per row.

    Notes
    -----
    Uses ``scipy.stats.zscore`` with default settings (population standardization).
    """
    return np.apply_along_axis(zscore, 1, matrix)

# -----------------------------
# Core computations
# -----------------------------

def compute_distance_matrix(coordinates: np.ndarray) -> np.ndarray:
    """Compute Euclidean distance matrix between brain regions.

    Parameters
    ----------
    coordinates : np.ndarray
        Array of shape (n_regions, 3) with xyz coordinates.

    Returns
    -------
    np.ndarray
        Distance matrix of shape (n_regions, n_regions).
    """
    return squareform(pdist(coordinates, metric="euclidean"))


def compute_cge(z_gene_expression: np.ndarray) -> np.ndarray:
    """Compute correlated gene expression (CGE) between regions.

    Parameters
    ----------
    z_gene_expression : np.ndarray
        Z-scored gene expression matrix of shape (n_regions, n_genes). Rows are regions.

    Returns
    -------
    np.ndarray
        Correlation matrix (CGE) of shape (n_regions, n_regions).
    """
    return np.corrcoef(z_gene_expression)


def exponential_decay(d: np.ndarray, A: float, n: float, B: float) -> np.ndarray:
    """Exponential decay function A * exp(-d / n) + B.

    Parameters
    ----------
    d : np.ndarray
        Distance values.
    A : float
        Amplitude.
    n : float
        Scale/decay parameter.
    B : float
        Offset/baseline.
    """
    return A * np.exp(-d / n) + B


def fit_exponential_decay(distances: np.ndarray, correlations: np.ndarray,
                          initial_params: Sequence[float]) -> Tuple[float, float, float]:
    """Fit the exponential decay relationship between distance and observations.

    Parameters
    ----------
    distances : np.ndarray
        1D array of pairwise distances (upper triangle entries).
    correlations : np.ndarray
        1D array of observed values matching distances.
    initial_params : Sequence[float]
        Initial guess for parameters (A, n, B).

    Returns
    -------
    Tuple[float, float, float]
        Fitted parameters (A, n, B).

    Raises
    ------
    RuntimeError
        If curve fitting fails to converge.
    """
    popt, _ = curve_fit(exponential_decay, distances, correlations, p0=initial_params)
    A, n, B = popt
    return float(A), float(n), float(B)


def compute_expected_matrix(distance_matrix: np.ndarray, A: float, n: float, B: float) -> np.ndarray:
    """Compute expected matrix using fitted exponential decay parameters.

    Parameters
    ----------
    distance_matrix : np.ndarray
        Pairwise distance matrix.
    A, n, B : float
        Fitted parameters for exponential decay.

    Returns
    -------
    np.ndarray
        Expected values per pair.
    """
    return A * np.exp(-distance_matrix / n) + B

# -----------------------------
# PLS utilities (shared across modules)
# -----------------------------
from sklearn.cross_decomposition import PLSRegression
from sklearn.model_selection import KFold, cross_val_score
from sklearn.utils import shuffle


def select_optimal_components(X: np.ndarray, Y: np.ndarray,
                              max_components: int = 10,
                              cv_splits: int = 5,
                              random_state: int = 42) -> Tuple[int, list]:
    """Select the optimal number of PLS components using K-Fold cross-validation.

    This function evaluates Partial Least Squares (PLS) regression models with
    different numbers of components and selects the configuration that achieves
    the lowest mean cross-validated Mean Squared Error (MSE).

    Key implementation details:
    - Upper bound on n_components: Scikit-learn's PLSRegression enforces that
      ``n_components <= min(n_samples, n_features, n_targets)``. We compute this
      upper bound from the input data and cap the search space accordingly to
      avoid runtime errors.
    - Cross-validation: Uses K-Fold CV with shuffling to obtain stable estimates
      of generalization performance. The scoring metric is negative MSE, which
      is converted back to MSE for interpretability.

    Parameters
    ----------
    X : np.ndarray
        Predictor matrix of shape (n_samples, n_features).
    Y : np.ndarray
        Response vector or matrix of shape (n_samples,) or (n_samples, n_targets).
        If a 1D vector is provided, it is treated as a single-target regression
        with ``n_targets = 1``.
    max_components : int, optional
        Maximum number of components to consider (before applying the upper bound
        constraint). Default is 10.
    cv_splits : int, optional
        Number of cross-validation folds (K in K-Fold). Default is 5.
    random_state : int, optional
        Random seed used for shuffling in K-Fold to ensure reproducibility.
        Default is 42.

    Returns
    -------
    Tuple[int, list]
        - best_n_comp: The number of components (1-based) yielding the lowest
          mean CV MSE across folds.
        - mse_scores: A list of mean CV MSE values for each evaluated component
          count, ordered from 1 to ``min(max_components, upper_bound)``.

    Notes
    -----
    - If multiple component counts result in identical MSE, ``np.argmin``
      returns the first occurrence (i.e., the smallest number of components).
    - The returned ``mse_scores`` can be plotted against component counts to
      visualize the bias-variance trade-off and identify potential overfitting.
    """
    # Prepare CV splitter with reproducible shuffling
    cv = KFold(n_splits=cv_splits, shuffle=True, random_state=random_state)

    # Determine sklearn's upper bound for n_components
    n_samples = X.shape[0]
    n_features = X.shape[1]
    n_targets = 1 if Y.ndim == 1 else Y.shape[1]
    upper_bound = int(min(n_samples, n_features, n_targets))

    # Cap the component search space to avoid invalid configurations
    max_n = int(min(max_components, upper_bound))

    mse_scores = []  # Collect mean CV MSE for each component count

    # Evaluate PLS models from 1 to max_n components
    for n_comp in range(1, max_n + 1):
        pls = PLSRegression(n_components=n_comp)
        # cross_val_score returns negative MSE; convert to positive MSE by negation
        scores = cross_val_score(pls, X, Y, cv=cv, scoring='neg_mean_squared_error')
        mse_scores.append(-np.mean(scores))

    # Select the component count with the smallest mean CV MSE
    best_n_comp = int(np.argmin(mse_scores) + 1)  # +1 to map index -> component count
    return best_n_comp, mse_scores


def run_pls(X: np.ndarray, Y: np.ndarray, n_components: int) -> Tuple[PLSRegression, np.ndarray, np.ndarray, np.ndarray]:
    """Fit a PLS regression model and return weights and scores.

    Parameters
    ----------
    X : np.ndarray
        Predictor matrix (n_samples, n_features).
    Y : np.ndarray
        Response vector/matrix (n_samples,) or (n_samples, n_targets).
    n_components : int
        Number of latent components in PLS.

    Returns
    -------
    Tuple[PLSRegression, np.ndarray, np.ndarray, np.ndarray]
        Fitted PLS model, x_weights, x_scores, y_scores.
    """
    pls = PLSRegression(n_components=n_components)
    pls.fit(X, Y)
    return pls, pls.x_weights_, pls.x_scores_, pls.y_scores_


def permutation_pvalues(X: np.ndarray, Y: np.ndarray, n_components: int,
                        target_component_index: int,
                        n_permutations: int = 1000) -> np.ndarray:
    """Compute permutation p-values for PLS weights of a specific component.

    Parameters
    ----------
    X : np.ndarray
        Predictor matrix.
    Y : np.ndarray
        Response vector/matrix.
    n_components : int
        Number of PLS components to fit.
    target_component_index : int
        Index of the component whose weights are tested.
    n_permutations : int, optional
        Number of permutations, default 1000.

    Returns
    -------
    np.ndarray
        P-values per feature for the target component's weights.

    Notes
    -----
    - The null distribution is built by shuffling X and Y jointly with a fixed
      random seed per permutation for reproducibility.
    - Two-sided testing is approximated by comparing absolute weights to the
      empirical null absolute weights.
    """
    pls, x_weights, x_scores, _ = run_pls(X, Y, n_components)
    true_weights = x_weights[:, target_component_index]

    perm_weights = np.zeros((n_permutations, X.shape[1]))
    for i in range(n_permutations):
        X_perm, Y_perm = shuffle(X, Y, random_state=i)
        pls_perm = PLSRegression(n_components=n_components)
        pls_perm.fit(X_perm, Y_perm)
        w = pls_perm.x_weights_[:, target_component_index]
        perm_weights[i, :] = w

    p_values = np.mean(np.abs(perm_weights) >= np.abs(true_weights[None, :]), axis=0)
    return p_values


def plot_mse_curve(mse_scores: Sequence[float], save_path: Optional[str] = None) -> None:
    """Plot mean CV MSE vs. number of PLS components.

    Parameters
    ----------
    mse_scores : Sequence[float]
        Mean CV MSE per component count.
    save_path : Optional[str], optional
        Path to save the figure (created if directory missing). If None, only
        renders the plot in memory for the caller to handle.
    """
    import matplotlib.pyplot as plt
    plt.figure(figsize=(8, 5))
    plt.plot(range(1, len(mse_scores) + 1), mse_scores, marker='o')
    plt.xlabel('PLS Components')
    plt.ylabel('MSE (CV)')
    plt.grid(True, linestyle='--', alpha=0.6)
    if save_path:
        d = os.path.dirname(save_path)
        if d:
            os.makedirs(d, exist_ok=True)
        plt.savefig(save_path, dpi=300)


def permutation_explained_variance(X: np.ndarray, Y: np.ndarray, n_components: int, n_permutations: int = 1000):
    """Compute explained variance ratio per component and permutation p-values for components.

    Parameters
    ----------
    X : np.ndarray
        Predictor matrix.
    Y : np.ndarray
        Response matrix/vector.
    n_components : int
        Number of PLS components.
    n_permutations : int, optional
        Number of permutations, default 1000.

    Returns
    -------
    Tuple[np.ndarray, np.ndarray, np.ndarray]
        explained_variance_ratio (components,), p_values (components,), weights (features x components)

    Notes
    -----
    - Explained variance is computed from X scores relative to total variance of X.
    - Permutation p-values quantify whether the observed explained variance per
      component exceeds the null distribution obtained by shuffling.
    """
    pls, x_weights, x_scores, y_scores = run_pls(X, Y, n_components)
    total_var_X = np.var(X, axis=0).sum()
    explained_var_X = np.var(x_scores, axis=0) / total_var_X

    # Permutation to get null distribution of explained variance per component
    null_explained = np.zeros((n_permutations, n_components))
    for i in range(n_permutations):
        X_perm, Y_perm = shuffle(X, Y, random_state=i)
        pls_perm = PLSRegression(n_components=n_components)
        pls_perm.fit(X_perm, Y_perm)
        scores_perm = pls_perm.x_scores_
        null_explained[i, :] = np.var(scores_perm, axis=0) / total_var_X

    p_values = np.mean(null_explained >= explained_var_X[None, :], axis=0)
    return explained_var_X, p_values, x_weights


def plot_rmse_and_variance(cv_errors: np.ndarray,
                           explained_variance_ratio: np.ndarray,
                           fig_outputfile: str) -> None:
    """Save two figures: CV RMSE curve and explained variance per component.

    Parameters
    ----------
    cv_errors : np.ndarray
        Mean CV RMSE per number of components.
    explained_variance_ratio : np.ndarray
        Explained variance ratio of X per component.
    fig_outputfile : str
        Base output path (two figures are saved with suffixes).
    """
    import matplotlib.pyplot as plt
    import os
    root, ext = os.path.splitext(fig_outputfile)
    rmse_path = f"{root}_RMSE{ext or '.png'}"
    var_path = f"{root}_ExplainedVariance{ext or '.png'}"
    for p in [rmse_path, var_path]:
        d = os.path.dirname(p)
        if d:
            os.makedirs(d, exist_ok=True)

    plt.figure(figsize=(6, 5))
    plt.plot(range(1, len(cv_errors) + 1), cv_errors, marker='o')
    plt.title('PLS CV RMSE')
    plt.xlabel('Components')
    plt.ylabel('RMSE')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig(rmse_path, dpi=300)
    plt.close()

    plt.figure(figsize=(6, 5))
    plt.plot(range(1, len(explained_variance_ratio) + 1), explained_variance_ratio * 100, marker='o', color='orange')
    plt.title('Explained Variance (X)')
    plt.xlabel('Components')
    plt.ylabel('Explained Variance (%)')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig(var_path, dpi=300)
    plt.close()