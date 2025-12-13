"""
@author: M. Bernt

Module that provides the diferent methods to merge featurelist.
"""

import logging
from typing import Dict, List, Union

from mitos import feature
from mitos.mitfi import cmrealign


def featureappend(
    appendList, featurelist, nfeaturelist, circular, length, overlap, rnd=False
):
    """
    append a given list of features to an existing list of features such that
    no conflict emerges

    conflict: overlap is larger than the maximum, i.e. >overlap or >len(tRNA)-1
    for tRNA rRNA overlaps

    if the rnd flag is set to True:
    if tRNA-rRNA overlap with tRNA e-value > 10^-3 and tRNA included in rRNA
    the tRNA is removed

    @param[in,out] appendList the list of new features to be checked for insertion
    @param[in,out] featurelist the list where the new features should be appended
    @param[in,out] nfeaturelist the list where the non features should be appended
    @param[in] circular the circularity of the genome
    @param[in] length the length of the genome
    @param[in] overlap maximum allowed overlap of two features
    @param[in] rnd remove "low quality" tRNAs (from the feature list) that overlaps an rRNA (in appendList/featurelist)
    """

    # for tRNA check
    mintRNAscore = 1e-3

    # over new features
    for ffeat in appendList:
        flen = ffeat.length(circular, length)
        logging.debug("featureappend %s" % str(ffeat))
        # the tRNA that have to less score
        delettRNA = []
        # set "put it in feature list" default True
        conflict = False
        # over the old featurelist
        for sfeat in featurelist:
            slen = sfeat.length(circular, length)
            # if sfeat.strand != ffeat.strand and (sfeat.type == "gene" and ffeat.type == "rRNA" or ffeat.type == "gene" and sfeat.type == "rRNA"):
            #    continue

            # set overlap to default
            maxoverlap = overlap
            # calculate the overlap
            cap = feature.cap(
                ffeat.start, ffeat.stop, sfeat.start, sfeat.stop, circular, length
            )

            # whatever the overlap is .. inclusion is forbidden .. except for endonucleases encoded in introns
            # (since for these continue is called also inclusion > maxovl is possible)
            if cap == slen or cap == flen:
                # Intron encoded proteins can be included (usual restrictions
                # apply if they overlap)
                if (
                    ffeat.type == "Intron"
                    and sfeat.name in ["lagli", "giy"]
                    and cap == slen
                ) or (
                    sfeat.type == "Intron"
                    and ffeat.name in ["lagli", "giy"]
                    and cap == flen
                ):
                    continue
                else:
                    logging.debug("featureappend \t conflict %s" % str(sfeat))
                    conflict = True
                    break

            # for tRNA - rRNA: check if the overlap is len(tRNA) -1
            if (sfeat.type == "tRNA" and ffeat.type == "rRNA") or (
                ffeat.type == "tRNA" and sfeat.type == "rRNA"
            ):

                if sfeat.type == "tRNA":
                    tr = sfeat
                    # rr = ffeat
                else:
                    tr = ffeat
                    # rr = sfeat

                maxoverlap = max(overlap, tr.length(circular, length) - 1)
                # delete only in the first rnd
                if rnd:
                    # if the tRNAs evalue is insufficient AND
                    # the overlap is too large or the tRNA is included in the rRNA
                    # then the tRNA is marked to be removed
                    if tr.evalue > mintRNAscore and (
                        cap > maxoverlap or cap == tr.length(circular, length)
                    ):
                        delettRNA.append(tr)
                        continue

            # if overlap is > maximum allowed -> set the
            # conflict flag and stop search for another conflicting feature
            if cap > maxoverlap:
                logging.debug("featureappend \t conflict %s [%f]" % (str(sfeat), cap))
                conflict = True
                break

        # if no conflicting feature is already in the list -> add it
        if not conflict:
            featurelist.append(ffeat)

            # over the tRNA to delete
            for delfeat in delettRNA:
                logging.debug(
                    "featureappend: remove %s %d %d for %s %d %d"
                    % (
                        delfeat.name,
                        delfeat.start,
                        delfeat.stop,
                        ffeat.name,
                        ffeat.start,
                        ffeat.stop,
                    )
                )
                nfeaturelist.append(delfeat)
                featurelist.remove(delfeat)
        else:
            nfeaturelist.append(ffeat)
            logging.debug(
                "featureappend: not adding %s %d %d"
                % (ffeat.name, ffeat.start, ffeat.stop)
            )

    featurelist.sort(key=lambda x: x.start)
    nfeaturelist.sort(key=lambda x: x.start)

    return featurelist


def appendlocalfeature(
    lokalHits,
    lname,
    rrnafeat,
    featurelist,
    seqlen,
    allowoverlap=35,
    circular=True,
    debug=False,
):
    """
    tries to fit in possible local hits.

    A) a gap is searched, i.e. a region between two genes
    1 if there is a global hit (which did not fit in) then a gap is searched
      only in the region covered by the best global hit. except if there
      is no gap in this region, then the mode 2 is employed
      larger gaps are prefered.
    2 if there is no global hit the complete genome is considered.


    In both modes the the gap that can take the best hit is searched.
    That is the first gap that can take an (as goods as possible) feature.
    The best features are tested first starting with the largest gaps.

    B) When the gap was found all local hits are removed that do not fit
    in the gap. Thus, also more than the best local hit can be chosen.

    C) Finally the chosen local hits are checked if they overlap each other.
    Good ones are preferred.

    @param[in] lokalHits the local hits for the rRNA with name lname
        - included features that overlap features in featurelist are removed
        - but the remaining list is not the same as the features that are
          appended to featurelist!
    @param[] lname the name of the rRNA
    @param[] rrnafeat the global hits (to check if there is any. even
             if it is not included in the featurelist [due to overlap])
    @param[in,out] featurelist the current list of features predicted by MITOS
    @param[in] seqlen length of the sequence
        - features from lokalHits are included if not in conflict
    @param[] allowoverlap max allowed overlap with features in featurelist
             (for tRNAs len-1 is allowed)
    @param[in] circular circularity of the genome
    @param[in] length length of the genome
    """

    # sort local hits by evalue. determines potential insertion order
    lokalHits.sort(key=lambda x: (-x.mito, x.evalue))

    # sort features by start position for efficient overlap check
    featurelist.sort(key=lambda x: x.start)

    # get the hits of the global search for the considered RNA
    globalhit = [x for x in rrnafeat if x.name == lname]
    globalhit.sort(key=lambda x: (-x.mito, x.evalue))

    # set for global
    anfang = 0
    ende = 0
    localgap = False

    # get the list of gaps between features
    # - gaps: just the plain gaps
    # - egaps: the gaps extended by the allowed overlap
    # note: featurelist is treated circular in the first place linear
    # sequences are postprocessed
    egaps = []
    gaps = []
    # note the iteration is done circular manner regardless if the genome is
    # this is fixed below
    for j in range(len(featurelist)):
        el = featurelist[j].stop
        le = el - min(allowoverlap, featurelist[j].length(circular, seqlen) - 1)

        r = featurelist[(j + 1) % len(featurelist)].start - 1
        re = r + min(
            allowoverlap,
            featurelist[(j + 1) % len(featurelist)].length(circular, seqlen) - 1,
        )

        gaps.append((el, r))
        egaps.append((le, re))

    if not circular:
        gaps.insert(0, (0, gaps[-1][1]))
        gaps[-1][1] = seqlen - 1
        egaps.insert(0, (0, egaps[-1][1]))
        egaps[-1][1] = seqlen - 1

        gaps = [(max(l, 0), min(r, seqlen - 1)) for (l, r) in gaps if r > l]
        egaps = [(max(l, 0), min(r, seqlen - 1)) for (l, r) in egaps if r > l]
    else:
        gaps = [(l % seqlen, r % seqlen) for (l, r) in gaps]
        # if ( feature.length( r, l, circular, seqlen ) > feature.length( l, r,
        # circular, seqlen ) and feature.length( l, r, circular, seqlen ) >= 0 ) ]
        egaps = [(l % seqlen, r % seqlen) for (l, r) in egaps]
    # if ( feature.length( r, l, circular, seqlen ) > feature.length( l, r,
    # circular, seqlen ) and feature.length( l, r, circular, seqlen ) >= 0 ) ]

    #     print "append local features"
    #     print "local"
    #     for l in lokalHits:
    #         print l.name, l.start, l.stop
    #     print "into"
    #     for f in featurelist:
    #         print f.name, f.start, f.stop
    #     print "global"
    #     for g in globalhit:
    #         print g.name, g.start, g.stop, g.mito, g.evalue
    #     print "-----"

    for i in range(len(gaps)):
        logging.debug(
            "gap {idx} {gap} e {egap}".format(idx=i, gap=gaps[i], egap=egaps[i])
        )

    # if there is a global hit then the only consider the region covered by the
    # _best_ global hit, i.e. the local features are fitted in the gaps between
    # the features in/overlapping this region. the largest gap where a local
    # feature fits perfectly is chosen if no such gap exists the largest is
    # taken
    if len(globalhit) > 0:
        logging.debug("appendlocalfeature: globalhit")
        #        print "GLOBALHIT"

        # get the start and end position of the best global hit
        globalanfang = globalhit[0].start
        globalende = globalhit[0].stop

        # get the gaps that overlap with the best global hit
        ggaps = [
            (l, r)
            for (l, r) in gaps
            if feature.cap(l, r, globalanfang, globalende, circular, seqlen)
        ]

        # sort the gaps in decreasing by their length (large first)
        ggaps.sort(key=lambda x: -feature.length(x[0], x[1], circular, seqlen))

        # if there are gaps .. fit it in
        if len(ggaps):

            # determine the local features that fit perfectly in a gap
            perfecthit = [f for f in lokalHits if (f.start, f.stop) in ggaps]

            # if there is no such perfect match take the largest gap
            if len(perfecthit) == 0:
                logging.debug("appendlocalfeature: local feature does not fit perfect")
                globalanfang = ggaps[0][0]
                globalende = ggaps[0][1]
            else:
                logging.debug("appendlocalfeature: local feature fits perfect")
                globalanfang = perfecthit[0].start
                globalende = perfecthit[0][1]
                if len(perfecthit) > 1:
                    logging.error(
                        "appendlocalfeature: unexpected more than one local hit fits perfectly"
                    )

            # determine the corresponding extended gap
            # - sort by overlap
            # - take the one with the largest overlap
            egaps.sort(
                key=lambda left, right: feature.cap(
                    left, right, globalanfang, globalende, circular, seqlen
                ),
                reverse=True,
            )
            if (
                feature.cap(
                    egaps[0][0], egaps[0][1], globalanfang, globalende, circular, seqlen
                )
                > 0
            ):
                anfang = egaps[0][0]
                ende = egaps[0][1]
            else:
                logging.error("appendlocalfeature: no corresponding extended gap found")
                localgap = True

            # sort by if it is in the global hit then sort after mitos and then
            # sort after evalue
            lokalHits.sort(
                key=lambda x: (
                    feature.cap(
                        x.start, x.stop, globalanfang, globalende, circular, seqlen
                    )
                    <= 0,
                    -x.mito,
                    x.evalue,
                )
            )

        # otherwise if there is no gap inbeween the features in the global hit then fit the
        # feature between any two features (i.e. not necessarily in the region of
        # the globalhit) -> localgap = True
        else:
            localgap = True

        if localgap:
            logging.debug("appendlocalfeature: global hit unsuccessfull")
        else:
            logging.debug("appendlocalfeature: global hit successfull")

    # if there is no global hit
    else:
        localgap = True

    # if there is no glocal hit or the local ones did not fit in the
    # gaps between the features covered by the global hit
    if localgap:
        logging.debug("appendlocalfeature: localgap")
        # get the gap with the best local feature (i.e. best evalue)
        i = 0
        # determine anfang and ende (i.e. start and stop of the gap where the best
        # local feature is fits in)
        # therefore loop over all local features (starting with the best)
        # and check if it does not overlap with any feature in featurelist
        gapfound = False
        while i < len(lokalHits):
            if len(featurelist) == 0:
                ende = seqlen - 1
                break

            for g in egaps:
                if feature.cap(
                    lokalHits[i].start, lokalHits[i].stop, g[0], g[1], circular, seqlen
                ) == lokalHits[i].length(circular, seqlen):
                    anfang = g[0]
                    ende = g[1]
                    gapfound = True
                    break

            if gapfound:
                break

            i += 1

    logging.debug("appendlocalfeature: anfang %d ende %d" % (anfang, ende))

    # insert features into the featurelist if
    # - they fit in the determined gap (anfang,ende)
    # - if their queryrange does not interfere with the one of previously
    #   added local features (by more than allowoverlap)
    query = set()
    for lf in lokalHits:
        logging.debug(lf)
        if feature.cap(lf.start, lf.stop, anfang, ende, circular, seqlen) < lf.length(
            circular, seqlen
        ):
            logging.debug("appendlocalfeature: \tremove .. to less overlap with gap")
            continue

        fqset = set(range(lf.qstart, lf.qstop))
        if len(query.intersection(fqset)) > allowoverlap:
            logging.debug(
                "appendlocalfeature: \tremove ..  to much overlap with other features"
            )
            continue

        query |= fqset  # append fqset positions
        logging.debug(
            "appendlocalfeature: final %s %d %d" % (lf.name, lf.start, lf.stop)
        )
        featurelist.append(lf)

    return featurelist


def checklocalfeature(
    localcheck,
    featurelist,
    sequence,
    refdir,
    circular,
    length,
):
    """
    - remove single local feature <= 55 nt

    - check and combine consecutive features that have been determined with
      local search if they can be merged:
      * same name, same strand
      * difference of the distance in sequence and query by factor < 1.5

    @param localcheck the list of names of the rRNA(s) to check
    @param featurelist the list of features
    @param sequence the sequence of the genome
    @param refdir
    @param circular is the sequence circular
    @param length sequence length
    """

    # over all lokal append rRNA's
    for lname in localcheck:

        # get all features in the feature list which are due to local features
        localfeats = [x for x in featurelist if x.name == lname]
        #        print localfeats

        # remove if single feature shorter 56
        if len(localfeats) == 1 and localfeats[0].length(circular, length) <= 55:
            logging.debug(
                "checklocalfeature: remove %s %d %d (single & <55)"
                % (localfeats[0].name, localfeats[0].start, localfeats[0].stop)
            )
            featurelist.remove(localfeats[0])
            continue

    featurelist.sort(key=lambda x: x.start)

    i = 0
    while i < len(featurelist):
        if not circular and i == (len(featurelist) - 1):
            break

        ii = (i + 1) % len(featurelist)

        if circular and i == ii:  # in case there in only 1 feature
            break

        # features to merge must have the same name and in localcheck (i.e.
        # there must be local features of this type)
        if (
            featurelist[i].name not in localcheck
            or featurelist[i].name != featurelist[ii].name
        ):
            i += 1
            continue

        info = "%s %d %d %d (%d %d) with %s %d %d %d (%d %d)" % (
            featurelist[i].name,
            featurelist[i].strand,
            featurelist[i].start,
            featurelist[i].stop,
            featurelist[i].qstart,
            featurelist[i].qstop,
            featurelist[ii].name,
            featurelist[ii].strand,
            featurelist[ii].start,
            featurelist[ii].stop,
            featurelist[ii].qstart,
            featurelist[ii].qstop,
        )
        # logging.error( "checklocalfeature: %s" % ( info ) )

        # features to merge must be on the same strand
        if featurelist[i].strand != featurelist[ii].strand:
            logging.debug("checklocalfeature: incompatible strand %s" % (info))
            i += 1
            continue

        # distance of the 2 features in the query positions, calculated as
        # distance of the mid points of the query ranges
        querydist = (
            (featurelist[ii].qstop - featurelist[ii].qstart) / 2.0
            + featurelist[ii].qstart
            - (
                (featurelist[i].qstop - featurelist[i].qstart) / 2.0
                + featurelist[i].qstart
            )
        )

        # features to merge must be in the same direction wrt query and
        # reference
        if (
            querydist > 0
            and featurelist[i].strand < 0
            or querydist <= 0
            and featurelist[i].strand > 0
        ):
            logging.debug("checklocalfeature: wrong direction %s" % (info))
            i += 1
            continue

        # distance of the two features on the sequence
        genomdist = feature.length(
            featurelist[i].midposition(circular, length),
            featurelist[ii].midposition(circular, length),
            circular,
            length,
        )

        # features to merge must be in approx the same distance in query and
        # reference
        try:
            faktor = abs(genomdist) / abs(querydist)
        except ZeroDivisionError:
            faktor = 0

        if (2 / 3.0) >= faktor or faktor >= 1.5:
            i += 1
            logging.debug("checklocalfeature: 2/3 >= factor >= 3/2 %s" % (info))
            continue

        logging.debug("checklocalfeature: merge %s" % (info))
        # get start and stop position, sequence, and a structure (from
        # cmrealign)
        start = featurelist[i].start
        stop = featurelist[ii].stop

        sseq = str(sequence.subseq(start, stop, featurelist[i].strand))

        struct = cmrealign(sseq, featurelist[i].name, refdir)

        newfeat = feature.mitfifeature(
            name=featurelist[i].name,
            tpe="rRNA",
            start=start,
            stop=stop,
            strand=featurelist[i].strand,
            score=(featurelist[i].score + featurelist[ii].score) / 2.0,
            sequence=sseq,
            struct=struct,
            anticodonpos=None,
            anticodon=None,
            qstart=min(featurelist[i].qstart, featurelist[ii].qstart),
            qstop=max(featurelist[i].qstop, featurelist[ii].qstop),
            evalue=(featurelist[i].evalue + featurelist[ii].evalue) / 2.0,
            bitscore=(featurelist[i].bitscore + featurelist[ii].bitscore) / 2.0,
            model=featurelist[i].name,
            local=True,
            mito=(featurelist[i].mito + featurelist[ii].mito + 1) / 2.0,
        )
        #
        featurelist[i] = newfeat
        del featurelist[ii]

    return featurelist


def _copy_part(
    hits: List[Union[feature.blast_feature, feature.mitfifeature]],
    fragovl: float,
    fragfac: float,
) -> Dict[str, Dict[int, List[Union[feature.blast_feature, feature.mitfifeature]]]]:
    """
    determine the copy and part numbers of the features based on query positions
    old info is overwritten

    @param[in,out] hits a list of blast_feature where the positions are sought
    @param fragovl max fraction allowed that two hits overlap to be counted as
         fragments
    @param[in] fragfac max factor by which fragments (ie parts) of one copy may
        differ in their score
    @return index hits of each copy: idx[n][c] includes the list of hits
        belonging to copy c of gene n (c might be None)
    """

    # reset copy and part info
    for h in hits:
        h.copy = None
        h.part = None

    # dictionary to aggregate the copies and their parts
    # predictions[n][c][p] prediction of gene n, copy c, and part p
    predictions: Dict[
        str, List[List[Union[feature.blast_feature, feature.mitfifeature]]]
    ] = dict()

    # sort hits by corresponding attributes:
    # - blast features by score - must be -log(evalue) and
    # - mitfi features by evalue)
    bfeat = [x for x in hits if isinstance(x, feature.blast_feature)]
    ifeat = [x for x in hits if isinstance(x, feature.mitfifeature)]
    assert len(bfeat) + len(ifeat) == len(hits)

    bfeat.sort(key=lambda x: [x.name, x.score], reverse=True)
    ifeat.sort(key=lambda x: [x.name, x.evalue], reverse=False)

    hits = bfeat + ifeat

    # upper and lower bound defined by fragfac
    if fragfac > 0:
        fragfaclb = 1.0 / float(fragfac)
        fragfacub = 1.0 * float(fragfac)
    else:
        fragfaclb = 0
        fragfacub = float("inf")

    for h in hits:
        logging.debug("check %s " % (h))

        if h.name not in predictions:
            predictions[h.name] = []

        # check for each of the already determined copies if the current
        # prediction fits in
        newhit = True
        for j in range(len(predictions[h.name])):

            logging.debug("check against")
            for x in predictions[h.name][j]:
                logging.debug("\t %s %d %d %d " % (x.name, x.qstart, x.qstop, x.strand))

            # now check for each part of the current "copy" if the height
            # and query overlap is appropriate
            appropriate = True
            for k in range(len(predictions[h.name][j])):
                pred0 = predictions[h.name][j][0]
                if isinstance(h, feature.blast_feature):
                    assert isinstance(pred0, feature.blast_feature)
                    fac = float(h.score) / predictions[h.name][j][0].score
                else:
                    assert isinstance(h, feature.mitfifeature)
                    assert isinstance(pred0, feature.mitfifeature)
                    if h.evalue != 0.0 and pred0.evalue != 0:
                        fac = float(h.evalue) / pred0.evalue
                    elif h.evalue == 0.0 and pred0.evalue == 0:
                        # accept the hit .. has the same e-value
                        fac = (fragfaclb + fragfacub) / 2.0
                    elif h.evalue != 0.0 and pred0.evalue == 0:
                        if h.evalue <= 0.001:
                            # accept the hit .. its good enough
                            fac = (fragfaclb + fragfacub) / 2.0
                        else:
                            fac = 2.0 * fragfacub
                    else:
                        logging.error(
                            "wrong combination of  h.evalue and predictions[h.name][j][0].evalue"
                        )
                        raise Exception("internal error")

                # combine only if in the same league wrt. the height
                if not fragfaclb <= fac <= fragfacub:
                    logging.debug("! high enough %f" % (fac))
                    appropriate = False
                    break

                qstart = predictions[h.name][j][k].qstart
                qstop = predictions[h.name][j][k].qstop

                cap, cup = feature.capcup(
                    h.qstart, h.qstop, qstart, qstop, circular=False, size=0
                )
                logging.debug(
                    "cap %d cup %d len %d %d %d - %d %d - %d"
                    % (
                        cap,
                        cup,
                        feature.length(h.qstart, h.qstop, False, 0),
                        feature.length(qstart, qstop, False, 0),
                        h.qstart,
                        h.qstop,
                        qstart,
                        qstop,
                    )
                )

                if (
                    cap / float(feature.length(h.qstart, h.qstop, False, 0)) > fragovl
                    or cap / float(feature.length(qstart, qstop, False, 0)) > fragovl
                ):
                    logging.debug(
                        "too much overlap %f %f"
                        % (
                            cap / float(feature.length(h.qstart, h.qstop, False, 0)),
                            cap / float(feature.length(qstart, qstop, False, 0)),
                        )
                    )
                    appropriate = False
                    break

            # if the currently considered prediction fits in this copy
            # 1) append it, mark that it was inserted into an existing copy,
            # and do not check other copies
            if appropriate:
                predictions[h.name][j].append(h)
                # sort by query position
                predictions[h.name][j].sort(key=lambda k: k.qstart)
                newhit = False
                break

        if newhit:
            logging.debug("new hit")
            predictions[h.name].append([h])

    # Assing copy and part numbers to the features
    cpyprt: Dict[
        str, Dict[int, List[Union[feature.blast_feature, feature.mitfifeature]]]
    ] = {}
    for name in list(predictions.keys()):
        cpyprt[name] = {}
        k = 0
        for phits in predictions[name]:
            for i in range(len(phits)):
                if len(predictions[name]) > 1:
                    phits[i].copy = k
                if len(phits) > 1:
                    phits[i].part = i
            cpyprt[name][k] = phits
            k += 1

    return cpyprt
