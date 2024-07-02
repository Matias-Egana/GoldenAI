import cv2
import pytesseract
import re
import os
from datetime import datetime
from database import check_patente_permitida, detect_anomalia, get_path_output, get_path_output_dir, save_to_database
from my_email import send_email
from PyQt5.QtWidgets import QApplication, QProgressDialog, QMessageBox
from PyQt5.QtCore import QTimer, Qt

# Configuración de Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

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
                
                # Verificar si la patente está en la lista permitida del usuario
                if check_patente_permitida(cleaned_text, usuario_id):
                    estado = "Autorizado"
                    print("Abriendo Portón...")
                    mostrar_progress_dialog()
                else:
                    estado = "Denegado"
                    print("Anomalia detectada")
                    # Obtener correo del usuario
                    to_email = detect_anomalia(usuario_id)

                    # Guardar la imagen procesada en la carpeta 'resultado'
                    output_path = get_path_output(index)
                    cv2.imwrite(output_path, image)
                    print(f"Imagen guardada en: {output_path}")

                    # Enviar correo de anomalia
                    subject = 'Alerta de Anomalía: Acceso Denegado'
                    body = f'Se ha detectado una anomalía con la patente: {cleaned_text}.'

                    try:
                        send_email(subject, body, to_email, output_path)
                    except Exception as e:
                        print(f"No se pudo enviar el correo a {to_email}: {e}")

                # Guardar la patente, estado y la fecha/hora en la base de datos SQLite
                save_to_database(cleaned_text, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), estado, usuario_id)

                print(f"Acceso {estado} para patente: {cleaned_text}")

    # Guardar la imagen procesada en la carpeta 'resultado' solo si se detectó una patente
    if patente_detectada:
        output_dir  = get_path_output_dir()
        output_path = os.path.join(output_dir, f'Resultado{index}.jpg')
        cv2.imwrite(output_path, image)
        print(f"Imagen guardada en: {output_path}")
    else:
        print("No se detectó ninguna patente en la imagen.")

def mostrar_progress_dialog():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    
    dialog = QProgressDialog()
    dialog.setWindowTitle("Acceso Autorizado")
    dialog.setLabelText("Abriendo Portón...")
    dialog.setWindowModality(Qt.WindowModal)
    dialog.setMinimum(0)
    dialog.setMaximum(100)  # Establece un máximo para la barra de progreso
    dialog.setValue(0)
    dialog.setCancelButton(None)
    dialog.show()

    # Configura un temporizador para actualizar el progreso cada 50 milisegundos
    timer = QTimer()
    timer.setInterval(50)  # Actualiza cada 50 milisegundos
    incremento = 0

    def actualizar_progreso():
        nonlocal incremento
        incremento += 1
        dialog.setValue(incremento)

        # Detiene el temporizador y cierra el diálogo después de 5 segundos (5000 milisegundos)
        if incremento >= 100:
            timer.stop()
            QTimer.singleShot(500, dialog.close)  # Cerrar el diálogo 500 ms después de completar la barra

    timer.timeout.connect(actualizar_progreso)
    timer.start()

    app.exec_()
    app.exec_()