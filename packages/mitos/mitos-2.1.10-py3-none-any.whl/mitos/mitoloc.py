#!/usr/bin/venv python

"""
@author: M. Bernt

locates the closest sequenced mitogenome(s) for a given taxid

input are:

1. the files nodes.dmp and names.dmp found in the ncbi taxonomy
   data base (in ftp://ftp.ncbi.nih.gov/pub/taxonomy/taxdump.tar.gz)
2. a directory with genbank files

output:

for each valid taxid two files (taxid.fas and taxid.tax)   containing the
fasta formatted sequences and the list of taxids

optionally:

- a minimum number of mitogenomes to report
- a directory where the ouput files are written (default is working directory)


genbank files can be obtained as a single file from:
ftp://ftp.ncbi.nlm.nih.gov/refseq/release/mitochondrion/mitochondrion.1.genomic.gbff.gz
this can be split into the separate files with refseqsplit.py

@author: maze
"""

import argparse
import logging
import os
import os.path
import sys

from mitos.gb import gbfromfile

usage = "search for closest mitogenomes"
parser = argparse.ArgumentParser(description=usage)

parser.add_argument("--gbdir", action="store", required=True, help="genbank directory")
parser.add_argument(
    "--names", action="store", required=True, help="names.dmp file to use"
)
parser.add_argument(
    "--nodes", action="store", required=True, help="nodes.dmp file to use"
)
parser.add_argument(
    "--dir",
    action="store",
    required=False,
    default=os.getcwd(),
    help="output directory",
)
parser.add_argument(
    "--min",
    action="store",
    type=int,
    default=1,
    help="minimum number of mitos required to report",
)

args = parser.parse_args()


def mitos_in_subtree(id, chld, taxidacc):
    cont = set()

    if id in chld:
        for c in chld[id]:
            cont.update(mitos_in_subtree(c, chld, taxidacc))
    else:
        if id in taxidacc:
            cont.add((id, taxidacc[id]))

    return cont


# crawl the gbdirectory and store accession to taxid mappings
acctaxid = {}
taxidacc = {}
accgb = {}

x = 0
for f in os.listdir(args.gbdir):
    if not os.path.isfile(args.gbdir + "/" + f):
        continue

    if not f.endswith(".gb"):
        continue

    gb = gbfromfile(args.gbdir + "/" + f)

    acctaxid[gb.accession] = gb.taxid
    taxidacc[gb.taxid] = gb.accession

    accgb[gb.accession] = gb
    x += 1
#     if x > 100:
#         break

# read the taxid name mapping. the two dictionaries nmsmap and taxmap
# map from id to name (nmsmap) and vice versa (taxmap)
nmsmap = {}
taxmap = {}
nmsdmp = open(args.names)
for line in nmsdmp.readlines():
    line = line.split("|")
    line = [x.strip() for x in line]
    line[0] = int(line[0])
    if not line[0] in nmsmap:
        nmsmap[line[0]] = line[1]

    taxmap[line[1]] = line[0]
nmsdmp.close()

# read the taxonomic tree
chld = {}
prnt = {}

rankmap = {}
ndsdmp = open(args.nodes)
for line in ndsdmp.readlines():
    line = line.split("|")
    line = [x.strip() for x in line]
    line[0] = int(line[0])
    line[1] = int(line[1])

    if line[1] != line[0]:
        try:
            chld[line[1]].append(line[0])
        except Exception:
            chld[line[1]] = [line[0]]
        prnt[line[0]] = line[1]
    elif line[0] != 1 or line[1] != 1:
        logging.error("cycle detected: \t%d \t%d" % (line[0], line[1]))

    if line[0] not in rankmap:
        rankmap[line[0]] = line[2]
    else:
        logging.error(
            "duplicate rank in nodes.dmp: \n\t%d %s\t%s"
            % (line[0], line[2], rankmap[line[0]])
        )
ndsdmp.close()

while 1:

    try:
        taxid = eval(input("enter taxid (exit = 0):"))
    except SyntaxError:
        continue

    if taxid == 0:
        break

    if taxid in nmsmap:
        sys.stdout.write("=> %s\n" % nmsmap[taxid])
    else:
        sys.stdout.write("no such leaf node\n")
        continue

    cid = taxid
    while 1:
        cont = mitos_in_subtree(cid, chld, taxidacc)
        sys.stdout.write("%s:%s %d\n" % (rankmap[cid], nmsmap[cid], len(cont)))

        if len(cont) >= args.min:
            f = open("%s/%d.tax" % (args.dir, taxid), "w")
            for c in cont:
                f.write("%d\n" % (c[0]))
            f.close()

            f = open("%s/%d.fas" % (args.dir, taxid), "w")
            for c in cont:
                f.write("> %s %d\n" % (c[1], taxid))
                f.write("%s\n" % (accgb[c[1]].sequence))
            f.close()

            break

        try:
            cid = prnt[cid]
        except Exception:
            break
