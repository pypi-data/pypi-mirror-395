"""
@author: M. Bernt

get infos from a set of gb-files
"""

# import pickle
import sys
from optparse import OptionParser
from os import listdir
from os.path import isdir, isfile

from mitos.gb import gbfromfile

usage = "usage: %prog [options] gbfiles"
parser = OptionParser(usage)
parser.add_option(
    "-f",
    dest="format",
    action="store",
    type="string",
    default=">%a\n%g",
    metavar="FORMAT",
    help="output format: %n=name, %a=accession, %taxid: taxid, %c: code table, %s: size, %t: taxonomy string",
)
parser.add_option(
    "-t",
    dest="atax",
    action="append",
    type="string",
    metavar="TAX",
    help="allow only entries with TAX in the taxonomy",
)
parser.add_option(
    "-T",
    dest="ftax",
    action="append",
    type="string",
    metavar="TAX",
    help="forbid all entries with TAX in the taxonomy",
)

(options, args) = parser.parse_args()

# check arguments
# no input files / dirs given?
if len(args) == 0:
    print("no input file given")
    print(usage)
    sys.exit(1)

files = []  # input files
for arg in args:
    if isfile(arg):
        files.append(arg)
    elif isdir(arg):
        for f in listdir(arg):
            if isfile(arg + "/" + f):
                files.append(arg + "/" + f)
    else:
        sys.stderr.write("skipping %s\n" % arg)

if len(files) == 0:
    sys.stderr.write("no files given\n")
    sys.exit()


cc = {}
tot = 0

ac = {}
ptot = 0

for arg in files:
    if arg.endswith(".gb"):
        gb = gbfromfile(arg)

    #    sys.stderr.write("%s\n" % arg)
    if not gb.is_allowed(options.atax, options.ftax):
        continue

    for f in gb.getfeatures(atypes=["gene"]):
        ptot += len(f.translation)
        for a in str(f.translation):
            try:
                ac[a] += 1
            except KeyError:
                ac[a] = 1

        x = f.start

        while True:
            # print x, f.start, f.stop, f.strand
            if x > f.stop:
                break

            c = str(gb.sequence.subseq(x, x + 2, f.strand))

            try:
                cc[c] += 1
            except KeyError:
                cc[c] = 1
            print("..", c, x, f.strand, f.name, f.start, f.stop)
            tot += 1
            x += 3


for c in cc:
    print(c, cc[c], cc[c] / float(tot) * 100)

for a in ac:
    print(a, ac[a], ac[a] / float(ptot) * 100)
# print tot, ptot
