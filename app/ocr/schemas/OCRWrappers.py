import bs4
import re
import random
from typing import Callable


class OCRLine:
    """Data wrapper of a line of text.

    In our application, a line of text is an atomic unit of OCR results. This
    is equivalently represented as `ocr_line` `<spans>` in `hOCR` standard.

    Attrs:
        bbox(list[int]): bounding-box of a token, [left top right bottom]
        words(list[str]): list of words in one token
    """

    def __init__(
        self,
        bbox: list[int, int, int, int],
        words: list[str],
        baseline: tuple[float, int],
    ):
        """

        Args:
            bbox (list[int, int, int, int]):
                top, left, right, bottom corners of token's bounding box
            words (list[str]):
                list of words in one token
            baseline (tuple[float, int]):
                baseline[0] is slope angle of the baseline
                baseline[1] is y-axis cross

        Notes:
            For more information on the properties, see hOCR specification
            of `ocr_line`. https://kba.github.io/hocr-spec/1.2
        """
        self.bbox = bbox
        self.text_line = " ".join(words)
        self.baseline = baseline

    def result(self):
        return {
            "OCRLine": {
                "bbox": self.bbox,
                "text_line": self.text_line,
                "baseline": self.baseline,
            }
        }


class OCRParagraph:
    """Data wrapper for a list of text lines.

    Attrs:
        lines(list[OCRLine]):
    """

    def __init__(
        self,
        *,
        parsed_elements: bs4.element.ResultSet = None,
        lines: list[OCRLine] = None
    ):
        """If `parsed_elements` is set, then `lines` parameter is ignored
        and this object is initialized by parsing `parsed_elements` to acquire
        individual lines. Otherwise, this object is initialized with `lines`.

        Args:
            parsed_elements (bs4.element.ResultSet, optional): Defaults to None.
            lines (list[OCRLine], optional): Defaults to None.
        """
        if parsed_elements is not None:
            self.lines = [
                OCRLine(
                    bbox=list(map(int, e["title"].split(";")[0].split(" ")[1:])),
                    words=[
                        word.string for word in e.find_all("span", class_="ocrx_word")
                    ],
                    baseline=tuple(e["title"].split(";")[1].split(" ")[2:]),
                )
                for e in parsed_elements
            ]
        else:
            self.lines = lines

    def result(self):
        return {"OCRParagraph": {"lines": [line.result() for line in self.lines]}}

    def get_textlines(self) -> list[str]:
        """Get a list of text lines as defined in this paragraph

        Returns:
            [line.text_line]: list of text_lines
        """
        text_lines = [line.text_line for line in self.lines]
        return text_lines

    def match(self, regex: re.Pattern) -> list[OCRLine]:
        """Returns a list of matched lines.

        A line is matched if it contains words that match the defined
        regex patterns.

        Args:
            regex (re.Pattern):

        Returns:
            matches (list[OCRLine])
        """
        matches = []
        for token in self.lines:
            # Match the pattern
            line = token.text_line
            match = regex.search(line)

            if match:
                matches += [token]

        return matches


class OCRPage:
    """Data wrapper for list of `OCRParagraph`s.

    `OCRPage` performs text-density clustering on parsed inputs from hOCR,
    i.e. it groups close text lines to form a paragraph, and assign different labels
    to different clusters (roughly paragraphs) to distinguish them.
    """

    def __init__(
        self,
        *,
        parsed_elements: bs4.element.ResultSet,
        cluster: Callable[[OCRParagraph], list[int]]
    ):
        ocr_lines = OCRParagraph(parsed_elements=parsed_elements)

        # Perform algorithm-specific token clustering
        # from an external callable.
        labels = cluster(ocr_lines)

        # Group tokens with the same labels
        # using Hash-table for fast lookup
        hash_table = {}
        for idx in range(len(labels)):
            label = labels[idx]
            token = ocr_lines.lines[idx]  # returns a token

            if label == 0:
                # Special label marked as lines that cannot be
                # grouped with other lines
                hash_table[random.randint(50, 999999)] = [token]
            elif label in hash_table:
                hash_table[label].append(token)
            else:
                hash_table[label] = [token]

        # Store the list of blocks
        self.paragraphs = [OCRParagraph(lines=hash_table[key]) for key in hash_table]

    def result(self):
        return {
            "OCRPage": {
                "paragraphs": [paragraph.result() for paragraph in self.paragraphs]
            }
        }

    def match(self, regex: re.Pattern) -> list[OCRParagraph]:
        """Returns a list of matched `TokensGroup`.

        A `TokensGroup` is matched if it contains a word that match the defined
        regex pattern.

        Args:
            regex (re.Pattern): _description_

        Returns:
            list[TokensGroup]: _description_
        """
        matches = []
        for block in self.paragraphs:
            if block.match(regex):
                matches.append(block)
            else:
                continue

        return matches
