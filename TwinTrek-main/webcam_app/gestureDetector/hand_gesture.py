import cv2
import mediapipe as mp
import copy
import itertools
import numpy as np
from .keypoint_classifier.keypoint_classifier import KeyPointClassifier


class HandDetector:
    def __init__(self,mode=False,maxHands = 2,detection = 0.62,tracking = 0.5):
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode = mode,
            max_num_hands=maxHands,
            min_detection_confidence=detection,
            min_tracking_confidence=tracking,
        )
        self.mpDraw = mp.solutions.drawing_utils

    def drawHands(self,img):
        imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        results = self.hands.process(imgRGB)

        if results.multi_hand_landmarks is not None:
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks,results.multi_handedness):
                self.mpDraw.draw_landmarks(img,hand_landmarks,self.mpHands.HAND_CONNECTIONS)
        
        return img

    def getBoundingValues(self,landmarks):
        xmin,ymin = 10**8,10**8
        xmax,ymax=0,0

        for point in landmarks:
            xmin = min(point[0],xmin)
            xmax = max(point[0],xmax)
            ymin = min(point[1],ymin)
            ymax = max(point[1],ymax)

        return xmin,xmax,ymin,ymax


    def getHandInfo(self,img):
        img = cv2.flip(img,1)
        image_width, image_height = img.shape[1], img.shape[0]
        imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        results = self.hands.process(imgRGB)

        info = []

        if results.multi_hand_landmarks is not None:
            # info['landmarks']=[]
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks,results.multi_handedness):
                dict = {}
                dict['landmarks']=[]
                for lm in hand_landmarks.landmark:
                    lmx = min(int(lm.x * image_width), image_width - 1)
                    lmy = min(int(lm.y * image_height), image_height - 1)

                    dict['landmarks'].append([lmx,lmy])
                hand = handedness.classification[0].label[0:]
                dict['hand']=hand
                info.append(dict)
        return info
    


    def preprocessLandmark(self,landmark_list):
        temp_landmark_list = copy.deepcopy(landmark_list)

        # Convert to relative coordinates
        base_x, base_y = 0, 0
        for index, landmark_point in enumerate(temp_landmark_list):
            if index == 0:
                base_x, base_y = landmark_point[0], landmark_point[1]

            temp_landmark_list[index][0] = temp_landmark_list[index][0] - base_x
            temp_landmark_list[index][1] = temp_landmark_list[index][1] - base_y

        # Convert to a one-dimensional list
        temp_landmark_list = list(
            itertools.chain.from_iterable(temp_landmark_list))

        # Normalization
        max_value = max(list(map(abs, temp_landmark_list)))

        def normalize_(n):
            return n / max_value

        temp_landmark_list = list(map(normalize_, temp_landmark_list))

        return temp_landmark_list


def main():
    det = HandDetector()
    cap = cv2.VideoCapture(0)

    forward = False
    distance = 0

    labels = ['start','NULL','Left','Right','Mark','Pick','Drop']

    kpc = KeyPointClassifier()


    while True:
        ret,img = cap.read()


        if not ret:
            return

        pimg = det.drawHands(img)

        hands_info = det.getHandInfo(img)

        for hand in hands_info:
            if(hand['hand']=='Left'):
                
                xt,yt = hand['landmarks'][4][0],hand['landmarks'][4][1]
                xf,yf = hand['landmarks'][8][0],hand['landmarks'][8][1]

                forward = yt>yf
                # print(forward)

                # xmin,xmax,ymin,ymax = det.getBoundingValues(hand['landmarks'])

                #scale for distance independence
                # xt = np.interp(xt,(xmin,xmax),(0,300))
                # xf = np.interp(xf,(xmin,xmax),(0,300))
                # yt = np.interp(yt,(ymin,ymax),(0,300))
                # yf = np.interp(yf,(ymin,ymax),(0,300))
                
                distance = np.hypot(xt-xf,yt-yf)  # goes atmax to 300
                # print(distance)
                # print(preprocessed_lm)
            else:
                preProcessedLandmark = det.preprocessLandmark(hand['landmarks'])
                signId = kpc(preProcessedLandmark)
                
                print(labels[signId])
                if(labels[signId]=='start'):
                    print(forward,distance)



        # print()

        cv2.imshow("Video",pimg)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


if __name__=="__main__":
    main()