#!/usr/bin/env python
# coding:utf-8

import os
from flask import Flask, render_template
from flask import request
from flask import Response
from idgen import IdGen
from xmlbt import XmlBt

import socket

app = Flask(__name__)
app.debug = True


@app.route('/', methods=["GET"])
def index():
    return render_template('index.html')

@app.route('/hhdr', methods=["GET"])
def hhdr_index():

    headers = { k : v for (k, v) in request.headers.items() }

    if 'DYNO' in os.environ:
        remote_addr = headers['X-Forwarded-For']
        headers = { k: v for k, v in headers.iteritems() if not k.startswith('X-Forwarded-') }
    else:
        remote_addr = request.remote_addr

    remote_host = None
    try:
        remote_host = socket.gethostbyaddr(remote_addr)[0]
    except:
        pass

    return render_template('hhdr_index.html',
            remote_addr=remote_addr,
            remote_host=remote_host,
            headers=headers )

@app.route('/base', methods=["GET"])
def base_index():
    return render_template('base_index.html')

@app.route('/urle', methods=["GET"])
def urle_index():
    return render_template('urle_index.html')

@app.route('/unie', methods=["GET"])
def unie_index():
    return render_template('unie_index.html')

@app.route('/xmlbt', methods=["GET"])
def xmlbt_index():
    return render_template('xmlbt_index.html')

@app.route('/xmlbt/beautify', methods=['POST'])
def xmlbt_beautify():
    orig = request.form['original']
    b = XmlBt()
    r = b.beautify(orig)
    return Response(r, mimetype='text/plain')

@app.route('/ids', methods=["GET"])
def ids_index():
    return render_template('ids_index.html')

@app.route('/ids/preview', methods=['POST'])
def ids_preview():
    preview_cnt = 5
    base = int(request.form['base'])
    idlen = int(request.form['idlen'])
    g = IdGen(base)
    ids = g.makeIdSet(idlen, preview_cnt)
    return Response("\n".join(ids), mimetype='text/plain')

@app.route('/ids/download', methods=['POST'])
def ids_download():
    base = int(request.form['base'])
    idlen = int(request.form['idlen'])
    idcnt = int(request.form['idcnt'])
    g = IdGen(base)

    if g.checkParam(idlen, idcnt) or idlen > 100 or idcnt > 1000000:
        return Response("Invalid parameter.", mimetype='text/plain')

    ids = g.makeIdSet(idlen, idcnt)

    headers = { "Content-Disposition" : "attachment; filename=generated_ids.txt" }
    def generate():
        for d in ids:
            yield d + '\n'
    return Response(generate(), headers=headers, mimetype='text/plain')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


# http://flask.pocoo.org/docs/0.11/patterns/streaming/
