docker run --privileged --runtime nvidia --rm -v /data:/data -e DISPLAY -v /tmp:/tmp -ti yolov5 python3 detect.py --source 0 --weights yolov5x.pt --conf 0.4

