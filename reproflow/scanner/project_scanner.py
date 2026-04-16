import os
import json
import yaml


class ProjectScanner:

    def __init__(self, project_path):
        self.project_path = project_path
        self.language = None
        self.dependency_file = None
        self.entry_command = None

    def detect_language(self):

        files = os.listdir(self.project_path)

        if "requirements.txt" in files:
            self.language = "Python"
            self.dependency_file = "requirements.txt"
        elif "pyproject.toml" in files:
            self.language = "Python"
            self.dependency_file = "pyproject.toml"
        elif "Pipfile" in files:
            self.language = "Python"
            self.dependency_file = "Pipfile"
        elif "package.json" in files:
            self.language = "Node"
            self.dependency_file = "package.json"
        elif "pom.xml" in files:
            self.language = "Java"
            self.dependency_file = "pom.xml"
        else:
            self.language = "Unknown"

    def detect_entry_command(self):

        files = os.listdir(self.project_path)

        if self.language == "Python":
            python_candidates = ["train.py", "main.py", "run_experiment.py", "run.py", "app.py", "model.py"]
            for file in python_candidates:
                if file in files:
                    self.entry_command = f"python {file}"
                    return
            py_files = [f for f in files if f.endswith('.py')]
            if py_files:
                self.entry_command = f"python {py_files[0]}"
                return
            self.entry_command = "python script.py"

        elif self.language == "Node":
            try:
                with open(os.path.join(self.project_path, "package.json")) as f:
                    data = json.load(f)
                    if "scripts" in data and "start" in data["scripts"]:
                        self.entry_command = "npm start"
                        return
            except Exception:
                pass
                
            if "index.js" in files:
                self.entry_command = "node index.js"
            elif "app.js" in files:
                self.entry_command = "node app.js"
            else:
                self.entry_command = "npm start"

        elif self.language == "Java":
            if "pom.xml" in files:
                self.entry_command = "mvn exec:java"
            else:
                self.entry_command = "java -jar target/app.jar"
        else:
            self.entry_command = "echo 'Entry command not found'"

    def save_metadata(self, metadata):

        metadata_path = os.path.join(self.project_path, "reproflow_metadata.json")

        with open(metadata_path, "w") as f:
            json.dump(metadata, f, indent=4)

    def scan(self):

        self.detect_language()
        self.detect_entry_command()

        metadata = {
            "language": self.language,
            "dependency_file": self.dependency_file,
            "entry_command": self.entry_command
        }
        
        config_path = os.path.join(self.project_path, ".reproflow.yml")
        if os.path.exists(config_path):
            try:
                with open(config_path, "r") as f:
                    overrides = yaml.safe_load(f)
                    if overrides:
                        print("Applying user overrides from .reproflow.yml...")
                        if "language" in overrides:
                            metadata["language"] = overrides["language"]
                        if "dependency_file" in overrides:
                            metadata["dependency_file"] = overrides["dependency_file"]
                        if "entry_command" in overrides:
                            metadata["entry_command"] = overrides["entry_command"]
            except Exception as e:
                print(f"Warning: Failed to parse .reproflow.yml: {e}")

        self.save_metadata(metadata)

        return metadata