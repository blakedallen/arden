# docker run --privileged --runtime nvidia --rm -v /data:/data -e DISPLAY -v /tmp:/tmp -ti yolov5 python3 detect_f.py --source DJI_0225_Trim.mp4 --weights yolov5x.pt --conf 0.4 --network arden

docker run --privileged --runtime nvidia --rm -v /data:/data -e DISPLAY -v /tmp:/tmp -ti --network arden yolov5_final python3 detect_f.py --source grey_trim_540p.mp4 --weights yolov5s.pt --conf 0.4 
