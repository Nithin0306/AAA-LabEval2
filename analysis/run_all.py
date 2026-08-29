#!/usr/bin/env python3
"""
run_all.py — Run all benchmarks for all three problems.
Usage:  python3 analysis/run_all.py
"""

import subprocess
import sys
import os

SCRIPTS = ["run_429.py", "run_10171.py", "run_321.py"]
DIR = os.path.dirname(__file__)

for script in SCRIPTS:
    path = os.path.join(DIR, script)
    print(f"\n{'='*60}")
    print(f"Running {script}")
    print("=" * 60)
    result = subprocess.run([sys.executable, path])
    if result.returncode != 0:
        print(f"[WARN] {script} exited with code {result.returncode}")

print("\nAll benchmarks complete.")
