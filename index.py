from datetime import datetime
from os import environ
from flask import Flask, jsonify, request, render_template, make_response
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
        t0_palabra=time(),
        tiempoPalabra=0,
        tiempo=0,
        numPalabra=numPalabra,
        numTotalPalabras=numTotalPalabras,
        fallosCaracter=False,
        hayErrPalabra=False,
        tiempoErrPalabra=0,
        t0_error=0,
        fin=fin,

    )



@app.route('/autenticacion',methods = ["GET", "POST"])
def autenticacion():

    palabraLeida = ""
    palabra = "MESA"
    usuario = 'Jesus'
    t0 = time()
    tiempo = 0
    t0_error = 0
    tiempoErrPalabra = 0
    t0_palabra = time()
    tiempoPalabra = 0
    hayErrPalabra = False
    fin = False

    if request.method == 'POST':
        usuario = 'Jesus'
        palabraLeida = request.form['palabraLeida']
        tiempo = str(time() - float(request.form['t0']))
        t0_error = float(request.form['t0_error'])
        t0_palabra = float(request.form['t0_palabra'])

        if (mismaPalabra(palabra, palabraLeida)):
                fin = True
                if  (t0_error != 0):
                    tiempoErrPalabra = str(time() - t0_error)
                t0_error = 0
                tiempoPalabra = str(time() - t0_palabra)
                t0_palabra = time()
        else:
            if  (t0_error != 0):
                tiempoErrPalabra = time() - t0_error
                tiempoErrPalabra = tiempoErrPalabra + (time() - t0_error)

            t0_error = time()
            hayErrPalabra = True


    return render_template(
        'autenticacion.html',
        title='Autenticacion',
        year=datetime.now().year,
        message='Teclea la palabra para autenticarte',
        palabra= palabra,
        usuario=usuario,
        t0=t0,
        tiempo=0,
        fallosCaracter=False,
        hayErrPalabra=hayErrPalabra,
        tiempoErrPalabra=tiempoErrPalabra,
        t0_error=t0_error,
        t0_palabra=t0_palabra,
        tiempoPalabra=tiempoPalabra,
        fin=fin)



@app.route('/getCaracter', methods=['POST'])
def getCaracter():
    usuario = 'Jesus'
    palabra = request.form['palabra']
    palabraLeida = request.form['palabraLeida']
    tiempo = str(time() - float(request.form['t0']))
    ultimoCaracter = ""
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
    else:
        ultimoCaracter = palabraLeida[len(palabraLeida) - 1]

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
        'hayErrPalabra': False,
        'tiempoErrPalabra': 0,
        't0_error': time(),

    })


@app.route('/siguiente_palabra', methods=['POST'])
def siguiente_palabra():
    objeto = {}
    numPalabra = int(request.form['numPalabra'])
    numTotalPalabras = request.form['numTotalPalabras']
    usuario = 'Jesus'
    palabras = doc_palabras.find()
    docPalabra = doc_palabras.find_one({'numPalabra': int(numPalabra)})
    palabra = docPalabra['palabra']
    nuevaPalabra = ""
    palabraLeida = request.form['palabraLeida']
    tiempo = str(time() - float(request.form['t0']))
    t0_error = float(request.form['t0_error'])
    tiempoErrPalabra = 0
    t0_palabra = float(request.form['t0_palabra'])
    tiempoPalabra = 0

    hayErrPalabra = False
    fin = False

    if(int(numPalabra) == (int(numTotalPalabras) - 1)):
        fin = True
    else :
        docNuevaPalabra = doc_palabras.find_one({'numPalabra': int(numPalabra) + 1})
        nuevaPalabra  = docNuevaPalabra["palabra"]
        if (mismaPalabra(palabra, palabraLeida)):
            if  (t0_error != 0):
                tiempoErrPalabra = str(time() - t0_error)
            t0_error = 0
            tiempoPalabra = str(time() - t0_palabra)
            t0_palabra = time()
            numPalabra = int(numPalabra) + 1
        else:
            if  (t0_error != 0):
                tiempoErrPalabra = time() - t0_error
                tiempoErrPalabra = tiempoErrPalabra + (time() - t0_error)

            t0_error = time()
            hayErrPalabra = True
            nuevaPalabra = palabra
    # Guardamos el ojeto en la BD
    doc_features.insert({
                'usuario': usuario,
                'palabra': palabra,
                'palabraLeida': palabraLeida,
                'tiempo': tiempo,
                'hayErrPalabra': hayErrPalabra,
                'tiempoErrPalabra': tiempoErrPalabra,
                'numPalabra': numPalabra,
                'numTotalPalabras': numTotalPalabras,
                'tiempoPalabra':tiempoPalabra,
                'tamPalabra': len(palabra)
            })



    return render_template(
        'entrenamiento.html',
        title='Entrenamiento',
        year=datetime.now().year,
        message='Teclea las palabras que te aparezcan',
        usuario=usuario,
        palabra=nuevaPalabra,
        t0=time(),
        tiempo=0,
        numPalabra=numPalabra,
        numTotalPalabras=numTotalPalabras,
        fallosCaracter=False,
        hayErrPalabra=hayErrPalabra,
        tiempoErrPalabra=tiempoErrPalabra,
        t0_error=t0_error,
        t0_palabra=t0_palabra,
        tiempoPalabra=tiempoPalabra,
        fin=fin)


def isValidoUltimoCaracter(palabra, palabraLeida):
    if(len(palabraLeida) <= len(palabra) and len(palabraLeida) > 0):
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


@app.route('/list',methods = ["GET"])
def list():
    ops = doc_features.find()
    ss = ""
    for o in ops:
      try:
        ss += o["usuario"] 
        ss += ";" 
        ss += o["palabra"] 
        ss += ";" 
        ss += o["palabraLeida"] 
        ss += ";" 
        ss += o["tiempo"] 
        ss += ";" 
        ss += o["hayErrPalabra"] 
        ss += ";" 
        ss += o["tiempoErrPalabra"] 
        ss += ";" 
        ss += o["numPalabra"] 
        ss += ";" 
        ss += o["palabraLeida"] 
        ss += ";" 
        ss += o["tiempoPalabra"] 
        ss += ";" 
        ss += o["tamPalabra"]
        ss += ";"  
        ss += "\n"
      except Exception as e:
        pass
    output = make_response(ss)
    output.headers["Content-Disposition"] = "attachment; filename=export.csv"
    output.headers["Content-type"] = "text/csv"
    return output



# #################### RUN APP #############################

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'ec2-52-205-165-220.compute-1.amazonaws.com')
    try:
        PORT = int(environ.get('SERVER_PORT', '8000'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT, debug=True)
