import mysql.connector
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np

# Conectar a la base de datos MySQL
db = mysql.connector.connect(
    host="host",          # Nombre del host
    user="usuario",               # Usuario de MySQL
    password="Contraseña",      # Contraseña de MySQL
    database="Tiro_Con_Arco"   # El nombre de la base de datos
)

cursor = db.cursor()

# Obtener el último ID_Entrenamiento de la base de datos
cursor.execute("SELECT MAX(FK_ID_Entrenamiento) FROM Disparo")
ultimo_entrenamiento = cursor.fetchone()[0]

# Obtener los puntos del último entrenamiento
cursor.execute(f"""
    SELECT Puntos
    FROM Disparo
    WHERE FK_ID_Entrenamiento = {ultimo_entrenamiento};
""")
resultados = cursor.fetchall()

# Cerrar la conexión a la base de datos
cursor.close()
db.close()

# Extraer los puntos de los resultados
puntos = [r[0] for r in resultados]

# Definir los colores
colores = {
    'X': '#ffff80',  # Verde claro
    '10': '#ffff80',  # Amarillo claro
    '9': '#ffff80',  # Amarillo claro
    '8': '#ff9999',  # Rojo claro
    '7': '#ff9999',  # Rojo claro
    '6': '#99b3ff',  # Azul claro
    '5': '#99b3ff',  # Azul claro
    '4': '#000000',  # Negro
    '3': '#000000',  # Negro
    '2': '#ffffff',  # Blanco
    '1': '#ffffff',  # Blanco
    'M': '#a0e0a0'   # Verde claro
}

# Contar los puntos
conteo_puntos = Counter(puntos)

# Definir el orden deseado
orden_deseado = ['X', '10', '9', '8', '7', '6', '5', '4', '3', '2', '1', 'M']

# Preparar datos para el gráfico en el orden deseado
etiquetas = []
valores = []
for punto in orden_deseado:
    if punto in conteo_puntos:
        etiquetas.append(f"{punto}")
        valores.append(conteo_puntos[punto])

# Añadir los totales de aciertos y fallos
total_flechas = sum(valores)
total_misses = conteo_puntos.get('M', 0)
total_hits = total_flechas - total_misses

# Crear el gráfico de pastel
fig, ax = plt.subplots(figsize=(10, 7))

wedges, texts, autotexts = ax.pie(
    valores,
    labels=None,  # Se añaden manualmente
    colors=[colores.get(etiqueta, '#cccccc') for etiqueta in etiquetas],
    autopct='',  # No mostrar porcentaje
    startangle=90,
    wedgeprops=dict(width=0.4, edgecolor='w')
)

# Añadir el total de aciertos y fallos en el centro
centre_circle = plt.Circle((0, 0), 0.5, color='white', fc='white')
fig.gca().add_artist(centre_circle)

# Mostrar los totales en el centro
ax.text(
    0, 0,
    f'Total Aciertos\n{total_hits}\nTotal Fallos\n{total_misses}',
    horizontalalignment='center',
    verticalalignment='center',
    fontsize=12,
    bbox=dict(facecolor='white', alpha=0.8)
)

# Añadir etiquetas y valores en el gráfico
for wedge, etiqueta, cantidad in zip(wedges, etiquetas, valores):
    angle = (wedge.theta2 - wedge.theta1) / 2 + wedge.theta1
    angle_rad = np.deg2rad(angle)

    # Coordenadas para las etiquetas fuera del gráfico
    x_text = 1.2 * wedge.r * np.cos(angle_rad)
    y_text = 1.2 * wedge.r * np.sin(angle_rad)

    # Coordenadas para los valores dentro del gráfico
    x_center = 0.8 * wedge.r * np.cos(angle_rad)
    y_center = 0.8 * wedge.r * np.sin(angle_rad)

    # Añadir la etiqueta (punto) fuera del gráfico
    ax.text(
        x_text, y_text,
        etiqueta,
        horizontalalignment='center',
        verticalalignment='center',
        fontsize=10,
        bbox=dict(facecolor='white', edgecolor='None', alpha=0.5)
    )

    # Añadir el valor dentro del segmento
    ax.text(
        x_center, y_center,
        str(cantidad),
        horizontalalignment='center',
        verticalalignment='center',
        fontsize=12,
        color='black'
    )

# Mejorar la apariencia
plt.title('Distribución de Puntos en el Entrenamiento', fontsize=14)

# Guardar la gráfica como PDF
output_pdf_path = r'C:/Users/josma/OneDrive/Documentos/Proyectos/Automatizacion_Registro_Tiro_Con_Arco/Automation Anywhere/Archivos/Distribucion_Flechas.pdf'
plt.savefig(output_pdf_path, format='pdf', bbox_inches='tight')
