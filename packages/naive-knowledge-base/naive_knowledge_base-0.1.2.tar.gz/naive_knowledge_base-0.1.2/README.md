# Naive Knowledge Base

A dependency graph analyzer using smolagents for building and analyzing code dependencies.

## Features

- 🔍 **Dependency Graph Generation**: Automatically generate dependency graphs from source code
- 🤖 **AI-Powered Analysis**: Uses smolagents for intelligent code analysis
- 📊 **Multiple Language Support**: Support for Java and other languages
- 🌳 **Directory Tree Visualization**: Generate visual representations of project structure
- 📝 **File Operations**: Read, write, and manage files programmatically

## Installation

### From Source

```bash
git clone https://github.com/yourusername/naive-knowledge-base.git
cd naive-knowledge-base
pip install -e .
```

### From PyPI (when published)

```bash
pip install naive-knowledge-base
```

## Requirements

- Python 3.8+
- OpenAI API key (or compatible API)

## Configuration

Create a `.env` file in your project directory with the following:

```env
OPENAI_API_KEY=your_api_key_here
# Or configure your API endpoint
API_BASE_URL=your_api_base_url
```

## Usage

### Command Line Interface

After installation, you can use the `naive-kb` command:

```bash
# Basic usage
naive-kb /path/to/source/directory

# Specify file extensions
naive-kb /path/to/source/directory java

# Specify directories to ignore
naive-kb /path/to/source/directory java "target,.git,test,node_modules"
```

### Python API

```python
from naive_knowledge_base import run_analysis

# Run dependency graph analysis
result = run_analysis(
    source_directory="/path/to/source",
    file_extensions="java",
    ignore_dirs="target,.git,test"
)
```

### Advanced Usage

```python
from smolagents import CodeAgent, ToolCallingAgent
from naive_knowledge_base.api_models import FlowApiModel
from naive_knowledge_base.tools import (
    save_content_to_file,
    read_file_content,
    delete_folder_or_file,
    generate_folder_tree
)
from naive_knowledge_base.agents.dependency_graph import generate_dependency_graph

# Create custom agents
model = FlowApiModel(model_id="gpt-4.1", temperature=0.5)

dependency_agent = ToolCallingAgent(
    tools=[generate_dependency_graph],
    model=model,
    max_steps=7,
    name="dependency_graph_agent"
)

manager_agent = CodeAgent(
    managed_agents=[dependency_agent],
    model=model,
    tools=[read_file_content, save_content_to_file],
    max_steps=30,
    name="tech_lead_agent"
)

# Run analysis
result = manager_agent.run("Analyze dependencies in /path/to/source")
```

## Package Structure

```
naive_knowledge_base/
├── agents/
│   ├── common/          # Common agent utilities
│   │   ├── base.py
│   │   ├── exceptions.py
│   │   ├── logging.py
│   │   └── utils.py
│   └── dependency_graph/  # Dependency graph analysis
│       ├── agent.py
│       └── model.py
├── api_models/          # API model integrations
│   └── flow_api_model.py
└── tools/              # Agent tools
    ├── io.py           # File I/O operations
    └── tree.py         # Directory tree generation
```

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/yourusername/naive-knowledge-base.git
cd naive-knowledge-base

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in editable mode with dev dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest tests/
```

### Code Formatting

```bash
# Format code
black .
isort .

# Check code quality
pylint naive_knowledge_base/
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with [smolagents](https://github.com/huggingface/smolagents)
- Uses OpenAI API for AI-powered analysis

## Support

For issues and questions, please file an issue on the [GitHub repository](https://github.com/yourusername/naive-knowledge-base/issues).
