# Share part of your GPU with your friends using Burrow!

* With Burrow, you can share part of your GPU with your friends with a single link! 🚀🔗
* Work collaboratively in the same terminal, especially thanks to sshx.io 👨‍💻👩‍💻
* With security in mind, Burrow uses sandbox Docker containers, so your friends can't access your local files. 🛡️🐳🔒

# Install

## Prerequises
You need the following software installed in order to run Burrow, if you already have them installed you can skip this section.
* Burrow requires __Docker__ to run
* Burrow requires __Python3__ to run

## Install with a script

Run the installation script
```
curl -sSL https://raw.githubusercontent.com/incomingflyingbrick/burrow-cli/main/install_burrow.sh | sudo bash
```

# Quick Start

Launch a sharable GPU container with 3GB GRA
```bash
burrow start 3gi
```

List all running burrow container
```bash
burrow list
```

Stop a burrow container
```bash
burrow stop <container_id>
# or stop all container
burrow stop all
```

# Development

* This project is developed using __Poetry__ and __Typer__
* Python version __3.12.3__

# Compatbility Test
We are trying to test Burrow with GPU, below are the test result.
## Ubuntu
* Ubuntu Noble 24.04 (LTS) (Not tested yet)
* Ubuntu Mantic 23.10 (EOL: July 12, 2024) (Not tested yet)
* Ubuntu Jammy 22.04 (LTS) (Tested with GPU)
* Ubuntu Focal 20.04 (LTS) (Tested with GPU)

## CentOS (Not tested with GPU yet)
* CentOS 7 (EOL: June 30, 2024) (Needs to install python3 and git first)
* CentOS 8 (stream) (EOL: May 31, 2024) (Needs to install python3 and git first)
* CentOS 9 (stream) (Needs to install git first)


## Debian (Not tested with GPU yet)
* Debian Bookworm 12 (stable) (Needs to install git first)
* Debian Bullseye 11 (oldstable) (Needs to install git first)