import requests
from buggyController import BuggyController
import time
 
server_ip = "192.168.111.242"

position_endpoint = "http://"+server_ip+":8000/api/get-buggy-coordinates/"
smoke_endpoint = 'http://'+server_ip+':8000/api/get-smoke-level/'
ultrasonic_endpoint = 'http://'+server_ip+':8000/api/get-obstacle-distance/'
direction_endpoint = 'http://'+server_ip+':8000/api/api/get-direction/'
 
GPIO_TRIGGER = 18
GPIO_ECHO = 24


 
bc = BuggyController()
bc.gpsSetup()
bc.ultrasonicSetup(GPIO_TRIGGER,GPIO_TRIGGER) 
bc.magnetoSetup()


while True:
    try:
        lat,long = bc.getLatLong()
        smokeLevel = bc.getSmokeLevel()



        # data to be sent to api
        posData = {'latitude':lat,
                'longitude': long}
        smokeData = {'smokeLevel':smokeLevel}
        
        magnetoData = {
            'direction' : bc.get_current_direction()
        }
        distanceData = {
            'distance' : bc.getDistance()
        }

        requests.post(url=position_endpoint, data=posData)
        requests.post(url=smoke_endpoint,data=smokeData)
        requests.post(url=ultrasonic_endpoint,data=distanceData)
        requests.post(url=direction_endpoint,data=magnetoData)
    except:
        pass
    time.sleep(1)
 
