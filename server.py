import socket as sck
import threading as thr
import time
import RPi.GPIO as GPIO
import sqlite3

#classe alphabot per far muovere il robot
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


#classe thread
class Classe_Thread(thr.Thread):
    #funzione che si avvia alla creazione della classe
    def __init__(self, connessione, indrizzo, alphabot):
        thr.Thread.__init__(self)   #costruttore super (java)
        self.connessione = connessione
        self.indrizzo = indrizzo
        self.alphabot = alphabot
        self.running = True

    #funzione che si avvia con il comando start()
    def run(self):
        while self.running:
            messaggio = self.connessione.recv(4096).decode()

            #collegamento con il database
            database = sqlite3.connect('database.db')
            #creazione del cursore
            cursore = database.cursor()

            #interrogazione del database per estrarre il movimento complesso
            movimento = str(cursore.execute(f"SELECT sequenza FROM Movimenti WHERE movimento = '{messaggio}'").fetchall())
            movimento = movimento[3:-4]

            if len(movimento) != 0:
                #esecuzione del movimento complesso
                print(movimento)

                movimento = movimento.split(',')

                for i in movimento:
                    if i[0] == "W":
                        self.alphabot.forward()
                        time.sleep(int(i[1:]) / 1000)
                        self.alphabot.stop()
                    
                    if i[0] == "D":
                        self.alphabot.right()
                        time.sleep(int(i[1:]) / 1000)
                        self.alphabot.stop()

                    if i[0] == "A":
                        self.alphabot.left()
                        time.sleep(int(i[1:]) / 1000)
                        self.alphabot.stop()

                    if i[0] == "S":
                        self.alphabot.backward()
                        time.sleep(int(i[1:]) / 1000)
                        self.alphabot.stop()
            else:
                #esecuzione del movimento base
                if messaggio[0] == "W":
                        self.alphabot.forward()
                        time.sleep(int(messaggio[1:]) / 1000)
                        self.alphabot.stop()
    
                elif messaggio[0] == "D":
                    self.alphabot.right()
                    time.sleep(int(messaggio[1:]) / 1000)
                    self.alphabot.stop()

                elif messaggio[0] == "A":
                    self.alphabot.left()
                    time.sleep(int(messaggio[1:]) / 1000)
                    self.alphabot.stop()

                elif messaggio[0] == "S":
                    self.alphabot.backward()
                    time.sleep(int(messaggio[1:]) / 1000)
                    self.alphabot.stop()
                
                elif messaggio == "R":
                    self.alphabot.stop()
                
                else:
                    messaggio = ""
                
                print(messaggio)
            
            self.connessione.sendall("OK".encode())


def main():
    #creazione del socket e listen
    s = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
    s.bind(('192.168.0.129', 5000))
    s.listen()

    connessione, indrizzo = s.accept()
    
    #creazione dell'oggetto alphabot per far muovere il robot
    Ab = AlphaBot()

    client = Classe_Thread(connessione, indrizzo, Ab)
    client.start()

    

    s.close()

main()
