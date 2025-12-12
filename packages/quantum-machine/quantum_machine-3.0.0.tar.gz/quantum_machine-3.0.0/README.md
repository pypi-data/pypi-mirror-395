# Quantum Machine

**Quantum-Machine CLI** is a command-line interface developed by **QuantumDatalytica LLC** to help developers build, run, test, logs, and manage modular analytics components called **Quantum Machines**. These machines are the foundation of scalable, distributed data workflows within the QuantumDatalytica ecosystem. The CLI streamlines local development and ensures consistent behavior across environments.

> **Note:**  
> [`quantum-core-engine`](https://github.com/QuantumDatalytica-LLC/quantum-core-engine.git) is a public dependency and must be installed manually. Please contact the QuantumDatalytica team or refer to internal documentation for setup instructions.

---

## 🚀 Features

- 🧱 Initialize new Quantum Machines with starter templates
- 🧪 Test and lint your machine logic
- 🐳 Build Container images for machine deployment
- ▶️ Run machines locally or in containers
- 🔎 Validate `Project.json` and dependencies
- 🔁 Create Workflows and define DAG-style machine dependencies
- 📜 View logs of machine executions

---

## 📦 Installation

```bash
pip install quantum-machine
```

---

## 📖 Usage

```bash
quantum --help
```

### Available Commands

| Command           | Description                                                                 |
|------------------|-----------------------------------------------------------------------------|
| `init machine`    | Initialize a new Quantum Machine project with boilerplate files             |
| `run machine`     | Run a machine and observe its behavior locally                              |
| `build machine`   | Build a Container image for the specified machine                              |
| `test machine`    | Run unit tests defined for the machine                                      |
| `lint machine`    | Check the machine's code for linting/style issues                           |
| `validate machine`| Validate the machine's `Project.json` and required structure                |
| `init workflow`   | Initialize a new workflow YAML file with DAG structure                      |
| `add machine`     | Add a machine as a task to a workflow and define its dependencies           |
| `run workflow`    | Run a workflow DAG by executing machines in topological order               |
| `logs machine`    | View logs from the last execution of a specified machine                    |

---

## 🧪 Example Commands

### 🔧 Initialize a machine

```bash
quantum init machine HelloWorld
```

Creates:
- `HelloWorld/main.py`
- `HelloWorld/Project.json`
- `HelloWorld/requirements.txt`
- `HelloWorld/Dockerfile`
- `HelloWorld/input.json`
- `HelloWorld/output.json`


---

### ▶️ Run the machine

```bash
quantum run machine HelloWorld [--container] [--kube] [--rebuild] [--no-rebuild] 
```

---

### 🐳 Build the machine as Container Image

```bash
quantum build machine HelloWorld
```

Builds a Container image with dependencies for the machine.

---

### 🧪 Test your machine

```bash
quantum test machine HelloWorld
```

Runs the test suite defined under the machine's directory.

---

### 🎯 Lint your machine

```bash
quantum lint machine HelloWorld
```

Applies flake8 or equivalent linting tools to maintain code standards.

---

### 🛡 Validate machine structure

```bash
quantum validate machine HelloWorld\<file_name>
```

Ensures the machine has the correct `Project.json`, required fields, and structure.

### 🦮 Create a Workflow

```bash
quantum init workflow my_workflow
```

Creates a `workflow.yaml` file to define machine dependencies.

---

### ➕ Add DAG Machine to Workflow

```bash
quantum add machine 1st_Machine -w my_workflow
quantum add machine 2nd_Machine -w my_workflow
quantum add machine 3rd_Machine -p HelloWorld --workflow  my_workflow
quantum add machine 4th_Machine -parent 2nd_Machine -w my_workflow
quantum add machine 5th_Machine -p 3rd_Machine 4th_Machine -w my_workflow
```

---

### 🚀 Run a Workflow

```bash
quantum run workflow my_workflow  [--container] [--kube] [--rebuild] [--no-rebuild]
```

Executes machines in the correct DAG order as defined in `workflow.yaml`.

---

### 🚀 View machine logs

```bash
quantum logs machine HelloWord
```

Displays the logs from the most recent execution of the HelloWorld machine.

---

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## 🧠 About QuantumDatalytica LLC

**QuantumDatalytica (QDL)** is a modular data automation and analytics platform that empowers developers to build, test, logs, and publish reusable logic units called **Quantum Machines**. These machines are designed to run as part of scalable, enterprise-grade data pipelines.

As a Machine Developer, QDL gives you the tools to:
- Build data processing logic in isolated, portable units  
- Seamlessly integrate your machines into larger workflows  
- Automate complex tasks with minimal overhead  
- Ensure consistency, reusability, and performance in analytics at scale

With its focus on **flexibility**, **scalability**, and **workflow automation**, QuantumDatalytica enables organizations to transform raw data into actionable insights — faster and more efficiently than ever before.

---
