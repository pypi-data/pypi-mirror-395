"""
Claude Model Selector

Intelligent model selection for optimal cost-effectiveness with Anthropic's Claude AI.

Copyright (c) 2025 AeonBridge Co.
Licensed under the MIT License.
"""

__version__ = "1.0.0"
__author__ = "AeonBridge Co."
__email__ = "support@aeonbridge.com"
__license__ = "MIT"

from .selector import (
    ClaudeModel,
    TaskAnalysis,
    ClaudeModelSelector,
    quick_select,
)

__all__ = [
    "ClaudeModel",
    "TaskAnalysis",
    "ClaudeModelSelector",
    "quick_select",
]
