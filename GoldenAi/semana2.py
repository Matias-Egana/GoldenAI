import sqlite3
import cv2
import pytesseract
import re
import os
from datetime import datetime

# Configuración de Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

# Directorio base donde se encuentra el script
base_dir = os.path.dirname(__file__)
print(base_dir)

# Directorio para guardar las imágenes y el archivo CSV
output_dir = os.path.join(base_dir, 'resultado')
database_file = os.path.join(base_dir, 'mi_base_de_datos.db')

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

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
        correo TEXT
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
        patentes_registradas TEXT UNIQUE
    )
    ''')
    
    conn.commit()
    conn.close()

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
def save_permitida(patente):
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT OR IGNORE INTO patentes_permitidas (patentes_registradas) VALUES (?)
    ''', (patente,))
    
    conn.commit()
    conn.close()

# Función para verificar si una patente está en la lista de patentes permitidas
def check_patente_permitida(patente):
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT * FROM patentes_permitidas WHERE patentes_registradas = ?
    ''', (patente,))

    result = cursor.fetchone()
    conn.close()
    
    return result is not None

# Función para procesar una imagen
def procesar_imagen(image, index):
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
                
                # Verificar si la patente está en la lista permitida
                if check_patente_permitida(cleaned_text):
                    estado = "Autorizado"
                    print("Abriendo Portón...")
                else:
                    estado = "Denegado"
                    print("Anomalia detectada")

                # Guardar la patente, estado y la fecha/hora en la base de datos SQLite
                usuario_id = None  # Asumimos que no tenemos el usuario asociado por ahora
                save_to_database(cleaned_text, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), estado, usuario_id)

                print(f"Acceso {estado} para patente: {cleaned_text}")

    # Mostrar imagen
    cv2.imshow('Resultados', image)
    
    # Guardar la imagen procesada en la carpeta 'resultado'
    cv2.imwrite(os.path.join(output_dir, f'Resultado{index}.jpg'), image)
    print(f"Imagen guardada en: {output_dir}")

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
            exit()

    cap.release()
    cv2.destroyAllWindows()
    return frame, index

# Función para agregar una nueva patente permitida
def agregar_patente_permitida(patente):
    if len(patente) == 6 and re.match(r'^[A-Z0-9]+$', patente):
        save_permitida(patente)
        print(f"Patente {patente} agregada a la lista de permitidas.")
    else:
        print("La patente debe tener exactamente 6 caracteres alfanuméricos.")

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

def mostrar_patentes_permitidas():
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM patentes_permitidas')
    rows = cursor.fetchall()
    conn.close()
    
    print("Contenido de la tabla 'patentes_permitidas':")
    for row in rows:
        print(row)
def agregar_usuario(nombre, apellido, correo):
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO usuarios (nombre, apellido, correo) VALUES (?, ?, ?)
    ''', (nombre, apellido, correo))
    
    conn.commit()
    conn.close()
    
    print(f"Usuario {nombre} {apellido} agregado con éxito.")

# Función principal
def main():
    initialize_database()
    # Preguntar al usuario si desea agregar un nuevo usuario
    nuevo_usuario = input("¿Desea agregar un nuevo usuario? (S/N): ").strip().upper()
    if nuevo_usuario == 'S':
        print("estoy")
        nombre = input("Ingrese el nombre: ")
        apellido = input("Ingrese el apellido: ")
        correo = input("Ingrese el correo: ")
        agregar_usuario(nombre, apellido, correo)

    # Preguntar al usuario si desea agregar una nueva patente permitida
    opcion = input("¿Desea agregar una patente permitida? (S/N): ").strip().upper()
    if opcion == 'S':
        patente = input("Ingrese la patente permitida (6 caracteres alfanuméricos): ").strip().upper()
        agregar_patente_permitida(patente)

    while True:
        # Capturar imagen desde la cámara y obtener el nuevo índice cada vez
        imagen, index = capturar_imagen()

        # Procesar la imagen
        procesar_imagen(imagen, index)
        mostrar_usuarios()
        mostrar_patentes()
        mostrar_patentes_permitidas()

if __name__ == "__main__":
    main()
