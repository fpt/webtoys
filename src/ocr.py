#!/usr/bin/env python
# coding:utf-8

import pprint
import requests
from argparse import ArgumentParser
import json
import base64
import sys

class Ocr():
    def process(self, file):
        #parser = ArgumentParser()
        #parser.add_argument('query', nargs='?', help='query string')
        #args = parser.parse_args()

        #qstr = unicode(args.query, sys.stdout.encoding)
        encoded_string = base64.b64encode(file.read()).decode('ascii')

        data = {
            "requests": [
                {
                    "image": {
                        "content": encoded_string
                    },
                    "features": [
                        {
                            "type": "TEXT_DETECTION"
                        }
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

        for re in resp['responses']:
            if 'fullTextAnnotation' in re:
              txt = re['fullTextAnnotation']['text']
              texts.append(txt)
            else:
              texts.append(json.dumps(re))
        return { 'results': texts }

if __name__ == '__main__':
    ocr = Ocr()
    ocr.process()
