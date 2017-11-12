#!/usr/bin/env python
import struct
import os
import os.path
import zlib
import math
from array import array
from pprint import pprint

from io import BytesIO, StringIO
from PIL import Image, ImageOps, ImageChops

from pdfminer.pdftypes import LITERALS_FLATE_DECODE, LITERALS_DCT_DECODE, PDFObjRef
from pdfminer.pdfcolor import LITERAL_DEVICE_GRAY, LITERAL_DEVICE_RGB, LITERAL_DEVICE_CMYK

import logging

logger = logging.getLogger(__name__)


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

    def extract_image(self, image):
        stream = image.stream
        filters = stream.get_filters()
        (width, height) = image.srcsize
        bits = image.bits
        colorspace = image.colorspace
        logger.debug(filters[0])
        logger.debug(image.srcsize)
        logger.debug(bits)
        logger.debug(image.colorspace)
        logger.debug(image.imagemask)

        if len(filters) == 1 and filters[0] in LITERALS_FLATE_DECODE:
            path = image.name + '.png'
            raw_data = stream.get_rawdata()
            data = zlib.decompress(raw_data)

            img = None
            if bits == 4:
                buf = BytesIO()
                line_len = (width + 1) >> 1
                for i in range(0, len(data), line_len):
                    line = data[i:i + line_len]
                    line = list(decode_4bpp(line))[:width]
                    buf.write(bytes(line))
                mode = 'L'
                img = Image.frombuffer(mode, image.srcsize, buf.getbuffer(), 'raw', mode, 0, 1)
                # NOTE: this image is vertically flipped.
                img = img.transpose(Image.FLIP_TOP_BOTTOM)
            elif bits == 8:
                if colorspace[0] == LITERAL_DEVICE_GRAY:
                    mode = 'L'
                elif colorspace[0] == LITERAL_DEVICE_RGB:
                    mode = 'RGB'
                elif isinstance(colorspace[0], PDFObjRef):
                    o = colorspace[0].resolve()
                    if any([x == LITERAL_DEVICE_CMYK for x in o]):
                        mode = 'CMYK'
                        # giving up
                        # TODO: impl
                        return (None, None)
                img = Image.frombytes(mode, image.srcsize, data, 'raw', mode, 0, 1)
                #img = img.transpose(Image.FLIP_TOP_BOTTOM)
                img = ImageOps.invert(img)

            return (img, path)
        elif len(filters) == 1 and filters[0] in LITERALS_DCT_DECODE:
            path = image.name + '.jpg'
            logger.debug(path)
            raw_data = stream.get_rawdata()
            ifp = BytesIO(raw_data)
            img = Image.open(ifp)
            #img = img.transpose(Image.FLIP_TOP_BOTTOM)
            return (img, path)
        elif isinstance(filters[0], PDFObjRef):
            ref = filters[0]
            obj = ref.resolve()
            logger.debug(obj)
            # TODO: hmm?

        return (None, None)
