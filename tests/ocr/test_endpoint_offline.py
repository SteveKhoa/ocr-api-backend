import app.ocr.router
import base64
from app.ocr.schemas import RequestBody
import app.responses
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

    expected_output = app.responses.Collection(
        ["prepared 3 reports weekly for management"]
    )
    assert res.__dict__ == expected_output.__dict__


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

    expected_output = app.responses.Collection(
        [
            [
                "Bachelor Of Arts",
                "in History",
                "River Brook University,",
                "Chicago, IL",
                "Graduated Magna Cum Laude",
                "May 2015",
                "&",
            ],
            [
                "(212) 204-5342",
                "Chicago, IL 60622",
                "davidperez@gmail.com",
                "linkedin.com/in/davidperez",
            ],
            [
                "Administrative Assistant",
                "September 2019 - Present Redford & Sons, Chicago, IL",
                "e Schedule and coordinate meetings, appointments, and travel arrangements",
                "for supervisors and managers",
            ],
            [
                "Secretary Suntrust Financial, Chicago, IL",
                "June 2015 - August 2017",
                "e Recorded, transcribed and distributed weekly meetings",
                "e Answered upwards of 20 phone calls daily, taking detailed messages",
                "e Arranged appointments and ensured executives arrived to meetings with",
                "clients on time",
            ],
        ]
    )
    assert res.__dict__ == expected_output.__dict__
