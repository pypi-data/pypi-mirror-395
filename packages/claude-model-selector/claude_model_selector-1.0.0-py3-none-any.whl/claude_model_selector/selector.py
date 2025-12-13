"""
Claude Model Selector
Intelligently selects the most cost-effective Claude model for each task
"""

import re
import json
from typing import Dict, Optional, List
from dataclasses import dataclass
from pathlib import Path
from enum import Enum


class ClaudeModel(Enum):
    """Available Claude models with pricing"""

    HAIKU = {
        "name": "haiku",
        "cost_per_mtok_input": 0.80,  # $0.80 per million input tokens
        "cost_per_mtok_output": 4.00,  # $4.00 per million output tokens
        "speed": "fastest",
        "use_cases": ["simple", "quick", "straightforward"],
    }
    SONNET = {
        "name": "sonnet",
        "cost_per_mtok_input": 3.00,  # $3.00 per million input tokens
        "cost_per_mtok_output": 15.00,  # $15.00 per million output tokens
        "speed": "balanced",
        "use_cases": ["reliable", "common", "standard"],
    }
    OPUS = {
        "name": "opus",
        "cost_per_mtok_input": 15.00,  # $15.00 per million input tokens
        "cost_per_mtok_output": 75.00,  # $75.00 per million output tokens
        "speed": "slowest",
        "use_cases": ["complex", "planning", "strategic", "critical"],
    }


@dataclass
class TaskAnalysis:
    """Analysis results for a task"""

    complexity_score: float  # 0-100
    recommended_model: str  # "haiku", "sonnet", or "opus"
    reasoning: str
    confidence: float  # 0-1
    estimated_tokens: int
    estimated_cost: float


class ClaudeModelSelector:
    """
    Intelligently selects the most cost-effective Claude model for tasks

    Model Selection Strategy:
    - Haiku (0-30): Simple, quick tasks, straightforward operations
    - Sonnet (31-70): Standard reliability tasks, common operations
    - Opus (71-100): Complex planning, strategic thinking, critical tasks
    """

    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize the model selector

        Args:
            config_path: Path to configuration file (optional)
        """
        self.config = self._load_config(config_path)

        # Complexity indicators
        self.complexity_keywords = {
            "haiku": {
                "keywords": [
                    "simple",
                    "quick",
                    "basic",
                    "straightforward",
                    "easy",
                    "list",
                    "summarize",
                    "extract",
                    "format",
                    "convert",
                    "read",
                    "check",
                    "verify",
                    "validate",
                    "count",
                ],
                "weight": -30,  # Reduces complexity score
            },
            "sonnet": {
                "keywords": [
                    "analyze",
                    "review",
                    "implement",
                    "create",
                    "develop",
                    "write",
                    "generate",
                    "build",
                    "process",
                    "handle",
                    "parse",
                    "transform",
                    "optimize",
                    "refactor",
                    "test",
                ],
                "weight": 5,  # Slight increase for standard tasks
            },
            "opus": {
                "keywords": [
                    "plan",
                    "design",
                    "architect",
                    "strategy",
                    "complex",
                    "critical",
                    "research",
                    "investigate",
                    "evaluate",
                    "comprehensive",
                    "multi-step",
                    "advanced",
                    "deep dive",
                    "trade-off",
                    "decision",
                    "compare",
                    "assess",
                    "scalable",
                    "microservice",
                ],
                "weight": 60,  # Increases complexity score
            },
        }

        # Task type patterns
        self.task_patterns = {
            "planning": {
                "patterns": [
                    r"\bplan\b",
                    r"\bdesign\b",
                    r"\barchitect",
                    r"\bstrateg",
                    r"\broadmap\b",
                    r"\bapproach\b",
                    r"\bmethodology\b",
                ],
                "weight": 105,
            },
            "coding_complex": {
                "patterns": [
                    r"\bmulti[- ]step\b",
                    r"\bcomplex\s+\w+\s+system\b",
                    r"\brefactor\s+entire\b",
                    r"\bredesign\b",
                    r"\bmigrat(e|ion)\b",
                    r"\bscalability\b",
                ],
                "weight": 45,
            },
            "research": {
                "patterns": [
                    r"\bresearch\b",
                    r"\binvestigat\b",
                    r"\banalyz\b.*\bdeep",
                    r"\bcomprehensive\b",
                    r"\bexplor\b.*\boption",
                ],
                "weight": 50,
            },
            "decision_making": {
                "patterns": [
                    r"\btrade[- ]off\b",
                    r"\bcompare\s+\w+\s+approach",
                    r"\bevaluate\s+option",
                    r"\bdecid\b.*\bbest\b",
                    r"\brecommend\b.*\bstrategy\b",
                ],
                "weight": 45,
            },
            "simple_task": {
                "patterns": [
                    r"\blist\s+\w+\b",
                    r"\bcount\s+\w+\b",
                    r"\bextract\s+\w+\b",
                    r"\bformat\s+\w+\b",
                    r"\bconvert\s+\w+\s+to\s+\w+\b",
                ],
                "weight": -30,
            },
        }

    def _load_config(self, config_path: Optional[Path]) -> Dict:
        """Load configuration from file or use defaults"""
        if config_path and config_path.exists():
            with open(config_path) as f:
                config = json.load(f)
                # Handle nested thresholds structure
                if "thresholds" in config:
                    thresholds = config["thresholds"]
                    config["haiku_threshold"] = thresholds.get("haiku_max", 30)
                    config["sonnet_threshold"] = thresholds.get("sonnet_max", 70)
                return config
        return {
            "haiku_threshold": 30,
            "sonnet_threshold": 70,
            "default_model": "sonnet",
            "cost_optimization": True,
        }

    def analyze_task(
        self, task_description: str, context: Optional[str] = None
    ) -> TaskAnalysis:
        """
        Analyze a task and recommend the best model

        Args:
            task_description: Description of the task to perform
            context: Additional context (optional)

        Returns:
            TaskAnalysis with recommendation
        """
        # Calculate complexity score
        complexity_score = self._calculate_complexity(task_description, context)

        # Select model based on complexity
        model_name = self._select_model(complexity_score)

        # Generate reasoning
        reasoning = self._generate_reasoning(
            task_description, complexity_score, model_name
        )

        # Estimate tokens and cost
        estimated_tokens = self._estimate_tokens(task_description, context)
        estimated_cost = self._estimate_cost(model_name, estimated_tokens)

        # Calculate confidence
        confidence = self._calculate_confidence(task_description, complexity_score)

        return TaskAnalysis(
            complexity_score=complexity_score,
            recommended_model=model_name,
            reasoning=reasoning,
            confidence=confidence,
            estimated_tokens=estimated_tokens,
            estimated_cost=estimated_cost,
        )

    def _calculate_complexity(self, task: str, context: Optional[str] = None) -> float:
        """
        Calculate complexity score (0-100)

        Higher score = more complex = use better model
        """
        score = 40.0  # Base score
        task_lower = task.lower()

        # Check complexity keywords
        for model_type, config in self.complexity_keywords.items():
            for keyword in config["keywords"]:  # type: ignore
                if keyword in task_lower:
                    score += config["weight"] / len(config["keywords"])  # type: ignore

        # Check task patterns
        for pattern_type, config in self.task_patterns.items():
            for pattern in config["patterns"]:  # type: ignore
                if re.search(pattern, task_lower):
                    score += config["weight"] / len(config["patterns"])  # type: ignore

        # Length factor (longer descriptions often mean more complexity)
        word_count = len(task.split())
        if word_count > 100:
            score += 15
        elif word_count > 50:
            score += 10
        elif word_count < 5:
            score -= 10
        elif word_count < 10:
            score -= 5

        # Context adds complexity
        if context:
            score += min(len(context.split()) / 20, 15)

        # Question marks might indicate uncertainty/complexity
        question_count = task.count("?")
        if question_count > 2:
            score += question_count * 5

        # Multiple conditions or steps
        if any(
            word in task_lower
            for word in ["and then", "after that", "also", "additionally"]
        ):
            score += 10

        # Negative indicators (simple tasks)
        if any(word in task_lower for word in ["just", "simply", "only", "quick"]):
            score -= 15

        # Clamp to 0-100
        return max(0, min(100, score))

    def _select_model(self, complexity_score: float) -> str:
        """Select model based on complexity score"""
        haiku_threshold = self.config.get("haiku_threshold", 30)
        sonnet_threshold = self.config.get("sonnet_threshold", 70)

        if complexity_score <= haiku_threshold:
            return "haiku"
        elif complexity_score <= sonnet_threshold:
            return "sonnet"
        else:
            return "opus"

    def _generate_reasoning(self, task: str, score: float, model: str) -> str:
        """Generate explanation for model selection"""
        reasons = []

        # Complexity-based reasoning
        if score < 30:
            reasons.append("Task appears straightforward and simple")
        elif score < 50:
            reasons.append("Task has moderate complexity")
        elif score < 70:
            reasons.append("Task requires reliable, standard processing")
        else:
            reasons.append("Task is complex and requires advanced reasoning")

        # Model-specific reasoning
        if model == "haiku":
            reasons.append("Haiku is fastest and most cost-effective for this task")
        elif model == "sonnet":
            reasons.append("Sonnet provides optimal balance of quality and cost")
        else:
            reasons.append("Opus recommended for critical thinking and planning")

        # Keyword-based reasoning
        task_lower = task.lower()
        if "plan" in task_lower or "design" in task_lower:
            reasons.append("Planning/design tasks benefit from Opus capabilities")
        if "quick" in task_lower or "simple" in task_lower:
            reasons.append("Quick/simple task suited for faster models")

        return "; ".join(reasons)

    def _estimate_tokens(self, task: str, context: Optional[str] = None) -> int:
        """
        Estimate token count for the task

        Rough estimation: 1 token ≈ 4 characters for English
        """
        total_chars = len(task)
        if context:
            total_chars += len(context)

        # Add estimate for system prompts and overhead
        total_chars += 500  # System prompt overhead

        # Add estimate for output (assume 2x input for average task)
        estimated_tokens = int((total_chars / 4) * 3)

        return estimated_tokens

    def _estimate_cost(self, model_name: str, tokens: int) -> float:
        """
        Estimate cost for the task

        Args:
            model_name: Name of the model
            tokens: Estimated total tokens (input + output)

        Returns:
            Estimated cost in USD
        """
        model_enum = ClaudeModel[model_name.upper()]
        model_info = model_enum.value

        # Assume 40% input, 60% output tokens
        input_tokens = int(tokens * 0.4)
        output_tokens = int(tokens * 0.6)

        input_cost = (input_tokens / 1_000_000) * model_info[  # type: ignore
            "cost_per_mtok_input"
        ]
        output_cost = (output_tokens / 1_000_000) * model_info[  # type: ignore
            "cost_per_mtok_output"
        ]

        return input_cost + output_cost

    def _calculate_confidence(self, task: str, score: float) -> float:
        """Calculate confidence in the recommendation (0-1)"""
        confidence = 0.7  # Base confidence

        # High confidence for extreme scores
        if score < 20 or score > 80:
            confidence = 0.95
        elif score < 35 or score > 65:
            confidence = 0.85

        # Lower confidence for ambiguous tasks
        if len(task.split()) < 5:
            confidence -= 0.15

        # Higher confidence for clear indicators
        task_lower = task.lower()
        clear_indicators = ["plan", "design", "simple", "quick", "complex", "critical"]
        if any(word in task_lower for word in clear_indicators):
            confidence += 0.1

        return max(0.5, min(1.0, confidence))

    def get_model_info(self, model_name: str) -> Dict:
        """Get detailed information about a model"""
        try:
            model_enum = ClaudeModel[model_name.upper()]
            return model_enum.value
        except KeyError:
            raise ValueError(f"Unknown model: {model_name}")

    def compare_models(self, task: str, estimated_tokens: int = 10000) -> List[Dict]:
        """
        Compare all models for a given task

        Args:
            task: Task description
            estimated_tokens: Token estimate for comparison

        Returns:
            List of model comparisons with costs
        """
        comparisons = []

        for model_enum in ClaudeModel:
            model_info = model_enum.value
            cost = self._estimate_cost(
                model_info["name"], estimated_tokens  # type: ignore
            )

            comparisons.append(
                {
                    "model": model_info["name"],
                    "speed": model_info["speed"],
                    "estimated_cost": cost,
                    "use_cases": model_info["use_cases"],
                }
            )

        return sorted(comparisons, key=lambda x: x["estimated_cost"])


def quick_select(task: str) -> str:
    """
    Quick model selection without full analysis

    Args:
        task: Task description

    Returns:
        Model name (haiku, sonnet, or opus)
    """
    selector = ClaudeModelSelector()
    analysis = selector.analyze_task(task)
    return analysis.recommended_model


if __name__ == "__main__":
    # Example usage
    selector = ClaudeModelSelector()

    test_tasks = [
        "List all Python files in the project",
        "Analyze the codebase and suggest improvements",
        "Design a scalable architecture for the video processing pipeline",
        "Convert this JSON to CSV format",
        "Create a comprehensive strategy for migrating to microservices",
        "Quick fix: add error handling to the function",
    ]

    print("=" * 80)
    print("CLAUDE MODEL SELECTOR - Test Results")
    print("=" * 80)

    for task in test_tasks:
        analysis = selector.analyze_task(task)
        print(f"\nTask: {task}")
        print(f"  Model: {analysis.recommended_model.upper()}")
        print(f"  Complexity: {analysis.complexity_score:.1f}/100")
        print(f"  Confidence: {analysis.confidence:.0%}")
        print(f"  Est. Cost: ${analysis.estimated_cost:.6f}")
        print(f"  Reasoning: {analysis.reasoning}")
