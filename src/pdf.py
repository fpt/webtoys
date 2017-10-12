#!/usr/bin/env python
# coding:utf-8

# 一括処理
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfparser import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfparser import PDFPage
from pdfminer.pdfdevice import PDFDevice
from pdfminer.converter import PDFPageAggregator
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.layout import LTTextBoxHorizontal

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

    def preview(self, fp):
        device, interpreter, pages = self._make_pages(fp)
        page_1 = pages[0]

        # interpreter page1
        interpreter.process_page(page_1)

        # receive the LTPage object for the page.
        # layoutの中にページを構成する要素（LTTextBoxHorizontalなど）が入っている
        layout = device.get_result()

        texts = []
        for l in layout:
        #     print(l) # l is object
            if isinstance(l, LTTextBoxHorizontal):
                texts.append(l.get_text())
        return { 'results': texts }

    def convert(self, fp):
        device, interpreter, pages = self._make_pages(fp)

        texts = []

        for page_1 in pages:
            # interpreter page1
            interpreter.process_page(page_1)

            # receive the LTPage object for the page.
            # layoutの中にページを構成する要素（LTTextBoxHorizontalなど）が入っている
            layout = device.get_result()
            # print(layout)

            for l in layout:
            #     print(l) # l is object
                if isinstance(l, LTTextBoxHorizontal):
                    texts.append(l.get_text())
        return "\n".join(texts)