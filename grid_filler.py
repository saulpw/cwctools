#!/usr/bin/env python3

# find grid templates from gxd compatible with the given unfilled grid

from xdfile import utils
import xdfile
import grid_potentials


def print_potential_grid(xd, pots):
    unfixed = []
    for r, row in enumerate(pots):
        for c, ch in enumerate(row):
            if ch:
                print('%2s ' % len(ch), end='')
            else:
                print('%2s ' % xd.cell(r,c), end='')
        print()


def main():
    args = utils.get_args(desc='show grid potentials')

    wordlist = grid_potentials.get_wordlist()
    for input_source in args.inputs:
        for fn, contents in xdfile.utils.find_files(input_source, ext='.xd'):
            xd = xdfile.xdfile(contents.decode('utf-8'), fn)

            pots, answers = grid_potentials.get_potentials(xd, wordlist)
            print_potential_grid(xd, pots)

            for key, v in sorted(answers.items(), key=lambda x:len(x[1][1])):
                pattern, matches = v
                if len(matches) < 10:
                    print(key, pattern, len(matches), ' '.join(matches))
                else:
                    print(key, pattern, len(matches))

if __name__ == '__main__':
    main()
