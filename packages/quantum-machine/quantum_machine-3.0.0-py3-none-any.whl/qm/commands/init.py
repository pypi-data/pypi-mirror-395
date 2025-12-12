import typer
import json
import yaml
from pathlib import Path

app = typer.Typer(help="""
Initialize a new Quantum Machine with a predefined folder structure.

This command creates the following files:
- main.py
- project.json
- requirements.txt
- Container file
- input.json
- output.json
- tests/test_main.py
- .gitignore

Example:
    quantum init machine HelloWorld
""")


def print_qdl_header():
    typer.secho("")
    typer.secho("┌───────────────────────────────────────────────┐", fg=typer.colors.CYAN)
    typer.secho("│                                               │", fg=typer.colors.CYAN)
    typer.secho("│    🚀  Q U A N T U M   M A C H I N E   ⚙️      │", fg=typer.colors.CYAN, bold=True)
    typer.secho("│                                               │", fg=typer.colors.CYAN)
    typer.secho("└───────────────────────────────────────────────┘", fg=typer.colors.CYAN)
    typer.secho("")

def print_workflow_header():
    typer.secho("")
    typer.secho("┌───────────────────────────────────────────────┐", fg=typer.colors.BRIGHT_MAGENTA)
    typer.secho("│                                               │", fg=typer.colors.BRIGHT_MAGENTA)
    typer.secho("│  🚀   Q U A N T U M   W O R K F L O W   🔁    │", fg=typer.colors.BRIGHT_MAGENTA, bold=True)
    typer.secho("│                                               │", fg=typer.colors.BRIGHT_MAGENTA)
    typer.secho("└───────────────────────────────────────────────┘", fg=typer.colors.BRIGHT_MAGENTA)
    typer.secho("")

@app.command("machine")
def machine(name: str):
    """
    Initialize a new Quantum Machine with the given name.

    Example:
        quantum init machine HelloWorld
    """
    print_qdl_header()
    name = name.strip().replace(" ", "").lower()
    machine_path = Path(name)
    if machine_path.exists():
        typer.secho(f"❌ A machine named '{name}' already exists at {machine_path.resolve()}", fg=typer.colors.RED)
        typer.secho("")
        raise typer.Exit(1)
    else:
        machine_path.mkdir(parents=True, exist_ok=True)

    (Path.joinpath(machine_path, "main.py")).write_text(
        "from quantum.CoreEngine import CoreEngine\n\n"
        "class MyMachine(CoreEngine):\n\n"
        "    input_data = {}\n"
        "    dependent_machine_data = {}\n\n"
        "    def receiving(self, input_data, dependent_machine_data, callback):\n"
        "        \"\"\"Receiving\n"
        "        :param input_data: Configure parameter values\n"
        "        :param dependent_machine_data: Dependant/Previous machine data values\n"
        "        :return: callback method to pass data and error into next step\n"
        "        \"\"\"\n"
        "        data = {}\n"
        "        error_list = []\n"
        "        try:\n"
        "            # Review Final data and Error list\n"
        "            data = self.get_final_data()\n"
        "            error_list = self.get_error_list()\n\n"
        "            self.input_data = input_data\n"
        "            self.dependent_machine_data = dependent_machine_data\n\n\n"
        "        except Exception as e:\n"
        "            err_msg = f\"Error : {str(e)}\"\n"
        "            error_list.append(err_msg)\n"
        "        finally:\n"
        "            callback(data, error_list)\n\n"
        "    def pre_processing(self, callback):\n"
        "        \"\"\"Pre-Processing\n"
        "        :return: callback method to pass data and error into next step\n"
        "        \"\"\"\n"
        "        data = {}\n"
        "        error_list = []\n"
        "        try:\n"
        "            # Updated Final data and Error list\n"
        "            data = self.get_final_data()\n"
        "            error_list = self.get_error_list()\n\n\n"
        "        except Exception as e:\n"
        "            err_msg = f\"Error : {str(e)}\"\n"
        "            error_list.append(err_msg)\n"
        "        finally:\n"
        "            callback(data, error_list)\n\n"
        "    def processing(self, callback):\n"
        "        \"\"\"Processing\n"
        "        :return: callback method to pass data and error into next step\n"
        "        \"\"\"\n"
        "        data = {}\n"
        "        error_list = []\n"
        "        try:\n"
        "            # Updated Final data and Error list\n"
        "            data = self.get_final_data()\n"
        "            error_list = self.get_error_list()\n\n\n"
        "        except Exception as e:\n"
        "            err_msg = f\"Error : {str(e)}\"\n"
        "            error_list.append(err_msg)\n"
        "        finally:\n"
        "            callback(data, error_list)\n\n"
        "    def post_processing(self, callback):\n"
        "        \"\"\"Post-Processing\n"
        "        :return: callback method to pass data and error into next step\n"
        "        \"\"\"\n"
        "        data = {}\n"
        "        error_list = []\n"
        "        try:\n"
        "            # Updated Final data and Error list\n"
        "            data = self.get_final_data()\n"
        "            error_list = self.get_error_list()\n\n\n"
        "        except Exception as e:\n"
        "            err_msg = f\"Error : {str(e)}\"\n"
        "            error_list.append(err_msg)\n"
        "        finally:\n"
        "            callback(data, error_list)\n\n"
        "    def packaging_shipping(self, callback):\n"
        "        \"\"\"Packaging & Shipping\n"
        "        :return: callback method to pass data and error into next step, This is final data to use into next machine\n"
        "        \"\"\"\n"
        "        data = {}\n"
        "        error_list = []\n"
        "        try:\n"
        "            # Updated Final data and Error list\n"
        "            data = self.get_final_data()\n"
        "            error_list = self.get_error_list()\n\n\n"
        "        except Exception as e:\n"
        "            err_msg = f\"Error : {str(e)}\"\n"
        "            error_list.append(err_msg)\n"
        "        finally:\n"
        "            callback(data, error_list)\n\n"
        "if __name__ == '__main__':\n"
        "    # Create a machine instance and start the process\n"
        "    machine = MyMachine()\n"
        "    machine.start()\n"
    )
    # Green "create" + clickable file path (hyperlink for VS Code and modern terminals)
    file_path = Path.joinpath(machine_path, "main.py").resolve()
    relative_path = str(file_path.relative_to(Path.cwd()))
    link = f"\033]8;;file://{file_path}\033\\{relative_path}\033]8;;\033\\"
    typer.secho(f"  create ", fg=typer.colors.GREEN, nl=False)
    typer.echo(link)

    (Path.joinpath(machine_path, "Project.json")).write_text(
        '{\n  "name": "' + name + '",\n'
        '  "version": "1.0.0",\n'
        '  "title": "' + name + '",\n'
        '  "author": "",\n'
        '  "license": "",\n'
        '  "short_description": "",\n'
        '  "long_description": "",\n'
        '  "specification": {\n'
        '    "input": "",\n'
        '    "output": ""\n'
        '  },\n'
        '  "infrastructure": {\n'
        '    "os": "",\n'
        '    "storage": "",\n'
        '    "memory": "",\n'
        '    "cpu": "",\n'
        '    "cloud": ""\n'
        '  },\n'
        '  "parameters": [],\n'
        '  "faq": [\n'
        '    {\n'
        '      "question": "",\n'
        '      "answer": ""\n'
        '    },\n'
        '    {\n'
        '      "question": "",\n'
        '      "answer": ""\n'
        '    },\n'
        '    {\n'
        '      "question": "",\n'
        '      "answer": ""\n'
        '    }\n'
        '  ]\n'
        '}'
    )
    file_path = Path.joinpath(machine_path, "Project.json").resolve()
    relative_path = str(file_path.relative_to(Path.cwd()))
    link = f"\033]8;;file://{file_path}\033\\{relative_path}\033]8;;\033\\"
    typer.secho(f"  create ", fg=typer.colors.GREEN, nl=False)
    typer.echo(link)


    (Path.joinpath(machine_path, "requirements.txt")).write_text(
        "git+https://github.com/QuantumDatalytica-LLC/quantum-core-engine.git@main"
    )
    file_path = Path.joinpath(machine_path, "requirements.txt").resolve()
    relative_path = str(file_path.relative_to(Path.cwd()))
    link = f"\033]8;;file://{file_path}\033\\{relative_path}\033]8;;\033\\"
    typer.secho(f"  create ", fg=typer.colors.GREEN, nl=False)
    typer.echo(link)


    (Path.joinpath(machine_path, "Dockerfile")).write_text(
        "FROM python:3.10-buster\n\n"
        "# Creating Application Source Code Directory\n"
        "# RUN mkdir -p /usr/src/app\n\n"
        "# Setting Home Directory for containers\n"
        "WORKDIR /usr/src/app/\n\n"
        "# Installing python dependencies\n"
        "COPY requirements.txt .\n"
        "RUN pip install --no-cache-dir -r requirements.txt\n\n"
        "# Copying src code to Container\n"
        "COPY . .\n\n"
        "# Execute code under Container\n"
        "CMD [\"python\", \"main.py\"]\n"
    )
    file_path = Path.joinpath(machine_path, "Dockerfile").resolve()
    relative_path = str(file_path.relative_to(Path.cwd()))
    link = f"\033]8;;file://{file_path}\033\\{relative_path}\033]8;;\033\\"
    typer.secho(f"  create ", fg=typer.colors.GREEN, nl=False)
    typer.echo(link)

    
    (Path.joinpath(machine_path, "input.json")).write_text(
        "{\n"
        "   \"machine_name\": \"" + name + "\",\n"
        "   \"workflow_name\": \"TestWorkFlow\",\n"
        "   \"input_data\": {\n"
        "   },\n"
        "   \"output\": \"" + name + ".json\",\n"
        "   \"depends_machine\": []\n"
        "}"
    )
    file_path = Path.joinpath(machine_path, "input.json").resolve()
    relative_path = str(file_path.relative_to(Path.cwd()))
    link = f"\033]8;;file://{file_path}\033\\{relative_path}\033]8;;\033\\"
    typer.secho(f"  create ", fg=typer.colors.GREEN, nl=False)
    typer.echo(link)


    (Path.joinpath(machine_path, "output.json")).write_text(
        "{\n"
        "}"
    )
    file_path = Path.joinpath(machine_path, "output.json").resolve()
    relative_path = str(file_path.relative_to(Path.cwd()))
    link = f"\033]8;;file://{file_path}\033\\{relative_path}\033]8;;\033\\"
    typer.secho(f"  create ", fg=typer.colors.GREEN, nl=False)
    typer.echo(link)


    (Path.joinpath(machine_path, ".gitignore")).write_text(
        "tests/\n"
    )
    file_path = Path.joinpath(machine_path, ".gitignore").resolve()
    relative_path = str(file_path.relative_to(Path.cwd()))
    link = f"\033]8;;file://{file_path}\033\\{relative_path}\033]8;;\033\\"
    typer.secho(f"  create ", fg=typer.colors.GREEN, nl=False)
    typer.echo(link)


    tests_dir = (Path.joinpath(machine_path, "tests"))
    tests_dir.mkdir(exist_ok=True)
    (Path.joinpath(tests_dir, "test_main.py")).write_text(
        "import unittest\n"
        "from main import MyMachine\n\n"
        "class TestMyMachine(unittest.TestCase):\n"
        "    def test_run(self):\n"
        "        machine = MyMachine()\n"
        "        #machine.set_input('input_data', 'quantum')\n"
        "        machine.start()\n"
        "        #self.assertEqual(machine.get_output('result'), 'QUANTUM')\n\n"
        "if __name__ == '__main__':\n"
        "    unittest.main()\n"
    )
    file_path = Path.joinpath(tests_dir, "test_main.py").resolve()
    relative_path = str(file_path.relative_to(Path.cwd()))
    link = f"\033]8;;file://{file_path}\033\\{relative_path}\033]8;;\033\\"
    typer.secho(f"  create ", fg=typer.colors.GREEN, nl=False)
    typer.echo(link)
    typer.echo("")

    typer.secho(f"✅ Quantum Machine '{name}' scaffolded!", fg=typer.colors.GREEN)
    typer.echo("")
    typer.echo("")


@app.command("workflow")
def workflow(name: str):
    """
    Initialize a new Quantum Workflow with the given name.
    
    Example:
        quantum init workflow testworkflow
    """
    print_workflow_header()
    name = name.strip().replace(" ", "").lower()
    workflow_path = Path(name)
    if workflow_path.exists():
        typer.secho(f"❌ A workflow named '{name}' already exists as {workflow_path.resolve()}", fg=typer.colors.RED)
        typer.secho("")
        raise typer.Exit(1)
    else:
        workflow_path.mkdir(parents=True, exist_ok=True)

    (Path.joinpath(workflow_path, "workflow.yaml")).write_text(
        "# DAG format: for each machine in workflow will run top to bottom\n"
        "name: "+ name +"\n"
        "machines:\n"
    )
    file_path = Path.joinpath(workflow_path, "workflow.yaml").resolve()
    relative_path = str(file_path.relative_to(Path.cwd()))
    link = f"\033]8;;file://{file_path}\033\\{relative_path}\033]8;;\033\\"
    typer.secho(f"  create ", fg=typer.colors.GREEN, nl=False)
    typer.echo(link)
    typer.echo("")

    typer.secho(f"✅ Quantum Workflow '{name}' scaffolded!", fg=typer.colors.GREEN)
    typer.echo("")
    typer.echo("")