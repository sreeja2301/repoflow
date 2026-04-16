import os
import json


class MakefileGenerator:

    def __init__(self, project_path):
        self.project_path = project_path
        self.metadata_path = os.path.join(project_path, "reproflow_metadata.json")

    def load_metadata(self):
        with open(self.metadata_path) as f:
            return json.load(f)

    def generate_makefile(self):
        metadata = self.load_metadata()
        entry_command = metadata["entry_command"]

        makefile_content = f""".PHONY: build run clean

build:
\t@echo "Building Docker container..."
\tdocker build -t reproflow_experiment .

run: build
\t@echo "Creating outputs folder..."
\tmkdir -p outputs
\t@echo "Running experiment..."
\tdocker run \\
\t\t-v $(PWD)/outputs:/app/outputs \\
\t\treproflow_experiment \\
\t\t{entry_command}
\t@echo "Experiment finished. Outputs stored in ./outputs"

clean:
\t@echo "Cleaning outputs..."
\trm -rf outputs/*
\t@echo "Outputs cleaned."
"""
        makefile_path = os.path.join(self.project_path, "Makefile")

        with open(makefile_path, "w") as f:
            f.write(makefile_content)

        print("Makefile generated.")
