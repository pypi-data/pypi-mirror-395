# 🌿 IvyBloom CLI

> **Command-line interface for Ivy Biosciences' computational biology and drug discovery platform**

[![PyPI version](https://badge.fury.io/py/ivybloom.svg)](https://badge.fury.io/py/ivybloom)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Documentation](https://img.shields.io/badge/docs-latest-brightgreen.svg)](https://docs.ivybiosciences.com/cli)

Accelerate your computational biology research with powerful command-line tools for protein structure prediction, drug discovery, ADMET analysis, and workflow automation.

---

## 📑 Table of Contents

- [Quick Start](#-quick-start)
- [Key Features](#-key-features)
- [Terminal User Interface (TUI)](#-terminal-user-interface-tui)
- [Command Reference](#-command-reference)
- [Research Use Cases](#-research-use-cases)
- [Configuration](#-configuration)
- [Development](#-development)
- [Documentation](#-documentation)
- [Contributing](#-contributing)
- [Support](#-support)

---

## 🚀 Quick Start

### Installation

```bash
# Install from PyPI
pip install ivybloom

# Or with pipx for isolated environment
pipx install ivybloom
```

### Authentication

```bash
# Browser-based login (recommended)
ivybloom auth login --browser

# Or use API key authentication
ivybloom auth login --api-key YOUR_API_KEY
```

### Your First Job

```bash
# Predict protein structure with ESMFold
ivybloom run esmfold protein_sequence=MKLLVLGLVGFGVGFGVGFGVGFGVGFGVGFG

# Monitor progress in real-time
ivybloom jobs status JOB_ID --follow

# List recent jobs
ivybloom jobs list --limit 10
```

---

## ✨ Key Features

### 🧬 Computational Biology Tools

| Tool                   | Description                                       |
| ---------------------- | ------------------------------------------------- |
| **ESMFold**            | State-of-the-art protein structure prediction     |
| **AlphaFold**          | Deep learning protein folding integration         |
| **REINVENT**           | Generative drug design and molecular optimization |
| **ADMETLab3**          | Comprehensive ADMET property prediction           |
| **ProTox3**            | Toxicity assessment and safety profiling          |
| **AiZynthFinder**      | Retrosynthesis and synthesis planning             |
| **DeepSol**            | Protein solubility prediction                     |
| **Fragment Libraries** | Fragment-based drug discovery screening           |

### 🔗 Advanced Workflows

- **Job Chaining**: Link multiple analyses with automatic parameter passing
- **Parallel Execution**: Run multiple optimizations simultaneously
- **YAML Workflows**: Define complex multi-step pipelines declaratively
- **Dry-Run Mode**: Validate workflows before execution
- **Progress Tracking**: Real-time status updates and result reporting

### 🎨 Professional Interface

- **Earth-Tone Design**: Biology-inspired, eye-friendly color scheme
- **Rich Formatting**: Progress bars, tables, spinners, and status indicators
- **Multiple Formats**: Output as JSON, YAML, CSV, or formatted tables
- **Interactive Prompts**: Guided input with validation and suggestions
- **Shell Completion**: Tab completion for commands and arguments

### 🔐 Enterprise Authentication

- **Browser OAuth**: Seamless "click here to login" experience with PKCE
- **Device Flow**: Perfect for SSH sessions and headless environments
- **API Keys**: Traditional authentication for CI/CD and automation
- **Secure Storage**: System keyring with encrypted file fallback

---

## 🖥 Terminal User Interface (TUI)

Launch the full-featured terminal UI for an interactive experience:

```bash
ivybloom tui
```

### TUI Features

- **Three-Panel Layout**: Jobs list, details view, and artifact preview
- **Real-Time Updates**: Live job status with adaptive refresh
- **Protein Visualization**: ASCII/braille protein structure rendering
- **Molecule Viewer**: SMILES depiction and molecular preview
- **Command Palette**: Fuzzy search for all commands (`Ctrl+K`)
- **Artifact Browser**: Preview JSON, CSV, PDB, and more inline
- **Project Switcher**: Quickly switch between projects

### TUI Keybindings

| Key       | Action                |
| --------- | --------------------- |
| `Ctrl+K`  | Open command palette  |
| `j` / `k` | Navigate jobs list    |
| `l`       | Follow selected job   |
| `a`       | View artifacts        |
| `o`       | Open primary artifact |
| `?`       | Show help overlay     |
| `q`       | Quit TUI              |

---

## 📋 Command Reference

### Core Commands

```bash
# Authentication
ivybloom auth login --browser      # Browser OAuth login
ivybloom auth status               # Check authentication status
ivybloom auth logout               # Clear credentials

# Jobs
ivybloom jobs list                 # List all jobs
ivybloom jobs status JOB_ID        # Get job details
ivybloom jobs status JOB_ID --follow  # Stream live updates
ivybloom jobs results JOB_ID       # Get job results
ivybloom jobs cancel JOB_ID        # Cancel a running job

# Tools
ivybloom tools list                # List available tools
ivybloom tools info TOOL_NAME      # Get tool details and parameters
ivybloom tools schema TOOL_NAME    # Get JSON schema for tool

# Running Jobs
ivybloom run TOOL_NAME param=value # Run a tool with parameters
ivybloom run esmfold --help        # Get help for specific tool

# Projects
ivybloom projects list             # List your projects
ivybloom projects info PROJECT_ID  # Get project details

# Workflows
ivybloom workflows run FILE.yaml   # Execute a workflow file
ivybloom workflows validate FILE   # Validate workflow syntax

# Account
ivybloom account info              # View account details
ivybloom account usage             # Check usage and limits

# Configuration
ivybloom config get KEY            # Get config value
ivybloom config set KEY VALUE      # Set config value
ivybloom config list               # List all settings
ivybloom config edit               # Interactive config editor
```

### Output Formats

All listing commands support multiple output formats:

```bash
ivybloom jobs list --format json   # JSON output
ivybloom jobs list --format yaml   # YAML output
ivybloom jobs list --format csv    # CSV output
ivybloom jobs list --format table  # Rich table (default)
```

---

## 🔬 Research Use Cases

### Protein Structure Prediction

```bash
# Single protein prediction
ivybloom run esmfold protein_sequence=MKFLILLFNILCLFPVLAADNHGVGPQGAS

# With project assignment
ivybloom run esmfold protein_sequence=MKFLILLFNILCLFPVLAADNHGVGPQGAS \
    --project-id my-project
```

### Drug Discovery Pipeline

```yaml
# drug_pipeline.yaml
name: protein_to_drug_pipeline
description: End-to-end drug discovery workflow

steps:
  - name: predict_structure
    tool: esmfold
    parameters:
      protein_sequence: ${input.sequence}

  - name: generate_candidates
    tool: reinvent
    depends_on: predict_structure
    parameters:
      target_structure: ${predict_structure.output.pdb_file}
      num_molecules: 100

  - name: filter_admet
    tool: admetlab3
    depends_on: generate_candidates
    parameters:
      molecules: ${generate_candidates.output.molecules}
```

```bash
# Run the pipeline
ivybloom workflows run drug_pipeline.yaml \
    --input sequence=MKLLVLGLVGFGVGFGVGFGVGFGVGFGVGFG \
    --project-id drug-discovery
```

### High-Throughput Screening

```bash
# Batch processing with parallel execution
ivybloom batch run admetlab3 \
    --input-file compounds.csv \
    --parallel 10 \
    --project-id screening-2025
```

### Fragment-Based Design

```bash
ivybloom workflows run fragment_discovery.yaml \
    --input target_protein=structure.pdb \
    --input fragment_library=fragments.sdf \
    --parallel
```

---

## ⚙️ Configuration

Configuration is stored in `~/.config/ivybloom/config.json`.

### Key Settings

```bash
# Set default project
ivybloom config set default_project_id my-project

# Enable debug mode
ivybloom config set debug true

# Configure API timeout
ivybloom config set timeout 60

# Set default output format
ivybloom config set default_format table

# View all settings
ivybloom config list

# View configuration schema
ivybloom config schema
```

### Environment Variables

```bash
# API authentication
export IVYBLOOM_API_KEY=ivy_sk_...

# Alternative key name
export IVY_API_KEY=ivy_sk_...

# Disable keyring storage
export IVYBLOOM_DISABLE_KEYRING=1

# Enable debug output
export IVYBLOOM_DEBUG=1
```

---

## 🛠 Development

### Local Installation

```bash
# Clone the repository
git clone https://github.com/ivybiosciences/ivybloom-cli.git
cd ivybloom-cli

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Verify installation
ivybloom --version
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=ivybloom_cli

# Run specific test file
pytest tests/test_run_parsing.py

# Run only unit tests
pytest -m unit
```

### Code Quality

```bash
# Format code with Black
black ivybloom_cli tests

# Lint with Flake8
flake8 ivybloom_cli

# Type check with Mypy
mypy ivybloom_cli
```

---

## 📚 Documentation

| Resource                                              | Description                    |
| ----------------------------------------------------- | ------------------------------ |
| [CLI Guide](docs/cli/README.md)                       | Complete feature documentation |
| [User Guide](docs/user/USER_GUIDE.md)                 | Getting started and tutorials  |
| [Authentication](docs/user/guides/authentication.md)  | Auth setup and security        |
| [Commands Reference](docs/user/COMMANDS_REFERENCE.md) | Full command documentation     |
| [Workflow Examples](docs/cli/examples/)               | Real-world pipeline examples   |
| [TUI Design](docs/tui/tui_design.md)                  | Terminal UI architecture       |
| [API Reference](https://docs.ivybiosciences.com/api)  | Backend API documentation      |

---

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

```bash
# Quick contribution workflow
git checkout -b feature/your-feature
# Make changes...
pytest                    # Run tests
black ivybloom_cli tests  # Format code
git commit -m "feat: your feature description"
git push origin feature/your-feature
# Open a Pull Request
```

---

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

---

## 🆘 Support

- **Documentation**: [docs.ivybiosciences.com/cli](https://docs.ivybiosciences.com/cli)
- **Issues**: [GitHub Issues](https://github.com/ivybiosciences/ivybloom-cli/issues)
- **Discussions**: [GitHub Discussions](https://github.com/ivybiosciences/ivybloom-cli/discussions)
- **Email**: [support@ivybiosciences.com](mailto:support@ivybiosciences.com)

---

<p align="center">
  <strong>🌿 Computational Biology & Drug Discovery at Your Fingertips</strong>
  <br>
  <sub>Built with ❤️ by <a href="https://ivybiosciences.com">Ivy Biosciences</a></sub>
</p>
