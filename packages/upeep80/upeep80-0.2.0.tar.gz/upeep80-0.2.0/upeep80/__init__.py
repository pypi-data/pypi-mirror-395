"""
upeep80 - Universal Peephole Optimizer for 8080/Z80

A language-agnostic optimization library for compilers targeting
the Intel 8080 and Zilog Z80 processors.
"""

__version__ = "0.2.0"
__author__ = "upeep80 project"

# Peephole optimizer is language-agnostic (works on assembly text)
from .peephole import (
    InputSyntax,
    PeepholeOptimizer,
    PeepholePattern,
    Target,
    optimize_8080,
    optimize_asm,
    optimize_peephole,
    optimize_z80,
)

__all__ = [
    # Version
    "__version__",

    # Peephole Optimization
    "InputSyntax",
    "PeepholeOptimizer",
    "PeepholePattern",
    "Target",
    "optimize_8080",
    "optimize_asm",
    "optimize_peephole",
    "optimize_z80",
]
