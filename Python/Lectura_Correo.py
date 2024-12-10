import os
import extract_msg
import chardet  # Necesita este módulo para detectar la codificación


def detect_encoding(text):
    """
    Detecta la codificación del texto usando la librería chardet.
    Devuelve el texto correctamente decodificado según la codificación detectada.
    """
    result = chardet.detect(text.encode())  # Detecta la codificación del texto
    encoding = result['encoding']
    try:
        # Intenta decodificar el texto con la codificación detectada.
        return text.encode(encoding).decode('utf-8')
    except:
        # Si no puede decodificar correctamente, devuelve el texto original
        return text


def guardar_contenido_en_txt(file_path, output_file):
    """
    Lee un archivo .msg y guarda su contenido (asunto, remitente, fecha, cuerpo y adjuntos)
    en un archivo de texto (.txt).

    :param file_path: Ruta del archivo .msg
    :param output_file: Ruta del archivo .txt donde se guardará el contenido
    """
    if not os.path.exists(file_path):
        print("El archivo no existe. Verifica la ruta.")
        return

    try:
        # Cargar el archivo .msg
        msg = extract_msg.Message(file_path)
        msg_subject = detect_encoding(msg.subject or "")
        msg_sender = detect_encoding(msg.sender or "")
        msg_date = msg.date
        msg_body = detect_encoding(msg.body or "")

        # Crear el contenido que se escribirá en el archivo .txt
        contenido_correo = f"===== Detalles del mensaje =====\n"
        contenido_correo += f"📌 Asunto: {msg_subject}\n"
        contenido_correo += f"📧 Remitente: {msg_sender}\n"
        contenido_correo += f"📅 Fecha: {msg_date}\n"
        contenido_correo += f"\n===== Contenido =====\n{msg_body}\n"

        # Agregar los adjuntos (si los hay)
        if msg.attachments:
            contenido_correo += "\n===== Archivos adjuntos =====\n"
            for attachment in msg.attachments:
                contenido_correo += f"📎 {attachment.longFilename}\n"

        # Guardar el contenido en el archivo .txt
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(contenido_correo)

        print(f"El contenido del correo ha sido guardado en {output_file}")
    except Exception as e:
        print(f"Ocurrió un error al leer el archivo: {e}")


# Ruta del archivo .msg
ruta_archivo = "C:/Users/josma/OneDrive/Documentos/Proyectos/Automatizacion_Registro_Tiro_Con_Arco/Automation Anywhere/Documentos/Resultados_Entrenamiento.msg"
# Ruta donde se guardará el archivo .txt
ruta_salida = "C:/Users/josma/OneDrive/Documentos/Proyectos/Automatizacion_Registro_Tiro_Con_Arco/Automation Anywhere/Documentos/Resultados_Entrenamiento.txt"

# Llamar a la función para guardar el contenido en un archivo de texto
guardar_contenido_en_txt(ruta_archivo, ruta_salida)
