import pandas as pd

# Ruta del archivo CSV de entrada
csv_file = r'C:\Users\josma\OneDrive\Documentos\Proyectos\Automatizacion_Registro_Tiro_Con_Arco\Automation Anywhere\Documentos\Resultados_Entrenamiento.csv'

# Ruta del archivo XLSX de salida
xlsx_file = 'C:/Users/josma/OneDrive/Documentos/Proyectos/Automatizacion_Registro_Tiro_Con_Arco/Automation Anywhere/Documentos/Resultados_Entrenamiento.xlsx'

# Leer el archivo CSV usando ';' como separador y omitiendo la primera fila
df = pd.read_csv(csv_file, sep=';', header=None,
                 engine='python', skiprows=1, on_bad_lines='skip')

# Definir los nombres de las columnas según el formato que deseas
df.columns = [
    "Titulo", "Fecha", "Serie estándar", "Interior", "Arco", "Flecha",
    "Serie", "Distancia", "Blanco", "Tanda", "Fecha/Hora", "Puntos",
    "Números de flecha", "x", "y"
]

# Guardar el DataFrame como un archivo XLSX
df.to_excel(xlsx_file, index=False)

print(f"Archivo convertido y guardado como: {xlsx_file}")
