import socket
import cv2
import time
# import humanDetector


server_ip = "192.168.111.242"
server_port=22000

def connect():
    global sock
    try:
        sock.connect((server_ip,server_port))
        # print("connected")
        return 1
    except:
        return 0
    
def setup():
    global sock
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    while(not connect()):
        time.sleep(0.5)
        pass

cam = cv2.VideoCapture(0)
# humanDetector = humanDetector.HumanDetector()


while True:
    
    setup()

    ret ,frame = cam.read()
    
    if(not ret):
        print("unable to capture image")
        continue
    # print('success')
    
    # frame = humanDetector.drawHuman(frame)
    
    img = cv2.imencode('.jpeg',frame)[1]


    # print("Sent image to server")
    try:
        sock.send(img)
    except:
        continue

    # time.sleep(0.033)       # 30 fps



