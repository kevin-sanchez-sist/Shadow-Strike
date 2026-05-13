from PIL import Image
import os

def recortar_transparente(carpeta):
    for root, dirs, files in os.walk(carpeta):
        for file in files:
            if file.endswith('.png'):
                path = os.path.join(root, file)
                img = Image.open(path)
                img = img.crop(img.getbbox())  # recorta al bounding box no transparente
                img.save(path)
                print(f"Recortado: {path}")

recortar_transparente("Sprites\Knight")