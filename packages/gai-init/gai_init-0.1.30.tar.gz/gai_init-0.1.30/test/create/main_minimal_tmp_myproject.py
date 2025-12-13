#!/usr/bin/env python3
"""
Standalone script to create a test project at /tmp/myproject_minimal using MINIMAL template.
Run with: python main_minimal_tmp_myproject.py
"""
import os
import sys
import shutil

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))

from gai.create.gai_create import create_project


def main():
    """
    Create a project at /tmp/myproject_minimal using the 'minimal' template.
    """
    project_dir = "/tmp/myproject_minimal"
    project_name = "myproject_minimal"
    template = "minimal"

    print(f"Creating project at: {project_dir}")
    print(f"Template: {template}")
    print("-" * 50)

    # Always remove existing project if it exists
    if os.path.exists(project_dir):
        print(f"🗑️  Removing existing project at {project_dir}...")
        shutil.rmtree(project_dir)
        print(f"✅ Deleted existing project")

    # Change to /tmp directory
    original_cwd = os.getcwd()
    try:
        os.chdir("/tmp")

        # Create the project with force=True to ensure clean creation
        create_project(project_name, template=template, force=True)

        # Verify and show contents
        if os.path.exists(project_dir):
            print("\n" + "=" * 50)
            print(f"✅ Project created successfully!")
            print(f"📁 Location: {project_dir}")
            print(f"📄 Contents:")
            print("=" * 50)

            # List all files and directories
            for root, dirs, files in os.walk(project_dir):
                level = root.replace(project_dir, "").count(os.sep)
                indent = " " * 2 * level
                print(f"{indent}{os.path.basename(root)}/")
                subindent = " " * 2 * (level + 1)
                for file in files:
                    print(f"{subindent}{file}")
        else:
            print(f"❌ Project was not created at {project_dir}")

    finally:
        os.chdir(original_cwd)


if __name__ == "__main__":
    main()
