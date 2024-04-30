TESSDATA_DIR = "/Users/admin/Desktop/ocr-api-project/tess-experiments/tessconfig"
TESS_CONFIG = "/Users/admin/Desktop/ocr-api-project/tess-experiments/tessconfig/default"


from app.ocr.schemas.ImageWrappers import SourceImage, ImageRegion
from app.ocr.schemas.OCRWrappers import OCRLine, OCRParagraph, OCRPage
import sklearn.cluster
import numpy as np
import pytesseract
import bs4
import re


def __post_correct(hocr_parser: bs4.BeautifulSoup) -> bs4.BeautifulSoup:
    """Fix the uncorrected (low confidence) predicted tokens.

    This function enhaces accuracy of an ocr task.

    Args:
        hocr_parser (bs4.BeautifulSoup):

    Returns:
        bs4.BeautifulSoup:
    """

    # See this tool if I want to implement this function:
    # https://github.com/wolfgarbe/SymSpell

    return hocr_parser


def query_lines(
    *,
    image: SourceImage,
    pattern: str,
    pivot_pattern: str = None,
    tightness: float = 0.95,
    region: ImageRegion = None,
) -> list[OCRLine]:
    """Extract target lines matched by `pattern` from a specific `region` of
    the image, if they are spatially closed enough (controlled with `tightness`)
    to the pivot lines matched by `pivot_pattern`.

    If multiple pivot lines are matched, the closest line to those matched by
    `pattern` will be selected as the pivot lines.

    Args:
        image (SourceImage):
        pattern (str): regex pattern to match the target lines
        pivot_pattern (str): regex pattern the match the pivot lines
        tightness (float): value in range 0.0 to 1.0, used as a threshold to remove target lines that are too far from pivot lines.
        region (dict): region descriptor to extract subimage from image

    Return:
        matches(list[OCRLine]): a list of lines matched with the `pattern`
    """

    if tightness < 0.0 or tightness > 1.0:
        raise ValueError("Expect tightness in range 0.0 to 1.0.")

    if region is not None:
        subimage = region.extract(image)
    else:
        subimage = image

    hocr = pytesseract.image_to_pdf_or_hocr(
        subimage.source,
        extension="hocr",
        config=f"stdout --tessdata-dir {TESSDATA_DIR} {TESS_CONFIG}",
    )
    hocr_parser = bs4.BeautifulSoup(hocr, "html.parser")
    hocr_parser = __post_correct(hocr_parser)

    target_regex = re.compile(pattern)
    pivot_regex = re.compile(pivot_pattern)

    token_elements = hocr_parser.find_all("span", class_="ocr_line")

    matches = []
    # Treat the entire page as a paragraph
    paragraph = OCRParagraph(parsed_elements=token_elements)
    targets = paragraph.match(target_regex)
    pivots = paragraph.match(pivot_regex)

    if targets is None:
        return matches

    # Compute distance between targets and the minimum distance pivot
    # then decide if the extraction is feasible or not
    if pivots is None:
        matches = targets
    else:
        for target in targets:
            distances = [image.spatial_distance(target, pivot) for pivot in pivots]
            distance = min(distances)  # we just need the closest pivot token
            score = 1 - distance  # compute score as complement

            if score < tightness:
                matches += []
            else:  # score >= tightness
                matches += [target]

    return matches


def query_paragraphs(
    *,
    image: SourceImage,
    pattern: str,
    region: ImageRegion = None,
) -> list[OCRParagraph]:
    """Extract text paragraphs containing words matched by `pattern`.

    Args:
        image (SourceImage):
        pattern (str): regex pattern to match the target paragraph
        region (dict): region descriptor to extract subimage from image
    """

    if region is not None:
        subimage = region.extract(image)
    else:
        subimage = image

    hocr = pytesseract.image_to_pdf_or_hocr(
        subimage.source,
        extension="hocr",
        config=f"stdout --tessdata-dir {TESSDATA_DIR} {TESS_CONFIG}",
    )
    hocr_parser = bs4.BeautifulSoup(hocr, "html.parser")
    hocr_parser = __post_correct(hocr_parser)

    token_elements = hocr_parser.find_all("span", class_="ocr_line")

    def cluster(token_list: OCRParagraph):
        """Perform line clustering based on top-left corner point
        of each token's bounding box using DBSCAN clustering algorithm
        on Euclidean space with 'manhattan' distance.

        Args:
            token_list (OCRParagraph):

        Returns:
            labels:
                a list of integers, starting from 0. Label 0 is a special line
                that can not be grouped with any other lines to form a paragraph.
        """

        # Get coordinates normalizer
        coor_normalizer = image.coordinate_normalizer()

        # Take top-left corner point as the representative of one token
        # in Euclidean space, as a basis for later clustering.
        data = np.asarray(
            [np.array(coor_normalizer(token.bbox[:2])) for token in token_list.lines]
        )

        # Perform token clustering using DBSCAN algorithm
        eps = 0.05
        metric = "manhattan"
        dbscan = sklearn.cluster.DBSCAN(eps, min_samples=2, metric=metric)
        labels = dbscan.fit(data).labels_ + 1

        return labels

    matches = []
    blocks = OCRPage(parsed_elements=token_elements, cluster=cluster)
    targets = blocks.match(re.compile(pattern))

    if targets:
        matches += targets
    else:
        pass

    return matches
