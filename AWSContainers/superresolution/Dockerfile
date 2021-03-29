FROM ubuntu
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update
RUN apt install -y python3-dev python3-pip  python3-opencv vim-tiny  libopencv-dev
RUN pip3 install numpy 
RUN pip3 install numpy paho-mqtt
RUN pip3 install boto3

WORKDIR /root
COPY *.py ./
RUN chmod 700 *.*
