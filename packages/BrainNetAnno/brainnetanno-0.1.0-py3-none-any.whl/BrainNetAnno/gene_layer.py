import pandas as pd
import numpy as np
from typing import List, Optional, Tuple, Set
from scipy.stats import norm
from statsmodels.stats.multitest import multipletests
import os

from .utils import load_table_generic

import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger(__name__)


def load_layer_markers(excel_path: str,
                       sheet_name: str = 'Table S4B',
                       gene_col: str = 'gene',
                       layer_names: Optional[List[str]] = None,
                       t_stat_prefix: str = 't_stat_') -> Tuple[pd.DataFrame, List[str]]:
    """Load cortical layer marker statistics from an Excel file.

    Parameters
    ----------
    excel_path : str
        Path to the Excel file containing layer-specific marker statistics.
    sheet_name : str, optional
        Sheet name to read, by default 'Table S4B'.
    gene_col : str, optional
        Column name for gene symbols, by default 'gene'.
    layer_names : Optional[List[str]], optional
        List of layer names (e.g., ['Layer1', 'Layer2', ...]). If None, infer
        from columns beginning with `t_stat_prefix`, by default None.
    t_stat_prefix : str, optional
        Prefix of t-statistic columns for each layer (e.g., 't_stat_'), by default 't_stat_'.

    Returns
    -------
    Tuple[pd.DataFrame, List[str]]
        A tuple of (gene_tvals, layers). `gene_tvals` is a DataFrame indexed by gene symbol
        with columns for each layer's t-statistic. `layers` is the ordered list of layers used.
    """
    df = load_table_generic(excel_path, sheet_name=sheet_name)
    df[gene_col] = df[gene_col].astype(str).str.upper()

    if layer_names is None:
        layer_names = [c.replace(t_stat_prefix, '') for c in df.columns if c.startswith(t_stat_prefix)]

    layer_cols = [f"{t_stat_prefix}{l}" for l in layer_names]
    missing = [c for c in layer_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Missing layer t-stat columns: {missing}")

    gene_tvals = df.set_index(gene_col)[layer_cols]
    return gene_tvals, layer_names


def load_target_genes(csv_path: str,
                      gene_col: str = 'Gene Index',
                      uppercase: bool = True) -> Set[str]:
    """Load target genes from a CSV file.

    Parameters
    ----------
    csv_path : str
        Path to the CSV containing the target genes.
    gene_col : str, optional
        Column name for gene symbols, by default 'Gene Index'.
    uppercase : bool, optional
        Whether to uppercase gene symbols, by default True.

    Returns
    -------
    Set[str]
        Set of target gene symbols.
    """
    df = load_table_generic(csv_path)
    genes = df[gene_col].astype(str)
    return set(genes.str.upper() if uppercase else genes)


def compute_layer_enrichment(gene_tvals: pd.DataFrame,
                             target_genes: Set[str],
                             n_perm: int = 5000,
                             random_state: Optional[int] = 42) -> pd.DataFrame:
    """Permutation-based enrichment test of target genes across cortical layers.

    For each layer, compute the mean t-statistic of the target genes and compare
    against a null distribution built by randomly sampling gene sets of the same size.

    Parameters
    ----------
    gene_tvals : pd.DataFrame
        DataFrame indexed by gene symbol; columns are layer t-statistics.
    target_genes : Set[str]
        Set of target genes to evaluate.
    n_perm : int, optional
        Number of permutations, by default 5000.
    random_state : Optional[int], optional
        Seed for reproducibility, by default 42.

    Returns
    -------
    pd.DataFrame
        Results with columns: Layer, Z-Score, Raw P-Value, FDR, Mean t (Target Genes), Mean t (Random)
    """
    if len(target_genes) == 0:
        raise ValueError("No target genes provided.")

    # Intersect target genes with available markers
    intersect_genes = list(set(target_genes).intersection(gene_tvals.index))
    if len(intersect_genes) == 0:
        raise ValueError("None of the target genes were found in layer markers.")

    true_mean_t = gene_tvals.loc[intersect_genes].mean()

    rng = np.random.default_rng(random_state)
    all_genes = gene_tvals.index.to_list()
    n_target = len(intersect_genes)

    perm_means = np.zeros((n_perm, gene_tvals.shape[1]))
    for i in range(n_perm):
        sampled_genes = rng.choice(all_genes, n_target, replace=False)
        perm_means[i, :] = gene_tvals.loc[sampled_genes].mean().values

    perm_mean = perm_means.mean(axis=0)
    perm_std = perm_means.std(axis=0, ddof=0)
    z_scores = (true_mean_t.values - perm_mean) / np.where(perm_std > 0, perm_std, np.inf)

    # Two-sided p-values using normal approximation
    p_values = 2 * norm.sf(np.abs(z_scores))

    # FDR correction
    _, p_fdr, _, _ = multipletests(p_values, method='fdr_bh')

    layers = [c for c in gene_tvals.columns]
    result_df = pd.DataFrame({
        'Layer': layers,
        'Z-Score': z_scores,
        'Raw P-Value': p_values,
        'FDR': p_fdr,
        'Mean t (Target Genes)': true_mean_t.values,
        'Mean t (Random)': perm_mean,
    })

    return result_df.sort_values('FDR').reset_index(drop=True)


def run_pipeline(layer_marker_path: str,
                 target_genes_path: str,
                 output_path: Optional[str] = None,
                 sheet_name: str = 'Table S4B',
                 gene_col: str = 'gene',
                 target_gene_col: str = 'Gene Index',
                 layer_names: Optional[List[str]] = None,
                 t_stat_prefix: str = 't_stat_',
                 n_perm: int = 5000,
                 random_state: Optional[int] = 42) -> pd.DataFrame:
    """Run cortical layer enrichment analysis and optionally save results.

    This high-level pipeline loads layer-specific marker statistics from an
    Excel file and a list of target genes from a CSV file, performs a
    permutation-based enrichment test to assess whether the target genes are
    enriched in specific cortical layers, and returns a sorted results
    DataFrame. If an output path is provided, results are written to CSV.

    Parameters
    ----------
    layer_marker_path : str
        Path to the Excel file containing cortical layer marker statistics.
        The file must include a gene column (specified by ``gene_col``) and
        one or more t-statistic columns whose names begin with ``t_stat_prefix``.
    target_genes_path : str
        Path to the CSV file containing the list of target genes to evaluate.
        The file must include a gene column (specified by ``target_gene_col``).
    output_csv : Optional[str], optional
        If provided, the pipeline will save the resulting enrichment table to
        this CSV path. Parent directories are created automatically.
        Default is ``None`` (do not save).
    sheet_name : str, optional
        Name of the Excel sheet to read from ``layer_marker_path``. Default is
        ``'Table S4B'``.
    gene_col : str, optional
        Column name for gene symbols in the Excel file. Default is ``'gene'``.
    target_gene_col : str, optional
        Column name for gene symbols in the target CSV file. Default is
        ``'Gene Index'``.
    layer_names : Optional[List[str]], optional
        Explicit list of layer names to use (e.g., ``['Layer1','Layer2',...]``).
        If ``None``, layer names are inferred from columns beginning with
        ``t_stat_prefix``. Default is ``None``.
    t_stat_prefix : str, optional
        Prefix used by t-statistic columns for each layer (e.g., ``'t_stat_'``).
        Default is ``'t_stat_'``.
    n_perm : int, optional
        Number of permutations for the null distribution when computing
        enrichment statistics. Larger values improve stability but increase
        runtime. Default is ``5000``.
    random_state : Optional[int], optional
        Random seed for reproducibility of permutations. Default is ``42``.

    Returns
    -------
    pd.DataFrame
        A DataFrame sorted by the Benjamini–Hochberg FDR, with columns:
        - ``Layer``: Layer name.
        - ``Z-Score``: Z-score comparing target mean t-statistic vs. null.
        - ``Raw P-Value``: Two-sided p-value from the normal approximation.
        - ``FDR``: Benjamini–Hochberg adjusted p-value.
        - ``Mean t (Target Genes)``: Mean t-statistic across target genes.
        - ``Mean t (Random)``: Mean t-statistic across permutation samples.

    Notes
    -----
    - The set of target genes is intersected with the genes available in the
      layer markers; an error is raised if the intersection is empty.
    - Parent directories for ``output_csv`` are created automatically when
      saving results.
    """
    logger.info(f"Loading layer markers from: {layer_marker_path} (sheet={sheet_name})")
    gene_tvals, layers = load_layer_markers(
        excel_path=layer_marker_path,
        sheet_name=sheet_name,
        gene_col=gene_col,
        layer_names=layer_names,
        t_stat_prefix=t_stat_prefix,
    )
    logger.info(f"Loaded markers. Layers: {layers}; genes: {gene_tvals.shape[0]}")

    logger.info(f"Loading target genes from: {target_genes_path} (col={target_gene_col})")
    targets = load_target_genes(target_genes_path, gene_col=target_gene_col)
    logger.info(f"Target genes loaded: {len(targets)}")

    logger.info(f"Running enrichment (n_perm={n_perm}, random_state={random_state})")
    result_df = compute_layer_enrichment(gene_tvals, targets, n_perm=n_perm, random_state=random_state)

    if output_path:
        import os
        d = os.path.dirname(output_path)
        if d:
            os.makedirs(d, exist_ok=True)
        result_df.to_csv(output_path, index=False)
        logger.info(f"Saved layer enrichment results to: {output_path}")

    logger.info("Layer enrichment pipeline completed successfully.")
    return result_df
