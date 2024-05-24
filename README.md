# Share part of your GPU with your friends!

* With Burrow, you can share part of your GPU with your friends with a single link! 🚀🔗
* Work collaboratively in the same terminal, especially thanks to sshx.io 👨‍💻👩‍💻
* With security in mind, Burrow uses sandbox Docker containers, so your friends can't access your local files. 🛡️🐳🔒

# Install
## Prerequises
* Burrow requires Docker to run. It will install Docker on your local machine if it's not already installed. The automated Docker installation only works on Ubuntu; if you are using other Linux distributions, you will need to install Docker yourself first.
## Install with a script
Run the installation script(Only tested on Ubuntu)
```
curl -sSL https://raw.githubusercontent.com/incomingflyingbrick/burrow-cli/main/install_burrow.sh | sudo sh
```

# Quick Start
Launch a sharable GPU container with 3GB GRAM
```shell
burrow start 3gi
```

List all running burrow container
```
burrow list
```

# Development

* This project is developed using Poetry and Typer
* Python version 3.12.3