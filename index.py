from datetime import datetime
from flask import render_template
from os import environ
from flask import Flask, jsonify,request, make_response
import sys
from random import randint
from time import time
import pymongo
import cPickle
from pymongo import MongoClient


MONGODB_URI =  "mongodb://admin:admin@ds159050.mlab.com:59050/flaskdb"
client = MongoClient(MONGODB_URI)
db = client.get_default_database()
collection = db.cristhian

app = Flask(__name__)

@app.route('/')
@app.route('/home')

def home():
    return render_template(
        'index.html',
        title='Pagina principal',
        year=datetime.now().year,
    )

@app.route('/entrenamiento')
def entrenamiento():
    return render_template(
        'entrenamiento.html',
        title='Entrenamiento',
        year=datetime.now().year,
        message='Teclea las palabras que te aparezcan',
        palabras=["ROJO","PERRO","PANTALON","CRISTHIANO RONALDO","MANANA POR LA MANANA", "MINERIA DE DATOS", "ADIOS","GRACIAS"]
    )

@app.route('/autenticacion')
def autenticacion():
    return render_template(
        'autenticacion.html',
        title='Autenticacion',
        year=datetime.now().year,
        message='Teclea la palabra para autenticarte',
        palabra='GATITO'
    )

@app.route('/getCaracter', methods=['POST'])
def getCaracter():
    ss = request.form['keyword']
    ss += "\n"
    print('hola mundo 2  ')
 
    collection.insert({'caracter': request.form['keyword'], 'tiempo': str(time())})
    return jsonify({'caracter': request.form['keyword']})

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(debug=True)