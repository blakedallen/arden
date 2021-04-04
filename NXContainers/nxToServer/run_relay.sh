docker run -it --rm --privileged -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix --name relaycontainer -e MY_AWS_IP=3.101.26.64 --rm --network arden relay bash
