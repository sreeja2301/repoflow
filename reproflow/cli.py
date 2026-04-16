import click
import os
import shutil
import subprocess
import platform

from scanner.project_scanner import ProjectScanner
from environment.docker_generator import DockerGenerator
from environment.devcontainer_generator import DevcontainerGenerator
from environment.compose_generator import ComposeGenerator
from runner.run_generator import RunGenerator
from runner.makefile_generator import MakefileGenerator
from reprocheck.repro_check import ReproCheck
from docs.documentation_generator import DocumentationGenerator
from demo import run_demo

@click.group()
def cli():
    """ReproFlow CLI - Reproducible Experiment Generator"""
    pass

@click.command()
@click.argument("project_path")
def reproduce(project_path):

    if shutil.which("docker") is None:
        click.secho(
            "\n[Error] Docker is not installed or not available in PATH. Please install Docker Desktop or make sure 'docker' can be run from the shell.",
            fg="red",
            bold=True,
        )
        return

    print("\nStep 1: Scanning project...")
    scanner = ProjectScanner(project_path)
    scanner.scan()

    print("Scan completed.")

    print("\nStep 2: Generating environment...")
    docker = DockerGenerator(project_path)
    docker.generate_dockerfile()

    devcontainer = DevcontainerGenerator(project_path)
    devcontainer.generate_devcontainer()

    compose = ComposeGenerator(project_path)
    compose.generate_compose()

    print("Environment generated.")

    print("\nStep 3: Generating run scripts...")
    runner = RunGenerator(project_path)
    runner.generate_run_script()
    
    makefile = MakefileGenerator(project_path)
    makefile.generate_makefile()

    print("Run scripts generated.")

    print("\nStep 4: Running experiment...")

    import subprocess
    try:
        if platform.system() == "Windows":
            print("Executing run.ps1 on Windows...")
            subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", "./run.ps1"], cwd=project_path, check=True)
        else:
            print("Executing run.sh...")
            subprocess.run(["bash", "run.sh"], cwd=project_path, check=True)
    except subprocess.CalledProcessError as e:
        click.secho(f"\n[Error] Experiment execution failed with exit code {e.returncode}.", fg="red", bold=True)
        click.secho("Please check the Docker build or run logs above.", fg="red")
        return
    except FileNotFoundError:
        click.secho("\n[Error] Execution failed. Is Docker installed and available in PATH?", fg="red", bold=True)
        return

    print("\nStep 5: Running reproducibility check...")
    checker = ReproCheck(project_path)
    try:
        checker.run_check()
    except subprocess.CalledProcessError as e:
        click.secho(f"\n[Error] Reproducibility check failed to execute container. Exit code: {e.returncode}", fg="red", bold=True)
        return
    except FileNotFoundError as e:
        click.secho(f"\n[Error] {e}", fg="red", bold=True)
        return

    print("\nStep 6: Generating documentation...")
    docs = DocumentationGenerator(project_path)
    docs.generate_docs()

    click.secho("\nReproduction pipeline completed successfully.", fg="green", bold=True)


@click.command()
@click.argument("project_path")
def scan(project_path):

    scanner = ProjectScanner(project_path)
    result = scanner.scan()

    print("\nProject Scan Results")
    print("---------------------")
    print("Language:", result["language"])
    print("Dependencies:", result["dependency_file"])
    print("Entry Command:", result["entry_command"])


@click.command()
@click.argument("project_path")
def generate(project_path):

    docker = DockerGenerator(project_path)
    docker.generate_dockerfile()

    devcontainer = DevcontainerGenerator(project_path)
    devcontainer.generate_devcontainer()

    compose = ComposeGenerator(project_path)
    compose.generate_compose()

    print("\nEnvironment generation completed.")


@click.command()
@click.argument("project_path")
def run(project_path):

    runner = RunGenerator(project_path)
    runner.generate_run_script()
    
    makefile = MakefileGenerator(project_path)
    makefile.generate_makefile()

    print("Run scripts created. Execute with ./run.sh or make run")

@click.command()
@click.argument("project_path")
def reprocheck(project_path):

    checker = ReproCheck(project_path)
    checker.run_check()

@click.command()
@click.argument("project_path")
def docs(project_path):

    generator = DocumentationGenerator(project_path)
    generator.generate_docs()
    
@click.command()
def demo():
    """Run an automated, visually guided ReproFlow tour on the example pipeline."""
    run_demo("example_pipeline")

cli.add_command(scan)
cli.add_command(generate)
cli.add_command(run)
cli.add_command(reprocheck)
cli.add_command(docs)
cli.add_command(reproduce)
cli.add_command(demo)

if __name__ == "__main__":
    cli()