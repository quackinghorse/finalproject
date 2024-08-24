import cv2
import numpy as np
from django.conf import settings
from socket import *
import numpy as np
import cv2

class HumanDetector:
    def __init__(self):
        
        
        proto = "./webcam_app/humanDetectorWeights/MobileNetSSD_deploy.prototxt"
        weights = "./webcam_app/humanDetectorWeights/MobileNetSSD_deploy.caffemodel"
        self.net = cv2.dnn.readNetFromCaffe(proto , weights)
        
        self.classNames = { 0: 'background',
			1: 'aeroplane', 2: 'bicycle', 3: 'bird', 4: 'boat',
			5: 'bottle', 6: 'bus', 7: 'car', 8: 'cat', 9: 'chair',
			10: 'cow', 11: 'diningtable', 12: 'dog', 13: 'horse',
			14: 'motorbike', 15: 'person', 16: 'pottedplant',
			17: 'sheep', 18: 'sofa', 19: 'train', 20: 'tvmonitor' }
		

  
  
    def drawHuman(self,img):
        img_resized = cv2.resize(img , (300 , 300))
        blob = cv2.dnn.blobFromImage(img_resized , 0.007843 , (300 , 300) , 
									(127.5 , 127.5 , 127.5) , False)
        self.net.setInput(blob)
        detections = self.net.forward()
        
        height , width , _ = img.shape
        
        final = detections.squeeze()
        
        for i in range(final.shape[0]):
            conf = final[i , 2]
            if conf > 0.6:
                class_name = self.classNames[final[i , 1]]
                if class_name=='person':      
                    x1 , y1 , x2 , y2 = final[i , 3:]
                    x1 *= width
                    y1 *= height
                    x2 *= width
                    y2 *= height
                    top_left = (int(x1) , int(y1))
                    bottom_right = (int(x2) , int(y2))
                    img = cv2.rectangle(img , top_left , bottom_right , (0 , 255 , 0) , 3)
                    
			
        return img
                



class BuggyCam(object):
    def __init__(self):
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.bind(('0.0.0.0', 22002))  # Use a different port number

        self.hd = HumanDetector()
        self.sock.listen(10)

    def __del__(self):
        cv2.destroyAllWindows()
        self.sock.close()

    def get_frame(self):
        try:
            comm, addr = self.sock.accept()
            data = bytes()
            while True:
                rcv = comm.recv(1000000)
                if not rcv:
                    break
                data += rcv

            data = np.asarray(bytearray(data), dtype='uint8')
            data = cv2.imdecode(data, cv2.IMREAD_COLOR)
            data = self.hd.drawHuman(data)
            data = cv2.imencode('.jpeg', data)[1]
            return data.tobytes()
        except Exception as e:
            print(f"Error in get_frame: {e}")
        finally:
            comm.close()
