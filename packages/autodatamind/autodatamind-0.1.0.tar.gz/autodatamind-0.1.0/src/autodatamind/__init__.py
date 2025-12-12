"""
AutoDataMind
============

Your Native Automated Data & ML Engine

Zero-code data analysis, machine learning, and deep learning.
No Pandas knowledge required. No ML expertise needed.

Simple Usage:
    >>> import autodatamind as adm
    >>> adm.analyze("sales.csv")
    >>> model = adm.autotrain("sales.csv", target="revenue")
    >>> adm.dashboard("sales.csv")

Author: Idriss Olivier Bado
Email: idrissbadoolivier@gmail.com
License: MIT
"""

__version__ = "0.1.0"
__author__ = "Idriss Olivier Bado"
__email__ = "idrissbadoolivier@gmail.com"

# Import main API functions
from autodatamind.core.reader import read_data
from autodatamind.core.cleaner import autoclean
from autodatamind.agents.profile_agent import analyze
from autodatamind.agents.viz_agent import dashboard
from autodatamind.agents.ml_agent import autotrain
from autodatamind.agents.dl_agent import auto_deep
from autodatamind.agents.insight_agent import generate_insights

# Expose simple API
__all__ = [
    'read_data',
    'autoclean',
    'analyze',
    'dashboard',
    'autotrain',
    'auto_deep',
    'generate_insights',
]
