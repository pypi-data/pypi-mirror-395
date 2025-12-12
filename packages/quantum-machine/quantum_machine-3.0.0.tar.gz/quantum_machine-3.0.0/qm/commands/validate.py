import typer
import json
from pathlib import Path
import re

app = typer.Typer(help="Validate a Quantum Machine's structure and files.")

REQUIRED_METHODS = [
    "receiving",
    "pre_processing",
    "processing",
    "post_processing",
    "packaging_shipping"
]

REQUIRED_PROJECT_KEYS = {"name", "version", "title"}
REQUIRED_INPUT_KEYS = {"machine_name", "input_data", "output", "depends_machine"}

@app.command()
def machine(path: str):
    """
    Validate the structure and files of a Quantum Machine.

    Example:
        quantum validate machine HelloWorld
    """
    typer.secho("")
    path = path.strip().replace(" ","").lower()
    project_path = Path(path).resolve()

    # Validate main.py
    main_file = project_path / "main.py"
    if not main_file.exists():
        typer.secho("❌ main.py not found.", fg=typer.colors.RED)
        typer.secho("")
        raise typer.Exit(1)

    try:
        with open(main_file) as f:
            main_content = f.read()
    except Exception as e:
        typer.secho(f"❌ Error reading main.py: {e}", fg=typer.colors.RED)
        typer.secho("")
        raise typer.Exit(1)

    # Check for required import
    if "from quantum.CoreEngine import CoreEngine" not in main_content:
        typer.secho("❌ main.py must import 'from quantum.CoreEngine import CoreEngine'.", fg=typer.colors.RED)
        typer.secho("")
        raise typer.Exit(1)

    # Check for required class declaration
    class_pattern = r"class\s+(\w+)\(CoreEngine\):"
    match = re.search(class_pattern, main_content)
    if not match:
        typer.secho("❌ main.py must declare a class inheriting from 'CoreEngine'.", fg=typer.colors.RED)
        typer.secho("")
        raise typer.Exit(1)

    class_name = match.group(1)
    typer.secho(f"✅ Found class '{class_name}' inheriting from 'CoreEngine'.", fg=typer.colors.GREEN)

    # Check for required methods
    missing_methods = [method for method in REQUIRED_METHODS if f"def {method}(" not in main_content]
    if missing_methods:
        typer.secho(f"❌ main.py is missing required methods: {', '.join(missing_methods)}", fg=typer.colors.RED)
        typer.secho("")
        raise typer.Exit(1)

    typer.secho("✅ main.py is valid.", fg=typer.colors.GREEN)

    # Validate Project.json
    project_json_file = project_path / "Project.json"
    if not project_json_file.exists():
        typer.secho("❌ Project.json not found.", fg=typer.colors.RED)
        typer.secho("")
        raise typer.Exit(1)

    try:
        with open(project_json_file) as f:
            project_data = json.load(f)
    except json.JSONDecodeError:
        typer.secho("❌ Project.json is not valid JSON.", fg=typer.colors.RED)
        typer.secho("")
        raise typer.Exit(1)

    missing_project_keys = REQUIRED_PROJECT_KEYS - project_data.keys()
    if missing_project_keys:
        typer.secho(f"❌ Project.json is missing required keys: {', '.join(missing_project_keys)}", fg=typer.colors.RED)
        typer.secho("")
        raise typer.Exit(1)

    typer.secho("✅ Project.json is valid.", fg=typer.colors.GREEN)

    # Validate input.json
    input_json_file = project_path / "input.json"
    if not input_json_file.exists():
        typer.secho("")
        typer.secho("❌ input.json not found.", fg=typer.colors.RED)
        raise typer.Exit(1)

    try:
        with open(input_json_file) as f:
            input_data = json.load(f)
    except json.JSONDecodeError:
        typer.secho("❌ input.json is not valid JSON.", fg=typer.colors.RED)
        typer.secho("")
        raise typer.Exit(1)

    missing_input_keys = REQUIRED_INPUT_KEYS - input_data.keys()
    if missing_input_keys:
        typer.secho(f"❌ input.json is missing required keys: {', '.join(missing_input_keys)}", fg=typer.colors.RED)
        typer.secho("")
        raise typer.Exit(1)

    typer.secho("✅ input.json is valid.", fg=typer.colors.GREEN)

    # Final success message
    typer.secho("🎉 Quantum Machine validation passed!", fg=typer.colors.GREEN)

    typer.secho("")
