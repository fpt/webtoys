#!/usr/bin/env python
# coding:utf-8

from difflib import SequenceMatcher

from argparse import ArgumentParser, FileType


class TextDiff(object):
    """Factory"""

    def __init__(self):
        pass

    @classmethod
    def _enclose(cls, pre, s, post, consider_newline = False):
        if consider_newline:
            ss = s.split('\n')
            return '\n'.join([pre + s + post for s in ss])
        else:
            return pre + s + post

    def _compare_lines(self, la, lb):
        sa = '\n'.join(la)
        sb = '\n'.join(lb)
        ta_result = ''
        tb_result = ''

        str_diff_start = '<em class="str-diff">'
        str_diff_end = '</em>'

        s = SequenceMatcher(None, sa, sb)
        ta_idx = 0
        tb_idx = 0
        for block in s.get_matching_blocks():
            (a_idx, b_idx, nmatch) = block
            print("a[%d] and b[%d] match for %d elements" % block)
            diff_a = sa[ta_idx:a_idx]
            same_a = sa[a_idx:a_idx + nmatch]
            diff_b = sb[tb_idx:b_idx]
            same_b = sb[b_idx:b_idx + nmatch]
            if diff_a or diff_b:
                ta_result += self._enclose(str_diff_start, diff_a, str_diff_end, consider_newline = True)
            ta_result += same_a
            if diff_a or diff_b:
                tb_result += self._enclose(str_diff_start, diff_b, str_diff_end, consider_newline = True)
            tb_result += same_b
            ta_idx = a_idx + nmatch
            tb_idx = b_idx + nmatch
        return (ta_result.split('\n'), tb_result.split('\n'))

    def compare(self, ta_lines, tb_lines, linebreak = ''):
        ta_result = []
        tb_result = []
        diff_lines = []

        line_diff_start = '<span class="line-num line-diff">'
        line_diff_end = '</span>'
        line_same_start = '<span class="line-num line-same">'
        line_same_end = '</span>'

        def _do_lines(diff, same, block_prefix, idx):
            result = []
            if diff:
                result.append('<div class="diff-block ' + block_prefix + 'dl' + str(idx) + '">')
                result.extend([self._enclose(line_diff_start, s, line_diff_end) for s in diff])
                result.append('</div>')
            result.extend([self._enclose(line_same_start, s, line_same_end) for s in same])
            return result

        s = SequenceMatcher(None, ta_lines, tb_lines)
        ta_idx = 0
        tb_idx = 0
        for block in s.get_matching_blocks():
            (a_idx, b_idx, nmatch) = block
            print("a[%d] and b[%d] match for %d elements" % block)
            diff_a = ta_lines[ta_idx:a_idx]
            same_a = ta_lines[a_idx:a_idx + nmatch]
            diff_b = tb_lines[tb_idx:b_idx]
            same_b = tb_lines[b_idx:b_idx + nmatch]

            if diff_a or diff_b:
                diff_a, diff_b = self._compare_lines(diff_a, diff_b)

            ta_result.extend(_do_lines(diff_a, same_a, 'a', ta_idx))
            tb_result.extend(_do_lines(diff_b, same_b, 'b', tb_idx))

            ta_idx = a_idx + nmatch
            tb_idx = b_idx + nmatch
            diff_lines.append(('adl' + str(ta_idx), 'bdl' + str(tb_idx)))

        return (linebreak.join(ta_result), linebreak.join(tb_result), diff_lines)


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
    (text1p, text2p, diff_lines) = d.compare(text1.splitlines(), text2.splitlines())

    print('----')
    print(text1p.replace('>', '>\n'))
    print('----')
    print(text2p.replace('>', '>\n'))
    print('----')
    print(diff_lines)
    print('----')


if __name__ == '__main__':
    main()
