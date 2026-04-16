import json
import os


class DockerGenerator:

    def __init__(self, project_path):
        self.project_path = project_path
        self.metadata_path = os.path.join(project_path, "reproflow_metadata.json")

    def load_metadata(self):
        with open(self.metadata_path) as f:
            return json.load(f)

    def generate_dockerfile(self):

        metadata = self.load_metadata()

        language = metadata["language"]
        dependency = metadata["dependency_file"]
        entry_command = metadata["entry_command"]

        dockerfile_path = os.path.join(self.project_path, "Dockerfile")
        
        uid = os.getuid() if hasattr(os, 'getuid') else 1000
        gid = os.getgid() if hasattr(os, 'getgid') else 1000

        if language == "Python":          
            py_version = "3.10"
            py_ver_path = os.path.join(self.project_path, ".python-version")
            if os.path.exists(py_ver_path):
                with open(py_ver_path) as pv:
                    py_version = pv.read().strip()

            cmd_list = entry_command.split()

            content = f"""
FROM python:{py_version}

# Create non-root user
RUN groupadd -g {gid} reprogroup || true && \\
    useradd -u {uid} -m -s /bin/bash -g reprogroup repro || true

WORKDIR /app
COPY . /app
RUN chown -R repro:reprogroup /app

USER repro

RUN pip install --no-cache-dir -r {dependency}

CMD {json.dumps(cmd_list)}
"""

        elif language == "Node":
            node_version = "18"
            nvmrc_path = os.path.join(self.project_path, ".nvmrc")
            if os.path.exists(nvmrc_path):
                with open(nvmrc_path) as nv:
                    node_version = nv.read().strip().replace('v', '')

            cmd_list = entry_command.split()

            content = f"""
FROM node:{node_version}

# Create non-root user
RUN groupadd -g {gid} reprogroup || true && \\
    useradd -u {uid} -m -s /bin/bash -g reprogroup repro || true

WORKDIR /app
COPY . /app
RUN chown -R repro:reprogroup /app

USER repro

RUN npm install

CMD {json.dumps(cmd_list)}
"""

        elif language == "Java":
            content = f"""
FROM maven:3.8-openjdk-17

# Create non-root user
RUN groupadd -g {gid} reprogroup || true && \\
    useradd -u {uid} -m -s /bin/bash -g reprogroup repro || true

WORKDIR /app
COPY . /app
RUN chown -R repro:reprogroup /app

USER repro

RUN mvn package -DskipTests

CMD {json.dumps(entry_command.split())}
"""
        else:
            content = f"""
FROM ubuntu:latest

# Create non-root user
RUN groupadd -g {gid} reprogroup || true && \\
    useradd -u {uid} -m -s /bin/bash -g reprogroup repro || true

WORKDIR /app
COPY . /app
RUN chown -R repro:reprogroup /app

USER repro

CMD ["bash"]
"""

        with open(dockerfile_path, "w") as f:
            f.write(content.strip())

        print("Dockerfile generated successfully.")