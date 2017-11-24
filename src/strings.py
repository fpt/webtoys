#!/usr/bin/env python
# -*- coding: utf-8 -*-


strings = {
    'en': {
        'site_title' : 'Web Toys',
        'nav_top' : 'Top',
        'dh_intro' : 'What\'s This?',
        'dd_intro' : 'Common tools for web developers.',
        'sh_hhdr' : 'HTTP Request Header',
        'sd_hhdr' : 'Check HTTP Request your browser is sending.',
        'sh_urle' : 'URL Encode/Decode',
        'sd_urle' : 'Apply Javascript encodeURI() or decodeURI()',
        'sh_unie' : 'Unicode Escape/Unescape',
        'sd_unie' : 'Apply Javascript escape() or unescape()',
        'sh_base' : 'Base64 Encoder/Decoder',
        'sd_base' : 'Apply Javascript window.atob/bota.',
        'sh_xmlbt' : 'XML Beautifier',
        'sd_xmlbt' : 'Pretty format XML',
        'sh_ids' : 'ID generator',
        'sd_ids' : 'Generate random IDs',
        'sh_pdfconv' : 'PDF converter',
        'sd_pdfconv' : 'Convert from PDF to Word or Text',
        'dh_pdfconv' : 'Usage',
        'dd_pdfconv' : 'This tool converts from PDF file to Word(docx) or Text file. Choose a PDF file to process.',
        'dd_pdfconv2' : 'NOTE: Currently page range is limited to 0-9.',
        'lb_pdfconv_choosepdf' : 'Choose a PDF file',
        'lb_pdfconv_preview' : 'Preview',
        'lb_pdfconv_format' : 'Output format',
        'lb_pdfconv_run' : 'Convert and Download',
        'sh_ocr' : 'OCR',
        'sd_ocr' : 'Extract text from image',
        'sh_diff' : 'Compare files',
        'sd_diff' : 'Compare contents of two files.',
        'dh_diff' : 'Usage',
        'dd_diff' : 'Drop two text or docx files. NOTE: both files must have the same type.',
    },
    'ja': {
        'site_title' : 'ウェブトイズ',
        'nav_top' : 'トップ',
        'dh_intro' : 'ここは何？',
        'dd_intro' : '仕事に役立つツールのコレクションです。',
        'sh_hhdr' : 'HTTP リクエストヘッダ確認',
        'sd_hhdr' : 'ブラウザが送信するHTMLリクエストヘッダを表示します。',
        'sh_urle' : 'URLエンコード・デコード',
        'sd_urle' : 'JavascriptのencodeURI()やdecodeURI()を使って、URL中の文字を変換します。',
        'sh_unie' : 'Unicodeエスケープ・アンケスケープ',
        'sd_unie' : 'Javascriptのescape()やunescape()を使って、URL中の文字を変換します。',
        'sh_base' : 'Base64エンコーダ・デコーダ',
        'sd_base' : 'Javascriptのatobやbotaを使って、文字列をBase64変換します。',
        'sh_xmlbt' : 'XML整形',
        'sd_xmlbt' : 'XMLを読みやすいインデントに整形します',
        'sh_ids' : 'ランダムID生成',
        'sd_ids' : 'ランダムなIDを生成します。',
        'sh_pdfconv' : 'PDF→ワード・テキスト変換',
        'sd_pdfconv' : 'PDFをワード・テキストに変換します。',
        'dh_pdfconv' : '使い方',
        'dd_pdfconv' : 'このツールはPDFをワード(docx)・テキストに変換します。変換したいPDFファイルを選択してください。',
        'dd_pdfconv2' : 'ご注意: 変換できるページ数の上限は10ページです。',
        'lb_pdfconv_choosepdf' : 'PDFファイルを選択',
        'lb_pdfconv_preview' : '変換プレビュー',
        'lb_pdfconv_format' : '出力形式',
        'lb_pdfconv_run' : '変換してダウンロード',
        'sh_ocr' : 'OCR',
        'sd_ocr' : '画像から文字を抽出します。',
        'sh_diff' : 'ファイル比較',
        'sd_diff' : '二つのファイルの内容を比較して差分をハイライトします。',
        'dh_diff' : '使い方',
        'dd_diff' : '2つのテキストファイル又はWord(docx)ファイルをドロップしてください。2つのファイルは同じ形式でなくてはなりません。',
    }
}


class Strings():
    def __init__(self, lang):
        if lang not in strings.keys():
            raise "invalid lang code"
        self._lang = lang


    @classmethod
    def get_lang(cls, lang):
        try:
            arr = [(lang.index(k), k) for k in strings.keys() if k in lang]
            arr = sorted(arr, key=lambda tup: tup[0])
            return arr[0][1]
        except ValueError as e:
            print(e)
            return 'en'


    def gettext(self, key):
        return strings[self._lang][key]
