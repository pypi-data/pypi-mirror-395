import os
import typer
import subprocess
from pathlib import Path
from collections import defaultdict, deque
from datetime import datetime, timezone
from typing import Optional
import json
import shutil
import yaml
import time
import textwrap

app = typer.Typer(help="""
    Run a Quantum Machine or Workflow locally using Python.

    Example:
        quantum run machine HelloWorld --container --kube
        quantum run workflow MyWorkflow --container --kube
    """
)

REQUIRED_KEYS = {"machine_name", "input_data", "output", "depends_machine", }

@app.command()
def machine(machine_name: str,
        container: bool = typer.Option(
            False,
            "--container",
            "-container",
            help="Run the Quantum Machine using its Container image.",
        ),
        kube: bool = typer.Option(
            False,
            "--kube",
            "-kube",
            help="Run the Quantum Machine as a Kubernetes Job (e.g. Minikube).",
        ),
        namespace: str = typer.Option(
            "default",
            "--namespace",
            "-n",
            help="Kubernetes namespace to use when running with -kube.",
        ),
        rebuild: Optional[bool] = typer.Option(
            None,
            "--rebuild/--no-rebuild",
            help=(
                "Auto-answer the image rebuild question. "
                "--rebuild = always rebuild, --no-rebuild = never rebuild. "
                "Default (no flag) = ask interactively."
            ),
        ),
    ):
    """
    Run a Quantum Machine locally using Python.

    Example:
        quantum run machine HelloWorld
    """
    typer.secho("")
    machine_name = machine_name.strip().replace(" ","").lower()
    # 🔐 sanity: container & kube cannot be used together
    if container and kube:
        typer.secho("❌ You cannot use both -container and -kube at the same time.", fg=typer.colors.RED)
        raise typer.Exit(1)
    
    machine_name, version = parse_machine_ref(machine_name)
    image_name = f"{machine_name.lower()}:{version}"
    auto_rebuild = rebuild  # True / False / None

    # ✅ Check for Machine Folder
    machine_path = Path(machine_name).resolve()
    if not machine_path.exists():
        typer.secho(f"❌ '{machine_name}' Machine Folder not found.", fg=typer.colors.RED)
        raise typer.Exit(1)

    # ✅ Load input.json
    input_json_path = machine_path / "input.json"
    if not input_json_path.exists():
        typer.secho("❌ input.json file not found in the machine directory.", fg=typer.colors.RED)
        typer.secho("")
        raise typer.Exit(1)

    try:
        with open(input_json_path) as f:
            input_data = json.load(f)
    except json.JSONDecodeError:
        typer.secho("❌ input.json is not valid JSON.", fg=typer.colors.RED)
        typer.secho("")
        raise typer.Exit(1)

    # ✅ Validate required keys
    missing_keys = REQUIRED_KEYS - input_data.keys()
    if missing_keys:
        typer.secho(f"❌ input.json is missing required keys: {', '.join(missing_keys)}", fg=typer.colors.RED)
        typer.secho("")
        raise typer.Exit(1)
    
    if "mode" in input_data:
        input_data["mode"] = "test"
    else:
        input_data["mode"] = "test"

    # 🧠 Common payload
    payload = json.dumps(input_data)

    workflow_name = input_data.get("workflow_name", machine_name)
    workflow_ts = datetime.now(timezone.utc).isoformat()

    # ─────────────────────────────────────────────
    # MODE 1: LOCAL PYTHON (default)
    # ─────────────────────────────────────────────
    if not container and not kube:
        local_machine_run(machine_name, machine_path, payload, workflow_name, workflow_ts)

    # ─────────────────────────────────────────────
    # MODE 2: CONTAINER
    # ─────────────────────────────────────────────
    if container:
        container_machine_run(machine_name, image_name, machine_path, payload, workflow_name, workflow_ts, auto_rebuild=auto_rebuild)

    # ─────────────────────────────────────────────
    # MODE 3: KUBERNETES / MINIKUBE
    # ─────────────────────────────────────────────
    if kube:
        kube_machine_run(machine_name, image_name, machine_path, payload, namespace, workflow_name, workflow_ts, auto_rebuild=auto_rebuild)

def local_machine_run(machine_name: str, machine_path: Path, payload: str, workflow_name: str, workflow_ts: str, success: set = None, failed: set = None):
    # Only local mode actually needs CoreEngine installed in the host env
    try:
        from quantum.CoreEngine import CoreEngine  # noqa: F401
    except ImportError:
        typer.secho(
            "❌ Missing dependency: 'quantum-core-engine' is required for local runs. "
            "Install it into this environment.",
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)

    main_script = machine_path / "main.py"
    if not main_script.exists():
        typer.secho("❌ main.py not found in machine directory.", fg=typer.colors.RED)
        typer.secho("")
        raise typer.Exit(1)

    python_executable = shutil.which("python") or shutil.which("python3")
    if not python_executable:
        typer.secho("❌ Neither 'python3' nor 'python' is available in the environment.", fg=typer.colors.RED)
        typer.secho("")
        raise typer.Exit(1)

    typer.echo(f"🚀 Starting Quantum Machine locally: {machine_name}")

    env = os.environ.copy()
    env["WORKFLOW_NAME"] = workflow_name
    env["WORKFLOW_NAME_TIMESTAMP"] = workflow_ts

    command = [
        python_executable,
        str(main_script),
        payload,  # QCE will read this from sys.argv[1]
    ]

    typer.echo(f"Running machine '{machine_name}' with env='dev'")
    process = subprocess.Popen(
        command, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.STDOUT, 
        text=True,
        env=env
    )

    for line in process.stdout:
        print(line, end="")

    process.wait()

    if process.returncode == 0:
        typer.echo("✅ Machine executed successfully")
        if success is not None:
            success.add(machine_name)   
    else:
        typer.echo("❌ Machine execution failed", err=True)
        if failed is not None:
            failed.add(machine_name)
    typer.secho("")

def container_machine_run(machine_name: str, image_name: str, machine_path: Path, payload: str, workflow_name: str, workflow_ts: str, success: set = None, failed: set = None, auto_rebuild: Optional[bool] = None):

    if not shutil.which("docker"):
        typer.secho("❌ 'container' CLI not found. Please install Docker / Docker Desktop.", fg=typer.colors.RED)
        raise typer.Exit(1)

    ensure_machine_image(image_name, machine_path, auto_rebuild)

    typer.echo(f"🐳 Running Quantum Machine '{machine_name}' via Container image '{image_name}'")

    # QCE will read this from ENV_SCRIPT_ARGS
    env = os.environ.copy()
    env["ENV_SCRIPT_ARGS"] = payload

    host_qwf_dir = os.path.expanduser("~/qwf-data")  # or read from config/env
    os.makedirs(host_qwf_dir, exist_ok=True)

    command = [
        "docker",
        "run",
        "--rm",
        "-e", f"ENV_SCRIPT_ARGS={payload}",
        "-e", f"WORKFLOW_NAME={workflow_name}",
        "-e", f"WORKFLOW_NAME_TIMESTAMP={workflow_ts}",
        "-v", f"{host_qwf_dir}:/mnt/qwf-data",
        image_name,
    ]

    typer.echo(f"Passing ENV_SCRIPT_ARGS={payload}")
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=env)

    for line in process.stdout:
        print(line, end="")

    process.wait()

    if process.returncode == 0:
        typer.echo("✅ Machine executed successfully")
        if success is not None:
            success.add(machine_name)   
    else:
        typer.echo("❌ Machine execution failed", err=True)
        if failed is not None:
            failed.add(machine_name)

def kube_machine_run(machine_name: str, image_name: str, machine_path: Path, payload: str, namespace: str, workflow_name: str, workflow_ts: str, success: set = None, failed: set = None, auto_rebuild: Optional[bool] = None):
    
    if not shutil.which("kubectl"):
            typer.secho("❌ 'kubectl' CLI not found. Please install kubectl and configure your cluster (e.g. Minikube).",
                        fg=typer.colors.RED)
            raise typer.Exit(1)
    
    ensure_machine_image(image_name, machine_path, auto_rebuild)
    ensure_quantum_pv_pvc(namespace)

    typer.echo(f"☸️  Running Quantum Machine '{machine_name}' as Kubernetes Job using image '{image_name}'")

    job_name = f"{machine_name.lower()}-run"

    job_manifest = {
        "apiVersion": "batch/v1",
        "kind": "Job",
        "metadata": {
            "name": job_name,
            "namespace": namespace,
        },
        "spec": {
            # optional but good to have so failed Jobs don't retry forever
            "backoffLimit": 0,
            "template": {
                "metadata": {
                    "name": job_name,
                },
                "spec": {
                    "restartPolicy": "Never",
                    # keep your security context (make sure image user = 1000)
                    "securityContext": {
                        "runAsUser": 0,
                        "runAsGroup": 0,
                    },
                    "containers": [
                        {
                            "name": machine_name,
                            "image": image_name,
                            "imagePullPolicy": "IfNotPresent",
                            "env": [
                                {
                                    "name": "ENV_SCRIPT_ARGS",
                                    "value": payload,
                                },
                                {
                                    "name": "WORKFLOW_NAME",
                                    "value": workflow_name,
                                },
                                {
                                    "name": "WORKFLOW_NAME_TIMESTAMP",
                                    "value": workflow_ts,
                                },
                            ],
                            "volumeMounts": [
                                {
                                    "name": "qwf-data",
                                    "mountPath": "/mnt/qwf-data",
                                },
                            ],
                        }
                    ],
                    "volumes": [
                        {
                            "name": "qwf-data",
                            "persistentVolumeClaim": {
                                "claimName": "quantum-pvc",   # 👈 PVC instead of hostPath
                            },
                        }
                    ],
                },
            },
        },
    }


    yaml_str = yaml.safe_dump(job_manifest)

    # Clean up any previous Job with same name
    subprocess.run(
        [
            "kubectl", "delete", "job", job_name,
            "-n", namespace,
            "--ignore-not-found=true",
        ],
        check=False,
    )

    # Apply the Job
    apply_proc = subprocess.run(
        ["kubectl", "apply", "-f", "-"],
        input=yaml_str.encode("utf-8"),
        check=False,
    )
    if apply_proc.returncode != 0:
        typer.secho("❌ Failed to apply Kubernetes Job manifest.", fg=typer.colors.RED)
        raise typer.Exit(1)

    typer.echo(f"📦 Job '{job_name}' created in namespace '{namespace}'")

    # Wait until the pod for this Job is ready (so logs exist)
    subprocess.run(
        [
            "kubectl", "wait",
            "--for=condition=Ready",
            "pod",
            "-l", f"job-name={job_name}",
            "-n", namespace,
            "--timeout=120s",
        ],
        check=False,
    )

    typer.echo("📜 Streaming logs (live):\n")
    subprocess.run(
        [
            "kubectl", "logs",
            "-l", f"job-name={job_name}",
            "-n", namespace,
            "--tail=100",
            "-f",
        ],
        check=False,
    )

    exit_code = wait_for_job_completion(job_name, namespace)

    if exit_code == 0:
        typer.secho("✅ Machine executed successfully", fg=typer.colors.GREEN)
        if success is not None:
            success.add(machine_name)   
    else:
        typer.secho(f"❌ Machine execution failed with exit code {exit_code}", fg=typer.colors.RED)
        if failed is not None:
            failed.add(machine_name)

    typer.secho("") 

def ensure_machine_image(image: str, machine_name: Path, auto_rebuild: Optional[bool]) -> None:
    """
    auto_rebuild:
        None  -> ask user (interactive)
        True  -> always rebuild (auto 'y')
        False -> never rebuild (auto 'n')
    """
    if container_image_exists(image):
        if auto_rebuild is None:
            # interactive mode
            rebuild = typer.confirm(
                f"✅ Found Quantum Machine image '{image}'. Do you want to rebuild it?",
                default=False,
            )
        else:
            # non-interactive mode, respect the flag
            rebuild = auto_rebuild

        if rebuild:
            typer.echo(f"🔨 Rebuilding image '{image}' for machine '{machine_name}'")
            build_machine_image(image, machine_name)
        else:
            typer.echo(f"🐳 Using existing image '{image}'")
    else:
        typer.echo(f"🔨 Image '{image}' not found. Building...")
        build_machine_image(image, machine_name)

def wait_for_job_completion(job_name: str, namespace: str = "default",
                            timeout_seconds: int = 600, poll_interval: int = 2) -> int:
    """
    Polls the Job status until it succeeds or fails.

    Returns:
        0 -> Job succeeded
        1 -> Job failed or timed out or couldn't fetch status
    """
    start = time.time()

    while True:
        result = subprocess.run(
            [
                "kubectl", "get", "job", job_name,
                "-n", namespace,
                "-o", "jsonpath={.status.succeeded} {.status.failed}",
            ],
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode != 0:
            typer.echo(
                f"⚠️ Failed to get job status for '{job_name}': {result.stderr.strip()}",
                err=True,
            )
            return 1

        out = (result.stdout or "").strip()
        parts = out.split()
        succeeded = int(parts[0]) if len(parts) > 0 and parts[0] else 0
        failed = int(parts[1]) if len(parts) > 1 and parts[1] else 0

        # ✅ Job completed successfully
        if succeeded >= 1 and failed == 0:
            return 0

        # ❌ Job failed
        if failed >= 1:
            return 1

        # ⏱️ Timeout
        if time.time() - start > timeout_seconds:
            typer.echo(
                f"⚠️ Timeout waiting for job '{job_name}' completion after {timeout_seconds}s",
                err=True,
            )
            return 1

        time.sleep(poll_interval)


def parse_machine_ref(ref: str) -> tuple[str, str]:
    if ":" in ref:
        name, version = ref.split(":", 1)
        version = version or "latest"
    else:
        name, version = ref, "latest"
    return name, version

def container_image_exists(image_name: str) -> bool:
    result = subprocess.run(
        ["docker", "image", "inspect", image_name],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0

def build_machine_image(tag: str, machine_root: Path) -> bool:
    
    if not (machine_root / "Dockerfile").exists():
        typer.secho("❌ Container file not found!", fg=typer.colors.RED)
        typer.secho("")
        raise typer.Exit(1)

    try:
        subprocess.run(["docker", "build", "-t", tag, str(machine_root)], check=True)
        typer.secho(f"✅ Container image '{tag}' built successfully!", fg=typer.colors.GREEN)
    except subprocess.CalledProcessError:
        typer.secho("❌ Failed to build Container image.", fg=typer.colors.RED)
        raise typer.Exit(1)

    typer.secho("")
    return True

def ensure_quantum_pv_pvc(namespace: str = "default") -> None:
    """
    Ensure quantum-pv (PV) and quantum-pvc (PVC) exist.
    Only creates them if they do not already exist.
    """
    # Check PV
    pv_exists = subprocess.run(
        ["kubectl", "get", "pv", "quantum-pv"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    ).returncode == 0

    # Check PVC
    pvc_exists = subprocess.run(
        ["kubectl", "get", "pvc", "quantum-pvc", "-n", namespace],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    ).returncode == 0

    if pv_exists and pvc_exists:
        typer.echo("📦 quantum-pv and quantum-pvc already exist. Skipping creation.")
        return

    typer.echo("📦 Creating quantum-pv / quantum-pvc (if missing)...")

    yaml_str = textwrap.dedent(
        f"""
        apiVersion: v1
        kind: PersistentVolume
        metadata:
          name: quantum-pv
        spec:
          capacity:
            storage: 5Gi
          accessModes:
            - ReadWriteMany
          storageClassName: quantum-local-sc
          persistentVolumeReclaimPolicy: Retain
          hostPath:
            path: /mnt/qwf-data
            type: DirectoryOrCreate
        ---
        apiVersion: v1
        kind: PersistentVolumeClaim
        metadata:
          name: quantum-pvc
          namespace: {namespace}
        spec:
          storageClassName: quantum-local-sc
          accessModes:
            - ReadWriteMany
          resources:
            requests:
              storage: 5Gi
        """
    ).strip()

    apply_proc = subprocess.run(
        ["kubectl", "apply", "-f", "-"],
        input=yaml_str.encode("utf-8"),
        check=False,
    )

    if apply_proc.returncode != 0:
        typer.secho("❌ Failed to create quantum-pv / quantum-pvc.", fg=typer.colors.RED)
        raise typer.Exit(1)

    typer.echo("✅ quantum-pv and quantum-pvc are ready.")


@app.command("workflow")
def run_workflow(
        workflow_name: str = typer.Argument(..., help="Name of the workflow to run (folder containing workflow.yaml)"),
        container: bool = typer.Option(
            False,
            "--container",
            "-container",
            help="Run the Quantum Machine using its Container image.",
        ),
        kube: bool = typer.Option(
            False,
            "--kube",
            "-kube",
            help="Run the Quantum Machine as a Kubernetes Job (e.g. Minikube).",
        ),
        namespace: str = typer.Option(
            "default",
            "--namespace",
            "-n",
            help="Kubernetes namespace to use when running with -kube.",
        ),
        rebuild: Optional[bool] = typer.Option(
            None,
            "--rebuild/--no-rebuild",
            help=(
                "Auto-answer the image rebuild question. "
                "--rebuild = always rebuild, --no-rebuild = never rebuild. "
                "Default (no flag) = ask interactively."
            ),
        ),
    ):
    """
    Run a Quantum Workflow locally.

    Example:
        quantum run workflow HelloWorld             # local (python)
        quantum run workflow HelloWorld --container # Container
        quantum run workflow HelloWorld --kube      # Kubernetes
    """
    typer.secho("")
    workflow_name = workflow_name.strip().replace(" ","").lower()

    workflow_file = Path.joinpath(Path(workflow_name), "workflow.yaml")

    # 🔐 sanity: container & kube cannot be used together
    if container and kube:
        typer.secho("❌ You cannot use both -container and -kube at the same time.", fg=typer.colors.RED)
        raise typer.Exit(1)
    
    if not workflow_file.exists():
        typer.secho(f"❌ Workflow file '{workflow_file}' does not exist.", fg=typer.colors.RED)
        typer.secho("")
        raise typer.Exit(1)

    if container:
        backend = "container"
    elif kube:
        backend = "kube"
    else:
        backend = "local"

    # store this somewhere you pass down to machine executor
    auto_rebuild = rebuild  # True / False / None

    with open(workflow_file, "r") as f:
        try:
            data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            typer.secho(f"❌ Error reading workflow.yaml: {e}", fg=typer.colors.RED)
            typer.secho("")
            raise typer.Exit(1)
    
    if backend == "local":
        try:
            from quantum.CoreEngine import CoreEngine
        except ImportError:
            typer.secho("❌ Missing dependency: 'quantum-core-engine' is required. Please install it.", fg=typer.colors.RED)
            typer.secho("")
            raise typer.Exit(1)
        
        python_exec = shutil.which("python") or shutil.which("python3")
        if not python_exec:
            typer.secho("❌ Python interpreter not found.", fg=typer.colors.RED)
            typer.secho("")
            raise typer.Exit(1)

    machines = data.get("machines", {})
    print(f"Machines: {machines}")
    
    # Build DAG and in-degree map
    dag = defaultdict(list)
    in_degree = defaultdict(int)
    for child, parents in machines.items():
        if isinstance(parents, list):
            for parent in parents:
                dag[parent].append(child)
                in_degree[child] += 1
        else:
            machines[child] = []

    # Queue machines with 0 in-degree (no dependencies)
    execution_queue = deque([m for m in machines if in_degree[m] == 0])
    execution_order = []

    while execution_queue:
        current = execution_queue.popleft()

        machine_path = Path(current).resolve()
        if not machine_path.exists():
            typer.secho(f"❌ '{machine}' Machine Folder not found.", fg=typer.colors.RED)
            typer.secho("")
            raise typer.Exit(1)
        
        input_json_path = machine_path / "input.json"
        if not input_json_path.exists():
            typer.secho(f"❌ input.json file not found in {machine}.", fg=typer.colors.RED)
            failed.add(machine)
            continue

        execution_order.append(current)
        for dependent in dag.get(current, []):
            in_degree[dependent] -= 1
            if in_degree[dependent] == 0:
                execution_queue.append(dependent)
    
    if len(execution_order) != len(machines):
        typer.secho("❌ Cycle detected or invalid dependencies in workflow graph.", fg=typer.colors.RED)
        typer.secho("")
        raise typer.Exit(1)

    typer.secho(f"\n📋 Execution Order: {execution_order}\n", fg=typer.colors.BLUE)

    success = set()
    failed = set()

    for machine in execution_order:
    
        machine, version = parse_machine_ref(machine)
        image_name = f"{machine.lower()}:{version}"
        machine_path = Path(machine).resolve()
        input_json_path = machine_path / "input.json"

        parents = machines[machine]
        if any(p not in success for p in parents):
            typer.secho(f"⏭️ Stopping '{machine}' because one or more parent(s) failed.", fg=typer.colors.YELLOW)
            failed.add(machine)
            typer.secho("")
            raise typer.Exit(1)

        try:
            with input_json_path.open() as f:
                input_data = json.load(f)
                input_data["workflow_name"] = workflow_name
        except json.JSONDecodeError:
            typer.secho("❌ input.json is not valid JSON.", fg=typer.colors.RED)
            failed.add(machine)
            continue

        missing_keys = REQUIRED_KEYS - input_data.keys()
        if missing_keys:
            typer.secho(f"❌ input.json is missing keys: {', '.join(missing_keys)}", fg=typer.colors.RED)
            failed.add(machine)
            continue

        if "mode" in input_data:
            input_data["mode"] = "test"
        else:
            input_data["mode"] = "test"

        # 🧠 Common payload
        payload = json.dumps(input_data)

        workflow_name = input_data.get("workflow_name", workflow_name)
        workflow_ts = datetime.now(timezone.utc).isoformat()

        # ─────────────────────────────────────────────
        # MODE 1: LOCAL PYTHON (default)
        # ─────────────────────────────────────────────
        if backend == "local":
            local_machine_run(machine, machine_path, payload, workflow_name, workflow_ts, success, failed)

        # ─────────────────────────────────────────────
        # MODE 2: CONTAINER
        # ─────────────────────────────────────────────
        if backend == "container":
            container_machine_run(machine, image_name, machine_path, payload, workflow_name, workflow_ts, success, failed, auto_rebuild=auto_rebuild)

        # ─────────────────────────────────────────────
        # MODE 3: KUBERNETES / MINIKUBE
        # ─────────────────────────────────────────────
        if backend == "kube":
            kube_machine_run(machine, image_name, machine_path, payload, namespace, workflow_name, workflow_ts, success, failed, auto_rebuild=auto_rebuild)        

    typer.secho("")
    typer.secho("\n🏁 Workflow Completed!", fg=typer.colors.CYAN)
    typer.secho(f"✅ Successful Machines: {sorted(success)}", fg=typer.colors.GREEN)
    typer.secho(f"❌ Failed Machines: {sorted(failed)}", fg=typer.colors.RED)
    typer.secho("")

