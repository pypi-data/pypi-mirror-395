"""
Optimization passes for IR transformation.

Custom passes extend the base Transform interface.
"""

from .batch_optimization import BatchOptimizationPass

__all__ = ["BatchOptimizationPass"]

