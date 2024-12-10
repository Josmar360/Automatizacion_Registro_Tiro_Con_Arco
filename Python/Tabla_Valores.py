import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
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
    '0': '#000000',
    'M': '#000000'   # Verde claro
}

# Conexión a la base de datos MySQL
db = mysql.connector.connect(
    host="host",          # Nombre del host
    user="usuario",               # Usuario de MySQL
    password="Contraseña",      # Contraseña de MySQL
    database="Tiro_Con_Arco"   # El nombre de la base de datos
)

cursor = db.cursor()

# Obtener el último valor de ID_Entrenamiento
cursor.execute("SELECT MAX(FK_ID_Entrenamiento) FROM Disparo;")
ultimo_id_entrenamiento = cursor.fetchone()[0]

# Consulta SQL para obtener los datos necesarios
query = f"""
SELECT Serie, Tanda, X, Y, Puntos
FROM Disparo
WHERE FK_ID_Entrenamiento = {ultimo_id_entrenamiento}
ORDER BY Serie, Tanda, PK_ID_Disparo;
"""
cursor.execute(query)
resultados = cursor.fetchall()

# Cerrar la conexión a la base de datos
cursor.close()
db.close()

# Convertir los resultados a un DataFrame de pandas para facilitar la manipulación
df = pd.DataFrame(resultados, columns=['Serie', 'Tanda', 'X', 'Y', 'Puntos'])

# Convertir 'M' a 0 en la columna 'Puntos' para cálculos
df['Puntos'] = df['Puntos'].apply(
    lambda x: 0 if x == 'M' else (10 if x == 'X' else int(x))
)

# Calcular la precisión sin contar 'M' (0)


def calcular_precision(data):
    puntos_totales = len(data) * 10
    puntos_obtenidos = sum(data)
    return (puntos_obtenidos / puntos_totales) * 100


# Crear el PDF con varias páginas
pdf_path = 'Reporte_Tiro_Con_Arco.pdf'
with PdfPages(pdf_path) as pdf:

    # Obtener las series únicas
    series_unicas = df['Serie'].unique()

    for serie in series_unicas:
        # Filtrar los datos por serie
        df_serie = df[df['Serie'] == serie]

        # Agrupar los datos por tanda dentro de la serie
        agrupado = df_serie.groupby(['Serie', 'Tanda'])

        # Crear la figura y los ejes
        fig, ax = plt.subplots(figsize=(14, 10))
        ax.set_axis_off()

        # Crear la tabla usando matplotlib Table
        tabla = Table(ax, bbox=[0, 0, 1, 1])

        # Añadir el título
        ax.set_title(f'Serie {serie}', fontsize=14, weight='bold')

        # Obtener el número máximo de flechas por tanda
        max_flechas = df_serie.groupby('Tanda')['Puntos'].count().max()

        # Crear los encabezados dinámicamente en función del número de flechas
        columnas = ['Serie', 'Tanda'] + [str(i) for i in range(1, max_flechas + 1)] + [
            'Puntuación', 'Acumulado', 'Precisión (%)']
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
            flechas_ordenadas = sorted(flechas, reverse=True)

            # Ajustar el número de flechas según la tanda
            while len(flechas_ordenadas) < max_flechas:
                # Usar 0 para vacíos en lugar de 'M'
                flechas_ordenadas.append(0)

            puntuacion = sum(flechas)
            acumulado = df_serie[df_serie['Tanda'] <= tanda]['Puntos'].sum()
            precision = calcular_precision(flechas)

            fila = [serie, tanda] + flechas_ordenadas[:max_flechas] + \
                [puntuacion, acumulado, round(precision, 2)]

            for i, valor in enumerate(fila):
                if i >= 2 and i < (max_flechas + 2):
                    # Mostrar "M" en vez de 0 visualmente
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

        # Añadir fila de sumatoria
        total_puntos = df_serie['Puntos'].sum()
        total_flechas_ordenadas = sorted(
            df_serie['Puntos'].tolist(), reverse=True)
        last_three_flechas = total_flechas_ordenadas[:3]

        sumatoria_fila = ['Total', ''] + [''] * max_flechas + [total_puntos,
                                                               total_puntos, round(calcular_precision(df_serie['Puntos'].tolist()), 2)]

        for i, valor in enumerate(sumatoria_fila):
            # Asegurarse de que los colores se apliquen correctamente
            if i >= (max_flechas + 2) and i < (max_flechas + 2):
                if i - (max_flechas + 2) < len(last_three_flechas):
                    color = colores.get(
                        str(last_three_flechas[i - (max_flechas + 2)]), 'white')
                    text_color = 'white' if color == '#000000' else 'black'
                    cell = tabla.add_cell(len(agrupado) + 1, i, width=0.1, height=0.1, text=str(
                        last_three_flechas[i - (max_flechas + 2)]), loc='center', edgecolor='black', facecolor=color)
                    cell.set_fontsize(10)
                    cell.set_text_props(color=text_color)
                else:
                    cell = tabla.add_cell(len(agrupado) + 1, i, width=0.1, height=0.1,
                                          text='', loc='center', edgecolor='black', facecolor='white')
                    cell.set_fontsize(10)
            else:
                cell = tabla.add_cell(len(agrupado) + 1, i, width=0.1, height=0.1, text=str(
                    valor), loc='center', edgecolor='black', facecolor='lightgrey')
                cell.set_fontsize(10)

        # Ajustar el tamaño de las celdas
        tabla.auto_set_font_size(False)
        tabla.set_fontsize(8)

        # Añadir la tabla al gráfico
        ax.add_table(tabla)

        # Guardar cada serie en una página separada
        pdf.savefig(fig)
        plt.close(fig)

print(f'El reporte PDF se ha guardado en: {pdf_path}')
