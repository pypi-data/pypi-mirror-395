#!/usr/bin/venv python3

"""
@author: M. Bernt

get gene orders from OGRe website
"""

import re
import sys
import urllib.error
import urllib.parse
import urllib.request


def getacc(desc):
    acc = None
    ogrespe = urllib.request.urlopen(
        "http://drake.physics.mcmaster.ca/cgi-bin/ogre/featurelist.pl?genome=%s" % desc
    )
    sm = re.search("(NC_\\d{6})", ogrespe.read())
    if sm is not None:
        acc = sm.group(1)
    ogrespe.close()
    if acc is None:
        sys.stderr.write("Couldn't determine accessision of %s\n" % desc)
    return acc


trna = set([])
genes = set(
    [
        "COX1",
        "COX2",
        "COX3",
        "CYTB",
        "ATP6",
        "ATP8",
        "12S",
        "16S",
        "ND1",
        "ND2",
        "ND3",
        "ND4",
        "ND4L",
        "ND5",
        "ND6",
        "A",
        "C",
        "D",
        "E",
        "F",
        "G",
        "H",
        "I",
        "K",
        "L1",
        "L2",
        "N",
        "M",
        "P",
        "Q",
        "R",
        "S1",
        "S2",
        "T",
        "V",
        "W",
        "Y",
    ]
)

orgeformdata = urllib.parse.urlencode([("trna_choice", "trna")])
ogre = urllib.request.urlopen(
    "http://drake.physics.mcmaster.ca/cgi-bin/ogre/go_str_print.cgi", orgeformdata
)
ogrelines = ogre.readlines()
ogre.close()

rexp = re.compile(
    "^</td></tr><td width=5><b>(\\d+)\\s*</b></td><td width=20><FONT COLOR=blue>(\\w+)\\s*</FONT></td><td width=10><FONT COLOR=blue>\\d+\\s*</FONT></td><td>(.*)"
)

for o in ogrelines:
    # print o
    om = rexp.match(o)
    if om is not None:
        i = om.group(1)
        a = om.group(2)
        acc = getacc(a)

        geneorder = om.group(3)
        geneorder = geneorder.replace("RNL", "16S").replace("RNS", "12S")
        geneorder = geneorder.split(",")
        gs = {}
        #        print geneorder
        for i in range(len(geneorder) - 1, -1, -1):
            geneorder[i] = geneorder[i].strip()
            if geneorder[i][0] == "-":
                s = "-"
                x = geneorder[i][1:]
            else:
                s = ""
                x = geneorder[i]

            if x == "L":
                x = "L1"
            elif x == "S":
                x = "S2"
            elif x == "S2":
                x = "S1"

            if x not in genes:
                sys.stderr.write("Unknown gene %s\n" % x)
                del geneorder[i]
                continue
            geneorder[i] = s + x
            try:
                gs[x] += 1
            except KeyError:
                gs[x] = 1

        if set(gs.keys()) != genes:
            sys.stderr.write("Non standard gene set in %s\n" % acc)
            sys.stderr.write(
                "\t not included %s\n" % " ".join(genes.difference(set(gs.keys())))
            )
            sys.stderr.write(">%s\n%s\n" % (acc, " ".join(geneorder)))
        elif len(genes) != len(geneorder):
            sys.stderr.write("\tNot %d genes (" % len(genes))
            for g in gs:
                if gs[g] != 1:
                    sys.stderr.write("%d x %s, " % (gs[g], g))
            sys.stderr.write(")\n")
            sys.stderr.write(">%s\n%s\n" % (acc, " ".join(geneorder)))
        else:
            sys.stdout.write(">%s\n%s\n" % (acc, " ".join(geneorder)))
