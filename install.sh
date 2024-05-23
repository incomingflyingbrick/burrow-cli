#install genv
sudo pip install genv
git clone https://github.com/run-ai/genv.git $HOME/genv
wget https://raw.githubusercontent.com/incomingflyingbrick/burrow/main/genv_run_time.py
python3 genv_run_time.py
systemctl restart docker
cp -f $HOME/genv/genv-docker/genv-docker.sh /usr/local/bin/genv-docker
genv-docker run --rm ubuntu env | grep GENV_
rm genv_run_time.py

#install burrow-cli
pip install burrow-cli
echo "Burrow install success"
