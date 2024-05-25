# Share part of your GPU with your friends!

* With Burrow, you can share part of your GPU with your friends with a single link! 🚀🔗
* Work collaboratively in the same terminal, especially thanks to sshx.io 👨‍💻👩‍💻
* With security in mind, Burrow uses sandbox Docker containers, so your friends can't access your local files. 🛡️🐳🔒

# Install

## Prerequises

* Burrow requires Docker to run. It will install Docker on your local machine if it's not already installed. The automated Docker installation only works on Ubuntu for now; if you are using other Linux distributions, you will need to install Docker yourself first.

## Install with a script

Run the installation script (Only tested on Ubuntu22.04 for now, more coming)
```
curl -sSL https://raw.githubusercontent.com/incomingflyingbrick/burrow-cli/main/install_burrow.sh | sudo sh
```

# Quick Start
Launch a sharable GPU container with 3GB GRAM

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

* This project is developed using Poetry and Typer
* Python version 3.12.3

# Compatbility
## Ubuntu
* Ubuntu Noble 24.04 (LTS)
* Ubuntu Mantic 23.10 (EOL: July 12, 2024)
* Ubuntu Jammy 22.04 (LTS)
* Ubuntu Focal 20.04 (LTS)

## CentOS
* CentOS 7 (EOL: June 30, 2024)
* CentOS 8 (stream) (EOL: May 31, 2024)
* CentOS 9 (stream)


## Debian
* Debian Bookworm 12 (stable)
* Debian Bullseye 11 (oldstable)