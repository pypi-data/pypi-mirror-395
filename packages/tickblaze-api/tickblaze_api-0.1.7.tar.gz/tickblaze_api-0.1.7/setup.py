import os
import subprocess
import shutil
import tempfile

from setuptools import setup, find_packages
from setuptools.command.build_py import build_py as build_py_orig

with open("README.md", "r") as readme_file:
    description = readme_file.read()

class build_py(build_py_orig):
    def run(self):
        
        # === STEP #1: Build the C# console application (ScriptsCompiler) ===
        cs_proj = os.path.join(os.path.dirname(__file__), "..", "..", "Tickblaze.Python.ScriptsCompiler", "Tickblaze.Python.ScriptsCompiler.csproj")
        
        # Use a temporary directory for the build output
        with tempfile.TemporaryDirectory() as temp_out_dir:
            subprocess.check_call([
                "dotnet", "publish", cs_proj,
                "-c", "Release",
                "-o", temp_out_dir,
                "-r", "win-x64",
                "/p:PublishSingleFile=false", # <-- Publish the C# project as a single file EXE
                "/p:SelfContained=false", # <-- But without .NET runtime
            ])
            
            # Target folder inside the Python package
            references_dir = os.path.join(self.build_lib, "tbapi", "utilities")
            os.makedirs(references_dir, exist_ok=True)
            
            if os.path.exists(references_dir):
                shutil.rmtree(references_dir)
        
            # Copy the generated files into the package
            exe_dst = os.path.join(references_dir, "script_generator")
            shutil.copytree(temp_out_dir, exe_dst)
        
        
        # === STEP #2: Copy the source code of Scripts template project ===
        script_project_src = os.path.join(
            os.path.dirname(__file__),
            "..", "..",
            "Tickblaze.Python.Scripts"
        )
        
        script_project_dst = os.path.join(references_dir, "scripts_template_project")

        # Remove destination if it already exists
        if os.path.exists(script_project_dst):
            shutil.rmtree(script_project_dst)

        # Copy entire folder tree of the project into the package
        shutil.copytree(script_project_src, script_project_dst)        
        
        super().run()
        

# Todo: after migration to Python >= 3.10 use importlib.metadata for versioning.
setup(name = "tickblaze-api",
    license = "MIT",
    version = "0.1.7",
    packages = find_packages(),
    package_data = { "": ["*.dll"], },
    long_description = description,
    long_description_content_type = "text/markdown",
    cmdclass={"build_py": build_py},
    entry_points={
        "console_scripts": [
            "tbapi = tbapi.script_generator:main"
        ]
    },
)