"""
PromptMachine Eval - LLM Evaluation Framework

A comprehensive toolkit for evaluating and comparing Large Language Models
using ELO ratings, arena battles, and benchmark testing.

Example:
    >>> from promptmachine_eval import EloCalculator, BattleRunner
    >>> 
    >>> # Calculate ELO changes
    >>> elo = EloCalculator()
    >>> new_a, new_b = elo.update_ratings(1200, 1000, score_a=1.0)
    >>> 
    >>> # Run a battle
    >>> runner = BattleRunner(openai_api_key="sk-...")
    >>> result = await runner.battle("Write a poem", "gpt-4o", "gpt-4o-mini")

Links:
    - Documentation: https://promptmachine.io/docs/eval
    - GitHub: https://github.com/framersai/promptmachine
    - PyPI: https://pypi.org/project/promptmachine-eval/
"""

from promptmachine_eval.elo import EloCalculator, EloConfig, EloUpdateResult
from promptmachine_eval.matchmaking import MatchmakingService, MatchmakingConfig, ModelInfo
from promptmachine_eval.runner import PromptTester, TestResult
from promptmachine_eval.battle import BattleRunner, BattleResult, Judgement
from promptmachine_eval.cost import CostTracker, CostEstimate, MODEL_PRICING

__version__ = "0.1.0"
__author__ = "Frame.dev"
__email__ = "hello@frame.dev"

__all__ = [
    # Version
    "__version__",
    
    # ELO
    "EloCalculator",
    "EloConfig", 
    "EloUpdateResult",
    
    # Matchmaking
    "MatchmakingService",
    "MatchmakingConfig",
    "ModelInfo",
    
    # Testing
    "PromptTester",
    "TestResult",
    
    # Battles
    "BattleRunner",
    "BattleResult",
    "Judgement",
    
    # Costs
    "CostTracker",
    "CostEstimate",
    "MODEL_PRICING",
]

