import re
import os
from datetime import datetime

from PIL import Image
import piexif

from nmdviewer import config

from fractions import Fraction


class MetadataDTO:
    DEFAULT_VALUE = 'N/A'

    def __init__(self, entity: dict):
        self.focal = self.get_focal(entity.get('EXIF_FocalLength'))
        self.aperture = self.get_aperture(entity.get('EXIF_FNumber'))
        self.exposure_time = self.get_exposure_time(entity.get('EXIF_ExposureTime'))
        self.iso = entity.get('EXIF_ISOSpeedRatings', self.DEFAULT_VALUE)
        self.artist = entity.get('EXIF_Artist', self.DEFAULT_VALUE)
        self.camera_name = entity.get('EXIF_Make', 'Analog')
        self.camera_model = entity.get('EXIF_Model', '')
        self.camera = " ".join([self.camera_name, self.camera_model])
        self.date = self.get_date(entity.get('EXIF_DateTimeOriginal', ''))

    @classmethod
    def get_focal(cls, focal):
            return f"{round(cls._divide_numbers(focal))} mm" if focal else cls.DEFAULT_VALUE

    @classmethod
    def get_aperture(cls, aperture):
        return f"f/{cls._divide_numbers(aperture)}" if aperture else cls.DEFAULT_VALUE

    @classmethod
    def get_exposure_time(cls, value):
        if isinstance(value, tuple) and len(value) == 2:
            exposure = cls._divide_numbers(value)
        elif isinstance(value, Fraction):
            exposure = float(value)
        elif isinstance(value, (int, float)):
            exposure = float(value)
        else:
            try:
                exposure = float(Fraction(value.decode() if isinstance(value, bytes) else value))
            except Exception:
                return str(value)

        if exposure < 1:
            return f"1/{int(round(1 / exposure))} s"
        else:
            return f"{round(exposure, 2)} s"

    @classmethod
    def get_date(cls, date):
        try:
            date_obj = datetime.strptime(date, "%Y:%m:%d %H:%M:%S")
            return date_obj.strftime("%Y/%m/%d %H:%M:%S")
        except:
            return cls.DEFAULT_VALUE

    @staticmethod
    def _divide_numbers(numbers):
        try:
            if isinstance(numbers, str):
                a, b = numbers.split('/')
                return int(a) / int(b)
            elif isinstance(numbers, tuple):
                result = numbers[0] / numbers[1]
                return int(result) if result == int(result) else result
        except Exception:
            return numbers


def _decode_piexif_value(value):
    if isinstance(value, bytes):
        try:
            return value.decode("utf-8")
        except UnicodeDecodeError:
            try:
                return value.decode("latin-1")  # fallback
            except UnicodeDecodeError:
                return value
    return value

def get_exif_data(image_path):
    metadata = {}

    try:
        with Image.open(image_path) as img:
            metadata['format'] = img.format
            metadata['mode'] = img.mode
            metadata['size'] = img.size

            try:
                exif_dict = piexif.load(img.info.get("exif", b""))
                for ifd in exif_dict:
                    for tag_id, value in exif_dict[ifd].items():
                        value = _decode_piexif_value(value)
                        try:
                            tag_name = piexif.TAGS[ifd][tag_id]["name"]
                        except KeyError:
                            tag_name = tag_id
                        metadata[f"EXIF_{tag_name}"] = value
            except Exception:
                pass

    except Exception as e:
        print(f"Error Metadata: {e}")

    return MetadataDTO(metadata)

def get_projects():
    try:
        return [
            p.lower() for p in os.listdir(config.PROJECTS_PATH) if os.path.isdir(os.path.join(config.PROJECTS_PATH, p))
        ]
    except FileNotFoundError:
        return []

def is_valid_image(image_path):
    try:
        with Image.open(image_path) as img:
            img.verify()
            return True
    except (IOError, SyntaxError):
        return False

def get_images_metadata(project_selected):
    _project_path = os.path.join(config.PROJECTS_PATH, project_selected) if project_selected else config.PROJECTS_PATH
    _rgx = '\$(.*?)\$'

    try:
        images_lst = os.listdir(_project_path)
    except FileNotFoundError:
        images_lst = []

    return [
        dict(
            name=image,
            mobile_align=f"{re.search(_rgx, image).group(1)}%" if re.search(_rgx, image) else None,
            metadata=get_exif_data(f'{_project_path}/{image}')
        ) for image in [i for i in images_lst if is_valid_image(os.path.join(config.PROJECTS_PATH, project_selected, i))]
    ]

def get_template_context():
    return {
        "projects": get_projects(),
        "config": config
    }

if __name__ == '__main__':
    directory_path = "Z:\\projects_viewer\\coutainville"
    for file in os.listdir(directory_path):
        print(file)
        print(get_exif_data(f"{directory_path}\\{file}"))
