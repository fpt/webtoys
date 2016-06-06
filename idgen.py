#!/usr/bin/env python
# coding:utf-8

from argparse import ArgumentParser
import sys
import random
import sys

class IdGen:

    baseVal = 36
    base62chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

    def __init__(self, baseval = 36):
        self.baseVal = baseval

    def checkParam(self, id_len, id_cnt):
        return id_cnt > self.baseVal ** id_len

    def getId(self, l):
        s = ''
        for i in range(l): 
            s += self.base62chars[random.randint(0, self.baseVal - 1)]
        return s

    def makeIdSet(self, id_len, id_cnt):
        s = set()

        cnt = 0

        while True:
            s.add(self.getId(id_len))
            cnt += 1
            if len(s) >= id_cnt:
                break

        sys.stderr.write("cnt : %d\n" % (cnt,))

        return s

def main():
    parser = ArgumentParser()
    parser.add_argument('length', action='store', nargs=1, help='id length', default=5, type=int)
    parser.add_argument('-c', '--count', action='store', nargs='?', default=1, type=int )
    parser.add_argument('-t', '--base36', action='store_true' )
    parser.add_argument('-s', '--base62', action='store_true' )
    args = parser.parse_args()

    id_cnt = args.count
    id_len = args.length[0]

    if args.base36:
        g = IdGen(36)
    else:
        g = IdGen(62)

    if g.checkParam(id_len, id_cnt):
        sys.stderr.write("Too short!!\n")
        sys.exit(1)

    s = g.makeIdSet(id_len, id_cnt)

    for i in s:
        print(i)

if __name__ == '__main__':
    main()

