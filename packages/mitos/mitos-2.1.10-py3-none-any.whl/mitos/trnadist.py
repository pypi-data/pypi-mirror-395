import argparse
import itertools
import logging
import multiprocessing
import os.path
import pickle
import random
import re
import sys

import numpy

from mitos import mitofile, rna


def apply_statistics(allocomp, allocompdist, isocomp, isocompdist):
    """
    compute rank and z-score
    """

    #    isocomp[acc][ac].append( { "t1": c1, "t2":c2, "sim":compare( c1, c2 ), "wrt": acc } )
    #    isocompdist[ac]
    sys.stderr.write("iso stat\n")
    # precompute mean and std
    isomean = {}
    isostd = {}
    for ac in isocompdist:
        #        print ac, len( isocompdist[ac] )
        isomean[ac] = numpy.mean(isocompdist[ac])
        isostd[ac] = numpy.std(isocompdist[ac])

    for acc in isocomp:
        for ac in isocomp[acc]:

            for i in range(len(isocomp[acc][ac])):

                try:
                    isocomp[acc][ac][i]["z"] = (
                        isocomp[acc][ac][i]["sim"] - isomean[ac]
                    ) / isostd[ac]
                except FloatingPointError:
                    isocomp[acc][ac][i]["z"] = 0
                # same a above, i.e. the rank has the same "orientation" as z-score
                # here small z-scores are of interest and small ranks.
                rank = len(
                    [x for x in isocompdist[ac] if (x < isocomp[acc][ac][i]["sim"])]
                )
                # norm
                isocomp[acc][ac][i]["rank"] = float(rank) / len(isocompdist[ac])

    # compute mean and standard deviation for each alloacceptor distribution
    allomean = {}
    allostd = {}
    sys.stderr.write("allo stat\n")
    for name1 in allocompdist:
        allomean[name1] = {}
        allostd[name1] = {}
        for name2 in allocompdist[name1]:
            allomean[name1][name2] = numpy.mean(allocompdist[name1][name2])
            allostd[name1][name2] = numpy.std(allocompdist[name1][name2])

    # compute z-score and rank for all
    for acc in allocomp:
        for name in allocomp[acc]:
            for i in range(len(allocomp[acc][name])):
                name2 = allocomp[acc][name][i]["t2"].name
                try:
                    allocomp[acc][name][i]["z"] = (
                        allocomp[acc][name][i]["sim"] - allomean[name][name2]
                    ) / allostd[name][name2]
                except FloatingPointError:
                    if allostd[name][name2] == 0:
                        allocomp[acc][name][i]["z"] = 0
                    else:
                        logging.error(
                            "Floating Point error with (%f-%f)/%f"
                            % (
                                allocomp[acc][name][i]["sim"],
                                allomean[name][name2],
                                allostd[name][name2],
                            )
                        )

                # print allocomp[acc][name][i]["sim"], allomean[name][name2] ,
                # allostd[name][name2], allocomp[acc][name][i]["z"]

                # determine the number of elements in the distribution
                # that are <= the value; thus large ranks are of interest
                # (which is as in the z-score)
                rank = len(
                    [
                        x
                        for x in allocompdist[name][name2]
                        if x < allocomp[acc][name][i]["sim"]
                    ]
                )
                # norm

                allocomp[acc][name][i]["rank"] = float(rank) / len(
                    allocompdist[name][name2]
                )


def compare(p):
    """
    execute a comparison function for a pair of
    list of sequences and list of structures
    """
    # print p[0], p[1], rna.forester.RNAforester(sequences = p[0],structures =
    # p[1], r = True )

    return rna.forester.RNAforester(sequences=p[0], structures=p[1], r=True)


def compareaa(lst):
    """
    execute all vs all comparisons
    """

    # lst = [x for x in lst if x]

    sequences = []
    structures = []
    for i in range(len(lst)):
        for j in range(len(lst)):
            sequences.append(lst[i].sequence)
            sequences.append(lst[j].sequence)
            structures.append(lst[i].structure)
            structures.append(lst[j].structure)

    scores = rna.forester.RNAforester(sequences, structures, r=True)
    scoremat = []
    x = 0
    for i in range(len(lst)):
        scoremat.append([])
        for j in range(len(lst)):
            scoremat[i].append(scores[x])
            x += 1

    return scoremat


def compare_list(comp, threads):
    """
    @param comp a list of pairs containing two tRNAs to be compared
    @param threads the number of threads to use
    """
    ss = []

    # generate work packages of size 1000
    for i in range(len(comp)):
        if i % 1000 == 0:
            ss.append(([], []))
        ss[-1][0].append(comp[i][0].sequence)
        ss[-1][0].append(comp[i][0].sequence)
        ss[-1][1].append(comp[i][1].structure)
        ss[-1][1].append(comp[i][1].structure)

    # compute the work packages
    p = multiprocessing.Pool(threads)
    dlst = p.map(compare, ss)
    p.close()
    p.join()

    # compile final distance list
    fdlist = []
    for d in dlst:
        fdlist += d
    return fdlist


def get_alloacceptorhist(data, fname):
    f = open(fname, "w")
    hist = {}
    for acc in data:
        for feat in data[acc]:
            f.write(str(feat.name) + "\n")
            try:
                hist[str(feat.name)] += 1
            except KeyError:
                hist[str(feat.name)] = 1

    f.close()

    return hist


# ## the output is the allocomaprison pkl file
def get_allocomparisons(data, threads):
    """
    get the comparisions of the tRNAs in the same species
    (the name is due that originally only those with different
    alloacceptor have been generated)

    @param data the data
    @param threads number of threads to use
    """

    p = multiprocessing.Pool(threads)
    dmatrix = p.map(compareaa, list(data.values()))
    p.close()
    p.join()

    allocomp = {}
    x = 0

    for acc in data:
        # print(acc)
        sys.stderr.write("allo %s %d/%d\r" % (acc, x + 1, len(data)))

        if acc not in allocomp:
            allocomp[acc] = {}

        #        dmatrix = compareaa( data[acc] )
        for i in range(len(data[acc])):
            f1 = data[acc][i]
            if f1.name not in allocomp[acc]:
                allocomp[acc][f1.name] = []
            # compare to different alloacceptor in the same species
            for j in range(len(data[acc])):
                f2 = data[acc][j]
                #                if f1.name == f2.name:
                #                    continue

                allocomp[acc][f1.name].append(
                    {"t1": f1, "t2": f2, "sim": dmatrix[x][i][j]}
                )

        #        for i in range( len( data[acc] ) ):
        #            f1 = data[acc][i]
        #
        #            if not f1.name in allocomp[acc]:
        #                allocomp[acc][f1.name] = []
        #
        #            # compare to different alloacceptor in the same species
        #            for j in range( len( data[acc] ) ):
        #                f2 = data[acc][j]
        #                if f1.name == f2.name:
        #                    continue
        #
        #    #            dist = compare( f1, f2 )
        #                allocomp[acc][f1.name].append( { "t1": f1, "t2":f2, "sim":compare( f1, f2 ) } )
        x += 1
    sys.stderr.write("\n")
    #        if x >= 10:
    #            break
    return allocomp


def get_allocompdist(allocomp, fname):  # i'm here now
    allocompdist = {}
    for acc in allocomp:
        for name in allocomp[acc]:
            if name not in allocompdist:
                allocompdist[name] = {}

            for i in range(len(allocomp[acc][name])):
                if allocomp[acc][name][i]["t2"].name not in allocompdist[name]:
                    allocompdist[name][allocomp[acc][name][i]["t2"].name] = []
                allocompdist[name][allocomp[acc][name][i]["t2"].name].append(
                    allocomp[acc][name][i]["sim"]
                )

    f = open(fname, "w")
    for n1 in allocompdist:
        for n2 in allocompdist[n1]:
            allocompdist[n1][n2].sort()

            for s in allocompdist[n1][n2]:
                f.write("%s %s %f\n" % (n1, n2, s))
    f.close()

    return allocompdist


def get_isocomp(data, tax, threads, mult):
    """ """
    isocomp = {}
    ln = 1
    for acc in data:

        sys.stderr.write("iso %s %d/%d\r" % (acc, ln, len(data)))
        if acc not in isocomp:
            isocomp[acc] = {}

        # get trnas with the same anticodon
        # in the same or a related species
        anticodons = set([str(x.anticodon) for x in data[acc]])

        st = sorted_taxonomy(acc, tax)
        for ac in anticodons:

            if ac not in isocomp[acc]:
                isocomp[acc][ac] = []

            cand = {}
            cnt = 0

            # go through the sorted taxonomy and and check for a trna with
            # the same anticodon
            for d in sorted(st.keys()):
                for accession2 in st[d]:
                    c = [x for x in data[accession2] if (str(x.anticodon) == ac)]
                    cand[accession2] = c
                    cnt += len(c)

                # as soon as a second tRNA was found (different from the tRNA
                # in the current genome itself)
                if cnt > 1:
                    break
            # if there is more than one tRNAs with the same anticodon in the same species
            # get all pairs (in both directions)
            if acc in cand and len(cand[acc]) > 1:
                for c1 in cand[acc]:
                    for c2 in cand[acc]:
                        if c1 == c2:
                            continue
                        isocomp[acc][ac].append(
                            {"t1": c1, "t2": c2, "sim": 0, "wrt": acc}
                        )

            # tRNAs in different species
            # get all pairs of the trna in the current species with those in
            # the other
            else:
                # the trna itself should be the first (and only) candidate
                # stored for the accession
                if len(cand[acc]) != 1:
                    logging.error("isocomp: wrong nr. of matches in %s %s" % (acc, ac))

                c1 = cand[acc][0]
                for accession2 in cand:
                    if acc == accession2:
                        continue

                    for c2 in cand[accession2]:
                        isocomp[acc][ac].append(
                            {"t1": c1, "t2": c2, "sim": 0, "wrt": accession2}
                        )
        ln += 1

    # compile comparisons to execute
    comparisons = []
    for acc in isocomp:
        for ac in isocomp[acc]:
            for i in range(len(isocomp[acc][ac])):
                comparisons.append(
                    (isocomp[acc][ac][i]["t1"], isocomp[acc][ac][i]["t2"])
                )

    # contains similarity scores from RNAforester
    dlist = compare_list(comparisons, threads)

    # fill in data
    x = 0
    for acc in isocomp:
        for ac in isocomp[acc]:
            for i in range(len(isocomp[acc][ac])):
                # print len(dlist), x, dlist[x]
                isocomp[acc][ac][i]["sim"] = dlist[x]
                x += 1

            if not mult:
                continue

            # print("Here")
            # ONLY REMOVE ONE PER TRNA
            t1s = sorted([z["t1"] for z in isocomp[acc][ac]])
            t1s = [key for key, _ in itertools.groupby(t1s)]

            tmp = isocomp[acc][ac]
            isocomp[acc][ac] = []

            for t in t1s:
                best = [z for z in tmp if z["t1"] == t]
                best.sort(key=lambda k: k["sim"])
                isocomp[acc][ac].append(best[0])

    return isocomp


def get_isocompdist(isocomp, fname):
    isocompdist = {}
    f = open(fname, "w")
    for acc in isocomp:
        for ac in isocomp[acc]:
            if ac not in isocompdist:
                isocompdist[ac] = []

            for i in range(len(isocomp[acc][ac])):

                if acc == isocomp[acc][ac][i]["wrt"]:
                    copy = 1
                else:
                    copy = 0
                f.write("%s %f %d\n" % (ac, isocomp[acc][ac][i]["sim"], copy))
                isocompdist[ac].append(isocomp[acc][ac][i]["sim"])

    for ac in list(isocompdist.keys()):
        if len(isocompdist[ac]) > 0:
            isocompdist[ac].sort()
        else:
            del isocompdist[ac]

    f.close()

    return isocompdist


def get_isoacceptorhist(data, fname):
    f = open(fname, "w")
    hist = {}
    for acc in data:
        for feat in data[acc]:
            f.write(str(feat.anticodon) + "\n")
            try:
                hist[str(feat.anticodon)] += 1
            except KeyError:
                hist[str(feat.anticodon)] = 1
    f.close()

    return hist


def get_results(data, allocomp, allocompdist, isocomp, isocompdist, stat, fname):
    """
    @param data
    @param allocomp
    @param allocompdist
    @param isocomp
    @param isocompdist
    @param stat statistics to use (z/rank/sim)
    fname
    """
    # print "Allocomp", allocomp, "End-Allocomp "+stat+"\n \n \n"
    # print "Allocompdist", allocompdist, "End-Allocomp dist \n \n \n"
    # print "Isocomp", isocomp, "End-Isocomp \n \n\ \n"
    # print "Isocompdist", isocompdist, "End-Isocomp dist \n \n\ \n"

    # print data
    f = open(fname, "w")

    stop = False
    ln = 1
    for acc in data:
        sys.stderr.write("%s %d/%d\r" % (acc, ln + 1, len(data)))

        # if acc != "NC_008140":
        for i in range(len(data[acc])):

            # e.g. acceptors only found once in the data set
            if not str(data[acc][i].anticodon) in isocompdist:
                sys.stderr.write(
                    "skipping %s %s(%s): no isoacceptor found\n"
                    % (acc, data[acc][i].name, data[acc][i].anticodon)
                )
                continue

            if len(isocompdist[str(data[acc][i].anticodon)]) == 0:
                sys.stderr.write(
                    "skipping %s %s(%s): no isoacceptor partner found\n"
                    % (acc, data[acc][i].name, data[acc][i].anticodon)
                )
                continue

            # e.g. only one tRNA in the genome

            if len(allocomp[acc]) <= 1:
                sys.stderr.write(
                    "skipping %s %s: no alloacceptor partner found\n"
                    % (acc, data[acc][i].name)
                )
                continue

            # determine max similarity of the tRNA with another in the same genome
            # i.e. the maximum value of the statistics (rank/z)
            maxcmpap = None
            for acmp in allocomp[acc][data[acc][i].name]:
                # fraction of the allo-comparisons that are more similar than
                # this pair
                if maxcmpap is None or acmp[stat] > maxcmpap[stat]:
                    maxcmpap = acmp

            # determine min similarity of the tRNA with another with the same
            # isoacc
            comparision = [
                x
                for x in isocomp[acc][str(data[acc][i].anticodon)]
                if x["t1"] == data[acc][i]
            ]

            mincmpip = None
            for c in comparision:
                if mincmpip is None or c[stat] < mincmpip[stat]:
                    mincmpip = c

            try:
                #            print maxcmpap['t1'].name, maxcmpap['t2'].name, maxap, maxcmpap['rank'], maxcmpap['z'], \
                #                    mincmpip['wrt'], str( mincmpip['t2'].anticodon ), mincmpip['rank'], mincmpip['z']
                f.write(
                    "%s\t%s\t%s\t%f\t%f\t%f\t%s\t%s\t%f\t%f\t%f\n"
                    % (
                        acc,
                        maxcmpap["t1"].name,
                        maxcmpap["t2"].name,
                        maxcmpap["sim"],
                        maxcmpap["rank"],
                        maxcmpap["z"],
                        mincmpip["wrt"],
                        str(mincmpip["t2"].anticodon),
                        mincmpip["sim"],
                        mincmpip["rank"],
                        mincmpip["z"],
                    )
                )
            except Exception:
                sys.stderr.write(
                    "%s %s %s %s\n"
                    % (
                        acc,
                        data[acc][i].name,
                        data[acc][i].anticodon,
                        repr(data[acc][i]),
                    )
                )
                print(mincmpip)
                print(len(comparision))
                print(len(isocompdist[str(data[acc][i].anticodon)]))
                for c in isocomp[acc][str(data[acc][i].anticodon)]:
                    print(c)

                for i in range(len(data[acc])):
                    print(data[acc][i])

                stop = True
                break
            # else:
            #    continue

        if stop is True:
            break
        ln += 1

    #            .append( { "t1": c1, "t2":c2, "sim":compare( c1, c2 ), "wrt": accession2 } )
    f.close()
    sys.stderr.write("\n")


def len_common_prefix(t1, t2):
    """
    determine the length of the common prefix of two taxonomy lists
    @param t1 taxonomy list
    @param t2 taxonomy list
    @return lenght
    """
    i = 0
    while i < len(t1) and i < len(t2):
        if t1[i] == t2[i]:
            i += 1
        else:
            break

    return i


def load_data(dirs):
    """ """
    data = {}
    # extract all tRNAs from the MITOS results that have an annotated
    # anticodon (and discard the others) + replace nonstandard bases with
    # random bases(ACGTU)
    for dr in dirs:
        # if not os.listdir(dr) == []:
        #     continue
        if not os.path.isdir(dr):
            sys.stderr.write("skipping non dir %s\n" % dr)
            continue

        try:
            gb = mitofile.mitofromfile(dr + "/result")
        except IOError:
            sys.stderr.write("skipping (no result) %s\n" % dr)
            continue

        try:
            f = open(dr + "/result.pkl")
            features = pickle.load(f)
            f.close()
        except IOError:
            sys.stderr.write("skipping (no features) %s\n" % dr)
            continue

        tmp = [x for x in features if (x.type == "tRNA" and x.anticodon is None)]
        for t in tmp:
            logging.warning("remove degenerated tRNA: %s %s" % (gb.accession, t.name))

        data[gb.accession] = [
            x for x in features if (x.type == "tRNA" and x.anticodon is not None)
        ]

        for i in range(len(data[gb.accession])):
            while 1:
                r = random.choice(["A", "U", "C", "G"])
                (data[gb.accession][i].sequence, cnt) = re.subn(
                    "[^ACGTU]", r, data[gb.accession][i].sequence, count=1
                )
                if cnt == 0:
                    break
                else:
                    logging.warning("replaced nonstandard base by random: %s" % r)
    return data


def load_taxonomy(taxfname):
    """
    read taxonomy from a file with the accession in the first column
    followed by the space separtated taxstring
    @param taxfname
    @return taxonomy dictionary
    """
    tax = {}
    f = open(taxfname)
    for line in f.readlines():
        line = line.split()
        tax[line[0]] = line[1:]
    f.close()
    return tax


def sorted_taxonomy(acc, tax):
    """
    given an accession a and the taxonomy lists for a set of accessions S
    including the accession a itself return a list of the accessions S
    sorted by their distance to a. The distance is the distance in the tree.
    Let a and b two accessions and T_a and T_b their accesion lists, and
    C be the common prefix of T_a and T_b. Then the distance is computed as
    (|T_a|-|C|)+(|T_b|-|C|).

    @param acc accession
    @param tax taxonomy lists for all accessions given as dict
    @return sorted list of accessions
    """
    st = {}
    for t in tax:
        lcp = len_common_prefix(tax[acc], tax[t])
        d = (len(tax[acc]) - lcp) + (len(tax[t]) - lcp)

        if d not in st:
            st[d] = []

        st[d].append(t)

    return st


if __name__ == "__main__":
    usage = "usage: %prog dirs"
    parser = argparse.ArgumentParser(description=usage)
    parser.add_argument("dirs", metavar="DIRS", nargs="+", help="directories")
    parser.add_argument(
        "-t",
        "--tax",
        action="store",
        required=True,
        metavar="FILE",
        help="taxomomy file",
    )
    parser.add_argument(
        "--threads",
        action="store",
        type=int,
        default=4,
        metavar="N",
        help="number of threads",
    )
    args = parser.parse_args()

    random.seed(42)
    numpy.seterr(invalid="raise")

    sys.stderr.write("load data\n")
    tax = load_taxonomy(args.tax)
    data = load_data(args.dirs)

    # return the anti-codon histogram and the file that contain the
    # anti-codons to draw it
    get_isoacceptorhist(data, "isohist.dat")
    get_alloacceptorhist(data, "allohist.dat")

    # x = 0
    # for k in data.keys():
    #    if x > 10:
    #        del tax[k]
    #        del data[k]
    #    x += 1

    # for each pair of alloacceptor all pairs within the same genome
    # creating the allo pkl file if it's not already there
    sys.stderr.write("alloacceptor comparisons\n")
    if os.path.exists("allocomp.pkl"):
        f = open("allocomp.pkl")
        allocomp = pickle.load(f)
        f.close()
    else:
        allocomp = get_allocomparisons(data, args.threads)
        f = open("allocomp.pkl", "w")
        pickle.dump(allocomp, f)
        f.close()

    # pairs of trnas with the same isoacceptor from the same or related species
    # creating the iso pkl file if it's not already there
    sys.stderr.write("isoacceptor comparisons\n")
    if os.path.exists("isocomp.pkl"):
        f = open("isocomp.pkl")
        isocomp = pickle.load(f)
        f.close()
    else:
        isocomp = get_isocomp(data, tax, args.threads, False)
        f = open("isocomp.pkl", "w")
        pickle.dump(isocomp, f)
        f.close()

    # print isocomp, "test"
    # sys.exit()

    sys.stderr.write("compiling isoacceptor distribution\n")
    # take as argument the iso pkl file and the output file
    isocompdist = get_isocompdist(isocomp, "iso.dat")

    # isocompdist contains the codon, the similarity score, and the copy

    sys.stderr.write("compiling alloacceptor distribution\n")
    # take as argument the allo pkl file and the output file
    allocompdist = get_allocompdist(allocomp, "allo.dat")

    # allocompdist contains the tRNA1, tRNA2, and the similarity score

    sys.stderr.write("computing statistics\n")
    apply_statistics(allocomp, allocompdist, isocomp, isocompdist)

    for s in "sim", "z", "rank":
        get_results(
            data,
            allocomp,
            allocompdist,
            isocomp,
            isocompdist,
            s,
            "results" + s + ".dat",
        )

    si = [
        ("NC_010209", "trnR", "TCT"),
        ("NC_010210", "trnR", "TCT"),
        ("NC_010171", "trnY", "ATA"),
        ("NC_010213", "trnN", "GTT"),
        ("NC_006894", "trnN", "GTT"),
        ("NC_006894", "trnA", "TCG"),
        ("NC_006894", "trnC", "GCA"),
    ]
    for acc, name, acod in si:
        print("=======", acc, name)
        for c in sorted(allocomp[acc][name], key=lambda k: k["sim"]):
            #            if str( c["t1"].anticodon ) != acod:
            #                continue

            print(
                c["t1"].outputname(), c["t2"].outputname(), c["sim"], c["rank"], c["z"]
            )

        for feat in data[acc]:
            if name != feat.name:
                continue

            ac = str(feat.anticodon)
            for c in sorted(isocomp[acc][ac], key=lambda k: k["sim"]):
                print(c["wrt"], c["t1"].outputname(), c["sim"], c["rank"], c["z"])


#    sys.exit()

# PROCESS THE RESULTS
# or just determine fraction
