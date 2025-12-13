import pandas as pd
import numpy as np
from scipy.stats import norm
from statsmodels.stats.multitest import multipletests
from typing import Dict, Set, Iterable, Tuple, Optional
import logging
import os
from .utils import load_table_generic

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger(__name__)


def load_celltype_markers(csv_path: str,
                          gene_col: str = 'gene',
                          celltype_col: str = 'class',
                          uppercase: bool = True) -> Tuple[pd.DataFrame, Dict[str, Set[str]], Set[str]]:
    """Load cell-type marker table and build marker sets per cell type.

    Parameters
    ----------
    csv_path : str
        Path to a CSV file containing marker genes with columns for gene names and cell-type labels.
    gene_col : str, optional
        Column name for gene symbols, by default 'gene'.
    celltype_col : str, optional
        Column name for cell-type labels, by default 'class'.
    uppercase : bool, optional
        Whether to uppercase all gene symbols, by default True.

    Returns
    -------
    Tuple[pd.DataFrame, Dict[str, Set[str]], Set[str]]
        - Original DataFrame (with gene column possibly uppercased)
        - Mapping from cell-type to its marker gene set
        - Background gene set (all unique marker genes)
    """
    df = load_table_generic(csv_path)
    if uppercase:
        df[gene_col] = df[gene_col].astype(str).str.upper()
    cell_types = df[celltype_col].unique()
    markers: Dict[str, Set[str]] = {ct: set(df[df[celltype_col] == ct][gene_col]) for ct in cell_types}
    background: Set[str] = set(df[gene_col].unique())
    return df, markers, background


def load_target_genes(csv_path: str,
                      gene_col: str = 'Gene Index',
                      uppercase: bool = True) -> Set[str]:
    """Load target gene list from CSV.

    Parameters
    ----------
    csv_path : str
        Path to the CSV containing the target gene list.
    gene_col : str, optional
        Column name that holds gene symbols, by default 'Gene Index'.
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


def compute_overlap_enrichment(celltype_markers: Dict[str, Set[str]],
                               target_genes: Set[str],
                               background_genes: Optional[Set[str]] = None,
                               n_perm: int = 5000,
                               random_state: Optional[int] = 42) -> pd.DataFrame:
    """Compute enrichment of target genes in cell-type marker sets via permutation test.

    Parameters
    ----------
    celltype_markers : Dict[str, Set[str]]
        Mapping from cell-type name to its marker gene set.
    target_genes : Set[str]
        Set of target genes to test for enrichment.
    background_genes : Optional[Set[str]], optional
        Background gene universe to sample from. If None, use the union of all marker genes.
    n_perm : int, optional
        Number of permutations for null distribution, by default 5000.
    random_state : Optional[int], optional
        Random seed for reproducibility, by default 42.

    Returns
    -------
    pd.DataFrame
        DataFrame with columns: Cell Type, Overlap, Z-Score, Raw P-Value, Mean Overlap (Random), FDR
    """
    if background_genes is None:
        background_genes = set().union(*celltype_markers.values())
    target_genes = set(target_genes)

    true_overlaps = {ct: len(target_genes & markers) for ct, markers in celltype_markers.items()}

    rng = np.random.default_rng(random_state)
    bg_list = list(background_genes)
    n_target = len(target_genes)

    perm_counts = {ct: [] for ct in celltype_markers}
    for _ in range(n_perm):
        sampled = set(rng.choice(bg_list, n_target, replace=False))
        for ct, markers in celltype_markers.items():
            perm_counts[ct].append(len(sampled & markers))

    results = []
    for ct, true_val in true_overlaps.items():
        perm_vals = np.asarray(perm_counts[ct], dtype=float)
        mean_perm = perm_vals.mean()
        std_perm = perm_vals.std(ddof=0)
        z = (true_val - mean_perm) / std_perm if std_perm > 0 else 0.0
        p = float(2 * norm.sf(abs(z))) if std_perm > 0 else 1.0
        results.append({
            'Cell Type': ct,
            'Overlap': int(true_val),
            'Z-Score': float(z),
            'Raw P-Value': p,
            'Mean Overlap (Random)': float(mean_perm)
        })

    result_df = pd.DataFrame(results)
    result_df['FDR'] = multipletests(result_df['Raw P-Value'], method='fdr_bh')[1]
    return result_df

def run_pipeline(
    celltype_path: str,
    target_genes_path: str,
    output_path: str,
    marker_gene_col: str = 'gene',
    celltype_col: str = 'class',
    target_gene_col: str = 'Gene Index',
    n_perm: int = 5000,
    random_state: Optional[int] = 42,
) -> pd.DataFrame:
    """Run cell-type enrichment analysis and optionally save results.

    This high-level pipeline loads a table of cell-type marker genes from a CSV
    file and a list of target genes from another CSV, performs a permutation-
    based enrichment test to assess whether the target genes are overrepresented
    within specific cell types, and returns a sorted results DataFrame. If an
    output path is provided, results are written to CSV.

    Parameters
    ----------
    celltype_csv : str
        Path to the CSV containing cell-type marker genes and their associated
        labels/scores. Must include the columns specified by ``gene_col`` and
        ``celltype_col``. Optionally a score column (``score_col``) may be
        present and used upstream.
    target_genes_csv : str
        Path to the CSV containing the list of target genes to evaluate. Must
        include the gene column specified by ``target_gene_col``.
    output_csv : str
        Path to save the resulting enrichment table as CSV. Parent directories
        are created automatically.
    marker_gene_col : str, optional
        Column name for marker gene symbols in the marker CSV, by default 'gene'.
    celltype_col : str, optional
        Column name in ``celltype_csv`` holding cell-type labels. Default is
        ``'CellType'``.
    target_gene_col : str, optional
        Column name for gene symbols in ``target_genes_csv``. Default is
        ``'Gene Index'``.
    n_perm : int, optional
        Number of permutations used to form the null distribution when
        computing enrichment statistics. Larger values improve stability but
        increase runtime. Default is ``5000``.
    random_state : Optional[int], optional
        Random seed for reproducibility of permutations. Default is ``42``.

    Returns
    -------
    pd.DataFrame
        A DataFrame sorted by the Benjamini–Hochberg FDR, with columns:
        - ``Cell Type``: Cell-type name.
        - ``Overlap``: Observed overlap count of target genes with markers.
        - ``Z-Score``: Z-score comparing observed overlap vs. null.
        - ``Raw P-Value``: Two-sided p-value from the normal approximation.
        - ``Mean Overlap (Random)``: Mean overlap from permutation samples.
        - ``FDR``: Benjamini–Hochberg adjusted p-value.

    Notes
    -----
    - The background gene universe is taken as the union of all marker genes
      unless ``background_genes`` is provided upstream.
    - Parent directories for ``output_csv`` are created automatically when
      saving results.
    """
    logger.info(f"Loading cell type markers from: {celltype_path}")
    try:
        _, markers, background = load_celltype_markers(celltype_path, gene_col=marker_gene_col, celltype_col=celltype_col)

    except Exception as e:
        logger.error(f"Failed to read celltype CSV: {e}")
        raise
    logger.info(f"Markers loaded. Cell types: {len(markers)}; background genes: {len(background)}")

    logger.info(f"Loading target genes from: {target_genes_path} (col={target_gene_col})")
    try:
        targets = load_target_genes(target_genes_path, gene_col=target_gene_col)
    except Exception as e:
        logger.error(f"Failed to read target genes CSV: {e}")
        raise
    logger.info(f"Target genes loaded: {len(targets)}")

    logger.info(f"Running cell type enrichment (n_perm={n_perm}, random_state={random_state})")
    result_df = compute_overlap_enrichment(markers, targets, background_genes=background, n_perm=n_perm, random_state=random_state)

    logger.info(f"Saving results to: {output_path}")

    d = os.path.dirname(output_path)
    if d:
        os.makedirs(d, exist_ok=True)
    result_df.to_csv(output_path, index=False)
    logger.info(f"Saved cell type enrichment results to: {output_path}")

    logger.info("Cell type enrichment pipeline completed successfully.")
    return result_df