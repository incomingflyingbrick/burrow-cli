#!/bin/bash

# This script will install docker and pip3 on your system if it's not installed
# Tested for ubuntu 24.04, 23.10 EOL, 22.04, 20.04
# Tested for debian 12,11,10
# Tested for centOS 9
# centOS 8 and lower doesn't have python3 installed, so you have to install python3 yourself first

# Function to check if a command is available
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Detect the operating system
os_name=""
if [ -f /etc/os-release ]; then
    . /etc/os-release
    os_name=$ID
elif [ -f /etc/centos-release ]; then
    os_name="centos"
else
    echo "Unsupported operating system."
    exit 1
fi

# Print the detected operating system
echo "Detected operating system: $os_name"

# Check if Docker is installed
if command_exists docker; then
    echo "Docker is installed already."
else
    echo "Docker not found installing docker for $os_name."
    if [ $os_name = "ubuntu" ]; then
        echo "Docker is not installed. Installing Docker..."

        # Update package list and install prerequisites
        sudo apt-get update -y
        sudo apt-get install ca-certificates curl wget -y

        # Add Docker's official GPG key
        sudo install -m 0755 -d /etc/apt/keyrings
        sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
        sudo chmod a+r /etc/apt/keyrings/docker.asc

        # Add Docker repository to Apt sources
        echo \
        "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
        $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
        sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

        # Update package list and install Docker
        sudo apt-get update -y
        sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y

        # Run the hello-world container to verify Docker installation
        sudo docker run hello-world


    elif [ $os_name = "debian" ]; then
        echo "installing docker on debian"
        # Add Docker's official GPG key:
        sudo apt-get update -y
        sudo apt-get install ca-certificates curl -y
        sudo install -m 0755 -d /etc/apt/keyrings
        sudo curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc
        sudo chmod a+r /etc/apt/keyrings/docker.asc

        # Add the repository to Apt sources:
        echo \
        "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian \
        $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
        sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
        sudo apt-get update -y

        #install docker engine
        sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y
        sudo docker run hello-world

    elif [ $os_name = "centos" ]; then
        echo "installing docker on centos"
        sudo yum install -y yum-utils
        sudo yum-config-manager -y --add-repo https://download.docker.com/linux/centos/docker-ce.repo
        sudo yum install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
        sudo systemctl start docker
        sudo docker run hello-world
    else
        echo "You have to install Docker first in order to use Burrow"
        
    fi


fi

# Check if pip3 is installed
if command_exists pip3; then
    echo "pip3 is already installed."
else # install pip
    echo "Installing pip3 for $os_name."
    if [ $os_name = "ubuntu" ]; then
        # Update package list and install pip
        sudo apt update -y
        sudo apt install python3-pip -y
    elif [ $os_name = "debian" ]; then
        # Update package list and install pip
        sudo apt update -y
        sudo apt install python3-pip -y
    elif [ $os_name = "centos" ]; then
        # install pip using python
        python3 -m ensurepip --upgrade
    else
        echo "You have to install pip3 firt in order to use Burrow"
        
    fi
fi

pip3 --help

#install genv
sudo pip3 install genv
git clone https://github.com/run-ai/genv.git $HOME/genv
wget https://raw.githubusercontent.com/incomingflyingbrick/burrow-cli/main/genv_run_time.py
python3 genv_run_time.py
systemctl restart docker
cp -f $HOME/genv/genv-docker/genv-docker.sh /usr/local/bin/genv-docker
genv-docker run --rm ubuntu env | grep GENV_
rm genv_run_time.py

#install burrow-cli
pip3 install burrow-cli
echo "Burrow python library install success! now try 'burrow start 2gi' cmd to launch a fractional GPU container and share it to your friends!"
