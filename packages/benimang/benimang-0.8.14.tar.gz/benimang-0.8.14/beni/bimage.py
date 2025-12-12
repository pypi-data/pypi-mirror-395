from PIL import Image

from .btype import XPath


def convert(imgFile: XPath, maxSize: int | None = None, format: str | None = None):
    if set([maxSize, format]) == {None}:
        raise Exception('至少需要一个有效参数')
    imgList: list[Image.Image] = []
    try:
        img = Image.open(imgFile)
        imgList.append(img)
        if maxSize:
            img.thumbnail((maxSize, maxSize))
        if format == 'JPEG' and img.mode != 'RGB':
            img = img.convert('RGB')
            imgList.append(img)
        img.save(imgFile, format)
    finally:
        for img in imgList:
            img.close()
        imgList.clear()
