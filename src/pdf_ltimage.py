#!/usr/bin/env python
import struct
import os
import os.path
import zlib
import math
from array import array

from io import BytesIO, StringIO
from PIL import Image
from PIL import ImageChops

from pdfminer.pdftypes import LITERALS_FLATE_DECODE, LITERALS_DCT_DECODE
from pdfminer.pdfcolor import LITERAL_DEVICE_GRAY
from pdfminer.pdfcolor import LITERAL_DEVICE_RGB
from pdfminer.pdfcolor import LITERAL_DEVICE_CMYK

from .ocr import Ocr


def decode_4bpp(line):
    for c in line:
        hi = c & 0xf0
        lo = (c & 0xf) << 4
        yield hi
        yield lo


##  ImageWriter
##
class ImageWriter(object):

    def __init__(self):
        pass

    def export_image(self, image):
        stream = image.stream
        filters = stream.get_filters()
        (width, height) = image.srcsize
        bits = image.bits
        print(filters)
        print(image.srcsize)
        print(bits)

        if len(filters) == 1 and filters[0] in LITERALS_FLATE_DECODE:
            path = image.name + '.png'
            raw_data = stream.get_rawdata()
            data = zlib.decompress(raw_data)

            line_len = (width + 1) >> 1
            buf = BytesIO()
            if bits == 4:
                for i in range(0, len(data), line_len):
                    line = data[i:i + line_len]
                    line = list(decode_4bpp(line))[:width]
                    buf.write(bytes(line))

            mode = 'L'
            img = Image.frombuffer(mode, image.srcsize, buf.getbuffer(), 'raw', mode, 0, 1)
            img = img.transpose(Image.FLIP_TOP_BOTTOM)

            buf = BytesIO()
            img.save(buf, format="png")
            buf.seek(0)
            ocr = Ocr()
            print(ocr.process(buf))

            img.save(path)
        elif len(filters) == 1 and filters[0] in LITERALS_DCT_DECODE:
            path = image.name + '.jpg'
            print(path)
            raw_data = stream.get_rawdata()
            ifp = BytesIO(raw_data)
            i = Image.open(ifp)
            i.save(path)
        return
