from .OCRWrappers import OCRLine
from PIL import Image
import numpy as np
import base64
import io


class SourceImage:
    """Data wrapper for raw numpy.ndarray arrays

    Attributes:
        source(np.ndarray): store the raw numpy.ndarray representation of an image
    """

    def __init__(self, image: np.ndarray | str):
        """_summary_

        Args:
            image (np.ndarray | str): np.ndarray or base64 string.
        """
        if type(image) is np.ndarray:
            pass  # do nothing
        elif type(image) is str:
            try:
                # Throw exception if not valid base64
                base64.b64encode(base64.b64decode(image)) == image
            except Exception:
                raise Exception("image is not base64!")

            bin_img = base64.b64decode(image)
            image = np.array(Image.open(io.BytesIO(bin_img)))
        else:
            raise Exception("Invalid interface type")

        self.source = image

    def spatial_distance(self, line1: OCRLine, line2: OCRLine) -> float:
        """Compute normalized Euclidean distance between two OCRLine in
        image's spatial space.

        Args:
            tok1 (OCRLine):
            tok2 (OCRLine):

        Returns:
            distance(float): normalized (0.0 to 1.0) distance
        """
        height = self.source.shape[0]
        width = self.source.shape[1]

        tok1_norm_coord = np.array(
            [
                float(line1.bbox[0]) / width,
                float(line1.bbox[1]) / height,
                float(line1.bbox[2]) / width,
                float(line1.bbox[3]) / height,
            ]
        )

        tok2_norm_coord = np.array(
            [
                float(line2.bbox[0]) / width,
                float(line2.bbox[1]) / height,
                float(line2.bbox[2]) / width,
                float(line2.bbox[3]) / height,
            ]
        )

        # Compute Euclidean distance between box corners
        box_top_distance = np.linalg.norm(tok1_norm_coord[:2] - tok2_norm_coord[:2])
        box_bottom_distance = np.linalg.norm(tok1_norm_coord[2:] - tok2_norm_coord[2:])

        # Take the mean of box corners' distance
        distance = 0.5 * box_top_distance + 0.5 * box_bottom_distance

        return distance

    def coordinate_normalizer(self):
        """Return a high-order function as a coordinate normalizer.

        Coordinate normalizer is a function that maps a coordinate vector
        into the range between 0.0 and 1.0.
        """

        def normalizer(vector: list[int]) -> np.ndarray:
            img_dimens = self.source.shape[:-1][::-1]
            assert len(vector) == len(img_dimens)

            norm_coors = []
            for idx, coor in zip(range(len(img_dimens)), vector):
                norm_coor = float(coor) / float(img_dimens[idx])
                norm_coors.append(norm_coor)

            return norm_coors

        return normalizer


class ImageRegion:
    """Descriptor for an image region. Used to extract subimage from
    original `SourceImage`.
    """

    def __init__(self, left, top, right, bottom):
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom

    def extract(self, image: SourceImage) -> SourceImage:
        # Index checking
        if (
            self.left < 0
            or self.top < 0
            or self.right >= image.size[0]
            or self.bottom >= image.size[1]
        ):
            raise IndexError(f"Out-of-range indexes {image.shape}")

        subimage = image[self.left : self.right + 1][self.top : self.bottom + 1]
        return SourceImage(subimage)
