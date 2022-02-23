import os
import os.path


def get_img_paths(FILE_PATH):
    """
    When provided a path to a file of images, returns the path to each image inside.
    """
    img_paths = []
    valid_images = [".jpg", ".gif", ".png", ".tga"]
    for f in os.listdir(FILE_PATH):
        ext = os.path.splitext(f)[1]
        if ext.lower() not in valid_images:
            continue
        img_paths.append(os.path.join(FILE_PATH, f))
    return img_paths