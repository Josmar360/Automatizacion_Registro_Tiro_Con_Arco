import mysql.connector
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.table import Table

# Definir los colores
colores = {
    'X': '#ffff80',  # Amarillo claro
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

# Conexión a la base de datos MySQL
db = mysql.connector.connect(
    host="localhost",          # Cambia esto según sea necesario
    user="root",               # Tu usuario de MySQL
    password="Sarinha_3",      # Tu contraseña de MySQL
    database="Tiro_Con_Arco"   # El nombre de tu base de datos
)

cursor = db.cursor()

# Obtener el último valor de ID_Entrenamiento
cursor.execute("SELECT MAX(ID_Entrenamiento) FROM Disparo;")
ultimo_id_entrenamiento = cursor.fetchone()[0]

# Consulta SQL para obtener los datos necesarios
query = f"""
SELECT Serie, Tanda, X, Y, Puntos
FROM Disparo
WHERE ID_Entrenamiento = {ultimo_id_entrenamiento}
ORDER BY Serie, Tanda, ID_Disparo;
"""
cursor.execute(query)
resultados = cursor.fetchall()

# Cerrar la conexión a la base de datos
cursor.close()
db.close()

# Convertir los resultados a un DataFrame de pandas para facilitar la manipulación
df = pd.DataFrame(resultados, columns=['Serie', 'Tanda', 'X', 'Y', 'Puntos'])

# Convertir 'M' a 0 en la columna 'Puntos' para el cálculo
df['Puntos'] = df['Puntos'].apply(
    lambda x: 0 if x == 'M' else (10 if x == 'X' else int(x)))

# Calcular la precisión


def calcular_precision(data):
    # Asumimos que cada flecha tiene un valor máximo de 10 puntos
    puntos_totales = len(data) * 10
    puntos_obtenidos = sum(data)
    return (puntos_obtenidos / puntos_totales) * 100


# Preparar los datos para la tabla
# Agrupar los datos por Serie y Tanda
agrupado = df.groupby(['Serie', 'Tanda'])

# Crear la figura y los ejes
fig, ax = plt.subplots(figsize=(14, 10))
ax.set_axis_off()

# Crear la tabla usando matplotlib Table
tabla = Table(ax, bbox=[0, 0, 1, 1])

# Añadir el título
titulo = 'Conteo por Serie'
ax.set_title(titulo, fontsize=14, weight='bold')

# Encabezados de las columnas
columnas = ['Serie', 'Tanda', '1', '2', '3', '4', '5', '6',
            '7', '8', 'Puntuación', 'Acumulado', 'Precisión (%)']
n_columnas = len(columnas)

# Añadir encabezados
for i, col in enumerate(columnas):
    cell = tabla.add_cell(0, i, width=0.1, height=0.1, text=col,
                          loc='center', edgecolor='black', facecolor='lightgrey')
    cell.set_fontsize(10)

# Añadir filas de datos
for j, (clave, data) in enumerate(agrupado):
    serie, tanda = clave
    flechas = data['Puntos'].tolist()
    # Ordenar flechas de mayor a menor
    flechas_ordenadas = sorted(flechas, reverse=True)

    # Rellenar con ceros si hay menos de 8 flechas
    while len(flechas_ordenadas) < 8:
        flechas_ordenadas.append(0)

    # Calcular puntuación total
    puntuacion = sum(flechas)
    acumulado = df[(df['Serie'] == serie) & (
        df['Tanda'] <= tanda)]['Puntos'].sum()  # Acumulado
    precision = calcular_precision(flechas)  # Calcular precisión

    fila = [serie, tanda] + flechas_ordenadas[:8] + \
        [puntuacion, acumulado, round(precision, 2)]
    for i, valor in enumerate(fila):
        # Aplicar color solo a las flechas disparadas
        if i >= 2 and i < 10:  # Solo las celdas correspondientes a flechas
            color = colores.get(str(valor), 'white')
            text_color = 'white' if color == '#000000' else 'black'
            cell = tabla.add_cell(j + 1, i, width=0.1, height=0.1, text=str(
                valor), loc='center', edgecolor='black', facecolor=color)
            cell.set_fontsize(10)
            cell.set_text_props(color=text_color)
        else:  # Para columnas como Serie, Tanda, Puntuación y Acumulado
            cell = tabla.add_cell(j + 1, i, width=0.1, height=0.1, text=str(
                valor), loc='center', edgecolor='black', facecolor='white')
            cell.set_fontsize(10)

# Añadir fila de sumatoria
total_puntos = df['Puntos'].sum()
total_flechas_ordenadas = sorted(df['Puntos'].tolist(), reverse=True)
# Tomar solo los últimos tres valores
last_three_flechas = total_flechas_ordenadas[:3]

# Crear fila con valores vacíos para las flechas, excepto los últimos tres
sumatoria_fila = ['Total', ''] + [''] * 8 + [total_puntos,
                                             total_puntos, round(calcular_precision(df['Puntos'].tolist()), 2)]

for i, valor in enumerate(sumatoria_fila):
    if i >= 10 and i < 10:  # Solo las celdas correspondientes a flechas
        if i - 2 < len(last_three_flechas):  # Mostrar solo los últimos tres valores
            color = colores.get(str(last_three_flechas[i - 2]), 'white')
            text_color = 'white' if color == '#000000' else 'black'
            cell = tabla.add_cell(len(agrupado) + 1, i, width=0.1, height=0.1, text=str(
                last_three_flechas[i - 2]), loc='center', edgecolor='black', facecolor=color)
            cell.set_fontsize(10)
            cell.set_text_props(color=text_color)
        else:
            cell = tabla.add_cell(len(agrupado) + 1, i, width=0.1, height=0.1,
                                  text='', loc='center', edgecolor='black', facecolor='white')
            cell.set_fontsize(10)
    else:  # Para columnas como Serie, Tanda, Puntuación y Acumulado
        cell = tabla.add_cell(len(agrupado) + 1, i, width=0.1, height=0.1, text=str(
            valor), loc='center', edgecolor='black', facecolor='lightgrey')
        cell.set_fontsize(10)

# Ajustar el tamaño de las celdas
tabla.auto_set_font_size(False)
tabla.set_fontsize(8)

# Añadir la tabla al gráfico
ax.add_table(tabla)

# Mostrar la tabla
plt.show()

# Ruta donde se guardará la imagen
ruta_guardado = r'C:\Users\josma\OneDrive\Documentos\Proyectos\Automation Anywhere 360\Tiro Con Arco\Recursos\Precision.png'

# Guardar la imagen
fig.savefig(ruta_guardado, bbox_inches='tight')

print(f'La imagen se ha guardado en: {ruta_guardado}')
