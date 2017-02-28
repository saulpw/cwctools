#!/usr/bin/env python3

from xdfile import utils, clues


def main():
    utils.get_args(desc='get wordlist from corpus')
    wordlist = set()
    for ca in clues():
        wordlist.add(ca.answer)

    for w in sorted(list(wordlist)):
        print(w)


main()
