import cv2
import pytesseract
import re
import os
import csv
from datetime import datetime

# Configuración de Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

# Directorio base donde se encuentra el script
base_dir = base_dir = os.path.join(os.path.dirname(__file__), '..')
print(base_dir)

# Directorio para guardar las imágenes y el archivo CSV
output_dir = os.path.join(base_dir, 'resultado')
csv_file = os.path.join(base_dir, 'patentes.csv')

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Función para inicializar el archivo CSV si no existe
def initialize_csv():
    if not os.path.exists(csv_file):
        with open(csv_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Patente', 'Fecha y Hora'])

# Función para guardar la patente y la fecha/hora en el archivo CSV
def save_to_csv(patente, fecha_hora):
    with open(csv_file, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([patente, fecha_hora])

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
                
                # Guardar la patente y la fecha/hora en el archivo CSV
                save_to_csv(cleaned_text, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

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

def mostrar_contenido_csv():
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            print(row)

# Función principal
def main():
    initialize_csv()
    while True:
        # Capturar imagen desde la cámara y obtener el nuevo índice cada vez
        imagen, index = capturar_imagen()

        # Procesar la imagen
        procesar_imagen(imagen, index)
        mostrar_contenido_csv()

if __name__ == "__main__":
    main()
