from flask import Flask, render_template, request, make_response, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)
@app.route("/", methods=['GET', 'POST'])

def index():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']

    if validate(username, password):
      resp = make_response(redirect(url_for('controlloRobot')))
      resp.set_cookie('username', username)
      print(request.cookies.get('username'))
      return resp
  return render_template('login.html')
  

def validate(username, password):
    con = sqlite3.connect('C:/Users/GINOM/Dropbox/Scuola/TPSIT/Esercizi/HTTP/flask_examples/cookies/db.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM Users")
    rows = cur.fetchall()
    for row in rows:
        if row[0]==username and row[1] == password:
            return True
    
    return False

@app.route(f'/controlloRobot', methods=['GET', 'POST'])
def controlloRobot():
    con = sqlite3.connect('C:/Users/GINOM/Dropbox/Scuola/TPSIT/Esercizi/HTTP/flask_examples/cookies/db.db')
    cur = con.cursor()

    if request.method == 'POST':
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

        if request.form.get('avanti') == 'avanti':
            print("Avanti")
            cur.execute(f"INSERT INTO comandi (utente, comando, data) VALUES ('{request.cookies.get('username')}','avanti','{dt_string}')")
        elif  request.form.get('indietro') == 'indietro':
            print("Indietro")
            cur.execute(f"INSERT INTO comandi (utente, comando, data) VALUES ('{request.cookies.get('username')}','indietro','{dt_string}')")
        elif  request.form.get('sinistra') == 'sinistra':
            print("Sinistra")
            cur.execute(f"INSERT INTO comandi (utente, comando, data) VALUES ('{request.cookies.get('username')}','sinistra','{dt_string}')")
        elif  request.form.get('destra') == 'destra':
            print("Destra")
            cur.execute(f"INSERT INTO comandi (utente, comando, data) VALUES ('{request.cookies.get('username')}','destra','{dt_string}')")
        elif  request.form.get('stop') == 'stop':
            print("Stop")
            cur.execute(f"INSERT INTO comandi (utente, comando, data) VALUES ('{request.cookies.get('username')}','stop','{dt_string}')")

    con.commit()
    return render_template("controlloRobot.html")


app.run(debug=True, host='localhost')