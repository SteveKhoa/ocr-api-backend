
<!-- PROJECT LOGO -->
<br />
<div align="center">
  <img src="https://github.com/SteveKhoa/ocr-api-backend/blob/main/ocrapi.svg"> 
  <a href="https://github.com/SteveKhoa/hackhcmc">
    <h3 align="center">OCR API</h3>
  </a>

  <p align="center">
    A containerized web service for Optical Character Recognition. 
    
  Built with <a href="https://fastapi.tiangolo.com/">FastAPI</a>, <a href="https://www.sqlite.org/index.html">SQLite</a>, <a href="https://github.com/tesseract-ocr/tesseract">Google Tesseract OCR Engine</a>, and <a href="https://www.docker.com/">Docker</a>.
  </p>
</div>

## Distinctive features

- Improved accuracy from baseline Tesseract with [DBScan](https://en.wikipedia.org/wiki/DBSCAN) clustering algorithm.
- [Base64](https://datatracker.ietf.org/doc/html/rfc4648#section-4)-encoded images for interoperability.
- User input validation, including base64 and request body validations.
- Text-from-image queries capability.
- Pre-commit checking for development environment consistency
