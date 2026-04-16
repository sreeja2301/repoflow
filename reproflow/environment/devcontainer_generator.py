import json
import os


class DevcontainerGenerator:

    def __init__(self, project_path):
        self.project_path = project_path
        self.metadata_path = os.path.join(project_path, "reproflow_metadata.json")

    def load_metadata(self):

        with open(self.metadata_path) as f:
            return json.load(f)

    def generate_devcontainer(self):

        metadata = self.load_metadata()
        language = metadata.get("language", "Python")
        
        devcontainer_dir = os.path.join(self.project_path, ".devcontainer")

        os.makedirs(devcontainer_dir, exist_ok=True)
        
        post_create_command = ""
        extensions = []
        
        if language == "Python":
            dependency_file = metadata.get("dependency_file", "requirements.txt")
            post_create_command = f"pip install -r {dependency_file}"
            extensions = ["ms-python.python"]
        elif language == "Node":
            post_create_command = "npm install"
            extensions = ["dbaeumer.vscode-eslint"]
        elif language == "Java":
            post_create_command = "mvn install"
            extensions = ["vscjava.vscode-java-pack"]
        else:
            post_create_command = "echo 'No specific installation steps'"
            extensions = []

        devcontainer_config = {
            "name": "ReproFlow Dev Container",
            "build": {
                "dockerfile": "../Dockerfile"
            },
            "postCreateCommand": post_create_command,
            "customizations": {
                "vscode": {
                    "extensions": extensions
                }
            }
        }

        path = os.path.join(devcontainer_dir, "devcontainer.json")

        with open(path, "w") as f:
            json.dump(devcontainer_config, f, indent=4)

        print(".devcontainer configuration generated.")