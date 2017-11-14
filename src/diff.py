#!/usr/bin/env python
# coding:utf-8

import difflib

from argparse import ArgumentParser, FileType


class Diff(object):
    """Factory"""

    def __init__(self, fp):
        self.fp = fp
        self.document = Document()

    def add_heading(self, str, level=None):
        self.document.add_heading(str, level=level)

    def add_paragraph(self, str):
        self.document.add_paragraph(str)

    def add_image(self, img):
        img_bytes = BytesIO()
        img.save(img_bytes, format="png")
        img_bytes.seek(0)
        self.document.add_picture(img_bytes)

    def add_page_break(self):
        self.document.add_page_break()

    def close(self):
        self.document.save(self.fp)


def main():
    parser = ArgumentParser()
    args = parser.parse_args()
    
    text1 = """Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Integer
eu lacus accumsan arcu fermentum euismod. Donec pulvinar porttitor
tellus. Aliquam venenatis. Donec facilisis pharetra tortor.  In nec
mauris eget magna consequat convallis. Nam sed sem vitae odio
pellentesque interdum. Sed consequat viverra nisl. Suspendisse arcu
metus, blandit quis, rhoncus ac, pharetra eget, velit. Mauris
urna. Morbi nonummy molestie orci. Praesent nisi elit, fringilla ac,
suscipit non, tristique vel, mauris. Curabitur vel lorem id nisl porta
adipiscing. Suspendisse eu lectus. In nunc. Duis vulputate tristique
enim. Donec quis lectus a justo imperdiet tempus."""
    text1_lines = text1.splitlines()

    text2 = """Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Integer
eu lacus accumsan arcu fermentum euismod. Donec pulvinar, porttitor
tellus. Aliquam venenatis. Donec facilisis pharetra tortor. In nec
mauris eget magna consequat convallis. Nam cras vitae mi vitae odio
pellentesque interdum. Sed consequat viverra nisl. Suspendisse arcu
metus, blandit quis, rhoncus ac, pharetra eget, velit. Mauris
urna. Morbi nonummy molestie orci. Praesent nisi elit, fringilla ac,
suscipit non, tristique vel, mauris. Curabitur vel lorem id nisl porta
adipiscing. Duis vulputate tristique enim. Donec quis lectus a justo
imperdiet tempus. Suspendisse eu lectus. In nunc. """
    text2_lines = text2.splitlines()

    diff = difflib.ndiff(text1_lines, text2_lines)
    print('\n'.join(list(diff)))


if __name__ == '__main__':
    main()
