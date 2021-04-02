FROM tensorflow/tensorflow:1.13.1-py3
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update
RUN apt install -y python3-dev python3-pip  python3-opencv vim-tiny  libopencv-dev
RUN pip3 install numpy 
RUN pip3 install paho-mqtt
RUN pip3 install boto3
RUN pip3 install tensorflow==1.13.1
RUN pip3 install ISR==2.1

RUN apt-get update && apt-get install -y --no-install-recommends
	bzip2 \
	g++ \
 	git \
	graphviz \
 	libgl1-mesa-glx \
 	libhdf5-dev \
	openmpi-bin \
	screen \
	wget && \
	rm -rf /var/lib/apt/lists/* \
	apt-get upgrade

RUN python3 -m pip install isr

WORKDIR /root
COPY *.py ./
RUN chmod 700 *.*
