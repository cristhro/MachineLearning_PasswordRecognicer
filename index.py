from datetime import datetime
from os import environ
from flask import Flask, jsonify, request, render_template
from time import time
from pymongo import MongoClient


MONGODB_URI = "mongodb://admin:admin@ds159050.mlab.com:59050/flaskdb"
client = MongoClient(MONGODB_URI)
db = client.get_default_database()

doc_palabras = db.palabras
doc_usuarios = db.doc_usuarios
doc_features = db.features

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def home():
    return render_template(
        'index.html',
        title='App',
        message='autentication',
    )


@app.route('/entrenamiento')
def entrenamiento():
    usuario = 'jesus'
    numPalabra = 0
    palabra = doc_palabras.find_one({'numPalabra': numPalabra})
    numTotalPalabras = doc_palabras.count()
    fin = False

    return render_template(
        'entrenamiento.html',
        title='Entrenamiento',
        year=datetime.now().year,
        message='Teclea las palabras que te aparezcan',
        usuario=usuario,
        palabra=palabra['palabra'],
        t0=time(),
        tiempo=0,
        numPalabra=numPalabra,
        numTotalPalabras=numTotalPalabras,
        fallosCaracter=False,
        falloPalabra=True,
        tiempoError=0,
        t0_error=0,
        fin=fin
    )


@app.route('/autenticacion')
def autenticacion():

    return render_template(
        'autenticacion.html',
        title='Autenticacion',
        year=datetime.now().year,
        message='Teclea la palabra para autenticarte',
        palabra='GATITO',
        t0=time(),
        tiempo=0
    )


@app.route('/getCaracter', methods=['POST'])
def getCaracter():
    usuario = 'Jesus'
    palabra = request.form['palabra']
    palabraLeida = request.form['palabraLeida']
    tiempo = str(time() - float(request.form['t0']))
    ultimoCaracter = palabraLeida[len(palabraLeida) - 1]
    fallosCaracter = False

    objeto = {
        'usuario': usuario,
        'palabra': palabra,
        'palabraLeida': palabraLeida,
        'tiempo': tiempo,
        'caracter': ultimoCaracter,
        'fallosCaracter': fallosCaracter,
        't0': time()
    }
    if not (isValidoUltimoCaracter(palabra, palabraLeida)):
        fallosCaracter = True
        objeto['fallosCaracter'] = fallosCaracter

    doc_features.insert(objeto)

    return jsonify({
        'usuario': usuario,
        'palabra': palabra,
        'palabraLeida': palabraLeida,
        'tiempo': tiempo,
        'caracter': ultimoCaracter,
        'fallosCaracter': fallosCaracter,
        't0': time(),
        'tiempo': tiempo,
        'falloPalabra': False,
        'tiempoError': 0,
        't0_error': time(),
    })


@app.route('/siguiente_palabra', methods=['POST'])
def siguiente_palabra():

    objeto = {}
    usuario = 'Jesus'
    numPalabra = request.form['numPalabra']
    palabras = doc_palabras.find()
    docPalabra = doc_palabras.find_one({'numPalabra': int(numPalabra)})
    palabra = docPalabra['palabra']
    numTotalPalabras = request.form['numTotalPalabras']
    nuevaPalabra = doc_palabras.find_one({'numPalabra': int(numPalabra) + 1})
    palabraLeida = request.form['palabraLeida']
    tiempo = str(time() - float(request.form['t0']))
    t0_error = str(time() - float(request.form['t0_error']))
    tiempoError = str(time() - float(t0_error))
    fin = False

    if(int(numPalabra) == (int(numTotalPalabras) - 1)):
        fin = True

    else:
		if not (mismaPalabra(palabra, palabraLeida)):
			tiempoError = 0
			objeto = {
				'usuario': usuario,
				'palabra': palabra,
				'palabraLeida': palabraLeida,
				'tiempo': tiempo,
				'falloPalabra': True,
				'tiempoError': tiempoError,
				't0_error': t0_error,
				'numPalabra': numPalabra,
				'numTotalPalabras': numTotalPalabras
			}
		else:
			palabra = nuevaPalabra['palabra']
			numPalabra = int(numPalabra) + 1
			t0_error = 0

			objeto = {
			    'usuario': usuario,
			    'palabra': palabra,
			    'palabraLeida': palabraLeida,
			    'tiempo': tiempo,
			    'falloPalabra': False,
			    'tiempoError': tiempoError,
			    't0_error': t0_error,
			    'numPalabra': numPalabra,
			    'numTotalPalabras': numTotalPalabras
			}
    doc_features.insert(objeto)
    return render_template(
        'entrenamiento.html',
        title='Entrenamiento',
        year=datetime.now().year,
        message='Teclea las palabras que te aparezcan',
        usuario=usuario,
        palabra=palabra,
        t0=time(),
        tiempo=0,
        numPalabra=numPalabra,
        numTotalPalabras=numTotalPalabras,
        fallosCaracter=False,
        falloPalabra=True,
        tiempoError=tiempoError,
        t0_error=t0_error,
        fin=fin)


def isValidoUltimoCaracter(palabra, palabraLeida):
    if(len(palabraLeida) <= len(palabra)):
        if(palabra[len(palabraLeida) - 1] == palabraLeida[len(palabraLeida) - 1]):
            return True
        else:
            return False
    else:
        return False


def mismaPalabra(palabra, palabraLeida):
    if(palabra == palabraLeida):
        return True
    else:
        return False


def insertatPalabras(doc):
    doc.insert({'numPalabra': 0, 'palabra': "ROJO"})
    doc.insert({'numPalabra': 1, 'palabra': "PANTALON"})
    doc.insert({'numPalabra': 2, 'palabra': "ZANAHORIA"})
    doc.insert({'numPalabra': 3, 'palabra': "MINERIA DE DATOS"})
    doc.insert({'numPalabra': 4, 'palabra': "CRISTHIANO RONALDO"})
    doc.insert({'numPalabra': 5, 'palabra': "ADIOS"})
    doc.insert({'numPalabra': 6, 'palabra': "GRACIAS"})

# #################### RUN APP #############################

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5000'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT, debug=True)
