import os
import json
import typer
import platform
from pathlib import Path

app = typer.Typer(help="""
Fetch output of a Quantum Machine.

    This command reads the output.json file of the specified machine to determine the workflow name
    and fetches the corresponding output logs from the workflow directory.

    Example:
        quantum output machine MyMachine
""")

@app.command()
def machine(machine_name: str):
    """
    Fetch output of a Quantum Machine.

    This command reads the input.json file of the specified machine to determine the workflow name
    and fetches the corresponding output logs from the workflow directory.

    Example:
        quantum output machine MyMachine
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
    workflow_folder = Path(workflow_name).resolve()

    __base_os = platform.system().lower()
    __main_folder = "/mnt/qwf-data"  # Default for Linux
    if __base_os == "darwin":  # 'Darwin' is the identifier for macOS
        home_dir = os.environ.get("HOME")  # Equivalent to `echo $HOME`
        __main_folder = f"{home_dir}/mnt/qwf-data"

    output_log_file = os.path.join(__main_folder, workflow_name, f"output_{machine_name}.json")

    machine_logfile_path = Path(output_log_file).resolve()

    # Check if the output log file exists
    if not machine_logfile_path.exists():
        typer.secho(f"❌ Log file '{machine_logfile_path}' not found for machine '{machine_name}'.", fg=typer.colors.RED)
        typer.secho("")
        raise typer.Exit(1)

    # Read and display the log file
    try:
        with machine_logfile_path.open("r") as f:
            log_data = json.load(f)
    except json.JSONDecodeError:
        typer.secho(f"❌ Log file '{machine_logfile_path}' is not a valid JSON.", fg=typer.colors.RED)
        typer.secho("")
        raise typer.Exit(1)

    typer.secho("─────────────────────────────────────────────────────────", fg=typer.colors.CYAN)
    typer.secho(f"📄 Output Logs of machine '{machine_name}':", fg=typer.colors.BLUE)
    typer.secho("─────────────────────────────────────────────────────────", fg=typer.colors.CYAN)
    typer.secho(json.dumps(log_data, indent=4), fg=typer.colors.GREEN)
    typer.secho("")