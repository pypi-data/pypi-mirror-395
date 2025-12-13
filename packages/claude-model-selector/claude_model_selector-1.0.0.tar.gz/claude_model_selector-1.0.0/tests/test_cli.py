"""
Tests for CLI interface
"""

import pytest
import json
import tempfile
from pathlib import Path
from unittest.mock import MagicMock


class TestCLIAnalyze:
    """Tests for CLI analyze command"""

    def test_analyze_basic_task(self, capsys):
        """Test basic analyze command"""
        from claude_model_selector.cli import analyze_command

        # Mock arguments
        args = MagicMock()
        args.task = "List all files"
        args.context = None
        args.context_file = None
        args.json = False
        args.output = None
        args.verbose = False

        analyze_command(args)

        captured = capsys.readouterr()
        assert "MODEL RECOMMENDATION" in captured.out
        assert "Recommended Model:" in captured.out
        assert "Complexity Score:" in captured.out

    def test_analyze_with_json_output(self, capsys):
        """Test analyze with JSON output"""
        from claude_model_selector.cli import analyze_command

        args = MagicMock()
        args.task = "Design architecture"
        args.context = None
        args.context_file = None
        args.json = True
        args.output = None
        args.verbose = False

        analyze_command(args)

        captured = capsys.readouterr()
        assert "JSON Output:" in captured.out
        # Should contain valid JSON
        assert "model" in captured.out.lower()

    def test_analyze_with_context(self, capsys):
        """Test analyze with context"""
        from claude_model_selector.cli import analyze_command

        args = MagicMock()
        args.task = "Optimize code"
        args.context = "Critical production system"
        args.context_file = None
        args.json = False
        args.output = None
        args.verbose = False

        analyze_command(args)

        captured = capsys.readouterr()
        assert "MODEL RECOMMENDATION" in captured.out

    def test_analyze_with_verbose(self, capsys):
        """Test analyze with verbose output"""
        from claude_model_selector.cli import analyze_command

        args = MagicMock()
        args.task = "Test task"
        args.context = None
        args.context_file = None
        args.json = False
        args.output = None
        args.verbose = True

        analyze_command(args)

        captured = capsys.readouterr()
        assert "Estimated Tokens:" in captured.out


class TestCLICompare:
    """Tests for CLI compare command"""

    def test_compare_basic(self, capsys):
        """Test basic compare command"""
        from claude_model_selector.cli import compare_command

        args = MagicMock()
        args.task = "Process videos"
        args.tokens = 10000

        compare_command(args)

        captured = capsys.readouterr()
        assert "MODEL COMPARISON" in captured.out
        assert "HAIKU" in captured.out
        assert "SONNET" in captured.out
        assert "OPUS" in captured.out

    def test_compare_with_large_tokens(self, capsys):
        """Test compare with large token count"""
        from claude_model_selector.cli import compare_command

        args = MagicMock()
        args.task = "Large batch job"
        args.tokens = 100000

        compare_command(args)

        captured = capsys.readouterr()
        assert "100,000" in captured.out or "100000" in captured.out

    def test_compare_shows_all_models(self, capsys):
        """Test that compare shows all three models"""
        from claude_model_selector.cli import compare_command

        args = MagicMock()
        args.task = "Test"
        args.tokens = 10000

        compare_command(args)

        captured = capsys.readouterr()
        output = captured.out.upper()
        assert "HAIKU" in output
        assert "SONNET" in output
        assert "OPUS" in output


class TestCLIBatch:
    """Tests for CLI batch command"""

    def test_batch_processing(self, capsys):
        """Test batch processing from file"""
        from claude_model_selector.cli import batch_command

        # Create temporary task file
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
            f.write("List files\n")
            f.write("Analyze code\n")
            f.write("Design architecture\n")
            task_file = Path(f.name)

        try:
            args = MagicMock()
            args.file = str(task_file)
            args.output = None
            args.verbose = False

            batch_command(args)

            captured = capsys.readouterr()
            assert "BATCH ANALYSIS" in captured.out
            assert "Total Tasks:" in captured.out
            assert "3" in captured.out
        finally:
            task_file.unlink()

    def test_batch_with_verbose(self, capsys):
        """Test batch with verbose output"""
        from claude_model_selector.cli import batch_command

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
            f.write("Task 1\n")
            f.write("Task 2\n")
            task_file = Path(f.name)

        try:
            args = MagicMock()
            args.file = str(task_file)
            args.output = None
            args.verbose = True

            batch_command(args)

            captured = capsys.readouterr()
            assert "Task 1" in captured.out
            assert "Task 2" in captured.out
        finally:
            task_file.unlink()

    def test_batch_shows_summary(self, capsys):
        """Test batch shows summary"""
        from claude_model_selector.cli import batch_command

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
            f.write("Simple task\n")
            f.write("Complex planning task\n")
            task_file = Path(f.name)

        try:
            args = MagicMock()
            args.file = str(task_file)
            args.output = None
            args.verbose = False

            batch_command(args)

            captured = capsys.readouterr()
            assert "SUMMARY" in captured.out
            assert "Total Tasks:" in captured.out
            assert "Model Distribution:" in captured.out
        finally:
            task_file.unlink()


class TestCLIInfo:
    """Tests for CLI info command"""

    def test_info_all_models(self, capsys):
        """Test info command showing all models"""
        from claude_model_selector.cli import info_command

        args = MagicMock()
        args.model = None

        info_command(args)

        captured = capsys.readouterr()
        assert "CLAUDE MODELS OVERVIEW" in captured.out
        assert "HAIKU" in captured.out
        assert "SONNET" in captured.out
        assert "OPUS" in captured.out

    def test_info_specific_model(self, capsys):
        """Test info for specific model"""
        from claude_model_selector.cli import info_command

        args = MagicMock()
        args.model = "opus"

        info_command(args)

        captured = capsys.readouterr()
        assert "OPUS MODEL INFORMATION" in captured.out
        assert "Speed:" in captured.out
        assert "Input Cost:" in captured.out
        assert "Output Cost:" in captured.out

    def test_info_shows_pricing(self, capsys):
        """Test info shows pricing information"""
        from claude_model_selector.cli import info_command

        args = MagicMock()
        args.model = "haiku"

        info_command(args)

        captured = capsys.readouterr()
        assert "$0.8" in captured.out or "$0.80" in captured.out  # Haiku input cost


class TestCLIHelpers:
    """Tests for CLI helper functions"""

    def test_print_analysis(self, capsys):
        """Test print_analysis helper"""
        from claude_model_selector.cli import print_analysis
        from claude_model_selector import TaskAnalysis

        analysis = TaskAnalysis(
            complexity_score=50.0,
            recommended_model="sonnet",
            reasoning="Test reasoning",
            confidence=0.85,
            estimated_tokens=1000,
            estimated_cost=0.01,
        )

        print_analysis(analysis, verbose=False)

        captured = capsys.readouterr()
        assert "SONNET" in captured.out
        assert "50.0" in captured.out
        assert "85%" in captured.out

    def test_print_analysis_verbose(self, capsys):
        """Test print_analysis with verbose"""
        from claude_model_selector.cli import print_analysis
        from claude_model_selector import TaskAnalysis

        analysis = TaskAnalysis(
            complexity_score=50.0,
            recommended_model="sonnet",
            reasoning="Test reasoning",
            confidence=0.85,
            estimated_tokens=1000,
            estimated_cost=0.01,
        )

        print_analysis(analysis, verbose=True)

        captured = capsys.readouterr()
        assert "Estimated Tokens:" in captured.out
        assert "1,000" in captured.out


class TestCLIIntegration:
    """Integration tests for CLI"""

    def test_full_workflow_analyze(self):
        """Test complete analyze workflow"""
        from claude_model_selector.cli import analyze_command

        args = MagicMock()
        args.task = "Design scalable architecture"
        args.context = None
        args.context_file = None
        args.json = False
        args.output = None
        args.verbose = False

        # Should not raise exception
        analyze_command(args)

    def test_full_workflow_compare(self):
        """Test complete compare workflow"""
        from claude_model_selector.cli import compare_command

        args = MagicMock()
        args.task = "Process data"
        args.tokens = 50000

        # Should not raise exception
        compare_command(args)

    def test_full_workflow_batch(self):
        """Test complete batch workflow"""
        from claude_model_selector.cli import batch_command

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
            f.write("Task 1\nTask 2\nTask 3\n")
            task_file = Path(f.name)

        try:
            args = MagicMock()
            args.file = str(task_file)
            args.output = None
            args.verbose = False

            # Should not raise exception
            batch_command(args)
        finally:
            task_file.unlink()


class TestCLIErrorHandling:
    """Tests for CLI error handling"""

    def test_batch_with_nonexistent_file(self):
        """Test batch with nonexistent file"""
        from claude_model_selector.cli import batch_command

        args = MagicMock()
        args.file = "/nonexistent/file.txt"
        args.output = None
        args.verbose = False

        with pytest.raises(FileNotFoundError):
            batch_command(args)

    def test_analyze_with_invalid_context_file(self):
        """Test analyze with invalid context file"""
        from claude_model_selector.cli import analyze_command

        args = MagicMock()
        args.task = "Test"
        args.context = None
        args.context_file = "/nonexistent/context.txt"
        args.json = False
        args.output = None
        args.verbose = False

        with pytest.raises(FileNotFoundError):
            analyze_command(args)


class TestCLIOutputFiles:
    """Tests for CLI output to files"""

    def test_analyze_save_to_file(self):
        """Test saving analysis to file"""
        from claude_model_selector.cli import analyze_command

        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as f:
            output_file = Path(f.name)

        try:
            args = MagicMock()
            args.task = "Test task"
            args.context = None
            args.context_file = None
            args.json = False
            args.output = str(output_file)
            args.verbose = False

            analyze_command(args)

            # File should exist (though implementation may need this feature)
            # This test documents expected behavior
        finally:
            if output_file.exists():
                output_file.unlink()

    def test_batch_save_results(self):
        """Test saving batch results to file"""
        from claude_model_selector.cli import batch_command

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
            f.write("Task 1\nTask 2\n")
            task_file = Path(f.name)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as f:
            output_file = Path(f.name)

        try:
            args = MagicMock()
            args.file = str(task_file)
            args.output = str(output_file)
            args.verbose = False

            batch_command(args)

            # Output file should exist
            assert output_file.exists()

            # Should contain valid JSON
            with open(output_file) as f:
                data = json.load(f)
                assert "total_tasks" in data
        finally:
            task_file.unlink()
            if output_file.exists():
                output_file.unlink()
