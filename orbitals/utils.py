

def get_image_by_name(novaclient, name):
    images = novaclient.images.list()
    for image in images:
        if name in image.name:
            return image
