import argparse
import glob
import os
import pickle
import time
from os import listdir

import numpy as np
from Bio import AlignIO, SeqIO

# 23 JAN : check where is the error in the annotation, before or after the alignment position

# fasta_files_dir = "/Users/Abdullah/Documents/PhD/work/mitos-extension/test2/fasta_files/"
# tab_files_dir = "/Users/Abdullah/Documents/PhD/work/mitos-extension/test2/fasta_files/tab_output"
output_dir = "/homes/brauerei/abdullah/Desktop/PhD/python/mtdbnew/src/Metazoa-new/Paper_revision/"
groups_dir = "/homes/brauerei/abdullah/Desktop/PhD/python/mtdbnew/src/Metazoa-new/Paper_revision/"

# full_groups_dir ="/homes/brauerei/abdullah/Desktop/PhD/python/mtdbnew/src/Metazoa-new/New_Equations/"
full_groups_dir = "/homes/brauerei/abdullah/Desktop/PhD/python/mtdbnew/src/Metazoa-new/Metazoa.007/abdul-results/Deuterostomia/"


suspecious_OH = []
suspecious_OL = []
all_OH_starts = []
all_OH_ends = []


def get_features(gbfile):
    gbhandle = open(gbfile, "r")
    record = SeqIO.read(gbhandle, "gb")
    gbhandle.close()

    return record.features, record.seq


def OH_annotation_shift(
    bedfile, genetoshift, seq_length, accession
):  # ## another option would be to shift OH and OL in different functions to solve the case where some species have only one of the origins
    OH_start = 0
    OH_end = 0

    global suspecious_OH
    global all_OH_starts

    all_OH = []
    res_OH = []
    f = open(bedfile)
    arr = []
    for line in f:
        line = line.split()
        line[0] = str(line[0])
        line[1] = int(line[1])
        line[2] = int(line[2])
        line[3] = str(line[3])
        line[4] = str(line[4])

        if line[3].startswith("OH"):
            OH_start = int(line[1])
            OH_end = int(line[2])
            all_OH.append((OH_start, OH_end))

        if OH_start > OH_end:
            suspecious_OH.append(("OH", accession))

        # if OH_end - OL_start > 40:
        #     suspecious_OL.append(accession)

        if line[3].startswith(genetoshift):
            genetoshift_start = line[1]
            # genetoshift_end = line[2]

        arr.append(line)

    if not all_OH:
        print("No OH found for accession " + accession)
    else:
        for i in range(len(all_OH)):
            OH_mid_position = ((all_OH[i][1] + all_OH[i][0]) / 2) % seq_length

            if all_OH[i][0] < genetoshift_start:

                OH_shiftedstart = (
                    all_OH[i][0] + (seq_length - genetoshift_start)
                ) % seq_length
                OH_shiftedend = (
                    all_OH[i][1] + (seq_length - genetoshift_start)
                ) % seq_length

                OH_shifted_mid_position = (
                    OH_mid_position + (seq_length - genetoshift_start)
                ) % seq_length
            else:
                OH_shiftedstart = all_OH[i][0] - genetoshift_start
                OH_shiftedend = all_OH[i][1] - genetoshift_start

                OH_shifted_mid_position = OH_mid_position - genetoshift_start

            #             if (all_OH[i][1] < genetoshift_end):
            #                 OH_shiftedend = (all_OH[i][1] + (seq_length - genetoshift_start)) % seq_length
            #             else:
            #                 OH_shiftedend = all_OH[i][1] - genetoshift_start
            #
            res_OH.append((OH_shiftedstart, OH_shiftedend, OH_shifted_mid_position))
    return res_OH


def OL_annotation_shift(
    bedfile, genetoshift, seq_length, accession
):  # ## another option would be to shift OH and OL in different functions to solve the case where some species have only one of the origins

    global suspecious_OL

    OL_start = 0
    OL_end = 0
    all_OL = []
    res_OL = []
    f = open(bedfile)
    arr = []
    for line in f:
        line = line.split()
        line[0] = str(line[0])
        line[1] = int(line[1])
        line[2] = int(line[2])
        line[3] = str(line[3])
        line[4] = str(line[4])

        if line[3].startswith("OL"):
            OL_start = int(line[1])
            OL_end = int(line[2])
            all_OL.append((OL_start, OL_end))
        # print all_OL
        #         if OL_start > OL_end:
        #             suspecious_OL.append(("OL",accesion,"1"))
        #
        #         if OL_end - OL_start > 40:
        #             suspecious_OL.append(("OL",accession, "2"))
        #
        #
        # suspecious_OL.append((accession,OL_start, OL_end))
        if line[3].startswith(genetoshift):
            genetoshift_start = line[1]
            # genetoshift_end = line[2]

        arr.append(line)

    if not all_OL:
        print("No OL found for accession " + accession)
    else:
        for i in range(len(all_OL)):
            OL_mid_position = ((all_OL[i][1] + all_OL[i][0]) / 2) % seq_length
            if all_OL[i][0] < genetoshift_start:

                OL_shifted_mid_position = (
                    OL_mid_position + (seq_length - genetoshift_start)
                ) % seq_length

                OL_shiftedstart = (
                    all_OL[i][0] + (seq_length - genetoshift_start)
                ) % seq_length
                OL_shiftedend = (
                    all_OL[i][1] + (seq_length - genetoshift_start)
                ) % seq_length

            else:

                OL_shifted_mid_position = OL_mid_position - genetoshift_start

                OL_shiftedstart = all_OL[i][0] - genetoshift_start
                OL_shiftedend = all_OL[i][1] - genetoshift_start

            res_OL.append((OL_shiftedstart, OL_shiftedend, OL_shifted_mid_position))
    #
    # continue

    #    if accession == "NC_009683":
    #        print "NC_009683",res_OL
    #    if accession == "NC_008773":
    #        print "NC_008773", res_OL
    # print "OL", accession, res_OL
    return res_OL


def positioninalignment(alignseq, seqpos):
    apos = 0
    if seqpos == 0:
        return 0
    while seqpos > 0:
        # print apos
        if alignseq[apos] != "-":
            seqpos -= 1
        apos += 1

    return apos - 1


def sequence_positions(geneorder, shifted_ori_alignment_mid, accession, groupdir):

    # ## how should we deal with gene order groups?? should we take them as one group or each one of them as a group???
    # print groupdir, geneorder
    seq_alignment = AlignIO.read(
        groupdir
        + "/fasta-files/"
        + geneorder
        + "/nad1-shifted-fasta-"
        + geneorder
        + ".aln",
        "clustal",
    )  # contain a multiple alignement data type
    # final_origins = []

    for ai in range(len(seq_alignment)):
        if seq_alignment[ai].id == accession:
            shifted_ori_sequence_mid = positioninnormalseq(
                seq_alignment[ai], shifted_ori_alignment_mid
            )

        else:
            # print "no no no", accession
            continue
    # print shifted_ori_alignment_mid
    return shifted_ori_sequence_mid


def mid_alignment_positions(geneorder, shifted_ori_mid, accession, groupdir):

    # ## how should we deal with gene order groups?? should we take them as one group or each one of them as a group???
    # print groupdir, geneorder
    seq_alignment = AlignIO.read(
        groupdir
        + "/fasta-files/"
        + geneorder
        + "/nad1-shifted-fasta-"
        + geneorder
        + ".aln",
        "clustal",
    )  # contain a multiple alignement data type
    # final_origins = []

    for ai in range(len(seq_alignment)):
        if seq_alignment[ai].id == accession:
            shifted_ori_alignment_mid = positioninalignment(
                seq_alignment[ai], shifted_ori_mid
            )

        else:
            # print "no no no", accession
            continue
    # print shifted_ori_alignment_mid
    return shifted_ori_alignment_mid


def alignment_positions(
    geneorder, shifted_ori_start, shifted_ori_end, accession, groupdir
):

    # ## how should we deal with gene order groups?? should we take them as one group or each one of them as a group???
    # print groupdir, geneorder
    seq_alignment = AlignIO.read(
        groupdir
        + "/fasta-files/"
        + geneorder
        + "/nad1-shifted-fasta-"
        + geneorder
        + ".aln",
        "clustal",
    )  # contain a multiple alignement data type
    # final_origins = []
    # OH_start = []
    # OH_end = []
    # OL_start = []
    # OL_end = []

    for ai in range(len(seq_alignment)):
        if seq_alignment[ai].id == accession:
            shifted_ori_alignment_start = positioninalignment(
                seq_alignment[ai], shifted_ori_start
            )
            shifted_ori_alignment_end = positioninalignment(
                seq_alignment[ai], shifted_ori_end
            )

        else:
            # print "no no no", accession
            continue

    return shifted_ori_alignment_start, shifted_ori_alignment_end


def column(matrix, i):
    return [row[i] for row in matrix]


def get_replication_origins():  # ### get origins from bed files instead -- 14 JAN : generate new bed files and run the analysis on them instead and check if things changes
    """

    In some groups, the max start is larger than the min end, this is caused by some wrong annotations in the RefSeq of some species,
    this needs to be fixed manually and wrong annotations which should not belong to this positions in the genome needs to be removed or changed.
    """
    global groups_dir
    all_seq_features = {}
    list_files = {}
    for path, directories, files in os.walk(os.path.dirname(full_groups_dir)):
        if "geneorder" in path:  # already filtered based on size
            geneorder = path.split("/")[-1]
            group = path.split("/")[-3]

            if group not in list_files:
                list_files[group] = {}
            if geneorder not in list_files[group]:
                list_files[group][geneorder] = [
                    f.replace(".fas", ".bed")
                    for f in listdir(path)
                    if f.startswith("NC_") and f.endswith("fas")
                ]

    # test = []

    # ### update bed should be runned before on the full_groups_dir in order that the new_beds are created
    for path, directories, files in os.walk(os.path.dirname(full_groups_dir)):
        if "new_bed" in path and "inverted-species" not in path:
            for gr in list_files:
                if path.split("/")[-2] == gr:
                    # print gr
                    for go in list_files[gr]:
                        # alignment_positions(path[:-8],go, 12, 12)
                        for fl in list_files[gr][go]:
                            # OH_shifted_start = 0
                            # OH_shifted_end = 0
                            # OL_shifted_start = 0
                            # OL_shifted_end = 0
                            gbfile = fl.replace(".bed", ".gb")
                            record = SeqIO.read(
                                os.path.join(path[:-7] + "gb-files/", gbfile), "genbank"
                            )
                            accession = record.name

                            try:

                                OH_coord = OH_annotation_shift(
                                    os.path.join(path, fl),
                                    "nad1",
                                    len(record.seq),
                                    accession,
                                )

                            except Exception:
                                continue
                            try:

                                OL_coord = OL_annotation_shift(
                                    os.path.join(path, fl),
                                    "nad1",
                                    len(record.seq),
                                    accession,
                                )
                                # print OL_coord
                            except Exception:
                                continue

                            if gr == "Xenoturbella":
                                print(OH_coord, accession)
                            if gr not in all_seq_features:
                                all_seq_features[gr] = {}
                            if go not in all_seq_features[gr]:
                                all_seq_features[gr][go] = {}
                            if accession not in all_seq_features[gr][go]:
                                all_seq_features[gr][go][accession] = {}
                            # all_seq_features[gr][go].append((accession, OH_shifted_start, OH_shifted_end,OL_shifted_start, OL_shifted_end,path[:-9]))
                            all_seq_features[gr][go][accession]["OH"] = OH_coord
                            all_seq_features[gr][go][accession]["OL"] = OL_coord
                            all_seq_features[gr][go][accession]["path"] = path[:-8]

    # print all_seq_features
    OH_start = []
    OH_end = []

    OL_start = []
    OL_end = []

    result = []
    # ol_start_pos = []
    # ol_end_pos = []

    # oh_start_pos = []
    # oh_end_pos = []

    # shifted_OH_mid_alignment_positions = []
    # shifted_OL_mid_alignment_positions = []
    for taxa in all_seq_features:
        for go in all_seq_features[taxa]:
            for acc in all_seq_features[taxa][go]:

                for i in range(len(all_seq_features[taxa][go][acc]["OH"])):
                    shifted_OH_align_start, shifted_OH_align_end = alignment_positions(
                        go,
                        all_seq_features[taxa][go][acc]["OH"][i][0],
                        all_seq_features[taxa][go][acc]["OH"][i][1],
                        acc,
                        all_seq_features[taxa][go][acc]["path"],
                    )

                    OH_start.append(
                        sequence_positions(
                            go,
                            shifted_OH_align_start,
                            acc,
                            all_seq_features[taxa][go][acc]["path"],
                        )
                    )
                    OH_end.append(
                        sequence_positions(
                            go,
                            shifted_OH_align_end,
                            acc,
                            all_seq_features[taxa][go][acc]["path"],
                        )
                    )

                    # shifted_OH_mid_alignment_positions.append(mid_alignment_positions(go, all_seq_features[taxa][go][acc]['OH'][i][2],acc, all_seq_features[taxa][go][acc]['path']))

                for j in range(len(all_seq_features[taxa][go][acc]["OL"])):
                    shifted_OL_align_start, shifted_OL_align_end = alignment_positions(
                        go,
                        all_seq_features[taxa][go][acc]["OL"][j][0],
                        all_seq_features[taxa][go][acc]["OL"][j][1],
                        acc,
                        all_seq_features[taxa][go][acc]["path"],
                    )

                    OL_start.append(
                        sequence_positions(
                            go,
                            shifted_OL_align_start,
                            acc,
                            all_seq_features[taxa][go][acc]["path"],
                        )
                    )
                    OL_end.append(
                        sequence_positions(
                            go,
                            shifted_OL_align_end,
                            acc,
                            all_seq_features[taxa][go][acc]["path"],
                        )
                    )

                    # OL_start.append(shifted_OL_align_start)
                    # OL_end.append(shifted_OL_align_end)
                    # print all_seq_features[taxa][go][acc]['OL'][i]

                    # shifted_OL_mid_alignment_positions.append(mid_alignment_positions(go, all_seq_features[taxa][go][acc]['OL'][j][2],acc, all_seq_features[taxa][go][acc]['path']))
            # print taxa, go,  sum(shifted_OH_mid_alignment_positions)/len(shifted_OH_mid_alignment_positions), sum(shifted_OL_mid_alignment_positions)/len(shifted_OL_mid_alignment_positions)
            # if len(all_seq_features[taxa][go]) == 1:        ## in the case where we have only 1 species in this geneorder group

            # print sum(shifted_OH_mid_alignment_positions), len(shifted_OH_mid_alignment_positions)
            # result.append((taxa, go, sum(shifted_OH_mid_alignment_positions)/float(len(shifted_OH_mid_alignment_positions)), sum(shifted_OL_mid_alignment_positions)/float(len(shifted_OL_mid_alignment_positions))))
            # else:
            # result.append((taxa,go, max(OH_start), min(OH_end), max(OL_start), min(OL_end)))

            #             if not shifted_OH_mid_alignment_positions and not shifted_OL_mid_alignment_positions:
            #                 continue
            #             elif not shifted_OH_mid_alignment_positions:
            #                 print "\n No OH annotated for "+ taxa+ " "+go
            #                 OL_mid_sequence_positions = mid_sequence_positions(go, sum(shifted_OL_mid_alignment_positions)/len(shifted_OL_mid_alignment_positions),acc, all_seq_features[taxa][go][acc]['path'])
            #                 result.append((taxa, go,  "No_OH_RefSeq",OL_mid_sequence_positions))
            #
            #             elif not shifted_OL_mid_alignment_positions:
            #                 print "No OL annotated for "+ taxa+ " "+go + "\n"
            #                 OH_mid_sequence_positions = mid_sequence_positions(go, sum(shifted_OH_mid_alignment_positions)/len(shifted_OH_mid_alignment_positions),acc, all_seq_features[taxa][go][acc]['path'])
            #                 result.append((taxa, go,  OH_mid_sequence_positions, "No_OL_RefSeq"))
            #
            #             else:
            #                 OH_mid_sequence_positions = mid_sequence_positions(go, sum(shifted_OH_mid_alignment_positions)/len(shifted_OH_mid_alignment_positions),acc, all_seq_features[taxa][go][acc]['path'])
            #                 OL_mid_sequence_positions = mid_sequence_positions(go, sum(shifted_OL_mid_alignment_positions)/len(shifted_OL_mid_alignment_positions),acc, all_seq_features[taxa][go][acc]['path'])
            #                 result.append((taxa, go,  OH_mid_sequence_positions, OL_mid_sequence_positions))
            #
            # print taxa,go, OH_start
            if not OH_start and not OL_start:
                continue

            elif not OH_start:
                print("\n No OH annotated for " + taxa + " " + go)
                # result.append((taxa, go,  "No_OH_RefSeq",OL_mid_sequence_positions))
                result.append(
                    (
                        taxa,
                        go,
                        "No_OH_RefSeq",
                        "No_OH_RefSeq",
                        max(OL_start),
                        min(OL_end),
                        all_seq_features[taxa][go][acc]["path"],
                    )
                )
            elif not OL_start:
                print("No OL annotated for " + taxa + " " + go + "\n")

                # OH_mid_sequence_positions = mid_sequence_positions(go, sum(shifted_OH_mid_alignment_positions)/len(shifted_OH_mid_alignment_positions),acc, all_seq_features[taxa][go][acc]['path'])
                # result.append((taxa, go,  OH_mid_sequence_positions, "No_OL_RefSeq"))
                result.append(
                    (
                        taxa,
                        go,
                        max(OH_start),
                        min(OH_end),
                        "No_OL_RefSeq",
                        "No_OL_RefSeq",
                        all_seq_features[taxa][go][acc]["path"],
                    )
                )

            else:
                # OH_mid_sequence_positions = mid_sequence_positions(go, sum(shifted_OH_mid_alignment_positions)/len(shifted_OH_mid_alignment_positions),acc, all_seq_features[taxa][go][acc]['path'])
                # OL_mid_sequence_positions = mid_sequence_positions(go, sum(shifted_OL_mid_alignment_positions)/len(shifted_OL_mid_alignment_positions),acc, all_seq_features[taxa][go][acc]['path'])
                # result.append((taxa, go,  OH_mid_sequence_positions, OL_mid_sequence_positions))

                # OHstart,OHend = sequence_positions(go, max(OH_start),acc, all_seq_features[taxa][go][acc]['path']), sequence_positions(go, min(OH_end),acc, all_seq_features[taxa][go][acc]['path'])
                # OLstart,OLend = sequence_positions(go, max(OL_start),acc, all_seq_features[taxa][go][acc]['path']), sequence_positions(go, min(OL_end),acc, all_seq_features[taxa][go][acc]['path'])
                result.append(
                    (
                        taxa,
                        go,
                        max(OH_start),
                        min(OH_end),
                        max(OL_start),
                        min(OL_end),
                        all_seq_features[taxa][go][acc]["path"],
                    )
                )

            del OH_start[:]
            del OH_end[:]

            del OL_start[:]
            del OL_end[:]
        # print taxa, go, result
    #             del shifted_OH_mid_alignment_positions[:]
    #             del shifted_OL_mid_alignment_positions[:]
    print(result)
    return result


def get_one_species_replication_origins():  # ### get origins from bed files instead -- 14 JAN : generate new bed files and run the analysis on them instead and check if things changes

    """

    In this function, we only take one species from each group as a represntative of this group in order to avoid the start > end problem of the control region
    """
    global groups_dir
    all_seq_features = {}
    list_files = {}
    for path, directories, files in os.walk(os.path.dirname(full_groups_dir)):
        if "geneorder" in path:  # already filtered based on size
            geneorder = path.split("/")[-1]
            group = path.split("/")[-3]

            if group not in list_files:
                list_files[group] = {}
            if geneorder not in list_files[group]:
                list_files[group][geneorder] = [
                    f.replace(".fas", ".bed")
                    for f in listdir(path)
                    if f.startswith("NC_") and f.endswith("fas")
                ]

    # test = []

    # ### update bed should be runned before on the full_groups_dir in order that the new_beds are created
    for path, directories, files in os.walk(os.path.dirname(full_groups_dir)):
        if "new_bed" in path and "inverted-species" not in path:
            for gr in list_files:
                if path.split("/")[-2] == gr:
                    # print gr
                    for go in list_files[gr]:
                        # alignment_positions(path[:-8],go, 12, 12)
                        for fl in list_files[gr][go]:
                            # OH_shifted_start = 0
                            # OH_shifted_end = 0
                            # OL_shifted_start = 0
                            # OL_shifted_end = 0
                            gbfile = fl.replace(".bed", ".gb")
                            record = SeqIO.read(
                                os.path.join(path[:-7] + "gb-files/", gbfile), "genbank"
                            )
                            accession = record.name

                            try:

                                OH_coord = OH_annotation_shift(
                                    os.path.join(path, fl),
                                    "nad1",
                                    len(record.seq),
                                    accession,
                                )

                            except Exception:
                                continue
                            try:

                                OL_coord = OL_annotation_shift(
                                    os.path.join(path, fl),
                                    "nad1",
                                    len(record.seq),
                                    accession,
                                )
                                # print OL_coord
                            except Exception:
                                continue

                            if gr not in all_seq_features:
                                all_seq_features[gr] = {}
                            if go not in all_seq_features[gr]:
                                all_seq_features[gr][go] = {}
                            if accession not in all_seq_features[gr][go]:
                                all_seq_features[gr][go][accession] = {}
                            # all_seq_features[gr][go].append((accession, OH_shifted_start, OH_shifted_end,OL_shifted_start, OL_shifted_end,path[:-9]))
                            all_seq_features[gr][go][accession]["OH"] = OH_coord
                            all_seq_features[gr][go][accession]["OL"] = OL_coord
                            all_seq_features[gr][go][accession]["path"] = path[:-8]

    # print all_seq_features
    #     OH_start = []
    #     OH_end = []
    #
    #     OL_start = []
    #     OL_end = []

    result = []
    # ol_start_pos = []
    # ol_end_pos = []

    # oh_start_pos = []
    # oh_end_pos = []

    # shifted_OH_mid_alignment_positions = []
    # shifted_OL_mid_alignment_positions = []
    for taxa in all_seq_features:
        for go in all_seq_features[taxa]:
            for acc in all_seq_features[taxa][go]:

                for i in range(len(all_seq_features[taxa][go][acc]["OH"])):

                    if (
                        all_seq_features[taxa][go][acc]["OH"][i][0]
                        < all_seq_features[taxa][go][acc]["OH"][i][1]
                        and all_seq_features[taxa][go][acc]["OH"][i][0] > 10000
                    ):
                        (
                            shifted_OH_align_start,
                            shifted_OH_align_end,
                        ) = alignment_positions(
                            go,
                            all_seq_features[taxa][go][acc]["OH"][i][0],
                            all_seq_features[taxa][go][acc]["OH"][i][1],
                            acc,
                            all_seq_features[taxa][go][acc]["path"],
                        )

                        OH_start = sequence_positions(
                            go,
                            shifted_OH_align_start,
                            acc,
                            all_seq_features[taxa][go][acc]["path"],
                        )
                        OH_end = sequence_positions(
                            go,
                            shifted_OH_align_end,
                            acc,
                            all_seq_features[taxa][go][acc]["path"],
                        )
                        break
                    # shifted_OH_mid_alignment_positions.append(mid_alignment_positions(go, all_seq_features[taxa][go][acc]['OH'][i][2],acc, all_seq_features[taxa][go][acc]['path']))

                for j in range(len(all_seq_features[taxa][go][acc]["OL"])):

                    if (
                        all_seq_features[taxa][go][acc]["OL"][j][0]
                        < all_seq_features[taxa][go][acc]["OL"][j][1]
                        and all_seq_features[taxa][go][acc]["OL"][j][0] < 4000
                    ):
                        (
                            shifted_OL_align_start,
                            shifted_OL_align_end,
                        ) = alignment_positions(
                            go,
                            all_seq_features[taxa][go][acc]["OL"][j][0],
                            all_seq_features[taxa][go][acc]["OL"][j][1],
                            acc,
                            all_seq_features[taxa][go][acc]["path"],
                        )

                        OL_start = sequence_positions(
                            go,
                            shifted_OL_align_start,
                            acc,
                            all_seq_features[taxa][go][acc]["path"],
                        )
                        OL_end = sequence_positions(
                            go,
                            shifted_OL_align_end,
                            acc,
                            all_seq_features[taxa][go][acc]["path"],
                        )
                        break

            if not OH_start and not OL_start:
                continue

            elif not OH_start:
                print("\n No OH annotated for " + taxa + " " + go)
                # result.append((taxa, go,  "No_OH_RefSeq",OL_mid_sequence_positions))
                result.append(
                    (
                        taxa,
                        go,
                        "No_OH_RefSeq",
                        "No_OH_RefSeq",
                        OL_start,
                        OL_end,
                        all_seq_features[taxa][go][acc]["path"],
                    )
                )
            elif not OL_start:
                print("No OL annotated for " + taxa + " " + go + "\n")
                # OH_mid_sequence_positions = mid_sequence_positions(go, sum(shifted_OH_mid_alignment_positions)/len(shifted_OH_mid_alignment_positions),acc, all_seq_features[taxa][go][acc]['path'])
                # result.append((taxa, go,  OH_mid_sequence_positions, "No_OL_RefSeq"))
                result.append(
                    (
                        taxa,
                        go,
                        OH_start,
                        OH_end,
                        "No_OL_RefSeq",
                        "No_OL_RefSeq",
                        all_seq_features[taxa][go][acc]["path"],
                    )
                )
            else:
                # OH_mid_sequence_positions = mid_sequence_positions(go, sum(shifted_OH_mid_alignment_positions)/len(shifted_OH_mid_alignment_positions),acc, all_seq_features[taxa][go][acc]['path'])
                # OL_mid_sequence_positions = mid_sequence_positions(go, sum(shifted_OL_mid_alignment_positions)/len(shifted_OL_mid_alignment_positions),acc, all_seq_features[taxa][go][acc]['path'])
                # result.append((taxa, go,  OH_mid_sequence_positions, OL_mid_sequence_positions))

                # OHstart,OHend = sequence_positions(go, max(OH_start),acc, all_seq_features[taxa][go][acc]['path']), sequence_positions(go, min(OH_end),acc, all_seq_features[taxa][go][acc]['path'])
                # OLstart,OLend = sequence_positions(go, max(OL_start),acc, all_seq_features[taxa][go][acc]['path']), sequence_positions(go, min(OL_end),acc, all_seq_features[taxa][go][acc]['path'])
                result.append(
                    (
                        taxa,
                        go,
                        OH_start,
                        OH_end,
                        OL_start,
                        OL_end,
                        all_seq_features[taxa][go][acc]["path"],
                    )
                )

            OH_start = 0
            OH_end = 0

            OL_start = 0
            OL_end = 0
        # print taxa, go, result
    #             del shifted_OH_mid_alignment_positions[:]
    #             del shifted_OL_mid_alignment_positions[:]
    print(result)
    # return result


def unique_rows(a):
    new_array = [tuple(row) for row in a]
    uniques = np.unique(new_array)
    return uniques


def if_intersect(predicted_pos, refseq_pos_start, refseq_pos_end):
    predicted_pos = int(predicted_pos)
    if predicted_pos > 1:
        predicted_pos_minus = [t for t in range(predicted_pos, predicted_pos - 100, -1)]
        predicted_pos_plus = [t for t in range(predicted_pos, predicted_pos + 100, 1)]
        predicted_pos = predicted_pos_plus + predicted_pos_minus

    else:
        predicted_pos = [t for t in range(predicted_pos, predicted_pos + 100, 1)]

    refseq_pos = list(range(refseq_pos_start, refseq_pos_end + 1))

    set_predicted_pos = set(predicted_pos)
    set_refseq_pos = set(refseq_pos)

    output = list(set_predicted_pos.intersection(set_refseq_pos))

    if not output:
        return False

    else:
        return True


def statistics(refseq_results, pval_threshold, final_result):
    """
    get from our results the data points predicted for a set of pvalue thresholds (0 -> 1) and output for each data point if its TN,FN,TP,FP based on the control region exctracted from the RefSeq
    this should be applied for both models presented in the manuscript.

    since we have a step size of 200, the comparison with the intervals generated from RefSeq for the control region does not make sense since we cannot match coordinates smaller than the step size. so the idea is to
    to take the 200 nucleotide nucleotide around the point we predicted and check if the RefSeq annotation overlapps with it or no
    """

    #     final_result = open(output_dir+"final_stats_old.txt","w")
    # print refseq_results
    for i in range(len(refseq_results)):
        our_arr = []  # contains our predictions

        if os.path.exists(
            refseq_results[i][6]
            + "/"
            + refseq_results[i][1]
            + "-merged_tables_revisions.txt"
        ):

            with open(
                refseq_results[i][6]
                + "/"
                + refseq_results[i][1]
                + "-merged_tables_revisions.txt"
            ) as f:
                # next(f)
                for line in f:
                    if line.startswith('"vOH"'):
                        continue
                    line = line.split()

                    line[0] = str(line[0])
                    line[1] = float(line[1])
                    line[2] = float(line[2])
                    line[3] = float(line[3])
                    line[4] = float(line[4])
                    pred_OH = line[1]
                    pred_OL = line[2]
                    gcslope = line[3]
                    pval = line[4]

                    # ############# IMP : i should add an if statement to only append the rows that have a negative GC-skew

                    # print refseq_results[i][0], pred_OH, pred_OL
                    our_arr.append((pred_OH, pred_OL, gcslope, pval))
        # print "111111111111111111111111",our_arr
        # print refseq_results[i][0], refseq_results[i][1], len(our_arr)

        #         np_our_arr = np.array(our_arr)
        #         our_unique_arr = unique_rows(np_our_arr)
        #         our_unique_arr = our_unique_arr.tolist()

        our_unique_arr = our_arr

        #         if not refseq_results[i][2] == "No_OH_RefSeq":
        #             print refseq_results[i][0], refseq_results[i][1],pval_threshold,refseq_results[i][2],refseq_results[i][3],refseq_results[i][4],refseq_results[i][5]
        #             for xx in range(len(our_unique_arr)):       ## for OH
        #
        #                 if our_unique_arr[xx][2] > 0 and our_unique_arr[xx][3] <= pval_threshold:
        #                     final_result.write(refseq_results[i][0]+" "+refseq_results[i][1]+" "+str(our_unique_arr[xx][0])+" "+str(our_unique_arr[xx][1])+" FP "+str(pval_threshold)+"\n")
        #
        #                 elif our_unique_arr[xx][2] > 0 and our_unique_arr[xx][3] > pval_threshold:
        #                     final_result.write(refseq_results[i][0]+" "+refseq_results[i][1]+" "+str(our_unique_arr[xx][0])+" "+str(our_unique_arr[xx][1])+" TN "+str(pval_threshold)+"\n")
        #
        #
        #                 elif if_intersect(our_unique_arr[xx][0], refseq_results[i][2], refseq_results[i][3]) is True and our_unique_arr[xx][3] <= pval_threshold:   ## only matched OH, and prediction -> TP
        #
        #                     final_result.write(refseq_results[i][0]+" "+refseq_results[i][1]+" "+str(our_unique_arr[xx][0])+" "+str(our_unique_arr[xx][1])+" TP "+str(pval_threshold)+"\n")
        #
        #                 elif if_intersect(our_unique_arr[xx][0], refseq_results[i][2], refseq_results[i][3]) is True and our_unique_arr[xx][3] > pval_threshold:    ## only match OH, and no prediction -> FN
        #
        #                     final_result.write(refseq_results[i][0]+" "+refseq_results[i][1]+" "+str(our_unique_arr[xx][0])+" "+str(our_unique_arr[xx][1])+" FN "+str(pval_threshold)+"\n")
        #
        #                 elif not if_intersect(our_unique_arr[xx][0], refseq_results[i][2], refseq_results[i][3]) is True and our_unique_arr[xx][3] <= pval_threshold:   ## mismatched OH, and prediction -> TP
        #
        #                     final_result.write(refseq_results[i][0]+" "+refseq_results[i][1]+" "+str(our_unique_arr[xx][0])+" "+str(our_unique_arr[xx][1])+" FP "+str(pval_threshold)+"\n")
        #
        #                 elif not if_intersect(our_unique_arr[xx][0], refseq_results[i][2], refseq_results[i][3]) is True and our_unique_arr[xx][3] > pval_threshold:    ## only match OH, and no prediction -> FN
        #
        #                     final_result.write(refseq_results[i][0]+" "+refseq_results[i][1]+" "+str(our_unique_arr[xx][0])+" "+str(our_unique_arr[xx][1])+" TN "+str(pval_threshold)+"\n")
        #
        #
        #                 else:
        #                     print our_unique_arr[xx][0],our_unique_arr[xx][1],our_unique_arr[xx][2]

        #
        #         if not refseq_results[i][4] == "No_OL_RefSeq":  ## for OL
        #             print refseq_results[i][0], refseq_results[i][1],pval_threshold,refseq_results[i][2],refseq_results[i][3],refseq_results[i][4],refseq_results[i][5]
        #             for xx in range(len(our_unique_arr)):
        #
        #                 if our_unique_arr[xx][2] > 0 and our_unique_arr[xx][3] <= pval_threshold:
        #                     final_result.write(refseq_results[i][0]+" "+refseq_results[i][1]+" "+str(our_unique_arr[xx][0])+" "+str(our_unique_arr[xx][1])+" FP "+str(pval_threshold)+"\n")
        #
        #                 elif our_unique_arr[xx][2] > 0 and our_unique_arr[xx][3] > pval_threshold:
        #                     final_result.write(refseq_results[i][0]+" "+refseq_results[i][1]+" "+str(our_unique_arr[xx][0])+" "+str(our_unique_arr[xx][1])+" TN "+str(pval_threshold)+"\n")
        #
        #
        #                 elif if_intersect(our_unique_arr[xx][1], refseq_results[i][4], refseq_results[i][5]) is True and our_unique_arr[xx][3] <= pval_threshold:   ## only matched OH, and prediction -> TP
        #
        #                     final_result.write(refseq_results[i][0]+" "+refseq_results[i][1]+" "+str(our_unique_arr[xx][0])+" "+str(our_unique_arr[xx][1])+" TP "+str(pval_threshold)+"\n")
        #
        #                 elif if_intersect(our_unique_arr[xx][1], refseq_results[i][4], refseq_results[i][5]) is True and our_unique_arr[xx][3] > pval_threshold:    ## only match OH, and no prediction -> FN
        #
        #                     final_result.write(refseq_results[i][0]+" "+refseq_results[i][1]+" "+str(our_unique_arr[xx][0])+" "+str(our_unique_arr[xx][1])+" FN "+str(pval_threshold)+"\n")
        #
        #                 elif not if_intersect(our_unique_arr[xx][1], refseq_results[i][4], refseq_results[i][5]) is True and our_unique_arr[xx][3] <= pval_threshold:   ## mismatched OH, and prediction -> TP
        #
        #                     final_result.write(refseq_results[i][0]+" "+refseq_results[i][1]+" "+str(our_unique_arr[xx][0])+" "+str(our_unique_arr[xx][1])+" FP "+str(pval_threshold)+"\n")
        #
        #                 elif not if_intersect(our_unique_arr[xx][1], refseq_results[i][4], refseq_results[i][5]) is True and our_unique_arr[xx][3] > pval_threshold:    ## only match OH, and no prediction -> FN
        #
        #                     final_result.write(refseq_results[i][0]+" "+refseq_results[i][1]+" "+str(our_unique_arr[xx][0])+" "+str(our_unique_arr[xx][1])+" TN "+str(pval_threshold)+"\n")
        #
        #
        #                 else:
        #                     print our_unique_arr[xx][0],our_unique_arr[xx][1],our_unique_arr[xx][2]
        #
        #

        # TP : position is inside RefSeq, and was predicted as inside
        # FP : position not inside RefSeq, but was predicted as inside
        # TN : position is not inside RefSeq, and was predicted as not inside
        # FN : position inside RefSeq, and was predcited as not inside

        if (
            not refseq_results[i][2] == "No_OH_RefSeq"
            and not refseq_results[i][4] == "No_OL_RefSeq"
        ):  # both OH and OL are found in RefSeq, we only save these cases and we ignore the case where one (or both) origin is missing from RefSeq
            print(
                refseq_results[i][0],
                refseq_results[i][1],
                pval_threshold,
                refseq_results[i][2],
                refseq_results[i][3],
                refseq_results[i][4],
                refseq_results[i][5],
            )

            for xx in range(len(our_unique_arr)):

                if (
                    if_intersect(
                        our_unique_arr[xx][0],
                        refseq_results[i][2],
                        refseq_results[i][3],
                    )
                    is True
                    and if_intersect(
                        our_unique_arr[xx][1],
                        refseq_results[i][4],
                        refseq_results[i][5],
                    )
                    is True
                ):  # both are found, True
                    if (
                        our_unique_arr[xx][2] < 0
                        and our_unique_arr[xx][3] <= pval_threshold
                    ):  # correct slope and pval <= threshold -> positive

                        final_result.write(
                            refseq_results[i][0]
                            + " "
                            + refseq_results[i][1]
                            + " "
                            + str(our_unique_arr[xx][0])
                            + " "
                            + str(our_unique_arr[xx][1])
                            + " TP "
                            + str(pval_threshold)
                            + "\n"
                        )

                    else:  # negative
                        final_result.write(
                            refseq_results[i][0]
                            + " "
                            + refseq_results[i][1]
                            + " "
                            + str(our_unique_arr[xx][0])
                            + " "
                            + str(our_unique_arr[xx][1])
                            + " FN "
                            + str(pval_threshold)
                            + "\n"
                        )

                elif (
                    if_intersect(
                        our_unique_arr[xx][0],
                        refseq_results[i][2],
                        refseq_results[i][3],
                    )
                    is True
                    and if_intersect(
                        our_unique_arr[xx][1],
                        refseq_results[i][4],
                        refseq_results[i][5],
                    )
                    is False
                ):  # found only OH, False
                    if (
                        our_unique_arr[xx][2] < 0
                        and our_unique_arr[xx][3] <= pval_threshold
                    ):  # correct slope and pval <= threshold -> positive

                        final_result.write(
                            refseq_results[i][0]
                            + " "
                            + refseq_results[i][1]
                            + " "
                            + str(our_unique_arr[xx][0])
                            + " "
                            + str(our_unique_arr[xx][1])
                            + " FP "
                            + str(pval_threshold)
                            + "\n"
                        )

                    else:  # negative
                        final_result.write(
                            refseq_results[i][0]
                            + " "
                            + refseq_results[i][1]
                            + " "
                            + str(our_unique_arr[xx][0])
                            + " "
                            + str(our_unique_arr[xx][1])
                            + " TN "
                            + str(pval_threshold)
                            + "\n"
                        )

                elif (
                    if_intersect(
                        our_unique_arr[xx][0],
                        refseq_results[i][2],
                        refseq_results[i][3],
                    )
                    is False
                    and if_intersect(
                        our_unique_arr[xx][1],
                        refseq_results[i][4],
                        refseq_results[i][5],
                    )
                    is True
                ):  # found only OL, False
                    if (
                        our_unique_arr[xx][2] < 0
                        and our_unique_arr[xx][3] <= pval_threshold
                    ):  # correct slope and pval <= threshold -> positive

                        final_result.write(
                            refseq_results[i][0]
                            + " "
                            + refseq_results[i][1]
                            + " "
                            + str(our_unique_arr[xx][0])
                            + " "
                            + str(our_unique_arr[xx][1])
                            + " FP "
                            + str(pval_threshold)
                            + "\n"
                        )

                    else:  # negative
                        final_result.write(
                            refseq_results[i][0]
                            + " "
                            + refseq_results[i][1]
                            + " "
                            + str(our_unique_arr[xx][0])
                            + " "
                            + str(our_unique_arr[xx][1])
                            + " TN "
                            + str(pval_threshold)
                            + "\n"
                        )

                elif (
                    if_intersect(
                        our_unique_arr[xx][0],
                        refseq_results[i][2],
                        refseq_results[i][3],
                    )
                    is False
                    and if_intersect(
                        our_unique_arr[xx][1],
                        refseq_results[i][4],
                        refseq_results[i][5],
                    )
                    is False
                ):  # found nothing, False
                    if (
                        our_unique_arr[xx][2] < 0
                        and our_unique_arr[xx][3] <= pval_threshold
                    ):  # correct slope and pval <= threshold -> positive

                        final_result.write(
                            refseq_results[i][0]
                            + " "
                            + refseq_results[i][1]
                            + " "
                            + str(our_unique_arr[xx][0])
                            + " "
                            + str(our_unique_arr[xx][1])
                            + " FP "
                            + str(pval_threshold)
                            + "\n"
                        )

                    else:  # negative
                        final_result.write(
                            refseq_results[i][0]
                            + " "
                            + refseq_results[i][1]
                            + " "
                            + str(our_unique_arr[xx][0])
                            + " "
                            + str(our_unique_arr[xx][1])
                            + " TN "
                            + str(pval_threshold)
                            + "\n"
                        )

                else:
                    print("shiiit")

        #                 if our_unique_arr[xx][2] > 0 and our_unique_arr[xx][3] <= pval_threshold:
        #                     final_result.write(refseq_results[i][0]+" "+refseq_results[i][1]+" "+str(our_unique_arr[xx][0])+" "+str(our_unique_arr[xx][1])+" FP "+str(pval_threshold)+"\n")
        #
        #                 elif our_unique_arr[xx][2] > 0 and our_unique_arr[xx][3] > pval_threshold:
        #                     final_result.write(refseq_results[i][0]+" "+refseq_results[i][1]+" "+str(our_unique_arr[xx][0])+" "+str(our_unique_arr[xx][1])+" TN "+str(pval_threshold)+"\n")
        #
        #
        #                 elif if_intersect(our_unique_arr[xx][0], refseq_results[i][2], refseq_results[i][3]) is True and if_intersect(our_unique_arr[xx][1], refseq_results[i][4], refseq_results[i][5]) is True and our_unique_arr[xx][3] <= pval_threshold:
        #                 #if our_unique_arr[xx][0] >= refseq_results[i][2] and our_unique_arr[xx][0] <= refseq_results[i][3] and our_unique_arr[xx][1] >= refseq_results[i][4] and our_unique_arr[xx][1] <= refseq_results[i][5] and our_unique_arr[xx][2] <= pval_threshold:     ### predictions are inside the RefSeq OH,OL --> TP
        #                     final_result.write(refseq_results[i][0]+" "+refseq_results[i][1]+" "+str(our_unique_arr[xx][0])+" "+str(our_unique_arr[xx][1])+" TP "+str(pval_threshold)+"\n")
        #
        #                 elif if_intersect(our_unique_arr[xx][0], refseq_results[i][2], refseq_results[i][3]) is True and if_intersect(our_unique_arr[xx][1], refseq_results[i][4], refseq_results[i][5]) is True and our_unique_arr[xx][3] > pval_threshold:
        #                 #elif our_unique_arr[xx][0] >= refseq_results[i][2] and our_unique_arr[xx][0] <= refseq_results[i][3] and our_unique_arr[xx][1] >= refseq_results[i][4] and our_unique_arr[xx][1] <= refseq_results[i][5] and our_unique_arr[xx][2] > pval_threshold:     ### predictions are inside the RefSeq OH,OL but larger than p-value threshold --> FN
        #                     final_result.write(refseq_results[i][0]+" "+refseq_results[i][1]+" "+str(our_unique_arr[xx][0])+" "+str(our_unique_arr[xx][1])+" FN "+str(pval_threshold)+"\n")
        #
        #
        #                 elif if_intersect(our_unique_arr[xx][0], refseq_results[i][2], refseq_results[i][3]) is False and if_intersect(our_unique_arr[xx][1], refseq_results[i][4], refseq_results[i][5]) is False and our_unique_arr[xx][3] <= pval_threshold:
        #                 #elif our_unique_arr[xx][0] >= refseq_results[i][2] and our_unique_arr[xx][0] > refseq_results[i][3] and our_unique_arr[xx][1] >= refseq_results[i][4] and our_unique_arr[xx][1] >= refseq_results[i][5] and our_unique_arr[xx][2] <= pval_threshold:     ### predictions are outside the RefSeq OH,OL and smaller than p-value threshold--> FP
        #                     final_result.write(refseq_results[i][0]+" "+refseq_results[i][1]+" "+str(our_unique_arr[xx][0])+" "+str(our_unique_arr[xx][1])+" FP "+str(pval_threshold)+"\n")
        #
        #                 elif if_intersect(our_unique_arr[xx][0], refseq_results[i][2], refseq_results[i][3]) is False and if_intersect(our_unique_arr[xx][1], refseq_results[i][4], refseq_results[i][5]) is False and our_unique_arr[xx][3] > pval_threshold:
        #                 #elif our_unique_arr[xx][0] >= refseq_results[i][2] and our_unique_arr[xx][0] > refseq_results[i][3] and our_unique_arr[xx][1] >= refseq_results[i][4] and our_unique_arr[xx][1] >= refseq_results[i][5] and our_unique_arr[xx][2] > pval_threshold:     ### predictions are outside the RefSeq OH,OL and larger than p-value threshold --> TN
        #                     final_result.write(refseq_results[i][0]+" "+refseq_results[i][1]+" "+str(our_unique_arr[xx][0])+" "+str(our_unique_arr[xx][1])+" TN "+str(pval_threshold)+"\n")
        #
        #                 elif if_intersect(our_unique_arr[xx][0], refseq_results[i][2], refseq_results[i][3]) is True and if_intersect(our_unique_arr[xx][1], refseq_results[i][4], refseq_results[i][5]) is False and our_unique_arr[xx][3] <= pval_threshold:
        # #                     print our_unique_arr[xx][0],our_unique_arr[xx][1],our_unique_arr[xx][2]
        #                     final_result.write(refseq_results[i][0]+" "+refseq_results[i][1]+" "+str(our_unique_arr[xx][0])+" "+str(our_unique_arr[xx][1])+" FP "+str(pval_threshold)+"\n")
        #
        #                 elif if_intersect(our_unique_arr[xx][0], refseq_results[i][2], refseq_results[i][3]) is False and if_intersect(our_unique_arr[xx][1], refseq_results[i][4], refseq_results[i][5]) is True and our_unique_arr[xx][3] <= pval_threshold:
        #                     final_result.write(refseq_results[i][0]+" "+refseq_results[i][1]+" "+str(our_unique_arr[xx][0])+" "+str(our_unique_arr[xx][1])+" FP "+str(pval_threshold)+"\n")
        #
        #                 elif if_intersect(our_unique_arr[xx][0], refseq_results[i][2], refseq_results[i][3]) is True and if_intersect(our_unique_arr[xx][1], refseq_results[i][4], refseq_results[i][5]) is False and our_unique_arr[xx][3] > pval_threshold:
        # #
        #                     final_result.write(refseq_results[i][0]+" "+refseq_results[i][1]+" "+str(our_unique_arr[xx][0])+" "+str(our_unique_arr[xx][1])+" TN "+str(pval_threshold)+"\n")
        #
        #                 elif if_intersect(our_unique_arr[xx][0], refseq_results[i][2], refseq_results[i][3]) is False and if_intersect(our_unique_arr[xx][1], refseq_results[i][4], refseq_results[i][5]) is True and our_unique_arr[xx][3] > pval_threshold:
        #                     final_result.write(refseq_results[i][0]+" "+refseq_results[i][1]+" "+str(our_unique_arr[xx][0])+" "+str(our_unique_arr[xx][1])+" TN "+str(pval_threshold)+"\n")
        #
        #                 else:
        #                     print our_unique_arr[xx][0],our_unique_arr[xx][1],our_unique_arr[xx][2]
        del our_unique_arr[:]
        # print "1111111111",our_unique_arr
        # final_result.close()


def positioninnormalseq(alignseq, alignpos):
    gapcount = 0
    alignind = alignpos
    if alignpos == 0:
        return 0
    while alignind >= 0:
        if alignseq[alignind] == "-":
            gapcount += 1
        alignind -= 1
    return alignpos - gapcount


def cwdist(x, y, length):
    if x <= y:
        return y - x
    else:
        return length - x + y


def compare_annotations(res_origins):
    """
    res_origins : contains origins extracted from RefSeq
    """
    comparison_results = []
    for path, directories, files in os.walk(os.path.dirname(full_groups_dir)):
        if "geneorder" in path:
            geneorder = path.split("/")[-1]
            group = path.split("/")[-3]
            taxa_path = path[:-22]
            for i in range(len(res_origins)):
                if res_origins[i][1] == geneorder and res_origins[i][0] == group:
                    if os.path.exists(taxa_path + geneorder + "-min_error_points.txt"):
                        our_result = open(
                            taxa_path + geneorder + "-min_error_points.txt", "r"
                        ).readline()
                        # l = int(open(taxa_path + geneorder + "-mean-length.txt", "r").readline())
                        # print group, geneorder,taxa_path+geneorder+"-min_error_points.txt"
                        # print l
                        our_OH = int(float(our_result.split()[0]))

                        our_OL = int(float(our_result.split()[1]))

                        # difference should be : min(|d(our_OH,their_OH)|,|d(their_OH,our_OH)|)

                        # ### the differences should be both for SEQUENCe position ---------- FEB 2014
                        if res_origins[i][2] == "No_OH_RefSeq":
                            # our_best_OL = min(abs(cwdist(our_OL,res_origins[i][3], l)),abs(cwdist(res_origins[i][3],our_OL, l)))        ### the correct version 12 FEB 2014 - commented for testing
                            comparison_results.append(
                                (
                                    group,
                                    geneorder,
                                    0,
                                    our_OL - res_origins[i][3],
                                    "No_OH_RefSeq",
                                )
                            )
                            # comparison_results.append((group, geneorder, 0, our_best_OL,"No_OH_RefSeq"))
                        elif res_origins[i][3] == "No_OL_RefSeq":
                            # our_best_OH = min(abs(cwdist(our_OH,res_origins[i][2], l)),abs(cwdist(res_origins[i][2],our_OH, l)))
                            comparison_results.append(
                                (
                                    group,
                                    geneorder,
                                    our_OH - res_origins[i][2],
                                    0,
                                    "No_OL_RefSeq",
                                )
                            )
                            # comparison_results.append((group, geneorder, our_best_OH, 0,"No_OL_RefSeq"))
                        else:
                            # our_best_OL = min(abs(cwdist(our_OL,res_origins[i][3], l)),abs(cwdist(res_origins[i][3],our_OL, l)))
                            # our_best_OH = min(abs(cwdist(our_OH,res_origins[i][2], l)),abs(cwdist(res_origins[i][2],our_OH, l)))
                            comparison_results.append(
                                (
                                    group,
                                    geneorder,
                                    our_OH - res_origins[i][2],
                                    our_OL - res_origins[i][3],
                                    "Both_Refseq",
                                )
                            )
                            # comparison_results.append((group, geneorder, -our_best_OH, -our_best_OL,"Both_Refseq"))
                    else:
                        print("No clear results for " + group + " " + geneorder)
    toplot = open("test_old_eq_annotation_differences.txt", "w")
    for j in range(len(comparison_results)):
        toplot.write(
            comparison_results[j][0]
            + "\t"
            + comparison_results[j][1]
            + "\t"
            + str(comparison_results[j][2])
            + "\t"
            + str(comparison_results[j][3])
            + "\t"
            + comparison_results[j][4]
            + "\n"
        )

    # print comparison_results


#     print suspecious_OL, "\n"
# #
#     print "min OL start",min(OL_start),"\n"
#     print "max OL start",max(OL_start),"\n"
#
#     print "min OL end",min(OL_end),"\n"
#    print "max OL end",max(OL_end)
#    max_val = 0
#    acc = ""
#    for r in range(len(test)):
#        if (test[r][0] > max_val):
#            max_val = test[r][0]
#            acc = test[r][2]
#    print acc
#
#    print all_seq_features
#    for group in set(column(all_seq_features,7)):
#        #print group
#        for geneord in set(column(all_seq_features,1)):
#
#            for i in range(len(all_seq_features)):
#                #print group, geneorder, all_seq_features[i][6]
#                #print all_seq_features[i][2], all_seq_features[i][3],all_seq_features[i][4], all_seq_features[i][5], all_seq_features[i][0], all_seq_features[i][6]
#
#                shifted_OH_align_start, shifted_OH_align_end, shifted_OL_align_start, shifted_OL_align_end = alignment_positions(geneord, all_seq_features[i][2], all_seq_features[i][3],all_seq_features[i][4], all_seq_features[i][5], all_seq_features[i][0], all_seq_features[i][6])
##
#                OH_start.append(shifted_OH_align_start)
#                OH_end.append(shifted_OH_align_end)
#
#                OL_start.append(shifted_OL_align_start)
#                OL_end.append(shifted_OL_align_end)

#            result.append((group,geneord, max(OH_start), min(OH_end), max(OL_start), min(OL_end)))

#        del OH_start
#        del OH_end
#
#        del OL_start
#        del OL_end
#
#        print result
#
#                        fbed = open(os.path.join(path,fl), "r")
#                        record = SeqIO.read(os.path.join(path,fl), "genbank")
#

#                        #print gr,go, accession
#                        all_features, gbseq = get_features(os.path.join(path,fl))
#
#                        for feature in all_features:
#
#                            if feature.type == "D-loop":
#                                #print feature
#                                start = 0
#                                end = 0
#                                strand = 0
#                                log_features_locations = _parse_feature_locations(feature)
#
#                                log_features_name = _parse_feature_name(feature)
#
#
#
#                                if len(log_features_locations) > 1:
#                                #for li in range(len(log_features_locations)):
#                                    start = log_features_locations[0][0]
#                                    end = log_features_locations[len(log_features_locations)-1][1]
#                                    strand = log_features_locations[0][2]
#                                else:
#                                    start = log_features_locations[0][0]
#                                    end = log_features_locations[0][1]
#                                    strand = log_features_locations[0][2]
#
#                                shiftedstart, shiftedend = annotation_shift(path[:-8], start, end, "nad1", accession, len(gbseq))
#                                #if accession == "NC_011519":
#                                #    print accession, start, end, shiftedstart, shiftedend
#                                all_seq_features.append((accession, "OH", set(log_features_name), shiftedstart, shiftedend, len(gbseq)))
#
#                            if feature.type == "rep_origin":
#                                start = 0
#                                end = 0
#                                strand = 0
#                                log_features_locations = _parse_feature_locations(feature)
#
#                                log_features_name = _parse_feature_name(feature)
#
#
#                                if len(log_features_locations) > 1:
#                                    start = log_features_locations[0][0]
#                                    end = log_features_locations[len(log_features_locations)-1][1]
#                                    strand = log_features_locations[0][2]
#                                else:
#                                    start = log_features_locations[0][0]
#                                    end = log_features_locations[0][1]
#                                    strand = log_features_locations[0][2]
#
#
#                                shiftedstart, shiftedend = annotation_shift(path[:-8], start, end, "nad1", accession, len(gbseq))
#                                all_seq_features.append((accession, "OL", set(log_features_name), shiftedstart, shiftedend, len(gbseq))
#    print len(all_seq_features)


def _parse_feature_name(f):
    """
    try to determine the name of a feature
    for trna, rrna, and genes try to guess the name from the gene or product qualifier

    MB remove the strand parameter if not used
    @param[in] f the feature
    @param[in] strand the strand of the feature
    @return the name of None (if could not be determined)
    """

    # feature which has only this name as a qualifier -- problem

    # remove fasta files with less than 10 sequences
    features_arr = []
    for q in f.qualifiers:
        for x in f.qualifiers[q]:
            if q in ["gene", "product"]:
                # save them into file
                features_arr.append(x)
                # print x
            if q in ["standard_name", "note", "direction", "product", "gene"]:
                # save them into file
                features_arr.append(x)
                # print x
    return features_arr


def _parse_feature_locations(feat):
    """
    parse location(s) from subfeatures
    @return list of locations, i.e. list of triples (start, stop, strand)
    """
    loc = []
    if len(feat.sub_features) > 0:
        for f in feat.sub_features:
            loc += _parse_feature_locations(f)
    else:

        if feat.strand is None or feat.strand >= 0:
            strand = 1
        else:
            strand = -1

        loc.append(
            (feat.location.start.position, feat.location.end.position - 1, strand)
        )

    return loc


def get_data(gbfiles):
    """
    this function will calculate the number of genes on the +/- strand and will output the percentage of C and G on the given strand
    """
    all_seq_features = []

    for fl in gbfiles:
        maxper = ""
        record = SeqIO.read(fl, "genbank")
        accession = record.name

        all_features, gbseq = get_features(fl)

        countA = gbseq.count("A")
        perc_A = (countA * 100) / len(gbseq)

        countT = gbseq.count("T")
        perc_T = (countT * 100) / len(gbseq)

        countG = gbseq.count("G")
        perc_G = (countG * 100) / len(gbseq)

        # reverse_comp = gbseq.reverse_complement()

        countC = gbseq.count("C")
        perc_C = (countC * 100) / len(gbseq)

        if perc_G + perc_A > perc_C + perc_T:
            maxper = "G-rich"
        else:
            maxper = "C-rich"
        countp = 0
        countm = 0
        # print accession, countG, countC, maxper_G
        for feat in all_features:
            if feat.type in ["rRNA", "CDS"]:
                feat_strand = _parse_feature_strand(feat)

                if feat_strand == 1:
                    countp += 1
                else:
                    countm += 1
                    # print feat
        all_seq_features.append(
            (
                accession,
                countp,
                countm,
                maxper,
                perc_C,
                perc_G,
                perc_A + perc_G,
                perc_C + perc_T,
            )
        )

    return all_seq_features


def _parse_feature_strand(feat):
    """
    get strand from feature
    @return strand +1 or -1
    """

    if feat.strand is None or feat.strand >= 0:
        strand = 1
    else:
        strand = -1

    return strand


def coding_strand(feat_arr):
    global output_dir

    """
    Final output consist of a table as follow:

    accession    percentage of C in given strand    percenteage of G in given strand     major coding strand
    """
    f = open(output_dir + "output_tab_Chordata.txt", "w")
    for i in range(len(feat_arr)):
        if feat_arr[i][1] > feat_arr[i][2] and feat_arr[i][3] == "G-rich":
            # print "G-rich strand is major coding strand"
            f.write(
                feat_arr[i][0]
                + "\t"
                + str(feat_arr[i][1])
                + "\t"
                + str(feat_arr[i][2])
                + "\t"
                + str(feat_arr[i][4])
                + "\t"
                + str(feat_arr[i][5])
                + "\t"
                + str(feat_arr[i][6])
                + "\t"
                + str(feat_arr[i][7])
                + "\tG-rich\n"
            )
        elif feat_arr[i][1] > feat_arr[i][2] and feat_arr[i][3] == "C-rich":
            # print "C-rich strand is major coding strand"
            f.write(
                feat_arr[i][0]
                + "\t"
                + str(feat_arr[i][1])
                + "\t"
                + str(feat_arr[i][2])
                + "\t"
                + str(feat_arr[i][4])
                + "\t"
                + str(feat_arr[i][5])
                + "\t"
                + str(feat_arr[i][6])
                + "\t"
                + str(feat_arr[i][7])
                + "\tC-rich\n"
            )
        elif feat_arr[i][1] < feat_arr[i][2] and feat_arr[i][3] == "G-rich":
            # print "C-rich strand is major coding strand"
            f.write(
                feat_arr[i][0]
                + "\t"
                + str(feat_arr[i][1])
                + "\t"
                + str(feat_arr[i][2])
                + "\t"
                + str(feat_arr[i][4])
                + "\t"
                + str(feat_arr[i][5])
                + "\t"
                + str(feat_arr[i][6])
                + "\t"
                + str(feat_arr[i][7])
                + "\tC-rich\n"
            )
        elif feat_arr[i][1] < feat_arr[i][2] and feat_arr[i][3] == "C-rich":
            # print "G-rich strand is major coding strand"
            f.write(
                feat_arr[i][0]
                + "\t"
                + str(feat_arr[i][1])
                + "\t"
                + str(feat_arr[i][2])
                + "\t"
                + str(feat_arr[i][4])
                + "\t"
                + str(feat_arr[i][5])
                + "\t"
                + str(feat_arr[i][6])
                + "\t"
                + str(feat_arr[i][7])
                + "\tG-rich\n"
            )
        else:
            print("Exception")
    f.close()


def uniq(inlist):
    uniques = []
    for item in inlist:
        if item not in uniques:
            uniques.append(item)
    return uniques


def uniq_col_list(list, col):
    un = []
    for val in range(len(list)):
        un.append(list[val][col])
    return uniq(un)


if __name__ == "__main__":
    usage = "usage: %prog dirs"
    parser = argparse.ArgumentParser(description=usage)
    parser.add_argument("gbfiles", metavar="DIRS", nargs="+", help="gb files")
    # parser.add_argument('group_dir', metavar = 'DIRS', help = 'main group directory')
    args = parser.parse_args()

    # global work_dir
    start = time.time()
    allgbfiles = list(f for arg in args.gbfiles for f in glob.glob(arg))

    print("loading sequences and features ... \n")
    # feats = get_data(allgbfiles)
    print("sequences and features successfully loaded \n")
    # coding_strand(feats)

    # compare_annotations(get_replication_origins())
    # get_replication_origins()

    #     topkl_list = get_one_species_replication_origins()
    #
    #     fh = open(output_dir+"list_stall_one_species.pkl", 'wb')
    #     pickle.dump(topkl_list, fh)
    #     fh.close()

    #
    fh = open(output_dir + "list_stall_one_species.pkl", "rb")
    refseq_results = pickle.load(fh)
    fh.close()
    #
    #     ### half right side is from CR[len(CR)/2:len-1] -> old start will become : old start + len(CR)/2 and end will stay the same
    #     ### 1/4 right side is from CR[-len(CR)/4:]    -> old start will become : old start + len(CR)/2 + len(CR)/4
    #     complete_CR_left = []
    #     for i in range(len(refseq_results)):
    #         if not refseq_results[i][2] == 'No_OH_RefSeq':
    #             CRlen = refseq_results[i][3] - refseq_results[i][2]
    #             #lefthalf_refseq_results.append((refseq_results[i][0],refseq_results[i][1],refseq_results[i][2],refseq_results[i][2]+CRlen/2,refseq_results[i][4],refseq_results[i][5],refseq_results[i][6]))
    #             #righthalf_refseq_results.append((refseq_results[i][0],refseq_results[i][1],refseq_results[i][2]+CRlen/2,refseq_results[i][3],refseq_results[i][4],refseq_results[i][5],refseq_results[i][6]))
    #             complete_CR_left.append((refseq_results[i][0],refseq_results[i][1],refseq_results[i][3],refseq_results[i][3]+CRlen,refseq_results[i][4],refseq_results[i][5],refseq_results[i][6]))
    #             #complete_CR_left.append((refseq_results[i][0],refseq_results[i][1],refseq_results[i][2]-CRlen,refseq_results[i][2],refseq_results[i][4],refseq_results[i][5],refseq_results[i][6]))
    #
    # insectivora_test = [['Insectivora', 'geneorder0', 12700, 14513, 2423, 2461, '/homes/brauerei/abdullah/Desktop/PhD/python/mtdbnew/src/Metazoa-new/Metazoa.007/abdul-results/Deuterostomia/Chordata/Craniata/Vertebrata/Euteleostomi/Sarcopterygii/Mammalia/Eutheria/Laurasiatheria/Insectivora']]
    # insectivora_test=[['Ostariophysi', 'geneorder0', 12809, 13746, 2447, 2479, '/homes/brauerei/abdullah/Desktop/PhD/python/mtdbnew/src/Metazoa-new/Metazoa.007/abdul-results/Deuterostomia/Chordata/Craniata/Vertebrata/Euteleostomi/Actinopterygii/Neopterygii/Teleostei/Ostariophysi']]
    final_result = open(
        output_dir + "complete_CR_refseq_final_stats_stall_0.05.txt", "a"
    )

    # for nb in np.arange(0, 1, 0.1):
    statistics(refseq_results, 0.05, final_result)
    final_result.close()

    # annotation_shift(get_replication_origins(allgbfiles), "nad1")

end = time.time()
print("elapsed time", end - start)
