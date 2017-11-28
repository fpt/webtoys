from unittest import TestCase
from nose.tools import ok_, eq_
import sys, os

sys.path.append('src')

from diff import TextDiff


class DiffTestCase(TestCase):
    def setUp(self):
        print('before test')

    def tearDown(self):
        print('after test')

    def test_diff_01(self):
        d = TextDiff()
        text1 = 'a\nb\nc'
        text2 = 'a\nd\nc'
        (text1p, text2p) = d.compare(text1.splitlines(), text2.splitlines())

        eq_(text1p, '<span class="line-num line-same">a</span><span class="line-num line-diff"><span class="str-diff">b</span></span><span class="line-num line-same">c</span>')
        eq_(text2p, '<span class="line-num line-same">a</span><span class="line-num line-diff"><span class="str-diff">d</span></span><span class="line-num line-same">c</span>')
