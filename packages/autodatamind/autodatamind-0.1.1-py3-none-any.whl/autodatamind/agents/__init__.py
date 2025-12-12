"""
Agents - Native Intelligence Agents
====================================

6 specialized agents for automated data science.
"""

from autodatamind.agents.data_agent import DataAgent
from autodatamind.agents.profile_agent import ProfileAgent, analyze
from autodatamind.agents.viz_agent import VizAgent, dashboard
from autodatamind.agents.ml_agent import MLAgent, autotrain
from autodatamind.agents.dl_agent import DLAgent, auto_deep
from autodatamind.agents.insight_agent import InsightAgent, generate_insights

__all__ = [
    'DataAgent',
    'ProfileAgent',
    'VizAgent',
    'MLAgent',
    'DLAgent',
    'InsightAgent',
    'analyze',
    'dashboard',
    'autotrain',
    'auto_deep',
    'generate_insights',
]
