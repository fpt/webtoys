#!/usr/bin/env python
# coding:utf-8

import sys,os
import socket
from flask import Flask, render_template, make_response, jsonify, send_file
from flask import request
from flask import Response
from io import BytesIO
from zipfile import ZipFile

sys.path.append('src')
from idgen import IdGen
from xmlbt import XmlBt
from ocr import Ocr
from pdf import PdfTxt


app = Flask(__name__)
app.debug = True


# index
@app.route('/', methods=["GET"])
def index():
    return render_template('index.html')

# HTTP Header
@app.route('/hhdr', methods=["GET"])
def hhdr_index():

    headers = { k : v for (k, v) in request.headers.items() }

    if 'DYNO' in os.environ:
        remote_addr = headers['X-Forwarded-For']
        headers = { k: v for k, v in headers.items() if not k.startswith('X-Forwarded-') }
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

# base64
@app.route('/base', methods=["GET"])
def base_index():
    return render_template('base_index.html')


# url encode
@app.route('/urle', methods=["GET"])
def urle_index():
    return render_template('urle_index.html')


@app.route('/unie', methods=["GET"])
def unie_index():
    return render_template('unie_index.html')


# xml beautify
@app.route('/xmlbt', methods=["GET"])
def xmlbt_index():
    return render_template('xmlbt_index.html')


@app.route('/xmlbt/beautify', methods=['POST'])
def xmlbt_beautify():
    orig = request.form['original']
    b = XmlBt()
    r = b.beautify(orig)
    return Response(r, mimetype='text/plain')


# ids
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


# OCR
@app.route('/ocr', methods=["GET"])
def ocr_index():
    return render_template('ocr_index.html')


@app.route('/ocr/process', methods=["POST"])
def ocr_process():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect('/ocr')
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect('/ocr')

        print(file)
        ocr = Ocr()
        res = ocr.process(file.stream)
        return jsonify(res)


# PDF to text
@app.route('/pdfconv', methods=["GET"])
def pdfconv_index():
    return render_template('pdfconv_index.html')


@app.route('/pdfconv/preview', methods=["POST"])
def pdfconv_preview():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect('/pdfconv')
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect('/pdfconv')

        print(file)
        pdf = PdfTxt()
        txt = pdf.convert_to_txt(file.stream, prange=range(0, 1))
        res = {'result' : txt}
        return jsonify(res)


@app.route('/pdfconv/convert', methods=["POST"])
def pdfconv_convert():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect('/pdfconv')
        file = request.files['file']
        print(file)
        if file.filename == '':
            flash('No selected file')
            return redirect('/pdfconv')

        file_fmt = request.form['file_fmt']
        print(file_fmt)

        print(file)
        memory_file = BytesIO()

        pdf = PdfTxt()
        if file_fmt == 'docx':
            doc = pdf.convert_to_doc(file.stream, prange=range(0, 10))

            fn = file.filename + '.docx'
            with ZipFile(memory_file, 'w') as zf:
                zf.writestr(fn, doc.read())
        else:
            txt = pdf.convert_to_txt(file.stream, prange=range(0, 10))

            fn = file.filename + '.txt'
            with ZipFile(memory_file, 'w') as zf:
                zf.writestr(fn, txt)

        memory_file.seek(0)
        return send_file(memory_file, attachment_filename='pdfconv.zip', as_attachment=True)


# Let's encrypt
@app.route('/.well-known/acme-challenge/9Z4E_EJmMOaZm7sOoWNVQxSGxjyURPCdlBJb1vA8_Uo', methods=["GET"])
def letsencrypt():
    return '9Z4E_EJmMOaZm7sOoWNVQxSGxjyURPCdlBJb1vA8_Uo.rq8s6XKxE74WK5RjTi-jsdMPGIEuiNVG9oIhE8IGgNI'

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


# http://flask.pocoo.org/docs/0.11/patterns/streaming/
