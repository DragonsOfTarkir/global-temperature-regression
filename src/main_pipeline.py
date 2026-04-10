#!/usr/bin/env python3
"""
Main Pipeline Script
Runs the complete climate analysis pipeline
"""

import subprocess
import sys
from pathlib import Path

def run_script(script_name):
    """Run a Python script"""
    script_path = Path('src') / script_name
    if script_path.exists():
        print(f"Running {script_name}...")
        result = subprocess.run([sys.executable, str(script_path)], cwd=Path.cwd())
        if result.returncode == 0:
            print(f"{script_name} completed successfully")
        else:
            print(f"Error in {script_name}")
    else:
        print(f"Script {script_name} not found")

def main():
    print("Starting Climate Analysis Pipeline")

    # Step 1: Data Collection
    run_script('data_collection.py')

    # Step 2: Data Preprocessing
    run_script('data_preprocessing.py')

    # Step 3: Model Training
    run_script('model_training.py')

    # Step 4: Visualization
    run_script('visualization.py')

    print("Pipeline completed!")
    print("Check the reports/ directory for results")

if __name__ == "__main__":
    main()