import os
import glob
import json
import typer
import platform
from pathlib import Path

app = typer.Typer(help="""
Fetch logs for a Quantum Machine.

    This command reads the input.json file of the specified machine to determine the workflow name
    and fetches the corresponding output logs from the workflow directory.

    Example:
        quantum logs machine MyMachine
""")

@app.command()
def machine(machine_name: str):
    """
    Fetch logs for a Quantum Machine.

    This command reads the input.json file of the specified machine to determine the workflow name
    and fetches the corresponding output logs from the workflow directory.

    Example:
        quantum logs machine MyMachine
    """
    typer.secho("")
    machine_name = machine_name.strip().replace(" ", "").lower()
    # Check if the machine folder exists
    machine_path = Path(machine_name).resolve()
    if not machine_path.exists():
        typer.secho(f"❌ '{machine_name}' Machine Folder not found.", fg=typer.colors.RED)
        typer.secho("")
        raise typer.Exit(1)

    # Check if input.json exists
    input_path = Path.joinpath(machine_path, "input.json")
    if not input_path.exists():
        typer.secho(f"❌ input.json not found in '{machine_name}'. Cannot fetch logs.", fg=typer.colors.RED)
        typer.secho("")
        raise typer.Exit(1)

    # Read input.json to get workflow_name
    try:
        with input_path.open("r") as f:
            input_data = json.load(f)
    except json.JSONDecodeError:
        typer.secho(f"❌ input.json in '{machine_name}' is not a valid JSON.", fg=typer.colors.RED)
        typer.secho("")
        raise typer.Exit(1)

    workflow_name = input_data.get("workflow_name")
    if not workflow_name:
        typer.secho(f"❌ 'workflow_name' not found in input.json of '{machine_name}'.", fg=typer.colors.RED)
        typer.secho("")
        raise typer.Exit(1)

    # Determine the workflow folder and output log file
    machine_logfile_path = get_latest_log(machine_name, workflow_name)

    # If the log file is found, read and display it
    if not machine_logfile_path:
        typer.secho(f"❌ Log file not found for machine '{machine_name}'.", fg=typer.colors.RED)
        typer.secho("")
        raise typer.Exit(1)
    else:
        try:
            typer.secho("─────────────────────────────────────────────────────────", fg=typer.colors.CYAN)
            typer.secho(f"📄 Logs for machine '{machine_name}':", fg=typer.colors.BLUE)
            typer.secho("─────────────────────────────────────────────────────────", fg=typer.colors.CYAN)
            with open(machine_logfile_path, "r") as f:
                for line in f:
                    # Optionally highlight certain words
                    if "ERROR" in line:
                        typer.secho(line.rstrip(), fg=typer.colors.RED)
                    elif "DEBUG" in line:
                        typer.secho(line.rstrip(), fg=typer.colors.BLUE)
                    elif "INFO" in line:
                        typer.secho(line.rstrip(), fg=typer.colors.GREEN)
                    else:
                        typer.echo(line.rstrip())
            typer.secho("")
        except json.JSONDecodeError:
            typer.secho(f"❌ Log file '{machine_logfile_path}' is not a valid JSON.", fg=typer.colors.RED)
            typer.secho("")
            raise typer.Exit(1)

def get_latest_log(machine_name: str, base_dir=".") -> str:
    latest_file = None
    latest_mtime = 0

    workflow_path = Path(base_dir).resolve()
    if not workflow_path.exists():
        typer.secho(f"❌ '{base_dir}' Workflow Folder not found.", fg=typer.colors.RED)
        typer.secho("")
        raise typer.Exit(1)

    # Search for all folders in the base directory
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith(f"{machine_name}.log"):
                file_path = os.path.join(root, file)
                mtime = os.path.getmtime(file_path)
                if mtime > latest_mtime:
                    latest_mtime = mtime
                    latest_file = file_path

    return latest_file