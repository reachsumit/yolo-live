import subprocess
#subprocess.call(r"./darknet detect cfg/yolov3.cfg yolov3.weights data/dog.jpg", shell=True)
subprocess.call(r"./darknet detector test cfg/yolov3.cfg yolov3.weights --dont_show data/dog.jpg", shell=True, cwd="/home/ubuntu/darknet")
print("Post Malone")
