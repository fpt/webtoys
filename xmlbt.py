#!/usr/bin/env python
# coding:utf-8

from argparse import ArgumentParser
import sys
import random
import sys

from yattag import indent

class XmlBt:
    def beautify(self, instr, indent_text = False):
        # To indent_text = True
        outstr = indent(
            instr,
            indentation = '    ',
            newline = '\r\n',
            indent_text = indent_text
        )

        return outstr

def main():
    parser = ArgumentParser()
    parser.add_argument('ugly_xml', action='store', nargs=1, help='beautify subjective', default='', type=str)
    parser.add_argument('-t', '--indent-text', action='store_true' )
    args = parser.parse_args()

    indent_text = args.indent_text
    ugly_xml = args.ugly_xml[0]

    b = XmlBt()

    print(b.beautify(ugly_xml, indent_text = indent_text))

if __name__ == '__main__':
    main()

# http://stackoverflow.com/questions/749796/pretty-printing-xml-in-python