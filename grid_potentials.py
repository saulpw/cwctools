#!/usr/bin/env python3

import sys
import xdfile
import string
from statistics import mean, pstdev, pvariance


def word_match(x, y):
    for a, b in zip(x, y):
        if b != '.':
            if a not in b:
                return False

    return True


def get_wordcells(xd):
    # returns mapping of cell coords to the specific across/down answers and position within them
    wordcells = {}   # [(r,c)] = [(across_clueid, pos), (down_clueid, pos)]

    for r, row in enumerate(xd.grid):
        for c, ch in enumerate(row):
            wordcells[(r,c)] = [ None, None ]

    for direction, num, answer, r, c in xd.iteranswers_full():
        if '.' in answer:
            if direction == 'A':
                acr_wordpos = 0
                while xd.cell(r, c+acr_wordpos) not in xdfile.NON_ANSWER_CHARS:
                    wordcells[(r, c+acr_wordpos)][0] = (direction+str(num), acr_wordpos)
                    acr_wordpos += 1

            elif direction == 'D':
                down_wordpos = 0
                while xd.cell(r+down_wordpos, c) not in xdfile.NON_ANSWER_CHARS:
                    wordcells[(r+down_wordpos, c)][1] = (direction+str(num), down_wordpos)
                    down_wordpos += 1

    return wordcells


def get_potentials(xd, wordlist, potentials=None):
    if potentials is None:  # no previous list
        potentials = []  # list of lists corresponding to grid

        for r, row in enumerate(xd.grid):
            potentials.append([])
            for c, ch in enumerate(row):
                potentials[-1].append(None)

    wordcells = get_wordcells(xd)

    answerlist = {}  # ['A64'] = ('E..O', [ 'ERGO', 'EGOO', ...])
    for direction, num, answer, r, c in xd.iteranswers_full():
        if '.' in answer:
            answer_union = []
            if direction == 'A':
                for i in range(0, len(answer)):
                    answer_union.append(potentials[r][c+i] or answer[i])
            elif direction == 'D':
                for i in range(0, len(answer)):
                    answer_union.append(potentials[r+i][c] or answer[i])

            matches = [w for w in wordlist[len(answer_union)] if word_match(w, answer_union)]
            key = direction+str(num)
            answerlist[key] = (answer, matches)

    for r, row in enumerate(xd.grid):
        for c, ch in enumerate(row):
            across, down = wordcells[(r,c)]
            if across:
                acr_key, acr_pos = across
                across_matches = answerlist[acr_key][1]
            else:
                across_matches = set()

            if down:
                down_key, down_pos = down
                down_matches = answerlist[down_key][1]
            else:
                down_matches = set()

            p = set([s[acr_pos] for s in across_matches])
            q = set([s[down_pos] for s in down_matches])
            potentials[r][c] = ''.join(sorted(x for x in (p & q) if x in string.ascii_uppercase))

    return potentials, answerlist

def solve_round(xd):
    pots, answers = get_potentials(xd, get_wordlist(), None)


def get_wordlist():
    allwords = open('allwords.txt', 'r').read().split()

    ret = {}   # wordlen -> [words]
    for w in allwords:
        if len(w) not in ret:
            ret[len(w)] = []

        ret[len(w)].append(w)

    return ret


def main():
    global args
    args = xdfile.utils.get_args(desc='show sorted list of grid potentials')

    wordlist = get_wordlist()

    print ("filename mean stdev var min_answer")
    for input_source in args.inputs:
        for fn, contents in xdfile.utils.find_files(input_source, ext='.xd'):
            xd = xdfile.xdfile(contents.decode('utf-8'), fn)

            pots, answers = get_potentials(xd, wordlist)

            all_pots = []
            unfixed = [len(ch) for row2 in pots for ch in row2 if ch]
            if unfixed:
                all_pots.append((xd, pots, answers, unfixed))
                matches_list = [x[1] for x in answers.values()]
                print ("%s %.02f %.02f %.02f %d" % (xd, mean(unfixed), pstdev(unfixed), pvariance(unfixed), min(len(x) for x in matches_list)))

    print ('\n--')

    for xd, pots, answers, unfixed in sorted(all_pots, key=lambda r: mean(r[3]), reverse=True):
        print ("%20s %.02f %.02f %.02f" % (xd, mean(unfixed), pstdev(unfixed), pvariance(unfixed)))


if __name__ == '__main__':
    main()
