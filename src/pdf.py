#!/usr/bin/env python
# coding:utf-8


from pdfminer.pdfparser import PDFParser
from pdfminer.pdfparser import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfparser import PDFPage
from pdfminer.pdfdevice import PDFDevice
from pdfminer.converter import PDFPageAggregator
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.layout import LTChar, LTText, LTFigure, LTImage, LTRect, LTCurve, LTTextLineHorizontal
from argparse import ArgumentParser, FileType
from io import StringIO, BytesIO
from PIL import Image

import logging
logger = logging.getLogger(__name__)

from pdf_ltimage import ImageWriter
from ocr import Ocr
from docgen import TxtWriter, DocWriter


class PdfPage:
    def __init__(self):
        self.ocr_img = None
        self.any_img = False
        self.rsrcmgr = None


    def process(self, layout, rsrcmgr):
        logger.debug("processing a page")
        logger.debug(layout)

        page_size = (int(layout.width), int(layout.height))
        self.ocr_img = Image.new('L', page_size)
        self.rsrcmgr = rsrcmgr

        texts = self._process_layout(layout)

        if self.ocr_img and self.any_img:
            ocr_img = self.ocr_img
            # all images are upside-down. flip it.
            #ocr_img = ocr_img.transpose(Image.FLIP_TOP_BOTTOM)

            result = self._do_ocr(ocr_img, "page.png")
            if result:
                texts.extend(result)

        return texts


    def _do_ocr(self, img, path):
        buf = BytesIO()
        img.save(buf, format="png")
        buf.seek(0)
        img.save(path)

        ocr = Ocr()
        rslt = ocr.process(buf)
        logger.debug(rslt)

        return [PageObj('text', (0, 0, 0, 0), texts = rslt['results'])]


    def _process_layout(self, layout):
        pobjs = []
        chars = {}
        for l in layout:
            if isinstance(l, LTChar):
                logger.debug(l)
                t = l.get_text()
                bl = int(l.y1)
                if bl not in chars:
                    chars[bl] = []
                chars[bl].append(l.get_text())
            elif isinstance(l, LTTextLineHorizontal):
                logger.debug(l)
                texts = list(filter(lambda s: s.strip(), l.get_text().split("\n")))
                if texts:
                    pobjs.append(PageObj('text', l.bbox, texts=texts))
            elif issubclass(type(l), LTText):
                logger.debug(l)
                texts = list(filter(lambda s: s.strip(), l.get_text().split("\n")))
                if texts:
                    pobjs.append(PageObj('text', l.bbox, texts=texts))
            elif isinstance(l, LTImage):
                logger.debug(l)

                if isinstance(layout, LTFigure) and \
                    (layout.matrix[1] != .0 or layout.matrix[1] != .0):
                    pass # skip rotated image bcs. ocr will fail.
                else:
                    # an image, so save it to the designated folder, and note it's place in the text 
                    #logger.debug(l)
                    iw = ImageWriter()
                    img, path = iw.extract_image(l)

                    if img:
                        # should scale
                        # should consider bounding box
                        nw = int(l.x1 - l.x0)
                        nh = int(l.y1 - l.y0)
                        if nw > 0 and nh > 0 and self.ocr_img:
                            img = img.resize((nw, nh), Image.ANTIALIAS)
                            self.ocr_img.paste(img, (int(l.x0), int(l.y0)))
                            self.any_img = True
                        pobjs.append(PageObj('image', l.bbox, image=img))

            elif isinstance(l, LTRect) or isinstance(l, LTCurve):
                pass
            elif isinstance(l, LTFigure):
                logger.debug(l)
                # LTFigure objects are containers for other LT* objects, so recurse through the children
                #text_content.append(parse_lt_objs(l.objs, page_number, images_folder, text_content))
                s = self._process_layout(l)
                if s:
                    pobjs.extend(s)

        for key, v in chars.items():
            if v:
                pobjs.append(PageObj('text', l.bbox, texts=[''.join(v),]))

        logger.debug(pobjs)

        return pobjs


class PageObj(object):
    def __init__(self, type, rect, texts = None, image = None):
        assert type in ('text', 'image')
        self.type = type
        assert len(rect) == 4
        self.rect = rect

        self.texts = None
        self.text_lines = None
        self.line_height = None
        self.text_style = None
        if texts:
            self.texts = texts
            self.text_lines = len(self.texts)
            self.line_height = (rect[3] - rect[1]) / (self.text_lines + (self.text_lines - 1) * .5)

        self.image = image

    def __repr__(self):
        return "%s %s %s %s %s\n" % (self.type, str(self.rect), str(self.line_height), str(self.texts), str(self.image))

    def write(self, writer):
        if self.type is 'text':
            if self.text_style and self.text_style[0] == 'h':
                for t in self.texts:
                    writer.add_heading(t, level=int(self.text_style[1]))
            else:
                for t in self.texts:
                    writer.add_paragraph(t)
        elif self.type is 'image':
            writer.add_image(self.image)


class PdfTxt(object):
    def __init__(self):
        pass

    def _make_pages(self, fp):
        # Create a PDF parser object associated with the file object.
        parser = PDFParser(fp)
        document = PDFDocument()
        parser.set_document(document)

        # Create a PDF document object that stores the document structure.
        # Supply the password for initialization.
        password=""
        document.set_parser(parser)
        document.initialize(password)

        # Create a PDF resource manager object that stores shared resources.
        rsrcmgr = PDFResourceManager()

        # Set parameters for analysis.
        laparams = LAParams()

        # Create a PDF page aggregator object.
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        pages = list(document.get_pages())
        return (device, interpreter, pages, rsrcmgr)

    def convert_to_txt(self, fp, prange = None):
        of = StringIO()
        writer = TxtWriter(of)

        self._convert(fp, writer, prange)

        of.seek(0)
        result = of.read()

        return result

    def convert_to_doc(self, fp, prange = None):
        of = BytesIO()
        writer = DocWriter(of)

        self._convert(fp, writer, prange)

        writer.close()

        of.seek(0)

        return of

    def _convert(self, fp, writer, prange):
        device, interpreter, pages, rsrcmgr = self._make_pages(fp)

        for page_no, page_1 in enumerate(pages):
            if prange and page_no not in prange:
                continue

            # interpreter page1
            interpreter.process_page(page_1)

            # receive the LTPage object for the page.
            # layoutの中にページを構成する要素（LTTextBoxHorizontalなど）が入っている
            layout = device.get_result()
            # logger.debug(layout)
            ppage = PdfPage()
            pobjs = ppage.process(layout, rsrcmgr)

            for po in sorted(pobjs, key=lambda o: o.rect[1], reverse=True):
                if po.line_height:
                    logger.debug(po.line_height)
                    if po.line_height > 15:
                        po.text_style = 'h1'
                    elif po.line_height > 13:
                        po.text_style = 'h2'
                po.write(writer)
            writer.add_page_break()


def main():
    parser = ArgumentParser()
    parser.add_argument('infile', nargs='?', type=FileType('rb'))
    args = parser.parse_args()

    logger.setLevel(logging.DEBUG)
    import pdf_ltimage
    pdf_ltimage.logger.setLevel(logging.DEBUG)

    o = PdfTxt()
    logger.debug(args)
    r = o.convert_to_txt(args.infile, prange=range(0,10))
    with open("result.txt", 'w') as f:
        f.write(r)
    #r = o.convert_to_doc(args.infile, prange=range(0,1))
    # with open("result.docx", 'wb') as f:
    #     f.write(r.read())

    logger.debug(r)


if __name__ == '__main__':
    main()
