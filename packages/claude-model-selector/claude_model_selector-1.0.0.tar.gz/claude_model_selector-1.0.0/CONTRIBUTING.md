# Contributing to Claude Model Selector

First off, thank you for considering contributing to Claude Model Selector! It's people like you that make this tool better for everyone.

## 🌟 Ways to Contribute

- **Bug Reports**: Found a bug? Let us know!
- **Feature Requests**: Have an idea? We'd love to hear it!
- **Code Contributions**: Submit pull requests
- **Documentation**: Improve or add documentation
- **Examples**: Share how you're using the tool
- **Testing**: Help test new features

## 🚀 Getting Started

### 1. Fork the Repository

Click the "Fork" button at the top right of the repository page.

### 2. Clone Your Fork

```bash
git clone https://github.com/YOUR_USERNAME/claude-model-selector.git
cd claude-model-selector
```

### 3. Set Up Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Install pre-commit hooks (optional but recommended)
pip install pre-commit
pre-commit install
```

### 4. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

## 📝 Development Guidelines

### Code Style

We use **Black** for code formatting and **Flake8** for linting.

```bash
# Format code
black src/ tests/

# Check linting
flake8 src/ tests/

# Type checking
mypy src/
```

### Code Standards

- **PEP 8** compliance (handled by Black)
- **Type hints** for all functions
- **Docstrings** for all public APIs (Google style)
- **Comments** for complex logic
- **Tests** for all new features

### Example Code Format

```python
"""Module docstring."""

from typing import Optional

class ExampleClass:
    """Class docstring.

    Attributes:
        attribute: Description of attribute.
    """

    def example_method(self, param: str, optional: Optional[int] = None) -> bool:
        """Method docstring.

        Args:
            param: Description of param.
            optional: Description of optional parameter.

        Returns:
            Description of return value.

        Raises:
            ValueError: When param is invalid.
        """
        if not param:
            raise ValueError("param cannot be empty")
        return True
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=claude_model_selector --cov-report=html

# Run specific test file
pytest tests/test_selector.py

# Run specific test
pytest tests/test_selector.py::test_quick_select
```

### Writing Tests

- Place tests in `tests/` directory
- Name test files as `test_*.py`
- Name test functions as `test_*`
- Use descriptive test names
- Test both success and failure cases

Example test:

```python
import pytest
from claude_model_selector import quick_select

def test_quick_select_simple_task():
    """Test that simple tasks select Haiku."""
    result = quick_select("List all files")
    assert result == "haiku"

def test_quick_select_complex_task():
    """Test that complex tasks select Opus."""
    result = quick_select("Design comprehensive architecture")
    assert result == "opus"
```

## 📋 Pull Request Process

### 1. Update Documentation

- Update README.md if needed
- Update docstrings
- Add/update examples
- Update CHANGELOG.md

### 2. Run Tests

```bash
# Run full test suite
pytest

# Check code style
black src/ tests/ --check
flake8 src/ tests/
mypy src/
```

### 3. Commit Your Changes

Use clear, descriptive commit messages:

```bash
git add .
git commit -m "Add feature: intelligent batch processing

- Implement parallel task analysis
- Add progress tracking
- Include cost estimation summary
- Add tests for batch processing
"
```

### 4. Push to Your Fork

```bash
git push origin feature/your-feature-name
```

### 5. Create Pull Request

1. Go to the original repository
2. Click "New Pull Request"
3. Select your fork and branch
4. Fill in the PR template
5. Submit!

### PR Template

```markdown
## Description
Brief description of what this PR does.

## Type of Change
- [ ] Bug fix (non-breaking change)
- [ ] New feature (non-breaking change)
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] New tests added for new features
- [ ] Manual testing completed

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] No new warnings generated
```

## 🐛 Reporting Bugs

### Before Submitting

- Check existing issues
- Verify you're using the latest version
- Collect relevant information

### Bug Report Template

```markdown
**Describe the Bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Import '...'
2. Call method '...'
3. See error

**Expected Behavior**
What you expected to happen.

**Actual Behavior**
What actually happened.

**Code Sample**
```python
# Minimal code to reproduce
from claude_model_selector import quick_select
result = quick_select("...")
```

**Environment**
- OS: [e.g., macOS 13.0]
- Python: [e.g., 3.11.0]
- Version: [e.g., 1.0.0]

**Additional Context**
Any other relevant information.
```

## 💡 Feature Requests

We love new ideas! Please provide:

1. **Use Case**: Why do you need this feature?
2. **Proposed Solution**: How should it work?
3. **Alternatives**: What alternatives have you considered?
4. **Examples**: Show example usage

## 📚 Documentation Contributions

Documentation is just as important as code!

### What to Document

- API references
- Usage examples
- Tutorials
- Best practices
- FAQs

### Documentation Style

- Clear, concise language
- Code examples for all features
- Real-world use cases
- Screenshots/diagrams where helpful

## 🔒 Security Issues

**Do NOT** open public issues for security vulnerabilities.

Instead, email: security@aeonbridge.com

Include:

- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

## 📜 Code of Conduct

### Our Pledge

We pledge to make participation in our project a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards

**Positive behavior includes:**

- Using welcoming and inclusive language
- Being respectful of differing viewpoints
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards others

**Unacceptable behavior includes:**

- Trolling, insulting/derogatory comments
- Public or private harassment
- Publishing others' private information
- Other unprofessional conduct

### Enforcement

Violations may result in:

1. Warning
2. Temporary ban
3. Permanent ban

Report violations to: conduct@aeonbridge.com

## 💬 Communication Channels

- **GitHub Issues**: Bug reports, feature requests
- **GitHub Discussions**: Questions, ideas, general discussion
- **Email**: support@aeonbridge.com
- **Discord**: [Coming soon]

## 🎯 Priority Areas

We're especially interested in contributions for:

1. **Performance Optimization**
   - Faster complexity analysis
   - Batch processing improvements

2. **New Features**
   - Web UI
   - Advanced analytics
   - Integration examples

3. **Documentation**
   - More examples
   - Video tutorials
   - Translation to other languages

4. **Testing**
   - Edge cases
   - Integration tests
   - Performance benchmarks

## 📦 Release Process

1. Version bump in `setup.py`
2. Update CHANGELOG.md
3. Create git tag: `git tag -a v1.0.0 -m "Version 1.0.0"`
4. Push tag: `git push origin v1.0.0`
5. Build: `python -m build`
6. Upload to PyPI: `twine upload dist/*`
7. Create GitHub release

## ❓ Questions?

Don't hesitate to ask! We're here to help.

- Open a [GitHub Discussion](https://github.com/aeonbridge/claude-model-selector/discussions)
- Email: support@aeonbridge.com

## 🙏 Thank You!

Your contributions make this project better for everyone. We appreciate your time and effort!

---

**Happy Contributing! 🚀**

*AeonBridge Co.*
