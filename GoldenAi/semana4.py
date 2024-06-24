import sqlite3
import cv2
import pytesseract
import re
import os
from datetime import datetime
from hashlib import sha256
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Configuración de Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

# Directorio base 
base_dir = os.getcwd()

# Directorio para guardar las imágenes
output_dir = os.path.join(base_dir, 'resultado')
database_file = os.path.join(base_dir, 'mi_base_de_datos.db')

if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"Directorio {output_dir} creado.")
else:
    print(f"Directorio {output_dir} ya existe.")

# Función para inicializar la base de datos SQLite y las tablas
def initialize_database():
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()
    
    # Crear tabla de usuarios si no existe
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        usuario_id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        apellido TEXT,
        correo TEXT UNIQUE,
        contrasena TEXT
    )
    ''')
    
    # Crear tabla de patentes si no existe
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS patentes (
        patente_id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER,
        digitos_patente TEXT,
        hora_registro TEXT,
        fecha_registro TEXT,
        estado TEXT DEFAULT 'Denegado',
        FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id)
    )
    ''')

    # Crear tabla de patentes permitidas si no existe
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS patentes_permitidas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER,
        patentes_registradas TEXT UNIQUE,
        FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id)
    )
    ''')
    
    conn.commit()
    conn.close()

# Función para encriptar contraseñas
def encrypt_password(password):
    return sha256(password.encode()).hexdigest()

# Función para el login de usuario
def login(correo, contrasena):
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT usuario_id, contrasena FROM usuarios WHERE correo = ?
    ''', (correo,))
    
    result = cursor.fetchone()
    conn.close()
    
    if result and result[1] == encrypt_password(contrasena):
        return result[0]
    return None

# Función para guardar la patente y la fecha/hora en la base de datos SQLite
def save_to_database(patente, fecha_hora, estado='Denegado', usuario_id=None):
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO patentes (usuario_id, digitos_patente, hora_registro, fecha_registro, estado) VALUES (?, ?, ?, ?, ?)
    ''', (usuario_id, patente, fecha_hora.split()[1], fecha_hora, estado))
    
    conn.commit()
    conn.close()

# Función para guardar patente permitida en la base de datos SQLite
def save_permitida(patente, usuario_id):
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT OR IGNORE INTO patentes_permitidas (usuario_id, patentes_registradas) VALUES (?, ?)
    ''', (usuario_id, patente))
    
    conn.commit()
    conn.close()

# Función para verificar si una patente está en la lista de patentes permitidas de un usuario
def check_patente_permitida(patente, usuario_id):
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT * FROM patentes_permitidas WHERE patentes_registradas = ? AND usuario_id = ?
    ''', (patente, usuario_id))

    result = cursor.fetchone()
    conn.close()
    
    return result is not None

# Función para procesar una imagen
def procesar_imagen(image, index, usuario_id):
    # Convertir a escala de grises
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Aplicar umbralización
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Realizar operaciones morfológicas para eliminar el ruido
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)

    # Encontrar contornos
    cnts, _ = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Iterar sobre los contornos
    for c in cnts:
        x, y, w, h = cv2.boundingRect(c)
        
        # Filtrar contornos basados en el área y la relación de aspecto
        if cv2.contourArea(c) > 5000 and 1 < w / h < 5:
            # Recortar región de interés
            roi = gray[y:y+h, x:x+w]
            
            # Aplicar OCR a la región de interés
            text = pytesseract.image_to_string(roi, config='--psm 6')
            
            # Limpiar y mostrar el texto
            cleaned_text = ''.join(filter(str.isalnum, text))
            
            # Filtrar por longitud del texto y caracteres válidos
            if len(cleaned_text) == 6 and re.match(r'^[A-Z0-9]+$', cleaned_text):
                print('PATENTE ENCONTRADA:', cleaned_text)

                # Dibujar rectángulo alrededor de la placa
                cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(image, cleaned_text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                
                # Verificar si la patente está en la lista permitida del usuario
                if check_patente_permitida(cleaned_text, usuario_id):
                    estado = "Autorizado"
                    print("Abriendo Portón...")
                else:
                    estado = "Denegado"
                    print("Anomalia detectada")
                    # Obtener correo del usuario
                    conn = sqlite3.connect(database_file)
                    cursor = conn.cursor()
                    cursor.execute('SELECT correo FROM usuarios WHERE usuario_id = ?', (usuario_id,))
                    to_email = cursor.fetchone()[0]
                    conn.close()

                    # Guardar la imagen procesada en la carpeta 'resultado'
                    output_path = os.path.join(output_dir, f'Resultado{index}.jpg')
                    cv2.imwrite(output_path, image)
                    print(f"Imagen guardada en: {output_path}")

                    # Enviar correo de anomalia
                    subject = 'Alerta de Anomalía: Acceso Denegado'
                    body = f'Se ha detectado una anomalía con la patente: {cleaned_text}.'
                    send_email(subject, body, to_email, output_path)

                # Guardar la patente, estado y la fecha/hora en la base de datos SQLite
                save_to_database(cleaned_text, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), estado, usuario_id)

                print(f"Acceso {estado} para patente: {cleaned_text}")

    # Mostrar imagen
    cv2.imshow('Resultados', image)
    
    # Guardar la imagen procesada en la carpeta 'resultado'
    output_path = os.path.join(output_dir, f'Resultado{index}.jpg')
    cv2.imwrite(output_path, image)
    print(f"Imagen guardada en: {output_path}")

def send_email(subject, body, to_email, attachment_path):
    # Configuración del servidor SMTP
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_user = 'eganaamatias@gmail.com'
    smtp_password = 'ynmm zyhy tjna zmlm'

    # Crear el mensaje
    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['To'] = to_email
    msg['Subject'] = subject

    # Adjuntar el cuerpo del mensaje
    msg.attach(MIMEText(body, 'plain'))

    # Adjuntar el archivo
    attachment = open(attachment_path, 'rb')
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(attachment_path)}')
    msg.attach(part)

    try:
        # Conectar al servidor SMTP y enviar el correo
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(smtp_user, to_email, msg.as_string())
        server.quit()
        print(f'Correo enviado a {to_email}')
    except Exception as e:
        print(f'Error al enviar correo: {e}')

# Función para capturar una imagen desde la cámara
def capturar_imagen():
    # Encontrar el número más alto actual en los nombres de archivo existentes
    existing_numbers = [int(re.findall(r'\d+', filename)[0]) for filename in os.listdir(output_dir) if re.match(r'Resultado\d+.jpg', filename)]
    if existing_numbers:
        index = max(existing_numbers) + 1
    else:
        index = 1

    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        cv2.imshow('Presiona espacio para capturar', frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord(' '):
            break
        elif key == 27:  # '27' es el código ASCII para la tecla 'Esc'
            cap.release()
            cv2.destroyAllWindows()
            return None, None

    cap.release()
    cv2.destroyAllWindows()
    return frame, index

# Función para agregar una nueva patente permitida
def agregar_patente_permitida(patente, usuario_id):
    if len(patente) == 6 and re.match(r'^[A-Z0-9]+$', patente):
        save_permitida(patente, usuario_id)
        print(f"Patente {patente} agregada a la lista de permitidas para el usuario {usuario_id}.")
    else:
        print("La patente debe tener exactamente 6 caracteres alfanuméricos.")

# Función para agregar un nuevo usuario
def agregar_usuario(nombre, apellido, correo, contrasena):
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO usuarios (nombre, apellido, correo, contrasena) VALUES (?, ?, ?, ?)
    ''', (nombre, apellido, correo, encrypt_password(contrasena)))
    
    conn.commit()
    conn.close()
    
    print(f"Usuario {nombre} {apellido} agregado con éxito.")

# Función para mostrar el contenido de la tabla usuarios
def mostrar_usuarios():
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM usuarios')
    rows = cursor.fetchall()
    conn.close()
    
    print("Contenido de la tabla 'usuarios':")
    for row in rows:
        print(row)

# Función para mostrar el contenido de la tabla patentes
def mostrar_patentes():
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM patentes')
    rows = cursor.fetchall()
    conn.close()
    
    print("Contenido de la tabla 'patentes':")
    for row in rows:
        print(row)

# Función para mostrar el contenido de la tabla patentes permitidas
def mostrar_patentes_permitidas():
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM patentes_permitidas')
    rows = cursor.fetchall()
    conn.close()
    
    print("Contenido de la tabla 'patentes_permitidas':")
    for row in rows:
        print(row)

# Función principal
def main():
    initialize_database()
    
    # Preguntar al usuario si desea registrarse o iniciar sesión
    registro_o_login = input("¿Desea registrarse o iniciar sesión? (R/L): ").strip().upper()
    if registro_o_login == 'R':
        nombre = input("Ingrese el nombre: ")
        apellido = input("Ingrese el apellido: ")
        correo = input("Ingrese el correo: ")
        contrasena = input("Ingrese la contraseña: ")
        agregar_usuario(nombre, apellido, correo, contrasena)
    
    correo = input("Ingrese su correo: ")
    contrasena = input("Ingrese su contraseña: ")
    
    usuario_id = login(correo, contrasena)
    if usuario_id:
        print(f"Login exitoso. Bienvenido, {correo}")
        
        # Preguntar al usuario si desea agregar una nueva patente permitida
        opcion = input("¿Desea agregar una patente permitida? (S/N): ").strip().upper()
        if opcion == 'S':
            patente = input("Ingrese la patente permitida (6 caracteres alfanuméricos): ").strip().upper()
            agregar_patente_permitida(patente, usuario_id)

        while True:
            # Capturar imagen desde la cámara y obtener el nuevo índice cada vez
            imagen, index = capturar_imagen()
            if imagen is None: break

            # Procesar la imagen
            procesar_imagen(imagen, index, usuario_id)
            mostrar_usuarios()
            mostrar_patentes()
            mostrar_patentes_permitidas()
    else:
        print("Correo o contraseña incorrectos. Inténtelo de nuevo.")

if __name__ == "__main__":
    main()
