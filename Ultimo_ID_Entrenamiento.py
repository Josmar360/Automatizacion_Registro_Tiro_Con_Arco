from flask import Flask, render_template_string
import mysql.connector
import time
import subprocess
import threading

# Conectar a la base de datos MySQL
db = mysql.connector.connect(
    host="localhost",          # Nombre del host
    user="root",               # Usuario de MySQL
    password="Sarinha_3",      # Contraseña de MySQL
    database="Tiro_Con_Arco"   # El nombre de la base de datos
)

cursor = db.cursor()

# Obtener el máximo valor de Tanda en el último ID_Entrenamiento
cursor.execute("""
    SELECT MAX(Tanda) AS MaxTanda
    FROM Disparo
    WHERE ID_Entrenamiento = (SELECT MAX(ID_Entrenamiento) FROM Disparo);
""")
max_tanda = cursor.fetchone()[0]

# Cerrar la conexión a la base de datos
cursor.close()
db.close()

# Crear una aplicación Flask
app = Flask(__name__)

# Página principal que muestra el valor de Tanda en dos tablas separadas
@app.route('/')
def show_tanda():
    # HTML con dos tablas: una para el nombre de la tabla y otra para el valor máximo
    html = '''
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Valor de Tanda</title>
        <style>
            table {
                border-collapse: collapse;
                width: 50%;
                margin: 50px auto;
            }
            th, td {
                border: 1px solid #ddd;
                padding: 8px;
                text-align: center;
            }
            th {
                background-color: #f2f2f2;
            }
            h2 {
                text-align: center;
            }
        </style>
    </head>
    <body>
        <h2>Valor de Tanda</h2>
        <!-- Primera tabla con el nombre de la tabla -->
        <table>
            <thead>
                <tr>
                    <th>Número máximo de series</th>
                </tr>
            </thead>
        </table>
        
        <!-- Segunda tabla con el valor máximo -->
        <table>
            <thead>
                <tr>
                    <td>{{ max_tanda }}</td>
                </tr>
            </thead>
        </table>
    </body>
    </html>
    '''

    return render_template_string(html, max_tanda=max_tanda)

def open_browser():
    # Esperar a que el servidor Flask esté en funcionamiento
    time.sleep(5)  # Aumenta el tiempo de espera para asegurarse de que el servidor Flask esté listo
    
    # Ruta al ejecutable de Chrome en Windows
    chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
    url = 'http://127.0.0.1:5000/'
    
    # Usar subprocess para abrir una nueva ventana
    subprocess.Popen([chrome_path, '--new-window', url], shell=True)

if __name__ == '__main__':
    # Ejecutar la aplicación Flask
    flask_thread = threading.Thread(target=lambda: app.run(debug=False, use_reloader=False))
    flask_thread.start()

    # Abrir el navegador
    open_browser()
