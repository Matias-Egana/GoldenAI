import sqlite3
import os
from datetime import datetime
from hashlib import sha256

# Directorio base 
base_dir = os.getcwd()

# Directorio para guardar las imágenes
output_dir = os.path.join(base_dir, 'resultado')
database_file = os.path.join(base_dir, 'mi_base_de_datos.db')

def folder_exist():
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Directorio {output_dir} creado.")
    else:
        print(f"Directorio {output_dir} ya existe.")

# Función para inicializar la base de datos SQLite y las tablas
def initialize_database():
    folder_exist()
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

# Función para mostrar las patentes permitidas de un usuario específico
def mostrar_patentes_permitidas(usuario_id):
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM patentes_permitidas WHERE usuario_id = ?', (usuario_id,))
    patentes_permitidas = cursor.fetchall()
    
    conn.close()
    
    return patentes_permitidas

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

def agregar_usuario(nombre, apellido, correo, contrasena):
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
        INSERT INTO usuarios (nombre, apellido, correo, contrasena) VALUES (?, ?, ?, ?)
        ''', (nombre, apellido, correo, encrypt_password(contrasena)))
        conn.commit()
        usuario_id = cursor.lastrowid
        print(f'Usuario {nombre} {apellido} agregado exitosamente.')
        return usuario_id
    except sqlite3.IntegrityError:
        print(f'Error: el correo {correo} ya está registrado.')
        return None
    finally:
        conn.close()
  
# Función para mostrar los usuarios
def mostrar_usuarios():
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM usuarios')
    usuarios = cursor.fetchall()
    
    for usuario in usuarios:
        print(usuario)
    
    conn.close()

# Función para mostrar las patentes
def mostrar_patentes():
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM patentes')
    patentes = cursor.fetchall()
    
    for patente in patentes:
        print(patente)
    
    conn.close()

# Función para agregar una patente permitida
def agregar_patente_permitida(patente, usuario_id):
    save_permitida(patente, usuario_id)
    print(f'Patente permitida {patente} agregada exitosamente.')

# Función para eliminar una patente permitida
def eliminar_patente_permitida(patente, usuario_id):
    delete_permitida(patente, usuario_id)
    print(f'Patente permitida {patente} eliminada exitosamente.')

# Función para guardar patente permitida en la base de datos SQLite
def delete_permitida(patente, usuario_id):
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()

    # Query para eliminar la patente permitida
    cursor.execute('''
        DELETE FROM patentes_permitidas
        WHERE usuario_id = ? AND patentes_registradas = ?
    ''', (usuario_id, patente))

    conn.commit()
    conn.close()

# Función para capturar una imagen desde la cámara
def capturar_imagen(cap, index):
    ret, frame = cap.read()
    if not ret:
        print("Error al capturar la imagen.")
        return None, None
    return frame, index

def detect_anomalia(usuario_id):
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()
    cursor.execute('SELECT correo FROM usuarios WHERE usuario_id = ?', (usuario_id,))
    to_email = cursor.fetchone()[0]
    conn.close()
    return to_email

def get_path_output(index):
    output_path = os.path.join(output_dir, f'Resultado{index}.jpg')
    return output_path

def get_path_output_dir():
    output_dir = os.path.join(base_dir, 'resultado')
    return output_dir

def mostrar_patente_widget():
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()
        
    cursor.execute('SELECT patente_id, digitos_patente, hora_registro, fecha_registro, estado FROM patentes')
    patentes = cursor.fetchall()
        
    conn.close()
    return patentes