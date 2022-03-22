from shutil import copyfileobj


def load_images(image, file_name):
    with open(file_name, 'wb') as buffer:
        copyfileobj(image.file, buffer)
