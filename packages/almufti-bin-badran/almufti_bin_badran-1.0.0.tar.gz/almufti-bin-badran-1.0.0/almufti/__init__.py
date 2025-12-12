"""
المفتي بن بدران - Almufti Bin Badran
A lightweight AI assistant with Arabic language support
"""

__version__ = "1.0.0"
__author__ = "Almufti Development Team"
__email__ = "dev@almufti.ai"

from almufti.core.chat_engine import ChatEngine
from almufti.search.web_search import WebSearch
from almufti.learning.continuous_learning import ContinuousLearning
from almufti.homework.math_solver import MathSolver
from almufti.database.db_manager import DatabaseManager

__all__ = [
    "ChatEngine",
    "WebSearch",
    "ContinuousLearning",
    "MathSolver",
    "DatabaseManager",
]
