"""
Functions and Objects to manage Tesseract's Language Models.

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
    """Tesseract Language Model (Lang)

    This class is a wrapper for .traineddata files.

    For other Langs, please see:
    https://github.com/tesseract-ocr/tessdata_best
    """

    def __init__(self, source: str, name: str = None):
        local_filename = source.split("/")[-1] if name is None else name
        local_filename += ".traineddata"

        self.__source = source
        self.id = local_filename.split(".")[0]
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

    def free(self) -> None:
        """
        Free the associated data relating to this language model from disk
        """
        os.unlink(self.__local_path)

    def use(self) -> str:
        """Return language's unique id on disk"""
        return self.id


class DefaultLangs:
    """Default Tesseract Language Models

    This namespace contains default Langs ready for use.
    Available models support detection on different languages
    (eng_best, vie_best), math equations (equ_best), and
    orientation and script detection (osd_best).

    {name}_fast : fast models designed for performance
    {name}_best : best available models designed for accuracy"""

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
