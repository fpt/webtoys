#!/usr/bin/env python
# coding:utf-8

import os
from flask import Flask, render_template
from flask import request
from flask import Response
from idgen import IdGen, makeIdSet

import socket

app = Flask(__name__)
app.debug = True


@app.route('/', methods=["GET"])
def index():
    return render_template('index.html')

@app.route('/base', methods=["GET"])
def base_index():
    return render_template('base_index.html')

@app.route('/ue', methods=["GET"])
def ue_index():
    return render_template('ue_index.html')

@app.route('/ids', methods=["GET"])
def ids_index():
    return render_template('ids_index.html')

@app.route('/hhdr', methods=["GET"])
def hhdr_index():
    remote_addr = request.remote_addr
    remote_host = None
    try:
        remote_host = socket.gethostbyaddr(remote_addr)
    except:
        pass

    return render_template('hhdr_index.html',
            remote_addr=remote_addr,
            remote_host=remote_host,
            headers=request.headers.items() )

@app.route('/ids/preview', methods=['POST'])
def ids_preview():
    preview_cnt = 5
    base = int(request.form['base'])
    idlen = int(request.form['idlen'])
    g = IdGen(base)
    ids = makeIdSet(g, idlen, preview_cnt)
    return "\n".join(ids)

@app.route('/ids/download', methods=['POST'])
def ids_download():
    base = int(request.form['base'])
    idlen = int(request.form['idlen'])
    idcnt = int(request.form['idcnt'])
    g = IdGen(base)

    if g.checkParam(idlen, idcnt) or idlen > 100 or idcnt > 1000000:
        return Response("Invalid parameter.", mimetype='text/plain')

    ids = makeIdSet(g, idlen, idcnt)

    headers = { "Content-Disposition" : "attachment; filename=generated_ids.txt" }
    def generate():
        for d in ids:
            yield d + '\n'
    return Response(generate(), headers=headers, mimetype='text/plain')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


# http://flask.pocoo.org/docs/0.11/patterns/streaming/
