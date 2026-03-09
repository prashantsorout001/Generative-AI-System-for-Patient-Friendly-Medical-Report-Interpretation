from paddleocr import PaddleOCR

ocr = PaddleOCR(use_angle_cls=True, lang='en')

result = ocr.ocr("report.jpeg")

for line in result:
    print(line[1][0])