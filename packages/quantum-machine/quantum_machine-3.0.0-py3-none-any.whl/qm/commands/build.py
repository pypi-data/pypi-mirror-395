import typer
import subprocess
from pathlib import Path

app = typer.Typer(help="""
Build a Quantum Machine image using build command.

This command creates a image using the machine's Container file and dependencies.

Example:
    quantum build machine HelloWorld
""")

@app.command()
def machine(path: str, tag: str = "quantum-machine:latest"):
    """
    Build a Quantum Machine image using build command.

    This command creates a image using the machine's Container file and dependencies.

    Example:
        quantum build machine HelloWorld
    """
    typer.secho("")
    path = path.strip().replace(" ","").lower()
    tag = tag.strip().replace(" ","").lower()

    machine_name, version = parse_machine_ref(tag)
    tag = f"{machine_name}:{version}"
    
    tag = tag.lower()   # <-- enforce lowercase always
    
    project_path = Path(path).resolve()

    if not (project_path / "Dockerfile").exists():
        typer.secho("❌ Container file not found!", fg=typer.colors.RED)
        typer.secho("")
        raise typer.Exit(1)

    try:
        subprocess.run(["docker", "build", "-t", tag, str(project_path)], check=True)
        typer.secho(f"✅ Container image '{tag}' built successfully!", fg=typer.colors.GREEN)
    except subprocess.CalledProcessError:
        typer.secho("❌ Failed to build Container image.", fg=typer.colors.RED)

    typer.secho("")

def parse_machine_ref(ref: str) -> tuple[str, str]:
    if ":" in ref:
        name, version = ref.split(":", 1)
        version = version or "latest"
    else:
        name, version = ref, "latest"
    return name, version
    