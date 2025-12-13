"""
@author: M. Bernt

get gene orders from a set of gb-files
@author: M. Bernt
@todo if no file is given -> take from db
"""

# import pickle
import sys
from optparse import OptionParser
from os import listdir
from os.path import isdir, isfile

from mitos import mito
from mitos.bedfile import bedfromfile
from mitos.gb import gbfromfile

usage = "usage: %prog [options] gbfiles"
parser = OptionParser(usage)
parser.add_option(
    "-o",
    "--outfile",
    action="store",
    type="string",
    metavar="FILE",
    help="write values to FILE (default: stdout)",
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
parser.add_option("--notrna", action="store_true", default=False, help="ignore tRNAs")
parser.add_option(
    "--ignore",
    action="append",
    type="string",
    metavar="NAME",
    help="ignore genes with name NAME",
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

# outfile and outdir given ?
if options.outfile is None:
    ohandle = sys.stdout
else:
    ohandle = open(options.outfile, "w")

wancy = ["trnW", "trnA", "trnN", "trnC", "trnY"]

trna = set(mito.trna)
genes = mito.prot + mito.rrna

if options.notrna:
    if not options.ignore:
        options.ignore = []
    options.ignore += trna

#    options.ignore.append("trnL")
#    options.ignore.append("trnS")

genes = set(genes + mito.trna)
if options.ignore:
    for i in options.ignore:
        try:
            genes.remove(i)
        except ValueError:
            break


def unique(lst):
    """
    contruct data and gene orders
    """
    i = 0

    while i < len(lst):
        if lst[i] == lst[(i + 1) % len(lst)]:
            del lst[i]
        else:
            i += 1

    return lst


for arg in files:
    if arg.endswith(".bed"):
        gb = bedfromfile(arg)

    else:
        gb = gbfromfile(arg)

    if not gb.is_allowed(options.atax, options.ftax):
        continue

    features = gb.getfeatures(atypes=["gene", "rRNA", "tRNA"], fnames=options.ignore)

    m = 1000
    M = 0
    for i in range(len(features)):
        if features[i].name in wancy:
            m = min(m, i)
            M = max(M, i)

    if M - m + 1 != len(wancy):
        sys.stderr.write(
            "No WANCY %d %d %d %s\n"
            % (m, M, len(wancy), str([x.name for x in features]))
        )
        continue

    name = options.atax[0].replace(" ", "_").replace("+", "p")
    for i in range(m, M + 1):
        if features[i].strand == -1:
            name += "-"
        else:
            name += "+"
        name += features[i].name

    strand = features[m].strand
    #     start = min(features[(m - 1) % len(features)].stop + 1, features[m].start)
    #     stop = max(features[(M + 1) % len(features)].start - 1, features[M].stop)
    start = features[m].start
    stop = features[M].stop

    f = open("%s.fas" % name, mode="a")
    f.write("> %s\n" % gb.accession)
    f.write("%s\n" % gb.sequence.subseq(start, stop, +1))
    f.close()

    f = open("%s.bed" % name, mode="a")
    for i in range(m, M + 1):
        features[i].start -= start
        features[i].stop -= start
        f.write("%s\n" % features[i].bedstr(gb.accession))
    f.close()


#     out = options.format
#     out = out.replace("%ap", gb.abspre(mito.prot))
#     out = out.replace("%a", gb.accession)
#     out = out.replace("%n", gb.name)
#     out = out.replace("%taxid", str(gb.taxid))
#     out = out.replace("%code", str(gb.transl_table))
#     out = out.replace("%s", str(gb.size))
#     out = out.replace("%g", " ".join(go))
#     out = out.replace("%t", " ".join(gb.taxonomy))
#     ohandle.write("%s\n" % out)

# for r in gb.references:
#    print r.authors, r.journal, r.title

# outfile and outdir given ?
if options.outfile is not None:
    ohandle.close()
