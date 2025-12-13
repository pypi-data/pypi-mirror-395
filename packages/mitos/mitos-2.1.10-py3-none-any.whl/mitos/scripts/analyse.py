#!/usr/bin/venv python
"""
@author: M. Bernt

compare the features given in two files (gb or bed).
for each feature f2 from file2 the feature f1 from file1 is searched which
intersects most and f2 is covered more than the given cutoff.
coverage is computed as the size of the intersection / the length of the feature.

the output is:
accession, f1.name, f2.name, standdiff, f1.cover, f2.cover, f1.score, f2.score, dstart, dend, fs

where:
stranddiff: is +1 for same strand, -1 different strand
fX.cover: intersection/fX.length

dstart|dend f1start-f2start , resp. end
fs 1 if frameshift for proteins NA otherwise

if perfeature is NOT set then each gene family is treated as a whole.
an additional column is added to the output giving the difference of the number of
members of the gene family in file1 and file2.
"""

from optparse import OptionGroup, OptionParser
from os.path import splitext
from sys import exit, stderr

from mitos import feature, mitofile
from mitos.bedfile import bedfromfile
from mitos.gb import gbfromfile


def featurelist2map(lst):
    """
    create a dictionary for a list of features
    for each name one name one entry is created in the map containing
    1. pos : the position of the features with the name
    2. sgn : a sorted list of signs of the features with the name
    3. cnt : the number of features with the name
    3. scr : the sum of the scores of features with the name

    @param[in] lst a list of features
    """

    mp = {}
    for f in lst:
        if f.name not in mp:
            mp[f.name] = {}
            mp[f.name]["pos"] = set()
            mp[f.name]["sgn"] = None
            mp[f.name]["cnt"] = 0
            mp[f.name]["scr"] = 0
            mp[f.name]["start"] = 100000000
            mp[f.name]["stop"] = -1
            mp[f.name]["type"] = ""

        if f.strand > 0:
            mp[f.name]["start"] = min(f.start, mp[f.name]["start"])
            mp[f.name]["stop"] = max(f.stop, mp[f.name]["stop"])
        else:
            mp[f.name]["start"] = min(f.start, mp[f.name]["stop"])
            mp[f.name]["stop"] = max(f.stop, mp[f.name]["start"])

        mp[f.name]["pos"] = mp[f.name]["pos"].union(set(range(f.start, f.stop + 1)))
        if mp[f.name]["sgn"] is None or mp[f.name]["sgn"] == f.strand:
            mp[f.name]["sgn"] = f.strand
        else:
            f.strand = 0
        mp[f.name]["cnt"] += 1
        if f.score is None:
            mp[f.name]["scr"] += 0
        else:
            mp[f.name]["scr"] += f.score * (f.stop - f.start + 1)
        mp[f.name]["type"] = f.type

    #    for i in mp.keys():
    #        mp[i]["sgn"].sort()

    return mp


def flist2map(flist, length):
    """
    @param flist feature list
    @param length genome size
    @return pair fmap, pmap
            fmap[N][C] gives a list of parts belonging to feature with name N copy C,
            pmap gives the set of positions of the corresponding features
    """
    fmap = {}  # feature map
    pmap = {}  # position map

    for f in flist:
        if f.copy is not None:
            c = f.copy
        else:
            c = -1
        if f.name not in fmap:
            fmap[f.name] = {}
            pmap[f.name] = {}
        if c not in fmap[f.name]:
            fmap[f.name][c] = []
            pmap[f.name][c] = []

        fmap[f.name][c].append(f)

    for name in fmap:
        for copy in fmap[name]:
            fmap[name][copy].sort(key=lambda x: x.part)
            pmap[name][copy] = set()
            for p in fmap[name][copy]:
                pmap[name][copy].update(
                    feature.crange(p.start, p.stop, 1, True, length)
                )

    return fmap, pmap


def main():
    usage = "usage: %prog [options] ANNOTATION REFERENCE"
    parser = OptionParser(usage)

    parser.add_option(
        "-s",
        "--size",
        action="store",
        type="int",
        default=0,
        help="length of the sequence (mandatory for circular sequences)",
    )

    parser.add_option(
        "--linear",
        dest="circular",
        action="store_false",
        default=True,
        help="treat sequence as linear",
    )

    # parser.add_option( "--perfeature", action = "store_true", default = False, \
    #                    help = "analyse each feature separately; default: analyse featuresets with the same name" )
    #
    # parser.add_option( "--cutoff", action = "store", default = 0, type = "float", \
    #                    help = "festure intersection cutoff; default: 0" )

    # parser.add_option( "-T", dest = "ftax", action = "append", type = "string", metavar = "TAX", help = "forbid all entries with TAX in the taxonomy" )
    # parser.add_option( "-f", dest = "format", action = "store", type = "string", default = ">%a\n%g", metavar = "FORMAT", help = "output format: %n=name, %a=accession, %g=gene order" )
    # parser.add_option( "--improve", action = "store_true", default = False, help = "improve with arwen and tRNAscan from database" )
    # parser.add_option( "--ignore", action = "append", type = "string", metavar = "NAME", help = "ignore genes with name NAME" )
    # parser.add_option( "--notrna", action = "store_true", default = False, help = "ignore tRNAs" )
    group = OptionGroup(
        parser,
        "parameters to specify a subset of the features",
        "type can be tRNA, rRNA, and gene"
        "Note: -y,-Y,-n,-N can be specified more than once, combinations are possible.",
    )
    group.add_option(
        "-y",
        "--atype",
        action="append",
        type="string",
        metavar="TYPE",
        help="get all features of type TYPE",
    )
    group.add_option(
        "-Y",
        "--ftype",
        action="append",
        type="string",
        metavar="TYPE",
        help="get all features except features of type TYPE",
    )

    group.add_option(
        "-n",
        "--aname",
        action="append",
        type="string",
        metavar="NAME",
        help="get all features with name NAME",
    )
    group.add_option(
        "-N",
        "--fname",
        action="append",
        type="string",
        metavar="NAME",
        help="get all features except features with name NAME",
    )
    parser.add_option_group(group)

    (options, args) = parser.parse_args()

    if len(args) != 2:
        stderr.write("error: analyse needs two input files. %d given" % len(args))
        exit()

    size = options.size
    circular = options.circular

    ext = splitext(args[0])[1]
    if ext == ".gb":
        g = gbfromfile(args[0])
        size = g.size
        circular = g.circular
    elif ext == ".embl":
        g = gbfromfile(args[0])
        size = g.size
        circular = True
    elif ext == ".bed":
        g = bedfromfile(args[0])
    elif ext == ".mitos":
        g = mitofile.mitofromfile(args[0])

    bname = g.accession
    feat1 = g.getfeatures(
        anames=options.aname,
        fnames=options.fname,
        atypes=options.atype,
        ftypes=options.ftype,
    )

    ext = splitext(args[1])[1]
    if ext == ".gb":
        g2 = gbfromfile(args[1])
        size = g2.size
        circular = g2.circular
    elif ext == ".embl":
        g2 = gbfromfile(args[1])
        size = g2.size
        circular = True
    elif ext == ".bed":
        g2 = bedfromfile(args[1])
    elif ext == ".mitos":
        g2 = mitofile.mitofromfile(args[0])

    feat2 = g2.getfeatures(
        anames=options.aname,
        fnames=options.fname,
        atypes=options.atype,
        ftypes=options.ftype,
    )
    if bname is None:
        bname = g2.accession

    f1map, p1map = flist2map(feat1, size)
    f2map, p2map = flist2map(feat2, size)

    maxmap12 = {}
    for n1 in p1map:
        for c1 in p1map[n1]:
            maxcap = 0
            maxidx = -1
            for n2 in p2map:
                for c2 in p2map[n2]:
                    cap = len(p1map[n1][c1].intersection(p2map[n2][c2]))
                    if cap > maxcap:
                        maxcap = cap
                        maxidx = (n2, c2)
                    elif cap == maxcap and n1 == n2:
                        maxcap = cap
                        maxidx = (n2, c2)
            maxmap12[(n1, c1)] = maxidx
    #         print ( n1, c1 ), maxidx

    # print "==="
    maxmap21 = {}
    for n2 in p2map:
        for c2 in p2map[n2]:
            maxcap = 0
            maxidx = -1
            for n1 in p1map:
                for c1 in p1map[n1]:
                    cap = len(p2map[n2][c2].intersection(p1map[n1][c1]))
                    if cap > maxcap:
                        maxcap = cap
                        maxidx = (n1, c1)
                    elif cap == maxcap and n1 == n2:
                        maxcap = cap
                        maxidx = (n1, c1)
            maxmap21[(n2, c2)] = maxidx
    #         print ( n2, c2 ), maxidx

    for n1 in f1map:
        for c1 in f1map[n1]:

            f1length = len(p1map[n1][c1])
            f1start = f1map[n1][c1][0].start
            f1stop = f1map[n1][c1][-1].stop
            f1strand = f1map[n1][c1][0].strand
            if f1strand == -1:
                f1start, f1stop = f1stop, f1start

            if f1map[n1][c1][0].type == "gene":
                f1score = max([f.score for f in f1map[n1][c1]])
            else:
                f1score = min([f.score for f in f1map[n1][c1]])
            try:
                f1bits = max([f.bitscore for f in f1map[n1][c1]])
            except Exception:
                f1bits = "NA"

            if maxmap12[(n1, c1)] != -1 and maxmap21[maxmap12[(n1, c1)]] == (n1, c1):
                n2, c2 = maxmap12[(n1, c1)]
                f2length = len(p2map[n2][c2])
                f2start = f2map[n2][c2][0].start
                f2stop = f2map[n2][c2][-1].stop
                f2strand = f2map[n2][c2][0].strand
                if f2strand == -1:
                    f2start, f2stop = f2stop, f2start
                if f2map[n2][c2][0].type == "gene":
                    f2score = max([f.score for f in f2map[n2][c2]])
                else:
                    f2score = min([f.score for f in f2map[n2][c2]])
                try:
                    f2bits = max([f.bitscore for f in f2map[n2][c2]])
                except Exception:
                    f2bits = "NA"

                if n1 == n2 and f1strand == f2strand:

                    # f2 left of f1, i.e. f1 starts late -> < 0
                    if feature.length(f1start, f2start, circular, size) > size / 2:
                        dstart = -1 * (
                            feature.length(f2start, f1start, circular, size) - 1
                        )
                    else:
                        dstart = feature.length(f1start, f2start, circular, size) - 1

                    # f2 left of f1 -> > 0
                    if feature.length(f1stop, f2stop, circular, size) > size / 2:
                        dstop = feature.length(f2stop, f1stop, circular, size) - 1
                    else:
                        dstop = -1 * (
                            feature.length(f1stop, f2stop, circular, size) - 1
                        )

                    # for the inverse strand it must be reversed -> then + means
                    # feat1 in feat2
                    if f1start == -1:
                        dstart *= -1
                        dstop *= -1
                else:
                    dstart = "NA"
                    dstop = "NA"

                    # frameshift analysis only if genes
                if (
                    f1map[n1][c1][0].type == "gene"
                    and f2map[n2][c2][0].type == "gene"
                    and f1strand == f2strand
                    and ((f1start % 3 + 1) != (f2start % 3 + 1))
                ):
                    fs = (f1start % 3 + 1) - (f2start % 3 + 1)
                else:
                    fs = "NA"

                cap = p2map[n2][c2].intersection(p1map[n1][c1])

                print(
                    bname,
                    n1,
                    n2,
                    f1strand,
                    f2strand,
                    len(cap) / float(f1length),
                    len(cap) / float(f2length),
                    f1score,
                    f2score,
                    dstart,
                    dstop,
                    fs,
                    f1map[n1][c1][0].type,
                    f2map[n2][c2][0].type,
                    f1length,
                    f2length,
                    f1start,
                    f2start,
                    f1stop,
                    f2stop,
                    f1bits,
                    f2bits,
                    len(f1map[n1][c1]),
                    len(f2map[n2][c2]),
                )
            else:
                print(
                    bname,
                    n1,
                    "NA",
                    f1strand,
                    "NA",
                    "NA",
                    "NA",
                    f1score,
                    "NA",
                    "NA",
                    "NA",
                    "NA",
                    f1map[n1][c1][0].type,
                    "NA",
                    f1length,
                    "NA",
                    f1start,
                    "NA",
                    f1stop,
                    "NA",
                    f1bits,
                    "NA",
                    len(f1map[n1][c1]),
                    "NA",
                )

    # print the elements from feat2 which have no 'partner' in feat1
    for f2 in feat2:
        if f2.copy is not None:
            f2copy = f2.copy
        else:
            f2copy = -1

        if maxmap21[(f2.name, f2copy)] == -1:
            f2start = f2map[f2.name][f2copy][0].start
            f2stop = f2map[f2.name][f2copy][-1].stop
            f2strand = f2map[f2.name][f2copy][0].strand
            if f2strand == -1:
                f2start, f2stop = f2stop, f2start
            if f2map[f2.name][f2copy][0].type == "gene":
                f2score = max([f.score for f in f2map[f2.name][f2copy]])
            else:
                f2score = min([f.score for f in f2map[f2.name][f2copy]])
            try:
                f2bits = max([f.bitscore for f in f2map[f2.name][f2copy]])
            except Exception:
                f2bits = "NA"

            print(
                bname,
                "NA",
                f2.name,
                "NA",
                f2strand,
                "NA",
                "NA",
                "NA",
                f2score,
                "NA",
                "NA",
                "NA",
                "NA",
                f2.type,
                "NA",
                len(p2map[f2.name][f2copy]),
                "NA",
                f2start,
                "NA",
                f2stop,
                "NA",
                f2bits,
                "NA",
                len(f2map[n2][c2]),
            )

    # MAP[NAME][COPY][PART - sorted list]


if __name__ == "__main__":
    main()
