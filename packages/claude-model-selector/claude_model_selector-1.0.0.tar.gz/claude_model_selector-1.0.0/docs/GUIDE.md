# Claude Model Selector

**Intelligent model selection for optimal cost-effectiveness**

Automatically choose the best Claude model (Opus, Sonnet, or Haiku) for each task based on complexity analysis, ensuring you get the best results while minimizing token costs.

## Overview

The Claude Model Selector analyzes your task description and automatically recommends the most cost-effective model:

- **Haiku** (0-30 complexity): Simple, quick tasks - Fastest & Cheapest
- **Sonnet** (31-70 complexity): Standard reliable tasks - Balanced
- **Opus** (71-100 complexity): Complex planning tasks - Most Capable

## Cost Comparison

| Model | Input ($/MTok) | Output ($/MTok) | Speed | Best For |
|-------|----------------|-----------------|-------|----------|
| **Haiku** | $0.80 | $4.00 | Fastest | Simple operations, quick tasks |
| **Sonnet** | $3.00 | $15.00 | Balanced | Standard development, analysis |
| **Opus** | $15.00 | $75.00 | Slowest | Planning, architecture, critical thinking |

**Example Cost Savings:**
- Simple task (10K tokens): Haiku $0.024 vs Opus $0.60 = **96% savings**
- Standard task (50K tokens): Sonnet $0.90 vs Opus $4.50 = **80% savings**

## Installation

No additional dependencies required beyond the base project:

```bash
# Make CLI executable
chmod +x ab/dc/cli_model_selector.py

# Test installation
python ab/dc/cli_model_selector.py info
```

## Quick Start

### 1. Analyze a Single Task

```bash
python ab/dc/cli_model_selector.py analyze "Design a scalable video processing architecture"
```

**Output:**
```
================================================================================
MODEL RECOMMENDATION
================================================================================

  Recommended Model: OPUS
  Complexity Score:  85.5/100
  Confidence:        95%
  Estimated Cost:    $0.001234

  Reasoning: Task is complex and requires advanced reasoning; Planning/design tasks benefit from Opus capabilities; Opus recommended for critical thinking and planning

================================================================================
```

### 2. Compare All Models

```bash
python ab/dc/cli_model_selector.py compare "Process 100 videos" --tokens 50000
```

**Output:**
```
Model      Speed        Est. Cost       Use Cases
--------------------------------------------------------------------------------
HAIKU      fastest      $0.024000      simple, quick, straightforward
SONNET     balanced     $0.090000      reliable, common, standard
OPUS       slowest      $0.450000      complex, planning, strategic

  Recommended: SONNET (complexity: 65.0/100)
```

### 3. Batch Analysis

Create a file `tasks.txt`:
```
List all Python files
Analyze code for security issues
Design microservices architecture
Quick syntax fix in utils.py
```

Run batch analysis:
```bash
python ab/dc/cli_model_selector.py batch tasks.txt --verbose
```

## Programmatic Usage

### Basic Usage

```python
from ab.dc.claude_model_selector import ClaudeModelSelector

# Create selector
selector = ClaudeModelSelector()

# Analyze task
analysis = selector.analyze_task(
    task="Create a comprehensive testing strategy",
    context="For a video processing pipeline with 100K users"
)

print(f"Use model: {analysis.recommended_model}")
print(f"Complexity: {analysis.complexity_score:.1f}/100")
print(f"Est. cost: ${analysis.estimated_cost:.6f}")
```

### Quick Selection

```python
from ab.dc.claude_model_selector import quick_select

# Get model name directly
model = quick_select("List all files in directory")
# Returns: 'haiku'

model = quick_select("Design scalable architecture")
# Returns: 'opus'
```

### With Context

```python
selector = ClaudeModelSelector()

# Provide additional context for better analysis
analysis = selector.analyze_task(
    task="Optimize this code",
    context=open('my_code.py').read()
)

print(f"Model: {analysis.recommended_model}")
print(f"Reasoning: {analysis.reasoning}")
```

### Model Comparison

```python
selector = ClaudeModelSelector()

# Compare costs for all models
comparisons = selector.compare_models(
    task="Process large dataset",
    estimated_tokens=100000
)

for comp in comparisons:
    print(f"{comp['model']}: ${comp['estimated_cost']:.4f}")
```

## Integration with Task Tool

Use with Claude Code's Task tool:

```python
from ab.dc.claude_model_selector import quick_select

# Get optimal model for task
task_desc = "Design a multi-region deployment strategy"
optimal_model = quick_select(task_desc)

# Use with Task tool (in your code)
# Task(
#     prompt=task_desc,
#     model=optimal_model,  # 'opus', 'sonnet', or 'haiku'
#     subagent_type='general-purpose'
# )
```

## CLI Commands

### `analyze` - Analyze a Task

Analyze task complexity and get model recommendation:

```bash
# Basic analysis
python ab/dc/cli_model_selector.py analyze "Your task here"

# With context from file
python ab/dc/cli_model_selector.py analyze "Optimize this code" --context-file code.py

# JSON output
python ab/dc/cli_model_selector.py analyze "Task" --json

# Save to file
python ab/dc/cli_model_selector.py analyze "Task" --output analysis.json

# Verbose mode
python ab/dc/cli_model_selector.py analyze "Task" --verbose
```

### `compare` - Compare Models

Compare all models for a specific task:

```bash
# Default comparison (10K tokens)
python ab/dc/cli_model_selector.py compare "Process videos"

# Custom token estimate
python ab/dc/cli_model_selector.py compare "Large batch job" --tokens 100000
```

### `batch` - Batch Analysis

Analyze multiple tasks from a file:

```bash
# Analyze tasks from file
python ab/dc/cli_model_selector.py batch tasks.txt

# Verbose output
python ab/dc/cli_model_selector.py batch tasks.txt --verbose

# Save results
python ab/dc/cli_model_selector.py batch tasks.txt --output results.json
```

### `info` - Model Information

Get information about models:

```bash
# All models
python ab/dc/cli_model_selector.py info

# Specific model
python ab/dc/cli_model_selector.py info --model opus
```

## Complexity Scoring

The selector calculates a complexity score (0-100) based on:

### Keyword Analysis

**Haiku Indicators** (-20 points each):
- simple, quick, basic, straightforward, easy
- just, only, list, extract, format, convert

**Sonnet Indicators** (neutral):
- analyze, review, implement, create, develop
- write, generate, build, process, handle

**Opus Indicators** (+30 points each):
- plan, design, architect, strategy, complex
- critical, research, comprehensive, evaluate

### Pattern Matching

**Planning Tasks** (+40 points):
- Contains: plan, design, architect, strategy, roadmap

**Complex Coding** (+35 points):
- Multi-step, complex system, refactor entire, migration

**Research & Analysis** (+30 points):
- Research, investigate, comprehensive, deep analysis

**Decision Making** (+25 points):
- Trade-offs, compare approaches, evaluate options

**Simple Operations** (-30 points):
- List items, count, extract, format, convert

### Other Factors

- **Length**: Long descriptions (+15), very short descriptions (-10)
- **Context**: Additional context adds +1-15 points
- **Questions**: Multiple questions indicate complexity (+5 each)
- **Multi-step**: "and then", "after that" (+10)
- **Simplifiers**: "just", "simply", "only" (-15)

## Examples by Category

### Haiku Tasks (0-30 complexity)

```bash
# File operations
python ab/dc/cli_model_selector.py analyze "List all Python files in src/"

# Simple extraction
python ab/dc/cli_model_selector.py analyze "Extract email addresses from text"

# Format conversion
python ab/dc/cli_model_selector.py analyze "Convert JSON to CSV"

# Quick fixes
python ab/dc/cli_model_selector.py analyze "Fix syntax error in line 42"

# Simple checks
python ab/dc/cli_model_selector.py analyze "Check if API is responding"
```

### Sonnet Tasks (31-70 complexity)

```bash
# Code analysis
python ab/dc/cli_model_selector.py analyze "Analyze code for potential bugs"

# Implementation
python ab/dc/cli_model_selector.py analyze "Implement user authentication with JWT"

# Testing
python ab/dc/cli_model_selector.py analyze "Create comprehensive test suite"

# Refactoring
python ab/dc/cli_model_selector.py analyze "Refactor database layer for better performance"

# Documentation
python ab/dc/cli_model_selector.py analyze "Generate API documentation from code"
```

### Opus Tasks (71-100 complexity)

```bash
# Architecture
python ab/dc/cli_model_selector.py analyze "Design scalable microservices architecture"

# Planning
python ab/dc/cli_model_selector.py analyze "Plan migration from monolith to microservices"

# Research
python ab/dc/cli_model_selector.py analyze "Research and compare database solutions for high-traffic app"

# Strategy
python ab/dc/cli_model_selector.py analyze "Develop comprehensive security audit strategy"

# Trade-offs
python ab/dc/cli_model_selector.py analyze "Evaluate trade-offs between caching strategies"
```

## Configuration

Customize behavior by editing `model_selector_config.json`:

```json
{
  "thresholds": {
    "haiku_max": 30,
    "sonnet_max": 70
  },
  "default_model": "sonnet",
  "cost_optimization": true,
  "custom_rules": {
    "force_opus_keywords": ["critical", "production"],
    "force_haiku_keywords": ["trivial", "one-liner"]
  }
}
```

### Custom Configuration

```python
from pathlib import Path
from ab.dc.claude_model_selector import ClaudeModelSelector

# Load custom config
selector = ClaudeModelSelector(
    config_path=Path('my_custom_config.json')
)

analysis = selector.analyze_task("Your task")
```

## Cost Tracking

### Estimate Costs

```python
selector = ClaudeModelSelector()

# Get cost estimate
analysis = selector.analyze_task("Process 1000 videos")

print(f"Estimated cost: ${analysis.estimated_cost:.6f}")
print(f"Estimated tokens: {analysis.estimated_tokens:,}")
```

### Compare Savings

```python
selector = ClaudeModelSelector()

task = "Standard data processing task"
tokens = 50000

# Compare all models
comparisons = selector.compare_models(task, tokens)

haiku_cost = comparisons[0]['estimated_cost']
opus_cost = comparisons[2]['estimated_cost']

savings = opus_cost - haiku_cost
savings_pct = (savings / opus_cost) * 100

print(f"Savings: ${savings:.4f} ({savings_pct:.1f}%)")
```

## Real-World Examples

### Example 1: Video Processing Pipeline

```python
from ab.dc.claude_model_selector import ClaudeModelSelector

selector = ClaudeModelSelector()

tasks = {
    "Extract video metadata": None,
    "Analyze video content for highlights": None,
    "Design comprehensive video processing architecture": None,
    "Generate thumbnail from frame": None,
}

total_cost = 0
for task in tasks:
    analysis = selector.analyze_task(task)
    tasks[task] = analysis.recommended_model
    total_cost += analysis.estimated_cost

    print(f"{task}")
    print(f"  → {analysis.recommended_model.upper()} (${analysis.estimated_cost:.6f})")

print(f"\nTotal estimated cost: ${total_cost:.6f}")
```

**Output:**
```
Extract video metadata
  → HAIKU ($0.000024)
Analyze video content for highlights
  → SONNET ($0.000090)
Design comprehensive video processing architecture
  → OPUS ($0.000450)
Generate thumbnail from frame
  → HAIKU ($0.000024)

Total estimated cost: $0.000588
```

### Example 2: Batch Task Processing

```bash
# Create task list
cat > tasks.txt << EOF
List all uncommitted files
Analyze code coverage and suggest improvements
Design event-driven architecture for notifications
Fix typo in README
Create migration plan from PostgreSQL to MongoDB
Quick performance check
EOF

# Analyze all tasks
python ab/dc/cli_model_selector.py batch tasks.txt --verbose --output results.json
```

### Example 3: API Integration

```python
from ab.dc.claude_model_selector import ClaudeModelSelector

def process_with_optimal_model(task_description, context=None):
    """Process task with automatically selected optimal model"""
    selector = ClaudeModelSelector()

    # Analyze task
    analysis = selector.analyze_task(task_description, context)

    print(f"Task: {task_description}")
    print(f"Selected: {analysis.recommended_model.upper()}")
    print(f"Confidence: {analysis.confidence:.0%}")

    # Here you would call your actual Claude API
    # with the recommended model
    return analysis.recommended_model

# Usage
model = process_with_optimal_model(
    "Refactor authentication system for better security"
)
# Returns: 'sonnet'
```

## Best Practices

### 1. Provide Clear Task Descriptions

```python
# Bad (ambiguous)
analyze_task("Fix the code")

# Good (specific)
analyze_task("Fix authentication bug in login endpoint that causes 500 errors")
```

### 2. Include Context When Relevant

```python
# Better results with context
analysis = selector.analyze_task(
    task="Optimize this function",
    context=open('slow_function.py').read()
)
```

### 3. Batch Similar Tasks

```python
# More efficient to batch analyze
tasks = ["Task 1", "Task 2", "Task 3"]
for task in tasks:
    analysis = selector.analyze_task(task)
    # Process...
```

### 4. Review Confidence Scores

```python
analysis = selector.analyze_task("Ambiguous task")

if analysis.confidence < 0.7:
    print("Low confidence - consider reviewing the recommendation")
    print(f"Reasoning: {analysis.reasoning}")
```

## Troubleshooting

### "Unexpected model selection"

**Issue**: Task gets wrong model
**Solution**: Check the keywords and complexity score

```python
analysis = selector.analyze_task("Your task")
print(f"Complexity: {analysis.complexity_score}")
print(f"Reasoning: {analysis.reasoning}")
```

### "Costs higher than expected"

**Issue**: Token estimate seems high
**Solution**: Review token estimation

```python
analysis = selector.analyze_task("Your task")
print(f"Estimated tokens: {analysis.estimated_tokens:,}")
print(f"Cost breakdown: ${analysis.estimated_cost:.6f}")
```

### "Custom configuration not loading"

**Issue**: Config file not being used
**Solution**: Verify path and JSON syntax

```python
from pathlib import Path
import json

config_path = Path('model_selector_config.json')
if config_path.exists():
    with open(config_path) as f:
        config = json.load(f)  # Check for JSON errors
    selector = ClaudeModelSelector(config_path=config_path)
```

## Performance Tips

1. **Cache analyses** for repeated tasks
2. **Batch process** when analyzing multiple tasks
3. **Use custom config** to tune for your specific use case
4. **Monitor costs** with the built-in estimation

## Contributing

To add custom complexity rules:

1. Edit `model_selector_config.json`
2. Add keywords or patterns to appropriate categories
3. Adjust weights as needed
4. Test with representative tasks

## Support

For issues or questions:
- Check complexity score with `--verbose` flag
- Review reasoning in analysis output
- Examine configuration in `model_selector_config.json`
- Test with known examples from this documentation

## License

Part of the AEON-BRIDGE ab-instagram-video-processor project.
