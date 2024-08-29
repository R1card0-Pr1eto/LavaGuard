import os
import time
import cv2
from PIL import Image
import hashlib

folder_path = r"C:\Users\priet\OneDrive\Documentos\LavaGuard\go-lava\Go-Lava"
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

output_file = os.path.join(folder_path, "image_hashes.txt")

def get_latest_image(directory):
    files = [os.path.join(directory, f) for f in os.listdir(directory) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
  
    if not files:
        print("Error: No image files found in the specified directory.")
        return None

    latest_file = max(files, key=os.path.getmtime)
    return latest_file

def capture_images():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("No se pudo abrir la cámara.")
        return

    photo_count = 1

    while True:
        ret, frame = cap.read()
        if not ret:
            print("No se puede leer desde la cámara.")
            break

        filename = os.path.join(folder_path, f"foto{photo_count}.jpg")

        cv2.imwrite(filename, frame)
        print(f"Imagen guardada como {filename}")

        photo_count += 1

        time.sleep(5)

        process_latest_image()

    cap.release()
    cv2.destroyAllWindows()

def process_latest_image():
    print(f"Checking for the most recent image in {folder_path}...")

    image_file = get_latest_image(folder_path)

    if not image_file:
        return

    print(f"The path of your most recent image is {image_file}. Proceeding...")

    try:
        img = Image.open(image_file)
    except Exception as e:
        print(f"Error: {e}")
        return

    pixel_data = list(img.getdata())
    pixel_bytes = bytearray()
    for pixel in pixel_data:
        if len(pixel) == 4:  # RGBA
            pixel_bytes.extend(pixel[:3])
        elif len(pixel) == 3:  # RGB
            pixel_bytes.extend(pixel)

    hex_string = pixel_bytes.hex()

    hash_object = hashlib.sha512()
    hash_object.update(hex_string.encode('utf-8'))
    hex_string = hash_object.hexdigest()

    with open(output_file, 'a') as f:
        f.write(hex_string + "\n\n") 

    print(f"Generated string: {hex_string}")

if __name__ == "__main__":
    capture_images()
