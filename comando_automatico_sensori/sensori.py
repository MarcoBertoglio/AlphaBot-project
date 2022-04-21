import flask
from flask import jsonify
import RPi.GPIO as GPIO
import time
from alphabot import AlphaBot
from flask import request
import time

Ab = AlphaBot()
DR = 16
DL = 19

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(DR,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(DL,GPIO.IN,GPIO.PUD_UP)


app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/api/v1/sensors/obstacles', methods=['GET'])
def sensori():
    v = ['','']
    v[0] = GPIO.input(DL)
    v[1] = GPIO.input(DR)

    return (str(v[0]) + " " + str(v[1]))


@app.route('/api/v1/motors/both', methods=['GET'])
def motori():
    pwml = int(request.args['pwml'])
    pwmr = int(request.args['pwmr'])
    tempo = float(request.args['tempo'])
    Ab.set_motor(pwml, pwmr)
        
    return "OK"
    





app.run(debug=True, host='192.168.0.138')