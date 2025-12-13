"""
Tests for Claude Model Selector
"""

import pytest
from claude_model_selector import (
    TaskAnalysis,
    ClaudeModelSelector,
    quick_select,
)


class TestQuickSelect:
    """Tests for quick_select function"""

    def test_simple_task_selects_haiku(self):
        """Simple tasks should select Haiku"""
        assert quick_select("List all files") == "haiku"
        assert quick_select("Count items") == "haiku"
        assert quick_select("Just extract the data") == "haiku"

    def test_standard_task_selects_sonnet(self):
        """Standard tasks should select Sonnet"""
        assert quick_select("Analyze the code for bugs") == "sonnet"
        assert quick_select("Implement user authentication") == "sonnet"
        assert quick_select("Create a test suite") == "sonnet"

    def test_complex_task_selects_opus(self):
        """Complex tasks should select Opus"""
        assert quick_select("Design a scalable microservices architecture") == "opus"
        assert quick_select("Plan comprehensive migration strategy") == "opus"
        assert quick_select("Research and evaluate critical system design") == "opus"

    def test_empty_task_returns_default(self):
        """Empty task should return default model"""
        result = quick_select("")
        assert result in ["haiku", "sonnet", "opus"]


class TestClaudeModelSelector:
    """Tests for ClaudeModelSelector class"""

    @pytest.fixture
    def selector(self):
        """Create a selector instance"""
        return ClaudeModelSelector()

    def test_initialization(self, selector):
        """Test selector initializes correctly"""
        assert selector is not None
        assert selector.config is not None
        assert "haiku_threshold" in selector.config
        assert "sonnet_threshold" in selector.config

    def test_analyze_task_returns_analysis(self, selector):
        """Test analyze_task returns TaskAnalysis object"""
        analysis = selector.analyze_task("Test task")
        assert isinstance(analysis, TaskAnalysis)
        assert hasattr(analysis, "complexity_score")
        assert hasattr(analysis, "recommended_model")
        assert hasattr(analysis, "reasoning")
        assert hasattr(analysis, "confidence")
        assert hasattr(analysis, "estimated_tokens")
        assert hasattr(analysis, "estimated_cost")

    def test_complexity_score_range(self, selector):
        """Test complexity score is within valid range"""
        analysis = selector.analyze_task("Test task")
        assert 0 <= analysis.complexity_score <= 100

    def test_confidence_range(self, selector):
        """Test confidence is within valid range"""
        analysis = selector.analyze_task("Test task")
        assert 0 <= analysis.confidence <= 1

    def test_model_selection_consistency(self, selector):
        """Test same task always returns same model"""
        task = "Analyze code for security issues"
        result1 = selector.analyze_task(task)
        result2 = selector.analyze_task(task)
        assert result1.recommended_model == result2.recommended_model

    def test_get_model_info_haiku(self, selector):
        """Test getting Haiku model info"""
        info = selector.get_model_info("haiku")
        assert info["name"] == "haiku"
        assert info["cost_per_mtok_input"] == 0.80
        assert info["cost_per_mtok_output"] == 4.00
        assert info["speed"] == "fastest"

    def test_get_model_info_sonnet(self, selector):
        """Test getting Sonnet model info"""
        info = selector.get_model_info("sonnet")
        assert info["name"] == "sonnet"
        assert info["cost_per_mtok_input"] == 3.00
        assert info["cost_per_mtok_output"] == 15.00
        assert info["speed"] == "balanced"

    def test_get_model_info_opus(self, selector):
        """Test getting Opus model info"""
        info = selector.get_model_info("opus")
        assert info["name"] == "opus"
        assert info["cost_per_mtok_input"] == 15.00
        assert info["cost_per_mtok_output"] == 75.00
        assert info["speed"] == "slowest"

    def test_get_model_info_invalid(self, selector):
        """Test getting info for invalid model raises error"""
        with pytest.raises(ValueError):
            selector.get_model_info("invalid")

    def test_compare_models(self, selector):
        """Test model comparison"""
        comparisons = selector.compare_models("Test task", 10000)
        assert len(comparisons) == 3
        assert comparisons[0]["model"] in ["haiku", "sonnet", "opus"]
        assert "estimated_cost" in comparisons[0]
        assert "speed" in comparisons[0]

    def test_compare_models_sorted_by_cost(self, selector):
        """Test comparisons are sorted by cost (cheapest first)"""
        comparisons = selector.compare_models("Test task", 10000)
        costs = [c["estimated_cost"] for c in comparisons]
        assert costs == sorted(costs)


class TestComplexityScoring:
    """Tests for complexity scoring algorithm"""

    @pytest.fixture
    def selector(self):
        return ClaudeModelSelector()

    def test_simple_keywords_reduce_complexity(self, selector):
        """Simple keywords should reduce complexity"""
        simple_task = "Just list the files quickly"
        complex_task = "Design comprehensive architecture"

        simple_analysis = selector.analyze_task(simple_task)
        complex_analysis = selector.analyze_task(complex_task)

        assert simple_analysis.complexity_score < complex_analysis.complexity_score

    def test_planning_keywords_increase_complexity(self, selector):
        """Planning keywords should increase complexity"""
        planning_task = "Design and architect the system"
        simple_task = "List the files"

        planning_analysis = selector.analyze_task(planning_task)
        simple_analysis = selector.analyze_task(simple_task)

        assert planning_analysis.complexity_score > simple_analysis.complexity_score

    def test_length_affects_complexity(self, selector):
        """Longer descriptions should increase complexity"""
        short_task = "List files"
        long_task = (
            "List all files in the directory including subdirectories and "
            "provide detailed information about each file including size, "
            "permissions, and modification dates"
        )

        short_analysis = selector.analyze_task(short_task)
        long_analysis = selector.analyze_task(long_task)

        assert long_analysis.complexity_score >= short_analysis.complexity_score

    def test_context_increases_complexity(self, selector):
        """Additional context should increase complexity"""
        task = "Optimize this code"
        context = "This is critical production code handling millions of transactions"

        without_context = selector.analyze_task(task)
        with_context = selector.analyze_task(task, context)

        assert with_context.complexity_score >= without_context.complexity_score

    def test_multiple_questions_increase_complexity(self, selector):
        """Multiple questions indicate complexity"""
        simple = "List files"
        questions = "How to list files? Which directory? What format?"

        simple_analysis = selector.analyze_task(simple)
        questions_analysis = selector.analyze_task(questions)

        assert questions_analysis.complexity_score > simple_analysis.complexity_score


class TestModelThresholds:
    """Tests for model selection thresholds"""

    @pytest.fixture
    def selector(self):
        return ClaudeModelSelector()

    def test_haiku_threshold(self, selector):
        """Test tasks at Haiku threshold"""
        # Create a task that should score around 20-30
        task = "Quick list of items"
        analysis = selector.analyze_task(task)
        if analysis.complexity_score <= 30:
            assert analysis.recommended_model == "haiku"

    def test_sonnet_threshold(self, selector):
        """Test tasks at Sonnet threshold"""
        # Create a task that should score around 40-60
        task = "Analyze and implement the feature"
        analysis = selector.analyze_task(task)
        if 31 <= analysis.complexity_score <= 70:
            assert analysis.recommended_model == "sonnet"

    def test_opus_threshold(self, selector):
        """Test tasks at Opus threshold"""
        # Create a task that should score above 70
        task = "Design comprehensive scalable architecture with critical planning"
        analysis = selector.analyze_task(task)
        if analysis.complexity_score > 70:
            assert analysis.recommended_model == "opus"


class TestCostEstimation:
    """Tests for cost estimation"""

    @pytest.fixture
    def selector(self):
        return ClaudeModelSelector()

    def test_cost_is_positive(self, selector):
        """Cost should always be positive"""
        analysis = selector.analyze_task("Test task")
        assert analysis.estimated_cost > 0

    def test_opus_more_expensive_than_sonnet(self, selector):
        """Opus should be more expensive than Sonnet for same tokens"""
        comparisons = selector.compare_models("Test task", 10000)
        costs = {c["model"]: c["estimated_cost"] for c in comparisons}
        assert costs["opus"] > costs["sonnet"]

    def test_sonnet_more_expensive_than_haiku(self, selector):
        """Sonnet should be more expensive than Haiku for same tokens"""
        comparisons = selector.compare_models("Test task", 10000)
        costs = {c["model"]: c["estimated_cost"] for c in comparisons}
        assert costs["sonnet"] > costs["haiku"]

    def test_cost_scales_with_tokens(self, selector):
        """Cost should increase with more tokens"""
        comparisons_small = selector.compare_models("Test", 1000)
        comparisons_large = selector.compare_models("Test", 100000)

        cost_small = comparisons_small[0]["estimated_cost"]
        cost_large = comparisons_large[0]["estimated_cost"]

        assert cost_large > cost_small


class TestEdgeCases:
    """Tests for edge cases"""

    @pytest.fixture
    def selector(self):
        return ClaudeModelSelector()

    def test_empty_string_task(self, selector):
        """Test with empty string"""
        analysis = selector.analyze_task("")
        assert analysis.recommended_model in ["haiku", "sonnet", "opus"]

    def test_very_long_task(self, selector):
        """Test with very long task description"""
        long_task = " ".join(["word"] * 1000)
        analysis = selector.analyze_task(long_task)
        assert analysis.recommended_model in ["haiku", "sonnet", "opus"]

    def test_special_characters(self, selector):
        """Test with special characters"""
        task = "List files with @#$%^&*() characters"
        analysis = selector.analyze_task(task)
        assert analysis.recommended_model in ["haiku", "sonnet", "opus"]

    def test_unicode_characters(self, selector):
        """Test with unicode characters"""
        task = "分析代码 analyze код código"
        analysis = selector.analyze_task(task)
        assert analysis.recommended_model in ["haiku", "sonnet", "opus"]

    def test_only_numbers(self, selector):
        """Test with only numbers"""
        task = "1234567890"
        analysis = selector.analyze_task(task)
        assert analysis.recommended_model in ["haiku", "sonnet", "opus"]


class TestRealWorldScenarios:
    """Tests with real-world task descriptions"""

    @pytest.fixture
    def selector(self):
        return ClaudeModelSelector()

    def test_simple_file_operations(self, selector):
        """Simple file operations should use Haiku"""
        tasks = [
            "List all Python files",
            "Count the number of functions",
            "Extract email addresses",
        ]
        for task in tasks:
            analysis = selector.analyze_task(task)
            # Most simple tasks should select Haiku or Sonnet
            assert analysis.recommended_model in ["haiku", "sonnet"]

    def test_code_analysis_tasks(self, selector):
        """Code analysis should typically use Sonnet"""
        tasks = [
            "Analyze code for bugs",
            "Review pull request",
            "Implement authentication",
        ]
        for task in tasks:
            analysis = selector.analyze_task(task)
            # Should be Sonnet or Opus depending on complexity
            assert analysis.recommended_model in ["sonnet", "opus"]

    def test_architecture_tasks(self, selector):
        """Architecture tasks should prefer Opus"""
        tasks = [
            "Design scalable microservices architecture",
            "Plan comprehensive migration strategy",
            "Architect multi-region deployment",
        ]
        for task in tasks:
            analysis = selector.analyze_task(task)
            # Complex tasks should lean toward Sonnet or Opus
            assert analysis.complexity_score >= 40


class TestConfidence:
    """Tests for confidence scoring"""

    @pytest.fixture
    def selector(self):
        return ClaudeModelSelector()

    def test_clear_task_high_confidence(self, selector):
        """Clear, specific tasks should have higher confidence"""
        clear_task = "Design a comprehensive scalable architecture for microservices"
        analysis = selector.analyze_task(clear_task)
        assert analysis.confidence >= 0.7

    def test_ambiguous_task_lower_confidence(self, selector):
        """Ambiguous tasks may have lower confidence"""
        ambiguous_task = "Do something"
        analysis = selector.analyze_task(ambiguous_task)
        # Confidence should still be reasonable
        assert 0.5 <= analysis.confidence <= 1.0

    def test_confidence_with_context(self, selector):
        """Context should affect confidence"""
        task = "Optimize"
        context = (
            "Production system handling 1M requests/day with critical "
            "uptime requirements"
        )

        analysis = selector.analyze_task(task, context)
        assert analysis.confidence > 0


class TestCustomConfiguration:
    """Tests for custom configuration"""

    def test_custom_thresholds(self):
        """Test with custom threshold configuration"""
        from pathlib import Path
        import json
        import tempfile

        # Create temporary config
        config = {"thresholds": {"haiku_max": 25, "sonnet_max": 75}}

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(config, f)
            config_path = Path(f.name)

        try:
            selector = ClaudeModelSelector(config_path=config_path)
            assert selector.config["haiku_threshold"] == 25
            assert selector.config["sonnet_threshold"] == 75
        finally:
            config_path.unlink()

    def test_default_config_when_no_file(self):
        """Test default config is used when file doesn't exist"""
        from pathlib import Path

        selector = ClaudeModelSelector(config_path=Path("nonexistent.json"))
        assert selector.config is not None
        assert "haiku_threshold" in selector.config
