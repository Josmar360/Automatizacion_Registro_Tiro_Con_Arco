import mysql.connector
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import itertools

# Conectar a la base de datos MySQL Workbench
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

# Obtener las combinaciones de Serie y Tanda para el último ID_Entrenamiento
cursor.execute(f"""
    SELECT DISTINCT Serie, Tanda
    FROM Disparo
    WHERE FK_ID_Entrenamiento = {ultimo_entrenamiento}
    ORDER BY Serie, Tanda
""")
serie_tanda_combinaciones = cursor.fetchall()

# Colores para los impactos
colores = itertools.cycle(['darkred', 'darkblue', 'darkgreen', 'darkorange',
                           'purple', 'darkviolet', 'darkcyan', 'saddlebrown',
                           'black', 'darkslategray'])

# Inicialización del PDF
with PdfPages('C:/Users/josma/OneDrive/Documentos/Proyectos/Automatizacion_Registro_Tiro_Con_Arco/Automation Anywhere/Archivos/Impactos_Realizados.pdf') as pdf:

    # Recorrer cada combinación de serie y tanda para generar los gráficos
    for serie, tanda in serie_tanda_combinaciones:

        # Consultar los datos de la base de datos para la combinación específica
        query = f"""
        SELECT FK_ID_Entrenamiento, Serie, Tanda, X, Y, Puntos
        FROM Disparo
        WHERE FK_ID_Entrenamiento = {ultimo_entrenamiento} AND Serie = {serie} AND Tanda = {tanda}
        ORDER BY FK_ID_Entrenamiento;
        """
        cursor.execute(query)
        resultados = cursor.fetchall()

        # Configuración inicial del gráfico
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.set_xlim(-1.1, 1.1)
        ax.set_ylim(-1.1, 1.1)
        ax.set_title(f"Serie {serie} - Tanda {tanda}")
        ax.set_xlabel("X (Coordenadas)")
        ax.set_ylabel("Y (Coordenadas)")
        ax.invert_yaxis()
        ax.set_aspect('equal')

        # Dibujar la diana con círculos concéntricos
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

        # Lista para almacenar los objetos de dispersión de disparos y leyenda
        disparos = []
        disparos_colores = {}

        # Función para actualizar los disparos
        for frame, disparo in enumerate(resultados):
            x, y = disparo[3], disparo[4]
            puntos = disparo[5]

            # Manejar puntos especiales para la leyenda
            if puntos == 10:
                puntos_legenda = 'X'
            elif puntos == 0:
                puntos_legenda = 'M'
            else:
                puntos_legenda = str(puntos)

            # Obtener el color para el disparo actual
            color_actual = next(colores)

            # Añadir el disparo al gráfico
            dispersion = ax.scatter(x, y, color=color_actual, label=f'Disparo {
                                    frame + 1}: {puntos_legenda}')
            disparos.append(dispersion)

            # Guardar el color del disparo para la leyenda
            disparos_colores[frame] = (dispersion, f'Disparo {
                                       frame + 1}: {puntos_legenda}')

            # Evitar duplicados en la leyenda y manejar la transparencia de disparos anteriores
            if len(disparos) > 1:
                disparos[-2].set_alpha(0.5)

            # Primera leyenda: "Orden disparado"
            primera_leyenda = ax.legend(
                loc="center left",
                bbox_to_anchor=(1.05, 0.75),
                handles=[disparos_colores[i][0] for i in range(frame + 1)],
                labels=[disparos_colores[i][1] for i in range(frame + 1)],
                fontsize=10,
                title="Orden disparado"
            )
            ax.add_artist(primera_leyenda)

            # Segunda leyenda: "Orden de Puntos"
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

        # Guardar el gráfico en el PDF
        pdf.savefig(fig)
        plt.close(fig)

# Cerrar la conexión a la base de datos
cursor.close()
db.close()
