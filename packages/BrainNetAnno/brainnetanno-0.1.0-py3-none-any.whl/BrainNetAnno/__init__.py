# src/BrainNetAnno/__init__.py

"""
BrainNetAnno

A toolkit for molecular annotation of brain networks, integrating transcriptome, neurotransmitters, and mitochondria.
"""

__version__ = "0.1.0"

# 公共高层 API 导出（保持与模块函数名一致）
from .transcriptome import run_transcriptome_pipeline  # noqa: F401
from .mitochondrial import run_mitochondrial_pipeline  # noqa: F401
from .neurotransmitter import run_neurotransmitter_pipeline  # noqa: F401
from .transcriptome_pls_cge import run_transcriptome_pls_pipeline  # noqa: F401
from .mitochondrial_pls_cge import run_mitochondrial_pls_pipeline  # noqa: F401
from .neurotransmitter_pls_cge import run_neurotransmitter_pls_pipeline  # noqa: F401
from .gene_celltype import run_pipeline as gene_celltype_pipeline  # noqa: F401
from .gene_layer import run_pipeline as gene_layer_pipeline  # noqa: F401