def create_project(project_name, template="minimal", force=False):
    """
    Create a new Gai project with the specified name and template.
    """

    import os
    import shutil

    # Define the base directory for templates
    print("this directory:", os.path.dirname(__file__))
    base_template_dir = os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
        "data",
        "data",
        "gai",
        "project-templates",
    )
    template_dir = os.path.join(base_template_dir, template)

    if not os.path.exists(template_dir):
        print(f"Error: Template '{template}' does not exist.")
        return

    curr_dir = os.getcwd()
    print(f"Current working directory: {curr_dir}")

    project_dir = os.path.join(curr_dir, project_name)
    print(f"Creating project directory at: {project_dir}")

    if os.path.exists(project_dir):
        if force:
            print(f"Warning: Directory '{project_dir}' already exists. Overwriting...")
            shutil.rmtree(project_dir)
        else:
            print(
                f"Error: Directory '{project_dir}' already exists. Use --force to overwrite."
            )
            return

    try:
        shutil.copytree(template_dir, project_dir)

        # Replace {{PROJECT_NAME}} in files
        for root, dirs, files in os.walk(project_dir):
            for file in files:
                file_path = os.path.join(root, file)
                with open(file_path, "r") as f:
                    content = f.read()
                content = content.replace("{{PROJECT_NAME}}", project_name)
                with open(file_path, "w") as f:
                    f.write(content)

        print(
            f"Project '{project_name}' created successfully using the '{template}' template."
        )
    except Exception as e:
        print(f"Error creating project: {e}")
