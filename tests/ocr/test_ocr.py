import app.ocr.router
import base64
from app.ocr.schemas import RequestBody
import json

import os

dir_path = os.path.dirname(os.path.realpath(__file__))


class Path:
    def __init__(self, path):
        this_file_path = os.path.dirname(os.path.realpath(__file__))
        self.path = os.path.join(this_file_path, path)

    def get(self):
        return self.path


def test_unit_read_ocr_line():
    file_path = Path("./data/h.test.png")

    with open(file_path.get(), "rb") as f:
        bin_img = f.read()

    b64 = base64.b64encode(bin_img)

    req = {
        "image": {"base64": b64.decode("utf-8")},
        "target": {"pattern": "3 reports weekly"},
        "pivot": {"pattern": "Secretary", "tightness": "0.5"},
    }

    req = RequestBody.OCRLineRequestBody.model_validate(req)
    res = app.ocr.router.read_ocr_line(req)

    expected_output = {
        "status": 200,
        "data": ["prepared 3 reports weekly for management"],
    }
    assert res.to_json() == expected_output


def test_unit_read_ocr_paragraph():
    file_path = Path("./data/h.test.png")

    with open(file_path.get(), "rb") as f:
        bin_img = f.read()

    b64 = base64.b64encode(bin_img)

    req = {
        "image": {"base64": b64.decode("utf-8")},
        "target": {"pattern": ", IL"},
    }

    req = RequestBody.OCRParagraphRequestBody.model_validate(req)
    res = app.ocr.router.read_ocr_paragraph(req)

    expected_output = {
        "status": 200,
        "data": [
            [
                ">",
                "K",
                "Bachelor Of Arts",
                "in History",
                "River Brook University,",
                "Chicago, IL",
                "Graduated Magna Cum Laude",
                "May 2015",
                "&",
            ],
            ["Redford & Sons, Chicago, IL."],
            ["Suntrust Financial, Chicago, IL"],
            [
                "(212) 204-5342",
                "Chicago, IL 60622",
                "davidperezagmail.com",
                "linkedin.com/in/davidperez",
            ],
        ],
    }
    assert res.to_json() == expected_output
