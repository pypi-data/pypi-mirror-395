#!/usr/bin/venv python

"""
@author: M. Bernt

remove a certain gene from the sequence and
"""

from optparse import OptionParser
from sys import exit, stderr, stdout

from mitos.gb import gbfromfile

usage = """%prog [options] fasta files/fasta directory"
    predicts proteins with blastx, and writes the aminoacid sequences

genetic code:
- if genbank file with same name is found the code specified there is assumed
- otherwise the genetic code specified with --code is assumed
circularity is assumed to circular per default:
- if genbank file with same name is found the circularity is taken from there
- otherwise default circularity is assumed (can be set to linear with --linear)
"""
parser = OptionParser(usage)
parser.add_option(
    "-n",
    "--aname",
    action="append",
    type="string",
    metavar="NAME",
    help="get all features with name NAME",
)
(options, args) = parser.parse_args()


if len(args) != 1:
    stderr.write("!= 1 file given\n")
    exit()

gb = gbfromfile(args[0])
features = gb.getfeatures(anames=options.aname)
features = sorted(features, key=lambda x: x.start)

print("> ", gb.accession, " - ", str(options.aname))
s = 0
for f in features:
    #    print f

    if f.start > 0:
        ss = gb.sequence.subseq(s, f.start - 1, 1)
        stdout.write("%s" % ss)
    s = f.stop + 1

if s < gb.size:
    ss = gb.sequence.subseq(s, gb.size - 1, 1)
    stdout.write("%s" % ss)

stdout.write("\n")
