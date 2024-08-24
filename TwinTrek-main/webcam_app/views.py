# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from django.shortcuts import render
# from .serializers import WebcamImageSerializer
# import cv2
# import numpy as np
# import threading

# import numpy as np

# from .gestureDetector import HandDetector
# from .gestureDetector import KeyPointClassifier

# import socket

# from django.http.response import StreamingHttpResponse
# from webcam_app.camera import BuggyCam
# from django.views.decorators.csrf import csrf_exempt
# from django.views.decorators.http import require_POST
# from django.http import JsonResponse
# import json

# # Global variables
# mode = "manual"
# detector = HandDetector() #detector obj

# forward = False # is going forward or backward
# speed = 0   # speed of buggy

# labels = ['Start','NULL','Left','Right','Mark','Pick','Drop']   # labels of gestures

# kpc = KeyPointClassifier()  # gesture classification object

# latitude = 30.352899
# longitude = 78.386324
# smokeLevel =0
# direction = None
# obstacleDistance = None

# buggyCam = BuggyCam()

# # socket setup
# server_port = 23000
# sock = None
# use_socket = True
# busy_sock = False


# def manual(request):
#     global mode 
#     mode = "manual"
    
#     message = "Mode,manual\n"
#     send_cmd(message)
    
#     return render(request,"index.html")

# def automatic(request):
#     global mode
#     mode = "automatic"
    
#     message = "Mode,automatic\n"
#     send_cmd(message)
#     return render(request,"index2.html")
    

# @api_view(['GET'])
# def get_coordinates(request):
#     global latitude, longitude

#     data = {
#         'latitude': latitude,
#         'longitude': longitude,
#     }
#     return Response(data)

# @csrf_exempt
# @require_POST
# def post_coordinates(request):
#     try:
#         data = json.loads(request.body)
#         latitude = data.get('latitude')
#         longitude = data.get('longitude')
        
#         message = "Destination," + str(latitude) + "," + str(longitude) + "\n"
        
#         while busy_sock: 
#             pass
#         busy_sock = True
#         send_cmd(message)
#         busy_sock = False
        
        

#         print("Received coordinates - Latitude:", latitude, "Longitude:", longitude)

#         return JsonResponse({'message': 'Coordinates updated successfully.'})
#     except json.JSONDecodeError as e:
#         return JsonResponse({'error': 'Invalid JSON format.'}, status=400)
#     except Exception as e:
#         return JsonResponse({'error': str(e)}, status=500)
    
    
# @api_view(['POST'])    
# def getBuggyPosition(request):
#     try:
#         data = request.data
#         global latitude, longitude
#         latitude = float(data.get('latitude'))
#         longitude = float(data.get('longitude'))
        
#         print(latitude,longitude)
#         return JsonResponse({'status' : 'success'})
#     except:
#         return JsonResponse({'status': 'error'})

# @api_view(['POST'])    
# def getUltrasonicDistance(request):
#     try:
#         data = request.data
#         global obstacleDistance
#         obstacleDistance = float(data.get('distance'))
        
#         return JsonResponse({'status' : 'success'})
#     except:
#         return JsonResponse({'status': 'error'})
    
# @api_view(['POST'])    
# def getDirection(request):
#     try:
#         data = request.data
#         global direction
#         direction = float(data.get('direction'))
#         return JsonResponse({'status' : 'success'})
#     except:
#         return JsonResponse({'status': 'error'})

# @api_view(['POST'])    
# def getSmokeLevel(request):
#     try:
#         data = request.data
#         global smokeLevel
#         smokeLevel = float(data.get('smokeLevel'))        
#         print(smokeLevel)
#         return JsonResponse({'status' : 'success'})
#     except:
#         return JsonResponse({'status': 'error'})

# @api_view(['GET'])
# def get_gas_sensor_value(request):
#     global smokeLevel

#     return JsonResponse({'gas_value': smokeLevel})

# def send_cmd(cmd):
#     global sock
#     try:
#         sock.send(cmd.encode())
#     except:
#         print("Connection with buggy lost")
#         if(sock is not None):
#             sock.close()
#     return


# def socket_setup(): 
#     global sock
#     # print("here")
#     listen_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#     listen_sock.bind(("0.0.0.0",server_port))
#     listen_sock.listen(10)
#     while True:
#         (comm,addr) = listen_sock.accept()
#         sock = comm
    

# def setup():
    
#     if use_socket:
#         threading.Thread(target=socket_setup).start()

# setup()


# @api_view(['POST'])
# def webcam_image_view(request):
    
#     if request.method == 'POST':
        
#         data = np.asarray(bytearray(request.FILES['image'].read()),dtype='uint8')
#         data = cv2.imdecode(data,cv2.IMREAD_COLOR)
        
#         processHand(data)
            
#     return Response({'message': 'Webcam image processed successfully'})

# def gen(camera):
# 	while True:
# 		frame = camera.get_frame()
# 		yield (b'--frame\r\n'
# 				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

# def buggy_feed(request):
# 	return StreamingHttpResponse(gen(buggyCam),
# 					content_type='multipart/x-mixed-replace; boundary=frame')


# def processHand(image):
#     # img = cv2.flip(image,1)
#     global forward
#     global speed
#     global busy_sock

#     hands_info = detector.getHandInfo(image)

#     for hand in hands_info:
#         if(hand['hand']=='Left'):
            
#             xt,yt = hand['landmarks'][4][0],hand['landmarks'][4][1]
#             xf,yf = hand['landmarks'][8][0],hand['landmarks'][8][1]

#             forward = yt>yf
#             # print(forward)

#             xmin,xmax,ymin,ymax = detector.getBoundingValues(hand['landmarks'])

#             #scale for speed independence
#             xt = np.interp(xt,(xmin,xmax),(0,300))
#             xf = np.interp(xf,(xmin,xmax),(0,300))
#             yt = np.interp(yt,(ymin,ymax),(0,300))
#             yf = np.interp(yf,(ymin,ymax),(0,300))
            
#             speed = np.hypot(xt-xf,yt-yf)  # goes atmax to 300
#             print(speed)
#             # print(preprocessed_lm)
#         else:
#             preProcessedLandmark = detector.preprocessLandmark(hand['landmarks'])
#             signId = kpc(preProcessedLandmark)
            
#             message = str(forward) + "," + str(speed) + "," + str(signId) + '\n'
            
#             while busy_sock: 
#                 pass
#             busy_sock = True
#             send_cmd(message)
#             busy_sock = False
#             # print(labels[signId])
#             # if(signId==0):
#             #     print(forward,speed)
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from django.http import JsonResponse
from .serializers import GasSensorSerializer, PositionSerializer, DetectionSerializer
import cv2
import numpy as np
import threading
import json
from .gestureDetector import HandDetector, KeyPointClassifier
import socket
from django.http.response import StreamingHttpResponse
from webcam_app.camera import BuggyCam
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

# Global variables
mode = "manual"
detector = HandDetector()
forward = False
speed = 0
labels = ['Start', 'NULL', 'Left', 'Right', 'Mark', 'Pick', 'Drop']
kpc = KeyPointClassifier()
latitude =  30.35515908622681
longitude = 76.36968580268332
smokeLevel = 0
direction = None
obstacleDistance = None
buggyCam = BuggyCam()

# socket setup
server_port = 23000
sock = None
use_socket = True
busy_sock = False

@api_view(['GET'])
def get_coordinates(request):
    global latitude, longitude
    data = {'latitude': latitude, 'longitude': longitude}
    return Response(data)

@csrf_exempt
@require_POST
def post_coordinates(request):
    try:
        data = json.loads(request.body)
        global latitude, longitude
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        message = f"Destination,{latitude},{longitude}\n"
        
        while busy_sock:
            pass
        busy_sock = True
        send_cmd(message)
        busy_sock = False
        print(f"Received coordinates - Latitude: {latitude} Longitude: {longitude}")
        return JsonResponse({'message': 'Coordinates updated successfully.'})
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format.'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api_view(['POST'])
def getBuggyPosition(request):
    try:
        data = request.data
        global latitude, longitude
        latitude = float(data.get('latitude'))
        longitude = float(data.get('longitude'))
        print(latitude, longitude)
        return JsonResponse({'status': 'success'})
    except Exception:
        return JsonResponse({'status': 'error'})

@api_view(['POST'])
def getUltrasonicDistance(request):
    try:
        data = request.data
        global obstacleDistance
        obstacleDistance = float(data.get('distance'))
        return JsonResponse({'status': 'success'})
    except Exception:
        return JsonResponse({'status': 'error'})

@api_view(['POST'])
def getDirection(request):
    try:
        data = request.data
        global direction
        direction = float(data.get('direction'))
        return JsonResponse({'status': 'success'})
    except Exception:
        return JsonResponse({'status': 'error'})

@api_view(['POST'])
def getSmokeLevel(request):
    try:
        data = request.data
        global smokeLevel
        smokeLevel = float(data.get('smokeLevel'))
        print(smokeLevel)
        return JsonResponse({'status': 'success'})
    except Exception:
        return JsonResponse({'status': 'error'})

@api_view(['GET'])
def get_gas_sensor_value(request):
    global smokeLevel
    return JsonResponse({'gas_value': smokeLevel})

def send_cmd(cmd):
    global sock
    try:
        sock.send(cmd.encode())
    except Exception:
        print("Connection with buggy lost")
        if sock is not None:
            sock.close()

def socket_setup():
    global sock
    listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_sock.bind(("0.0.0.0", server_port))
    listen_sock.listen(10)
    while True:
        (comm, addr) = listen_sock.accept()
        sock = comm

def setup():
    if use_socket:
        threading.Thread(target=socket_setup).start()

setup()

@api_view(['POST'])
def webcam_image_view(request):
    if request.method == 'POST':
        data = np.asarray(bytearray(request.FILES['image'].read()), dtype='uint8')
        data = cv2.imdecode(data, cv2.IMREAD_COLOR)
        processHand(data)
    return Response({'message': 'Webcam image processed successfully'})

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        
def buggy_feed(request):
        return StreamingHttpResponse(gen(buggyCam), content_type='multipart/x-mixed-replace; boundary=frame')

def processHand(image):
    global forward, speed, busy_sock
    hands_info = detector.getHandInfo(image)
    for hand in hands_info:
        if hand['hand'] == 'Left':
            xt, yt = hand['landmarks'][4][0], hand['landmarks'][4][1]
            xf, yf = hand['landmarks'][8][0], hand['landmarks'][8][1]
            forward = yt > yf
            xmin, xmax, ymin, ymax = detector.getBoundingValues(hand['landmarks'])
            xt = np.interp(xt, (xmin, xmax), (0, 300))
            xf = np.interp(xf, (xmin, xmax), (0, 300))
            yt = np.interp(yt, (ymin, ymax), (0, 300))
            yf = np.interp(yf, (ymin, ymax), (0, 300))
            speed = np.hypot(xt - xf, yt - yf)
            print(speed)
        else:
            preProcessedLandmark = detector.preprocessLandmark(hand['landmarks'])
            signId = kpc(preProcessedLandmark)
            message = f"{forward},{speed},{signId}\n"
            while busy_sock:
                pass
            busy_sock = True
            send_cmd(message)
            busy_sock = False

@api_view(['GET'])
def get_detection(request):
    global latitude, longitude
    data = {'latitude': latitude, 'longitude': longitude}
    return Response(data)

