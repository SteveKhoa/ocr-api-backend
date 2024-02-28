"""Tesseract OCR Engine
"""

import pytesseract
from . import lang, preprocess, postprocess
import numpy as np


class TesseractOCR:
    """
        The TesseractOCR class is a Python wrapper for Tesseract,
    an optical character recognition (OCR) engine developed
    by Google. This class provides a convenient interface to
    extract text from images using Tesseract, with additional
    preprocessing and postprocessing steps to enhance accuracy
    and reliability.
    """

    def __init__(self, tesseract_lang: lang.Lang):
        self._lang = tesseract_lang

    def read(self, np_image: np.ndarray) -> str:
        """Extract text from input image

        This method assumes the input image contains uniform block of text."""

        # Load image
        image = np_image

        # Preprocessing
        binary_image = preprocess.binarize(image)
        masked_image = preprocess.mask_nontext(binary_image)
        bordered = preprocess.add_border(masked_image)

        # Extract string from image
        # This engine assumes that the input image contains a uniform block of text
        dataframe = pytesseract.image_to_data(
            image, lang=self._lang.use(), config="--psm 6", output_type="data.frame"
        )

        # Postprocessing
        dataframe = postprocess.correct_text(dataframe)
        text = postprocess.get_text(dataframe)

        return text
