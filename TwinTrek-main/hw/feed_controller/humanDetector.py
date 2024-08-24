from ultralytics import YOLO
import cv2
import math 

class HumanDetector:
    def __init__(self):
        # model
        self.model = YOLO("yolo-Weights/yolov8n.pt")

        # object classes
        self.classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
                    "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
                    "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
                    "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
                    "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
                    "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
                    "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
                    "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
                    "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
                    "teddy bear", "hair drier", "toothbrush"
                    ]
        

    def drawHuman(self,img):
        results = self.model(img, stream=True,verbose = False)
        # coordinates
        for r in results:
            boxes = r.boxes

            for box in boxes:
                # bounding box
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) # convert to int values
                
                # confidence
                confidence = math.ceil((box.conf[0]*100))/100
                obj = self.classNames[int(box.cls[0])]
                
                if(confidence>=0.5 and obj == 'person'):
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 3)
                    # object details
                    org = [x1, y1]
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    fontScale = 1
                    color = (255, 0, 0)
                    thickness = 2

                    cv2.putText(img, "Human Detected", org, font, fontScale, color, thickness)
                
        return img
                

                
if __name__ == "__main__":
    # start webcam
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    det = HumanDetector()



    while True:
        success, img = cap.read()
        
        img = det.drawHuman(img)
        
        cv2.imshow('Webcam', img)
        if cv2.waitKey(1) == ord('q'):
            break
        
    cap.release()
    cv2.destroyAllWindows()
