"""
Setup configuration for Claude Model Selector
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name="claude-model-selector",
    version="1.0.0",
    author="AeonBridge Co.",
    author_email="support@aeonbridge.com",
    description="Intelligent model selection for optimal cost-effectiveness with Anthropic's Claude AI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aeonbridge/claude-model-selector",
    project_urls={
        "Bug Tracker": "https://github.com/aeonbridge/claude-model-selector/issues",
        "Documentation": "https://github.com/aeonbridge/claude-model-selector#readme",
        "Source Code": "https://github.com/aeonbridge/claude-model-selector",
        "Discussions": "https://github.com/aeonbridge/claude-model-selector/discussions",
    },
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Natural Language :: English",
    ],
    python_requires=">=3.8",
    install_requires=[
        # Zero dependencies - pure Python!
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "build>=0.10.0",
            "twine>=4.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "claude-model-selector=claude_model_selector.cli:main",
        ],
    },
    keywords=[
        "claude",
        "anthropic",
        "ai",
        "model-selection",
        "cost-optimization",
        "llm",
        "gpt",
        "machine-learning",
        "artificial-intelligence",
    ],
    include_package_data=True,
    package_data={
        "claude_model_selector": ["config.json"],
    },
    zip_safe=False,
)
