import requests
from flask import jsonify
import time

sensori = [1,1]
while True:
    pwml = 0
    pwmr = 0

    r = requests.get("http://192.168.0.138:5000//api/v1/sensors/obstacles").text

    sensori[0] = r[0]
    sensori[1] = r[2]

    if (sensori[0] == "1" and sensori[1] == "1"):
        print("AVANTI")
        pwml = -40
        pwmr = 40
    elif(sensori[1] == "0"):
        print("SINISTRA")
        pwml = 40
        pwmr = 20
    elif(sensori[0] == "0"):
        print("DESTRA")
        pwml = -40
        pwmr = -20

    r = requests.get(f"http://192.168.0.138:5000//api/v1/motors/both?pwml={pwml}&pwmr={pwmr}&tempo={0.2}")
    time.sleep(0.3)