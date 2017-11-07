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
from pdfminer.layout import LTTextBox, LTTextBoxHorizontal, LTTextLine, LTFigure, LTImage
from argparse import ArgumentParser, FileType
from binascii import b2a_hex

from .pdf_ltimage import ImageWriter


class PdfTxt:

    def _make_pages(self, fp):
        # Open a PDF file.
        #fp = open('sample.pdf', 'rb')

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
        return (device, interpreter, pages)

    def _process_layout(self, layout):
        texts = []
        for l in layout:
        #     print(l) # l is object
            if isinstance(l, LTTextBox):
                texts.append(l.get_text())
            elif isinstance(l, LTImage):
                # an image, so save it to the designated folder, and note it's place in the text 
                print(l)
                iw = ImageWriter()
                #iw.export_image(l)
            elif isinstance(l, LTFigure):
                print(l)
                # LTFigure objects are containers for other LT* objects, so recurse through the children
                #text_content.append(parse_lt_objs(l.objs, page_number, images_folder, text_content))
                self._process_layout(l)
        return texts

    def preview(self, fp):
        device, interpreter, pages = self._make_pages(fp)
        page_1 = pages[0]

        # interpreter page1
        interpreter.process_page(page_1)

        # receive the LTPage object for the page.
        # layoutの中にページを構成する要素（LTTextBoxHorizontalなど）が入っている
        layout = device.get_result()

        texts = self._process_layout(layout)

        return { 'results': texts }

    def convert(self, fp):
        device, interpreter, pages = self._make_pages(fp)

        texts = None

        for page_1 in pages:
            # interpreter page1
            interpreter.process_page(page_1)

            # receive the LTPage object for the page.
            # layoutの中にページを構成する要素（LTTextBoxHorizontalなど）が入っている
            layout = device.get_result()
            # print(layout)
            texts = self._process_layout(layout)

        return "\n".join(texts)


def main():
    parser = ArgumentParser()
    parser.add_argument('infile', nargs='?', type=FileType('rb'))
    args = parser.parse_args()

    o = PdfTxt()
    print(args)
    r = o.preview(args.infile)
    #r = o.convert(args.infile)
    print(r)


if __name__ == '__main__':
    main()
