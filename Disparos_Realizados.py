import mysql.connector
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button
import itertools

# Conectar a la base de datos MySQL
db = mysql.connector.connect(
    host="localhost",          # Nombre del host
    user="root",               # Usuario de MySQL
    password="Sarinha_3",      # Contraseña de MySQL
    database="Tiro_Con_Arco"   # El nombre de la base de datos
)

cursor = db.cursor()

# Obtener el último ID_Entrenamiento de la base de datos
cursor.execute("SELECT MAX(ID_Entrenamiento) FROM Disparo")
ultimo_entrenamiento = cursor.fetchone()[0]

# Obtener las tandas disponibles para el último ID_Entrenamiento
cursor.execute(f"SELECT DISTINCT Tanda FROM Disparo WHERE ID_Entrenamiento = {
               ultimo_entrenamiento} ORDER BY Tanda")
tandas = [t[0] for t in cursor.fetchall()]

# Índice para la tanda actual
indice_tanda = 0

# Variable para la animación
ani = None  # Inicializar fuera del alcance de la función

# Función para configurar y mostrar la simulación por tanda


def simular_tanda(tanda):
    global ani  # Hacer referencia a la variable global

    # Consultar los datos de la base de datos para la tanda específica
    query = f"""
    SELECT ID_Disparo, Serie, Tanda, X, Y, Puntos
    FROM Disparo
    WHERE ID_Entrenamiento = {ultimo_entrenamiento} AND Tanda = {tanda}
    ORDER BY ID_Disparo;
    """
    cursor.execute(query)
    resultados = cursor.fetchall()

    # Limpiar la figura antes de dibujar una nueva tanda
    ax.clear()

    # Configuración inicial del gráfico
    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-1.1, 1.1)
    ax.set_title(
        f"Simulación de Impactos de Flechas en la Diana - Tanda {tanda}")
    ax.set_xlabel("X (Coordenadas)")
    ax.set_ylabel("Y (Coordenadas)")

    # Invertir el eje Y para corregir el efecto de espejo
    ax.invert_yaxis()

    # Establecer el aspecto del gráfico como igual
    ax.set_aspect('equal')

    # Dibujar la diana con círculos concéntricos, colores pastel y contornos negros
    circulos = [
        (1.0, '#f3f4f6'),  # Blanco pastel (más grande)
        (0.9, '#f3f4f6'),  # Blanco pastel
        (0.8, '#d3d3d3'),  # Negro pastel
        (0.7, '#d3d3d3'),  # Negro pastel
        (0.6, '#a6c8ff'),  # Azul pastel
        (0.5, '#a6c8ff'),  # Azul pastel
        (0.4, '#ffb3b3'),  # Rojo pastel
        (0.3, '#ffb3b3'),  # Rojo pastel
        (0.2, '#fff1b0'),  # Amarillo pastel
        (0.1, '#fff1b0'),  # Amarillo pastel
        (0.05, '#fff1b0')  # Amarillo pastel (más pequeño)
    ]

    # Añadir los círculos a la diana
    for radio, color in circulos:
        ax.add_patch(plt.Circle((0, 0), radio, color=color,
                     ec='black', linewidth=1.5, fill=True, alpha=0.8))

    # Lista para almacenar los objetos de dispersión de disparos y leyenda
    disparos = []
    disparos_colores = {}

    # Definir una lista de colores oscuros y vivos para los impactos
    colores = itertools.cycle(['darkred', 'darkblue', 'darkgreen', 'darkorange',
                              'purple', 'darkviolet', 'darkcyan', 'saddlebrown', 'black', 'darkslategray'])

    # Función de actualización para la animación
    def actualizar(frame):
        disparo = resultados[frame]
        x, y = disparo[3], disparo[4]
        puntos = disparo[5]

        # Obtener el color para el disparo actual
        color_actual = next(colores)

        # Añadir el disparo actual al gráfico
        dispersion = ax.scatter(x, y, color=color_actual, label=f'Disparo {
                                frame + 1}: {puntos}')
        disparos.append(dispersion)

        # Guardar el color del disparo para la leyenda
        disparos_colores[frame] = (dispersion, f'Disparo {
                                   frame + 1}: {puntos}')

        # Evitar duplicados en la leyenda y manejar la transparencia de disparos anteriores
        if len(disparos) > 1:
            # Hacer más transparente el disparo anterior
            disparos[-2].set_alpha(0.5)

        # === Primera Leyenda: "Orden disparado" ===
        primera_leyenda = ax.legend(
            loc="center left",
            bbox_to_anchor=(1.05, 0.75),
            handles=[disparos_colores[i][0] for i in range(frame + 1)],
            labels=[disparos_colores[i][1] for i in range(frame + 1)],
            fontsize=10,
            title="Orden disparado"
        )
        ax.add_artist(primera_leyenda)  # Añadir la primera leyenda manualmente

        # === Segunda Leyenda: "Orden de Puntos" ===
        disparos_ordenados = sorted(
            disparos_colores.items(),
            key=lambda x: 10 if x[1][1].split(
                ': ')[1] == 'X' else int(x[1][1].split(': ')[1]),
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
        ax.add_artist(segunda_leyenda)  # Añadir la segunda leyenda manualmente

    # Crear la animación y asignarla a la variable global 'ani'
    ani = animation.FuncAnimation(fig, actualizar, frames=len(
        resultados), interval=1000, repeat=False)
    plt.draw()

# Funciones de los botones de navegación


def next_tanda(event):
    global indice_tanda
    if indice_tanda < len(tandas) - 1:
        indice_tanda += 1
    simular_tanda(tandas[indice_tanda])


def prev_tanda(event):
    global indice_tanda
    if indice_tanda > 0:
        indice_tanda -= 1
    simular_tanda(tandas[indice_tanda])


# Configuración inicial del gráfico
fig, ax = plt.subplots(figsize=(10, 6))  # Tamaño ajustado

# Configuración de botones para manejar eventos de cambio de tanda
fig.canvas.mpl_connect('key_press_event', lambda event: next_tanda(
    event) if event.key == 'right' else None)
fig.canvas.mpl_connect('key_press_event', lambda event: prev_tanda(
    event) if event.key == 'left' else None)

# Mostrar la primera tanda
simular_tanda(tandas[indice_tanda])

plt.show()

# Cerrar la conexión a la base de datos
cursor.close()
db.close()
