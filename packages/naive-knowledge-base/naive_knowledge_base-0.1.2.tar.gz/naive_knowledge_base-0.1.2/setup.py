"""Setup configuration for naive_knowledge_base package."""
from setuptools import setup
from pathlib import Path

# Read the contents of README file
this_directory = Path(__file__).parent
try:
    long_description = (this_directory / "README.md").read_text(encoding="utf-8")
except FileNotFoundError:
    long_description = "A dependency graph analyzer using smolagents"

# Core requirements - extracted from requirements.txt
# Note: Some advanced dependencies like emerge-viz and toon_format are optional
requirements = [
    "smolagents>=1.16.0",
    "python-dotenv>=1.0.0",
    "openai>=1.0.0",
    "requests>=2.32.0",
    "networkx>=3.0",
    "GitPython>=3.1.0",
    "PyYAML>=6.0",
    "pydantic>=2.0",
    "click>=8.0",
]

# Try to include additional requirements from requirements.txt
try:
    with open("requirements.txt") as f:
        for line in f:
            line = line.strip()
            # Skip empty lines, comments, and git-based packages
            if line and not line.startswith("#") and "git+" not in line and "@" not in line:
                pkg_name = line.split("==")[0].split(">=")[0].split("<=")[0]
                # Only add if not already in core requirements
                if not any(pkg_name in req for req in requirements):
                    requirements.append(line)
except FileNotFoundError:
    pass  # Use core requirements only

setup(
    name="naive-knowledge-base",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A dependency graph analyzer using smolagents",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/naive-knowledge-base",
    py_modules=["cli", "main"],
    packages=[
        "agents",
        "agents.common",
        "agents.dependency_graph",
        "api_models",
        "tools",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "naive-kb=cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["py.typed", "*.md", "*.txt"],
    },
    zip_safe=False,
)
