#!/usr/bin/env python3
#
# Usage: $0 <input-text> ...
#    (uses fileinput)
#
# finds sentences in a text that meet the needs of a crossword theme:
#    - breakable into 3 parts on word boundaries
#    - first and last parts have same length
#    - middle part length is odd
#
# may require executing: nltk.download('punkt')


import fileinput
import nltk.data

size = 15


def sumlte(L, maxval, start_idx):
    if start_idx >= len(L):
        return 0, 0
    n = 0
    for i in range(start_idx, len(L)):
        if n + L[i] > maxval:
            return n, i
        else:
            n += L[i]
    return n, i+1


def words_only(sentence):
    sentence = ''.join(x.upper() for x in sentence if x.isalpha() or x.isspace())
    return sentence.split()


def main():
    sent_det = nltk.data.load('tokenizers/punkt/english.pickle')

    for S in sent_det.tokenize(' '.join(fileinput.input())):
        words = words_only(S)
        lens = [len(w) for w in words]
        if sum(lens) > 3*size or sum(lens) < 25:
            continue

        start = 0
        breakdowns = []
        while start < len(words):
            sumlens, nextstart = sumlte(lens, size, start)
            if sumlens == 0:
                break
            breakdowns.append((sumlens, start, nextstart, ' '.join(words[start:nextstart])))
            start = nextstart

        if len(breakdowns) < 3:
            continue

        if breakdowns[1][0] % 2 == 0:  # must be odd to fit with symmetry
            continue

        if breakdowns[0][0] != breakdowns[-1][0]:  # simple first/last symmetry
            continue

        nums = '/'.join(str(x[0]) for x in breakdowns)
        answers = '/'.join(x[3] for x in breakdowns)
        print('[%s] %s   %s' % (nums, ' '.join(S.split()), answers))

main()
