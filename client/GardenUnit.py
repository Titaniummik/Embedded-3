from grovepi import *
import math
import requests
import json

SLEEP_INTERVAL = 100
MAX_RETRIES = 3

class GardenUnit():    
    def __init__(self, host, user, pwd):
        self.__user = user
        self.__pwd = pwd
        if "http" not in host:
           self.host = "http://" + host
        else:
            self.host = host
        self.token = self.__auth()
        self.headers = headers = {"Authorization": self.token}

    def sensor_handler(func):
        def inner_function(self, *args, **kwargs):
            try:
                output = func(self,*args, **kwargs)
                if type(output) == list:
                    for i in output:
                        if math.isnan(i):
                            i = False
                else:
                    if math.isnan(output):
                        output = False
                return output
            except IOError as TypeError:
                return -1
        return inner_function

    def token_refresher(func):
        def inner_function(self, *args, **kwargs):
            try:
                return(func(self,*args, **kwargs))
            except:
                self.__auth()
                return(func(self,*args, **kwargs))
        return inner_function

    def __auth(self):
        url = self.host + "/api/auth/login"
        body = {
            "email": self.__user,
            "password": self.__pwd
            }
        r = requests.post(url, json=body)

        if r.status_code != 200:
            raise Exception(r.text)

        return ("Bearer {}".format(r.json()['token']))

    @sensor_handler
    def __read_temphumi(self, port):
        temp, hum = dht(port, 1)
        if temp == False or hum == False:
            return False, False
        return [int(temp), int(hum)]
    
    @sensor_handler
    def __read_light(self, port):
        light = analogRead(port)
        if light == False:
            return False
        return int(light)

    @token_refresher
    def update_temphum(self, port):
        temp, hum = self.__read_temphumi(port)

        if temp != False and hum != False:
            url = self.host + "/api/temperature"
            body = {"celcius": temp}
            
            r = requests.post(url, json=body, headers=self.headers)

            if r.status_code != 200:
                print(r.text)
            else:
                print(temp)

            url = self.host + "/api/humidity"
            body = {"percent": hum}
            
            r = requests.post(url, json=body, headers=self.headers)

            if r.status_code != 200:
                print(r.text)
            else:
                print(hum)
        else:
            print("Error while reading sensor")

    @token_refresher
    def update_light(self, port):
        light =  self.__read_light(port)
        if light != False:
            url = self.host + "/api/light"
            body = {"value": light}
            
            r = requests.post(url, json=body, headers=self.headers)

            if r.status_code != 200:
                print(r.text)
            else:
                print(light)
        else:
            print("Error while reading sensor")

if __name__ == "__main__":
    attempts = 0
    while attempts < MAX_RETRIES:
        try:
            unit = GardenUnit("http://3.73.140.96:5000", "pi@mail.com", "root")
            while True:
                unit.update_temphum(2)
                unit.update_light(1)
                time.sleep(SLEEP_INTERVAL)
        except Exception as e:
            attempts += 1
            if attempts < MAX_RETRIES:
                print("Error, will retry...")
            else:
                print("Error, Critical will not retry")
