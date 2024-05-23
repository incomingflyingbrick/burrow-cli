import typer
from rich import print
from typing_extensions import Annotated
import re
import docker
import tarfile
import os
import time

app = typer.Typer()

def print_file_content(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            print(content)
    except FileNotFoundError:
        print(f"Error: The file at '{file_path}' was not found.")
    except IOError as e:
        print(f"Error: An I/O error occurred while accessing the file: {e}")

def untar_and_list_files(tar_path, extract_path='.'):
    """
    Untars a tar file and lists the files inside.

    :param tar_path: Path to the tar file.
    :param extract_path: Path to extract the files. Defaults to current directory.
    """
    if not os.path.isfile(tar_path):
        print(f"File not found: {tar_path}")
        return

    try:
        with tarfile.open(tar_path, 'r') as tar:
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
    Init
    """


@app.command(name='start')
def start(gram: Annotated[str, typer.Argument(help="The size of GPU memory to share\nformat example 512mi or 2gi, mi == MB, gi == GB")]):
    """
    Start a shared GPU container with a user set memory size
    """
    pattern = r'^\d+(mi|gi)$'
    if bool(re.match(pattern, gram)):
        # client = docker.DockerClient(base_url='unix://var/run/docker.sock',version='1.45')
        client = docker.from_env()
        typer.echo("Start a shared GPU with GRAM size of {}".format(gram[0:-2]))
        name = "shared_gpu_1"
        env = ["GENV_GPUS={}".format(1),"GENV_GPU_MEMORY={}".format(gram)]
        file_name = 'server.txt'
        # client.containers.run('jyzisgod/python3:latest','sshx -q > {}.txt'.format(file_name),detach=True,remove=True,stdout=True,name=name,environment=env,runtime='genv')
        gpu_container = client.containers.run('jyzisgod/python3:latest',detach=True,remove=True,stdout=True,name=name)
        f = open('./sh_bin.tar', 'wb')
        time.sleep(10)
        bits, stat = gpu_container.get_archive('/workspace/server.txt')
        print(stat)
        print(type(bits))
        for chunk in bits:
            f.write(chunk)
        f.close()
        untar_and_list_files('./sh_bin.tar')
        print_file_content('./server.txt')
    else:
        typer.echo("Wrong memory size format, size should be like 512mi or 2gi")


@app.command()
def stop(container_id: Annotated[str, typer.Argument(help="stop a container with container_id")]):
    """
    Stop a running container
    """
    client = docker.DockerClient(base_url='unix://var/run/docker.sock')
    gpu_container = client.containers.get(container_id=container_id)
    stop_result = gpu_container.stop()
    typer.echo("Stop the container {}".format(stop_result))