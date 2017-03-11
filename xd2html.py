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

    allClues = [ '<p class="header"><b>Across</b></p>' ]
    allClues.extend(across_clues)
    allClues.append('<p class="header"><b>Down</b></p>')
    allClues.extend(down_clues)

    nc = int(len(allClues)/4)

    hdrs["LeftClues"] = "\n".join(allClues[0:2*nc+1]) # first half
    hdrs["MiddleClues"] = "\n".join(allClues[2*nc+1:3*nc+1]) # third quarter
    hdrs["RightClues"] = "\n".join(allClues[3*nc+1:]) # rest

    grid_html = '<div><table id="grid">' # xml1.format(**hdrs)

    cells = xd.numberedPuzzle()
    for r, row in enumerate(cells):
        grid_html += '<tr id="r%d">' % r
        for c, cluenum in enumerate(row):
            classes = ""
            contents = ""
            if cluenum == "#":
                classes += 'block '
                grid_html += '<td id="r%dc%d" class="block"><div class="blockinner"><img src="blackdot.png"/></div></td>' % (c+1, r+1)
                continue
            elif cluenum:
                classes += 'numbered '
                contents = "%d" % cluenum

            grid_html += '<td id="r%dc%d" class="%s">%s</td>' % (c+1, r+1, classes, contents)
        grid_html += '</tr>'

    grid_html += "</table></div>"

    hdrs["Grid"] = grid_html
#    hdrs["ccxml"] = json.dumps(" ".join(ccxml.strip().split("\n")))

    return html1.format(**hdrs)

html1 = '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<HTML>
<HEAD>
<meta http-equiv="X-UA-Compatible" content="IE=edge"/>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />

<link rel="StyleSheet" type="text/css" href="style.css"/>

<title>Crossword {xdid}: {Title}</title>

</HEAD>
<BODY TEXT="#000000" BGCOLOR="#ffffff">

<div class="outertext">
<table class="crossword">
<tr><td>{notes}</td></tr>
<tr><td>
<h2>{Title}</h2>
<div>
    <span class="CopyTag">{Copyright}</span>
    <i> {Author} <br/>{Date} </i>
    <br/>
</div>
<br/>

<div id="PrintablePuz">

<table cellspacing="4" border="0" cellpadding="4" class="Clues">
<tr valign="top">
<td width="33%">{LeftClues}</td>
<td width="66%" class="grid">{Grid}
   <table cellspacing=4 border=0 cellpadding=4 class="clues">
   <tr valign="top">
      <td width="50%">{MiddleClues}</td>
      <td width="50%">{RightClues}</td>
   </tr>
   </table>
</td>
</tr>
</table>

</div>

</div>
</td></tr></table>

</div>

</body>
</html>
'''

xml1 = """
<?xml version="1.0" encoding="UTF-8"?>
<crossword-compiler-applet xmlns="http://crossword.info/xml/crossword-compiler-applet">
<applet-settings width="597" height="408" cursor-color="#FFFF00"
selected-cells-color="#C0C0C0" hide-numbers="false">
<clues layout="right" font-family="SansSerif" font-size="11" width="200" gutter="5"
selection-color="#FF0000" bold-numbers="true" right-align-numbers="false"
period-with-numbers="true">
</clues>
<actions buttons-layout="left" wide-buttons="false" graphical-buttons="false"></actions>
<completion friendly-submit="false" only-if-correct="true">
You solved the puzzle perfectly.  Nice job!
</completion></applet-settings>
<rectangular-puzzle xmlns="http://crossword.info/xml/rectangular-puzzle"
alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ"><metadata>
<title>{Title}</title>
<creator>{Author}</creator>
<copyright>{Date}</copyright>
<description>{Desc}</description>
</metadata>
<crossword>
<grid width="{width}" height="{height}">
<grid-look numbering-scheme="normal" cell-size-in-pixels="26" clue-square-divider-width="0.7">
</grid-look>"""

xml_acrosshdr = """<clues ordering="normal"><title><b>Across</b></title>"""
xml_downhdr = """</clues><clues ordering="normal"><title><b>Down</b></title>"""
xml_footer = """</clues> </crossword> </rectangular-puzzle> </crossword-compiler-applet>"""


def getNumber(cells, cellnum):
    for r, row in enumerate(cells):
        for c, cluenum in enumerate(row):
            if cellnum == cluenum:
                return r * width + c
    return 0


main(sys.argv[1])
