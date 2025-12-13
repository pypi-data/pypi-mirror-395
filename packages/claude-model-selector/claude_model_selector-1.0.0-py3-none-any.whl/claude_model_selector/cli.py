#!/usr/bin/env python3
"""
CLI for Claude Model Selector
Intelligently select and execute tasks with the optimal Claude model
"""

import argparse
import sys
import json
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from claude_model_selector import ClaudeModelSelector, TaskAnalysis  # noqa: E402


def print_analysis(analysis: TaskAnalysis, verbose: bool = False):
    """Print task analysis in a formatted way"""
    print("\n" + "=" * 80)
    print("MODEL RECOMMENDATION")
    print("=" * 80)
    print(f"\n  Recommended Model: {analysis.recommended_model.upper()}")
    print(f"  Complexity Score:  {analysis.complexity_score:.1f}/100")
    print(f"  Confidence:        {analysis.confidence:.0%}")
    print(f"  Estimated Cost:    ${analysis.estimated_cost:.6f}")
    print(f"\n  Reasoning: {analysis.reasoning}")

    if verbose:
        print(f"\n  Estimated Tokens:  {analysis.estimated_tokens:,}")

    print("\n" + "=" * 80)


def analyze_command(args):
    """Analyze a task and show recommendation"""
    selector = ClaudeModelSelector()

    # Get task description
    task = args.task if args.task else input("Enter task description: ")

    # Get optional context
    context = None
    if args.context:
        context = args.context
    elif args.context_file:
        with open(args.context_file) as f:
            context = f.read()

    # Analyze
    analysis = selector.analyze_task(task, context)

    # Print results
    print_analysis(analysis, args.verbose)

    # JSON output if requested
    if args.json:
        output = {
            "task": task,
            "model": analysis.recommended_model,
            "complexity_score": analysis.complexity_score,
            "confidence": analysis.confidence,
            "estimated_cost": analysis.estimated_cost,
            "reasoning": analysis.reasoning,
            "estimated_tokens": analysis.estimated_tokens,
        }
        print("\nJSON Output:")
        print(json.dumps(output, indent=2))

    # Save to file if requested
    if args.output:
        output_data = {
            "task": task,
            "context": context,
            "analysis": {
                "model": analysis.recommended_model,
                "complexity_score": analysis.complexity_score,
                "confidence": analysis.confidence,
                "estimated_cost": analysis.estimated_cost,
                "reasoning": analysis.reasoning,
                "estimated_tokens": analysis.estimated_tokens,
            },
        }
        with open(args.output, "w") as f:
            json.dump(output_data, f, indent=2)
        print(f"\nAnalysis saved to: {args.output}")


def compare_command(args):
    """Compare models for a task"""
    selector = ClaudeModelSelector()

    task = args.task if args.task else input("Enter task description: ")
    tokens = args.tokens

    comparisons = selector.compare_models(task, tokens)

    print("\n" + "=" * 80)
    print("MODEL COMPARISON FOR TASK")
    print("=" * 80)
    print(f"\nTask: {task}")
    print(f"Estimated Tokens: {tokens:,}")
    print("\n")

    print(f"{'Model':<10} {'Speed':<12} {'Est. Cost':<15} {'Use Cases'}")
    print("-" * 80)

    for comp in comparisons:
        use_cases = ", ".join(comp["use_cases"][:3])
        model = comp["model"].upper()
        speed = comp["speed"]
        cost = comp["estimated_cost"]
        print(f"{model:<10} {speed:<12} ${cost:<14.6f} {use_cases}")

    # Show recommendation
    analysis = selector.analyze_task(task)
    print(
        f"\n  Recommended: {analysis.recommended_model.upper()} "
        f"(complexity: {analysis.complexity_score:.1f}/100)"
    )
    print("=" * 80)


def batch_command(args):
    """Analyze multiple tasks from a file"""
    selector = ClaudeModelSelector()

    # Read tasks from file
    with open(args.file) as f:
        tasks = [line.strip() for line in f if line.strip()]

    print("\n" + "=" * 80)
    print(f"BATCH ANALYSIS - {len(tasks)} tasks")
    print("=" * 80)

    results = []
    total_cost = 0.0

    for i, task in enumerate(tasks, 1):
        analysis = selector.analyze_task(task)
        results.append(
            {
                "task": task,
                "model": analysis.recommended_model,
                "complexity": analysis.complexity_score,
                "cost": analysis.estimated_cost,
            }
        )
        total_cost += analysis.estimated_cost

        if args.verbose:
            print(f"\n{i}. {task}")
            print(
                f"   → {analysis.recommended_model.upper()} "
                f"(complexity: {analysis.complexity_score:.1f}, "
                f"cost: ${analysis.estimated_cost:.6f})"
            )

    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)

    model_counts: dict = {}
    for result in results:
        model = result["model"]
        model_counts[model] = model_counts.get(model, 0) + 1

    print(f"\nTotal Tasks: {len(tasks)}")
    print(f"Total Estimated Cost: ${total_cost:.6f}")
    print("\nModel Distribution:")
    for model, count in sorted(model_counts.items()):
        percentage = (count / len(tasks)) * 100
        print(f"  {str(model).upper():<10} {count:>3} tasks ({percentage:.1f}%)")

    # Save results if requested
    if args.output:
        output_data = {
            "total_tasks": len(tasks),
            "total_cost": total_cost,
            "model_distribution": model_counts,
            "tasks": results,
        }
        with open(args.output, "w") as f:
            json.dump(output_data, f, indent=2)
        print(f"\nResults saved to: {args.output}")


def info_command(args):
    """Show model information"""
    selector = ClaudeModelSelector()

    if args.model:
        # Show specific model info
        info = selector.get_model_info(args.model)
        print("\n" + "=" * 80)
        print(f"{args.model.upper()} MODEL INFORMATION")
        print("=" * 80)
        print(f"\nSpeed:        {info['speed']}")
        print(f"Input Cost:   ${info['cost_per_mtok_input']}/million tokens")
        print(f"Output Cost:  ${info['cost_per_mtok_output']}/million tokens")
        print(f"Best for:     {', '.join(info['use_cases'])}")
        print("=" * 80)
    else:
        # Show all models
        print("\n" + "=" * 80)
        print("CLAUDE MODELS OVERVIEW")
        print("=" * 80)

        for model_name in ["haiku", "sonnet", "opus"]:
            info = selector.get_model_info(model_name)
            print(f"\n{model_name.upper()}:")
            print(f"  Speed:        {info['speed']}")
            print(f"  Input Cost:   ${info['cost_per_mtok_input']}/MTok")
            print(f"  Output Cost:  ${info['cost_per_mtok_output']}/MTok")
            print(f"  Best for:     {', '.join(info['use_cases'])}")

        print("\n" + "=" * 80)


def main():
    parser = argparse.ArgumentParser(
        description="Claude Model Selector - Choose the optimal model for each task",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze a task
  %(prog)s analyze "Design a scalable video processing architecture"

  # Analyze with context
  %(prog)s analyze "Optimize this code" --context-file code.py

  # Compare models
  %(prog)s compare "Process 100 videos" --tokens 50000

  # Batch analyze tasks from file
  %(prog)s batch tasks.txt

  # Show model information
  %(prog)s info --model opus

  # Get JSON output
  %(prog)s analyze "Create test suite" --json

Model Selection Strategy:
  HAIKU (0-30):  Simple, quick tasks - FASTEST & CHEAPEST
  SONNET (31-70): Standard reliable tasks - BALANCED
  OPUS (71-100):  Complex planning tasks - MOST CAPABLE

Cost (per million tokens):
  HAIKU:  Input $0.80  | Output $4.00
  SONNET: Input $3.00  | Output $15.00
  OPUS:   Input $15.00 | Output $75.00
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Analyze command
    analyze_parser = subparsers.add_parser(
        "analyze", help="Analyze a task and get model recommendation"
    )
    analyze_parser.add_argument("task", nargs="?", help="Task description")
    analyze_parser.add_argument("--context", help="Additional context")
    analyze_parser.add_argument("--context-file", help="File containing context")
    analyze_parser.add_argument("--json", action="store_true", help="Output as JSON")
    analyze_parser.add_argument("--output", "-o", help="Save analysis to file")
    analyze_parser.add_argument(
        "--verbose", "-v", action="store_true", help="Verbose output"
    )

    # Compare command
    compare_parser = subparsers.add_parser("compare", help="Compare models for a task")
    compare_parser.add_argument("task", nargs="?", help="Task description")
    compare_parser.add_argument(
        "--tokens", type=int, default=10000, help="Estimated tokens (default: 10000)"
    )

    # Batch command
    batch_parser = subparsers.add_parser(
        "batch", help="Analyze multiple tasks from file"
    )
    batch_parser.add_argument("file", help="File with task list (one per line)")
    batch_parser.add_argument("--output", "-o", help="Save results to file")
    batch_parser.add_argument(
        "--verbose", "-v", action="store_true", help="Verbose output"
    )

    # Info command
    info_parser = subparsers.add_parser("info", help="Show model information")
    info_parser.add_argument(
        "--model", choices=["haiku", "sonnet", "opus"], help="Specific model"
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # Execute command
    if args.command == "analyze":
        analyze_command(args)
    elif args.command == "compare":
        compare_command(args)
    elif args.command == "batch":
        batch_command(args)
    elif args.command == "info":
        info_command(args)


if __name__ == "__main__":
    main()
