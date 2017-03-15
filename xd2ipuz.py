#!/usr/bin/env python3

import sys
import json
import xdfile
from xdfile.html import markup_to_html


def main(fn):
    with open(fn, 'r') as fp:
        xd = xdfile.xdfile(fp.read(), fn)

    ipuz = dict(version="http://ipuz.org/v1",
                kind=["http://ipuz.org/crossword#1"],
                dimensions=dict(width=xd.width(), height=xd.height()),
                title=''
                )

    ipuz.update(dict((k.lower(), v) for k, v in xd.headers.items()))

    puzzle = []
    for x in range(xd.height()):
        puzzle.append([None] * xd.width())

    for direction, cluenum, answer, r, c in xd.iteranswers_full():
        puzzle[r][c] = cluenum

    ipuz["puzzle"] = puzzle
    ipuz["clues"] = {
            "Across": [(pos[1], markup_to_html(clue)) for pos, clue, answer in xd.iterclues() if pos.startswith('A')],
            "Down": [(pos[1], markup_to_html(clue)) for pos, clue, answer in xd.iterclues() if pos.startswith('D')],
            }

    ipuz["solution"] = [list(row) for row in xd.grid]

    print(json.dumps(ipuz))

if __name__ == '__main__':
    main(sys.argv[1])
