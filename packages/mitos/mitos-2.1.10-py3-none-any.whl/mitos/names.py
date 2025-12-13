"""
Created on Apr 12, 2016

get full names of all features

@author: maze
"""

import sys

from Bio import SeqIO


def parse(record):
    # print("%s %i" % (record.id, len(record)))

    locations = {}

    for f in record.features:
        if f.type not in ["tRNA", "tmRNA", "rRNA", "ncRNA", "gene", "CDS"]:
            continue

        loc = (f.location.start.position, f.location.end.position)
        if f.location not in locations:
            locations[loc] = set()

        for q in f.qualifiers:
            if q in ["gene", "product", "gene_synonym"]:
                for x in f.qualifiers[q]:
                    locations[loc].add(x)

    for loc in locations:
        print(";".join(locations[loc]))


if __name__ == "__main__":
    for record in SeqIO.parse(sys.argv[1], "genbank"):
        parse(record)
    pass
