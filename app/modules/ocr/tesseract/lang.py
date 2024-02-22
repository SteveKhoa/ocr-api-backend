"""
Functions and Objects to manage Tesseract's languages (models).

Provides several ready-to-use objects: eng_best, vie_fast, so on..

Importing this module for the first time can take
some time since all the .traineddata are downloaded
in import.
"""

# Conventional path to store .traineddata by Tesseract
TESSDATA_DIR = "/usr/share/tesseract-ocr/5/tessdata"

import requests
import shutil
import os


class Lang:
    """
    Wrapper for .traineddata files
    """

    def __init__(self, source: str, name: str = None):
        local_filename = (source.split("/")[-1] if name is None else name)
        local_filename += ".traineddata"

        self.__source = source
        self.name = local_filename.split(".")[0]
        self.__local_path = os.path.join(TESSDATA_DIR, local_filename)

        self.__fetch()

    def __fetch(self):
        local_exists = self.__check_exists()

        if not local_exists:
            # Directly stream (lazy downloading) self.__source into
            # the disk (via shutil.copyfileobj) without overflow main
            # memory.
            # https://stackoverflow.com/questions/16694907/download-large-file-in-python-with-requests
            with requests.get(self.__source, stream=True) as request:

                if request.status_code != 200:
                    raise ValueError("{} was not a valid URL.".format(self.__source))

                with open(self.__local_path, "wb") as f:
                    shutil.copyfileobj(request.raw, f)

    def __check_exists(self):
        return os.path.isfile(self.__local_path)

    def free(self):
        """
        Free the associated data relating to this language from disk
        """
        os.unlink(self.__local_path)


# English langs
eng_best = Lang(
    "https://github.com/tesseract-ocr/tessdata_best/raw/main/vie.traineddata",
    "eng_best",
)
eng_fast = Lang(
    "https://github.com/tesseract-ocr/tessdata_fast/raw/main/vie.traineddata",
    "eng_fast",
)

# Vietnamese langs
vie_best = Lang(
    "https://github.com/tesseract-ocr/tessdata_best/raw/main/vie.traineddata",
    "vie_best",
)
vie_fast = Lang(
    "https://github.com/tesseract-ocr/tessdata_fast/raw/main/vie.traineddata",
    "vie_fast",
)

# Math equations detection
equ_best = Lang(
    "https://github.com/tesseract-ocr/tessdata_best/raw/main/equ.traineddata",
    "equ_best",
)
equ_fast = Lang(
    "https://github.com/tesseract-ocr/tessdata_fast/raw/main/equ.traineddata",
    "equ_fast",
)

# Orientation and script detection
osd_best = Lang(
    "https://github.com/tesseract-ocr/tessdata_best/raw/main/osd.traineddata",
    "osd_best",
)
osd_fast = Lang(
    "https://github.com/tesseract-ocr/tessdata_fast/raw/main/osd.traineddata",
    "osd_fast",
)
