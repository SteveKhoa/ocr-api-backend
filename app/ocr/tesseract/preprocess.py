import cv2 as cv
import numpy as np
import imghdr
from PIL import Image


def load(raw_image: bytes) -> np.ndarray:
    """Read raw bytes of an image and return as a Numpy array"""

    accepted_exts = ["jpg", "png"]
    img_ext = imghdr.what(raw_image)
    if img_ext not in accepted_exts:
        raise NotImplementedError("img_ext: {} not supported".format(img_ext))

    pil = Image.open(raw_image).convert("RGB")
    np_img = np.array(pil)
    return np_img


def binarize(image: np.ndarray):
    """
    Return binary: white (background) and black (foreground) image
    """
    _, binary = cv.threshold(image, 0, 255, cv.THRESH_BINARY)
    return binary


def mask_nontext(image: np.ndarray) -> np.ndarray:  # ignore for now
    """
    Mask all non-textual parts of images into white color.
    """
    # note, nkhoa: difficult to implement
    # requires more research
    # and Tesseract is already able to distinguish
    # between text and non-text. so this might not be
    # critically important
    return image


def add_border(image: np.ndarray) -> np.ndarray:
    """
    Add a thin border (5 pixels) to each image.

    This is expected to improve the performance of Tesseract.
    """
    constant = 5

    image = cv.copyMakeBorder(
        image, constant, constant, constant, constant, cv.BORDER_CONSTANT, None, value=0
    )
    return image
