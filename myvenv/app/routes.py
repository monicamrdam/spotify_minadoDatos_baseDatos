from flask import Flask
from flask import jsonify

#Creamos la aplicación de servidor
app = Flask(__name__)

#Creamos una ruta de prueba home para testear que el servidor funciona
@app.route('/home')
def home():
    return '!Bienvenido!'


