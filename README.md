# RepoFlow

**Automated Experiment Reproducibility Framework**

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

RepoFlow is a powerful local CLI engine that instantly turns raw machine learning models, scripts, and software workflows into fully reproducible, containerized pipelines.

Say goodbye to the "it works on my machine" problem. RepoFlow dynamically analyzes your project, generates the Docker environment, executes it in isolated containers, and scientifically proves its reproducibility through byte-level hashing—all with zero manual setup.

---

## The "Why"

When sharing research or code, reviewers and colleagues often spend hours piecing together environments, guessing dependency versions, and debugging path issues.

**RepoFlow solves this by:**

1. Scanning your raw code to figure out what it needs.
2. Generating Dockerfiles, Docker-Compose, and Run Scripts.
3. Validating reproducibility by running dual-execution tests and aggressively checking for variance in outputs (JSON, CSV, and byte-hashes).

## Before & After

Point RepoFlow at a barebones directory:

**Before (Your Code):**

```text
example_pipeline/
├── train.py
└── requirements.txt
```

Run a single command:

```bash
python reproflow/main.py reproduce example_pipeline/
```

**After (Ready for the World):**

```text
example_pipeline/
├── train.py
├── requirements.txt
├── Dockerfile                  <-- Automatically Generated Environment
├── docker-compose.yml          <-- Automatically Generated Microservices
├── Makefile                    <-- Automatically Generated Shortcuts
├── run.sh / run.ps1            <-- Automatically Generated CI/CD scripts
├── .devcontainer/              <-- Automatically Generated VSCode Config
├── reproflow_metadata.json     <-- Structural scan results
├── repro_report.json           <-- Variance analysis & reproducibility proof
└── Reproduce.md                <-- Automatically Generated Documentation
```

## Features

- **Language Agnostic Detection**: Automatically detects Python, Node.js, and Java project entry points.
- **Zero-Touch Containerization**: Auto-generates Dockerfile, docker-compose.yml, and Devcontainers.
- **Reproducibility Engine**: Runs your code in isolated containers twice, diffing file hashes, JSON keys, and CSV structures to guarantee determinism.
- **Auto-Documentation**: Creates a ready-to-publish Reproduce.md for peer reviewers.
- **Cross-Platform Scripting**: Generates run.sh for Linux/Mac and run.ps1 for Windows natively.

## Installation

1. **Clone the repository:**

```bash
git clone https://github.com/yourusername/RepoFlow.git
cd RepoFlow
```

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

3. **Prerequisites:**
   Ensure you have Docker installed and running on your system.

## Quick Start

Want to see it in action without doing any configuration? Run the built-in, automated demo on the provided example pipeline:

```bash
python reproflow/main.py demo
```

To run RepoFlow on your own project from scratch, simply use the reproduce command:

```bash
python reproflow/main.py reproduce path/to/your/project
```

## CLI Commands

RepoFlow is incredibly modular. You can run individual stages rather than the whole pipeline:

| Command             | Description                                                             |
| ------------------- | ----------------------------------------------------------------------- |
| `scan <path>`       | Scans project for language, dependencies, and the entry command.        |
| `generate <path>`   | Builds the Dockerfile, Devcontainer, and Compose files.                 |
| `run <path>`        | Creates the run.sh, run.ps1 and Makefile execution scripts.             |
| `reprocheck <path>` | Performs dual-execution container testing to check for output variance. |
| `docs <path>`       | Generates the Reproduce.md guide.                                       |
| `reproduce <path>`  | Runs all of the above steps sequentially.                               |
| `demo`              | Runs the automated visual tour using the example pipeline.              |

## Configuration (Optional)

Not happy with the auto-detection? You can override RepoFlow by creating a `.reproflow.yml` file in your target project directory:

```yaml
# .reproflow.yml
language: Python
dependency_file: requirements.txt
entry_command: python custom_script.py --epochs 10
```

## Contributing

Contributions are welcome. Please feel free to submit a Pull Request or open an issue if you encounter a bug or have a feature request.
