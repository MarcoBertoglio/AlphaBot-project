from flask import Flask, render_template, request, make_response, redirect, url_for
import sqlite3
from datetime import datetime
import RPi.GPIO as GPIO

#Creazione della classe AlphaBot per muovere il Bot
class AlphaBot(object):
    def __init__(self, in1=13, in2=12, ena=6, in3=21, in4=20, enb=26):
        self.IN1 = in1
        self.IN2 = in2
        self.IN3 = in3
        self.IN4 = in4
        self.ENA = ena
        self.ENB = enb
        self.PA  = 50
        self.PB  = 48

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.IN1, GPIO.OUT)
        GPIO.setup(self.IN2, GPIO.OUT)
        GPIO.setup(self.IN3, GPIO.OUT)
        GPIO.setup(self.IN4, GPIO.OUT)
        GPIO.setup(self.ENA, GPIO.OUT)
        GPIO.setup(self.ENB, GPIO.OUT)
        self.PWMA = GPIO.PWM(self.ENA,500)
        self.PWMB = GPIO.PWM(self.ENB,500)
        self.PWMA.start(self.PA)
        self.PWMB.start(self.PB)
        self.stop()

    def forward(self):
        self.PWMA.ChangeDutyCycle(self.PA)
        self.PWMB.ChangeDutyCycle(self.PB)
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.HIGH)

    def stop(self):
        self.PWMA.ChangeDutyCycle(0)
        self.PWMB.ChangeDutyCycle(0)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.LOW)

    def backward(self):
        self.PWMA.ChangeDutyCycle(self.PA)
        self.PWMB.ChangeDutyCycle(self.PB)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)

    def left(self, speed=30):
        self.PWMA.ChangeDutyCycle(speed)
        self.PWMB.ChangeDutyCycle(speed)
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)

    def right(self, speed=30):
        self.PWMA.ChangeDutyCycle(speed)
        self.PWMB.ChangeDutyCycle(speed)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.HIGH)
        
    def set_pwm_a(self, value):
        self.PA = value
        self.PWMA.ChangeDutyCycle(self.PA)

    def set_pwm_b(self, value):
        self.PB = value
        self.PWMB.ChangeDutyCycle(self.PB)    
        
    def set_motor(self, left, right):
        if (right >= 0) and (right <= 100):
            GPIO.output(self.IN1, GPIO.HIGH)
            GPIO.output(self.IN2, GPIO.LOW)
            self.PWMA.ChangeDutyCycle(right)
        elif (right < 0) and (right >= -100):
            GPIO.output(self.IN1, GPIO.LOW)
            GPIO.output(self.IN2, GPIO.HIGH)
            self.PWMA.ChangeDutyCycle(0 - right)
        if (left >= 0) and (left <= 100):
            GPIO.output(self.IN3, GPIO.HIGH)
            GPIO.output(self.IN4, GPIO.LOW)
            self.PWMB.ChangeDutyCycle(left)
        elif (left < 0) and (left >= -100):
            GPIO.output(self.IN3, GPIO.LOW)
            GPIO.output(self.IN4, GPIO.HIGH)
            self.PWMB.ChangeDutyCycle(0 - left)

Ab = AlphaBot()

#Flask
app = Flask(__name__)
@app.route("/", methods=['GET', 'POST'])

#Pagina di login per accedere ai comandi del Robot
def index():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    
    #Se l'username e la password si trovano all'interno del DB, allora l'utente viene reindirizzato alla pagina del controllo del Robot
    if validate(username, password):
      resp = make_response(redirect(url_for('controlloRobot')))
      #Salvo l'username all'interno dei Cookie
      resp.set_cookie('username', username)
      print(request.cookies.get('username'))
      return resp
  return render_template('login.html')
  
#Funzione che controlla se l'username e la password sono all'interno del DB
def validate(username, password):
    con = sqlite3.connect('C:/Users/GINOM/Dropbox/Scuola/TPSIT/Esercizi/HTTP/flask_examples/cookies/db.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM Users")
    rows = cur.fetchall()
    for row in rows:
        if row[0]==username and row[1] == password:
            return True
    
    return False

#Pagina di controllo del Robot
@app.route(f'/controlloRobot', methods=['GET', 'POST'])
def controlloRobot():
    #Connessione con il DB
    con = sqlite3.connect('C:/Users/GINOM/Dropbox/Scuola/TPSIT/Esercizi/HTTP/flask_examples/cookies/db.db')
    cur = con.cursor()

    if request.method == 'POST':
        #Data e ora attuale grazie alla libreria DATETIME
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        
        if request.form.get('avanti') == 'avanti':
            print("Avanti")
            #Funzione che fa muovere il robot
            Ab.forward()
            #Salvo il movimento, l'username e la data all'interno del DB, in pratica faccio uno storico dei movimenti ordinati dall'utente
            cur.execute(f"INSERT INTO comandi (utente, comando, data) VALUES ('{request.cookies.get('username')}','avanti','{dt_string}')")
        elif  request.form.get('indietro') == 'indietro':
            print("Indietro")
            Ab.backward()
            cur.execute(f"INSERT INTO comandi (utente, comando, data) VALUES ('{request.cookies.get('username')}','indietro','{dt_string}')")
        elif  request.form.get('sinistra') == 'sinistra':
            print("Sinistra")
            Ab.left()
            cur.execute(f"INSERT INTO comandi (utente, comando, data) VALUES ('{request.cookies.get('username')}','sinistra','{dt_string}')")
        elif  request.form.get('destra') == 'destra':
            print("Destra")
            Ab.right()
            cur.execute(f"INSERT INTO comandi (utente, comando, data) VALUES ('{request.cookies.get('username')}','destra','{dt_string}')")
        elif  request.form.get('stop') == 'stop':
            print("Stop")
            Ab.stop()
            cur.execute(f"INSERT INTO comandi (utente, comando, data) VALUES ('{request.cookies.get('username')}','stop','{dt_string}')")
    
    #Salvo le modifiche del DB
    con.commit()
    return render_template("controlloRobot.html")


app.run(debug=True, host='localhost')