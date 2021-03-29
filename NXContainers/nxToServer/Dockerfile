FROM ubuntu
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update
RUN apt install -y python3-dev python3-pip  python3-opencv vim-tiny  libopencv-dev
RUN pip3 install numpy paho-mqtt
WORKDIR /apps
COPY *.py ./
RUN chmod 700 *.*

CMD python3 /apps/server.py
