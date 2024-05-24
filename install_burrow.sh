#!/bin/bash

# Check if Docker is installed
if command -v docker &> /dev/null
then
    echo "Docker is already installed"
else
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
fi

# Check if pip is installed
if command -v pip3 &> /dev/null
then
    echo "pip is already installed"
else
    echo "pip is not installed. Installing pip..."

    # Update package list and install pip
    sudo apt update -y
    sudo apt install python3-pip -y
fi

#install genv
sudo pip install genv
git clone https://github.com/run-ai/genv.git $HOME/genv
wget https://raw.githubusercontent.com/incomingflyingbrick/burrow-cli/main/genv_run_time.py
python3 genv_run_time.py
systemctl restart docker
cp -f $HOME/genv/genv-docker/genv-docker.sh /usr/local/bin/genv-docker
genv-docker run --rm ubuntu env | grep GENV_
rm genv_run_time.py

#install burrow-cli
pip install -U burrow-cli
echo "Burrow python library install success! now try 'burrow start 2gi' cmd to launch a fractional GPU container and share it to your friends!"
