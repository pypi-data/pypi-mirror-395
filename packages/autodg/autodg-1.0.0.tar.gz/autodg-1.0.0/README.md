# API Analyzer

A modular, extensible Python API analyzer that scans codebases and generates comprehensive documentation with AI-powered explanations.

## Features

- **Multi-Framework Support**: Flask, FastAPI, Django, Django REST Framework
- **AI-Powered Documentation**: Supports Ollama, OpenAI, Claude, and Gemini
- **Call Graph Analysis**: Visualizes function dependencies
- **Database Operation Detection**: Identifies DB queries and operations
- **MermaidJS Diagrams**: Auto-generated architecture diagrams
- **File-wise Documentation**: AI overviews for every Python file
- **Progress Tracking**: Real-time progress with ETA

## Installation

```bash
pip install autodg
```

### Optional Dependencies (AI Features)

> **Note**: AI-powered documentation generation is an **experimental feature**.
> For the best local experience, we recommend running [Ollama](https://ollama.com/) with the `llama3.1` model.

To enable support for specific cloud LLM providers, install the package with the corresponding extras:

```bash
# OpenAI Support
pip install autodg[openai]

# Claude Support
pip install autodg[claude]

# Gemini Support
pip install autodg[gemini]

# Support for all providers
pip install autodg[all]
```

## Quick Start

```bash
autodg --paths /path/to/your/project --output ./docs
```

## Configuration

Create a `config.yaml` file:

```yaml
llm:
  provider: ollama  # Options: ollama, openai, claude, gemini
  
  ollama:
    host: http://localhost:11434
    model: llama3.1
```

## Usage

```bash
# Basic usage
autodg --paths /path/to/project --output ./output

# With LLM explanations
autodg --paths /path/to/project --output ./output --ollama True
```

## Supported Frameworks

- **Flask**: Routes, Blueprints
- **FastAPI**: APIRouter, nested routers, class-based routes
- **Django**: path(), re_path(), FBV, CBV
- **DRF**: Routers, ViewSets

## Output

The analyzer generates:
- `request_docs/`: Documentation for each API endpoint (optional ai explanations)
- `files/`: AI-powered overviews of each Python file (optional ai explanations)

## License

MIT License - see LICENSE file for details.

## Author

Dhinagaran S (atsupp02@gmail.com)
