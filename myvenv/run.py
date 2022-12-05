#Archivo para ejecutar la aplicación
from app.routes import app

#Inicializamos el servidor
if __name__ =='__main__':
    #modo debug hace que el script ante los cambios se reinicie
    #puerto en el que escucha el servidor sera el 2000
    app.run(debug=True, port=2000)