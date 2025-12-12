from setuptools import setup, find_packages

# Read README.md for long_description
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="quantum-machine",
    version="3.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "typer",  # For CLI functionality
        "rich",   # For enhanced terminal output
        "flake8", # For linting (default tool used in lint.py)
        "pyyaml", # For YAML file handling
        # Add other linting tools if needed, e.g., "pylint"
    ],
    entry_points={
        "console_scripts": [
            "quantum=qm.main:app"
        ]
    },
    author="Quantum Datalytica LLC",
    author_email="itsupport@quantumdatalytica.com",
    description="Quantum-CLI: A powerful CLI to build, run, and test Quantum Machines.",
    long_description=long_description,
    long_description_content_type="text/markdown",  # ✅ Supports Markdown rendering
    url="https://www.quantumdatalytica.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)