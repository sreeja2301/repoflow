import os
import json
import subprocess
import hashlib
import shutil


class ReproCheck:

    def __init__(self, project_path):
        self.project_path = project_path
        self.metadata_path = os.path.join(project_path, "reproflow_metadata.json")

    def load_metadata(self):

        with open(self.metadata_path) as f:
            return json.load(f)

    def run_experiment(self, run_folder):

        os.makedirs(run_folder, exist_ok=True)

        try:
            subprocess.run(
                ["docker", "run",
                 "-v", f"{os.path.abspath(run_folder)}:/app/outputs",
                 "reproflow_experiment"],
                check=True
            )
        except FileNotFoundError:
            raise FileNotFoundError(
                "Docker executable not found. Install Docker and ensure 'docker' is available in PATH."
            )

    def _compare_files(self, file1, file2):
        if not os.path.exists(file2):
            return False, "File missing in run2"

        if file1.endswith('.json'):
            try:
                with open(file1) as f1, open(file2) as f2:
                    d1 = json.load(f1)
                    d2 = json.load(f2)
                    
                    for key in ['timestamp', 'run_time', 'execution_time', 'time']:
                        d1.pop(key, None)
                        d2.pop(key, None)
                        
                    return d1 == d2, "JSON diff"
            except Exception as e:
                return False, f"JSON parse error: {e}"
                
        elif file1.endswith('.csv'):
            try:
                with open(file1) as f1, open(file2) as f2:
                    lines1 = f1.readlines()
                    lines2 = f2.readlines()
                    if len(lines1) != len(lines2):
                        return False, "Row count differs"
                    for l1, l2 in zip(lines1, lines2):
                        if l1 != l2:
                            return False, "CSV content differs"
                    return True, "Match"
            except Exception as e:
                return False, f"CSV parse error: {e}"

        else:
            hash1 = hashlib.sha256()
            hash2 = hashlib.sha256()
            with open(file1, "rb") as f: hash1.update(f.read())
            with open(file2, "rb") as f: hash2.update(f.read())
            return hash1.hexdigest() == hash2.hexdigest(), "Byte hash diff"

    def compare_outputs(self, run1, run2):
        reproducible = True
        variance_log = []

        files1 = []
        for root, dirs, files in os.walk(run1):
            for file in files:
                files1.append(os.path.relpath(os.path.join(root, file), run1))
                
        for file in files1:
            f1_path = os.path.join(run1, file)
            f2_path = os.path.join(run2, file)
            
            match, reason = self._compare_files(f1_path, f2_path)
            if not match:
                reproducible = False
                variance_log.append({"file": file, "reason": reason})

        return reproducible, variance_log

    def safe_clean(self, runs_dir):
        if os.path.exists(runs_dir):
            for item in os.listdir(runs_dir):
                if item in ['run1', 'run2']:
                    shutil.rmtree(os.path.join(runs_dir, item))

    def run_check(self):

        runs_dir = os.path.join(self.project_path, "repro_runs")
        run1 = os.path.join(runs_dir, "run1")
        run2 = os.path.join(runs_dir, "run2")

        self.safe_clean(runs_dir)
        os.makedirs(run1, exist_ok=True)
        os.makedirs(run2, exist_ok=True)

        print("Running experiment: run1")
        self.run_experiment(run1)

        print("Running experiment: run2")
        self.run_experiment(run2)

        reproducible, variance_log = self.compare_outputs(run1, run2)

        report = {
            "reproducible": reproducible,
            "variance": variance_log
        }

        report_path = os.path.join(self.project_path, "repro_report.json")

        with open(report_path, "w") as f:
            json.dump(report, f, indent=4)

        print("\nReproducibility Report")
        print("----------------------")
        print("Reproducible:", reproducible)
        if not reproducible:
            print("Variance Found:")
            for v in variance_log:
                print(f"  - {v['file']}: {v['reason']}")