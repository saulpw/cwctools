#!/usr/bin/env python3

# find grid templates from gxd compatible with the given unfilled grid

from xdfile import utils, UNKNOWN_CHAR, BLOCK_CHAR
import xdfile
import copy


def fit_template(tmpl, xd):
    newg = []
    for r, row in enumerate(tmpl):
        newg.append('')
        for c, tmplch in enumerate(row):
            gridch = xd.cell(r, c)
            if tmplch == xdfile.BLOCK_CHAR:  # template block
                if gridch not in [ UNKNOWN_CHAR, BLOCK_CHAR ]:
                    return None
                else:
                    newg[-1] += tmplch

            elif gridch != xdfile.UNKNOWN_CHAR:  # fixed letter
                if tmplch not in [ gridch, UNKNOWN_CHAR ]:
                    return None
                else:
                    newg[-1] += gridch

            else:
                newg[-1] += xdfile.UNKNOWN_CHAR

    ret = copy.copy(xd)
    ret.grid = newg
    return ret


def main():
    args = utils.get_args(desc='find grid templates')

    templates = set()

    for xd in xdfile.corpus():
        tmpl = tuple(''.join(x if x == BLOCK_CHAR else UNKNOWN_CHAR for x in L) for L in xd.grid)
        templates.add(tmpl)

    print(len(templates), 'templates')
#    print('\n'.join(templates.pop()))

    for input_source in args.inputs:
        for fn, contents in utils.find_files(input_source, ext='.xd'):
            xd = xdfile.xdfile(contents.decode('utf-8'), fn)
            for T in templates:
                griddedxd = fit_template(T, xd)
                if griddedxd:
                    print(griddedxd.to_unicode())


main()
