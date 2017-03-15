#!/usr/bin/python3

# Usage: $0 <input>.xd
#
# outputs html to stdout

import xdfile.html
import xdfile
import sys
import json


def main(fn):
    for fn in sys.argv[1:]:
        print(to_html(xdfile.xdfile(open(fn).read(), fn)))


def to_html(xd):
    global width
    width = xd.width()

    hdrs = {
            'Title': '',
            'Copyright': '',
            'Author': '',
            'Checksum': '',
            'notes': xdfile.html.markup_to_html(xd.notes.replace('\n', '<br><br>'))
           }
    hdrs['height'] = xd.height()
    hdrs["xdid"] = xd.xdid()
    hdrs.update(xd.headers)

    across_clues = []
    down_clues = []

    for pos, clue, answer in xd.iterclues():
        clue_html = xdfile.html.markup_to_html(clue)
        if not answer:
            continue
        if pos[0] == 'A':
            across_clues.append('<p id="%s" class="clue"><b>%s.&nbsp;</b>%s</p>' % (pos, pos[1:], clue_html))
        elif pos[0] == 'D':
            down_clues.append('<p id="%s" class="clue"><b>%s.&nbsp;</b>%s</p>' % (pos, pos[1:], clue_html))

    allClues = ['<p class="header"><b>Across</b></p>']
    allClues.extend(across_clues)
    allClues.append('<p class="header"><b>Down</b></p>')
    allClues.extend(down_clues)

    nc = xd.height()+10

    hdrs["LeftClues"] = "\n".join(allClues[0:nc])
    hdrs["MiddleClues"] = "\n".join(allClues[nc:])
    hdrs["RightClues"] = ''

    grid_html = '<div><table id="grid">'

    cells = xd.numberedPuzzle()
    for r, row in enumerate(cells):
        grid_html += '<tr id="r%d">' % r
        for c, cluenum in enumerate(row):
            classes = ""
            contents = ""
            if cluenum == "#":
                classes += 'block '
                grid_html += '<td id="r%dc%d" class="block"><div class="blockinner"><img src="../blackdot.png"/></div></td>' % (c+1, r+1)
                continue
            elif cluenum:
                contents += '<span class="number">%d</span>' % cluenum

            contents += '<span class="cell" contenteditable="true"></span>'
            grid_html += '<td id="r%dc%d" class="%s">%s</td>' % (c+1, r+1, classes, contents)
        grid_html += '</tr>'

    grid_html += "</table></div>"

    hdrs["Grid"] = grid_html

    checksum = 0
    for row in xd.grid:
        for c in row:
            if c != '#':
                checksum += ord(c[0])

    hdrs["Checksum"] = checksum

    return html1.format(**hdrs)

html1 = '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<HTML>
<HEAD>
<meta http-equiv="X-UA-Compatible" content="IE=edge"/>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />

<link rel="StyleSheet" type="text/css" href="../style.css"/>

<title>Crossword {xdid}: {Title}</title>

</head>
<body>

<table class="crossword">
<!--tr><td>{notes}</td></tr-->
<tr><td>
<h2>{Title}</h2>
<span class="CopyTag">{Copyright}</span>
<i> {Author} <br/>{Date} </i>
<table id="main">
<tr>
    <td id="leftclues" class="clue">{LeftClues}</td>
    <td id="grid" checksum="{Checksum}">{Grid}</td>
</tr>
<tr>
    <td colspan="2" id="bottomclues" class="clue">
        {MiddleClues}{RightClues}
    </td>
</tr>
   </table>
</td>
</tr>
</table>

</td></tr></table>

</body>
</html>
'''


def getNumber(cells, cellnum):
    for r, row in enumerate(cells):
        for c, cluenum in enumerate(row):
            if cellnum == cluenum:
                return r * width + c
    return 0


main(sys.argv[1])
