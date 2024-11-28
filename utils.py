import exifread

def _extract_f_number(f_number):
    a, b = f_number.split('/')
    return int(a) / int(b)

def get_exif_data(image_path):
    raw_data = dict()
    with open(image_path, 'rb') as image_file:
        tags = exifread.process_file(image_file)
        for tag_name, tag_value in tags.items():
            if tag_name not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename'):
                if isinstance(tag_value, exifread.classes.IfdTag):
                    raw_data[tag_name] = tag_value.printable

        _default_value = 'N/A'
        _focale = f"{raw_data.get('EXIF FocalLength')} mm" if raw_data.get('EXIF FocalLength') else _default_value
        _f_number = _extract_f_number(raw_data['EXIF FNumber']) if '/' in raw_data.get('EXIF FNumber', '') else raw_data.get('EXIF FNumber', _default_value)

        selected_data = dict(
            date=raw_data.get('EXIF DateTimeOriginal', _default_value),
            exposure_time=raw_data.get('EXIF ExposureTime', _default_value),
            f_number=_f_number,
            focale=_focale,
            iso=raw_data.get('EXIF ISOSpeedRatings', _default_value),
            artist=raw_data.get('Image Artist', _default_value),
            camera_model=f'{raw_data.get("Image Make", "Analog")} {raw_data.get("Image Model", "")}'
        )


        return selected_data


if __name__ == '__main__':
    import os

    directory_path = "Z:\\projects_viewer\\coutainville"
    for file in os.listdir(directory_path):
        print(file)
        print(get_exif_data(f"{directory_path}\\{file}"))
