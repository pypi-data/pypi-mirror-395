import subprocess
import sys
import os

def main():
    exe_path = os.path.join(os.path.dirname(__file__), "utilities", "script_generator", "Tickblaze.Python.ScriptsCompiler")
    subprocess.run([exe_path] + sys.argv[1:], check=False)