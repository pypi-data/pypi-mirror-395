import typer
import yaml
import json
from pathlib import Path

app = typer.Typer(help="""
    Add a machine to a DAG-based workflow.yaml file.

    Example:
        quantum add machine MyMachine -p Parent1 -p Parent2 --workflow my-workflow
    """)

@app.command("machine")
def add(
    machine_name: str = typer.Argument(..., help="Machine name to add to workflow"),
    parent: list[str] = typer.Option([], "--parent", "-p", help="Parent machine(s) this depends on"),
    workflow: str = typer.Option(..., "--workflow", "-w", help="Workflow name (without .yaml)"),
):
    """
    Add a machine to a DAG-based workflow.yaml file.

    Example:
        quantum add machine MyMachine -p Parent1 -p Parent2 --workflow my-workflow
    """
    typer.secho("")
    workflow_file = Path.joinpath(Path(workflow),"workflow.yaml")
    machine_name = machine_name.strip().replace(" ", "").lower()
    if not workflow_file.exists():
        typer.secho(f"❌ Workflow file '{workflow_file}' does not exist.", fg=typer.colors.RED)
        typer.secho("")
        raise typer.Exit(1)
    
    # ✅ Check for Machine Folder is exist
    machine_path = Path(machine_name).resolve()
    if not machine_path.exists():
        typer.secho(f"❌ '{machine_name}' Machine Folder not found.", fg=typer.colors.RED)
        typer.secho("")
        raise typer.Exit(1)

    try:
        with workflow_file.open("r") as f:
            data = yaml.safe_load(f) or {}
    except yaml.YAMLError as e:
        typer.secho(f"❌ Error parsing YAML: {e}", fg=typer.colors.RED)
        typer.secho("")
        raise typer.Exit(1)

    # Ensure structure is correct
    if not isinstance(data.get("machines"), dict):
        data["machines"] = {}

    machines = data["machines"]

    # Update input.json of the machine with depends_machine
    input_path = Path.joinpath(machine_path, "input.json")
    if input_path.exists():
        try:
            with input_path.open("r") as f:
                input_data = json.load(f)
        except json.JSONDecodeError:
            typer.secho(f"❌ input.json in '{machine_name}' is not a valid JSON.", fg=typer.colors.RED)
            typer.secho("")
            raise typer.Exit(1)

        # Preserve and extend depends_machine
        existing_deps = input_data.get("depends_machine", [])
        if not isinstance(existing_deps, list):
            existing_deps = []
    else:
        typer.secho(f"⚠️ input.json not found in '{machine_name}'. Skipped updating depends_machine.", fg=typer.colors.YELLOW)
        typer.secho("")
        raise typer.Exit(1)

    if not parent:
        # Root machine (no parents)
        if machine_name not in machines:
            machines[machine_name] = []

            # Add new parents if not already present
            input_data["workflow_name"] = f"{workflow}"

            with input_path.open("w") as f:
                json.dump(input_data, f, indent=4)

            typer.secho(f"🔄 Updated '{machine_name}/input.json' with workfolw name:", fg=typer.colors.BLUE)

            typer.secho(f"✅ Added root machine '{machine_name}' to workflow '{workflow}'", fg=typer.colors.GREEN)
        else:
            typer.secho(f"⚠️ Machine '{machine_name}' already exists in workflow.", fg=typer.colors.YELLOW)
    else:
        for p in parent:

            # ✅ Check for Machine Folder is exist
            p_machine_path = Path(p).resolve()
            if not p_machine_path.exists():
                typer.secho(f"❌ '{p}' Machine Folder not found.", fg=typer.colors.RED)
            else:
                if machine_name not in machines:
                    machines[machine_name] = []
                if p not in machines[machine_name]:
                    machines[machine_name].append(p)

                    # Add new parents if not already present
                    updated_deps = list(set(existing_deps + parent))
                    input_data["depends_machine"] = updated_deps
                    input_data["workflow_name"] = f"{workflow}"

                    with input_path.open("w") as f:
                        json.dump(input_data, f, indent=4)

                    typer.secho(f"🔄 Updated '{machine_name}/input.json' with depends_machine: {updated_deps}", fg=typer.colors.BLUE)

                    # 3️⃣ Save the updated workflow.yaml
                    with workflow_file.open("w") as f:
                        yaml.dump(data, f, sort_keys=False)
                        
                    typer.secho(f"✅ Added machine '{machine_name}' under parent '{p}'", fg=typer.colors.GREEN)
                else:
                    typer.secho(f"⚠️ Machine '{machine_name}' already exists under parent '{p}'", fg=typer.colors.YELLOW)

        # Ensure the child node exists too
        machines.setdefault(machine_name, [])

    # Save changes
    with workflow_file.open("w") as f:
        yaml.dump(data, f, sort_keys=False)

    typer.secho("")
