#!/usr/bin/env python3
"""
Example: Using Claude Model Selector in Real Projects

Demonstrates practical integration of intelligent model selection
for cost-effective task execution.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from claude_model_selector import ClaudeModelSelector, quick_select


# Example 1: Basic Task Classification
def example_basic_classification():
    """Basic example of task classification"""
    print("\n" + "=" * 80)
    print("EXAMPLE 1: Basic Task Classification")
    print("=" * 80)

    selector = ClaudeModelSelector()

    tasks = {
        "Simple": "List all video files in the downloads folder",
        "Medium": "Analyze video metadata and extract popular moments",
        "Complex": "Design a scalable pipeline for processing 1M videos/day"
    }

    for category, task in tasks.items():
        analysis = selector.analyze_task(task)
        print(f"\n{category} Task:")
        print(f"  Task: {task}")
        print(f"  Model: {analysis.recommended_model.upper()}")
        print(f"  Complexity: {analysis.complexity_score:.1f}/100")
        print(f"  Cost: ${analysis.estimated_cost:.6f}")


# Example 2: Video Processing Pipeline
def example_video_pipeline():
    """Optimize costs for video processing pipeline"""
    print("\n" + "=" * 80)
    print("EXAMPLE 2: Video Processing Pipeline Tasks")
    print("=" * 80)

    selector = ClaudeModelSelector()

    pipeline_tasks = [
        "Extract video metadata using yt-dlp",
        "Analyze replay heatmap and find popular moments",
        "Cut video clips at specific timestamps",
        "Generate viral titles and descriptions for clips using AI",
        "Design thumbnail concepts for maximum engagement",
        "Validate video format and codec compatibility",
        "Upload clips to YouTube with metadata",
    ]

    total_cost = 0.0
    model_usage = {'haiku': 0, 'sonnet': 0, 'opus': 0}

    print("\nPipeline Task Analysis:")
    print("-" * 80)

    for i, task in enumerate(pipeline_tasks, 1):
        analysis = selector.analyze_task(task)
        total_cost += analysis.estimated_cost
        model_usage[analysis.recommended_model] += 1

        print(f"\n{i}. {task}")
        print(f"   Model: {analysis.recommended_model.upper():<8} "
              f"Cost: ${analysis.estimated_cost:.6f}  "
              f"Complexity: {analysis.complexity_score:.1f}")

    print("\n" + "-" * 80)
    print(f"Total Estimated Cost: ${total_cost:.6f}")
    print(f"\nModel Distribution:")
    for model, count in model_usage.items():
        if count > 0:
            print(f"  {model.upper():<8} {count} tasks")


# Example 3: Batch Processing with Cost Optimization
def example_batch_optimization():
    """Batch process tasks with cost tracking"""
    print("\n" + "=" * 80)
    print("EXAMPLE 3: Batch Processing with Cost Optimization")
    print("=" * 80)

    selector = ClaudeModelSelector()

    # Simulate multiple user requests
    user_requests = [
        "Quick: check video format",
        "Analyze this video transcript for key moments",
        "Design a comprehensive content moderation system",
        "Simple: convert MP4 to WebM",
        "Research best practices for video compression",
        "List all processed videos",
        "Create strategic plan for scaling infrastructure",
        "Fix bug in subtitle parser",
    ]

    results = []
    for request in user_requests:
        analysis = selector.analyze_task(request)
        results.append({
            'task': request,
            'model': analysis.recommended_model,
            'cost': analysis.estimated_cost,
            'complexity': analysis.complexity_score
        })

    # Group by model
    by_model = {'haiku': [], 'sonnet': [], 'opus': []}
    for result in results:
        by_model[result['model']].append(result)

    print("\nTasks Grouped by Model:")
    print("-" * 80)

    total_cost = 0.0
    for model in ['haiku', 'sonnet', 'opus']:
        tasks = by_model[model]
        if tasks:
            model_cost = sum(t['cost'] for t in tasks)
            total_cost += model_cost
            print(f"\n{model.upper()} ({len(tasks)} tasks, ${model_cost:.6f}):")
            for task in tasks:
                print(f"  • {task['task']}")

    print(f"\nTotal Cost: ${total_cost:.6f}")

    # Calculate savings vs using Opus for everything
    opus_total = sum(r['cost'] for r in results) * 4.25  # Approximate Opus cost multiplier
    savings = opus_total - total_cost
    savings_pct = (savings / opus_total) * 100

    print(f"Savings vs using Opus for all: ${savings:.6f} ({savings_pct:.1f}%)")


# Example 4: Quick Selection Helper
def example_quick_selection():
    """Quick model selection without full analysis"""
    print("\n" + "=" * 80)
    print("EXAMPLE 4: Quick Selection for Rapid Decisions")
    print("=" * 80)

    tasks = [
        "Extract timestamps",
        "Implement caching layer",
        "Architect multi-region deployment"
    ]

    print("\nQuick Model Selection:")
    for task in tasks:
        model = quick_select(task)
        print(f"  {task:<45} → {model.upper()}")


# Example 5: Context-Aware Selection
def example_context_aware():
    """Selection with additional context"""
    print("\n" + "=" * 80)
    print("EXAMPLE 5: Context-Aware Selection")
    print("=" * 80)

    selector = ClaudeModelSelector()

    # Same task, different contexts
    task = "Optimize this code"

    contexts = {
        "Simple": "# Just a basic loop\nfor i in range(10):\n    print(i)",
        "Complex": """# Critical payment processing system
                    # Handles $1M+ transactions daily
                    # Multiple database calls, cache layers, etc.
                    # 500+ lines of code with complex business logic"""
    }

    print("\nSame Task, Different Context:")
    for context_type, context in contexts.items():
        analysis = selector.analyze_task(task, context)
        print(f"\n{context_type} Context:")
        print(f"  Model: {analysis.recommended_model.upper()}")
        print(f"  Complexity: {analysis.complexity_score:.1f}/100")
        print(f"  Reasoning: {analysis.reasoning[:80]}...")


# Example 6: Cost Comparison
def example_cost_comparison():
    """Compare costs across models"""
    print("\n" + "=" * 80)
    print("EXAMPLE 6: Cost Comparison for Different Token Volumes")
    print("=" * 80)

    selector = ClaudeModelSelector()
    task = "Implement user authentication system"

    token_volumes = [1000, 10000, 50000, 100000]

    print(f"\nTask: {task}")
    print("\nCost by Model and Token Volume:")
    print("-" * 80)
    print(f"{'Tokens':<12} {'Haiku':<15} {'Sonnet':<15} {'Opus':<15} {'Best Choice'}")
    print("-" * 80)

    for tokens in token_volumes:
        comparisons = selector.compare_models(task, tokens)
        costs = {comp['model']: comp['estimated_cost'] for comp in comparisons}

        analysis = selector.analyze_task(task)
        best = analysis.recommended_model

        print(f"{tokens:<12,} "
              f"${costs['haiku']:<14.6f} "
              f"${costs['sonnet']:<14.6f} "
              f"${costs['opus']:<14.6f} "
              f"{best.upper()}")


# Example 7: Real-World Integration Pattern
def example_integration_pattern():
    """
    Practical pattern for integrating with actual task execution

    In a real Claude Code context, you would use this with the Task tool.
    """
    print("\n" + "=" * 80)
    print("EXAMPLE 7: Integration Pattern for Task Execution")
    print("=" * 80)

    def execute_task_with_optimal_model(task_description, context=None):
        """
        Execute a task with automatically selected optimal model

        In real usage, this would call the Task tool with the selected model
        """
        selector = ClaudeModelSelector()
        analysis = selector.analyze_task(task_description, context)

        print(f"\nTask: {task_description}")
        print(f"Selected Model: {analysis.recommended_model.upper()}")
        print(f"Complexity: {analysis.complexity_score:.1f}/100")
        print(f"Confidence: {analysis.confidence:.0%}")
        print(f"Est. Cost: ${analysis.estimated_cost:.6f}")

        # In real usage, you would call:
        # Task(
        #     prompt=task_description,
        #     model=analysis.recommended_model,
        #     subagent_type='general-purpose',
        #     description="Auto-selected model task"
        # )

        return analysis.recommended_model

    # Example usage
    print("\nExecuting tasks with auto-selection:")
    print("-" * 80)

    tasks = [
        "Find all TODO comments in the codebase",
        "Review the authentication module for security issues",
        "Design a comprehensive testing strategy for the platform"
    ]

    for task in tasks:
        execute_task_with_optimal_model(task)


# Example 8: Confidence-Based Decision Making
def example_confidence_based():
    """Use confidence scores to make better decisions"""
    print("\n" + "=" * 80)
    print("EXAMPLE 8: Confidence-Based Decision Making")
    print("=" * 80)

    selector = ClaudeModelSelector()

    ambiguous_tasks = [
        "Fix the code",  # Ambiguous
        "Fix authentication bug causing 500 errors in login endpoint",  # Clear
        "Optimize",  # Very ambiguous
        "Optimize database queries in user service reducing latency by 50%",  # Clear
    ]

    print("\nConfidence Analysis:")
    print("-" * 80)

    for task in ambiguous_tasks:
        analysis = selector.analyze_task(task)
        print(f"\nTask: {task}")
        print(f"  Model: {analysis.recommended_model.upper()}")
        print(f"  Confidence: {analysis.confidence:.0%} ", end="")

        if analysis.confidence < 0.7:
            print("⚠️  LOW CONFIDENCE - Consider more specific task description")
        elif analysis.confidence < 0.85:
            print("✓ Moderate confidence")
        else:
            print("✓✓ High confidence")


def main():
    """Run all examples"""
    print("\n" + "=" * 80)
    print("CLAUDE MODEL SELECTOR - USAGE EXAMPLES")
    print("=" * 80)
    print("\nDemonstrating intelligent cost-effective model selection")

    example_basic_classification()
    example_video_pipeline()
    example_batch_optimization()
    example_quick_selection()
    example_context_aware()
    example_cost_comparison()
    example_integration_pattern()
    example_confidence_based()

    print("\n" + "=" * 80)
    print("EXAMPLES COMPLETE")
    print("=" * 80)
    print("\nKey Takeaways:")
    print("  1. Use quick_select() for fast decisions")
    print("  2. Provide context for better accuracy")
    print("  3. Batch analyze for cost optimization")
    print("  4. Check confidence scores for ambiguous tasks")
    print("  5. Significant cost savings with smart selection")
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
