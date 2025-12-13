import os
import shutil
import yaml


def create_experiment(
    yaml_path,
    module_count=10,
    module_entries="module_names",
    root_entries="root_files"
):
    """
    Create an experiment setup from a YAML configuration file.

    This function reads a YAML configuration file to create a folder structure
    and files for machine learning experiments. It supports creating module
    folders, initializing Python files, and organizing modules into a pipeline  
    using an MLOps by design approach.

    Args:
        yaml_path (str): Path to the YAML configuration file.
        module_count (int, optional): Maximum number of modules to include in
            the pipeline. Defaults to 10.
        module_entries (str, optional): Key in the YAML file for module names.
            Defaults to "module_names".
        root_entries (str, optional): Key in the YAML file for root-level files.
            Defaults to "root_files".

    Returns:
        None
    """

    # Ingest YAML file
    try:
        with open(yaml_path, "r") as file:
            module_config = yaml.safe_load(file)
    except FileNotFoundError:
        print("""YAML configuration file not found. Please create 
              an experiment_module YAML.""")
        return

    # Design contracts
    assert module_config is not None, "Failed to load YAML"
    assert module_entries in module_config, f"{module_entries} is missing in YAML config"
    module_names = module_config[module_entries]

    # Create Folders
    ml_folder = "ml_pipeline"
    if os.path.exists(ml_folder) and os.path.isdir(ml_folder):
        print("Experiment has already been set up")
        return
    else:
        # Create module folders and files
        for module_name, subnames in module_names.items():
            os.makedirs(module_name, exist_ok=True)
            init_file_path = os.path.join(module_name, "__init__.py")
            if not os.path.exists(init_file_path):
                with open(init_file_path, "w") as init_file:
                    init_file.write(f"# {init_file_path}")
            if subnames:
                for subname in subnames:
                    py_file_path = os.path.join(module_name, f"{subname}.py")
                    if not os.path.exists(py_file_path):
                        with open(py_file_path, "w") as py_file:
                            py_file.write(f"# {subname} in {module_name}")

        # Move ML folders to ml_pipeline
        os.makedirs(ml_folder, exist_ok=True)
        modules_to_move = [folder for i, folder in enumerate(module_names.keys()) if i < module_count]
        for module in modules_to_move:
            if os.path.exists(module):
                destination = os.path.join(ml_folder, module)
                shutil.move(module, destination)

    # Create other root level files
    assert root_entries in module_config, f"{root_entries} is missing in YAML config"
    root_files = module_config[root_entries]
    for root_file in root_files:
        with open(root_file, "w") as r_file:
            r_file.write(f"# {root_file}")

    print("Experiment created successfully")