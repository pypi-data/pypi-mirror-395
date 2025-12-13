from setuptools import setup, find_packages

setup(
    name="mlops-bydesign-quickstart",
    version="0.1.0",
    author="Abel O. Akeni",
    description="""Quickly create ML experiments with standardized folder 
    structures and tools for implementing key aspects of MLOps throughout 
    your project's lifecycle from folder set up to model training, evaluation, 
    hyperparameter tuning; model serving, demo, drift detection and 
    continuous training""",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/abelunbound/mlops-bydesign-quickstart",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=["PyYAML>=6.0"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)