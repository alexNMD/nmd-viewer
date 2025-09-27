import os
from PIL import Image
import piexif

import config

PROJECTS_PATH = config.PROJECTS_PATH

# Parcours des dossiers
projects_lst = os.listdir(PROJECTS_PATH)

for project in projects_lst:
    images_lst = os.listdir(f"{PROJECTS_PATH}/{project}")
    for i in images_lst:
        if not i.endswith(".webp"):
            image_path = f"{PROJECTS_PATH}/{project}/{i}"

            # Lecture de l'image
            image = Image.open(image_path)
            image_name_without_ext = os.path.splitext(i)[0]
            webp_path = f"{PROJECTS_PATH}/{project}/{image_name_without_ext}.webp"

            # Extraction des métadonnées (EXIF uniquement, pour les formats pris en charge comme JPEG)
            exif_data = image.info.get("exif")

            # Sauvegarde de l'image au format WebP
            image.save(webp_path, 'webp', optimize=True, quality=100)

            # Réintégration des métadonnées EXIF dans le fichier WebP (si présentes)
            if exif_data:
                piexif.insert(exif_data, webp_path)

            print(f"{image_path} traité")

            # Suppression de l'ancienne image
            os.remove(image_path)
