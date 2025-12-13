# Changelog

All notable changes to Claude Model Selector will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-12-07

### Added
- Initial release of Claude Model Selector
- Intelligent complexity analysis engine (0-100 scoring)
- Automatic model selection (Haiku, Sonnet, Opus)
- CLI interface with 4 commands: analyze, compare, batch, info
- Python API with `quick_select()` and `ClaudeModelSelector` class
- Cost estimation and comparison across models
- Confidence scoring for reliability assessment
- Context-aware selection for better accuracy
- Batch processing support for multiple tasks
- Customizable configuration via JSON
- Keyword-based complexity indicators
- Pattern matching for task classification
- Zero external dependencies (pure Python)
- Comprehensive documentation
- Usage examples and integration patterns
- MIT License for maximum flexibility

### Features Detail

#### Core Engine
- Multi-factor complexity scoring algorithm
- Keyword analysis (simple, standard, complex indicators)
- Pattern matching (planning, coding, research, operations)
- Length-based complexity adjustment
- Context weight calculation
- Confidence scoring (0-1 range)

#### CLI Commands
- `analyze`: Analyze single task with detailed output
- `compare`: Compare all models with cost estimates
- `batch`: Process multiple tasks from file
- `info`: Display model information and pricing

#### Python API
- `quick_select(task)`: Fast one-liner model selection
- `ClaudeModelSelector.analyze_task()`: Detailed analysis
- `ClaudeModelSelector.compare_models()`: Cost comparison
- `ClaudeModelSelector.get_model_info()`: Model details

#### Model Selection Strategy
- Haiku (0-30 complexity): $0.80/$4.00 per MTok
- Sonnet (31-70 complexity): $3.00/$15.00 per MTok
- Opus (71-100 complexity): $15.00/$75.00 per MTok

#### Configuration
- Customizable complexity thresholds
- Custom keyword definitions
- Pattern rule configuration
- Force model selection keywords
- Project-specific rules

### Documentation
- Comprehensive README.md
- CONTRIBUTING.md guidelines
- Inline code documentation
- Usage examples
- API reference
- Integration patterns
- Best practices guide

### Testing
- Unit tests for core functionality
- Integration test examples
- Example usage scripts

---

## [Unreleased]

### Planned Features
- PyPI package publication
- Web UI for visual analysis
- Advanced ML-based complexity prediction
- Support for other AI providers
- Cost tracking dashboard
- Team collaboration features
- CI/CD integration templates
- Performance benchmarks
- Additional language support
- Video tutorials
- Community examples gallery

---

## Version History

### Version Numbering

We use [Semantic Versioning](https://semver.org/):

- **MAJOR** version: Incompatible API changes
- **MINOR** version: Backwards-compatible functionality additions
- **PATCH** version: Backwards-compatible bug fixes

### Links

- [1.0.0] - Initial release - 2025-12-07

---

## Migration Guides

### From 0.x to 1.0

This is the initial stable release. No migration needed.

---

## Support

For questions or issues:
- GitHub Issues: https://github.com/aeonbridge/claude-model-selector/issues
- Email: support@aeonbridge.com

---

**Maintained by AeonBridge Co.** | [GitHub](https://github.com/aeonbridge) | [Website](https://aeonbridge.com)
