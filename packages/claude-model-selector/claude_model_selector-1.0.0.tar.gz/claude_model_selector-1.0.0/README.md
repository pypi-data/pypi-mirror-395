# Claude Model Selector

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**Intelligent model selection for optimal cost-effectiveness with Anthropic's Claude AI**

Automatically choose the most cost-effective Claude model (Opus, Sonnet, or Haiku) for each task based on intelligent complexity analysis. Save 70-95% on AI costs while maintaining quality.

**Sponsored by [AeonBridge Co.](https://github.com/aeonbridge)**

---

## 🎯 Features

- **Automatic Complexity Analysis** - Analyzes task descriptions and scores complexity (0-100)
- **Intelligent Model Selection** - Chooses optimal model based on complexity
- **Cost Optimization** - Save 70-95% compared to using premium models for everything
- **Context-Aware** - Considers additional context for better accuracy
- **Confidence Scoring** - Provides confidence levels for recommendations
- **Batch Processing** - Analyze multiple tasks efficiently
- **CLI & API** - Both command-line and programmatic interfaces
- **Customizable** - Easily configure thresholds and rules
- **Zero Dependencies** - Pure Python, no external dependencies required

---

## 📊 Model Selection Strategy

| Model | Complexity Score | Speed | Cost (Input/Output per MTok) | Best For |
|-------|-----------------|-------|------------------------------|----------|
| **Haiku** | 0-30 | Fastest | $0.80 / $4.00 | Simple, quick tasks |
| **Sonnet** | 31-70 | Balanced | $3.00 / $15.00 | Standard, reliable tasks |
| **Opus** | 71-100 | Slowest | $15.00 / $75.00 | Complex, critical tasks |

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/aeonbridge/claude-model-selector.git
cd claude-model-selector

# Install the package
pip install -e .

# Or install from PyPI (when published)
pip install claude-model-selector
```

### Basic Usage

#### CLI

```bash
# Analyze a single task
claude-model-selector analyze "Design a scalable microservices architecture"

# Compare models with token estimate
claude-model-selector compare "Process 100 videos" --tokens 50000

# Batch analyze tasks
echo "Task 1\nTask 2\nTask 3" > tasks.txt
claude-model-selector batch tasks.txt

# Show model information
claude-model-selector info
```

#### Python API

```python
from claude_model_selector import ClaudeModelSelector, quick_select

# Quick selection (one-liner)
model = quick_select("List all Python files")
# Returns: 'haiku'

# Detailed analysis
selector = ClaudeModelSelector()
analysis = selector.analyze_task("Design a scalable architecture")

print(f"Model: {analysis.recommended_model.upper()}")
print(f"Complexity: {analysis.complexity_score:.1f}/100")
print(f"Confidence: {analysis.confidence:.0%}")
print(f"Cost: ${analysis.estimated_cost:.6f}")
print(f"Reasoning: {analysis.reasoning}")
```

---

## 💰 Cost Savings Example

**Scenario**: Processing a batch of 10 mixed tasks

```python
from claude_model_selector import ClaudeModelSelector

selector = ClaudeModelSelector()
tasks = [
    "List all files in directory",
    "Analyze code for security vulnerabilities",
    "Design comprehensive system architecture",
    "Convert JSON to CSV",
    "Plan migration strategy",
]

total_cost = 0
for task in tasks:
    analysis = selector.analyze_task(task)
    total_cost += analysis.estimated_cost
    print(f"{task}: {analysis.recommended_model.upper()}")

print(f"\nOptimized cost: ${total_cost:.6f}")
print(f"Using Opus for all: ${total_cost * 4.5:.6f}")
print(f"Savings: {((1 - total_cost / (total_cost * 4.5)) * 100):.1f}%")
```

**Output:**
```
List all files: HAIKU
Analyze code: SONNET
Design architecture: OPUS
Convert JSON: HAIKU
Plan migration: OPUS

Optimized cost: $0.032
Using Opus for all: $0.144
Savings: 77.8%
```

---

## 📖 Documentation

### How It Works

The selector uses a multi-factor algorithm to calculate complexity:

1. **Keyword Analysis**
   - Simple indicators (`list`, `extract`, `quick`) → Lower complexity
   - Standard indicators (`analyze`, `implement`, `create`) → Medium complexity
   - Complex indicators (`design`, `architect`, `plan`) → Higher complexity

2. **Pattern Matching**
   - Planning tasks → +40 points
   - Complex coding → +35 points
   - Research/analysis → +30 points
   - Simple operations → -30 points

3. **Context Factors**
   - Task description length
   - Additional context provided
   - Multi-step indicators
   - Uncertainty markers

4. **Final Score** (0-100) → Model Selection
   - 0-30: Haiku (fast & cheap)
   - 31-70: Sonnet (balanced)
   - 71-100: Opus (powerful)

### CLI Commands

#### `analyze` - Analyze a Task

```bash
# Basic analysis
claude-model-selector analyze "Your task description"

# With additional context
claude-model-selector analyze "Optimize this code" --context-file code.py

# JSON output
claude-model-selector analyze "Task" --json

# Save results
claude-model-selector analyze "Task" --output analysis.json

# Verbose mode
claude-model-selector analyze "Task" --verbose
```

#### `compare` - Compare Models

```bash
# Compare all models for a task
claude-model-selector compare "Implement authentication"

# With custom token estimate
claude-model-selector compare "Large batch job" --tokens 100000
```

#### `batch` - Batch Processing

```bash
# Analyze tasks from file
claude-model-selector batch tasks.txt

# With verbose output
claude-model-selector batch tasks.txt --verbose

# Save results
claude-model-selector batch tasks.txt --output results.json
```

#### `info` - Model Information

```bash
# Show all models
claude-model-selector info

# Specific model
claude-model-selector info --model opus
```

### Python API Reference

#### `quick_select(task: str) -> str`

Fast model selection without full analysis.

```python
from claude_model_selector import quick_select

model = quick_select("Design scalable architecture")
# Returns: 'opus'
```

#### `ClaudeModelSelector`

Main selector class for detailed analysis.

```python
from claude_model_selector import ClaudeModelSelector

selector = ClaudeModelSelector()

# Analyze task
analysis = selector.analyze_task(
    task="Your task description",
    context="Optional additional context"
)

# Access results
print(analysis.recommended_model)  # 'haiku', 'sonnet', or 'opus'
print(analysis.complexity_score)   # 0-100
print(analysis.confidence)          # 0-1
print(analysis.estimated_cost)      # USD
print(analysis.reasoning)           # Explanation

# Compare models
comparisons = selector.compare_models(
    task="Your task",
    estimated_tokens=50000
)

# Get model info
info = selector.get_model_info('opus')
```

---

## ⚙️ Configuration

Customize behavior by creating `config.json`:

```json
{
  "thresholds": {
    "haiku_max": 30,
    "sonnet_max": 70
  },
  "default_model": "sonnet",
  "cost_optimization": true,
  "custom_rules": {
    "force_opus_keywords": ["critical", "production", "security"],
    "force_haiku_keywords": ["trivial", "simple", "quick"]
  }
}
```

Load custom configuration:

```python
from pathlib import Path
from claude_model_selector import ClaudeModelSelector

selector = ClaudeModelSelector(config_path=Path('config.json'))
```

---

## 🎓 Examples

### Example 1: Integration with API Calls

```python
import anthropic
from claude_model_selector import quick_select

def smart_claude_call(task, content):
    """Call Claude with optimal model selection"""
    model_name = quick_select(task)

    # Map to actual model IDs
    model_map = {
        'haiku': 'claude-3-haiku-20240307',
        'sonnet': 'claude-3-5-sonnet-20241022',
        'opus': 'claude-3-opus-20240229'
    }

    client = anthropic.Anthropic(api_key="your-key")
    response = client.messages.create(
        model=model_map[model_name],
        max_tokens=1024,
        messages=[{"role": "user", "content": content}]
    )

    return response

# Use it
result = smart_claude_call(
    task="Analyze this code for bugs",
    content="def foo(): return bar"
)
```

### Example 2: Cost Tracking

```python
from claude_model_selector import ClaudeModelSelector

selector = ClaudeModelSelector()
tasks = ["Task 1", "Task 2", "Task 3"]

total_cost = 0
for task in tasks:
    analysis = selector.analyze_task(task)
    total_cost += analysis.estimated_cost

print(f"Estimated total cost: ${total_cost:.6f}")
```

### Example 3: Confidence-Based Decisions

```python
from claude_model_selector import ClaudeModelSelector

selector = ClaudeModelSelector()
analysis = selector.analyze_task("Ambiguous task")

if analysis.confidence < 0.7:
    print(f"⚠️  Low confidence ({analysis.confidence:.0%})")
    print(f"Consider: More specific task description")
    print(f"Reasoning: {analysis.reasoning}")
else:
    print(f"✓ Recommended: {analysis.recommended_model.upper()}")
```

---

## 🧪 Testing

```bash
# Run tests
python -m pytest tests/

# With coverage
python -m pytest tests/ --cov=claude_model_selector

# Run examples
python examples/basic_usage.py
python examples/batch_processing.py
```

---

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup

```bash
# Clone the repository
git clone https://github.com/aeonbridge/claude-model-selector.git
cd claude-model-selector

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black src/ tests/
```

---

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details.

Copyright (c) 2025 AeonBridge Co.

---

## 🙏 Acknowledgments

- Built with ❤️ by [AeonBridge Co.](https://github.com/aeonbridge)
- Inspired by the need for cost-effective AI usage
- Thanks to Anthropic for creating Claude

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/aeonbridge/claude-model-selector/issues)
- **Discussions**: [GitHub Discussions](https://github.com/aeonbridge/claude-model-selector/discussions)
- **Email**: support@aeonbridge.com

---

## 🗺️ Roadmap

- [ ] PyPI package publication
- [ ] Integration examples for popular frameworks
- [ ] Web UI for visual analysis
- [ ] Advanced ML-based complexity prediction
- [ ] Support for other AI model providers
- [ ] Cost tracking and analytics dashboard
- [ ] Team collaboration features
- [ ] CI/CD integration templates

---

## ⭐ Star History

If you find this project useful, please consider giving it a star on GitHub!

---

**Made with ❤️ by AeonBridge Co.**
