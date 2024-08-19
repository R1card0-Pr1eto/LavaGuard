import os
import time
import cv2
from PIL import Image
import hashlib

# Crear la carpeta "Go-Lava" si no existe
folder_path = r"C:\Users\priet\OneDrive\Documentos\LavaGuard\go-lava\Go-Lava"
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# Archivo de texto donde se guardarán los strings generados
output_file = os.path.join(folder_path, "image_hashes.txt")

def get_latest_image(directory):
    # Obtener la lista de archivos en el directorio y filtrar solo las imágenes
    files = [os.path.join(directory, f) for f in os.listdir(directory) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
    
    # Verificar si hay archivos en la lista
    if not files:
        print("Error: No image files found in the specified directory.")
        return None

    # Obtener el archivo más reciente por fecha de modificación
    latest_file = max(files, key=os.path.getmtime)
    return latest_file

def capture_images():
    # Abrir la primera cámara disponible
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("No se pudo abrir la cámara.")
        return

    photo_count = 1

    while True:
        # Leer una imagen de la cámara
        ret, frame = cap.read()
        if not ret:
            print("No se puede leer desde la cámara.")
            break

        # Generar el nombre del archivo de imagen
        filename = os.path.join(folder_path, f"foto{photo_count}.jpg")

        # Guardar la imagen en la carpeta "Go-Lava"
        cv2.imwrite(filename, frame)
        print(f"Imagen guardada como {filename}")

        # Incrementar el contador de fotos
        photo_count += 1

        # Esperar 5 segundos antes de tomar la siguiente foto
        time.sleep(5)

        # Procesar la última imagen capturada después de guardarla
        process_latest_image()

    # Liberar la cámara y cerrar todas las ventanas
    cap.release()
    cv2.destroyAllWindows()

def process_latest_image():
    print(f"Checking for the most recent image in {folder_path}...")

    # Obtener la imagen más reciente
    image_file = get_latest_image(folder_path)

    if not image_file:
        return

    print(f"The path of your most recent image is {image_file}. Proceeding...")

    # Abrir la imagen
    try:
        img = Image.open(image_file)
    except Exception as e:
        print(f"Error: {e}")
        return

    # Obtener los datos de los píxeles
    pixel_data = list(img.getdata())
    pixel_bytes = bytearray()
    for pixel in pixel_data:
        if len(pixel) == 4:  # RGBA
            pixel_bytes.extend(pixel[:3])
        elif len(pixel) == 3:  # RGB
            pixel_bytes.extend(pixel)

    hex_string = pixel_bytes.hex()

    # Aplicar la función hash SHA512
    hash_object = hashlib.sha512()
    hash_object.update(hex_string.encode('utf-8'))
    hex_string = hash_object.hexdigest()

    # Guardar el string generado en el archivo de texto
    with open(output_file, 'a') as f:
        f.write(hex_string + "\n\n")  # Añade dos saltos de línea para la separación

    # Retornar el string generado
    print(f"Generated string: {hex_string}")

if __name__ == "__main__":
    capture_images()
