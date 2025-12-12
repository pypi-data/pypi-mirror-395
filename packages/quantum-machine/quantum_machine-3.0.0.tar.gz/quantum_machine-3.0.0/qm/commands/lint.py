import typer
import subprocess
from pathlib import Path
import shutil

app = typer.Typer(help="""
Run linting for a Quantum Machine.

This command checks code formatting and style issues using tools like flake8 or pylint.

Example:
    quantum lint machine HelloWorld
    quantum lint machine HelloWorld --tool pylint       #Using a Custom Linting Tool (e.g., pylint):
                  
""")

@app.command()
def machine(path: str, tool: str = "flake8"):
    """
    Run linting for a Quantum Machine.

    This command checks code formatting and style issues using tools like flake8 or pylint.

    Example:
        quantum lint machine HelloWorld
    """
    typer.secho("")
    project_path = Path(path.strip().replace(" ","").lower()).resolve()

    # Check if the provided path exists
    if not project_path.exists():
        typer.secho("❌ The specified path does not exist.", fg=typer.colors.RED)
        typer.secho("")
        raise typer.Exit(1)

    # Check if main.py exists in the project directory
    if not (project_path / "main.py").exists():
        typer.secho("❌ No main.py found to lint.", fg=typer.colors.RED)
        typer.secho("")
        raise typer.Exit(1)

    # Check if the linting tool is installed
    if not shutil.which(tool):
        typer.secho(f"❌ The linting tool '{tool}' is not installed. Please install it and try again.", fg=typer.colors.RED)
        typer.secho("")
        raise typer.Exit(1)

    try:
        # Run the linting tool
        subprocess.run([tool, str(project_path)], check=True)
        typer.secho("✅ Lint passed: No major issues found!", fg=typer.colors.GREEN)
    except subprocess.CalledProcessError:
        typer.secho("⚠️ Linting failed. Please fix the above issues.", fg=typer.colors.YELLOW)
    except Exception as e:
        typer.secho(f"❌ An unexpected error occurred: {e}", fg=typer.colors.RED)
        typer.secho("")
        raise typer.Exit(1)
    
    typer.secho("")
