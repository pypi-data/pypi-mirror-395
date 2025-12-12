import typer
import subprocess
import shutil
from pathlib import Path

app = typer.Typer(help="""
Run tests for a Quantum Machine.

This command looks for test scripts and runs them to validate functionality.

Example:
    quantum test machine HelloWorld
""")

@app.command()
def machine(path: str):
    """
    Run tests for a Quantum Machine.

    This command looks for test scripts and runs them to validate functionality.

    Example:
        quantum test machine HelloWorld
    """
    typer.secho("")
    path = path.strip().replace(" ","").lower()
    project_path = Path(path).resolve()
    tests_path = project_path / "tests"

    if not tests_path.exists():
        typer.secho("❌ No 'tests' directory found.", fg=typer.colors.RED)
        typer.secho("")
        raise typer.Exit()

    # Determine the Python executable to use
    python_executable = shutil.which("python3") or shutil.which("python")
    if not python_executable:
        typer.secho("❌ Neither 'python3' nor 'python' is available in the environment.", fg=typer.colors.RED)
        typer.secho("")
        raise typer.Exit()

    try:
        # Run the tests and stream output line by line
        process = subprocess.Popen(
            [python_executable, "-m", "unittest", "discover", "-s", str(tests_path)],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True  # Ensures output is returned as a string
        )

        # Stream logs line by line
        for line in process.stdout:
            typer.echo(line, end='')  # Display each line in real-time

        process.wait()  # Wait for the process to complete

        # Check the return code to determine success or failure
        if process.returncode == 0:
            typer.secho("✅ All tests passed!", fg=typer.colors.GREEN)
        else:
            typer.secho("❌ Tests failed.", fg=typer.colors.RED)

    except FileNotFoundError:
        typer.secho("❌ Python executable not found. Ensure Python is installed.", fg=typer.colors.RED)
    except Exception as e:
        typer.secho(f"❌ An unexpected error occurred: {e}", fg=typer.colors.RED)

    typer.secho("")
