import pytesseract
from PIL import Image


class OCREngine:
    def __init__(self):
        pass

    def read(self, file_dir: str) -> str:
        input_img = Image.open(file_dir)
        str = repr(input_img)
        return str

if __name__ == "__main__":
    from tesseract.lang import vie_best

    print(vie_best)