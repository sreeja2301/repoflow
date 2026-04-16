import os
import json


class RunGenerator:

    def __init__(self, project_path):
        self.project_path = project_path
        self.metadata_path = os.path.join(project_path, "reproflow_metadata.json")

    def load_metadata(self):

        with open(self.metadata_path) as f:
            return json.load(f)

    def generate_run_script(self):

        metadata = self.load_metadata()

        entry_command = metadata["entry_command"]

        script_content_bash = f"""#!/bin/bash

echo "Building Docker container..."
docker build -t reproflow_experiment .

echo "Creating outputs folder..."
mkdir -p outputs

echo "Running experiment..."

docker run \\
    -v "$PWD/outputs":/app/outputs \\
    reproflow_experiment \\
    {entry_command}

echo "Experiment finished. Outputs stored in ./outputs"
"""

        script_content_ps1 = f"""Write-Host "Building Docker container..."
docker build -t reproflow_experiment .

Write-Host "Creating outputs folder..."
New-Item -ItemType Directory -Force -Path "outputs" | Out-Null

Write-Host "Running experiment..."

$CurrentDir = (Get-Location).Path
docker run `
    -v "$CurrentDir/outputs:/app/outputs" `
    reproflow_experiment `
    {entry_command}

Write-Host "Experiment finished. Outputs stored in ./outputs"
"""

        run_path_bash = os.path.join(self.project_path, "run.sh")
        run_path_ps1 = os.path.join(self.project_path, "run.ps1")

        with open(run_path_bash, "w", newline='\n') as f:
            f.write(script_content_bash)

        with open(run_path_ps1, "w") as f:
            f.write(script_content_ps1)

        os.chmod(run_path_bash, 0o755)

        print("run.sh and run.ps1 generated.")