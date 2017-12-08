#!/usr/bin/env python
# coding:utf-8

import pprint
import requests
from argparse import ArgumentParser, FileType
import json
import base64
import sys

import logging
logger = logging.getLogger(__name__)


class Ocr():
    def process(self, file):
        encoded_string = base64.b64encode(file.read()).decode('ascii')

        data = {
            "requests": [
                {
                    "image": {
                        "content": encoded_string
                    },
                    "features": [
                        { "type": "TEXT_DETECTION" },
                        { "type": "DOCUMENT_TEXT_DETECTION" }
                    ],
                    "imageContext": {
                        "languageHints": ["ja"]
                    }
                }
            ]
        }
        #print(data)
        #sys.exit(0)

        va_api_key = 'AIzaSyDb-qWQ62c-E0u_T6ia3iQaaTfNGeWhpfc'
        r = requests.post('https://vision.googleapis.com/v1/images:annotate',
                json.dumps(data),
                params = {'key':va_api_key},
                headers = {'Content-Type': 'application/json'} )
        resp = r.json()

        texts = []
        if 'responses' not in resp:
            texts.append('error: no response')
            texts.append(json.dumps(resp))
            return { 'results': texts }

        with open('gocr.json', 'w') as outfile:
            json.dump(resp, outfile)

        lines = self._analyze(resp)

        return { 'results': lines }

    def _analyze(self, resp):
        agr = Arranger()
        for r in resp['responses']:
            if 'textAnnotations' in r:

                for t in r['textAnnotations']:
                    if 'locale' in t:
                        continue

                    text = t['description']
                    bp = t['boundingPoly']['vertices']
                    xa = [v['x'] for v in bp]
                    ya = [v['y'] for v in bp]
                    rect = (min(xa), min(ya), max(xa), max(ya))
                    agr.append(text, rect)

        return agr.get_lines()


class Arranger():
    def __init__(self):
        self.hash = {}


    # rect = (left, top, right, botton)
    def append(self, text, rect):
        bl = rect[3]
        if bl not in self.hash:
            self.hash[bl] = []

        self.hash[bl].append((text, rect))


    def get_lines(self):
        bls = sorted(self.hash.keys())
        blc = []

        LINE_TOLERANCE = 3

        while len(bls) > 0:
            bl = bls.pop(0)
            if len(bls) != 0 and abs(bl - bls[0]) <= LINE_TOLERANCE:
                l = self.hash[bl]
                self.hash[bls[0]].extend(l)
            else:
                blc.append(bl)

        lines = []
        for b in blc:
            ln = self.hash[b]
            ln = sorted(ln, key = lambda c: c[1][0])
            avg_ch_w = sum([(s[1][2] - s[1][0]) / len(s[0]) for s in ln]) / len(ln)
            #lines.append(''.join([s[0] for s in ln]))

            st = ''
            for idx, s in enumerate(ln):
                if idx > 0 and s[1][0] - ln[idx - 1][1][2] > avg_ch_w:
                    st += ' '
                st += s[0]

            lines.append(st)
        return lines


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('infile', nargs='?', type=FileType('rb'))
    args = parser.parse_args()

    logger.setLevel(logging.DEBUG)

    ocr = Ocr()

    # r = ocr.process(args.infile)
    # print(r)
    # sys.exit(0)

    f = open('gocr.json', 'r')
    resp = json.load(f)
    ocr._analyze(resp)

