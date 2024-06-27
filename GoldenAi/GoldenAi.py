# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mockupGoldenAi.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtCore import QTimer, Qt
import sys
import cv2
import pytesseract
import re
import os
import sys
import res_rc
import sqlite3
import time
from datetime import datetime

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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1196, 864)
        MainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        MainWindow.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/image/background/icon_goldenAi.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet("background-color:rgb(149, 129, 200)")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setStyleSheet("")
        self.widget.setObjectName("widget")
        self.scrollArea = QtWidgets.QScrollArea(self.widget)
        self.scrollArea.setGeometry(QtCore.QRect(0, 0, 611, 751))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 609, 749))
        self.scrollAreaWidgetContents.setStyleSheet("")
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.Camara = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.Camara.setGeometry(QtCore.QRect(10, 60, 601, 701))
        self.Camara.setStyleSheet("background-color:white;")
        self.Camara.setText("")
        self.Camara.setObjectName("Camara")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.tableWidget = QtWidgets.QTableWidget(self.widget)
        self.tableWidget.setGeometry(QtCore.QRect(620, 60, 501, 701))
        self.tableWidget.setStyleSheet("             QTableWidget {\n"
"                background-color: rgba(245, 245, 255, 255); /* Morado muy claro */\n"
"                color: black;\n"
"                gridline-color: rgba(200, 200, 200, 255);\n"
"                font-size: 14px;\n"
"            }\n"
"            QHeaderView::section {\n"
"                background-color: rgba(220, 220, 255, 255); /* Morado claro */\n"
"                color: black;\n"
"                font-weight: bold;\n"
"                border: 1px solid rgba(200, 200, 200, 255);\n"
"            }\n"
"            QTableWidget::item:selected {\n"
"                background-color: rgba(235, 235, 255, 255); /* Morado muy claro */\n"
"                color: black;\n"
"            }")
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        self.bRegistrar = QtWidgets.QPushButton(self.widget)
        self.bRegistrar.setGeometry(QtCore.QRect(10, 770, 211, 51))
        self.bRegistrar.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.bRegistrar.setStyleSheet("            QPushButton {\n"
"                background-color: rgba(245, 245, 255, 255); /* Morado muy claro */\n"
"                color: black;\n"
"                border: none;\n"
"                padding: 10px 20px;\n"
"                border-radius: 5px;\n"
"            }\n"
"            QPushButton:hover {\n"
"                background-color: rgba(220, 220, 255, 255); /* Morado claro */\n"
"            }\n"
"            QPushButton:pressed {\n"
"                background-color: rgba(200, 200, 240, 255); /* Morado claro */\n"
"            } ")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/image/background/icon_agregarPatentes.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bRegistrar.setIcon(icon1)
        self.bRegistrar.setIconSize(QtCore.QSize(50, 50))
        self.bRegistrar.setObjectName("bRegistrar")
        self.bSalir = QtWidgets.QPushButton(self.widget)
        self.bSalir.setGeometry(QtCore.QRect(1110, 0, 51, 51))
        self.bSalir.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.bSalir.setStyleSheet("\n"
"\n"
"QPushButton {\n"
"     background-color: transparent; \n"
"      border: none;\n"
" }\n"
" QPushButton:hover {\n"
"      background-color: grey;\n"
" }")
        self.bSalir.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/image/background/close.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bSalir.setIcon(icon2)
        self.bSalir.setObjectName("bSalir")
        self.gridLayout.addWidget(self.widget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.cap = cv2.VideoCapture(0)
        self.index = 1
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(3000)

        initialize_database()
        self.mostrar_patentes()
    
    def start_timer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.mostrar_patentes)
        self.timer.start(1000)  # Actualiza cada 1 segundos

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, channel = frame_rgb.shape
            step = channel * width
            q_img = QImage(frame_rgb.data, width, height, step, QImage.Format_RGB888)
            self.Camara.setPixmap(QPixmap.fromImage(q_img))

            procesar_imagen(frame, self.index)
            self.index += 1

    # Función para mostrar las patentes
    def mostrar_patentes(self):
        conn = sqlite3.connect(database_file)
        cursor = conn.cursor()
        
        cursor.execute('SELECT patente_id, digitos_patente, hora_registro, fecha_registro, estado FROM patentes')
        patentes = cursor.fetchall()
        
        conn.close()

        # Configurar el número de filas y columnas del tableWidget
        self.tableWidget.setRowCount(len(patentes))
        self.tableWidget.setColumnCount(4)  # Asegúrate de que siempre haya 4 columnas

        # Llenar el tableWidget con los datos de las patentes
        for row_num, row_data in enumerate(patentes):
            for col_num, col_data in enumerate(row_data[1:5]):
                self.tableWidget.setItem(row_num, col_num, QTableWidgetItem(str(col_data)))
        

    def closeEvent(self, event):
        self.cap.release()
        event.accept()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "GoldenAI"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Digitos"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Hora"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Fecha"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Estado"))
        self.bRegistrar.setText(_translate("MainWindow", "Registro de patentes"))

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

        # Bandera para determinar si se ha detectado una patente
        patente_detectada = False

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
                    patente_detectada = True
                    print('PATENTE ENCONTRADA:', cleaned_text)

                    # Dibujar rectángulo alrededor de la placa
                    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    cv2.putText(image, cleaned_text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    # Guardar la patente, estado y la fecha/hora en la base de datos SQLite
                    estado = "Autorizado"
                    save_to_database(cleaned_text, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), estado)


        # Guardar la imagen procesada en la carpeta 'resultado' solo si se detectó una patente
        if patente_detectada:
            output_dir = 'resultado'  # Asegúrate de que este directorio exista
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            output_path = os.path.join(output_dir, f'Resultado{index}.jpg')
            cv2.imwrite(output_path, image)
            print(f"Imagen guardada en: {output_path}")
        else:
            print("No se detectó ninguna patente en la imagen.")

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

#  Función para guardar la patente y la fecha/hora en la base de datos SQLite
def save_to_database(patente, fecha_hora, estado='Denegado', usuario_id=None):
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO patentes (usuario_id, digitos_patente, hora_registro, fecha_registro, estado) VALUES (?, ?, ?, ?, ?)
    ''', (usuario_id, patente, fecha_hora.split()[1], fecha_hora.split()[0], estado))
    
    conn.commit()
    conn.close()

    ui.mostrar_patentes()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
