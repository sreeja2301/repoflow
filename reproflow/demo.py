import time
import click
import os
import platform
import subprocess

from scanner.project_scanner import ProjectScanner
from environment.docker_generator import DockerGenerator
from environment.devcontainer_generator import DevcontainerGenerator
from environment.compose_generator import ComposeGenerator
from runner.run_generator import RunGenerator
from runner.makefile_generator import MakefileGenerator
from reprocheck.repro_check import ReproCheck
from docs.documentation_generator import DocumentationGenerator


def run_demo(project_path="example_pipeline"):
    click.clear()
    click.secho("==================================================", fg="cyan", bold=True)
    click.secho("         ReproFlow Live Demonstration ", fg="cyan", bold=True)
    click.secho("==================================================\n", fg="cyan", bold=True)
    
    click.secho(f"Targeting project directory: ./{project_path}", fg="yellow")
    time.sleep(1.5)

    # Step 1: Scanner
    click.secho("\n[Step 1] Initializing Project Scanner...", fg="green", bold=True)
    click.secho("Scanning repository for language frameworks, dependencies, and entry scripts...", dim=True)
    scanner = ProjectScanner(project_path)
    result = scanner.scan()
    time.sleep(1)
    
    click.secho(f"  --> Detected Language: {result['language']}", fg="magenta")
    click.secho(f"  --> Detected Dependency File: {result['dependency_file']}", fg="magenta")
    click.secho(f"  --> Detected Entry Command: {result['entry_command']}", fg="magenta")
    time.sleep(1.5)

    # Step 2: Environment
    click.secho("\n[Step 2] Generating Containerized Dev Environments...", fg="green", bold=True)
    click.secho("Building smart Dockerfiles, Compose specs, and VS Code Devcontainers based on detected stack...", dim=True)
    time.sleep(1)
    
    docker = DockerGenerator(project_path)
    docker.generate_dockerfile()
    click.secho("  --> Created: Dockerfile (with non-root user)", fg="cyan")
    
    devcontainer = DevcontainerGenerator(project_path)
    devcontainer.generate_devcontainer()
    click.secho("  --> Created: .devcontainer/devcontainer.json (with language-specific IDE hooks)", fg="cyan")

    compose = ComposeGenerator(project_path)
    compose.generate_compose()
    click.secho("  --> Created: docker-compose.yml", fg="cyan")
    time.sleep(1.5)

    # Step 3: Run Scripts
    click.secho("\n[Step 3] Emitting One-Command Execution Scripts...", fg="green", bold=True)
    runner = RunGenerator(project_path)
    runner.generate_run_script()
    click.secho("  --> Created: run.sh & run.ps1", fg="cyan")
    
    makefile = MakefileGenerator(project_path)
    makefile.generate_makefile()
    click.secho("  --> Created: Makefile (make build, run, clean)", fg="cyan")
    time.sleep(1.5)
    
    # Step 4: Documentation
    click.secho("\n[Step 4] Auto-generating Documentation...", fg="green", bold=True)
    docs = DocumentationGenerator(project_path)
    docs.generate_docs()
    click.secho("  --> Created: Reproduce.md", fg="cyan")
    time.sleep(1.5)

    # Step 5: Execution
    click.secho("\n[Step 5] Executing Experiment in Sandbox Container...", fg="green", bold=True)
    click.secho("Firing cross-platform runner. Watch the container build & execute...\n", dim=True)
    time.sleep(1)

    try:
        if platform.system() == "Windows":
            subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", "./run.ps1"], cwd=project_path, check=True)
        else:
            subprocess.run(["bash", "run.sh"], cwd=project_path, check=True)
    except Exception as e:
        click.secho(f"\nDemo interrupted during container execution: {e}", fg="red")
        return
        
    time.sleep(1.5)

    # Step 6: Reproducibility Proof
    click.secho("\n[Step 6] Running Continuous Reproducibility Check...", fg="green", bold=True)
    click.secho("Executing the pipeline a second time to validate output determinism...", dim=True)
    checker = ReproCheck(project_path)
    try:
        checker.run_check()
    except Exception as e:
         click.secho(f"\nDemo interrupted during repro-check: {e}", fg="red")
         return
         
    click.secho("\n==================================================", fg="cyan", bold=True)
    click.secho("         Live Demonstration Complete! ", fg="cyan", bold=True)
    click.secho("==================================================\n", fg="cyan", bold=True)
