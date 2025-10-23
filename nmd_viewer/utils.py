from datetime import datetime

import exifread

DEFAULT_VALUE = 'N/A'

class MetadataDTO:

    def __init__(self, entity: dict):
        self.focal = self.get_focal(entity.get('EXIF FocalLength'))
        self.aperture = self.get_aperture(entity.get('EXIF FNumber'))
        self.exposure_time = self.get_exposure_time(entity.get('EXIF ExposureTime'))
        self.iso = entity.get('EXIF ISOSpeedRatings', DEFAULT_VALUE)
        self.artist = entity.get('Image Artist', DEFAULT_VALUE)
        self.camera_name = entity.get('Image Make', 'Analog')
        self.camera_model = entity.get('Image Model', '')
        self.camera = self.camera_name + ' ' + self.camera_model
        self.date = self.get_date(entity.get('EXIF DateTimeOriginal'))

    @classmethod
    def get_focal(cls, focal):
        return f"{focal} mm" if focal else DEFAULT_VALUE

    @classmethod
    def get_aperture(cls, aperture):
        return f"f/{cls._divide_f_number(aperture)}" if aperture else DEFAULT_VALUE

    @classmethod
    def get_exposure_time(cls, exposure_time):
        _second_sign = '"'
        if exposure_time:
            return exposure_time if "/" in exposure_time else f"{exposure_time}{_second_sign}"
        else:
            return DEFAULT_VALUE

    @classmethod
    def get_date(cls, date):
        try:
            date_obj = datetime.strptime(date, "%Y:%m:%d %H:%M:%S")
            return date_obj.strftime("%Y/%m/%d %H:%M:%S")
        except:
            return DEFAULT_VALUE

    @staticmethod
    def _divide_f_number(f_number):
        try:
            a, b = f_number.split('/')
            return int(a) / int(b)
        except:
            return f_number


def get_exif_data(image_path):
    raw_data = dict()

    try:
        with (open(image_path, 'rb') as image_file):
            tags = exifread.process_file(image_file)
            for tag_name, tag_value in tags.items():
                if tag_name not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename'):
                    if isinstance(tag_value, exifread.classes.IfdTag):
                        raw_data[tag_name] = tag_value.printable
    except exifread.heic.NoParser:
        pass

    return MetadataDTO(raw_data)


if __name__ == '__main__':
    import os

    directory_path = "Z:\\projects_viewer\\coutainville"
    for file in os.listdir(directory_path):
        print(file)
        print(get_exif_data(f"{directory_path}\\{file}"))
