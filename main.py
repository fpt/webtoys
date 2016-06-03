#!/usr/bin/env python
# coding:utf-8

import os
from flask import Flask, render_template
from flask import request
from idgen import IdGen, makeIdSet

app = Flask(__name__)
app.debug = True


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    base = int(request.form['base'])
    idlen = int(request.form['idlen'])
    idcnt = int(request.form['idcnt'])
    g = IdGen(base)
    ids = makeIdSet(g, idlen, idcnt)
    return render_template('result.html', ids=ids)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
