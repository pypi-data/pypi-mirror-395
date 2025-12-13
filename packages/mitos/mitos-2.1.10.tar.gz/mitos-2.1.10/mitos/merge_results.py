"""
This script will merge the results of tRNAscan and cmsearch. If the results has conflicts, we keep the results of cmsearch.
It also saves the count of the instances where:
1- we take our annotation
2- we take the tRNAscan annotation (i.e., we found nothing)
3- both methods found nothing
"""

from Bio import SeqIO

from mitos.sequence import sequence

# !/bin/bash
dir = "/home/wi93jaj/Documents/Work/MITOS/ncRNAs_171214/"
tRNAs = [
    "trnS1",
    "trnF",
    "trnD",
    "trnY",
    "trnS2",
    "trnL1",
    "trnL2",
    "trnH",
    "trnI",
    "trnM",
    "trnN",
    "trnC",
    "trnE",
    "trnP",
    "trnQ",
    "trnR",
    "trnT",
    "trnW",
    "trnK",
    "trnA",
    "trnG",
    "trnV",
]
test = ["trnS1"]


def cut_fasta(trna, bed_dict, fasta_file):
    """
    matched annotations found with cmsearch or tRNAscan has to be cut from the fastfiles I generated and not the original whole sequence fasta file
    """

    refseq_fasta = open(
        dir + "Fungi/fasta_all_together/" + trna + ".fasta", "r"
    )  # ## open the refseq fastafile generated using getfeatures.py
    fasta_sequences = SeqIO.parse(refseq_fasta, "fasta")
    all_sequences = {}
    for fasta in fasta_sequences:
        acc = fasta.id.split("_")[0] + "_" + fasta.id.split("_")[1]
        if acc not in all_sequences:
            all_sequences[acc] = 0
        all_sequences[acc] = sequence(str(fasta.seq))

    for acc in bed_dict:
        strand = 0
        if not bed_dict[acc]:
            continue
        if bed_dict[acc]["strand"] == "+":
            strand = 1
        else:
            strand = -1
        # print ">"+ acc+"\n"+str(all_sequences[acc].subseq(int(bed_dict[acc]['start']), int(bed_dict[acc]['stop']), strand))
        fasta_file.write(
            ">"
            + acc
            + "\n"
            + str(
                all_sequences[acc].subseq(
                    int(bed_dict[acc]["start"]), int(bed_dict[acc]["stop"]), strand
                )
            )
            + "\n"
        )


def uniq(inlist):
    uniques = []
    for item in inlist:
        if item not in uniques:
            uniques.append(item)
    return uniques


def merge(trna):

    cmsearch_output = {}
    trnascan_output = {}
    refseq = {}

    log_file = open(dir + "Fungi/log/" + trna + ".txt", "w")

    merged_bed = open(dir + "Fungi/merged_results/bedfiles/" + trna + ".bed", "w")

    print(trna)
    # open fasta file with refseq annotations
    fasta_file = open(dir + "Fungi/fasta_all_together/" + trna + ".fasta", "r")
    fasta_sequences = SeqIO.parse(fasta_file, "fasta")
    for fasta in fasta_sequences:
        acc = fasta.id.split("_")[0] + "_" + fasta.id.split("_")[1]
        refseq_strand = fasta.id.split("_")[2]
        refseq_start = fasta.id.split("_")[3]
        refseq_stop = fasta.id.split("_")[4]

        if trna not in refseq:
            refseq[trna] = {}
        if acc not in refseq[trna]:
            refseq[trna][acc] = {}
        refseq[trna][acc]["start"] = refseq_start
        refseq[trna][acc]["stop"] = refseq_stop
        refseq[trna][acc]["strand"] = refseq_strand

    # open cmsearch bed file
    cmsearch_bed = open(dir + "Fungi/cmsearch/bedfiles/" + trna + ".bed", "r")
    for line in cmsearch_bed:
        line = line.strip().split("\t")
        acc = line[0]
        start = line[1]
        stop = line[2]
        score = line[4]
        strand = line[5]
        if trna not in cmsearch_output:
            cmsearch_output[trna] = {}
        if acc not in cmsearch_output[trna]:
            cmsearch_output[trna][acc] = {}
        cmsearch_output[trna][acc]["start"] = start
        cmsearch_output[trna][acc]["stop"] = stop
        cmsearch_output[trna][acc]["score"] = score
        cmsearch_output[trna][acc]["strand"] = strand

    # open tRNA scan bed file
    trnascan_bed = open(dir + "Fungi/tRNAscan/bedfiles/" + trna + ".bed", "r")
    for line in trnascan_bed:
        line = line.strip().split("\t")
        acc = line[0]
        start = line[1]
        stop = line[2]
        score = line[4]
        strand = line[5]
        if trna not in trnascan_output:
            trnascan_output[trna] = {}
        if acc not in trnascan_output[trna]:
            trnascan_output[trna][acc] = {}
        trnascan_output[trna][acc]["start"] = start
        trnascan_output[trna][acc]["stop"] = stop
        trnascan_output[trna][acc]["score"] = score
        trnascan_output[trna][acc]["strand"] = strand
    # print trnascan_output

    merged_results = {}
    for refseq_acc in refseq[trna]:
        if refseq_acc not in merged_results:
            merged_results[refseq_acc] = {}

        if refseq_acc in list(cmsearch_output[trna].keys()) and refseq_acc in list(
            trnascan_output[trna].keys()
        ):  # our model found something and tRNAscan found something
            log_file.write(refseq_acc + "\t cmsearch\n")
            #            if float(cmsearch_output[trna][refseq_acc]['score']) <= 0.001:
            merged_results[refseq_acc] = cmsearch_output[trna][refseq_acc]

        if refseq_acc in list(cmsearch_output[trna].keys()) and refseq_acc not in list(
            trnascan_output[trna].keys()
        ):  # our model found something and tRNAscan did not find anything
            log_file.write(refseq_acc + "\t cmsearch\n")
            #            if float(cmsearch_output[trna][refseq_acc]['score']) <= 0.001:
            merged_results[refseq_acc] = cmsearch_output[trna][refseq_acc]

        if refseq_acc not in list(cmsearch_output[trna].keys()) and refseq_acc in list(
            trnascan_output[trna].keys()
        ):  # our model found nothing and tRNAscan found something
            log_file.write(refseq_acc + "\t tRNAscan\n")
            merged_results[refseq_acc] = trnascan_output[trna][refseq_acc]

        if refseq_acc not in list(
            cmsearch_output[trna].keys()
        ) and refseq_acc not in list(
            trnascan_output[trna].keys()
        ):  # both methods found nothing
            log_file.write(refseq_acc + "\t nothing\n")

    log_file.close()

    for acc in merged_results:
        if merged_results[acc]:
            merged_bed.write(
                acc
                + "\t"
                + merged_results[acc]["start"]
                + "\t"
                + merged_results[acc]["stop"]
                + "\t"
                + trna
                + "\t"
                + merged_results[acc]["score"]
                + "\t"
                + merged_results[acc]["strand"]
                + "\n"
            )
        # print acc, merged_results[acc]
    merged_bed.close()

    return merged_results
    # print len(cmsearch_output[trna].keys()),"\n", len(trnascan_output[trna].keys())


for g in tRNAs:
    merged_fasta = open(dir + "Fungi/merged_results/fasta/" + g + ".fasta", "w")
    cut_fasta(g, merge(g), merged_fasta)
    merged_fasta.close()
