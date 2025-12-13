# Overview

Quickly create ML experiments with standardized folder structures and tools for implementing key aspects of MLOps throughout your project's lifecycle from folder set up to model training, evaluation, hyperparameter tuning; model serving, demo, drift detection and continuous training.

## Use Cases

- **Starting new ML projects** - Get a professional structure instantly
- **Team standardization** - Ensure consistent project layouts
- **MLOps best practices** - Built-in separation of concerns
- **Rapid prototyping** - Focus on code, not folder setup
- **Educational purposes** - Learn MLOps project organization


## Installation

```bash
pip install mlops-bydesign-quickstart
```

## Quick Start

### 1. Create a YAML Configuration File

Create a file named `my_experiment_modules.yaml` (you can copy example below into a .yaml file):

```yaml
module_names:
  00_config:
    - config_file
  01_data_ingestion_and_cleaning:
  02_exploratory_data_analysis:
  03_feature_engineering:
  04_feature_selection:
  05_data_preprocessing:
  06_model_training_and_evaluation:
    - training
    - evaluation
    - hyperparameter_tuning
  07_mlops_model_monitoring:
    - drift_detection
    - experiments_log_tracking
    - artifact_tracking
  08_model_serving:
    - api_deployment
    - batch_inference_pipeline
  09_mlops_orchestration:
  ml_pipeline: []
  assets: []
  layouts: []
  test_suite: []
  documentation: []

root_entries:
  - app.py
  - .env
  - README.md
  - requirements.txt
  - config.yaml
  - .gitignore
```

### 2. Generate Your Project Structure

```python
from mlops_bydesign_quickstart import create_experiment

# Create the complete MLOps project structure
create_experiment("my_project.yaml")
```

### 3. Result

Your project structure will be created:

```
assets/
└── __init__.py

layouts/
└── __init__.py

test_suite/
└── __init__.py

documentation/
└── __init__.py

ml_pipeline/
├── 00_config/
│   ├── __init__.py
│   └── config_file.py
├── 01_data_ingestion_and_cleaning/
│   └── __init__.py
├── 02_exploratory_data_analysis/
│   └── __init__.py
├── 03_feature_engineering/
│   └── __init__.py
├── 04_feature_selection/
│   └── __init__.py
├── 05_data_preprocessing/
│   └── __init__.py
├── 06_model_training_and_evaluation/
│   ├── __init__.py
│   ├── training.py
│   ├── evaluation.py
│   └── hyperparameter_tuning.py
├── 07_mlops_model_monitoring/
│   ├── __init__.py
│   ├── drift_detection.py
│   ├── experiments_log_tracking.py
│   └── artifact_tracking.py
├── 08_model_serving/
│   ├── __init__.py
│   ├── api_deployment.py
│   └── batch_inference_pipeline.py
└── 09_mlops_orchestration/
    └── __init__.py

app.py
.env
README.md
requirements.txt
config.yaml
.gitignore
```

## Function Parameters

```python
create_experiment(
    yaml_path,              # Path to your YAML configuration file
    module_count=10,        # Number of modules to include (default: 10)
    module_entries="module_names",   # YAML key for modules (default: "module_names")
    root_entries="root_files"        # YAML key for root files (default: "root_files")
)
```

## Example: Custom Configuration

```python
from mlops_bydesign_quickstart import create_experiment

# Use custom parameters
create_experiment(
    "custom_project.yaml",
    module_count=5,  # Only include first 5 modules
    module_entries="modules",
    root_entries="files"
)
```

## YAML Configuration Guide

### Basic Structure

```yaml
module_names:
  ml_module_folder_name1:
    - python_file_1
    - python_file_2
    - python_file_3
  ml_module_folder_name2:
    - python_file_1
  ml_module_folder_name3: []
  non_ml_module_folder_name: []

root_files:
  - file_1.txt
  - file_2.md
  - .env
```





## Features

- ✅ Automated folder and file creation
- ✅ Standardized MLOps project structure
- ✅ Customizable via YAML configuration
- ✅ Automatic `__init__.py` generation for Python packages
- ✅ Prevention of duplicate project creation
- ✅ Support for nested module structures


## Requirements

- Python >= 3.8
- PyYAML >= 6.0

## License

MIT License

## Contributing

Contributions welcome! Visit the [GitHub repository](https://github.com/abelunbound/mlops-bydesign-quickstart) to contribute.

## Author

Abel Akeni holds an MSc in Applied Artificial Intelligence and Data Science and has a wealth of expertise acquired through 10+ years of handling progressively complex analytical leadership roles and products within data-sensitive public and private sector environments. He has built production-grade AI systems end-to-end using Python's scientific computing stack (pandas, scikit-learn, PyTorch, statsmodels, dash), developed ETL (Extract, Transform and Load) data engineering pipelines with SQL and Databricks, and integrated Large Language Models (LLMs), machine learning and deep learning models including Long Short-Term Memory (LSTM) neural networks, and various classification algorithms into production systems with robust MLOps, model monitoring and workflow orchestration. 

## Links

- **PyPI**: https://pypi.org/project/mlops-bydesign-quickstart/
- **GitHub**: https://github.com/abelunbound/mlops-bydesign-quickstart
- **Issues**: https://github.com/abelunbound/mlops-bydesign-quickstart/issues