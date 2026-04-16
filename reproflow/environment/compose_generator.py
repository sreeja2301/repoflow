import os


class ComposeGenerator:

    def __init__(self, project_path):
        self.project_path = project_path

    def generate_compose(self):

        compose_content = """
version: '3'

services:
    experiment:
        build: .
        volumes:
            - ./outputs:/app/outputs
"""

        compose_path = os.path.join(self.project_path, "docker-compose.yml")

        with open(compose_path, "w") as f:
            f.write(compose_content)

        print("docker-compose.yml generated.")