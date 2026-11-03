
from pathlib import Path
from datetime import datetime
import subprocess
import shutil
import time

# =========================
# CONFIGURATION
# =========================

REPORTS = Path("reports")
RUNS = REPORTS / "RUNS"
LATEST = REPORTS / "LATEST"

SCRIPTS = [
    "job_finder.py",
    "proposal_agent.py",
    "agent.py",
]

# =========================
# START RUN
# =========================

REPORTS.mkdir(exist_ok=True)
RUNS.mkdir(exist_ok=True)

run_started = time.time()

run_id = datetime.now().strftime("%Y-%m-%d_%H-%M-%S_%f")
run_folder = RUNS / run_id

run_folder.mkdir(parents=True, exist_ok=False)

print("\n================================")
print("      AI MONEY AGENT")
print("================================")
print(f"Run ID: {run_id}\n")

# =========================
# RUN ALL AGENTS
# =========================

for script in SCRIPTS:
    print(f"\nRunning {script}...\n")

    result = subprocess.run(
        ["python", script],
        check=False
    )

    if result.returncode != 0:
        print(f"\nWARNING: {script} failed.")
        print("Continuing with remaining scripts...\n")

# =========================
# SAVE THIS RUN
# =========================

print("\nSaving reports for this run...")

generated_files = []

for file in REPORTS.iterdir():
    if not file.is_file():
        continue

    if file.stat().st_mtime >= run_started:
        generated_files.append(file)

if not generated_files:
    print("WARNING: No new report files were detected.")

for file in generated_files:
    shutil.copy2(file, run_folder / file.name)

# =========================
# UPDATE LATEST
# =========================

if LATEST.exists():
    shutil.rmtree(LATEST)

LATEST.mkdir(parents=True)

for file in generated_files:
    shutil.copy2(file, LATEST / file.name)

# =========================
# FINISH
# =========================

print("\n================================")
print("       AGENT COMPLETED")
print("================================")

print(f"\nRun reports: {run_folder}")
print(f"Latest reports: {LATEST}")

print("\nAll reports saved successfully.")
