#!/usr/bin/env python
# coding:utf-8

import sys,os
import socket
from flask import Flask, Blueprint, g,render_template, make_response, jsonify, send_file
from flask import request, redirect
from flask import Response
from io import BytesIO
from zipfile import ZipFile

sys.path.append('src')

from idgen import IdGen
from xmlbt import XmlBt
from ocr import Ocr
from pdf import PdfTxt
from diff import TextDiff
from docreader import DocReader
from strings import Strings


app = Flask(__name__)
app.debug = True
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024

# http://flask.pocoo.org/docs/0.12/patterns/urlprocessors/
# https://stackoverflow.com/questions/25961711/flask-how-can-i-always-include-language-code-in-url
#bp = Blueprint('frontend', __name__, url_prefix='/<lang>')
bp = Blueprint('top', __name__)


# automatically inject values into a call for url_for()
@bp.url_defaults
def add_language_code(endpoint, values):
    if 'lang_code' in values or 'lang_code' not in g or not g.lang_code:
        return
    values['lang'] = g.lang_code


# executed right after the request was matched and can execute code based on the URL values.
@bp.url_value_preprocessor
def pull_lang_code(endpoint, values):
    if 'lang' in values:
        g.lang_code = values.pop('lang')
    else:
        g.lang_code = Strings.get_lang(request.headers.get('Accept-Language'))


# index
@bp.route('/', methods=["GET"])
def index():
    return render_template('index.html', s = Strings(g.lang_code) )


# HTTP Header
@bp.route('/hhdr', methods=["GET"])
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
@bp.route('/base', methods=["GET"])
def base_index():
    return render_template('base_index.html', s = Strings(g.lang_code) )


# url encode
@bp.route('/urle', methods=["GET"])
def urle_index():
    return render_template('urle_index.html', s = Strings(g.lang_code) )


@bp.route('/unie', methods=["GET"])
def unie_index():
    return render_template('unie_index.html', s = Strings(g.lang_code) )


# xml beautify
@bp.route('/xmlbt', methods=["GET"])
def xmlbt_index():
    return render_template('xmlbt_index.html', s = Strings(g.lang_code) )


@app.route('/xmlbt/beautify', methods=['POST'])
def xmlbt_beautify():
    orig = request.form['original']
    b = XmlBt()
    r = b.beautify(orig)
    return Response(r, mimetype='text/plain')


# ids
@bp.route('/ids', methods=["GET"])
def ids_index():
    return render_template('ids_index.html', s = Strings(g.lang_code) )


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
@bp.route('/ocr', methods=["GET"])
def ocr_index():
    return render_template('ocr_index.html', s = Strings(g.lang_code) )


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
@bp.route('/pdfconv', methods=["GET"])
def pdfconv_index():
    return render_template('pdfconv_index.html', s = Strings(g.lang_code) )


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


# PDF to text
@bp.route('/diff', methods=["GET"])
def diff_index():
    return render_template('diff_index.html', s = Strings(g.lang_code) )


@app.route('/diff/compare', methods=["POST"])
def diff_compare():
    def is_docx(file):
        docx_mime = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        return file.filename.endswith('.docx') and file.content_type == docx_mime
    def is_text(file):
        return file.content_type.startswith('text/')

    if request.method == 'POST':
        files = []
        for k, v in request.files.items():
            if k.startswith('file'):
                files.append(v)
        if not files or len(files) != 2:
            flash('Not enough files')
            return redirect('/diff')
        for f in files:
            if not f.filename:
                flash('No selected file')
                return redirect('/diff')

        file1, file2 = files
        body1 = None
        body2 = None
        print(file1)
        print(file2)
        if is_docx(file1) and is_docx(file2):
            dr = DocReader()
            body1 = list(dr.process(file1.stream))
            body2 = list(dr.process(file2.stream))
        elif is_text(file1) and is_text(file2):
            body1 = file1.stream.read().decode("utf-8").splitlines()
            body2 = file2.stream.read().decode("utf-8").splitlines()
        else:
            flash('unsupported.')

        td = TextDiff()
        file1_rslt, file2_rslt, diff_lines = td.compare(body1, body2)

        res = {
            'result' : 'ok',
            'left_filename' : files[0].filename,
            'left_result' : file1_rslt,
            'right_filename' : files[1].filename,
            'right_result' : file2_rslt,
            'diff_lines' : diff_lines,
        }
        return jsonify(res)


app.register_blueprint(bp, url_defaults={})
app.register_blueprint(bp, url_prefix='/ja', url_defaults={'lang': 'ja'})
#print(app.url_map)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


# http://flask.pocoo.org/docs/0.11/patterns/streaming/
