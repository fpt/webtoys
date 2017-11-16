#!/usr/bin/env python
# coding:utf-8

from difflib import SequenceMatcher

from argparse import ArgumentParser, FileType


class TextDiff(object):
    """Factory"""

    def __init__(self):
        pass

    def compare(self, ta, tb, linebreak = ''):
        ta_lines = ta
        tb_lines = tb

        ta_result = []
        tb_result = []

        s = SequenceMatcher(None, ta_lines, tb_lines)
        ta_idx = 0
        tb_idx = 0
        for block in s.get_matching_blocks():
            (a_idx, b_idx, nmatch) = block
            print("a[%d] and b[%d] match for %d elements" % block)
            ta_result.extend(['<span class="line-num line-diff">' + s + '</span>' for s in ta_lines[ta_idx:a_idx]])
            ta_result.extend(['<span class="line-num line-same">' + s + '</span>' for s in ta_lines[a_idx:a_idx + nmatch]])
            tb_result.extend(['<span class="line-num line-diff">' + s + '</span>' for s in tb_lines[tb_idx:b_idx]])
            tb_result.extend(['<span class="line-num line-same">' + s + '</span>' for s in tb_lines[b_idx:b_idx + nmatch]])
            ta_idx = a_idx + nmatch
            tb_idx = b_idx + nmatch

        return (linebreak.join(ta_result), linebreak.join(tb_result))


def main():
    parser = ArgumentParser()
    args = parser.parse_args()
    
    text1 = """Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Integer
eu lacus accumsan arcu fermentum euismod. Donec pulvinar porttitor
tellus. Aliquam venenatis. Donec facilisis pharetra tortor.  In nec
mauris eget magna consequat convallis. Nam sed sem vitae odio
pellentesque interdum. Sed consequat viverra nisl. Suspendisse arcu
metus, blandit quis, rhoncus ac, pharetra eget, velit. Mauris
urna. Morbi nonummy molestie orci. Praesent nisi elit, fringilla ac,
suscipit non, tristique vel, mauris. Curabitur vel lorem id nisl porta
adipiscing. Suspendisse eu lectus. In nunc. Duis vulputate tristique
enim. Donec quis lectus a justo imperdiet tempus."""
    text1_lines = text1.splitlines()

    text2 = """Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Integer
eu lacus accumsan arcu fermentum euismod. Donec pulvinar, porttitor
tellus. Aliquam venenatis. Donec facilisis pharetra tortor. In nec
mauris eget magna consequat convallis. Nam cras vitae mi vitae odio
pellentesque interdum. Sed consequat viverra nisl. Suspendisse arcu
metus, blandit quis, rhoncus ac, pharetra eget, velit. Mauris
urna. Morbi nonummy molestie orci. Praesent nisi elit, fringilla ac,
suscipit non, tristique vel, mauris. Curabitur vel lorem id nisl porta
adipiscing. Duis vulputate tristique enim. Donec quis lectus a justo
imperdiet tempus. Suspendisse eu lectus. In nunc. """
    text2_lines = text2.splitlines()

    d = TextDiff()
    (text1p, text2p) = d.compare(text1.splitlines(), text2.splitlines())

    print('----')
    print(text1p)
    print('----')
    print(text2p)
    print('----')


if __name__ == '__main__':
    main()
