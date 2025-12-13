import subprocess
import sys
import os

def run_2to3(file_path):
    if not os.path.isfile(file_path):
        print(f"File not found: {file_path}")
        return

    try:
        subprocess.run([
            "2to3",
            "-w",        # Write changes to file
            "-n",        # No backup
            "-f", "all", # Apply all fixers
            file_path
        ], check=True)
        print(f"Converted {file_path} to Python 3.")
    except subprocess.CalledProcessError as e:
        print(f"Error running 2to3: {e}")