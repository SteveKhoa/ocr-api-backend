import cv2 as cv

def binarize(image):
    """
    Return binary: white (background) and black (foreground) image
    """
    _, binary = cv.threshold(image,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
    return binary


def mask_nontext(image):  # ignore for now
    """
    Mask all non-textual parts of images into white color.
    """
    # note, nkhoa: difficult to implement
    # requires more research
    # and Tesseract is already able to distinguish
    # between text and non-text. so this might not be
    # critically important
    return image


def add_border(image):
    """
    Add a thin border (5 pixels) to each image.

    This is expected to improve the performance of Tesseract.
    """
    constant = 5

    image = cv.copyMakeBorder(
        image, constant, constant, constant, constant, cv.BORDER_CONSTANT, None, value=0
    )
    return image