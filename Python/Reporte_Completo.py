from collections import Counter
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.table import Table
import itertools
import numpy as np

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
    'M': '#000000'   # Verde claro
}

# Conectar a la base de datos MySQL
db = mysql.connector.connect(
    host="host",          # Nombre del host
    user="usuario",               # Usuario de MySQL
    password="contraseña",      # Contraseña de MySQL
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

# Extraer los puntos de los resultados
puntos = [r[0] for r in resultados]

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

# Crear el PDF donde se agregará todo
with PdfPages('C:/Users/josma/OneDrive/Documentos/Proyectos/Automatizacion_Registro_Tiro_Con_Arco/Automation Anywhere/Documentos/Reporte_Tiro_Con_Arco.pdf') as pdf:

    # Primero el gráfico de distribución de puntos
    fig, ax = plt.subplots(figsize=(10, 7))

    wedges, texts, autotexts = ax.pie(
        valores,
        labels=None,
        colors=[colores.get(etiqueta, '#cccccc') for etiqueta in etiquetas],
        autopct='',
        startangle=90,
        wedgeprops=dict(width=0.4, edgecolor='w')
    )

    centre_circle = plt.Circle((0, 0), 0.5, color='white', fc='white')
    fig.gca().add_artist(centre_circle)

    ax.text(
        0, 0,
        f'Total Aciertos\n{total_hits}\nTotal Fallos\n{total_misses}',
        horizontalalignment='center',
        verticalalignment='center',
        fontsize=12,
        bbox=dict(facecolor='white', alpha=0.8)
    )

    for wedge, etiqueta, cantidad in zip(wedges, etiquetas, valores):
        angle = (wedge.theta2 - wedge.theta1) / 2 + wedge.theta1
        angle_rad = np.deg2rad(angle)

        x_text = 1.2 * wedge.r * np.cos(angle_rad)
        y_text = 1.2 * wedge.r * np.sin(angle_rad)

        x_center = 0.8 * wedge.r * np.cos(angle_rad)
        y_center = 0.8 * wedge.r * np.sin(angle_rad)

        ax.text(
            x_text, y_text,
            etiqueta,
            horizontalalignment='center',
            verticalalignment='center',
            fontsize=10,
            bbox=dict(facecolor='white', edgecolor='None', alpha=0.5)
        )

        # Ajustar color del texto para "M", "3", y "4"
        text_color = 'white' if etiqueta in ['M', '3', '4'] else 'black'

        ax.text(
            x_center, y_center,
            str(cantidad),
            horizontalalignment='center',
            verticalalignment='center',
            fontsize=12,
            color=text_color
        )

    plt.title('Distribución de Puntos en el Entrenamiento', fontsize=14)
    pdf.savefig(fig)
    plt.close(fig)

    # Segundo: Tabla con los disparos por serie y tanda
    query = f"""
    SELECT Serie, Tanda, X, Y, Puntos
    FROM Disparo
    WHERE FK_ID_Entrenamiento = {ultimo_entrenamiento}
    ORDER BY Serie, Tanda, PK_ID_Disparo;
    """
    cursor.execute(query)
    resultados = cursor.fetchall()

    df = pd.DataFrame(resultados, columns=[
                      'Serie', 'Tanda', 'X', 'Y', 'Puntos'])

    # No convertir "X" a "10", mantén "X" tal cual
    df['Puntos'] = df['Puntos'].apply(lambda x: 0 if x == 'M' else x)

    def calcular_precision(data):
        puntos_totales = len(data) * 10
        puntos_obtenidos = sum([10 if x == 'X' else (
            0 if x == 'M' else int(x)) for x in data])
        return (puntos_obtenidos / puntos_totales) * 100

    # Crear la tabla de resultados
    series_unicas = df['Serie'].unique()

    for serie in series_unicas:
        df_serie = df[df['Serie'] == serie]
        agrupado = df_serie.groupby(['Serie', 'Tanda'])

        fig, ax = plt.subplots(figsize=(14, 10))
        ax.set_axis_off()
        tabla = Table(ax, bbox=[0, 0, 1, 1])

        ax.set_title(f'Serie {serie}', fontsize=14, weight='bold')
        max_flechas = df_serie.groupby('Tanda')['Puntos'].count().max()
        columnas = ['Serie', 'Tanda'] + [str(i) for i in range(1, max_flechas + 1)] + [
            'Puntuación', 'Acumulado', 'Precisión (%)']

        # Añadir encabezados de columna
        for i, col in enumerate(columnas):
            cell = tabla.add_cell(0, i, width=0.1, height=0.1, text=col,
                                  loc='center', edgecolor='black', facecolor='lightgrey')
            cell.set_fontsize(10)

        # Añadir filas de datos
        for j, (clave, data) in enumerate(agrupado):
            serie, tanda = clave
            flechas = data['Puntos'].tolist()
            flechas_ordenadas = sorted(flechas, key=lambda x: 11 if x == 'X' else (
                0 if x == 'M' else int(x)), reverse=True)
            while len(flechas_ordenadas) < max_flechas:
                flechas_ordenadas.append(0)

            puntuacion = sum([10 if x == 'X' else (
                0 if x == 'M' else int(x)) for x in flechas])
            acumulado = df_serie[df_serie['Tanda'] <= tanda]['Puntos'].apply(
                lambda x: 10 if x == 'X' else (0 if x == 'M' else int(x))).sum()
            precision = calcular_precision(flechas)

            fila = [serie, tanda] + flechas_ordenadas[:max_flechas] + [
                puntuacion, acumulado, round(precision, 2)]

            for i, valor in enumerate(fila):
                if i >= 2 and i < (max_flechas + 2):
                    display_value = 'M' if valor == 0 else valor
                    color = colores.get(str(display_value), 'white')
                    text_color = 'white' if color == '#000000' else 'black'
                    cell = tabla.add_cell(j + 1, i, width=0.1, height=0.1, text=str(
                        display_value), loc='center', edgecolor='black', facecolor=color)
                    cell.set_text_props(color=text_color)
                else:
                    cell = tabla.add_cell(j + 1, i, width=0.1, height=0.1, text=str(
                        valor), loc='center', edgecolor='black', facecolor='white')
                    cell.set_fontsize(10)

        # Añadir fila de sumatoria total
        total_puntos = df_serie['Puntos'].apply(
            lambda x: 10 if x == 'X' else (0 if x == 'M' else int(x))).sum()
        sumatoria_fila = ['Total', ''] + [''] * max_flechas + [total_puntos,
                                                               total_puntos, round(calcular_precision(df_serie['Puntos'].tolist()), 2)]

        for i, valor in enumerate(sumatoria_fila):
            color = 'lightgrey'  # Color de fondo gris para toda la fila
            text_color = 'white' if valor in ['M', '3', '4', 'X'] else 'black'
            cell = tabla.add_cell(len(agrupado) + 1, i, width=0.1, height=0.1, text=str(
                valor), loc='center', edgecolor='black', facecolor=color)
            cell.set_fontsize(10)
            cell.set_text_props(color=text_color)

        # Agregar la tabla al eje y guardar la figura
        ax.add_table(tabla)
        pdf.savefig(fig)
        plt.close(fig)

    # Tercer: Gráficos de impactos
    cursor.execute(f"""
        SELECT DISTINCT Serie, Tanda
        FROM Disparo
        WHERE FK_ID_Entrenamiento = {ultimo_entrenamiento}
        ORDER BY Serie, Tanda
    """)
    serie_tanda_combinaciones = cursor.fetchall()

    colores = itertools.cycle(['darkred', 'darkblue', 'darkgreen', 'darkorange',
                               'purple', 'darkviolet', 'darkcyan', 'saddlebrown',
                               'black', 'darkslategray'])

    for serie, tanda in serie_tanda_combinaciones:
        query = f"""
        SELECT FK_ID_Entrenamiento, Serie, Tanda, X, Y, Puntos
        FROM Disparo
        WHERE FK_ID_Entrenamiento = {ultimo_entrenamiento} AND Serie = {serie} AND Tanda = {tanda}
        ORDER BY FK_ID_Entrenamiento;
        """
        cursor.execute(query)
        resultados = cursor.fetchall()

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.set_xlim(-1.1, 1.1)
        ax.set_ylim(-1.1, 1.1)
        ax.set_title(f"Serie {serie} - Tanda {tanda}")
        ax.set_xlabel("X (Coordenadas)")
        ax.set_ylabel("Y (Coordenadas)")
        ax.invert_yaxis()
        ax.set_aspect('equal')

        circulos = [
            (1.0, '#f3f4f6'),  # Blanco pastel
            (0.9, '#f3f4f6'),
            (0.8, '#d3d3d3'),  # Negro pastel
            (0.7, '#d3d3d3'),
            (0.6, '#a6c8ff'),  # Azul pastel
            (0.5, '#a6c8ff'),
            (0.4, '#ffb3b3'),  # Rojo pastel
            (0.3, '#ffb3b3'),
            (0.2, '#fff1b0'),  # Amarillo pastel
            (0.1, '#fff1b0'),
            (0.05, '#fff1b0')
        ]
        for radio, color in circulos:
            ax.add_patch(plt.Circle((0, 0), radio, color=color,
                         ec='black', linewidth=1.5, fill=True, alpha=0.8))

        disparos = []
        disparos_colores = {}

        for frame, disparo in enumerate(resultados):
            x, y = disparo[3], disparo[4]
            puntos = disparo[5]

            if puntos == 10:
                puntos_legenda = 'X'
            elif puntos == 0:
                puntos_legenda = 'M'
            else:
                puntos_legenda = str(puntos)

            color_actual = next(colores)

            dispersion = ax.scatter(x, y, color=color_actual, label=f'Disparo {
                                    frame + 1}: {puntos_legenda}')
            disparos.append(dispersion)

            disparos_colores[frame] = (dispersion, f'Disparo {
                                       frame + 1}: {puntos_legenda}')

            if len(disparos) > 1:
                disparos[-2].set_alpha(0.5)

            primera_leyenda = ax.legend(
                loc="center left",
                bbox_to_anchor=(1.05, 0.75),
                handles=[disparos_colores[i][0] for i in range(frame + 1)],
                labels=[disparos_colores[i][1] for i in range(frame + 1)],
                fontsize=10,
                title="Orden disparado"
            )
            ax.add_artist(primera_leyenda)

            disparos_ordenados = sorted(
                disparos_colores.items(),
                key=lambda x: (
                    11 if 'X' in x[1][1] else
                    -1 if 'M' in x[1][1] else
                    int(x[1][1].split(': ')[1])),
                reverse=True
            )
            segunda_leyenda = ax.legend(
                loc="center left",
                bbox_to_anchor=(1.05, 0.3),
                handles=[disparo[1][0] for disparo in disparos_ordenados],
                labels=[disparo[1][1] for disparo in disparos_ordenados],
                fontsize=10,
                title="Orden de Puntos"
            )
            ax.add_artist(segunda_leyenda)

        pdf.savefig(fig)
        plt.close(fig)

# Cerrar la conexión a la base de datos
cursor.close()
db.close()
