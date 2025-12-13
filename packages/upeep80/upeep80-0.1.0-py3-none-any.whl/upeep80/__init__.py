"""
upeep80 - Universal Peephole Optimizer for 8080/Z80

A language-agnostic optimization library for compilers targeting
the Intel 8080 and Zilog Z80 processors.
"""

__version__ = "0.1.0"
__author__ = "upeep80 project"

from .ast_optimizer import (
    ASTOptimizer,
    OptimizeFor,
    OptimizationStats,
    optimize_ast,
)

from .peephole import (
    PeepholeOptimizer,
    PeepholePattern,
    Target,
    optimize_asm,
)

__all__ = [
    # Version
    "__version__",

    # AST Optimization
    "ASTOptimizer",
    "OptimizeFor",
    "OptimizationStats",
    "optimize_ast",

    # Peephole Optimization
    "PeepholeOptimizer",
    "PeepholePattern",
    "Target",
    "optimize_asm",
]
