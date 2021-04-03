docker run -it --rm --privileged -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix --name relaycontainer --rm --network arden relay bash
