import typer
from rich import print
from typing_extensions import Annotated
import re
import docker
import tarfile
import os
import time
import uuid
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from pathlib import Path

app = typer.Typer()
app_dir = typer.get_app_dir("burrow-cli")
container_env: Path = Path(app_dir) / "cached.json"


def print_file_content(file_path):
    try:
        with open(file_path, "r") as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print(f"Error: The file at '{file_path}' was not found.")
    except IOError as e:
        print(f"Error: An I/O error occurred while accessing the file: {e}")


def untar_and_list_files(tar_path, extract_path="."):
    """
    Untars a tar file and lists the files inside.

    :param tar_path: Path to the tar file.
    :param extract_path: Path to extract the files. Defaults to current directory.
    """
    if not os.path.isfile(tar_path):
        print(f"File not found: {tar_path}")
        return

    try:
        with tarfile.open(tar_path, "r") as tar:
            print("Files in the tar archive:")
            tar_members = tar.getnames()
            for member in tar_members:
                print(member)

            tar.extractall(path=extract_path)
            print(f"Files have been extracted to: {extract_path}")

    except tarfile.TarError as e:
        print(f"Error reading tar file: {e}")


@app.callback()
def callback():
    """
    Callback for every command
    """
    pass


@app.command(name="start")
def start(
    gram: Annotated[
        str,
        typer.Argument(
            help="The size of GRAM to share\n\nExample 512mi or 2gi, mi == MB, gi == GB"
        ),
    ],
    split_gpu: Annotated[
        bool,
        typer.Option(
            help="Choose weather to split the GPU memory or not. This option is for internal testing only, should not be used by public user."
        ),
    ] = True,
):
    """
    Start a shared GPU container with a user defined GRAM size.

    Example: burrow start 512mi -> This command launchs a GPU container with 512MB of GRAM

    Example: burrow start 8gi -> This command launchs a GPU container with 8GB of GRAM
    """

    pattern = r"^\d+(mi|gi)$"
    if bool(re.match(pattern, gram)):
        # client = docker.DockerClient(base_url='unix://var/run/docker.sock',version='1.45')
        client = docker.from_env()
        env = ["GENV_GPUS={}".format(1), "GENV_GPU_MEMORY={}".format(gram)]
        gpu_container = None
        if split_gpu:
            typer.echo("Start a shared GPU with GRAM size of {}".format(gram[0:-2]))
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                transient=True,
            ) as progress:
                progress.add_task(description="Downloading docker image", total=None)
                gpu_container = client.containers.run(
                    "jyzisgod/python3:latest",
                    detach=True,
                    remove=True,
                    stdout=True,
                    environment=env,
                    runtime="genv",
                    labels={"burrow-cli-container": uuid.uuid4().hex},
                )
        else:
            typer.echo(
                "Start a shared container without splitting GPU {}".format(gram[0:-2])
            )
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                transient=True,
            ) as progress:
                progress.add_task(description="Downloading docker image", total=None)
                gpu_container = client.containers.run(
                    "jyzisgod/python3:latest",
                    detach=True,
                    remove=True,
                    stdout=True,
                    environment=env,
                    labels={"burrow-cli-container": uuid.uuid4().hex},
                )

        f = open("./sh_bin.tar", "wb")
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(
                description="Creating GPU fractional container...usually take about 5 seconds",
                total=None,
            )
            time.sleep(5)

        bits, stat = gpu_container.get_archive("/workspace/server.txt")
        # print(stat)
        # print(type(bits))
        for chunk in bits:
            f.write(chunk)
        f.close()
        untar_and_list_files("./sh_bin.tar")
        sshx_url = print_file_content("./server.txt")
        print("[bold green]GPU fractional container created successfully![/bold green]")
        print(
            "Now you can send this link [bold blue]{}[/bold blue] to your friends, and start sharing the GPU 🚀💻✨".format(
                sshx_url
            )
        )
    else:
        typer.echo("Wrong memory size format, size should be like 512mi or 2gi")


@app.command(name="stop")
def stop(
    container_id: Annotated[
        str,
        typer.Argument(
            help="Stop a container with container_id, or `all` for all running burrow container"
        ),
    ]
):
    """
    Stop a running burrow container, or `burrow stop all` to stop all burrow container
    """
    if container_id == "all":
        client = docker.from_env()
        # client = docker.DockerClient(base_url='unix://var/run/docker.sock')
        container_list = client.containers.list(
            filters={"label": "burrow-cli-container"}
        )
        if len(container_list) == 0:
            print("No burrow container is running")
        else:
            for c in container_list:
                c.stop()
    else:
        client = docker.from_env()
        # client = docker.DockerClient(base_url='unix://var/run/docker.sock')
        gpu_container = client.containers.get(container_id=container_id)
        stop_result = gpu_container.stop()
        typer.echo("Stopped the container {}".format(stop_result))


@app.command("stop-all")
def stop_all():
    """
    Stop all running burrow container
    """
    client = docker.from_env()
    # client = docker.DockerClient(base_url='unix://var/run/docker.sock')
    container_list = client.containers.list(filters={"label": "burrow-cli-container"})
    if len(container_list) == 0:
        print("No burrow container is running")
    else:
        for c in container_list:
            c.stop()


@app.command(name="list")
def show_container():
    """
    List all running containers started by Burrow
    """
    client = docker.from_env()
    # client = docker.DockerClient(base_url='unix://var/run/docker.sock')
    container_list = client.containers.list(filters={"label": "burrow-cli-container"})
    if len(container_list) == 0:
        print("No burrow container is running")
    else:
        table = Table(title="All running burrow containers")
        table.add_column("ID", justify="right", style="cyan", no_wrap=True)
        table.add_column("name", style="magenta")
        table.add_column("status", justify="right", style="green")
        for container in container_list:
            table.add_row(container.short_id, container.name, container.status)
    print(table)
