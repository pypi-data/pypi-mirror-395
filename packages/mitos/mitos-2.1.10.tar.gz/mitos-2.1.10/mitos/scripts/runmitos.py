#!/usr/bin/env python

"""
@author: M. Bernt
"""

import io
import json
import logging
import os
import re
import shutil
import sys

from Bio import SeqIO
from Bio.SeqRecord import SeqRecord

from mitos import (
    __version__,
    bedfile,
    blast,
    feature,
    gfffile,
    mitfi,
    mito,
    protfeat,
    tbl,
    trna,
    util,
)
from mitos.mergefeature import _copy_part, checklocalfeature, featureappend
from mitos.mitofile import mitowriter
from mitos.rna.vienna import RNAplot
from mitos.sequence import (
    fastawriter,
    sequence_info_fromfile,
    sequence_info_fromfilehandle,
)


def mitos(
    fastafile,
    code,
    ncbicode,
    best,
    order,
    alarab=False,
    outdir=None,
    cutoff="%50",
    minevalue=2,
    finovl=100,
    clipfac=10,
    fragovl=0.2,
    fragfac=10.0,
    # prot = True, trna = True, rrna = True, cr = False,
    sensitive=False,
    localonly=False,
    refdir=None,
    ncev=0.001,
    circular=True,
    circrot=0,
    trnaovl=10,
    rrnaovl=10,
    plots=True,
    oldstst=False,
):
    """
    @param[in] fastafile
    @param[in] code the genetic code X / X* (is given as string)
    @param[in] ncbicode true: use the NCBI standard, false use learned code
    @param[in] best annotate only the best copy of each feature
    @param[in] order list of feature types to be added in the 1st round accepted
        content is gene, tRNA, rRNA, OL, OH
    @param[in] alarab use the method of Al Arab et al 2016 for protein prediction
    @param[in] outdir directory for the output (if None MITOS uses the
        directory containing the fasta file)
    @param[in] cutoff cutoff percentage
    @param[in] minevalue
    @param[in] finovl
    @param[in] clipfac
    @param[in] fragovl
    @param[in] fragfac
    @param[in] sensitive use only the sensitive mode of infernal
    @param[in] localonly True: run mitfi in local mode only, False: run mitfi first in glocal mode, then in local mode (if necessary)
    @param[in] refseqver version of RefSeq to use
    @param[in] ncev evalue to be used in inferal fast mode
    @param[in] circular treat sequence as circular
    @param[in] circrot circular rotation in [0:179] for the treatment of mitogenomes rotation of circrot and circrot+180 are tested
    @param[in] trnaovl max overlap allowed between trna
    @param[in] rrnaovl max overlap allowed between rrna
    @param[in] oldstst use the old start stop prediction method of MITOS1
    """
    # ststrange = 6, maxdegenerate = 2
    # @param[in] ststrange
    # @param[in] maxdegenerate maximum number of nt to allow for incomplete stop codons

    #     import inspect
    #     frame = inspect.currentframe()
    #     args, _, _, values = inspect.getargvalues(frame)
    #     logging.debug('function name "%s"' % inspect.getframeinfo(frame)[2])
    #     for i in args:
    #         logging.debug("    %s = %s" % (i, values[i]))
    prot = "gene" in order
    trna = "tRNA" in order
    rrna = "rRNA" in order
    orih = "OH" in order
    oril = "OL" in order
    intron = "intron" in order

    # get auxilliary data of the DB (genetic code, query feature lengths)
    if prot or orih:
        try:
            f = open("{refdir}/auxinfo.json".format(refdir=refdir))
            auxinfo = json.load(f)
            (stacod, stocod, len_pval, fas2len) = (
                auxinfo["start"],
                auxinfo["stop"],
                auxinfo["len_pval"],
                auxinfo["fas2len"],
            )
            f.close()
        except IOError:
            logging.error(
                "no auxilliary data found in reference data directory %s\n" % (refdir)
            )
            raise
        else:
            if not ncbicode:
                extcode = "%d*" % code
                fbcode = "2*"
            else:
                extcode = "%d" % code
                fbcode = "2"

            if extcode in stacod:
                stacod = stacod[extcode]
            else:
                stacod = stacod[fbcode]
                logging.warning(
                    "no start codons for code %s in auxilliary data. Using %s."
                    % (extcode, fbcode)
                )

            if extcode in stocod:
                stocod = stocod[extcode]
            else:
                stocod = stocod[fbcode]
                logging.warning(
                    "no stop codons for code %s in auxilliary data. Using %s."
                    % (extcode, fbcode)
                )

            if str(code) in len_pval:
                len_pval = len_pval[str(code)]
            else:
                len_pval = len_pval["2"]
                logging.warning(
                    "no length pvalues for code %s in auxilliary data. Using 2."
                    % (code)
                )
    else:
        stacod = None
        stocod = None
        len_pval = None
        fas2len = None

    # the path for storing the output
    if outdir is None:
        path = os.path.dirname(fastafile) + "/"
    else:
        path = outdir + "/"

    # the path where the mitfi results are safed
    mitfipath = "%s/mitfi-global/" % (path)
    if (trna or rrna or oril) and not os.path.exists(mitfipath):
        os.mkdir(mitfipath)

    # parse fasta header
    fasta = sequence_info_fromfile(fastafile, circular=circular)
    sequence = fasta[0]["sequence"]
    length = len(sequence)

    if circrot < 0 or circrot > 179:
        raise Exception("mitos: circular rotation not in [0,179]")

    if circular:
        rotations = [circrot, circrot + 180]
    else:
        rotations = [circrot]

    fastafiles = []
    offsets = []
    for rot in rotations:
        offset = int(length * rot / 360.0)
        for key in ["id", "name", "description"]:
            fasta[0][key] = fasta[0][key].replace("|", "_")

        sr = SeqRecord(
            seq=fasta[0]["sequence"][offset:] + fasta[0]["sequence"][:offset],
            id=fasta[0]["id"],
            name=fasta[0]["name"],
            description=fasta[0]["description"],
        )

        tmpff = "%s/%s-%s" % (path, os.path.basename(fastafile), str(offset))
        with open(tmpff, "w") as f:
            SeqIO.write(sr, f, "fasta")

        fastafiles.append(tmpff)
        offsets.append(offset)
    logging.debug("offsets %s" % str(offsets))
    logging.debug("files %s" % str(fastafiles))

    #     orgfastafile = fastafile
    #     # for analyzing a circular sequence correctly sequence is doubled and
    #     # stores under .lin in the output directory
    #     if circular:
    #         sr = SeqRecord(seq = fasta[0]["sequence"] + fasta[0]["sequence"][:int(circextend * length)], \
    #                         id = fasta[0]["id"], name = fasta[0]["name"], description = fasta[0]["description"])
    #
    #         fastafile = path + "/" + os.path.basename(orgfastafile) + ".lin"
    #         f = open(fastafile, "w")
    #         SeqIO.write(sr, f, "fasta")
    #         f.close()

    # create plot path
    if plots:
        if not os.path.exists("%s/plots/" % path):
            os.mkdir("%s/plots/" % path)

        # create empty (or reset) rna plot
        if rrna or trna or oril:
            open("%s/plots/rna.dat" % (path), "w").close()

    acc = []
    for a in "_".join(fasta[0]["name"].split()):
        if a.isalnum() or a == "_" or a == "-":
            acc.append(a)
        # else:
        #    acc.append("_")

    if len(acc) == 0:
        acc = "noname"
    else:
        acc = "".join(acc)

    # acc = "_".join(fasta[0]["name"].split())

    if "|" in acc:
        raise Exception("No | character allowed in fasta header! Aborting")

    # the list of candidates
    cand = [{}, {}]

    # run RNA models in fast mode with strict threshold (if not sensitive mode only)
    # TODO get copy and part numbers for ncRNAs
    if (trna or rrna or oril or intron) and not sensitive:
        rnalist = mitfi.mitfi(
            fastafiles,
            offsets,
            mitfipath,
            code,
            refdir,
            evalue=ncev,
            sensitive=False,
            length=length,
            gl=(not localonly),
            trna=trna,
            ori=oril,
            rrna=rrna,
            intron=intron,
            trnaovl=trnaovl,
            rrnaovl=rrnaovl,
        )
    # run RNA models in sensitive (aka slow) mode
    # - if sensitive mode only
    # - or for those RNAs that did not yield a result

    if (trna or rrna or oril and intron) and (
        sensitive
        or mitfi.remove_empty(trna, rrna, oril, intron, rnalist, mitfipath, offsets)
    ):
        rnalist = mitfi.mitfi(
            fastafiles,
            offsets,
            mitfipath,
            code,
            refdir,
            evalue=0.1,
            sensitive=True,
            length=length,
            gl=(not localonly),
            trna=trna,
            rrna=rrna,
            ori=oril,
            intron=intron,
            trnaovl=trnaovl,
            rrnaovl=rrnaovl,
        )

    if trna:
        cand[0]["tRNA"] = [x for x in rnalist if x.type == "tRNA" and x.mito == 2]
        cand[1]["tRNA"] = [
            x for x in rnalist if x.type == "tRNA" and x.mito == 1 and x.evalue <= 0.001
        ]
        if plots:
            print_for_plotting(
                cand[0]["tRNA"], cand[1]["tRNA"], "%s/plots/rna.dat" % (path), "global"
            )
    if rrna:
        cand[0]["rRNA"] = [x for x in rnalist if x.type == "rRNA" and x.mito == 2]
        cand[1]["rRNA"] = [x for x in rnalist if x.type == "rRNA" and x.mito == 1]
        if plots:
            print_for_plotting(
                cand[0]["rRNA"], cand[1]["rRNA"], "%s/plots/rna.dat" % (path), "global"
            )
    if oril:
        cand[0]["OL"] = [x for x in rnalist if (x.type == "rep_origin" and x.mito == 2)]
        cand[1]["OL"] = [x for x in rnalist if (x.type == "rep_origin" and x.mito == 1)]
        if plots:
            print_for_plotting(
                cand[0]["OL"], cand[1]["OL"], "%s/plots/rna.dat" % (path), "global"
            )
    if intron:
        cand[0]["intron"] = [x for x in rnalist if (x.type == "intron" and x.mito == 2)]
        cand[1]["intron"] = [x for x in rnalist if (x.type == "intron" and x.mito == 1)]
        if plots:
            print_for_plotting(
                cand[0]["intron"],
                cand[1]["intron"],
                "%s/plots/rna.dat" % (path),
                "global",
            )

    #     for f in cand[0]["tRNA"]:
    #         logging.debug("CAND %s" %f)

    # get protein and replication origin region features
    blastidx = dict()
    blastvalues = []
    if prot:
        try:
            besttrna = cand[0]["tRNA"]
        except KeyError:
            besttrna = []

        if alarab:
            blastfeat = protfeat.prot_feat_wrap(
                fastafiles,
                offsets,
                path + "/hmm/",
                circular,
                startcod=stacod,
                stopcod=stocod,
                len_pval=len_pval,
                trnas=besttrna,
                refdir=refdir,
                minevalue=minevalue,
                code=code,
                plot=plots,
                finovl=finovl,
                fragfac=fragfac,
                fragovl=fragovl,
                oldstst=oldstst,
            )
        else:
            blastfeat = blast.blast(
                fastafiles,
                offsets,
                prot,
                False,
                path,
                refdir=refdir,
                length=length,
                startcod=stacod,
                stopcod=stocod,
                fas2len=fas2len,
                len_pval=len_pval,
                idx=blastidx,
                values=blastvalues,
                fragfac=fragfac,
                fragovl=fragovl,
                trnas=besttrna,
                circular=circular,
                cutoff=cutoff,
                minevalue=minevalue,
                acc=acc,
                code=code,
                plot=plots,
                finovl=finovl,
                clipfac=clipfac,
                oldstst=oldstst,
            )
        #                     , ststrange = ststrange, maxdegenerate = maxdegenerate)

        # compile the list of candidate sets
        cand[0]["prot"] = [
            x
            for x in blastfeat
            if (
                x.type == "gene"
                and x.name in mito.metazoa_prot
                and (x.copy is None or x.copy == 0)
            )
        ]
        cand[1]["prot"] = [
            x
            for x in blastfeat
            if (
                x.type == "gene"
                and x.name in mito.metazoa_prot
                and (x.copy is not None and x.copy != 0)
            )
        ]
        cand[0]["oprot"] = [
            x
            for x in blastfeat
            if (
                x.type == "gene"
                and x.name not in mito.metazoa_prot
                and (x.copy is None or x.copy == 0)
            )
        ]
        cand[1]["oprot"] = [
            x
            for x in blastfeat
            if (
                x.type == "gene"
                and x.name not in mito.metazoa_prot
                and (x.copy is not None and x.copy != 0)
            )
        ]

    if orih:
        blastfeat = blast.blast(
            fastafiles,
            offsets,
            False,
            orih,
            path,
            refdir,
            length=length,
            startcod=stacod,
            stopcod=stocod,
            fas2len=fas2len,
            len_pval=len_pval,
            idx=blastidx,
            values=blastvalues,
            fragfac=fragfac,
            fragovl=fragovl,
            trnas=[],
            circular=circular,
            cutoff=cutoff,
            minevalue=minevalue,
            acc=acc,
            code=code,
            plot=plots,
            finovl=finovl,
            clipfac=clipfac,
        )
        #                     , ststrange = ststrange, maxdegenerate = maxdegenerate)
        cand[0]["OH"] = [
            x
            for x in blastfeat
            if (x.type == "rep_origin" and (x.copy is None or x.copy == 0))
        ]
        cand[1]["OH"] = [
            x
            for x in blastfeat
            if (x.type == "rep_origin" and (x.copy is not None and x.copy != 0))
        ]

    # sort the candidates accordingly
    for rnd in range(2):
        for tpe in cand[rnd]:
            if tpe in ["prot", "oprot", "OH"]:
                cand[rnd][tpe].sort(key=lambda x: x.score, reverse=True)
            elif tpe in ["tRNA", "rRNA", "intron", "OL"]:
                cand[rnd][tpe].sort(key=lambda x: x.evalue)
            else:
                raise Exception("unknown feature type %s" % tpe)

            logging.debug("Candidates {tpe} {round}".format(tpe=tpe, round=rnd))
            for f in cand[rnd][tpe]:
                logging.debug(
                    "\t{name} {strand} {start} {stop}".format(
                        name=f.name, strand=f.strand, start=f.start, stop=f.stop
                    )
                )

    # set features: 1st round
    featurelist = []
    nfeaturelist = []
    for tpe in ["prot", "tRNA", "rRNA", "intron", "OL", "oprot", "OH"]:
        if not (tpe in cand[0]):
            continue
        featureappend(
            cand[0][tpe],
            featurelist,
            nfeaturelist,
            circular,
            length,
            overlap=finovl,
            rnd=True,
        )

    #     # get default protein and rep-ori features for the two round (1st: best hit, 2nd the rest)
    #     if prot:
    #         protfeat = [x for x in blastfeat if (x.type == "gene" and \
    #                                                (x.copy is None or x.copy == 0))]
    #         mprotfeat = [x for x in blastfeat if (x.type == "gene" and \
    #                                                 (x.copy is not None and x.copy != 0))]
    #     else:
    #         protfeat = []
    #         mprotfeat = []
    #
    #     # determine the t/r RNA features for the first and second round.
    #     # - first round best hit (and for tRNA evalue <= 10^{-3})
    #     # - second round duplicates with worse evalue (and tRNAs above evalue threshold)
    #     if trna:
    #         trnafeat = [x for x in rnalist if x.type == "tRNA" and x.mito == 2]
    #         mtrnafeat = [x for x in rnalist if x.type == "tRNA" and x.mito == 1 and x.evalue <= 0.001]
    #         print_for_plotting(trnafeat, mtrnafeat, "%s/plots/rna.dat" % (path), "global")
    #     else:
    #         trnafeat = []
    #         mtrnafeat = []
    #
    #     if rrna:
    #         rrnafeat = [x for x in rnalist if x.type == "rRNA" and x.mito == 2]
    #         mrrnafeat = [x for x in rnalist if x.type == "rRNA" and x.mito == 1]
    #         print_for_plotting(rrnafeat, mrrnafeat, "%s/plots/rna.dat" % (path), "global")
    #     else:
    #         rrnafeat = []
    #         mrrnafeat = []
    #
    #     if cr:
    #         crfeat = [x for x in blastfeat + rnalist if ((x.type == "rep_origin")and \
    #                                                        (x.method != "mitfi" or x.evalue <= 0.1) \
    #                                              and (x.copy is None or x.copy == 0))]
    #         mcrfeat = [x for x in blastfeat + rnalist if ((x.type == "rep_origin") and \
    #                                                        (x.method != "mitfi" or x.evalue <= 0.1) \
    #                                               and (x.copy is not None and x.copy != 0))]
    #     else:
    #         crfeat = []
    #         mcrfeat = []
    #
    #     logging.debug("PROT FEATURES CANDIDATES")
    #     for f in protfeat:
    #         logging.debug("%s" % str(f))
    #     logging.debug("TRNA FEATURES CANDIDATES")
    #     for f in trnafeat:
    #         logging.debug("{name} {strand} {start} {stop}".format(name = f.name, strand = f.strand, start = f.start, stop = f.stop))
    #     logging.debug("RRNA FEATURES CAND")
    #     for f in sorted(rrnafeat, key = lambda x:x.start):
    #         logging.debug("{name} {strand} {start} {stop}".format(name = f.name, strand = f.strand, start = f.start, stop = f.stop))
    #     logging.debug("CR FEATURES CANDIDATES")
    #     for f in sorted(crfeat, key = lambda x:x.start):
    #         logging.debug("{name} {strand} {start} {stop}".format(name = f.name, strand = f.strand, start = f.start, stop = f.stop))
    #     logging.debug("MFEATURES CANDIDATES")
    #     for f in mprotfeat:
    #         logging.debug("%s" % str(f))
    #     for f in sorted(mtrnafeat, key = lambda x:x.start):
    #         logging.debug("{name} {strand} {start} {stop}".format(name = f.name, strand = f.strand, start = f.start, stop = f.stop))
    #     for f in sorted(mrrnafeat, key = lambda x:x.start):
    #         logging.debug("{name} {strand} {start} {stop}".format(name = f.name, strand = f.strand, start = f.start, stop = f.stop))
    #     for f in sorted(mcrfeat, key = lambda x:x.start):
    #         logging.debug("{name} {strand} {start} {stop}".format(name = f.name, strand = f.strand, start = f.start, stop = f.stop))
    #
    # #     print "ALL FEATURES CAND"
    # #     for f in [x for x in rnalist]:
    # #         print f.name, f.strand, f.start, f.stop
    #
    #     # sort the features such that the best are first in the list
    #     # then the featureappend function will remove the worse of duplicates
    #     # that are due to the handling of circularity
    #     protfeat.sort(key = lambda x:x.score, reverse = True)
    #     crfeat.sort(key = lambda x:x.score, reverse = True)
    #     trnafeat.sort(key = lambda x:x.evalue)
    #     rrnafeat.sort(key = lambda x:x.evalue)
    #
    #     # set features: 1st round
    #     featurelist = []
    #     featureappend(protfeat, featurelist, circular, length, overlap = finovl)
    #     featureappend(trnafeat, featurelist, circular, length, overlap = finovl)
    #     featureappend(rrnafeat, featurelist, circular, length, overlap = finovl, rnd = True)
    #     featureappend(crfeat, featurelist, circular, length, overlap = finovl)

    logging.debug("State after first round")
    for f in featurelist:
        logging.debug("%s %d %d" % (f.name, f.start, f.stop))

    # try to get results from the local search if global did not yielded a
    # result
    localcheck = []  # stores for which rRNAs the local mode was applied
    if rrna and not localonly:
        # search both rRNA, of course
        for lname in ["rrnS", "rrnL"]:
            # check if the feature exists
            if len([feat for feat in featurelist if feat.name == lname]) == 0:
                logging.debug("adding local %s" % (lname))

                # save the info that this rRNA was searched also with local
                # mode
                localcheck.append(lname)

        if len(localcheck) > 0:
            # the path where the mitfi results are saved
            lokalpath = "%s/mitfi-local/" % (path)
            if not os.path.exists(lokalpath):
                os.mkdir(lokalpath)

            # search
            if rrna and not sensitive:
                lrnalist = mitfi.mitfi(
                    fastafiles,
                    offsets,
                    lokalpath,
                    code,
                    refdir,
                    evalue=ncev,
                    sensitive=False,
                    length=length,
                    gl=False,
                    RNAlist=localcheck,
                    trna=False,
                    rrna=rrna,
                    ori=False,
                    trnaovl=trnaovl,
                    rrnaovl=rrnaovl,
                )

            if rrna and (
                sensitive
                or mitfi.remove_empty(
                    trna, rrna, oril, intron, lrnalist, lokalpath, offsets
                )
            ):
                lrnalist = mitfi.mitfi(
                    fastafiles,
                    offsets,
                    lokalpath,
                    code,
                    refdir,
                    evalue=10,
                    sensitive=True,
                    length=length,
                    gl=False,
                    RNAlist=localcheck,
                    trna=False,
                    rrna=rrna,
                    ori=False,
                    trnaovl=trnaovl,
                    rrnaovl=rrnaovl,
                )

            for lname in localcheck:
                # get a conflict free set of mito>0 features of name lname
                localhits = []
                nlocalhits = []
                featureappend(
                    [x for x in lrnalist if x.mito > 0 and x.name == lname],
                    localhits,
                    nlocalhits,
                    circular,
                    length,
                    overlap=finovl,
                )

                if plots:
                    print_for_plotting(
                        localhits, [], "%s/plots/rna.dat" % (path), "glocal"
                    )

                # append the local features
                featureappend(
                    localhits,
                    featurelist,
                    nfeaturelist,
                    circular,
                    length,
                    overlap=finovl,
                )
    #                 appendlocalfeature(localhits, lname, cand[0]["rRNA"], featurelist, length, allowoverlap = finovl)

    if not best:
        logging.debug("annotate weaker hits")
        # for the remaining rRNAs, tRNAs, and proteins (which were not in the set of the best of each kind)
        # - determine the quotient of the best evalue and the evalue (or quality for proteins)
        # - sort by the quotient
        # - try to add
        dolist = []
        for tpe in cand[1]:
            for feat in cand[1][tpe]:
                besthit = [x for x in featurelist if x.name == feat.name]
                if tpe in ["tRNA", "rRNA", "intron", "OL"]:
                    if len(besthit) == 0:
                        maxevalue = 1
                    else:
                        besthit.sort(key=lambda x: (-x.mito, x.evalue))
                        maxevalue = besthit[0].evalue
                    if maxevalue == 0:
                        maxevalue = 1e-46
                    feat.evalfaktor = feat.evalue / maxevalue
                elif tpe in ["prot", "oprot", "OH"]:
                    if len(besthit) == 0:
                        maxscore = 1
                    else:
                        besthit.sort(key=lambda x: x.score)
                        maxscore = besthit[0].score
                    if maxscore == 0:
                        maxscore = 1e46
                    logging.debug("%s %f" % (str(feat), maxscore))
                    feat.evalfaktor = 1 / (feat.score / maxscore)
                else:
                    raise Exception("unknown feature type %s" % tpe)
            dolist += cand[1][tpe]

        dolist.sort(key=lambda x: x.evalfaktor)
        featureappend(
            dolist, featurelist, nfeaturelist, circular, length, overlap=finovl
        )

    #         for feat in mrrnafeat + mtrnafeat:
    #             besthit = [x for x in featurelist if x.name == feat.name]
    #             if len(besthit) == 0:
    #                 maxevalue = 1
    #             else:
    #                 besthit.sort(key = lambda x:(-x.mito, x.evalue))
    #                 maxevalue = besthit[0].evalue
    #             if maxevalue == 0:
    #                 maxevalue = 1E-46
    #             feat.evalfaktor = feat.evalue / maxevalue
    #
    #         for feat in mprotfeat + mcrfeat:
    #             besthit = [x for x in featurelist if x.name == feat.name]
    #             if len(besthit) == 0:
    #                 maxscore = 1
    #             else:
    #                 besthit.sort(key = lambda x:x.score)
    #                 maxscore = besthit[0].score
    #             if maxscore == 0:
    #                 maxscore = 1E46
    #             feat.evalfaktor = 1 / (feat.score / maxscore)
    #
    #         dolist = mrrnafeat + mtrnafeat + mprotfeat + mcrfeat
    #         dolist.sort(key = lambda x:x.evalfaktor)
    #
    #         featureappend(dolist, featurelist, circular, length, overlap = finovl)

    # check if
    # - local features are too short -> remove
    # consecutive local features are mergeable
    checklocalfeature(localcheck, featurelist, sequence, refdir, circular, length)

    # determine final copy part numbers (also for ncRNAs)
    _copy_part(featurelist, fragovl, fragfac)

    #     # - apply start and stop prediction to the 1st and last parts
    #     if prot:
    #         ststf = open("%s/blast/stst.dat" % (path), "w")
    #         for n in cpyprt:
    #             for cpy in cpyprt[n]:
    #                 if cpyprt[n][cpy][0].type != "gene":
    #                     continue
    #                 plotdat = blast._improve_start_stop(cpyprt[n][cpy],
    #                                     'e', False, False, sequence,
    #                                     code, stacod, stocod, len_pval,
    #                                     blastidx[n], blastvalues, cpyprt, featurelist,
    #                                     circular)
    #                 ststf.write(plotdat)
    #         ststf.close()
    # #         _improve_start_stop_old(cpyprt[n][cpy], code, sequence, length, ststrange, idx[n], values, scoresel, havg, pavg)
    #
    #     # START STOP PREDICTION CREATES MORE THAT FINOVL OVERLAPS
    #     # -> remove
    #     for i in xrange(len(featurelist)):
    #         if featurelist[i] is None or featurelist[i].type != "gene":
    #             continue
    #
    #         for j in xrange(len(featurelist)):
    #             if featurelist[j] is None or featurelist[j].type != "gene" or i == j:
    #                 continue
    #
    #             cap = feature.cap(featurelist[i].start, featurelist[i].stop, featurelist[j].start, featurelist[j].stop, circular, len(sequence))
    #
    #             if cap <= finovl:
    #                 continue
    #
    #             if featurelist[i].score > featurelist[j].score:
    #                 featurelist[ j ] = None
    #             else:
    #                 featurelist[ i ] = None
    #
    #             break

    featurelist = [x for x in featurelist if x is not None]

    # remove features from nfeaturelist that appear as well in featurelist
    nfeaturelist = [x for x in nfeaturelist if x not in featurelist]
    #     i = 0
    #     while i < len(nfeaturelist):
    #         d = False
    #         for j in xrange(len(featurelist)):
    #             if nfeaturelist[i] == featurelist[j]:
    #                 d = True
    #                 break
    #         if d:
    #             del nfeaturelist[i]
    #         else:
    #             i += 1

    mitowriter(featurelist, acc, "%s/result.mitos" % (path))
    mitowriter(nfeaturelist, acc, "%s/ignored.mitos" % (path))
    # produce protein plot
    if plots and (prot or orih):
        if alarab:
            subpath = "hmm"
        else:
            subpath = "blast"

        cmd = [
            "plotprot.R",
            "%s/%s/%s.dat" % (path, subpath, subpath),
            "%s/result.mitos" % (path),
            "%s/plots/prot.pdf" % (path),
            "%d" % (len(sequence)),
        ]
        util.execute(cmd, supress_warning=True)

        cmd = ["plotstst.R", "%s/%s/stst.dat" % (path, subpath), "%s/plots/" % (path)]
        util.execute(cmd, supress_warning=True)

    if plots and (trna or rrna):
        cmd = [
            "plotrna.R",
            "%s/plots/rna.dat" % (path),
            "%d" % (len(sequence)),
            "%s/plots/rna.pdf" % (path),
        ]
        util.execute(cmd, supress_warning=True)

    # produce rRNA plots
    if plots:
        for f in featurelist:
            if f.type != "tRNA" and f.type != "rRNA" and f.name != "OL":
                continue

            if not os.path.exists("%s/plots/" % path):
                os.mkdir("%s/plots/" % path)

            #        print "seq", f.sequence
            #        print "str", f.structure
            RNAplot(
                f.sequence,
                f.structure,
                "%s/plots/%s-%d-%d.ps" % (path, f.name, f.start + 1, f.stop + 1),
            )
            RNAplot(
                f.sequence,
                f.structure,
                "%s/plots/%s-%d-%d.svg" % (path, f.name, f.start + 1, f.stop + 1),
                o="svg",
            )
    for fastafile in fastafiles:
        os.remove(fastafile)
    return featurelist


def print_for_plotting(features, mfeatures, fname, mode):
    """
    print 1st and 2nd grade features to a file for plotting
    @param features 1st grade features
    @param mfeatures 2nd grade features
    @param mode mode
    @param fname file name
    """

    f = open(fname, "a")
    for feat in features:
        f.write(
            "{start}\t{stop}\t{strand}\t{name}\t{type}\t{score}\t{mode}\t1\n".format(
                start=feat.start,
                stop=feat.stop,
                strand=feat.strand,
                name=feat.name,
                type=mito.types[feat.name],
                score=feat.score,
                mode=mode,
            )
        )
    for feat in mfeatures:
        f.write(
            "{start}\t{stop}\t{strand}\t{name}\t{type}\t{score}\t{mode}\t2\n".format(
                start=feat.start,
                stop=feat.stop,
                strand=feat.strand,
                name=feat.name,
                type=mito.types[feat.name],
                score=feat.score,
                mode=mode,
            )
        )
    f.close()


def problems_overlaps(features, circular, size):
    """
    get overlapping consecutive features
    @param fetaures the features to test
    @param circular circularity of the genome
    @param size size of the genome
    @return a list of pairs (i, c) where i and i+1 overlap by c
    """
    ovl = []
    for i in range(len(features)):
        cap = feature.cap(
            features[i].start,
            features[i].stop,
            features[(i + 1) % len(features)].start,
            features[(i + 1) % len(features)].stop,
            circular,
            size,
        )

        if cap > 0:
            ovl.append((i, cap))
    return ovl


def problems_internal_stops(features, sequence, code):
    """
    check for stop codons in protein coding genes
    @param[in] features list of features
    @param[in] sequence the sequence
    @param[in] code genetic code
    @return set of gene names mit internal stop codons

    """
    istop = set()
    for feat in features:
        if feat.type != "gene":
            continue
        mito_frag = sequence.subseq(feat.start, feat.stop, feat.strand)
        mito_frag = str(mito_frag.translate(table=code))
        if mito_frag[-1] == "*":
            mito_frag = mito_frag[:-1]
        if "*" in mito_frag:
            istop.add(feat.name)
    return istop


def problems(prot, ctrna, rrna, cr, features, circular, sequence, code):
    """
    determine lists of potential problems and peculiarities
    missing, duplicated/split genes
    @param prot consider protein
    @param ctrna consider tRNAs
    @param rrna consider rRNAs
    @param cr consider control region
    @param features the list of features that should be checked for problems
    @param circular sequence circularity
    @param sequence the original sequence
    @param code the genetic code
    @return a tuple containing missing, duplicated/split, non-standard features, translational exception
    """

    consider = []
    dup = []
    mis = []
    nst = []
    texc = []
    if prot:
        consider += mito.metazoa_prot
    if ctrna:
        consider += mito.metazoa_trna
    if rrna:
        consider += mito.metazoa_rrna
    if cr:
        consider += mito.rep_origin

    for c in consider:
        cf = [x.name for x in features if x.name == c]
        if len(cf) == 0:
            mis.append(c)
        elif len(cf) > 1:
            dup += cf

    for f in features:
        if f.name not in consider:
            nst.append(f.name)
        if f.type == "gene":
            startc = blast._get_codon(f.start, f.strand, sequence)
            stopc = blast._get_codon(f.stop - 2, f.strand, sequence)

            if f.strand < 0:
                startc, stopc = stopc, startc

            fl = f.length(circular, len(sequence))
            stopc = [x for x in stopc]
            stopc = stopc[(3 - (fl % 3)) % 3 :]
            while len(stopc) < 3:
                stopc.append("N")
            stopc = trna.codon("".join(stopc), "codon")

            if not startc.isstart(code) or not stopc.isstop(code):
                texc.append([f])
                if not startc.isstart(code):
                    texc[-1].append(startc)
                else:
                    texc[-1].append(None)

                polyastop = trna.codon(str(stopc).replace("N", "A"), "codon")
                if not (stopc.isstop(code) or polyastop.isstop(code)):
                    texc[-1].append(stopc)
                else:
                    texc[-1].append(None)

            if len(texc) > 0 and texc[-1][1] is None and texc[-1][2] is None:
                del texc[-1]

    mis = _Counter(mis)
    dup = _Counter(dup)
    nst = _Counter(nst)
    return (mis, dup, nst, texc)


class _objectview(object):
    """
    little helper to be able to access a dictionary like an object
    """

    def __init__(self, d):
        self.__dict__ = d


def _Counter(lst):
    """
    count number of occurences of items in a list and return as dict
    @param lst a list
    @return dict linking list items to number of occurences

    note this is idendical to collections.Counter (which was introduced with python 2.7)
    """
    cnt = {}
    for i in lst:
        try:
            cnt[i] += 1
        except KeyError:
            cnt[i] = 1
    return cnt


def main():
    # TODOs remove glength parameter from mitfi system call and length
    # parameter from cmsearch function

    import argparse

    usage = "%(prog)s [options]"
    parser = argparse.ArgumentParser(prog="runmitos.py", usage=usage)

    group = parser.add_argument_group("mandatory options")
    ingroup = parser.add_mutually_exclusive_group(required=False)
    ingroup.add_argument(
        "-i", "--input", dest="file", action="store", help="the input file"
    )
    ingroup.add_argument(
        "--fasta", dest="fasta", action="store", help="input fasta sequence"
    )
    group.add_argument(
        "-c",
        "--code",
        dest="code",
        action="store",
        required=False,
        type=int,
        help="the genetic code",
    )
    group.add_argument(
        "-o",
        "--outdir",
        dest="outdir",
        action="store",
        required=True,
        help="the directory where the output is written.",
    )
    group.add_argument(
        "--linear",
        dest="circular",
        action="store_false",
        default=True,
        help="treat sequence as linear",
    )
    group.add_argument(
        "-r",
        "--refseqver",
        dest="refseqver",
        action="store",
        required=False,
        help="directory containing the reference data (relative to --refdir)",
    )

    group = parser.add_argument_group("advanced options")
    group.add_argument(
        "-R",
        "--refdir",
        dest="refdir",
        action="store",
        default="",
        required=False,
        help="base directory containing the reference data",
    )
    group.add_argument(
        "--prot",
        action="store",
        type=int,
        default=1,
        help="position of protein prediction in 1st round (0: skip)",
    )
    group.add_argument(
        "--trna",
        action="store",
        type=int,
        default=2,
        help="position of tRNA prediction in 1st round (0: skip)",
    )
    group.add_argument(
        "--rrna",
        action="store",
        type=int,
        default=3,
        help="position of rRNA prediction in 1st round (0: skip)",
    )
    group.add_argument(
        "--intron",
        action="store",
        type=int,
        default=4,
        help="position of intron prediction in 1st round (0: skip)",
    )
    group.add_argument(
        "--oril",
        action="store",
        type=int,
        default=5,
        help="position of OL prediction in 1st round (0: skip)",
    )
    group.add_argument(
        "--orih",
        action="store",
        type=int,
        default=6,
        help="position of OH prediction in 1st round (0: skip)",
    )
    group.add_argument(
        "--finovl",
        action="store",
        type=int,
        metavar="NRNT",
        default=50,
        help="final overlap <= NRNT nucleotides ",
    )
    group.add_argument(
        "--circrot",
        action="store",
        type=int,
        metavar="DEG",
        default=0,
        help="cir circular: rotate mitogenome by DEG and DEG+180",
    )
    group.add_argument(
        "--best",
        action="store_true",
        default=False,
        help="annotate only the best copy of each feature",
    )
    group.add_argument(
        "--fragfac",
        action="store",
        type=float,
        metavar="FACTOR",
        default=10,
        help="allow fragments to differ in quality/evalue by at most a factor FACTOR. Ignored if <= 0.",
    )
    group.add_argument(
        "--fragovl",
        action="store",
        type=float,
        metavar="FRACTION",
        default=0.2,
        help="allow query range overlaps up for FRACTION for fragments",
    )
    group.add_argument(
        "--noplots",
        dest="plots",
        action="store_false",
        default=True,
        help="do not create the plots.",
    )

    group = parser.add_argument_group("protein prediction advanced options")
    group.add_argument(
        "--evalue",
        dest="minevalue",
        action="store",
        type=float,
        metavar="EVL",
        default=2,
        help="discard BLAST hits with -1*log(e-value)<EVL (EVL < 1 has no effect)",
    )
    group.add_argument(
        "--cutoff",
        action="store",
        type=float,
        metavar="fraction",
        default=0.5,
        help="discard positions with quality <.5 of max",
    )
    #     group.add_argument("--maxovl", action="store", type=float, metavar="FRACTION",
    # default=0.2, help="allow overlap up to a fraction of FRACTION ")
    group.add_argument(
        "--clipfac",
        action="store",
        type=float,
        metavar="FACTOR",
        default=10,
        help="overlapping features of the same name differing by at most a factor of FACTOR are clipped",
    )
    #     group.add_argument("--ststrange", action = "store", type = "int", metavar = "NRAA", default = 6, help = "search the perimeter of start and stop positions by NRAA aminocids for better values")
    #     group.add_argument("--maxdeg", action = "store", type = "int", metavar = "NRNT", default = 2, help = "maximum number of missing nt for incomplete stop")
    group.add_argument(
        "--ncbicode",
        action="store_true",
        default=False,
        help="use start/stop codons as in NCBI (default: learned start/stop codons)",
    )

    group.add_argument(
        "--alarab",
        action="store_true",
        default=False,
        help="Use the hmmer based method of Al Arab et al. 2016. This will consider the evalue, ncbicode, fragovl, fragfac",
    )
    group.add_argument(
        "--oldstst",
        action="store_true",
        default=False,
        help="Use the old start/stop prediction method of MITOS1",
    )

    group = parser.add_argument_group(parser, "RNA prediction advanced options")
    group.add_argument(
        "--locandgloc",
        dest="localonly",
        action="store_false",
        default=True,
        help="run mitfi in glocal and local mode (default: local only)",
    )
    group.add_argument(
        "--ncev",
        action="store",
        type=float,
        default=0.01,
        help="evalue to use for inferal fast mode",
    )
    group.add_argument(
        "--sensitive",
        action="store_true",
        default=False,
        help="use infernals sensitive mode only",
    )
    group.add_argument(
        "--maxtrnaovl",
        action="store",
        type=int,
        metavar="NT",
        default=50,
        help="allow tRNA overlap of up to X nt for mitfi",
    )
    group.add_argument(
        "--maxrrnaovl",
        action="store",
        type=int,
        metavar="NT",
        default=50,
        help="allow rRNA overlap of up to X nt for mitfi",
    )

    group = parser.add_argument_group("debug/misc options")
    group.add_argument(
        "--debug", action="store_true", default=False, help="print debug output"
    )
    group.add_argument("--zip", action="store_true", default=False, help="create zip")
    group.add_argument(
        "--json",
        default=None,
        help="a JSON file with parameters. then outdir is the only other argument needed.",
    )
    group.add_argument(
        "--version",
        action="version",
        version="%(prog)s {version}".format(version=__version__),
    )
    args = parser.parse_args()

    if args.json is not None:
        # get commandline arg/default as dict
        dargs = {}
        for o in dir(args):
            if o.startswith("_"):
                continue
            dargs[o] = getattr(args, o)

        f = open(args.json)
        jargs = json.load(f)
        f.close()

        # overwrite default args with json file contents
        for a in jargs:
            dargs[a] = jargs[a]

        args = _objectview(dargs)

    if args.refseqver is None:
        parser.error("no reference data directory given")
    if args.refdir != "":
        refdir = os.path.join(args.refdir, args.refseqver)
    elif "MITOS_REFDIR" in os.environ:
        refdir = os.path.join(os.environ["MITOS_REFDIR"], args.refseqver)
    else:
        refdir = args.refseqver

    if not os.path.isdir(refdir):
        parser.error("no such directory %s" % refdir)
    if args.file is None and args.fasta is None:
        parser.error("no input file/fasta given")
    elif args.file is not None and args.fasta is not None:
        parser.error("both file and fasta given")

    if not os.path.isdir(args.outdir):
        parser.error("no such directory %s" % args.outdir)

    if args.code is None:
        parser.error("no genetic code given")

    if args.alarab and not os.path.isdir(os.path.join(refdir, "featureProtHMM")):
        parser.error(
            "--alarab can only be used if the reference data contains HMMs in a subdirectory featureProtHMM"
        )

    if args.debug:
        logging.basicConfig(format="%(levelname)s - %(message)s", level=logging.DEBUG)
        logging.debug("debug on")

    orderdict = {
        "gene": args.prot,
        "tRNA": args.trna,
        "rRNA": args.rrna,
        "intron": args.intron,
        "OL": args.oril,
        "OH": args.orih,
    }
    order = [x for x in sorted(orderdict, key=orderdict.get) if orderdict[x] > 0]

    # get sequences from file / fasta
    if args.file is not None:
        fh = open(args.file)
    else:
        fh = io.StringIO(args.fasta)
    sequences = sequence_info_fromfilehandle(fh, circular=args.circular)
    fh.close()

    for i in range(len(sequences)):
        if len(sequences) > 1:
            odir = args.outdir + "/%d/" % i
            if not os.path.exists(odir):
                os.mkdir(odir)
        else:
            odir = args.outdir

        acc = sequences[i]["id"]

        # create temporaty sequence file in output dir

        for d in ["id", "name", "description"]:
            sequences[i][d] = re.sub("[()?|\t]", "_", sequences[i][d])

        with open("%s/sequence.fas" % odir, "w") as tmpf:
            sr = SeqRecord(
                seq=sequences[i]["sequence"],
                id=sequences[i]["id"],
                name=sequences[i]["name"],
                description=sequences[i]["description"],
            )
            SeqIO.write(sr, tmpf, "fasta")

        # MITOS
        featurelist = mitos(
            "%s/sequence.fas" % odir,
            args.code,
            args.ncbicode,
            args.best,
            order,
            args.alarab,
            odir,
            cutoff=args.cutoff,
            minevalue=args.minevalue,
            finovl=args.finovl,
            clipfac=args.clipfac,
            fragovl=args.fragovl,
            fragfac=args.fragfac,
            # prot=args.noprot, trna=args.notrna, rrna=args.norrna, cr=args.noorig\
            sensitive=args.sensitive,
            localonly=args.localonly,
            refdir=refdir,
            ncev=args.ncev,
            circular=args.circular,
            circrot=args.circrot,
            trnaovl=args.maxtrnaovl,
            rrnaovl=args.maxrrnaovl,
            plots=args.plots,
            oldstst=args.oldstst,
        )

        bedfile.bedwriter(featurelist, acc, outfile="%s/result.bed" % odir)
        tbl.tblwriter(featurelist, acc, outfile="%s/result.seq" % odir)
        gfffile.gffwriter(
            featurelist,
            acc,
            len(sequences[i]["sequence"]),
            args.circular,
            outfile="%s/result.gff" % odir,
            mode="w",
        )
        feature.genorderwriter(featurelist, acc, "%s/result.geneorder" % odir)
        fastawriter(
            featurelist,
            sequences[i]["sequence"],
            None,
            acc,
            "fas",
            outfile="%s/result.fas" % odir,
        )
        fastawriter(
            featurelist,
            sequences[i]["sequence"],
            args.code,
            acc,
            "faa",
            outfile="%s/result.faa" % odir,
        )

        # draw via external programm since reportlab prints
        # to stderr which should not be visible https://github.com/Distrotech/reportlab/issues/15
        cmd = [
            "drawmitos",
            "--input",
            f"{odir}/result.bed",
            "--output",
            f"{odir}/result.png",
            "--length",
            str(len(sequences[0]["sequence"])),
        ]
        util.execute(cmd, supress_warning=True)

        # parse fasta header
        sequence = sequences[i]["sequence"]
        mis, dup, nst, texc = problems(
            orderdict["gene"] > 0,
            orderdict["tRNA"] > 0,
            orderdict["rRNA"] > 0,
            orderdict["OH"] > 0 or orderdict["OL"] > 0,
            featurelist,
            args.circular,
            sequence,
            args.code,
        )
        istop = problems_internal_stops(featurelist, sequence, args.code)
        if len(mis) > 0:
            sys.stdout.write("missing:")
            for key, value in list(mis.items()):
                sys.stdout.write("%s " % (key))
            sys.stdout.write("\n")
        if len(dup) > 0:
            sys.stdout.write("duplicated:")
            for key, value in list(dup.items()):
                sys.stdout.write("%dx %s " % (value, key))
            sys.stdout.write("\n")
        if len(nst) > 0:
            sys.stdout.write("non standard:")
            for key, value in list(nst.items()):
                sys.stdout.write("%dx %s " % (value, key))
            sys.stdout.write("\n")
        if len(texc) > 0:
            sys.stdout.write("translational exceptions:\n")
            for f in texc:
                sys.stdout.write(
                    "\t%s,%d,%d,%d (%s, %s)\n"
                    % (f[0].name, f[0].strand, f[0].start, f[0].stop, f[1], f[2])
                )
        if len(istop) > 0:
            sys.stdout.write("internal stops: ")
            sys.stdout.write(" ".join(istop) + "\n")

        # remove temporary sequence file
        os.remove("%s/sequence.fas" % odir)

    if args.zip:
        shutil.make_archive(os.path.normpath(odir), "zip", odir)


if __name__ == "__main__":
    main()
