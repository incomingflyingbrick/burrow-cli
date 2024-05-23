FROM python:3
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get install -y openssh-server && \
    mkdir /var/run/sshd && \
    echo 'root:123' | chpasswd && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config
RUN apt-get install vim -y
RUN mkdir /workspace
WORKDIR /workspace
RUN curl -sSf https://sshx.io/get | sh
EXPOSE 22
# CMD ["/usr/sbin/sshd","-D"]
CMD sshx -q > server.txt
