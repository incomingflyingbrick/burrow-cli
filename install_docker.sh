# Add Docker's official GPG key:
sudo apt-get update -y
sudo apt-get install ca-certificates curl wget -y
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update -y
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y
sudo docker run hello-world

#install pip
sudo apt update -y
sudo apt install python3-pip -y

#install burrow
sudo pip install genv
git clone https://github.com/run-ai/genv.git $HOME/genv
wget https://raw.githubusercontent.com/incomingflyingbrick/burrow/main/genv_run_time.py
sudo python3 genv_run_time.py
systemctl restart docker
cp -f $HOME/genv/genv-docker/genv-docker.sh /usr/local/bin/genv-docker
genv-docker run --rm ubuntu env | grep GENV_
pip install burrow
echo "Burrow install success"