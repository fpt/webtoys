#!/usr/bin/env python
# coding:utf-8


from argparse import ArgumentParser, FileType
from docx import Document
from docx.shared import Inches
from itertools import chain


class DocReader(object):
    """Factory"""

    def __init__(self):
        pass

    def process(self, fp, do_table = False):

        def process_paragraphs(doc):
            for p in doc.paragraphs:
                yield p.text.strip()

        def process_tables(doc):
            for tbl in doc.tables:
                print(tbl.part)
                print(parts_recur(tbl.part))
                for row in tbl.rows:
                    yield '\t'.join([c.text.strip() for c in row.cells])

        def parts_recur(part):
            for k, p in part.related_parts.items():
                print(k)
                print(p)
                print(p.partname)
                parts_recur(p)

        doc = Document(fp)
        if do_table:
            return chain(process_paragraphs(doc), process_tables(doc))
        else:
            return process_paragraphs(doc)

        part = doc.part
        print(part.partname)
        print(part.related_parts)
        parts_recur(part)
        return []


def main():
    parser = ArgumentParser()
    parser.add_argument('infile', nargs='?', type=FileType('rb'))
    args = parser.parse_args()

    dr = DocReader()
    text = '\n'.join(list(dr.process(args.infile, do_table=True)))
    print(text)

if __name__ == '__main__':
    main()
