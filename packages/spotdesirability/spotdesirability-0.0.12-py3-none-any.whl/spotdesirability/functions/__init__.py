"""
Functions module for spotdesirability.

This module provides various test functions and optimization functions
for desirability analysis and response surface methodology.
"""

from spotdesirability.functions.rsm import conversion_pred, activity_pred, rsm_opt
from spotdesirability.functions.zdt import zdt1, zdt2, zdt3

__all__ = [
    "conversion_pred",
    "activity_pred",
    "rsm_opt",
    "zdt1",
    "zdt2",
    "zdt3",
]
