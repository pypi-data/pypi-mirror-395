"""Setup configuration for agent-framework-lib."""

from setuptools import setup
from setuptools.command.build_py import build_py
import subprocess
import sys
from pathlib import Path


class BuildWithDocs(build_py):
    """Custom build command that copies docs before building."""
    
    def run(self):
        """Run the build process with documentation copying."""
        # Copy documentation files
        scripts_dir = Path(__file__).parent / "scripts"
        copy_docs_script = scripts_dir / "copy_docs.py"
        
        if copy_docs_script.exists():
            print("Copying documentation files...")
            try:
                subprocess.run(
                    [sys.executable, str(copy_docs_script)],
                    check=True,
                    cwd=Path(__file__).parent
                )
                print("Documentation files copied successfully.")
            except subprocess.CalledProcessError as e:
                print(f"Warning: Failed to copy documentation files: {e}")
                print("Continuing with build...")
        else:
            print(f"Warning: copy_docs.py not found at {copy_docs_script}")
            print("Continuing with build without documentation copy...")
        
        # Continue with normal build
        super().run()


setup(
    cmdclass={
        'build_py': BuildWithDocs,
    }
)
