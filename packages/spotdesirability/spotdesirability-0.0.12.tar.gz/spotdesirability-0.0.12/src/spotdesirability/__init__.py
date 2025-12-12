"""
spotdesirability - a Python package for desirability function analysis.

This package provides tools for multi-objective optimization using
desirability functions, including various desirability classes,
test functions, and visualization utilities.

Version: 0.0.11
License: GPL-2.0
"""

from spotdesirability.utils.desirability import (
    DMax,
    DMin,
    DTarget,
    DArb,
    DBox,
    DCategorical,
    DOverall,
)
from spotdesirability.functions.rsm import conversion_pred, activity_pred, rsm_opt
from spotdesirability.functions.zdt import zdt1, zdt2, zdt3
from spotdesirability.plot.ccd import plotCCD

__version__ = "0.0.11"

__all__ = [
    # Desirability classes
    "DMax",
    "DMin",
    "DTarget",
    "DArb",
    "DBox",
    "DCategorical",
    "DOverall",
    # RSM functions
    "conversion_pred",
    "activity_pred",
    "rsm_opt",
    # ZDT test functions
    "zdt1",
    "zdt2",
    "zdt3",
    # Plotting
    "plotCCD",
]
