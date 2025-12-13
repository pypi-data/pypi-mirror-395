import argparse
import glob
import os
import os.path
import pickle
import random
import re
import sys
import time

# from tabulate import tabulate
from decimal import Decimal

import numpy
from Bio import AlignIO, SeqIO
from Bio.Data.CodonTable import register_ncbi_table
from ete2 import Tree

from mitos import mitofile
from mitos.bedfile import bedwriter
from mitos.feature import feature
from mitos.gb import gbfromfile

# hmmscan I take each frame alone (no merge_frames) #change in get_best_hits for the frame

# Rosewater
# -----------
start = time.time()

# taxidmap_file = "/homes/brauerei2/marwa/phd/gc/RefSeq/new_taxidtoacc-refseq63.txt"
# # tree_file = "/homes/brauerei2/marwa/phd/tool/mtdb/data/trees_and_data/tree_id.nw"
# tree_file ="/homes/brauerei2/marwa/phd/tool/mtdb/data/trees_and_data/Final_Metazoa.nw"
# tree_file1="/homes/brauerei2/marwa/phd/tool/mtdb/data/trees_and_data/tree.nw"
# work_dir = "/homes/brauerei2/marwa/phd/tool/mtdb/data/trees_and_data/"
# outp_dir = "/homes/brauerei2/marwa/phd/gc/RefSeq/outputdir/"
# #outp_dir = "/homes/brauerei/abdullah/Desktop/PhD/python/mtdbnew/src/RNAremold/tRNA-phylo/004/tRNA-CM/data/Higgs2003_Paper_test/remolding/"
# #main_dir = "/homes/brauerei/abdullah/Desktop/PhD/python/mtdbnew/src/RNAremold/tRNA-phylo/004/tRNA-CM/"
# fasta_files_dir = "/homes/brauerei2/marwa/phd/gc/RefSeq/refseq63-fasta"
# gene_models_dir ="/homes/brauerei2/marwa/phd/gc/RefSeq/outputdir/GM-refseq63-test/"
# # gb_files = "/homes/brauerei2/marwa/phd/gc/RefSeq/refseq63-gb/"
# gb_files = "/homes/brauerei2/marwa/phd/gc/RefSeq/refseq63-gb/"
# out_fasta ="/homes/brauerei2/marwa/phd/tool/mtdb/data/trees_and_data/fasta_files-test/"
# # out_stockholm ="/homes/brauerei2/marwa/phd/tool/mtdb/data/trees_and_data/stockholm_filesgenes/"
# out_stockholm ="/homes/brauerei2/marwa/phd/tool/mtdb/data/trees_and_data/stockholm_filesgenes-test/"
# out_models = "/homes/brauerei2/marwa/phd/tool/mtdb/data/trees_and_data/result_HMM_refseq63-test/"
# out_stockholm1="/homes/brauerei2/marwa/phd/tool/mtdb/data/trees_and_data/stockholm_filesgenes1-test/"
# internal_models_dir = "/Users/Abdullah/Documents/PhD/work/Others/mtdb/src/RNAremold/tRNA-phylo/004/tRNA-CM/data/Metazoa/result_CM_refseq56/"
# MAC


def load_sequences(gene):
    d = {}
    print(gene)
    for record in SeqIO.parse(
        "/homes/brauerei2/marwa/phd/tool/mtdb/data/trees_and_data/clean_fasta_files_leaves/"
        + gene
        + ".fas",
        "fasta",
    ):
        d[record.id] = record.seq

    return d


def load_features(acc):
    features = []
    featdir = "/homes/brauerei2/marwa/phd/gc/RefSeq/features/"
    try:
        with open(featdir + acc + ".gb", "r") as f:
            for line in f:
                features = line.split()
    except Exception:
        sys.stderr.write("")
    return features


def load_data(dirs):
    """ """
    data_gene = {}
    # extract all tRNAs from the MITOS results that have an annotated anticodon (and discard the others) + replace nonstandard bases with random bases(ACGTU)
    files = os.listdir(dirs)
    for file in files:
        acc = file.split(".")[0]
        features = load_features(acc)

        data_gene[acc] = [x for x in features]

    return data_gene


def load_phyla(dirs):
    phyla = {}
    files = os.listdir(dirs)
    for file in files:
        acc = file.split(".")[0]
        with open(gb_files + file, "r") as f:
            for line in f:
                if "Metazoa; " in line:
                    phyla[acc] = line.split("Metazoa; ")[1].split(";")[0]
                    break
    s = set()

    for val in list(phyla.values()):
        s.add(val)
    return phyla, s


def load_data_old(dirs):
    """ """
    data_gene = {}
    # extract all tRNAs from the MITOS results that have an annotated anticodon (and discard the others) + replace nonstandard bases with random bases(ACGTU)
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
        except Exception:
            sys.stderr.write("skipping (no features) %s\n" % dr)
            continue

        data_gene[gb.accession] = [x for x in features if (x.type == "gene")]

    #         for i in range(len(data_trna[ gb.accession ])):
    #             while 1:
    #                 r = random.choice(['A', 'U', 'C', 'G'])
    #                 (data_trna[ gb.accession ][i].sequence, cnt) = re.subn("[^ACGTU]", r, data_trna[ gb.accession ][i].sequence, count = 1)
    #                 if cnt == 0:
    #                     break
    #                 else:
    #                     logging.warning("replaced nonstandard base by random: %s" % r)
    #
    return data_gene


def convert_dict(dicti):
    d = {}
    for acc in dicti:
        if acc not in d:
            d[acc] = {}
        for g in range(len(dicti[acc])):
            # if dicti[acc][g].name in ["trnL1","trnL2"]:

            if dicti[acc][g].name not in d[acc]:
                d[acc][dicti[acc][g].name] = {}
                # anti_codon=str(dicti[acc][g].anticodon).replace('T','U')
            # d[acc][dicti[acc][g].name]['seq']=dicti[acc][g].sequence+anti_codon
            d[acc][dicti[acc][g].name]["seq"] = dicti[acc][g].sequence
            d[acc][dicti[acc][g].name]["structure"] = dicti[acc][g].structure
            d[acc][dicti[acc][g].name]["model"] = (
                "/homes/brauerei2/marwa/phd/gc/RefSeq/CM-refseq63/"
                + acc
                + "/"
                + dicti[acc][g].name
                + ".cm"
            )
    return d


def convert_dict_g(dicti, genes_sequences, taxidmap_file):

    d = {}
    for acc in dicti:
        if acc not in d:
            d[acc] = {}
        for g in range(len(dicti[acc])):
            # if dicti[acc][g].name in ["trnL1","trnL2"]:

            if not dicti[acc][g] in d[acc]:
                d[acc][dicti[acc][g]] = {}
                # anti_codon=str(dicti[acc][g].anticodon).replace('T','U')
            # d[acc][dicti[acc][g].name]['seq']=dicti[acc][g].sequence+anti_codon
            d[acc][dicti[acc][g]]["seq"] = get_sequence_PCgenes(
                acc, dicti[acc][g], genes_sequences
            )

            #    d[acc][dicti[acc][g].name]['structure']=dicti[acc][g].structure
            model_path = (
                gene_models_dir
                + acc
                + "/"
                + get_id(taxidmap_file, acc)
                + "_"
                + dicti[acc][g]
                + ".hm"
            )
            if os.path.isfile(model_path):
                d[acc][dicti[acc][g]]["model"] = (
                    gene_models_dir
                    + acc
                    + "/"
                    + get_id(taxidmap_file, acc)
                    + "_"
                    + dicti[acc][g]
                    + ".hm"
                )
            #                 outdir+"/GM-refseq63/"+acc+"/"+gname+"-"+get_id(taxidmap_file,acc)+ ".hm "
            else:
                d[acc][dicti[acc][g]]["model"] = None
    return d


def load_remolding_candidates(rem_cand_file):
    """
    read the remolding candidates that we found using the in-species analysis and only make the testing based on these events in the tree
    the file is as follows:
    accession    candidate_g1    candidate_g2
    """
    rem_dict = {}
    # inv_rem_dict = {}
    with open(rem_cand_file, "r") as inF:
        for line in inF:
            if line.startswith("acc"):
                continue
            line = line.split()
            #    line[0] : acc
            #    line[1] : g1
            #    line[2] : g2
            #             if not line[0] in rem_dict:
            #                 rem_dict[line[0]] = {}
            #             if not line[2] in rem_dict[line[0]]:
            #                 rem_dict[line[0]][line[2]] =line[1]

            if not get_id(taxidmap_file, line[0]) in rem_dict:
                rem_dict[get_id(taxidmap_file, line[0])] = []

            rem_dict[get_id(taxidmap_file, line[0])].append((line[1], line[2]))

    return rem_dict


def get_sequence_trna(id, gene, data):
    row = []
    accession = get_Nc(taxidmap_file, id)
    gene_seq = ""
    if accession in data:
        row = data[accession]
    else:
        sys.stderr.write("accession not found in the data table " + accession + "\n")

    for i in range(len(row)):

        if gene == row[i].name:
            gene_seq = row[i].sequence
    return gene_seq


def get_transtable(file):
    with open(file, "r") as inF:
        for line in inF:
            if "/transl_table" in line:
                return int(line.split("=")[1])
    return 1


def get_sequence_PCgenes(acc, gene, genes_sequences):
    for key, seq in list(genes_sequences.items()):
        if key == acc:
            return str(seq)


def get_sequence_PCgenes_old(accession, gene, fasta_files_dir, data):
    row = []
    # print gene,
    # accession=get_Nc(taxidmap_file, id))
    gene_seq = ""
    prot_seq = ""
    # proc = subprocess.Popen(["python /homes/brauerei2/marwa/phd/tool/mtdb/src/getinfo.py "+ gb_files + accession +".gb -f %c"], stdout=subprocess.PIPE, shell=True)
    # (out, err) = proc.communicate()
    gbfile = gb_files + accession + ".gb"
    transl_table = get_transtable(gbfile)
    if accession in data:
        row = data[accession]
        #         print row
        #         print row
        gene_start = []
        gene_end = []
        found = 0
        for i in range(len(row)):
            if gene == row[i].name:
                found = 1
                gene_start.append(row[i].start)
                gene_end.append(row[i].stop)
                #                 print row[i].score
                record = SeqIO.read(fasta_files_dir + accession + ".fas", "fasta")
                if len(gene_start) == 1:
                    if gene_start[0] > gene_end[0]:
                        gene_seq = (
                            record.seq[gene_start[0] : len(record.seq) - 1]
                            + record.seq[0 : gene_end[0]]
                        )
                    else:
                        gene_seq = record.seq[gene_start[0] : gene_end[0]]

                else:
                    lst = []
                    for i in range(0, len(gene_start) - 1):
                        # l.append(gene_end[i]-gene_start[i])
                        lst.append(row[i].score)
                    ind = lst.index(max(lst))

                    gene_seq = record.seq[gene_start[ind] : gene_end[ind]]
                #                 print gene_seq
                #                 print len(gene_start)
                prot_seq = gene_seq.translate(table=transl_table)
                if found == 0:
                    print("Gene Not found")
                    gene_seq = ""
                    prot_seq = ""
        #         prot_seq=get_protein(gene,gbfile)
        #         print gene

        #         print
        return prot_seq

    else:
        sys.stderr.write("accession not found in the data table " + accession + "\n")
        return


# def find_Nc(NC,folder):
#
#     os.chdir(folder)
#     found = False
#     for file in glob.glob("*"):
#         if file==NC:
#             found= True
#     return found


def find_id(tax_file, id):
    with open(tax_file, "r") as inF:
        for line in inF:
            line = line.split()
            if id == line[0]:
                found = True
            else:
                found = False
    return found


def get_Nc(tax_file, id):
    acc = ""
    with open(tax_file, "r") as inF:
        for line in inF:
            line = line.split()
            if id == line[0]:
                acc = line[1]
                break
    return acc


def get_id(tax_file, acc):
    id = ""
    with open(tax_file, "r") as inF:
        for line in inF:
            line = line.split()
            if acc == line[1]:
                id = line[0]
                break
    return id


def cmbuild_call(outdir, acc, gname):
    os.system(
        "/opt/bin/cmbuild -F "
        + outdir
        + "CM-refseq63/"
        + acc
        + "/"
        + gname
        + ".cm "
        + outdir
        + "/stockholm_files/"
        + acc
        + "/"
        + gname
        + ".sto"
    )


def hmmbuild_call(outdir, acc, gname):
    if not os.path.exists(outdir + "GM-refseq63"):
        os.makedirs(outdir + "GM-refseq63")
    os.system(
        "hmmbuild  "
        + outdir
        + "GM-refseq63/"
        + acc
        + "/"
        + get_id(taxidmap_file, acc)
        + "_"
        + gname
        + ".hm "
        + outdir
        + "stockholm_files/"
        + acc
        + "/"
        + get_id(taxidmap_file, acc)
        + "_"
        + gname
        + ".sto"
    )


#     print outdir+"/GM-refseq63-test/"+acc+"/"+get_id(taxidmap_file,acc)+'_'+gname+ ".hm "+ outdir+"/stockholm_files-test/"+acc+"/"+get_id(taxidmap_file,acc)+'_'+gname+".sto"
#            print "hmmbuild  "+outdir+"GM-refseq63/"+acc+"/"+gname+".hmm "+ outdir+"/stockholm_files/"+acc+"/"+gname+".sto"


def model_build_genes(
    pool, data, odirectory, gene_sequences, gene
):  # # takes the old dict before i convert it
    if not os.path.exists(odirectory):
        os.makedirs(odirectory)
    # print data
    if not os.path.exists(odirectory + "stockholm_files/"):
        os.makedirs(odirectory + "stockholm_files")

    if not os.path.exists(odirectory + "GM-refseq63"):
        os.makedirs(odirectory + "GM-refseq63")

    for acc in data:
        if not os.path.exists(odirectory + "stockholm_files/" + acc):
            os.makedirs(odirectory + "stockholm_files/" + acc)

        if not os.path.exists(odirectory + "GM-refseq63/" + acc):
            os.makedirs(odirectory + "GM-refseq63/" + acc)
        # print odirectory+acc
        fout = open(
            odirectory
            + "stockholm_files/"
            + acc
            + "/"
            + get_id(taxidmap_file, acc)
            + "_"
            + gene
            + ".sto",
            "w",
        )
        input = "# STOCKHOLM 1.0 \n"
        input += acc + "\t" + str(get_sequence_PCgenes(acc, gene, gene_sequences))
        input += "\n//"
        # print "test"
        # print str(input)
        # print input
        fout.write(input)
        fout.close()
        # hmmbuild_call(odirectory, acc, data[acc][i])
        pool.apply_async(hmmbuild_call, args=(odirectory, acc, gene))
        # os.system("/opt/bin/cmbuild -F "+odirectory+"/CM-refseq63/"+acc+"/"+data[acc][i].name+".cm "+ odirectory+"/stockholm_files/"+acc+"/"+data[acc][i].name+".sto")
        # print "cmbuild "+odirectory+"CM/"+acc+"/"+data[acc][i].name+".cm "+ odirectory+"stockholm-files/"+acc+"/"+data[acc][i].name+".sto"


# def model_build_PCgenes(data_genes, odirectory):
#     global taxidmap_file
#     global fasta_files_dir
#     if not os.path.exists(odirectory):
#         os.makedirs(odirectory)
#
#     if not os.path.exists(odirectory+"/stockholm-files/PCgenes"):
#
#         os.makedirs(odirectory+"/stockholm-files/PCgenes")
#
#     if not os.path.exists(odirectory+"/Hmm-refseq56/PCgenes"):
#         os.makedirs(odirectory+"/Hmm-refseq56/PCgenes")
#
#     for acc in data_genes:
#         if not os.path.exists(odirectory+"/stockholm-files/PCgenes/"+acc):
#             os.makedirs(odirectory+"/stockholm-files/PCgenes/"+acc)
#         if not os.path.exists(odirectory+"/Hmm-refseq56/PCgenes/"+acc):
#             os.makedirs(odirectory+"/Hmm-refseq56/PCgenes/"+acc)
#         id = get_taxid(taxidmap_file,acc)
#
#         for i in range(len(data_genes[acc])):
#                 #print data_genes[acc][i].name
#                 if get_sequence_PCgenes(id,data_genes[acc][i].name,fasta_files_dir,data_genes) is not None:
#                     fout = open(odirectory + "/stockholm-files/PCgenes/" + acc + "/" + data_genes[acc][i].name + ".sto", "w")
#                     input = "# STOCKHOLM 1.0 \n"
#                     input += acc + "_" + data_genes[acc][i].name + "\t" + get_sequence_PCgenes(id,data_genes[acc][i].name,fasta_files_dir,data_genes)
#                     input += "\n//"
#                     fout.write(str(input))
#                     fout.close()
#                     os.system("hmmbuild " + odirectory + "/Hmm-refseq56/PCgenes/" + acc + "/" + data_genes[acc][i].name + ".cm " + odirectory + "/stockholm-files/PCgenes/" + acc + "/" + data_genes[acc][i].name + ".sto")
#                 else:
#                     sys.stderr.write("skipping (no gene "+data_genes[acc][i].name+") in "+acc)
#             #print "cmbuild "+odirectory+"CM/"+acc+"/"+data[acc][i].name+".cm "+ odirectory+"stockholm-files/"+acc+"/"+data[acc][i].name+".sto"


def model_choice(sth1, sth2):
    """
    param[in] : two stockholm alignments (score files) which the output model will be built from.
    i count the number of sequences inside each alignment, and we build the model from the sequence with the larger number of sequenes.
    if the number of sequences is the same, we choose a random one.
    """

    f1 = open(sth1, "r")
    f2 = open(sth2, "r")
    i = 0
    j = 0
    for l1 in f1:
        if not l1.startswith("#"):
            i += 1
    f1.close()

    for l2 in f2:
        if not l2.startswith("#"):
            j += 1
    f2.close()

    if i > j:
        return sth1
    elif j > i:
        return sth2
    else:
        return random.choice([sth1, sth2])


def if_remolded(score_file):
    """
    it reads the score file generated from the alignment of 2 tRNA from 2 sister nodes and output the score for the infernal alignment of this model with the gene sequence(s)
    the idea is to look at the sister species and check the score, if S(X),m_Y' > S(X),m_X' => X is remolded from Y' | X' and Y' are the same tRNAs from the sister species

    for now, it just returns the score
    """

    sfile = open(score_file, "r")
    i = 0
    score = 0
    for line in sfile:
        if not line.startswith("#"):
            i += 1
            temp = line.split()
            aligned_gene = temp[1]
            score += float(temp[6])

    sfile.close()
    return aligned_gene, score / i


def alignment_score_internals(score_file):
    """
    it reads the score file generated from the alignment of 2 tRNA from 2 sister nodes and output the score for the infernal alignment of this model with the gene sequence(s)
    the idea is to look at the sister species and check the score, if S(X),m_Y' > S(X),m_X' => X is remolded from Y' | X' and Y' are the same tRNAs from the sister species
    """
    print(score_file)
    sfile = open(score_file, "r")
    score = 0
    i = 0
    for line in sfile:
        if not line.startswith("#"):
            i += 1
            temp = line.split()

            score += float(temp[6])

    sfile.close()
    return score / i


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


# def align(nd):
#     '''
#     should be only for non-leafs
#     '''
#
#     for chld in nd.get_children():


def get_bestmodel(score1, score2, mod1, mod2, ch1, ch2):
    if score1 > score2:
        return mod1, ch1
    else:
        return mod2, ch2


def get_score(stofile, v):
    # hmmer3
    file = open(stofile, "r")
    total = 0
    count = 0
    if v == 3:
        for line in file:
            if not line.startswith("#"):
                count += 1
                total += float(line.split()[5])
        if count == 0:
            count = 1
        file.close()
        # hmmer2
    elif v == 2:

        first = False
        second = False
        found = False
        temp = -1
        count = 0
        total = 0
        with open(stofile, "r") as f:
            for line in f:
                if not second and line.startswith("Sequence"):
                    if not first:
                        first = True
                    else:
                        second = True
                        temp = 2
                if temp > 0:
                    temp = temp - 1
                elif temp == 0:
                    found = True

                if found:
                    if not line or line.rstrip() == "":
                        if count == 0:
                            count = 1
                        break
                    else:
                        count = count + 1
                        total = total + float(line.split()[1])

    return total, count


def computeModelsh2(nd, gene):
    if nd.is_leaf() and gene in list(nd.arr.keys()):
        # print nd.name
        mod = nd.arr[gene]["model"]
        return mod

    if not nd.is_leaf():
        mod1 = computeModels(nd.get_children()[0], gene)
        if len(nd.get_children()) == 2:
            mod2 = computeModels(nd.get_children()[1], gene)
        else:
            mod2 = None
        # print mod1,mod2 ,"lllllllllllllllll"
        if mod1 is not None and mod2 is not None:

            # both children have models for this gene
            cmd1 = (
                "/opt/bin/hmmsearch  "
                + mod1
                + " "
                + out_fasta
                + nd.name
                + "_"
                + gene
                + ".fas  >"
                + out_stockholm
                + nd.name
                + "_"
                + gene
                + "_hm_"
                + nd.get_children()[0].name
                + ".sto"
            )
            cmd2 = (
                "/opt/bin/hmmsearch   "
                + mod2
                + " "
                + out_fasta
                + nd.name
                + "_"
                + gene
                + ".fas  >"
                + out_stockholm
                + nd.name
                + "_"
                + gene
                + "_hm_"
                + nd.get_children()[1].name
                + ".sto"
            )

            os.system(cmd1)
            os.system(cmd2)

            file1 = (
                out_stockholm
                + nd.name
                + "_"
                + gene
                + "_hm_"
                + nd.get_children()[0].name
                + ".sto"
            )
            score1, i = get_score(str(file1), 2)
            file2 = (
                out_stockholm
                + nd.name
                + "_"
                + gene
                + "_hm_"
                + nd.get_children()[1].name
                + ".sto"
            )
            score2, j = get_score(str(file2), 2)
            model, child = get_bestmodel(
                score1 / i,
                score2 / j,
                mod1,
                mod2,
                nd.get_children()[0].name,
                nd.get_children()[1].name,
            )
            print(child, model)
            if child == nd.get_children()[0].name:
                if (
                    not nd.get_children()[0].get_children()
                    or not os.path.exists(
                        out_fasta + nd.get_children()[1].name + "_" + gene + ".fas   "
                    )
                    or os.stat(
                        out_fasta + nd.get_children()[1].name + "_" + gene + ".fas   "
                    ).st_size
                    == 0
                    or not len(nd.get_children()) == 2
                ):  # first child does not have childrens // directly above leafs // no use for --mapali

                    print(
                        "aligning at "
                        + nd.name
                        + " based on "
                        + nd.get_children()[0].name
                        + " without mapali "
                    )
                    cmd = (
                        "/opt/bin/hmmalign -o "
                        + out_stockholm1
                        + gene
                        + "/"
                        + nd.name
                        + "_"
                        + gene
                        + "_hm_"
                        + child
                        + ".sto "
                        + model
                        + " "
                        + out_fasta
                        + nd.name
                        + "_"
                        + gene
                        + ".fas  "
                    )
                    os.system(cmd)
                    # alignment = out_stockholm1 + gene + '/' + nd.name + '_' + gene + '_hm_' + child + '.sto '
                    print("case 1 : ", cmd)
                else:  # has grand children >> use mapali
                    cmd = (
                        "/opt/bin/hmmalign --mapali "
                        + findSTH(child)
                        + " -o "
                        + out_stockholm1
                        + gene
                        + "/"
                        + nd.name
                        + "_"
                        + gene
                        + "_hm_"
                        + child
                        + ".sto "
                        + model
                        + " "
                        + out_fasta
                        + nd.get_children()[1].name
                        + "_"
                        + gene
                        + ".fas   "
                    )
                    os.system(cmd)
                    print("case 1.1")

            elif child == nd.get_children()[1].name:
                if (
                    not nd.get_children()[1].get_children()
                    or not os.path.exists(
                        out_fasta + nd.get_children()[0].name + "_" + gene + ".fas  "
                    )
                    or os.stat(
                        out_fasta + nd.get_children()[0].name + "_" + gene + ".fas   "
                    ).st_size
                    == 0
                    or not len(nd.get_children()) == 2
                ):
                    cmd = (
                        "/opt/bin/hmmalign  -o "
                        + out_stockholm1
                        + gene
                        + "/"
                        + nd.name
                        + "_"
                        + gene
                        + "_hm_"
                        + nd.get_children()[1].name
                        + ".sto "
                        + model
                        + " "
                        + out_fasta
                        + nd.name
                        + "_"
                        + gene
                        + ".fas   "
                    )
                    os.system(cmd)
                    print(
                        "case 2 :/opt/bi/hmmalign "
                        + model
                        + " "
                        + out_fasta
                        + nd.name
                        + "_"
                        + gene
                        + ".fas > "
                        + out_stockholm1
                        + gene
                        + "/"
                        + nd.name
                        + "_"
                        + gene
                        + "_hm_"
                        + nd.get_children()[1].name
                        + ".sto "
                    )
                else:  # has grand children >> use mapali
                    cmd = (
                        "/opt/bin/hmmalign --mapali  "
                        + findSTH(nd.get_children()[1].name)
                        + " -o "
                        + out_stockholm1
                        + gene
                        + "/"
                        + nd.name
                        + "_"
                        + gene
                        + "_hm_"
                        + nd.get_children()[1].name
                        + ".sto "
                        + model
                        + " "
                        + out_fasta
                        + nd.get_children()[0].name
                        + "_"
                        + gene
                        + ".fas "
                    )
                    os.system(cmd)
                    print("case 3 : ", cmd)

            if child == nd.get_children()[0].name:
                os.system(
                    '/opt/bin/hmmbuild   "'
                    + work_dir
                    + "result_HMM_refseq63/"
                    + gene
                    + "/"
                    + nd.name
                    + "_"
                    + gene
                    + '.hm" "'
                    + out_stockholm1
                    + gene
                    + "/"
                    + nd.name
                    + "_"
                    + gene
                    + "_hm_"
                    + nd.get_children()[0].name
                    + '.sto" '
                )
                # cmd='/opt/bin/hmmcalibrate   '+work_dir+'result_HMM_refseq63/'+gene+'/' + nd.name + '_' + gene + '.hm '
                # print cmd
                # os.system(cmd)
                with open("ndal.tmp", "a") as file:
                    file.write(
                        nd.name
                        + " "
                        + out_stockholm1
                        + gene
                        + "/"
                        + nd.name
                        + "_"
                        + gene
                        + "_hm_"
                        + nd.get_children()[0].name
                        + ".sto\n"
                    )
            else:
                os.system(
                    '/opt/bin/hmmbuild   "'
                    + work_dir
                    + "result_HMM_refseq63/"
                    + gene
                    + "/"
                    + nd.name
                    + "_"
                    + gene
                    + '.hm" "'
                    + out_stockholm1
                    + gene
                    + "/"
                    + nd.name
                    + "_"
                    + gene
                    + "_hm_"
                    + nd.get_children()[1].name
                    + '.sto" '
                )
                # cmd='/opt/bin/hmmcalibrate  '+work_dir+'result_HMM_refseq63/'+gene+'/' + nd.name + '_' + gene + '.hm '
                # print cmd
                # os.system(cmd)
                with open("ndal.tmp", "a") as file:
                    file.write(
                        nd.name
                        + " "
                        + out_stockholm1
                        + gene
                        + "/"
                        + nd.name
                        + "_"
                        + gene
                        + "_hm_"
                        + nd.get_children()[1].name
                        + ".sto\n"
                    )

            if os.path.isfile(
                work_dir
                + "result_HMM_refseq63/"
                + gene
                + "/"
                + nd.name
                + "_"
                + gene
                + ".hm"
            ):
                nd.arr[gene]["model"] = (
                    work_dir
                    + "result_HMM_refseq63/"
                    + gene
                    + "/"
                    + nd.name
                    + "_"
                    + gene
                    + ".hm"
                )
                return nd.arr[gene]["model"]

        elif (
            mod1 is not None and mod2 is None
        ):  # only child1 have model for this gene, align only based on child1
            if (
                not nd.get_children()[0].get_children()
                or not os.path.exists(
                    out_fasta + nd.get_children()[1].name + "_" + gene + ".fas   "
                )
                or os.stat(
                    out_fasta + nd.get_children()[1].name + "_" + gene + ".fas   "
                ).st_size
                == 0
                or not len(nd.get_children()) == 2
            ):
                cmd = (
                    "/opt/bin/hmmalign  -o "
                    + out_stockholm1
                    + gene
                    + "/"
                    + nd.name
                    + "_"
                    + gene
                    + "_hm_"
                    + nd.get_children()[0].name
                    + ".sto "
                    + mod1
                    + " "
                    + out_fasta
                    + nd.name
                    + "_"
                    + gene
                    + ".fas    "
                )
                os.system(cmd)
                print("case 4:", cmd)

            else:  # has grand children >> use mapali
                cmd = (
                    "/opt/bin/hmmalign --mapali "
                    + findSTH(nd.get_children()[0].name)
                    + " -o "
                    + out_stockholm1
                    + gene
                    + "/"
                    + nd.name
                    + "_"
                    + gene
                    + "_hm_"
                    + nd.get_children()[0].name
                    + ".sto "
                    + mod1
                    + " "
                    + out_fasta
                    + nd.get_children()[1].name
                    + "_"
                    + gene
                    + ".fas   "
                )
                os.system(cmd)

            os.system(
                '/opt/bin/hmmbuild   "'
                + work_dir
                + "result_HMM_refseq63/"
                + gene
                + "/"
                + nd.name
                + "_"
                + gene
                + '.hm" "'
                + out_stockholm1
                + gene
                + "/"
                + nd.name
                + "_"
                + gene
                + "_hm_"
                + nd.get_children()[0].name
                + '.sto" '
            )
            #             cmd = '/opt/bin/hmmcalibrate  '+work_dir+'result_HMM_refseq63/'+gene+'/' + nd.name + '_' + gene + '.hm '
            #             print cmd
            #             os.system(cmd)

            with open("ndal.tmp", "a") as file:
                file.write(
                    nd.name
                    + " "
                    + out_stockholm1
                    + gene
                    + "/"
                    + nd.name
                    + "_"
                    + gene
                    + "_hm_"
                    + nd.get_children()[0].name
                    + ".sto\n"
                )
                # file.write(nd.name +' '+ mod1+'\n')

            if os.path.isfile(
                work_dir
                + "result_HMM_refseq63/"
                + gene
                + "/"
                + nd.name
                + "_"
                + gene
                + ".hm"
            ):
                nd.arr[gene]["model"] = (
                    work_dir
                    + "result_HMM_refseq63/"
                    + gene
                    + "/"
                    + nd.name
                    + "_"
                    + gene
                    + ".hm"
                )

            return nd.arr[gene]["model"]

        elif (
            mod1 is None and mod2 is not None
        ):  # only child2 have model for this gene, align only based on child2

            if (
                not nd.get_children()[1].get_children()
                or not os.path.exists(
                    out_fasta + nd.get_children()[0].name + "_" + gene + ".fas   "
                )
                or os.stat(
                    out_fasta + nd.get_children()[0].name + "_" + gene + ".fas   "
                ).st_size
                == 0
                or not len(nd.get_children()) == 2
            ):  # second child does not have childrens // directly above leafs // no use for --mapali
                cmd = (
                    "/opt/bin/hmmalign  -o "
                    + out_stockholm1
                    + gene
                    + "/"
                    + nd.name
                    + "_"
                    + gene
                    + "_hm_"
                    + nd.get_children()[1].name
                    + ".sto "
                    + mod2
                    + " "
                    + out_fasta
                    + nd.name
                    + "_"
                    + gene
                    + ".fas   "
                )
                os.system(cmd)
                print("case 5 : ", cmd)
            else:  # has grand children >> use mapali
                cmd = (
                    "/opt/bin/hmmalign --mapali  "
                    + findSTH(nd.get_children()[1].name)
                    + " -o "
                    + out_stockholm1
                    + gene
                    + "/"
                    + nd.name
                    + "_"
                    + gene
                    + "_hm_"
                    + nd.get_children()[0].name
                    + ".sto "
                    + mod2
                    + " "
                    + out_fasta
                    + nd.get_children()[0].name
                    + "_"
                    + gene
                    + ".fas  "
                )
                os.system(cmd)
                print("case 6: ", cmd)
            os.system(
                '/opt/bin/hmmbuild   "'
                + work_dir
                + "result_HMM_refseq63/"
                + gene
                + "/"
                + nd.name
                + "_"
                + gene
                + '.hm" "'
                + out_stockholm1
                + gene
                + "/"
                + nd.name
                + "_"
                + gene
                + "_hm_"
                + nd.get_children()[1].name
                + '.sto" '
            )
            #             cmd='/opt/bin/calibrate   '+work_dir+'result_HMM_refseq63/'+gene+'/' + nd.name + '_' + gene + '.hm  '
            #             print cmd
            #             os.system(cmd)
            with open("ndal.tmp", "a") as file:
                file.write(
                    nd.name
                    + " "
                    + out_stockholm1
                    + gene
                    + "/"
                    + nd.name
                    + "_"
                    + gene
                    + "_hm_"
                    + nd.get_children()[1].name
                    + ".sto\n"
                )
            if os.path.isfile(
                work_dir
                + "result_HMM_refseq63/"
                + gene
                + "/"
                + nd.name
                + "_"
                + gene
                + ".hm"
            ):
                nd.arr[gene]["model"] = (
                    work_dir
                    + "result_HMM_refseq63/"
                    + gene
                    + "/"
                    + nd.name
                    + "_"
                    + gene
                    + ".hm"
                )

            return nd.arr[gene]["model"]

        else:  # both children have no model for this gene
            print("Oh shit!")
            return None


def do_alignments(nd, rarr, sis):
    """
    For each child of nd (if its a leaf and is a remolding candidate) we have rows inside the rem_dict dict.
    e.g:
        chld_g1 chld_g2
        sis_g1 sis_g2

    for each of them, i should perform the 4 following alignments:
        B with mB_sis, B with mA_sis, A with mB_sis and A with mA_sis
    """
    trna_log = open(work_dir + "result_log_file.txt", "a")

    chld = nd
    # sis = nd.get_sisters()[0]
    scrs = {}

    chld_g1 = rarr[0]
    chld_g2 = rarr[1]
    # sis_g1 = arr2[0]
    # sis_g2 = arr2[1]

    if not os.path.isfile(
        work_dir + "remolding/fasta_files/" + chld.name + "_" + chld_g1 + ".fas"
    ):

        f = open(
            work_dir + "remolding/fasta_files/" + chld.name + "_" + chld_g1 + ".fas",
            "w",
        )
        f.write(chld.arr[chld_g1]["seq"] + "\n")
        f.close()

    # ## chld_g1 with model of chld_g1 of the sister

    if chld_g1 in sis.arr:
        scr = 0  # ## test if the sister have g1, if yes align g1 with g1 of the sister (e.g B with mB_sis)
        os.system(
            '/opt/bin/cmalign "'
            + sis.arr[chld_g1]["model"]
            + '" "'
            + work_dir
            + "remolding/fasta_files/"
            + chld.name
            + "_"
            + chld_g1
            + '.fas" > '
            + work_dir
            + "remolding/stockholm_files/"
            + chld.name
            + "_"
            + chld_g1
            + "_cm_"
            + sis.name
            + "_"
            + chld_g1
            + ".sto "
        )
        os.system(
            "/opt/bin/cmalign --sfile "
            + work_dir
            + "remolding/score_files/"
            + chld.name
            + "_"
            + chld_g1
            + "_cm_"
            + sis.name
            + "_"
            + chld_g1
            + '.sto "'
            + sis.arr[chld_g1]["model"]
            + '" "'
            + work_dir
            + "remolding/fasta_files/"
            + chld.name
            + "_"
            + chld_g1
            + '.fas" '
        )

        node_gene, scr = if_remolded(
            work_dir
            + "remolding/score_files/"
            + chld.name
            + "_"
            + chld_g1
            + "_cm_"
            + sis.name
            + "_"
            + chld_g1
            + ".sto"
        )

        if chld.name + "_" + chld_g1 not in scrs:
            scrs[chld.name + "_" + chld_g1] = {}
        if sis.name + "_" + chld_g1 not in scrs[chld.name + "_" + chld_g1]:
            scrs[chld.name + "_" + chld_g1][sis.name + "_" + chld_g1] = scr
    else:
        trna_log.write(get_Nc(taxidmap_file, sis.name) + " " + chld_g1 + "\n")
        print(
            "Sister node "
            + get_Nc(taxidmap_file, sis.name)
            + " is missing tRNA "
            + chld_g1
        )

    # ## chld_g1 with model of chld_g2 of the sister
    if chld_g2 in sis.arr:
        scr = 0
        os.system(
            '/opt/bin/cmalign "'
            + sis.arr[chld_g2]["model"]
            + '" "'
            + work_dir
            + "remolding/fasta_files/"
            + chld.name
            + "_"
            + chld_g1
            + '.fas" > '
            + work_dir
            + "remolding/stockholm_files/"
            + chld.name
            + "_"
            + chld_g1
            + "_cm_"
            + sis.name
            + "_"
            + chld_g2
            + ".sto "
        )
        os.system(
            "/opt/bin/cmalign --sfile "
            + work_dir
            + "remolding/score_files/"
            + chld.name
            + "_"
            + chld_g1
            + "_cm_"
            + sis.name
            + "_"
            + chld_g2
            + '.sto "'
            + sis.arr[chld_g2]["model"]
            + '" "'
            + work_dir
            + "remolding/fasta_files/"
            + chld.name
            + "_"
            + chld_g1
            + '.fas" '
        )

        node_gene, scr = if_remolded(
            work_dir
            + "remolding/score_files/"
            + chld.name
            + "_"
            + chld_g1
            + "_cm_"
            + sis.name
            + "_"
            + chld_g2
            + ".sto"
        )
        if chld.name + "_" + chld_g1 not in scrs:
            scrs[chld.name + "_" + chld_g1] = {}
        if sis.name + "_" + chld_g2 not in scrs[chld.name + "_" + chld_g1]:
            scrs[chld.name + "_" + chld_g1][sis.name + "_" + chld_g2] = scr
    else:
        trna_log.write(get_Nc(taxidmap_file, sis.name) + " " + chld_g2 + "\n")
        print(
            (
                "Sister node "
                + get_Nc(taxidmap_file, sis.name)
                + " is missing tRNA "
                + chld_g2
            )
        )

    # #### same procedure, but with the switched remolding candidates. IMPORTANT ################################ IMPORTANT

    if not os.path.isfile(
        work_dir + "remolding/fasta_files/" + chld.name + "_" + chld_g2 + ".fas"
    ):

        f = open(
            work_dir + "remolding/fasta_files/" + chld.name + "_" + chld_g2 + ".fas",
            "w",
        )
        f.write(chld.arr[chld_g2]["seq"] + "\n")
        f.close()

    # ## chld_g2 with model of chld_g2 of the sister

    if chld_g2 in sis.arr:
        scr = 0  # ## test if the sister have g2
        os.system(
            '/opt/bin/cmalign "'
            + sis.arr[chld_g2]["model"]
            + '" "'
            + work_dir
            + "remolding/fasta_files/"
            + chld.name
            + "_"
            + chld_g2
            + '.fas" > '
            + work_dir
            + "remolding/stockholm_files/"
            + chld.name
            + "_"
            + chld_g2
            + "_cm_"
            + sis.name
            + "_"
            + chld_g2
            + ".sto "
        )
        os.system(
            "/opt/bin/cmalign --sfile "
            + work_dir
            + "remolding/score_files/"
            + chld.name
            + "_"
            + chld_g2
            + "_cm_"
            + sis.name
            + "_"
            + chld_g2
            + '.sto "'
            + sis.arr[chld_g2]["model"]
            + '" "'
            + work_dir
            + "remolding/fasta_files/"
            + chld.name
            + "_"
            + chld_g2
            + '.fas" '
        )

        node_gene, scr = if_remolded(
            work_dir
            + "remolding/score_files/"
            + chld.name
            + "_"
            + chld_g2
            + "_cm_"
            + sis.name
            + "_"
            + chld_g2
            + ".sto"
        )  # # scr of g1 with g1 of the sister

        if chld.name + "_" + chld_g2 not in scrs:
            scrs[chld.name + "_" + chld_g2] = {}
        if sis.name + "_" + chld_g2 not in scrs[chld.name + "_" + chld_g2]:
            scrs[chld.name + "_" + chld_g2][sis.name + "_" + chld_g2] = scr
    else:
        trna_log.write(get_Nc(taxidmap_file, sis.name) + " " + chld_g2 + "\n")
        print(
            (
                "Sister node "
                + get_Nc(taxidmap_file, sis.name)
                + " is missing tRNA "
                + chld_g2
            )
        )

    # ## chld_g2 with model of chld_g1 of the sister

    if chld_g1 in sis.arr:
        scr = 0
        os.system(
            '/opt/bin/cmalign "'
            + sis.arr[chld_g1]["model"]
            + '" "'
            + work_dir
            + "remolding/fasta_files/"
            + chld.name
            + "_"
            + chld_g2
            + '.fas" > '
            + work_dir
            + "remolding/stockholm_files/"
            + chld.name
            + "_"
            + chld_g2
            + "_cm_"
            + sis.name
            + "_"
            + chld_g1
            + ".sto "
        )
        os.system(
            "/opt/bin/cmalign --sfile "
            + work_dir
            + "remolding/score_files/"
            + chld.name
            + "_"
            + chld_g2
            + "_cm_"
            + sis.name
            + "_"
            + chld_g1
            + '.sto "'
            + sis.arr[chld_g1]["model"]
            + '" "'
            + work_dir
            + "remolding/fasta_files/"
            + chld.name
            + "_"
            + chld_g2
            + '.fas" '
        )

        node_gene, scr = if_remolded(
            work_dir
            + "remolding/score_files/"
            + chld.name
            + "_"
            + chld_g2
            + "_cm_"
            + sis.name
            + "_"
            + chld_g1
            + ".sto"
        )  # # scr of g1 with remdict[g1] (i.e candidate of remolding) from the sister
        if chld.name + "_" + chld_g2 not in scrs:
            scrs[chld.name + "_" + chld_g2] = {}
        if sis.name + "_" + chld_g1 not in scrs[chld.name + "_" + chld_g2]:
            scrs[chld.name + "_" + chld_g2][sis.name + "_" + chld_g1] = scr
    else:
        trna_log.write(get_Nc(taxidmap_file, sis.name) + " " + chld_g1 + "\n")
        print(
            "Sister node "
            + get_Nc(taxidmap_file, sis.name)
            + " is missing tRNA "
            + chld_g1
        )

    trna_log.write(str(scrs) + "\n")
    # print scrs
    return scrs


def up_sis(g1, g2, node, rem_dict):
    list = []
    while node:
        if not node.is_root():
            node = node.up
            if (
                not (g1, g2) in rem_dict[node.name]
                and not (g2, g1) in rem_dict[node.name]
            ):
                list.append(node.get_sisters()[0])
    return list


def remolding_in_tree(t, rem_dict):
    global taxidmap_file

    # print rem_dict

    remolding_output = open(work_dir + "all_remoldings.txt", "w")
    for nd in t.traverse("postorder"):
        # scrs = {}
        # if nd.is_root():
        #     continue

        if not nd.is_leaf():
            # scrs = {}
            chld = nd.get_children()[0]
            sis = nd.get_children()[1]

            res = {}
            #             print get_Nc(taxidmap_file, chld.name), get_Nc(taxidmap_file, sis.name)
            if (
                chld.name not in rem_dict and sis.name not in rem_dict
            ):  # ## both don't have remolding events

                continue

            elif (
                chld.name in rem_dict and sis.name in rem_dict
            ):  # ## both have remolding events
                remolding_direction = []
                direction_not_detected = []
                same_rem = []

                same_rem = list(
                    set(rem_dict[chld.name]) & set(rem_dict[sis.name])
                )  # # test if they have the same remolding candidates using list intersctions (no intersection -> no same remolding candidates)

                for el in rem_dict[
                    chld.name
                ]:  # test if the remolding candidates are the same but are swtiched
                    for ll in rem_dict[sis.name]:
                        if el == tuple(reversed(ll)):
                            if el not in same_rem and reversed(el) not in same_rem:
                                same_rem.append(el)
                #
                #                 if same_rem:
                #                     nd.add_feature('same',same_rem)

                res = {}

                for arr1 in rem_dict[
                    chld.name
                ]:  # array containing the 2 candidate genes from chld
                    if arr1 not in same_rem:
                        if chld not in res:
                            res[chld] = []
                        res[chld].append(
                            do_alignments(chld, arr1, chld.get_sisters()[0])
                        )

                for arr2 in rem_dict[
                    sis.name
                ]:  # array containing the 2 candidate genes from sis
                    if arr2 not in same_rem:
                        if sis not in res:
                            res[sis] = []
                        res[sis].append(do_alignments(sis, arr2, sis.get_sisters()[0]))

                # unique_unknown_direction = []
                # # loop through the result array, and get the remolding direction
                for kid in res:  # loop over all kids of nd
                    for d in res[kid]:  # loop over all dicts of kid
                        for k in d:
                            if (
                                len(list(d[k].keys())) > 1
                            ):  # # this is the sister tRNA is missing.
                                if (
                                    not k.split("_")[1]
                                    == max(d[k], key=lambda x: d[k][x]).split("_")[1]
                                ):

                                    # remolding_output.write(max(d[k], key=lambda x: d[k][x]).split("_")[1]+" "+k.split("_")[1]+" "+ get_Nc(taxidmap_file, k.split("_")[0])+"\n")
                                    remolding_output.write(
                                        max(d[k], key=lambda x: d[k][x]).split("_")[1]
                                        + " "
                                        + k.split("_")[1]
                                        + " "
                                        + k.split("_")[0]
                                        + "\n"
                                    )

                                    # trnN is remolded from  trnK  in accession NC_007438
                                    # Assuming N is remolded from K, this means that the sequence of N needs to be appended with K in the ancestor. The append can be done at the chld level.

                                    # node, remolded gene, donor gene
                                    remolding_direction.append(
                                        (
                                            kid,
                                            k.split("_")[1],
                                            max(d[k], key=lambda x: d[k][x]).split("_")[
                                                1
                                            ],
                                        )
                                    )
                                else:
                                    needed_genes = tuple(
                                        [i.split("_")[1] for i in list(d[k].keys())]
                                    )
                                    if (
                                        kid,
                                        needed_genes[0],
                                        needed_genes[1],
                                    ) not in direction_not_detected:
                                        direction_not_detected.append(
                                            (kid, needed_genes[0], needed_genes[1])
                                        )

                if (
                    remolding_direction
                ):  # # the case where we couldnt detect the direction of the remolding | ASK Matthias what should we do when we can't detect it.

                    for i in range(len(remolding_direction)):

                        node = remolding_direction[i][0]
                        remolded_gene = remolding_direction[i][1]
                        donor_gene = remolding_direction[i][2]

                        node.arr[donor_gene]["seq"] += node.arr[remolded_gene]["seq"]
                        node.arr[donor_gene]["structure"] += node.arr[remolded_gene][
                            "structure"
                        ]

                        node.arr[remolded_gene]["seq"] = ""
                        node.arr[remolded_gene]["structure"] = ""

                        nd.arr[donor_gene]["seq"] = aff_seq(
                            chld, sis, donor_gene, donor_gene
                        )
                        nd.arr[remolded_gene]["seq"] = aff_seq(
                            chld, sis, remolded_gene, remolded_gene
                        )

                        nd.arr[donor_gene]["model"] = computeModels(nd, donor_gene)
                        nd.arr[remolded_gene]["model"] = computeModels(
                            nd, remolded_gene
                        )

                #                         if not nd.name in rem_dict:
                #                             rem_dict[nd.name] =[]
                #
                #                         rem_dict[nd.name].append((remolded_gene,donor_gene))
                # test = {}
                if direction_not_detected:
                    for i in range(len(direction_not_detected)):
                        # nod = direction_not_detected[i][0]
                        g1 = direction_not_detected[i][1]
                        g2 = direction_not_detected[i][2]

                        # up_sis_nd = up_sis(nod)

            if (
                chld.name in rem_dict and sis.name not in rem_dict
            ):  # ## only chld have remolding candidate
                res = []
                remolding_direction = []
                direction_not_detected = []
                for arr1 in rem_dict[chld.name]:
                    res.append(do_alignments(chld, arr1, chld.get_sisters()[0]))

                for d in res:
                    for k in d:
                        if (
                            len(list(d[k].keys())) > 1
                        ):  # # this is the sister tRNA is missing.
                            if (
                                not k.split("_")[1]
                                == max(d[k], key=lambda x: d[k][x]).split("_")[1]
                            ):
                                # remolding_output.write(max(d[k], key=lambda x: d[k][x]).split("_")[1]+" "+k.split("_")[1]+" " + get_Nc(taxidmap_file, k.split("_")[0])+"\n")
                                remolding_output.write(
                                    max(d[k], key=lambda x: d[k][x]).split("_")[1]
                                    + " "
                                    + k.split("_")[1]
                                    + " "
                                    + k.split("_")[0]
                                    + "\n"
                                )

                                remolding_direction.append(
                                    (
                                        chld,
                                        k.split("_")[1],
                                        max(d[k], key=lambda x: d[k][x]).split("_")[1],
                                    )
                                )
                            else:
                                needed_genes = tuple(
                                    [i.split("_")[1] for i in list(d[k].keys())]
                                )
                                if (
                                    not (chld, needed_genes[0], needed_genes[1])
                                    in direction_not_detected
                                ):
                                    direction_not_detected.append(
                                        (chld, needed_genes[0], needed_genes[1])
                                    )

                # rem_internals = []
                if (
                    remolding_direction
                ):  # # the case where we couldnt detect the direction of the remolding | ASK Matthias what should we do when we can't detect it.

                    for i in range(len(remolding_direction)):

                        node = remolding_direction[i][0]
                        remolded_gene = remolding_direction[i][1]
                        donor_gene = remolding_direction[i][2]

                        node.arr[donor_gene]["seq"] += node.arr[remolded_gene]["seq"]
                        node.arr[donor_gene]["structure"] += node.arr[remolded_gene][
                            "structure"
                        ]

                        node.arr[remolded_gene]["seq"] = ""
                        node.arr[remolded_gene]["structure"] = ""

                        nd.arr[donor_gene]["seq"] = aff_seq(
                            chld, sis, donor_gene, donor_gene
                        )
                        nd.arr[remolded_gene]["seq"] = aff_seq(
                            chld, sis, remolded_gene, remolded_gene
                        )

                        nd.arr[donor_gene]["model"] = computeModels(nd, donor_gene)
                        nd.arr[remolded_gene]["model"] = computeModels(
                            nd, remolded_gene
                        )

                #
                #                         if not nd.name in rem_dict:
                #                             rem_dict[nd.name] =[]
                #
                #                         rem_dict[nd.name].append((remolded_gene,donor_gene))
                #
                if direction_not_detected:
                    for i in range(len(direction_not_detected)):
                        # nod = direction_not_detected[i][0]
                        g1 = direction_not_detected[i][1]
                        g2 = direction_not_detected[i][2]

                        if nd.name not in rem_dict:
                            rem_dict[nd.name] = []

                        if (
                            tuple(reversed((g1, g2))) not in rem_dict[nd.name]
                            and (g1, g2) not in rem_dict[nd.name]
                        ):
                            rem_dict[nd.name].append((g1, g2))

            if (
                chld.name not in rem_dict and sis.name in rem_dict
            ):  # ## only sis have remolding candidate
                remolding_direction = []
                direction_not_detected = []
                res = []
                for arr2 in rem_dict[sis.name]:
                    res.append(do_alignments(sis, arr2, sis.get_sisters()[0]))

                for d in res:
                    for k in d:
                        if (
                            len(list(d[k].keys())) > 1
                        ):  # # this is the sister tRNA is missing.
                            if (
                                not k.split("_")[1]
                                == max(d[k], key=lambda x: d[k][x]).split("_")[1]
                            ):
                                # remolding_output.write(max(d[k], key=lambda x: d[k][x]).split("_")[1]+" "+k.split("_")[1]+" " + get_Nc(taxidmap_file, k.split("_")[0])+"\n")
                                remolding_output.write(
                                    max(d[k], key=lambda x: d[k][x]).split("_")[1]
                                    + " "
                                    + k.split("_")[1]
                                    + " "
                                    + k.split("_")[0]
                                    + "\n"
                                )

                                remolding_direction.append(
                                    (
                                        sis,
                                        k.split("_")[1],
                                        max(d[k], key=lambda x: d[k][x]).split("_")[1],
                                    )
                                )
                            else:
                                needed_genes = tuple(
                                    [i.split("_")[1] for i in list(d[k].keys())]
                                )
                                # (sis,)+tuple(reversed((needed_genes[0],needed_genes[1]))) in direction_not_detected check if the reversed tuple is in the list
                                if (
                                    not (sis, needed_genes[0], needed_genes[1])
                                    in direction_not_detected
                                ):
                                    direction_not_detected.append(
                                        (sis, needed_genes[0], needed_genes[1])
                                    )

                if (
                    remolding_direction
                ):  # # the case where we couldnt detect the direction of the remolding | ASK Matthias what should we do when we can't detect it.

                    for i in range(len(remolding_direction)):

                        node = remolding_direction[i][0]
                        remolded_gene = remolding_direction[i][1]
                        donor_gene = remolding_direction[i][2]

                        node.arr[donor_gene]["seq"] += node.arr[remolded_gene]["seq"]
                        node.arr[donor_gene]["structure"] += node.arr[remolded_gene][
                            "structure"
                        ]

                        node.arr[remolded_gene]["seq"] = ""
                        node.arr[remolded_gene]["structure"] = ""

                        nd.arr[donor_gene]["seq"] = aff_seq(
                            chld, sis, donor_gene, donor_gene
                        )
                        nd.arr[remolded_gene]["seq"] = aff_seq(
                            chld, sis, remolded_gene, remolded_gene
                        )

                        nd.arr[donor_gene]["model"] = computeModels(nd, donor_gene)
                        nd.arr[remolded_gene]["model"] = computeModels(
                            nd, remolded_gene
                        )
                #
                #                         if not nd.name in rem_dict:
                #                             rem_dict[nd.name] =[]
                #
                #                         rem_dict[nd.name].append((remolded_gene,donor_gene))
                #
                if direction_not_detected:
                    for i in range(len(direction_not_detected)):
                        # nod = direction_not_detected[i][0]
                        g1 = direction_not_detected[i][1]
                        g2 = direction_not_detected[i][2]

                        if nd.name not in rem_dict:
                            rem_dict[nd.name] = []

                        if (
                            not tuple(reversed((g1, g2))) in rem_dict[nd.name]
                            and (g1, g2) not in rem_dict[nd.name]
                        ):
                            rem_dict[nd.name].append((g1, g2))

    remolding_output.close()


def aff_seq_all(nd, gene, genes_sequences, taxidmap_file):
    fasta = ""
    if not os.path.isdir(out_fasta):
        os.makedirs(out_fasta)
    if gene in list(nd.arr.keys()):
        # print nd.arr[gene]['seq'],"heyyyyyyyyyyy ",nd.arr['atp8']['seq']
        # print nd.arr['atp8']['seq']
        # if nd.is_leaf() and nd.arr[gene]['seq']:
        if (
            nd.is_leaf()
            and get_sequence_PCgenes(nd.acc, nd.arr[gene]["seq"], genes_sequences)
            is not None
        ):
            # print "hallo I am leaf  ", nd.acc
            # fasta="> "+nd.name+"_"+gene+"\n"+nd.arr[gene]['seq']+"\n"

            fasta = (
                "> "
                + nd.name
                + "_"
                + gene
                + "\n"
                + get_sequence_PCgenes(nd.acc, nd.arr[gene]["seq"], genes_sequences)
                + "\n"
            )
            nd.arr[gene]["seq"] = fasta

            seq = open(out_fasta + nd.name + "_" + gene + ".fas", "w")
            seq.write(str(fasta))
            seq.close()
            return str(fasta)

        if not nd.is_leaf():
            fasta = ""
            for chld in nd.get_children():
                if hasattr(chld, "arr"):
                    # print chld.name , chld.arr
                    if gene in list(chld.arr.keys()):
                        fasta += aff_seq_all(chld, gene, genes_sequences, taxidmap_file)
                        nd.arr[gene]["seq"] = fasta
                    else:
                        with open(work_dir + "missing_gene.txt", "a") as missing_trna:
                            missing_trna.write(
                                get_Nc(taxidmap_file, chld.name)
                                + " ("
                                + chld.name
                                + ") is missing "
                                + gene
                                + "\n"
                            )
                        continue

        # print nd.name

        seq = open(out_fasta + nd.name + "_" + gene + ".fas", "w")
        seq.write(str(fasta))
        seq.close()
        return str(fasta)
    else:
        # return ","
        sys.stderr.write(
            "skipping (no " + gene + ") in " + get_Nc(taxidmap_file, nd.name) + " "
        )


def computeModels(nd, gene):
    if nd.is_leaf() and gene in list(nd.arr.keys()):
        # print nd.name
        mod = nd.arr[gene]["model"]
        return mod

    if not nd.is_leaf():
        mod1 = computeModels(nd.get_children()[0], gene)
        if len(nd.get_children()) == 2:
            mod2 = computeModels(nd.get_children()[1], gene)
        else:
            mod2 = None
        #         print mod1,mod2 ,"lllllllllllllllll"
        if mod1 is not None and mod2 is not None:

            # both children have models for this gene
            os.system(
                "hmmsearch --tblout "
                + out_stockholm
                + nd.name
                + "_"
                + gene
                + "_hm_"
                + nd.get_children()[0].name
                + '.sto "'
                + mod1
                + '" "'
                + out_fasta
                + nd.name
                + "_"
                + gene
                + '.fas" '
            )
            os.system(
                "hmmsearch --tblout "
                + out_stockholm
                + nd.name
                + "_"
                + gene
                + "_hm_"
                + nd.get_children()[1].name
                + '.sto "'
                + mod2
                + '" "'
                + out_fasta
                + nd.name
                + "_"
                + gene
                + '.fas" '
            )
            file1 = (
                out_stockholm
                + nd.name
                + "_"
                + gene
                + "_hm_"
                + nd.get_children()[0].name
                + ".sto"
            )
            score1, i = get_score(str(file1), 3)
            file2 = (
                out_stockholm
                + nd.name
                + "_"
                + gene
                + "_hm_"
                + nd.get_children()[1].name
                + ".sto"
            )
            score2, j = get_score(str(file2), 3)
            model, child = get_bestmodel(
                score1 / i,
                score2 / j,
                mod1,
                mod2,
                nd.get_children()[0].name,
                nd.get_children()[1].name,
            )
            print(child, model)
            if child == nd.get_children()[0].name:
                if (
                    not nd.get_children()[0].get_children()
                    or not os.path.exists(
                        out_fasta + nd.get_children()[1].name + "_" + gene + ".fas   "
                    )
                    or os.stat(
                        out_fasta + nd.get_children()[1].name + "_" + gene + ".fas   "
                    ).st_size
                    == 0
                    or not len(nd.get_children()) == 2
                ):  # first child does not have childrens // directly above leafs // no use for --mapali

                    print(
                        "aligning at "
                        + nd.name
                        + " based on "
                        + nd.get_children()[0].name
                        + " without mapali "
                    )
                    cmd = (
                        "hmmalign -o "
                        + out_stockholm1
                        + gene
                        + "/"
                        + nd.name
                        + "_"
                        + gene
                        + "_hm_"
                        + child
                        + ".sto "
                        + model
                        + " "
                        + out_fasta
                        + nd.name
                        + "_"
                        + gene
                        + ".fas  "
                    )
                    os.system(cmd)
                    # alignment = out_stockholm1 + gene + '/' + nd.name + '_' + gene + '_hm_' + child + '.sto '
                    print("case 1 : ", cmd)
                else:  # has grand children >> use mapali
                    cmd = (
                        "hmmalign --mapali "
                        + findSTH(child)
                        + " -o "
                        + out_stockholm1
                        + gene
                        + "/"
                        + nd.name
                        + "_"
                        + gene
                        + "_hm_"
                        + child
                        + ".sto "
                        + model
                        + " "
                        + out_fasta
                        + nd.get_children()[1].name
                        + "_"
                        + gene
                        + ".fas   "
                    )
                    os.system(cmd)
                    print("case 1.1")

            elif child == nd.get_children()[1].name:
                if (
                    not nd.get_children()[1].get_children()
                    or not os.path.exists(
                        out_fasta + nd.get_children()[0].name + "_" + gene + ".fas  "
                    )
                    or os.stat(
                        out_fasta + nd.get_children()[0].name + "_" + gene + ".fas   "
                    ).st_size
                    == 0
                    or not len(nd.get_children()) == 2
                ):
                    cmd = (
                        "hmmalign  -o "
                        + out_stockholm1
                        + gene
                        + "/"
                        + nd.name
                        + "_"
                        + gene
                        + "_hm_"
                        + nd.get_children()[1].name
                        + ".sto "
                        + model
                        + " "
                        + out_fasta
                        + nd.name
                        + "_"
                        + gene
                        + ".fas   "
                    )
                    os.system(cmd)
                    print(
                        "case 2 :/opt/bi/hmmalign "
                        + model
                        + " "
                        + out_fasta
                        + nd.name
                        + "_"
                        + gene
                        + ".fas > "
                        + out_stockholm1
                        + gene
                        + "/"
                        + nd.name
                        + "_"
                        + gene
                        + "_hm_"
                        + nd.get_children()[1].name
                        + ".sto "
                    )
                else:  # has grand children >> use mapali
                    cmd = (
                        "hmmalign --mapali  "
                        + findSTH(nd.get_children()[1].name)
                        + " -o "
                        + out_stockholm1
                        + gene
                        + "/"
                        + nd.name
                        + "_"
                        + gene
                        + "_hm_"
                        + nd.get_children()[1].name
                        + ".sto "
                        + model
                        + " "
                        + out_fasta
                        + nd.get_children()[0].name
                        + "_"
                        + gene
                        + ".fas "
                    )
                    os.system(cmd)
                    print("case 3 : ", cmd)

            if child == nd.get_children()[0].name:
                os.system(
                    'hmmbuild   "'
                    + work_dir
                    + "result_HMM_refseq63/"
                    + gene
                    + "/"
                    + nd.name
                    + "_"
                    + gene
                    + '.hm" "'
                    + out_stockholm1
                    + gene
                    + "/"
                    + nd.name
                    + "_"
                    + gene
                    + "_hm_"
                    + nd.get_children()[0].name
                    + '.sto" '
                )
                #                 cmd='hmmcalibrate   '+work_dir+'result_HMM_refseq63/'+gene+'/' + nd.name + '_' + gene + '.hm '
                #                 print cmd
                #                 os.system(cmd)
                with open("ndal3.tmp", "a") as file:
                    file.write(
                        nd.name
                        + " "
                        + out_stockholm1
                        + gene
                        + "/"
                        + nd.name
                        + "_"
                        + gene
                        + "_hm_"
                        + nd.get_children()[0].name
                        + ".sto\n"
                    )
            else:
                os.system(
                    'hmmbuild   "'
                    + work_dir
                    + "result_HMM_refseq63/"
                    + gene
                    + "/"
                    + nd.name
                    + "_"
                    + gene
                    + '.hm" "'
                    + out_stockholm1
                    + gene
                    + "/"
                    + nd.name
                    + "_"
                    + gene
                    + "_hm_"
                    + nd.get_children()[1].name
                    + '.sto" '
                )
                #                 cmd='/opt/bin/hmmcalibrate  '+work_dir+'result_HMM_refseq63/'+gene+'/' + nd.name + '_' + gene + '.hm '
                #                 print cmd
                #                 os.system(cmd)
                with open("ndal3.tmp", "a") as file:
                    file.write(
                        nd.name
                        + " "
                        + out_stockholm1
                        + gene
                        + "/"
                        + nd.name
                        + "_"
                        + gene
                        + "_hm_"
                        + nd.get_children()[1].name
                        + ".sto\n"
                    )

            if os.path.isfile(
                work_dir
                + "result_HMM_refseq63/"
                + gene
                + "/"
                + nd.name
                + "_"
                + gene
                + ".hm"
            ):
                nd.arr[gene]["model"] = (
                    work_dir
                    + "result_HMM_refseq63/"
                    + gene
                    + "/"
                    + nd.name
                    + "_"
                    + gene
                    + ".hm"
                )
                return nd.arr[gene]["model"]

        elif (
            mod1 is not None and mod2 is None
        ):  # only child1 have model for this gene, align only based on child1
            if (
                not nd.get_children()[0].get_children()
                or not os.path.exists(
                    out_fasta + nd.get_children()[1].name + "_" + gene + ".fas   "
                )
                or os.stat(
                    out_fasta + nd.get_children()[1].name + "_" + gene + ".fas   "
                ).st_size
                == 0
                or not len(nd.get_children()) == 2
            ):
                cmd = (
                    "hmmalign  -o "
                    + out_stockholm1
                    + gene
                    + "/"
                    + nd.name
                    + "_"
                    + gene
                    + "_hm_"
                    + nd.get_children()[0].name
                    + ".sto "
                    + mod1
                    + " "
                    + out_fasta
                    + nd.name
                    + "_"
                    + gene
                    + ".fas    "
                )
                os.system(cmd)
                print("case 4:", cmd)

            else:  # has grand children >> use mapali
                cmd = (
                    "hmmalign --mapali "
                    + findSTH(nd.get_children()[0].name)
                    + " -o "
                    + out_stockholm1
                    + gene
                    + "/"
                    + nd.name
                    + "_"
                    + gene
                    + "_hm_"
                    + nd.get_children()[0].name
                    + ".sto "
                    + mod1
                    + " "
                    + out_fasta
                    + nd.get_children()[1].name
                    + "_"
                    + gene
                    + ".fas   "
                )
                os.system(cmd)

            os.system(
                'hmmbuild   "'
                + work_dir
                + "result_HMM_refseq63/"
                + gene
                + "/"
                + nd.name
                + "_"
                + gene
                + '.hm" "'
                + out_stockholm1
                + gene
                + "/"
                + nd.name
                + "_"
                + gene
                + "_hm_"
                + nd.get_children()[0].name
                + '.sto" '
            )
            #             cmd = '/opt/bin/hmmcalibrate  '+work_dir+'result_HMM_refseq63/'+gene+'/' + nd.name + '_' + gene + '.hm '
            #             print cmd
            #             os.system(cmd)

            with open("ndal3.tmp", "a") as file:
                file.write(
                    nd.name
                    + " "
                    + out_stockholm1
                    + gene
                    + "/"
                    + nd.name
                    + "_"
                    + gene
                    + "_hm_"
                    + nd.get_children()[0].name
                    + ".sto\n"
                )
                # file.write(nd.name +' '+ mod1+'\n')

            if os.path.isfile(
                work_dir
                + "result_HMM_refseq63/"
                + gene
                + "/"
                + nd.name
                + "_"
                + gene
                + ".hm"
            ):
                nd.arr[gene]["model"] = (
                    work_dir
                    + "result_HMM_refseq63/"
                    + gene
                    + "/"
                    + nd.name
                    + "_"
                    + gene
                    + ".hm"
                )

            return nd.arr[gene]["model"]

        elif (
            mod1 is None and mod2 is not None
        ):  # only child2 have model for this gene, align only based on child2

            if (
                not nd.get_children()[1].get_children()
                or not os.path.exists(
                    out_fasta + nd.get_children()[0].name + "_" + gene + ".fas   "
                )
                or os.stat(
                    out_fasta + nd.get_children()[0].name + "_" + gene + ".fas   "
                ).st_size
                == 0
                or not len(nd.get_children()) == 2
            ):  # second child does not have childrens // directly above leafs // no use for --mapali
                cmd = (
                    "hmmalign  -o "
                    + out_stockholm1
                    + gene
                    + "/"
                    + nd.name
                    + "_"
                    + gene
                    + "_hm_"
                    + nd.get_children()[1].name
                    + ".sto "
                    + mod2
                    + " "
                    + out_fasta
                    + nd.name
                    + "_"
                    + gene
                    + ".fas   "
                )
                os.system(cmd)
                print("case 5 : ", cmd)
            else:  # has grand children >> use mapali
                cmd = (
                    "hmmalign --mapali  "
                    + findSTH(nd.get_children()[1].name)
                    + " -o "
                    + out_stockholm1
                    + gene
                    + "/"
                    + nd.name
                    + "_"
                    + gene
                    + "_hm_"
                    + nd.get_children()[0].name
                    + ".sto "
                    + mod2
                    + " "
                    + out_fasta
                    + nd.get_children()[0].name
                    + "_"
                    + gene
                    + ".fas  "
                )
                os.system(cmd)
                print("case 6: ", cmd)
            os.system(
                'hmmbuild   "'
                + work_dir
                + "result_HMM_refseq63/"
                + gene
                + "/"
                + nd.name
                + "_"
                + gene
                + '.hm" "'
                + out_stockholm1
                + gene
                + "/"
                + nd.name
                + "_"
                + gene
                + "_hm_"
                + nd.get_children()[1].name
                + '.sto" '
            )
            #             cmd='/opt/bin/calibrate   '+work_dir+'result_HMM_refseq63/'+gene+'/' + nd.name + '_' + gene + '.hm  '
            #             print cmd
            #             os.system(cmd)
            with open("ndal3.tmp", "a") as file:
                file.write(
                    nd.name
                    + " "
                    + out_stockholm1
                    + gene
                    + "/"
                    + nd.name
                    + "_"
                    + gene
                    + "_hm_"
                    + nd.get_children()[1].name
                    + ".sto\n"
                )
            if os.path.isfile(
                work_dir
                + "result_HMM_refseq63/"
                + gene
                + "/"
                + nd.name
                + "_"
                + gene
                + ".hm"
            ):
                nd.arr[gene]["model"] = (
                    work_dir
                    + "result_HMM_refseq63/"
                    + gene
                    + "/"
                    + nd.name
                    + "_"
                    + gene
                    + ".hm"
                )

            return nd.arr[gene]["model"]

        else:  # both children have no model for this gene
            print("Oh shit!")
            return None


def init_leafs_seq(t, gene):
    for nd in t:
        if gene in list(nd.arr.keys()):

            if nd.is_leaf():
                fasta = "> " + nd.name + "_" + gene + "\n" + nd.arr[gene]["seq"] + "\n"

                nd.arr[gene]["seq"] = fasta
    return t


def aff_seq(chld, sis, g1, g2):

    if g1 in chld.arr and g2 in sis.arr:
        return chld.arr[g1]["seq"] + sis.arr[g2]["seq"]
    elif g1 in chld.arr and g2 not in sis.arr:
        return chld.arr[g1]["seq"]
    elif g1 not in chld.arr and g2 in sis.arr:
        return sis.arr[g1]["seq"]
    elif g1 not in chld.arr and g2 not in sis.arr:
        return ""
    else:
        print("shit,WTF")


def findSTH(id):
    file = open(
        "ndal3.tmp", "r"
    )  # ndal.tmp > temporary file to store the correct alignment models
    for line in file:
        line = line.split()
        if line[0] == id:
            best = line[1]
    file.close()

    return best


def intialize_non_leaves(t):
    # global taxidmap_file
    # file = taxidmap_file

    for n in t.traverse(strategy="postorder"):
        if not n.is_leaf():
            # genes_arr=["trnS1","trnF","trnD","trnY","trnS2","trnL1","trnL2","trnH","trnI","trnM","trnN","trnC","trnE","trnP","trnQ","trnR","trnT","trnW","trnK","trnA","trnG","trnV"]
            # genes_arr = ["trnL1","trnL2"]
            genes_arr = ["cox1", "atp8"]
            data = {k: {"model": "", "seq": "", "structure": ""} for k in genes_arr}
            n.add_feature("arr", data)
    return t


def intialize_non_leaves_g(t, file):

    for n in t.traverse(strategy="postorder"):
        if not n.is_leaf():
            # genes_arr=["trnS1","trnF","trnD","trnY","trnS2","trnL1","trnL2","trnH","trnI","trnM","trnN","trnC","trnE","trnP","trnQ","trnR","trnT","trnW","trnK","trnA","trnG","trnV"]
            # genes_arr = ["trnL1","trnL2"]
            genes_arr = [
                "cox1",
                "atp8",
                "atp6",
                "cox3",
                "nad3",
                "nad4l",
                "nad4",
                "nad5",
                "nad6",
                "cob",
                "nad1",
                "nad2",
                "heg",
                "mttb",
                "msh1",
                "atp9",
                "cox2",
            ]
            data = {k: {"model": "", "seq": ""} for k in genes_arr}
            n.add_feature("arr", data)
    return t


def initialize_leaves(t, data_array, outdir, file):

    for n in t.traverse(strategy="postorder"):
        n.add_feature("score", 0)
        # n.add_feature('arr', {gene:{'model': '', 'structure': '', 'seq': ''}})   ### make it as empty dictionary if possible

        if get_Nc(file, n.name) in data_array:
            n.add_feature("arr", data_array[get_Nc(taxidmap_file, n.name)])
        else:
            genes_arr = [
                "cox1",
                "atp8",
                "atp6",
                "cox3",
                "nad3",
                "nad4l",
                "nad4",
                "nad5",
                "nad6",
                "cob",
                "nad1",
                "nad2",
                "heg",
                "mttb",
                "msh1",
                "atp9",
                "cox2",
            ]

            data = {k: {"model": None, "seq": ""} for k in genes_arr}
            n.add_feature("arr", data)

        n.add_feature("acc", get_Nc(file, n.name))

    return t


def remolding_in_species_tree(t):  # ## this version includes the tree
    #     remove identity sequences from the alignments. only align one sequence to one model

    # i can do it without going through the whole tree, i can just go through the dictionary where the data is .. the tree is only needed when im working with the in tree remolding
    # # it is only needed in the case where i need to compare with the sister specie

    global taxidmap_file
    for nd in t:
        for g1 in nd.arr:  # to get the gene seq
            for g2 in nd.arr:  # to get the model
                if not os.path.isfile(
                    work_dir + "remolding/fasta_files/" + nd.name + "_" + g1 + ".fas"
                ):
                    f = open(
                        work_dir
                        + "remolding/fasta_files/"
                        + nd.name
                        + "_"
                        + g1
                        + ".fas",
                        "w",
                    )
                    # f.write("> "+nd.name+"_"+g1+"\n"+nd.arr[g1]['seq']+"\n")
                    # f.write("> "+nd.name+"_"+g2+"\n"+nd.arr[g2]['seq']+"\n")
                    f.write(nd.arr[g1]["seq"] + "\n")
                    # f.write(nd.arr[g2]['seq']+"\n")
                    f.close()
                # aligning with model of gene2

                os.system(
                    '/opt/bin/cmalign "'
                    + nd.arr[g2]["model"]
                    + '" "'
                    + work_dir
                    + "remolding/fasta_files/"
                    + nd.name
                    + "_"
                    + g1
                    + '.fas" > '
                    + work_dir
                    + "remolding/stockholm_files/"
                    + nd.name
                    + "_"
                    + g1
                    + "cm_"
                    + g2
                    + ".sto "
                )
                os.system(
                    "/opt/bin/cmalign --sfile "
                    + work_dir
                    + "remolding/score_files/"
                    + nd.name
                    + "_"
                    + g1
                    + "_cm_"
                    + g2
                    + '.sto "'
                    + nd.arr[g2]["model"]
                    + '" "'
                    + work_dir
                    + "remolding/fasta_files/"
                    + nd.name
                    + "_"
                    + g1
                    + '.fas" '
                )

                file = open(
                    work_dir
                    + "remolding/score_files/"
                    + nd.name
                    + "_"
                    + g1
                    + "_cm_"
                    + g2
                    + ".sto",
                    "r",
                )
                score1 = 0
                for line in file:
                    if not line.startswith("#"):

                        temp = line.split()
                        score1 = float(temp[6])
                file.close()

                with open(work_dir + "remolding/bit_scores.txt", "a") as remf:
                    #            accession                        taxid    gene_sequence    model    score
                    remf.write(
                        get_Nc(taxidmap_file, nd.name)
                        + " "
                        + nd.name
                        + " "
                        + g1
                        + " "
                        + g2
                        + "  "
                        + str(score1)
                        + "\n"
                    )


def cm_call(model, fasta_file, sth_file):
    # print '/opt/bin/cmalign ' + model+ ' '+fasta_file+' > '+sth_file
    # print '/opt/bin/cmalign --sfile '+sth_file +' '+ model + ' '+fasta_file

    # os.system('/opt/bin/cmalign ' + model+ ' '+fasta_file+' > '+sth_file)
    if not os.path.isfile(sth_file):
        os.system(
            "        /opt/bin/cmalign --sfile "
            + sth_file
            + " "
            + model
            + " "
            + fasta_file
        )


def species_no_trna():
    import ast

    outfile = open("species_zero_trna.txt", "w")
    ofile = open("remolding/missing_trnas.txt", "r")
    for line in ofile:
        line = line.split("set")
        lst = ast.literal_eval(line[1])
        acc = line[0].split(" ")[0]
        outfile.write(acc + "    " + str(len(lst)) + "\n")
    ofile.close()
    outfile.close()


def remolding_in_species(pool, dat_trna):  # ## this version DOES NOT includes the tree
    #     remove identity sequences from the alignments. only align one sequence to one model
    genes_arr = [
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
    global taxidmap_file
    for acc in dat_trna:
        if len(dat_trna[acc]) != len(genes_arr):
            with open(work_dir + "remolding/missing_trnas.txt", "a") as missing_trnas:
                missing_trnas.write(
                    acc
                    + " is missing "
                    + str(set(genes_arr) - set(dat_trna[acc].keys()))
                    + "\n"
                )

        for g1 in dat_trna[acc]:
            for g2 in dat_trna[acc]:
                if not os.path.isfile(
                    work_dir + "remolding/fasta_files/" + acc + "_" + g1 + ".fas"
                ):
                    f = open(
                        work_dir + "remolding/fasta_files/" + acc + "_" + g1 + ".fas",
                        "w",
                    )

                    f.write(
                        "> " + acc + "_" + g1 + "\n" + dat_trna[acc][g1]["seq"] + "\n"
                    )

                    f.close()
                # aligning with model of gene2
                # os.system('/opt/bin/cmalign \"' + dat_trna[acc][g2]['model'] + '\" \"'+work_dir+'remolding/fasta_files/' + acc + '_' + g1 + '.fas\" > '+work_dir+'remolding/stockholm_files/' + acc + '_' + g1+ 'cm_'+g2 + '.sto ')
                # os.system('/opt/bin/cmalign --sfile '+work_dir+'remolding/score_files/' + acc + '_' + g1+ '_cm_'+g2+ '.sto \"' + dat_trna[acc][g2]['model'] + '\" \"'+work_dir+'remolding/fasta_files/' + acc + '_' + g1+ '.fas\" '

                pool.apply_async(
                    cm_call,
                    args=(
                        dat_trna[acc][g2]["model"],
                        work_dir + "remolding/fasta_files/" + acc + "_" + g1 + ".fas",
                        work_dir
                        + "remolding/score_files/"
                        + acc
                        + "_"
                        + g1
                        + "_cm_"
                        + g2
                        + ".sto",
                    ),
                )


def get_scores_in_species(dat_trna):
    global taxidmap_file
    for acc in dat_trna:
        for g1 in dat_trna[acc]:
            for g2 in dat_trna[acc]:
                print(acc, g1, g2)
                try:
                    file = open(
                        work_dir
                        + "remolding/score_files/"
                        + acc
                        + "_"
                        + g1
                        + "_cm_"
                        + g2
                        + ".sto",
                        "r",
                    )
                except Exception:
                    print("Scheisse !!!")
                    continue
                score1 = 0
                for line in file:
                    if not line.startswith("#"):

                        temp = line.split()
                        score1 = float(temp[6])
                file.close()

                with open(outp_dir + "bit_scores.txt", "a") as remf:
                    remf.write(acc + " " + g1 + " " + g2 + "  " + str(score1) + "\n")


def trans_six_frames(seq, table):
    rev = seq.reverse_complement()
    for i in range(3):
        yield seq[i:].translate(table)
        yield rev[i:].translate(table)


def get_model(node):
    if node.is_leaf():
        acc = get_Nc(taxidmap_file, node.name)
        path = "/homes/brauerei2/marwa/phd/gc/RefSeq/outputdir/GM-refseq63/" + acc + "/"
        for file in os.listdir(path):
            if file == node.name + "_cox1.hm":
                return path + file
    else:
        if node.is_root():
            return "/homes/brauerei2/marwa/phd/tool/mtdb/data/trees_and_data/result_HMM_refseq63/NoName_cox1.hm"
        else:
            path = "/homes/brauerei2/marwa/phd/tool/mtdb/data/trees_and_data/result_HMM_refseq63/"
            for file in os.listdir(path):
                if file == node.name + "_cox1.hm":
                    return path + file


#         d={}
#         models_file = 'mod.out'
#         with open (models_file) as f:
#             for line in f:
#                 key, value = line.split(':')
#                 d[key.strip()] = value.strip()
#         for k in d:
#
#             if k==node:
#                 print d[k]
#                 return d[k]


def hmmscan_call_old(model, outfile):
    score = 0

    # print model
    # path ='hmmscan --noali --notextw -o homes/brauerei2/marwa/phd/tool/mtdb/data/trees_and_data/prot6frames/halfdb/'+outfile+'.out ' +model + '  /homes/brauerei2/marwa/phd/tool/mtdb/data/trees_and_data/prot6frames/NC_001712-2.fas'
    # print path
    # print " THE MODEL IS : ", model
    if model is not None:
        # if not os.path.isfile(model+'.h3f'):
        output = (
            "/homes/brauerei2/marwa/phd/tool/mtdb/data/trees_and_data/prot6frames/halfdb/"
            + outfile
        )

        os.system('hmmpress -f "' + model + '"')
        print("ggggggggggggggggggggggggggggggggggggggg", outfile)
        # print 'hmmscan --noali --notextw -o '+output+'.out \"' +model + '\"' /homes/brauerei2/marwa/phd/tool/mtdb/data/trees_and_data/prot6frames/NC_001712-2.fas'
        os.system(
            "hmmscan --noali --notextw -o "
            + output
            + ".out --tblout "
            + output
            + '-0.out "'
            + model
            + '"  /homes/brauerei2/marwa/phd/tool/mtdb/data/trees_and_data/prot6frames/NC_001712-2.fas'
        )
        #     os.system('hmmscan --noali --notextw -o scan-all.out  cox1.db  /homes/brauerei2/marwa/phd/tool/mtdb/data/trees_and_data/prot6frames/NC_001712-2.fas')
        # '.sto \"'+ mod1 + '\" \"' + out_fasta +nd.name + '_' + gene + '.fas\" >test.out ')
        # os.system('hmmalign \"' + model + '\" \"'+work_dir+'fasta_files/' + nd.name + '_' + gene + '.fas\" > '+out_stockholm1 + nd.name + '_' + gene + '_hm_' + child + '.sto ')

        file = open(output + "-0.out", "r")
        for line in file:
            print(line)
            if not line.startswith("#"):
                temp = line.split()
                score = float(temp[5])
        file.close()

        return score


def rec(n, outfile):
    # if n.is_leaf:
    #     outfile.write('by' + n.arr['cox1']['model'])
    #     return
    # print "hiiiiiiiiii"
    if not n.is_leaf():
        print(n.get_children()[0].name, n.get_children()[1].name)
        # print n.get_children()[0].get_ascii(show_internal=True)
        # print n.get_children()[1].get_ascii(show_internal=True)

        s0 = hmmscan_call(get_model(n.get_children()[0]), n.get_children()[0].name)
        if n.get_children()[1]:
            s1 = hmmscan_call(get_model(n.get_children()[1]), n.get_children()[1].name)
        if s1 != 0 and s0 != 0:
            if s0 > s1:
                outfile.write(
                    n.get_children()[0].name
                    + ":"
                    + str(s0)
                    + "--"
                    + n.get_children()[1].name
                    + ":"
                    + str(s1)
                )
                outfile.write("\n")
                outfile.write("s0>s1")
                outfile.write("\n")
                rec(n.get_children()[0], outfile)
            else:
                outfile.write(
                    n.get_children()[1].name
                    + ":"
                    + str(s1)
                    + "--"
                    + n.get_children()[0].name
                    + ":"
                    + str(s0)
                )
                outfile.write("\n")
                outfile.write("s1>s0")
                outfile.write("\n")

                rec(n.get_children()[1], outfile)
        elif s0 != 0 and s1 == 0:
            outfile.write(
                n.get_children()[0].name
                + ":"
                + str(s0)
                + "--"
                + n.get_children()[1].name
                + ":"
                + str(s1)
            )
            outfile.write("\n only ch0\n")
            rec(n.get_children()[0], outfile)
        elif s0 == 0 and s1 != 0:
            outfile.write(
                n.get_children()[1].name
                + ":"
                + str(s1)
                + "--"
                + n.get_children()[0].name
                + ":"
                + str(s0)
            )
            outfile.write("\n only ch1\n")
            rec(n.get_children()[1], outfile)
        else:
            outfile.write("both have no Models\n")

    else:
        print(n.name)
        s = hmmscan_call(get_model(n), n.name)
        outfile.write(n.name + ":" + str(s))
        outfile.write("\n")


# ## important : species NC_023272 was missing from in species remolding, it needs to be re calcuated -- 18 MARCH 2014
def get_non_sigmodels(modfile, scanfile):
    l1 = []
    l2 = []
    l3 = []
    with open(modfile) as modfile:
        for line in modfile:
            l1.append(line.split(":")[0])
    with open(scanfile) as scanfile:
        for line in scanfile:
            if not line.startswith("#"):
                temp = line.split()
                l2.append(temp[0].split("_cox1")[0])

    l3 = set(l1) - set(l2)
    print((len(l3)))

    return l2


def get_path(n, t):
    path = []

    while n.up:
        path.append(n.name)
        n = n.up
    path.append(n.name)
    return path


def find_node(n, file, gene):
    with open(file, "r") as f:
        node = ""
        for line in f:
            if line.split()[0].startswith(n):
                node = line.split()[0]
                return node.split("_" + gene)[0]


# def get_gm(t, file, gene):
#     pathes = []
#     l = []
#     with open (file, 'r')as f:
#         for n in t.traverse(strategy='levelorder'):
#             node = find_node(n.name + '_' + gene, file, gene)
#             if node is not None:
#                 pathes.append(get_path(t & node, t))
#         pathes = sorted(pathes, key=len)
#         print(pathes[len(pathes) - 1])


# def get_bed_info(file, root):
#     with open (file, 'r') as f:
#          for line in f:
#             if line.split()[0].startswith(root):
#                 s = line.split()[17]
#                 s = int(s) * 3
#                 s = str(s)
#                 e = line.split()[18]
#                 e = int(e) * 3
#                 e = str(e)
#                 g = file.split('.fas-')[1].split('-')[0]
#                 a = line.split()[0].split('_' + g)
#                 eval = str(line.split()[6])
#                 strand = file.split('.fas')[0].split('-')[1]
#                 break
#     return g, s, e, strand, eval


# def bed_generate(gb_files, root, accession):
#     phyla, uniq = load_phyla(gb_files)
#     for p in uniq:
#         dir = trans_files + p + '/'
#         lst = glob.glob(dir + '*.pos.out')
#         bed_dir = dir + '/bed/'
#         if not os.path.isdir(bed_dir):
#             os.makedirs(bed_dir)
#         for f in lst:
#             acc = f.split('.fas')[0].split('-')[0]

#             with open(bed_dir + acc + '.bed' 'a') as bed_file:
#                 if os.stat(bed_file).st_size > 0:
#                     bed_file.write('accession      gene      start      end      strand       E-value\n')
#                     g, s, e, strand, ev = get_bed_info(f, root)
#                     bed_file.write(accession + '      ' + g + '      ' + s + '      ' + e + '      ' + strand + '       ' + ev + '\n')


def hmmscan_call(file, gene, dbfile, level):
    # if gene =='cox2':
    #     ext='bad-fs-badcox2th01-re.out'

    # outdir=os.path.dirname(file)+'/'+level+'/mafft/'+gene+'/'
    outdir = os.path.dirname(file) + "/" + level + "/leveldb/" + gene + "/"

    if not os.path.exists(outdir):
        os.makedirs(outdir)
    scoredir = outdir + "outscore/"
    alndir = outdir + "aln/"
    if not os.path.exists(scoredir):
        os.makedirs(scoredir)
    if not os.path.exists(alndir):
        os.makedirs(alndir)
    scorefile = os.path.basename(file).split(".")[0] + ".out"
    # alnfile = os.path.basename(file).split('.')[0] + '.aln'
    cmd = (
        "hmmscan --max  --notextw --noali   --domtblout "
        + scoredir
        + scorefile
        + " "
        + dbfile
        + " "
        + file
    )  # + ' >' + alndir+alnfile
    #     print cmd
    os.system(cmd)


#     print 'shmmscan --max  --notextw    --domtblout '+file+'-'+gene+'-'+level +'-bad.out ' +dbfile + ' '+ file


def get_frame_old(acc, gene, el):
    tmp = {}

    for e in el:
        regex = re.escape(acc) + r".*" + re.escape(gene) + r".*-all.out"
        match = re.match(regex, str(os.path.basename(e)))
        if match:

            tmp[os.path.basename(e)] = os.path.getsize(e)
            #            print tmp[os.path.basename(e)]

            if len(tmp) == 6:

                z = max(tmp, key=tmp.get)
                return z


def get_strand(frame):
    if int(frame) % 2 == 0:
        strand = 1
    else:
        strand = -1
    return strand


def init_t(t):
    for n in t.traverse("postorder"):
        n.add_features(b=-1, s=-1, db=-1, ds=-1, p="no", a="", l=-1)
    return t


def get_aa_pos(frame, s, end, el):
    if frame == "0":
        aa_s = float(s) / 3

    elif frame == "4":
        aa_s = (s - 2) / 3

    return aa_s


def get_nuc_pos(frame, s, end, el):
    # print "aa",frame, s,end, l
    # print "frame s end l "
    # print frame,s,end,l
    s = int(s) - 1
    el = int(el)
    end = int(end) - 1
    # print type(frame),len(frame),frame
    if frame == "0":
        nuc_s = 3 * s
        nuc_e = 3 * (end + 1)
    elif frame == "1":
        nuc_s = el - (3 * (end + 1))
        nuc_e = el - (3 * s) - 1
    elif frame == "2":
        nuc_s = 3 * s + 1
        nuc_e = 3 * (end + 1) + 1
    elif frame == "3":
        nuc_s = el - (3 * (end + 1) + 1)
        nuc_e = el - (3 * s) - 1 - 1
    elif frame == "4":
        nuc_s = 3 * (s) + 2
        nuc_e = 3 * (end + 1) + 2
    elif frame == "5":
        nuc_s = el - (3 * (end + 1) + 2)
        nuc_e = el - (3 * s) - 2 - 1
    return nuc_s, nuc_e


def get_b_s(n, fpos, refs, el, th):
    b = -1
    s = -1
    a = ""
    with open(fpos, "r") as fp:
        nuc_s = -1000000000
        nuc_e = -1000000000
        eval = 20
        flag = True
        data = []

        # if n.split('NC')[0] is None:
        #     print 'none',n
        #     for line in fp:
        #         if not line.startswith('#'):
        #             data.append(line.split())
        # else:\
        for line in fp:
            # if not line.startswith('#'):
            #     print n.split('NC')[0], line.split()[0]
            #     print line.split()[3],n.split('NC')[1].split('--')[0]
            #     print line.split()[17],n.split('NC')[1].split('--')[1]
            #     print line.split()[18],n.split('NC')[1].split('--')[2]
            if not line.startswith("#"):

                if (
                    line.split()[0].endswith(n.split("NC")[0])
                    and line.split()[3]
                    .rstrip()
                    .endswith(n.split("NC")[1].split("--")[0])
                    and line.split()[17].startswith(n.split("NC")[1].split("--")[1])
                    and line.split()[18].startswith(n.split("NC")[1].split("--")[2])
                ):
                    data.append(line.split())
                    break
                    # print line.split()
        if data:
            # print data
            if len(data) == 1:
                s = data[0][17]
                end = data[0][18]
                b = data[0][13]
                eval = data[0][6]
                ceval = data[0][12]
                a = data[0][0]
                frame = data[0][len(data[0]) - 1]

            elif len(data) > 1:
                m = min(data, key=lambda x: float(x[6]))
                ind = []
                for x in data:
                    if x[6] == m[6]:
                        ind.append(data.index(x))

                if len(ind) == 1:
                    s = data[ind[0]][17]
                    end = data[ind[0]][18]
                    b = data[ind[0]][13]
                    eval = data[ind[0]][6]
                    ceval = data[ind[0]][12]
                    a = data[ind[0]][0]
                    frame = data[ind[0]][len(data[0]) - 1]
                elif len(ind) > 1:
                    tmp = []
                    for x in data:
                        if data.index(x) in ind:
                            tmp.append(x)
                    maxi = max(tmp, key=lambda x: float(x[7]))
                    ind2 = []
                    for x in data:
                        if data.index(x) in ind:
                            if x[13] == maxi[13]:
                                ind2.append(data.index(x))
                    if len(ind2) == 1:
                        s = data[ind2[0]][17]
                        end = data[ind2[0]][18]
                        b = data[ind2[0]][13]
                        eval = data[ind2[0]][6]
                        ceval = data[ind2[0]][12]
                        a = data[ind2[0]][0]
                        frame = data[ind2[0]][len(data[0]) - 1]

                    if len(ind2) > 1:
                        tmp2 = []
                        for x in data:
                            if data.index(x) in ind2:
                                tmp2.append(x)
                        mini = min(tmp2, key=lambda x: float(x[12]))
                        ind3 = data.index(mini)
                        s = data[ind3][17]
                        end = data[ind3][18]
                        b = data[ind3][13]
                        eval = data[ind3][6]
                        ceval = data[ind3][12]
                        a = data[ind3][0]
                        frame = data[ind3][len(data[0]) - 1]

            # print refs

            # print a,b,eval
            frame = frame.split(".")[0]
            if s > 0:
                # print "frameee "+frame
                nuc_s, nuc_e = get_nuc_pos(frame, s, end, el)
                # print data
                # print gene,s,nuc_s,end,nuc_e,frame,get_strand(int(frame))
                # s= abs(refs-nuc_s)

            if s < 0:
                flag = False
                frame = "7"

            return a, b, s, flag, frame, nuc_s, nuc_e, eval, ceval, end


def do_delta(acc, t, delta, fpos, phylum, gene, refs):
    t = init_t(t)
    seq = SeqIO.read(fasta_files_dir + acc + ".fas", "fasta")
    seq = seq.seq
    l_genome = len(seq)
    if get_id(taxidmap_file, acc) == "":
        # print "empty", get_id(taxidmap_file,acc)
        return
    with open(fpos, "r") as f:  # get best leaf
        nd = get_best_leaf(f)
    if nd is not None:
        # print nd,fpos
        p = get_path(t & nd, t)
        # print path
        for n in t.traverse("levelorder"):
            # print n.name,path
            if n.name in p:
                n.a, n.b, n.s, flag, frame, nuc_s = get_b_s(
                    n.name, fpos, refs, l_genome
                )
                # print fpos,n.name,n.a,n.b,n.s

                if n.s >= 0:
                    list = []
                    if not n.is_root():
                        n.db = abs(float(n.b) - float(n.up.b))
                        n.ds = abs(float(n.s) - float(n.up.s))
                        n.p = "yes"
                        list.append(n.a)
                        list.append(str("%.2f" % n.db))
                        list.append(str(n.ds))
                        list.append(n.p)
                        list.append(os.path.basename(fpos))
                        list.append(phylum)
                        list.append(str(frame))

                        list.append(str(refs))
                        list.append(n.up.name)
                        list.append(str(n.up.s))
                        list.append(str(l_genome))
                        delta.write("\t".join(list) + "\n")
                        if n.get_sisters():
                            sis = n.get_sisters()[0]
                            list = []
                            sis.a, sis.b, sis.s, flag, frame, nuc_s = get_b_s(
                                sis.name, fpos, refs, l_genome
                            )
                            if sis.s >= 0:
                                sis.p = "no"
                                sis.db = abs(float(sis.b) - float(sis.up.b))
                                sis.ds = abs(float(sis.s) - float(sis.up.s))
                                list.append(sis.a)
                                list.append(str("%.2f" % sis.db))
                                list.append(str(sis.ds))
                                list.append(sis.p)
                                list.append(os.path.basename(fpos))
                                list.append(phylum)
                                list.append(str(frame))

                                list.append(str(refs))
                                list.append(sis.up.name)
                                list.append(str(sis.up.s))
                                list.append(str(l_genome))

                                delta.write("\t".join(list) + "\n")

                    else:
                        n.db = 0
                        n.ds = 0
                        n.p = "yes"
                        list.append(n.a)
                        list.append(str("%.2f" % n.db))
                        list.append(str(n.ds))
                        list.append(n.p)
                        list.append(os.path.basename(fpos))
                        list.append(phylum)
                        list.append(str(frame))
                        list.append(str(n.s))

                        list.append(str(l_genome))

                        delta.write("\t".join(list) + "\n")


#                     delta.write(n.a+ '   '+str(n.db) + '    '+str(n.ds)+'    '+n.p+'       '+acc+'\n')

#                                 delta.write(sis.a+ '   '+str(sis.db) + '    '+str(sis.ds)+'    '+sis.p+'       '+acc+'\n')

#                     delta.write(n.a+ '   '+str(n.db) + '    '+str(n.ds)+'    '+n.p+'\n')


def get_level_models(ndfile, t, gene, level):
    taxes = []
    models = []
    global out_models
    if level == "root":
        mod = out_models + gene + "/" + "NoName" + "_" + gene + ".hm"
        # mod =out_models+gene+'/root.hm'
        models.append(mod)
    else:
        with open(ndfile, "r") as f:
            for line in f:
                if level in line.split("\t|")[2]:
                    taxes.append(line.split("\t|")[0])

            # print taxes
        for n in t.traverse(strategy="levelorder"):
            # print n.name
            if n.name in taxes:
                if level == "species":
                    mod = (
                        outp_dir
                        + "outputdir1/GM-refseq63/"
                        + get_Nc(taxidmap_file, n.name)
                        + "/"
                        + n.name
                        + "_"
                        + gene
                        + ".hm"
                    )
                    # print mod
                else:
                    mod = out_models + gene + "/" + n.name + "_" + gene + ".hm"
                # print mod
                if os.path.isfile(mod):
                    models.append(mod)
    models = set(models)

    # print len(taxes)
    return models


def get_start(gene, acc):

    file = gb_files + acc + ".gb"
    gb = gbfromfile(file)
    for f in gb.getfeatures():
        if f.name == gene:

            return f.start


def get_stop(gene, file):
    gb = gbfromfile(file)
    for f in gb.getfeatures():
        if f.name == gene:
            return f.stop


#     with open (gb_files+acc+'.gb','r')as gb:
#         for record in SeqIO.parse(gb,'genbank'):
#             for f in record.features:
#                 if (f.type in ['CDS','gene'] and (f.qualifiers['gene'][0]==gene.upper() or f.qualifiers['gene'][0]==gene)) or f.type =='misc_feature' and gene.upper in f.qualifiers['note'][0] :
# #                         print(f.qualifiers['gene'],f.type, f.location)
#                         return f.location.start.position


def get_best_leaf(f, t, gene):
    # print f
    for line in f:
        if not line.startswith("#"):
            nd = line.split()[0].split("_" + gene)[0]
            # print line
            print(nd)
            if nd:
                res = t & nd
                if res.is_leaf():
                    return res.name


def do_ds(fpos, gene, t, acc, phylum, refs, delta):
    t = init_t(t)
    with open(fpos, "r") as f:  # get best leaf
        nd = get_best_leaf(f, t, gene)
        # print fpos,nd

        # print type(nd)
        if nd is not None:
            # print nd,fpos
            p = get_path(t & nd, t)
            # print "psurat yasinath = ",p
            seq = SeqIO.read(fasta_files_dir + acc + ".fas", "fasta")
            seq = seq.seq
            l_genome = len(seq)
            for n in t.traverse(strategy="levelorder"):
                if n.name in p:
                    level = p.index(n.name) / float(len(p))
                    level = "{:.2f}".format(level)
                    # print n.name,p.index(n.name),len(p),level

                    n.a, n.b, n.s, flag, frame, nuc_s = get_b_s(
                        n.name, fpos, refs, l_genome
                    )

                    if n.s >= 0:
                        list = []
                        if not n.is_root():
                            n.ds = float(n.s) - float(n.up.s)
                        else:
                            n.ds = 0

                        list.append(n.a)
                        list.append(str(n.ds))
                        list.append(str(level))
                        list.append(os.path.basename(fpos))
                        list.append(str(frame))
                        list.append(str(nuc_s))
                        # list.append(str(refs))
                        # list.append(n.up.name)
                        # list.append(str(n.up.s))
                        # list.append(str(l_genome))
                        delta.write("\t".join(list) + "\n")


def merge_frames(acc, gene, el, p, level):
    mergedir = work_dir + "prot6frames-test/" + p + "/merged/" + level + "/upp/"
    mergedir = work_dir + "prot6frames-test/" + p + "/merged/" + level + "/leveldb/"

    if not os.path.exists(mergedir):
        os.makedirs(mergedir)
    file = mergedir + gene + "-" + acc + ".out"

    outfile = open(file, "w")
    outfile.close()
    with open(file, "a") as outfile:
        header = open(el[0], "r")
        head = [str(next(header)).rstrip() for x in range(3)]
        for line in head:
            outfile.write(str(line) + "\n")  # TODO last header columnt = 'frame'
        header.close()
        for f in el:
            with open(f, "r") as infile:
                for line in infile:
                    if not line.startswith("#"):
                        # add frames to merged file
                        line = (
                            line.rstrip()
                            + "    "
                            + os.path.basename(f).split(".fas")[0].split("-")[1]
                            + "\n"
                        )
                        # print  os.path.basename(f).split('.fas')[0].split('-')[1],
                        outfile.write(str(line))
    return file


def floatequal(f1, list):
    equal = False
    for f2 in list:
        if abs(Decimal(f1) - Decimal(f2)) < 0.00001:
            equal = True
    return equal


def index_2d(myList, v):
    ind = []
    if v == 0.0:
        v = 0
    if "-" in str(v):
        if len(str(v).split("-")[1]) == 1:
            v = str(v).split("-")[0] + "-0" + str(v).split("-")[1]
    for i, x in enumerate(myList):
        if str(v).lower() in x or floatequal(v, x):
            ind.append(i)
    return ind


def fix_overlap(featlist, l_genome):
    for f1 in featlist:
        for f2 in featlist:

            if f1 != f2:
                if f1.overlap(f2, "circular", l_genome) > 20:
                    # print f1.name,f2.name
                    # print 'overlap >20'
                    if f1.score == f2.score:
                        # print "equal scores"
                        tmp = []
                        tmp.append(f1)
                        tmp.append(f2)
                        v = random.choice(tmp)
                        print(v)
                        fixlist = [s for s in featlist if s != v]
                        # print fixlist
                        featlist = []
                        featlist.extend(fixlist)
                    elif f1.score < f2.score:
                        # print '2'
                        fixlist = [s for s in featlist if s != f2]
                        featlist = []
                        featlist.extend(fixlist)
                    else:
                        # print '1'
                        fixlist = [s for s in featlist if s != f1]
                        featlist = []
                        featlist.extend(fixlist)
                    # print f1.name,f2.name,f1.overlap(f2, "circular", l_genome), f2.overlap(f1,"circular",l_genome)
    return featlist


# return feature list if no overlatp (one gene)
# ToDO allow a 20%overlap


def get_best_hits(fpos, gene, l_genome, th, found):
    # print fpos
    # mod=[]
    # with open(fpos,'r') as fp:
    #     for line in fp:
    #         if not line.startswith('#'):
    #             mod.append(line.split()[0].rstrip())
    # mod=set(mod)
    # data=[]
    # best=[]
    # featlist=[]
    # if mod:
    #     for m in mod:
    #         for r in get_b_s(m,fpos,level,0,l_genome):
    #             eval=r[1]
    #             strand=get_strand(int(r[4]))
    #             if float(eval)<=th:
    #                 data.append(r)
    #     if not data:
    #         for m in mod:
    #             data.append(get_b_s(m,fpos,level,0,l_genome)[0])
    mod = []
    with open(fpos, "r") as fp:
        for line in fp:
            if line:
                if not line.startswith("#"):
                    # print line.split()[0]+line.split()[3],line.split()[17],line.split()[18]
                    mod.append(
                        line.split()[0]
                        + line.split()[3]
                        + "--"
                        + line.split()[17]
                        + "--"
                        + line.split()[18]
                    )

    mod = set(mod)
    #     print mod
    data = []
    best = []
    featlist = []
    if mod:
        # if same frame only one best hit is taken
        # if many frames then append in data
        for m in mod:
            a, b, s, flag, frame, nuc_s, nuc_e, eval, ceval, end = get_b_s(
                m, fpos, 0, l_genome, th
            )

            if frame:
                strand = get_strand(int(frame))

                if float(eval) < th and b > 0 and float(ceval) < th:
                    # print ceval
                    # seq =SeqIO.read(fpos.split('merged')[0]+'NC_'+fpos.split('NC_')[1].split('.')[0]+'-'+frame+'.fas','fasta')
                    # seq=str(seq.seq)
                    # print seq
                    # seq=seq[int(line.split()[17])+2:int(line.split()[18])-2]
                    # if not '*' in seq:
                    data.append([b, ceval, nuc_s, nuc_e, strand, s, end, frame])
                    # print data

        if data:
            if len(data) == 1:
                ind = [0]
            else:
                mi = min(Decimal(c[1]) for c in data)
                ind = index_2d(data, mi)
            #                 print  mi, " mi"

            ind2 = -1
            ma = -10

            if len(ind) > 1:

                for i in ind:
                    if float(data[i][0]) > (ma):
                        ma = data[i][0]

                ind2 = random.choice(index_2d(data, ma))
                best = data[ind2]
                best_ind = ind2
            else:
                # print ind[0]
                best = data[ind[0]]
                best_ind = ind[0]
            srt = sorted(data, key=lambda k: float(k[1]))
            res = []
            res.append(data[best_ind])
            f1 = feature(
                gene,
                "gene",
                int(best[2]),
                int(best[3]),
                best[4],
                "genbank",
                score=best[1],
            )
            featlist.append(f1)
            if found == "F" or (
                found == "NF" and gene != "atp8"
            ):  # if atp8 not found I take only the best hit
                for d in srt:
                    overlap = "no"
                    f2 = feature(
                        gene,
                        "gene",
                        int(d[2]),
                        int(d[3]),
                        int(d[4]),
                        "genbank",
                        score=d[1],
                    )
                    cap12, cup12 = f1.capcup(f2, "circular", l_genome)
                    for r in res:
                        f3 = feature(
                            gene,
                            "gene",
                            int(r[2]),
                            int(r[3]),
                            int(r[4]),
                            "genbank",
                            score=r[1],
                        )
                        cap23, cup23 = f2.capcup(f3, "circular", l_genome)
                        if (
                            float(cap23) / f2.length("circular", l_genome) > 0.2
                            or float(cap23) / f3.length("circular", l_genome) > 0.2
                        ):
                            overlap = "yes"
                    if overlap == "no":
                        res.append(d)
                        featlist.append(f2)

            return featlist


# TODO : test more in detaills incase of many nonoverlap
# bed files #
# run on all genes


def delgaps(gene, level, ndfile, t):
    models = get_level_models(ndfile, t, gene, level)
    sto = glob.glob(out_stockholm1 + gene + "/*")

    for mod in models:
        for stofile in sto:
            if os.path.basename(stofile).startswith(
                os.path.basename(mod).split(".")[0]
            ):
                align = AlignIO.read(stofile, "stockholm")
                indices = []
                for i in range(len(align[0]) - 1):
                    c = align[:, i]
                    if c.count("-") / float(len(align)) < 0.70:
                        indices.append(i)

                al = align[:, indices[0] : indices[0] + 1]
                for i in indices:
                    if i == indices[0]:
                        continue
                    al = al + align[:, i : i + 1]
                if not os.path.exists(out_stockholm1 + "pruned/" + gene):
                    os.makedirs(out_stockholm1 + "pruned/" + gene)
                outfile = (
                    out_stockholm1 + "pruned/" + gene + "/" + os.path.basename(stofile)
                )
                out = open(outfile, "w")
                AlignIO.write(al, out, "stockholm")


def parse_res():
    out = open(work_dir + "prot6frames-test/bedroot/stats.txt", "a")
    out.write("tp    fn    fp    eval \n")
    for root, dirs, files in os.walk(work_dir + "prot6frames-test/bedroot/"):
        for dir in dirs:
            if dir.startswith("eval"):
                print(dir)
                #                 os.system('sh ./compare-trna.sh ../../../gc/RefSeq/refseq63-gb-test '+ work_dir+'prot6frames-test/bedroot/'+dir)
                file = root + dir + "/results.tex"
                with open(file, "r") as f:
                    for line in f:
                        if line.startswith("gene"):
                            line.rstrip()

                            res = line.split("&")
                            res.pop(0)
                            for i, n in enumerate(res):
                                if "num" in n:
                                    res[i] = n.split("{")[1].split("}")[0]
                                if "\\\\" in n:
                                    res[i] = n.split("\\")[0]
                            d = list(zip(*[iter(res)] * 2))
                            print(d[0][0], d[2][0], d[3][0])
                            out.write(
                                d[0][0]
                                + "    "
                                + d[2][0]
                                + "    "
                                + d[3][0]
                                + "    "
                                + str(10 ** (int(dir.split(".")[1].split("r")[0])))
                                + "\n"
                            )


# ###TOD call compare from python looping over all imput bed
# ### parse results
# ## produce table tp,tn,fp fn , |  evalue
# draw graph
# check nad6 phylum alignments


def prunedmods(gene, level):
    if not os.path.exists(work_dir + "result_HMM_refseq63/pruned/" + gene):
        os.makedirs(work_dir + "result_HMM_refseq63/pruned/" + gene)
    if level == "root":
        print("root ")
        modname = (
            work_dir + "result_HMM_refseq63/pruned/" + gene + "/NoName_" + gene + ".hm"
        )
        cmd = (
            "hmmbuild "
            + modname
            + " "
            + out_stockholm1
            + "pruned/"
            + gene
            + "/NoName_"
            + gene
            + "*.sto"
        )
        print(cmd)
        os.system(cmd)
    else:
        for sto in glob.glob(out_stockholm1 + "pruned/" + gene + "/*"):

            if not os.path.basename(sto).startswith("NoName"):
                modname = (
                    work_dir
                    + "result_HMM_refseq63/pruned/"
                    + gene
                    + "/"
                    + os.path.basename(sto).split("_hm")[0]
                    + ".hm"
                )
                cmd = "hmmbuild " + modname + " " + sto
                print(cmd)
                os.system(cmd)


# TODO create databse of pruned nad6
# write bed , compare with genbank


def check_phyla():
    ndfile = work_dir + "nodes.dmp"
    t = Tree(tree_file, format=8)
    # models =
    get_level_models(ndfile, t, "cox1", "phylum")
    print(t & "702324")
    print(get_Nc(taxidmap_file, "702324"))
    print(get_Nc(taxidmap_file, "10228"))


#     for m in models:
#         print os.path.basename(m),len(t&os.path.basename(m).split('_')[0])
#     if not os.path.exists(work_dir+'prot6frames-test/phyladb/'):
#         os.makedirs(work_dir+'prot6frames-test/phyladb/')
#     for m in models:
#         os.system('cp '+m+' '+work_dir+'prot6frames-test/phyladb/')
#     for m in glob.glob(work_dir+'prot6frames-test/phyladb/*.hm'):
#         os.system('hmmpress -f '+work_dir+'prot6frames-test/phyladb/'+m)


def tpfp(file):
    with open(os.path.dirname(file) + "/dist.dat", "w") as dist:
        print(os.path.dirname(file) + "/dis.dat")
        with open(file, "r") as dat:
            for line in dat:
                line = line.split()
                if line[1] != "NA":
                    if line[2] == line[1]:
                        dist.write("tp    " + line[7] + "\n")
                    else:
                        dist.write("fp    " + line[7] + "\n")


def bed():
    phyla, uniq = load_phyla(gb_files)
    #     print len(phyla),len(uniq)
    #     print gb_files
    levels = ["phylum", "class", "order", "family"]
    levels = ["family"]
    #     accs=["NC_023776",'NC_024882','NC_025755','NC_024105','NC_024878','NC_025750', 'NC_025749', 'NC_025751','NC_023776','NC_025224','NC_024056','NC_025754','NC_025753', 'NC_025752','NC_023926','NC_025289','NC_025241']
    #     print len(accs)

    #     accs=['NC_024679','NC_024680','NC_024678','NC_024097','NC_024874','NC_024096','NC_024677','NC_025291','NC_024275','NC_025267','NC_023933','NC_024676']
    #     accs= ['NC_024676','NC_024874','NC_024680','NC_024097','NC_024679','NC_024096','NC_023782','NC_024754','NC_024677']
    #     accs=['NC_024096','NC_024275','NC_024097']
    #     accs=['NC_024935']
    #     with open('atp8fn.dat','r') as a:
    #         for line in a:
    #             accs.append(line.rstrip())
    #     print accs
    for level in levels:
        print(level)
        bedir = work_dir + "prot6frames-test/bed" + level + "/" + level + "atp8-phyl/"
        #         bedir=work_dir+'prot6frames-test/bed'+level+'/'+level+'atp8-phyl/'
        bedir = work_dir + "prot6frames-test/bed" + level + "/leveldb/"
        if not os.path.exists(bedir):
            os.makedirs(bedir)

        #         print bedir
        for p in uniq:
            # if  p == 'Ecdysozoa':
            print(p)
            for acc in ["NC_024026"]:
                if phyla[acc] == p:
                    f = acc + ".bed"
                    print(acc)
                    gbfile = gb_files + acc + ".gb"
                    seq = SeqIO.read(fasta_files_dir + acc + ".fas", "fasta")
                    seq = seq.seq
                    directory = work_dir + "/prot6frames-test/" + p + "/"
                    if not os.path.isdir(directory):
                        os.makedirs(directory)
                    transl_table = get_transtable(gbfile)

                    for orf in enumerate(trans_six_frames(seq, transl_table)):
                        file = directory + acc + "-" + str(orf[0]) + ".fas"
                        with open(file, "w") as prot:
                            prot.write(">" + acc + "-" + str(orf[0]) + "\n")
                            prot.write(str(orf[1]))
                        for gene in genes_arr:
                            db = work_dir + "dblevel/" + level + "/" + gene + ".db"
                            #                             hmmscan_call(file,gene, work_dir+'badseq/fasta/fs/NoName_'+gene+'-fs.fas'+gene+'-re.hm',level)
                            hmmscan_call(file, gene, db, level)

                    #                 seq = SeqIO.read(fasta_files_dir+acc+".fas", "fasta")
                    #                 seq=seq.seq
                    l_genome = len(seq)
                    get_id(taxidmap_file, acc)
                    #                     if phyla[acc]== p:
                    # #                     print acc,phyla[acc]

                    featlist = []
                    res = []
                    fixedlist = []
                    th = 0.006

                    if not os.path.exists(bedir):
                        os.makedirs(bedir)
                    bedfile = bedir + acc + ".bed"
                    #                     if not os.path.exists(bedfile):

                    for gene in genes_arr:
                        # if not gene in ['nad4','nad2','nad6','cob']   :
                        # if gene=='nad2':
                        #     level='class'
                        #     dir = work_dir+'prot6frames-test/'+p+'/'+level+'/'
                        # else:
                        #     level='root'
                        dir = (
                            work_dir
                            + "prot6frames-test/"
                            + p
                            + "/"
                            + level
                            + "/"
                            + gene
                            + "/"
                            + "outscore/"
                        )
                        dir = (
                            work_dir
                            + "prot6frames-test/"
                            + p
                            + "/"
                            + level
                            + "/leveldb/"
                            + gene
                            + "/"
                            + "outscore/"
                        )

                        #                             dir = work_dir+'prot6frames-test/'+p+'/'+level+'/upp/'+gene+'/'+'outscore/'

                        #                         else:
                        #                             dir = work_dir+'prot6frames-test/'+p+'/'+level+'/'+gene+'/'+'outscore/'

                        #                         if gene=='nad2':
                        #                             l=glob.glob(dir+acc+'*nad2-class.out')
                        #                             print acc,l
                        #                         else :
                        lst = glob.glob(dir + acc + "*.out")
                        #                         print l
                        fpos = merge_frames(acc, gene, lst, p, level)
                        #                         print fpos
                        res = get_best_hits(fpos, gene, l_genome, th, "F")
                        #                         if gene in ['nad6','nad2','nad4l'] :
                        #                             print res
                        #                             if not res:
                        #                                 res=[]
                        #                                 t=[]
                        #                                 with open (fpos,'r') as fp:
                        #                                     for line in fp:
                        #                                         if not line.startswith('#') :
                        #                                             t.append(line.split())
                        #
                        #                                 m= min(t,key=lambda x: float(x[11]))
                        #                                 s=m[17]
                        #                                 end=m[18]
                        #                                 b=m[13]
                        #                                 eval=m[12]
                        #                                 a=m[0]
                        #                                 frame =m[len(t[0])-1].split('.')[0]
                        #                                 strand=get_strand(int(frame))
                        #                                 nuc_s,nuc_e=get_nuc_pos(frame,s,end,l_genome)
                        #                                 if float(eval)<=th and b>0  :
                        #                                     res.append(feature(gene,'gene',int(nuc_s),int(nuc_e),strand,'genbank',score = float(eval)))

                        if res:
                            for feat in res:
                                featlist.append(feat)
                    #
                    #
                    srt = sorted(featlist, key=lambda f: float(f.score))

                    print(" srt : ", srt)
                    #                     i=0
                    # #                     for f in srt:
                    # #                         if f.name=='nad4' or f.name=='nad5':
                    # #                             print f.start,f.stop  ,f.score,f.name
                    for f in srt:
                        j = 0
                        ov = False
                        while j <= len(fixedlist) - 1:
                            r = fixedlist[j]
                            j += 1
                            cap, cup = f.capcup(r, "circular", l_genome)
                            if (
                                float(cap) / f.length("circular", l_genome) > 0.25
                                or float(cap) / r.length("circular", l_genome) > 0.25
                            ):
                                print(f, r)
                                ov = True
                        # print  f.name,r.name,r.overlap(f,'cicurlar',l_genome), f.start, f.stop , r.start, r.stop,f.score,r.score,f.strand,r.strand
                        #
                        #
                        if not ov:
                            fixedlist.append(f)

                    #                       print fixedlist
                    bedwriter(fixedlist, acc, outfile=bedfile, mode="w")


def sys_call(string):
    os.system(string)


if __name__ == "__main__":
    usage = "usage: %prog dirs"
    parser = argparse.ArgumentParser(description=usage)
    # parser.add_argument('dirs', metavar = 'DIRS', nargs = '+', help = 'directories')
    parser.add_argument("work_dir", help="workdir")
    parser.add_argument("outp_dir", help="outputdir")
    args = parser.parse_args()

    alldirs = []

    #     file = 'scan-all-atp8-0.out'
    #     gene = 'atp8'
    # #     print find_node('INT_79_cox1',file)
    # #     get_gm(t.get_tree_root(),file,gene)
    #     path =get_path(t&'INT_4405',t.get_tree_root())
    #     print path

    random.seed(42)
    numpy.seterr(invalid="raise")
    register_ncbi_table(
        name="Pterobranchia Mitochondrial",
        alt_name=None,
        id=24,
        table={
            "TTT": "F",
            "TTC": "F",
            "TTA": "L",
            "TTG": "L",
            "TCT": "S",
            "TCC": "S",
            "TCA": "S",
            "TCG": "S",
            "TAT": "Y",
            "TAC": "Y",
            "TGT": "C",
            "TGC": "C",
            "TGA": "W",
            "TGG": "W",
            "CTT": "L",
            "CTC": "L",
            "CTA": "L",
            "CTG": "L",
            "CCT": "P",
            "CCC": "P",
            "CCA": "P",
            "CCG": "P",
            "CAT": "H",
            "CAC": "H",
            "CAA": "Q",
            "CAG": "Q",
            "CGT": "R",
            "CGC": "R",
            "CGA": "R",
            "CGG": "R",
            "ATT": "I",
            "ATC": "I",
            "ATA": "I",
            "ATG": "M",
            "ACT": "T",
            "ACC": "T",
            "ACA": "T",
            "ACG": "T",
            "AAT": "N",
            "AAC": "N",
            "AAA": "K",
            "AAG": "K",
            "AGT": "S",
            "AGC": "S",
            "AGA": "S",
            "AGG": "K",
            "GTT": "V",
            "GTC": "V",
            "GTA": "V",
            "GTG": "V",
            "GCT": "A",
            "GCC": "A",
            "GCA": "A",
            "GCG": "A",
            "GAT": "D",
            "GAC": "D",
            "GAA": "E",
            "GAG": "E",
            "GGT": "G",
            "GGC": "G",
            "GGA": "G",
            "GGG": "G",
        },
        stop_codons=["TAA", "TAG"],
        start_codons=["TTG", "CTG", "ATG", "GTG"],
    )

    #     t= Tree(tree_file,format =8)
    sys.stderr.write("load data\n")

    all_directory = [
        os.path.join(args.work_dir, f) for f in os.listdir(args.work_dir)
    ]  # getting all directories
    work_dir = args.work_dir
    outp_dir = args.outp_dir
    start = time.time()
    refseqdir = "/homes/brauerei2/marwa/phd/gc/RefSeq/"

    taxidmap_file = outp_dir + "new_taxidtoacc-refseq63.txt"
    tree_file = work_dir + "Final_Metazoa.nw"

    #     fasta_files_dir = outp_dir+"refseq63-fasta/"
    fasta_files_dir = refseqdir + "refseq63-fasta/"
    fasta_files_dir = "/scr/k61san/marwa/RefSeq-h2/refseq69-fasta/"
    fasta_files_dir = "/homes/brauerei2/marwa/phd/bpcpp/refseq73/"
    gene_models_dir = outp_dir + "GM-refseq63/"
    gb_files = outp_dir + "refseq69-gb/"
    #     gb_files=outp_dir+'refseq63-gb/'
    #     print gb_files
    out_fasta = work_dir + "clean_fasta_files/"
    out_stockholm = work_dir + "stockholm_filesgenes/"
    out_models = work_dir + "result_HMM_refseq63/"
    out_stockholm1 = work_dir + "stockholm_filesgenes1/"
    genes_arr = [
        "atp6",
        "cox3",
        "nad3",
        "nad4l",
        "nad4",
        "nad5",
        "nad6",
        "cob",
        "nad1",
        "nad2",
        "cox2",
        "atp8",
        "cox1",
    ]

    #     tree_file='refseq69.nw'
    #     t=Tree(tree_file,format=8)
    #     ndfile=work_dir+'nodes.dmp'
    #     t= Tree(tree_file,format =8)
    #     for lev in ['root','phylum','class','order','family','species']:
    #         print lev
    #         for gene in genes_arr:
    #             print gene
    #             models= get_level_models(ndfile,t,gene,lev)
    #             for m in models:
    #                 os.system('cat '+m+' >>'+work_dir+'/dblevel/'+lev+'/'+gene+'.db')
    #             print gene, len(models)

    f = work_dir + "nodes.dmp"
    genes_arr = [
        "atp6",
        "cox3",
        "nad3",
        "nad4l",
        "nad4",
        "nad5",
        "nad6",
        "cob",
        "nad1",
        "nad2",
        "cox2",
        "atp8",
        "cox1",
    ]
    #     check_phyla()
    #     tpfp(work_dir+'prot6frames-test-/bedphylum/01/results.dat')
    #     parse_res()
    #     levels=['root','phylum']
    #     for level in levels:
    #     for gene in genes_arr:
    #         print gene
    # #             delgaps(gene,level,f,t)
    # #             prunedmods(gene,level)
    #         cmd= 'cat '+work_dir+'result_HMM_refseq63-test/pruned/'+gene+'/NoName*.hm >'+work_dir+'db-test/pruned/'+'root'+'-'+gene+'.db'
    #         print cmd
    #         os.system(cmd)
    # ######translate 6 frames#####################################
    #     phyla,uniq=load_phyla(gb_files)
    # #     l=phyla.values()
    # #     for p in uniq:
    # #         print p,l.count(p)
    # #     from collections import Counter
    # #     from itertools import chain
    # #
    # #     counts = Counter(chain.from_iterable(phyla.keys() for e in phyla))
    # #     print counts
    #     for p in uniq:
    #         print p, phyla.count(p)
    #
    #         if acc=='NC_023220':
    #             for p in uniq:
    #
    #                 gbfile=gb_files+acc+'.gb'
    #                 if phyla[acc]==p:
    #                     seq = SeqIO.read(fasta_files_dir+acc+".fas", "fasta")
    #                     seq=seq.seq
    #
    #                     directory = work_dir+'/prot6frames-test/'+p+'/'
    #                     if not os.path.isdir(directory):
    #                         os.makedirs(directory)
    #                     transl_table= get_transtable(gbfile)
    #
    #
    #                     l = trans_six_frames(seq,transl_table)
    #                     for orf in enumerate(l):
    #                         file = directory+acc+'-'+str(orf[0])+'.fas'
    #                         with open (file,'w') as prot:
    #                              prot.write('>'+acc+'-'+str(orf[0])+'\n')
    #                              prot.write(str(orf[1]))

    #                          real    1m33.207s
    #                         user    0m48.925s
    # #                         sys    0m0.822s

    #     print st,stop
    #     nst,nstop=get_nuc_pos('5', aasta, aasto, l)
    #     print nst,nstop,'god'
    #     s=seq[nst:nstop+1]
    #     transl_table=get_transtable(outp_dir+"refseq69-gb/NC_025936.gb")
    #     s=Seq(s)
    # #     print s
    #     l = trans_six_frames(s,transl_table)
    #     for orf in enumerate(l):
    #
    #         print('>'+acc+'-'+str(orf[0])+'\n')
    #         print(str(orf[1]))

    #     TODO: t
    #     I have amino acids positions from frames files
    #     I test the get_nuc_pos
    #     dir =work_dir+'sttest/'
    #     print 'wth'
    #     if not os.path.exists(dir):
    #         os.makedirs(dir)
    #     transl_table=get_transtable(outp_dir+"refseq69-gb/NC_025936.gb")
    #     seq = SeqIO.read(fasta_files_dir+acc+".fas", "fasta").seq
    #     l = trans_six_frames(seq,transl_table)
    #     for orf in enumerate(l):
    #         file = dir+acc+'-'+str(orf[0])+'.fas'
    #         with open (file,'w') as prot:
    #              prot.write('>'+acc+'-'+str(orf[0])+'\n')
    #              prot.write(str(orf[1]))

    #                     seq=seq.seq

    #     print c
    #   for gene in genes_arr:
    # #                        print gene
    # #                        dbfile='/homes/brauerei2/marwa/phd/tool/mtdb/data/trees_and_data/db/all-'+gene + '.db'
    # #                        print 'file=', file
    # #
    # #                        os.system('hmmscan --noali --notextw -o '+file+'-'+gene+'-all.out --tblout '+file+'-'+gene+'-score.out --domtblout '+file+'-'+gene+'-pos.out ' +dbfile + ' '+ file)
    # #
    # #         os.system('hmmscan --noali -COX1-notextw -o scan-all-atp8.out --tblout scan-all-atp8-0.out --domtblout scan-all-atp8-1.out atp8db.db  /homes/brauerei2/marwa/phd/tool/mtdb/data/trees_and_data/prot6frames/NC_001712-2.fas')

    #     print get_Nc(taxidmap_file,"1204564")

    # #####Compute models ############################
    #     pool = mp.Pool(8)
    #     data_gene = load_data(gb_files)
    #     print 'Mar'
    #     genes_arr=["atp6","cox3","nad3","nad4l","nad4","nad6","nad5","cob","nad1","nad2","cox2","atp8","cox1"]
    #     genes_arr=['nad4','nad6','nad5','nad1','nad2','atp8']
    #     genes_arr=['atp8']
    #     genes_arr=['nad4l']
    #     genes_arr=['nad6','nad5','nad1','nad2','atp8']
    #     genes_arr=['atp6','cob','cox2']
    #     genes_arr=["nad3","nad4l","nad4","nad6","nad5","cob","nad1","nad2","cox2","atp8","cox1"]

    #     genes_arr=['cox3']
    #     genes_arr=["atp6","nad3","nad4l","nad4","nad6","nad5","cob","nad1","nad2","cox2","atp8","cox1"]

    #     genes_arr=["nad1","nad2","atp9","cox2","atp8","cox1"]
    #     for gene in genes_arr:
    #         if not os.path.isdir(out_stockholm1+gene):
    #             os.makedirs(out_stockholm1+gene)
    #         print gene
    #         gene_sequences = load_sequences(gene)
    #
    # #         pool = mp.Pool(4)
    #         model_build_genes(pool,data_gene,outp_dir,gene_sequences,gene)
    #     pool.close()
    #     pool.join()

    #
    #             real    94m38.571s /200/4m
    #             user    339m45.428s    17m
    #             sys    3m54.737s
    #         sys.stderr.write("convert data\n")
    # #
    #     for  root, dirs, files in os.walk (outp_dir):
    #         for file in files:
    #             os.system('/opt/bin/hmmcalibrate '+root+'/'+file)

    # #       mapali fix
    #     print "Mapali fix"
    #     pool =mp.Pool(16)
    #     for gene in genes_arr:
    #         print gene
    #         keys = list(data_gene.keys())
    # #         print keys
    #         for key in keys:
    #
    #
    #             string=''
    #             gene_sequences = load_sequences(gene)
    #             model = gene_models_dir +key + '/'+get_id(taxidmap_file,key)+'_'+gene+'.hm'
    # #             sequence = get_sequence_PCgenes(key,gene,gene_sequences)
    # #             accdir=outp_dir+'stockholm_files/'+key+'/'
    # #             if not os.path.exists(accdir):
    # #                 os.makedirs(accdir)
    # #             stofile=accdir+get_id(taxidmap_file,key)+'_'+gene+'.sto'
    #             if os.path.isfile(model) and not os.path.getsize(model)==0:
    #                 stofile=outp_dir+'stockholm_files/'+key+'/'+get_id(taxidmap_file,key)+'_'+gene+'.sto'
    # #                 with open (stofile, 'w') as sto:
    # #                     sto.write('# Stockholm 1.0 \n')
    # #                     sto.write(str(sequence))
    # #                     sto.write('\n//')
    #             if not os.path.exists(out_stockholm1+gene):
    #                 os.makedirs(out_stockholm1+gene)
    #             string = 'hmmalign -o '+out_stockholm1+gene+'/' + get_id(taxidmap_file,key) + '_'+gene+ '_hm_' + get_id(taxidmap_file,key) + '.sto ' +  model +' '+ stofile
    #             os.system(string)
    #             pool.apply_async(sys_call, args=(string,))
    # #
    #     pool.close()
    #     pool.join()

    #      real    95m35.222s
    #         # user    77m7.090s
    #         # sys     5m2.695s
    #     for gene in ["cox3","nad3","nad4l","nad4"]:

    #                         # real    241m1.563s
    #                         # user    0m0.000s
    #     for gene in genes_arr:
    #     for gene in ["nad5","nad6","cob","nad1","nad2","atp9","cox2","atp8","cox1"]:
    # #         eal    698m24.527s
    # #         user    640m12.969s
    # # #         sys     40m35.400s
    #     genes_arr=['atp8']
    #     for gene in genes_arr:
    # #          if not os.path.exists(work_dir+'result_HMM_refseq63/'+gene):
    # #              os.makedirs(work_dir+'result_HMM_refseq63-/'+gene)
    #          print gene,'LL'
    #          gene_sequences = load_sequences(gene)
    #
    #          t=Tree(tree_file,format=8)
    #          t=intialize_non_leaves_g(t,taxidmap_file)
    #          dict_data = convert_dict_g(data_gene,gene_sequences,taxidmap_file)
    #          t=initialize_leaves(t, dict_data,outp_dir,taxidmap_file)
    #          n=t.get_tree_root()
    #          aff_seq_all(n,gene,gene_sequences,taxidmap_file)
    #          computeModels(n, gene)

    # ########concatenate models in database#############
    #     genes_arr=["cox1","atp8"]
    #     for gene in genes_arr:
    #         l=[]
    #         for dir in os.listdir('/homes/brauerei2/marwa/phd/gc/RefSeq/outputdir/GM-refseq63-test/'):
    #             path = '/homes/brauerei2/marwa/phd/gc/RefSeq/outputdir/GM-refseq63-test/'+dir+'/'
    #             for i in os.listdir(path):
    #                 if os.path.isfile(os.path.join(path,i)) and gene+'.hm' in i:
    #                     l.append(path+i)
    #         with open(work_dir+'db-test/leaves-'+gene+'.db', 'w') as outfile:
    #             for fname in l:
    #                 with open(fname, 'r') as readfile:
    #                     outfile.write(readfile.read())
    #     for gene in genes_arr:
    #         dir = out_models+gene+'/'
    #         os.system('cat '+dir + '* >'+work_dir+'db-test/int-'+gene+'.db')
    #         os.system('cat '+work_dir + 'db-test/int-'+gene+'.db '+work_dir + 'db-test/leaves-'+gene + '.db >'+work_dir+'db-test/all-'+gene+'.db')
    #
    # #
    #

    # ######right frame############
    #     t= Tree(tree_file,format=8)
    #     t=t.get_tree_root()
    #     n = t&'INT_17'conferences.html
    #     while not  n.is_root():
    #         n=n.up
    #         print n.name
    #     data_gene=load_data(gb_files)
    #     phyla,uniq=load_phyla(gb_files)
    #     print uniq
    # #     for p in uniq:
    # # #         if not os.path.exists(work_dir+'prot6frames-test/'+p) :
    # # #             os.makedirs(work_dir+'prot6frames-test/'+p)
    #     for gene in ['cox1','atp8']:
    #         delta= open (work_dir+'prot6frames-test/'+'all'+'-'+gene+'-deltas.data','w')
    #         delta.close()#     print n.get_children()[0].name
    #     print n.get_children()[1].name
    #
    #         delta= open (work_dir+'prot6frames-test/'+'all'+'-'+gene+'-deltas.data','a')
    #         for p in uniq:
    # #
    #             for acc in phyla:
    #                 if phyla[acc]== p:
    #
    #                     dir = work_dir+'prot6frames-test/'+p+'/'
    #
    #                     l= glob.glob(dir+acc+'*'+gene+'-pos.out')
    #
    #                     refs = get_start(gene,acc)
    #
    #                     if not type(refs)==None:
    #                         refs=refs
    #                         fpos= merge_frames(acc,gene,l,p)
    #                         do_delta(acc,t,delta,fpos,p,gene,refs)
    # #                     pool.apply_async(do_delta, args=(acc,t,delta,fpos,p,gene,refs))
    # #                     #                         pool.apply_async(hmmscan_call, args=(file,gene,dbfile))
    # #       #     print n.get_children()[0].name
    #     print n.get_children()[1].name
    # #                         print 'fpos   ',fpos
    #         delta.close()
    #     pool.close()
    #     pool.join()

    # ----------feature class-------------
    #     s=20.1
    #     featlist=[]
    #     acc='NC_003165'
    #     fpos='/homes/brauerei2/marwa/phd/tool/mtdb/data/trees_and_data/prot6frames-test/Chordata/merged/nad6-NC_003165-phylum-merged.out'
    #     seq = SeqIO.read(fasta_files_dir+acc+".fas", "fasta")
    #     seq=seq.seq
    #     l_genome=len(seq)
    #     print get_best_hits(fpos,'nad6','phylum',l_genome)

    #     f=feature('co1','gene',int(1),int(55),1,'genbank',score =float(s))
    #     f2=feature('co2','gene',int(56),int(100),1,'genbank',score=float(s))
    #     f3=feature('co3','gene',int(1),int(55),1,'genbank',score =10.1)

    #     featlist.append(f)
    #     featlist.append(f2)
    #     featlist.append(f3)
    #     print fix_overlap(featlist,200)
    #     cap,cup=f.capcup(f2,'circular',200)
    #     print cap,cup#     print n.get_children()[0].name
    #     print n.get_children()[1].name
    #     if f==f2:
    #         print "true equal"
    #     if f!=f2:
    #         print "true not equal"
    #     print f.name
    # ---------------------------eval dirs -------------------
    #     for  root, dirs, files in os.walk (work_dir+'prot6frames-test/bedphylum/'):
    #         for dir in dirs:
    #             if dir.startswith('eval') and dir.endswith('phylum'):
    #                os.chdir(work_dir+'prot6frames-test/')
    #                print dir
    #                os.system('cp */bed/'+dir+'/* bedphylum/'+dir)

    # ---------------------copy refseq69test files-------------
    #     for file in os.listdir('/scr/k61san/marwa/RefSeq/metazoa-fasta/'):
    #
    #         if not os.path.exists('/scr/k61san/marwa/RefSeq/refseq63-fasta/'+file):
    #             os.system('cp /scr/k61san/marwa/RefSeq/metazoa-fasta/'+file+ ' /scr/k61san/marwa/RefSeq/refseq69-fasta/')
    #    --------------- keys = data_gene.keys()
    # # # #     print len(keys)
    # #     from subprocess import Popen, PIPE
    # #     cmd = "awk '{print $5}' /homes/brauerei2/marwa/phd/tool/mtdb/data/trees_and_data/prot6frames-test/all-cox1-deltas.data | uniq"
    # #     p = Popen(cmd, stdout=PIPE, stderr=PIPE,shell=True)
    # #     stdout, stderr = p.communicate()
    # #     l = stdout.split()
    # #
    # #     for i in range(len(l)):
    # #         l[i]=l[i].split('-')[0]
    # #
    # #     temp = [item for item in keys if item not in l]start(gene,acc)
    # -----------------do_ds------------
    #     for gene in ['atp8','cox1']:
    #         delta = open(work_dir+'prot6frames-test/ds-'+gene+'.data','w')
    #         delta.close()
    #         delta = open(work_dir+'prot6frames-test/ds-'+gene+'.data','a')
    #
    #         for p in uniq:
    # #         for p in ['Porifera']:
    #             for acc in phyla:
    #     #                     if phyla[acc]==p:
    #                 if phyla[acc]== p:
    #     #                     print phyla[acc]
    #
    #                     dir = work_dir+'prot6frames-test/'+p+'/'
    #
    #                     l= glob.glob(dir+acc+'*'+gene+'-pos.out')
    #
    #     #                     print acc,get_id(taxidmap_file,acc)
    #                     refs = get_start(gene,acc)
    #     #                     st.write(str(acc)+ '   '+str(refs)+'\n')
    #     #                     print " refs: ", refs
    #                     if not type(refs)==None:
    # #                         refs=refs
    #                         fpos= merge_frames(acc,gene,l,p)
    #         #                 print refs
    # #                         fall= get_frame(acc,gene,l)
    #     #                         print dir
    #     #                         print acc,gene,l
    #     #                         print "fall", fall
    #     #                         print fall ,'fiiiiiii#     print n.get_children()[0].name
    #     print n.get_children()[1].nameiile'
    # #                         fpos=fall.split('-all')[0]+'-pos.out'
    #                         do_ds(fpos,gene,t,acc,p,refs,delta)
    #     delta.close()
    #                         pool.apply_async(do_ds,args=(fpos,gene,t,acc,p,refs))
    #     pool.close()
    #     pool.join()

    # -----------------------hmmer2scan----------------
    #     levels=['root','phylum']
    #     phyla,uniq=load_phyla(gb_files)
    #     f=work_dir+'nodes.dmp'
    #     genes_arr=['nad5']
    #     for gene in genes_arr:
    #         models=get_level_models(f,t,gene,levels[0])
    #         for mod in models:
    #             for p in uniq:
    #                 for fas in glob.glob(work_dir+'prot6frames-test/'+p+'/*.fas'):
    #                     cmd= '/opt/bin/hmmsearch ' +mod+' '+fas+ ' >'+fas+'-'+gene+'-'+level+'.out '
    #                     os.system(cmd)
    #

    # #--------------------get_phyla_models----------------
    #     levels=['class','phylum','root']
    # #     levels = ['class']
    #     for gene in genes_arr:
    # #         print gene
    # #         outfile=work_dir+'db/cpr/'+gene+'.db'
    # #         with open(outfile,'w') as out:
    # #             for level in levels:
    # #                 file = work_dir+'db/'+level+'/'+gene+'.db'
    # #                 with open (file,'r') as infile:
    # #                     out.write(infile.read())
    # #                     print infile
    # #         os.system('hmmpress -f '+outfile)
    #
    #     levels=['root']
    #     print levels
    # #     print '!!!!!!!!!!'
    #     genes_arr =["cox3","atp6","nad3","nad4l","nad4","nad5","nad6","cob","nad1","nad2","cox2","atp8","cox1"]
    # # #     genes_arr=['nad3']
    #     for level in levels:
    #         for gene in genes_arr:
    #             models=get_level_models(f,t,gene,level)
    # #             models=glob.glob(work_dir+'clear_hm/'+level+'/'+gene+'/*.hm')
    # #                 print type(models),"models"
    # #             print len(models)
    # #     #             print models
    #             dbdir =work_dir+'db-test/'+level+'/'
    #             if not os.path.exists(dbdir):
    #                 os.makedirs(dbdir)
    #             with open (dbdir+gene+'.db','w') as outfile:
    #                 for mod in models:
    # #                     print mod
    #                     with open (mod,'r') as infile:
    #                         outfile.write(infile.read())
    #             db=dbdir+gene+'.db'
    #             os.system('hmmpress -f '+db)
    # # #
    #
    #     pool =mp.Pool(16)
    # #     print genes_arr
    #     phyla,uniq=load_phyla(gb_files)
    #     genes_arr=['cox2','cox1']
    #     genes_arr = ['atp8','atp6','nad1']
    #     genes_arr =['nad2', 'cox3']
    #     genes_arr = ['nad3','nad4']
    #     genes_arr = ['cob','nad5']
    #     genes_arr = ['nad4l','nad6']
    #     genes_arr = ['nad5']
    #     genes_arr =['cox1']

    #     for level in ['species']:
    # # #
    #         for gene in genes_arr:
    #             print gene
    #             db = work_dir+'dblevel/'+level+'/'+gene+'.db'
    # # #             db=work_dir+'badseq/fasta/bad/NoName_'+gene+'.fas'+gene+'-re.hm'
    # # #             db=work_dir+'trimcol/'+level+'/NoName_'+gene+'-fs.hm'
    # # #             db=work_dir+'badseq/fasta/badfs/NoName_nad5-fs.fasnad5-re.hm'
    # # #             db='/homes/brauerei2/marwa/phd/tool/mtdb/data/trees_and_data/db-test/root/cob.db'
    # # #             db=work_dir+'badseq/fasta/fs/NoName_'+gene+'-fs.fas'+gene+'-re.hm'
    # #             db=work_dir+'maftal/maft-default/'+gene+'.fas.hm'
    # # #             db=work_dir+'uppal/'+gene+'.hm'
    # #             if os.path.exists(db):
    # #                 print gene
    #             for p in uniq:
    #                 for seqfile in glob.glob(work_dir+"prot6frames-test/"+p+"/*.fas"):
    # #                     print seqfile
    # #                     print os.path.dirname(seqfile)+'/'+level+'/leveldb/'+gene+'/outscore/'+os.path.basename(seqfile).split('.')[0]+'.out'
    #                     if  not os.path.exists(os.path.dirname(seqfile)+'/'+level+'/leveldb/'+gene+'/outscore/'+os.path.basename(seqfile).split('.')[0]+'.out'):
    #                         print seqfile
    #                         hmmscan_call(seqfile,gene,db,level)
    #     #                         hmmscan_call(seqfile,gene,work_dir+'maftal/maft-default/'+gene+'.fas.hm',level)
    #                         pool.apply_async(hmmscan_call, args=(seqfile, gene, db,level))
    #
    #     pool.close()
    #     pool.join()
    #
    #
    bed()
    #                                 real    49m26.179#     print n.get_children()[0].name
    #     print n.get_children()[1].names
    #                                 user    139m20.458s
    #                                 sys    22m58.488s

    #               wiith --max       real    168m36.664s
    #                                 user    620m57.972s
    #                                 sys     27m44.387s

    # -------------------merge frames---------------------

    #     import math
    #     levels=['phylum','root','class']
    # #     levels=['cpr']
    #     print 'iiiiiii'
    #     done=[]
    #     for f in os.listdir(work_dir+'prot6frames-test/bedphylum/01merge/testorder'):
    #         acc=f.split('.')[0]
    #         done.append(acc)
    #     genes_arr =["cox3","atp6","nad3","nad4l","nad4","nad5","nad6","cob","nad1","nad2","cox2","atp8","cox1"]
    # # #

    # # #

    # # TODO fixed list is messing
    #       fixed list is messing
    #                     real    98m35.018s
    #                     user    33m7.708s
    #                     sys     21m59.978s

    # #     cap,cup=f1.capcup(f2,"circular",50)

    # ToDo
    # create a db for the 3 levels
    # hmmscan
    # mergel28
    # -----------------------number of sequences with no hits----------------------
    #     dir1 = out_models
    #     dir2 = outp_dir+'/gm-refseq63-test/'
    #     d = work_dir+'prot6frames-test/'
    #     for gene in ["atp8","cox1"]:
    #         modcount= get_models_count(dir1,dir2,gene)
    #         hitcount=get_hits_count(d,gene,modcount)
    #         abs=sum(hitcount)/float(modcount)
    #         abs=abs/len(hitcount)
    #         print abs
    # 0.407144995509
    # 0.98988810519
    # ###----Run hmmscan------

    #     genes_arr=["atp8","cox1"]
    #     for gene in genes_arr:
    #         for

    #         if os.path.isfile (resul_HMM_refseq63/ + gene +nd.nam...)

    # #     path1="/homes/brauerei2/marwa/phd/tool/mtdb/data/trees_and_data/result_HMM_refseq63/*.hm"
    # #     path2="/homes/brauerei2/marwa/phd/tool/mtdb/data/trees_and_data/result_HMM_refseq63/"
    # #
    # #     l=glob.glob(path1)
    # #     for f in l :
    # #         if os.path.isfile(os.path.join(path2,f)):
    # #             file = path2+f
    # #             name=os.path.basename(file)
    # #             node = name.split('_cox1')[0]
    # #             print node,
    # #             n= t&node
    # #             n.arr['cox1']['model']=name
    #

    #                 l.append(path+i)
    # #
    #     t= Tree(tree_file,format=8)
    #     n=t&'132587'
    #     while n.up:
    #         n=n.up
    #         print n.name
    #     n = t&'6103'
    #     print n.get_children()[0].name, n.get_children()[1].name
    #

    # # # # #

    # 2 dimensional dictionnary to send all genes data to getsequneces (convert dict)
    # #
    #     t=intialize_non_leaves_g(t,taxidmap_file)
    # #     node= t.search_nodes(name='7729')[0]
    # #     node.detach()
    # #     node= t.search_nodes(name='10224')[0]
    # #     node.detach()
    # #     genes_arr =["atp6","cox3","nad3","nad4l","nad4","nad5","nad6","cob","nad1","nad2","heg","mttb","msh1","atp9","cox2"]
    # #     #"cox1,atp8"
    # #     for g in genes_arr:
    # #         print g
    # #         gene_sequences=load_sequences(g)
    # #         print "convert_dict_g"
    # #         dict_data = convert_dict_g(data_gene,gene_sequences,taxidmap_file)
    # # #     sys.stderr.write("TREE\n")
    # # #
    # #
    #     dict_data = convert_dict_g(data_gene,atp8_sequences,taxidmap_file)
    #     t=ini'nad6'tialize_leaves(t, dict_data,args.outdir)
    #     aff_seq_all(t.get_tree_root(),'atp8')
    # #     nd=t.get_tree_root()#     keys = data_gene.keys()
    # # #     print len(keys)
    #     from subprocess import Popen, PIPE
    #     cmd = "awk '{print $5}' /homes/brauerei2/marwa/phd/tool/mtdb/data/trees_and_data/prot6frames-test/all-cox1-deltas.data | uniq"
    #     p = Popen(cmd, stdout=PIPE, stderr=PIPE,shell=True)
    #     stdout, stderr = p.communicate()
    #     l = stdout.split()
    #
    #     for i in range(len(l)):
    #         l[i]=l[i].split('-')[0]
    #
    #     temp = [item for item in keys if item not in l]
    # # # # #     nd = t.search_nodes(name="337677")[0]
    # # # #
    #
    # #     print t.get_ascii(show_internal=True)
    #         nd = t.get_tree_root()
    #         sys.stderr.write("AFF SEQ\n")
    #
    #         aff_seq_all(nd,g)
    #         sys.stderr.write("COMPUTE MODELS\n")
    #        l
    #         computeModels(nd,g)

    #     print dict_data[get_Nc(taxidmap_file, '13085')]
    #

    # #     #print dict_data['NC_008142']
    # #     #pool = mp.Pool(12)
    # #     #remolding_in_species(pool,dict_data)
    # #     #model_build_trna(pool,data_trna, main_dir)
    # #     #pool.close()
    # #     #pool.join()
    # #
    #     #get_scores_in_species(dict_data)
    #    ------------------build-compute Models---------------------l

    # #       gene
    # #     genes_array = ["trnS1","trnF","trnD","trnY","trnS2","trnL1","trnL2","trnH","trnI","trnM","trnN","trnC","trnE","trnP","trnQ","trnR","trnT","trnW","trnK","trnA","trnG","trnV"]
    #     n=t.get_tree_root()

    #     ##### only for testing ####################
    #     # genes_array = ["trnL1","trnL2"]
    #     for g in genes_array:
    #         for nn in t.traverse():
    #             if not nn.is_leaf():
    #
    #                 nn.arr[g]['model'] = work_dir+'result_CM_refseq56/' + nn.name + '_' + g + '.cm'
    #     genes_array = ["cox1","atp8"]
    #     for g in genes_array:
    #         #init_leafs_seq(t, g)
    #         aff_seq_all(n,g,data_gene)l

    # #     remolding_in_species(t)
    #     for gene in genes_array:
    #         open('ndal.tmp', 'w').close()0,
    #         computeModels(n, gene)
    #
    # #     testfile=open('/homesgene/brauerei/abdullah/Desktop/PhD/python/mtdbnew/src/RNAremold/tRNA-phylo/004/tRNA-CM/data/Higgs2003_Paper_test/remolding/test.txt','w')
    # #     test=remolding_in_tree(t,remolding_cand)
    #     for nd in test.traverse():
    #         #if not nd.is_root():
    #
    #         for model in nd.scores:
    #             for g in nd.scores[model]:
    #                 print nd.name,g,model, nd.scores
    #                 #print model, g
    #                 #        used model    gene aligned on this model    score
    #                 testfile.write(model+"    "+g+"    "+str(nd.scores[model][g]+"\n"))
    #     testfile.close()
    #     tr= Tree(tree_file1,format =8)
    # #     print tr
    #     id = '30591'
    #     node = tr.search_nodes(name=id)[0]
    #     node.delete()
    #    # print tr
    # #     for key in data_gene.keys():
    # #         print key
    #
    #     #print dict_data
    #     tr = intialize_non_leaves_g(tr,taxidmap_file)
    #     tr = initialize_leaves(tr,dict_data,args.outdir,taxidmap_file)

    #     ac =get_Nc(taxidmap_file,'10224')

    #     print t

    #     gene="cox1"
    # mod1="/homes/brauerei2/marwa/phd/gc/RefSeq/outputdir/GM-refseq63/NC_000880/cox1.hmm"

    # os.system('hmmsearch --tblout \"' + mod1 + '\" \"' + out_fasta +nd.name + '_' + gene + '.fas\" > '+ out_stockholm +nd.name + '_' + gene + '_hm_' + nd.get_children()[0].name + '.sto ')
    # os.system('hmmsearch --tblout ' + out_stockholm + nd.name + '_' + gene + '_hm_' + nd.get_children()[0].name + '.sto \"'+ mod1 + '\" \"' + out_fasta +nd.name + '_' + gene + '.fas\" ')

    #
    #     l
    #

    # s    for n in t.traverse(strategy='postorder'):
    #        print n.arr['cox1']['seq']
    # proc = subprocess.Popen(["python /homes/brauerei2/marwa/phd/tool/mtdb/src/getinfo.py "+ gb_files  +"NC_*.gb -f %c"], stdout=subprocess.PIPE, shell=True)
    # (out, err) = proc.communicate()
    # print out

    #     for n in t:
    #         print get_Nc(taxidmap_file,n.name),n.name
    #      gene
    #     prot_seq='MYNNSMKLLFLSSLMMGTYLSISSTPWLGTWMGLEINLLSIIPMLTDNKNSMINEPAIKYFIIQSMASTMLLISILIIQMKYMMWWDNKNIPSMMIMSSMMMKMGAAPFHFWLPEVMSSTSWINCLMLMTWQKIAPMMTMSYCIKMSSFLFVVIMMGIIVGAMGGLNQTSLRQILAYSSISHLGWMISSMTISENTWEFYFLIYSTLNVIIIFMFKTMNLFFLNQIYSASYFKTEIKFMMMTSLLSLGGLPPMLGFLPKWIVMQSLIDNKMTALVLLMITFTTITLYYYMRISFSAIIMLHNENSWLTSIKMNKLVVALPILSMISTMGLICTSNFMLLLSSTQKWLFSTNHKDIGTLYFMFGAWAGMVGTSMSMIIRAELGQPGTMINDDQLYNVIITAHAFVMIFFMVMPIMIGGFGNWLVPLMIGAPDMAFPRMNNMSFWLLPPSLTLLLMSSVVDNGAGTGWTVYPPLASVIAHSGASVDLAIFSLHLAGVSSILGAINFITTAINMRSNNMTLDQTPLFVWSVAITALLLLLSLPVLAGAITMLLTDRNLNTSFFDPAGGGDPILYQHLFWFFGHPEVYILILPGFGIISHIVCQESGKIESFGTIGMIYAMLSIGLMGFIVWAHHMFTVGMDVDTRAYFTSATMIIAVPTGIKVFSWMATLYGTKFKFNPPLLWALGFIFLFTMGGLTGLVLANSSLDIVLHDTYYVVAHFHYVLSMGAVFAIMGGIIQWYPLFTGLTMNSKWLKIQFTIMFIGVNLTFFPQHFLGLAGMPRRYSDYPDAYTSWNVISSIGSTISITGIIMFILIMWESMIKQRNVFIWTNMSSSTEWLQNNPPAEHSYSELPLMATWSNLSLQDGASPLMEQLSFFHDHTMIDLLLITMIVGYSLSYMLLTKYTNRNMLHGHLIETIWTALPAITLIFIALPSLRLLYLLDDSSDAMITIKTIGRQWYWSYEYSDFINVEFDTYMTPENELNTDEFRLLEVDNRTTLPMNTEVRVLTSASDVLHSWAVPALVLKIDATPGRLNQGMFMINRPGLFFGQCSEICGANHSFMPIVIESTSIKLFIKWLSNMMINLMMTNLFSTFDPSTNLFNLSLNWTSTFLGLLLIPSMFWLMPSRINILWNKMNLNLHNEFKTLLGKNSFQGSTLILISIFIMMLFNNFMGLFPYIFTSTSHMTLTFSIALPMWMSFMLFGWINNTNHMFTHLVPQGTPNALMSFMVLIETISNVIRPGTLAVRLAANMIAGHLLLTLLGNTGPSLTTSIMLFLIIGQMLLLILESAVAMIQAYVFSILSTLYSSEVYMLTNNNNHPFHMVDYSPWPLTGAIGAMILTSGMTKWFHTFNMNLLMIGMTVIVLTMIQWWRDVVREGTFQGLHTKLVSKGLRWGMILFIASEVLFFASFFWAFFNSSLAPTIELGMKWPPMGIQPFNPIQIPLLNTAILLASGVTITWAHHSIMECNHSQALQGLFFTVMLGFYFTLLQMYEYWEAPFTIADAVYGSTFFVATGFHGLHVIIGTTFLLTCLIRHMMNQFSSNHHFGFEAAAWYWHFVDVVWLFLYLSIYWWGSICSLSFFFLFLFSTLFFILGIYYLMIDYSLFIEWELFSLNSSMVVMTFIIDWMSLVFMSFVMYISSLVIYYSNDYMHNEKNINRFIMIVLMFILSMAFLIISPNLISILLGWDGLGLVSYCLVIYYQNVKSYNAGMLTALSNRIGDVAILISISWMLNFGSWNYIYYYYFISDSFEMKIITLLIILAAMTKSAQIPFSSWLPAAMAAPTPVSALVHSSTLVTAGVYLLIRFNPMLMVYDFGWYILFIGCLTMFMSGLGANFEFDLKKIIALSTLSQLGLMMSILSMGYSDLAFFHLLTHALFKALLFMCAGSMIHNLRDSQDIRFMGSIIHFMPLTSICFNVSSLCLCGMPFLAGFYSKDLILEIVCLSWVNFFIFFLYFFSTGLTASYSFRLFYYSMSGDNNYYSSYSFNDSSYFISFGMIGLLIVAVFGGSLLSWLIFPVPYLVVLPWYLKFLTLLTIILGSYFGYVISDFVYSYELFSLNFLSFVMFTGSMWFMPFLSTNYVSYLPLSFGYYSLKSFDSGWGELLGGQGLYSFFVYLINYIQSLYDSNFKVYLLTFVFWMFILFVLFFL'
    #     with open('/homes/brauerei2/marwa/phd/tool/mtdb/data/trees_and_data/result_HMM_refseq63/prot.fas','w') as prot:
    #         prot.write(prot_seq)

    #     dna =SeqIO.read('/homes/brauerei2/marwa/phd/gc/RefSeq/refseq63-fasta/NC_000844.fas', 'fasta')
    #     d= dna.Seq.translate(table =5)
    #     print d
    #     coding_dna = Seq("ATGGCCATTGTAATGGGCCGCTGAAAGGGTGCCCGATAG", generic_dna)
    #     t= coding_dna.translate()
    #     print t
    # #
    #     for ac in l:
    #         for seq_record in SeqIO.parse("/homes/brauerei2/marwa/phd/gc/RefSeq/refseq63-fasta/"+ac+".fas", "fasta"):
    #             seq =seq_record.seql
    # #         print seq
    #         t = seq.translate(table =24)
    #         with open('/homes/brauerei2/marwa/phd/tool/mtdb/data/trees_and_data/result_HMM_refseq63/'+ac+'.fas','w') as prot:
    # #             prot.write('>'+ac+'\n')
    # #             prot.write(str(t))
    #             print t

    # Hmm Scan Begin

    #
    #     dbfile='/homes/brauerei2/marwa/phd/tool/mtdb/src/cox1db.db'
    # # # #     list =['NC_001712','NC_000844','NC_001708','NC_001573','NC_001606','NC_003136','NC_002012','NC_000834','NC_001887','NC_001572','NC_001627']
    #     list =['NC_001712']
    # #     list = ['NC_012920']
    #     for ac in list:
    #         seq = SeqIO.read("/homes/brauerei2/marwa/phd/gc/RefSeq/refseq63-fasta/"+ac+".fas", "fasta")
    #         seq=seq.seq
    #         #get_transtable()
    #         gbfile =gb_files + ac +".gb"
    #         transl_table= get_transtable(gbfile)
    #         print "trans table is :", transl_table
    #         l = trans_six_frames(seq,transl_table)
    #         for orf in enumerate(l):
    #             file = '/homes/brauerei2/marwa/phd/tool/mtdb/data/trees_and_data/prot6frames/'+ac+'-'+str(orf[0])+'.fas'
    #             with open (file,'w') as prot:
    #                 prot.write('>'+ac+'-'+str(orf[0])+'\n')
    #                 prot.write(str(orf[1]))
    #             os.system('hmmscan --noali --notextw --tblout  '+file+'.out ' +dbfile + ' '+ file)
    # #     os.system('hmmscan --tblout /homes/brauerei2/marwa/phd/tool/mtdb/data/trees_and_data/prot6frames/NC_001712-2.fas.out ' +dbfile + '  /homes/brauerei2/marwa/phd/tool/mtdb/data/trees_and_data/prot6frames/NC_001712-2.fas')
    #     os.system('hmmscan --tblout /homes/brauerei2/marwa/phd/tool/mtdb/data/trees_and_data/prot6frames/NC_001712-2.fas.out ' +dbfile + '  /homes/brauerei2/marwa/phd/tool/mtdb/data/trees_and_data/prot6frames/NC_001712-2.fas')

    # # #     print get_id(taxidmgeneap_file,'NC_001712')
    #     start=time.time()
    #     root = t.get_tree_root()
    #     model=d[root.name]
    #     os.system('hmmpress ' +model)
    #     dbfile =model
    #     os.system('hmmscan --tblout /homes/brauerei2/marwa/phd/tool/mtdb/data/trees_and_data/prot6frames/NC_001712-2.fas.out ' +dbfile + '  /homes/brauerei2/marwa/phd/tool/mtdb/data/trees_and_data/prot6frames/NC_001712-2.fas')
    # #

    #    l

    #     for n in t:
    #         print n.name
    #         print n.arr['cox1']['model']
    #     get_sequence_PCgenes('NC_002177','cox1',fasta_files_dir,data_gene)
    #     with open ('mod.out','w') as modfile:
    # # #
    #         for n in t.traverse(strategy='postorder'):
    #             modfile.write(n.name)
    #             modfile.write(":")
    #             modfile.write(str(get_model(n)))
    #             modfile.write('\n')
    #     start2= time.time()lgene
    #
    #     modfile='mod.out'
    #     scanfile='scan-all-0.out'
    #     l= get_non_sigmodels(modfile,scanfile)
    #     sys.stderr.write("load data\n")
    #     with open ('sig.txt','w')as f:
    #         for e in l:
    #         print e
    #         if not e=='' and not e=='160206':
    #             if t&#     keys = data_gene.keys()
    # # #     print len(keys)
    #     from subprocess import Popen, PIPE
    #     cmd = "awk '{print $5}' /homes/brauerei2/marwa/phd/tool/mtdb/data/trees_and_data/prot6frames-test/all-cox1-deltas.data | uniq"
    #     p = Popen(cmd, stdout=PIPE, stderr=PIPE,shell=True)
    #     stdout, stderr = p.communicate()
    #     l = stdout.split()
    #
    #     for i in range(len(l)):
    #         l[i]=l[i].split('-')[0]
    #
    #     temp = [item for item in keys if item not in l]e :
    #                n=t&e
    #                     size=len(n.get_leaves())
    #                  #     keys = data_gene.keys()
    # # #     print len(keys)
    #     from subprocess import Popen, PIPE
    #     cmd = "awk '{print $5}' /homes/brauerei2/marwa/phd/tool/mtdb/data/trees_and_data/prot6frames-test/all-cox1-deltas.data | uniq"
    #     p = Popen(cmd, stdout=PIPE, stderr=PIPE,shell=True)
    #     stdout, stderr = p.communicate()
    #     l = stdout.split()
    #
    #     for i in range(len(l)):
    #         l[i]=l[i].split('-')[0]
    #
    #     temp = [item for item in keys if item not in l]   f.write(e)l
    #                 f.write('  ')
    #                 f.write(str(size))
    #                 f.write("\n")
    #
    #

    #

    # #########################################################
    # ########################change stockholm names##########################
    #     for dir in os.listdir('/homes/brauerei2/marwa/phd/gc/RefSeq/outputdir/stockholm_files/'):
    #         id =get_id(taxidmap_file,dir)
    #         l=[]
    #         path='/homes/brauerei2/marwa/phd/gc/RefSeq/outputdir/stockholm_files/'+ dir+'/*.sto'
    #
    #         l= glob.glob(path)
    #         for file in l:
    #             newfile=os.path.splitext(file)[0]+'-'+id+'.sto'
    #             os.system('mv '+file +' '+newfile)l

    # ########################################################################
    #     print "aaaaaaaaaaaaaaaaaaaa"
    #     with open('file1.out','a') as outfile:
    # #         print "fffffffffff"
    #         rec(nd,outfile)
    #         outfile.close()
    # # #         print#     keys = data_gene.keys()
    # # #     print len(keys)
    #     from subprocess import Popen, PIPE
    #     cmd = "awk '{print $5}' /homes/brauerei2/marwa/phd/tool/mtdb/data/trees_and_data/prot6frames-test/all-cox1-deltas.data | uniq"
    #     p = Popen(cmd, stdout=PIPE, stderr=PIPE,shell=True)
    #     stdout, stderr = p.communicate()
    #     l = stdout.split()
    #
    #     for i in range(len(l)):
    #         l[i]=l[i].split('-')[0]
    #
    #     temp = [item for item in keys if item not in l] get_model('7850')
    #     os.system('hmmscan --noali --notextw -o scan-all-atp8.out --tblout scan-all-atp8-0.out --domtblout scan-all-atp8-1.out atp8db.db  /homes/brauerei2/marwa/phd/tool/mtdb/data/trees_and_data/prot6frames/NC_001712-2.fas')
    #     os.system('hmmscan --noali --notextw -o scan-all-atp8-human.out --tblout scan-all-atp8-0-human.out --domtblout scan-all-atp8-1-human.out atp8db.db  /homes/brauerei2/marwa/phd/tool/mtdb/data/trees_and_data/prot6frames/NC_012920-4.fas')

    #     write = open ('shifted-human.out','w')
    #     with open ('scan-all-1-human.out') as readfile:
    #         for line in readfile:
    #             if not line.startswith('#'):
    #                 tmp=line.split()
    #                 if int(tmp[15])>20:
    #                     write.write(tmp[0])
    #                     write.write('  ')
    #                     write.write(tmp[15])
    #                     write.write('  ')
    #                     write.write(tmp[16])
    #                     write.write('\n')
    #         write.close0,()
    #     l=[]
    #     with open ('shifted-human.out','r') as shifted:
    #         for line in shifted:
    #
    #             l.append(line.split()[0].split('_cox1')[0])
    #     with open ('ornament-human.map','w') as style:
    #         style.write('"<circle style=\'fill:blue;stroke:black\' r=\'7\'/>" I 9606')
    #         style.write('\n')
    #
    #         style.write('"<circle style=\'fill:red;stroke:black\' r=\'5l\'/>" I')
    #         for e in l:
    #            gene
    #             style.write(' '+e)

    #     print get_id(taxidmap_file,'NC_001712')

    #     n= t.search_nodes(name='6072')
    #     print n[1].get_ascii(show_internal=True)

    #     for dir in os.listdir('/homes/brauerei2/marwa/phd/gc/RefSeq/outputdir/stockholm_files'):
    #         path = '/homes/brauerei2/marwa/phd/gc/RefSeq/outputdir/stoclkholm_files/'+dir+'/'
    # # #         print path
    # # #         print dir
    # # #         print path
    #         for file in os.listdir(path):l
    # #             print datetime.datetime.strptime(time.ctime(os.path.getmtime(path+file)), "%a %b %d %H:%M:%S %Y")
    #
    # #             print "a"
    #             if  time.ctime(os.path.getmtime(path+file))!=datetime.date.today():
    #
    #                 os.remove(path+file)
    #                 print file

    # ###############################R Statistics########################################
    #     with open ('scan-all-1-human.out', 'r') as scandata:
    #         with open ('shift-human.data','w') as shiftdata:#     sys.stderr.write("load data\n")
    #             shiftdata.write('node  hfrom  hto    afrom  ato\n')
    #             for line in scandata:
    #                 if not line.startswith('#'):
    #                   #     keys = data_gene.keys()
    # # #     print len(keys)
    #     from subprocess import Popen, PIPE
    #     cmd = "awk '{print $5}' /homes/brauerei2/marwa/phd/tool/mtdb/data/trees_and_data/prot6frames-test/all-cox1-deltas.data | uniq"
    #     p = Popen(cmd, stdout=PIPE, stderr=PIPE,shell=True)
    #     stdout, stderr = p.communicate()
    #     l = stdout.split()
    #
    #     for i in range(len(l)):
    #         l[i]=l[i].split('-')[0]
    #
    #     temp = [item for item in keys if item not in l]  tmp=line.split()
    #                     if int(tmp[15])>20:
    #                         shiftdata.write(tmp[0])
    #                         shiftdata.write('  ')
    #                         shiftdata.write(tmp[15])
    #                         shiftdata.write('  ')
    #                         shigeneftdata.write(tmp[16])
    #                         shiftdata.write('  ')
    #                         shiftdata.write(tmp[17])
    #                         shiftdata.write('  ')
    #                         shiftdata.write(tmp[18])
    #                         shiftdata.write('\n')

    #     with open ('scan-all-atp8-1.out', 'r') as scandata:
    #         with open ('atp8.data','w') as shiftdata:
    #             shiftdata.write('id node  hfrom  hto    afrom  ato\n')
    #             i=1
    #             for line in scandata:
    #
    #                 if not line.startswith('#'):
    #                     tmp=line.split()
    #                     shiftdata.write(str(i))#     sys.stderr.write("load data\n")
    #                     shiftdata.write('  ')
    #
    #                     shiftdata.write(tmp[0])
    #                     shiftdata.write('  ')
    #                     shiftdata.write(tmp[15])
    #                     shiftdata.write('  ')
    #                     shiftdata.write(tmp[16])
    #                     shiftdata.write('  ')
    #                     shiftdata.write(tmp[17])
    #                     shiftdageneta.write('  ')
    #                     shiftdata.write(tmp[18])
    #                     shiftdata.write('\n')
    #                     i=i+1

    #     with open('shift.data', 'r') as sh:
    #         with open('shift2.data', 'w') as sh2:
    #             for line in sh:
    #                 if line.startswith('id'):
    #                    0, sh2.write(line)
    #                 else:
    #                     tmp = line.split();
    #                     nd= tmp[1].split('_cox1')[0]
    #                     sh2.write(tmp[0]+'  '+ nd + '  '+ tmp[2]+ '  '+tmp[3]+'  '+tmp[4]+'  '+ tmp[5]+ '\n')

    #
    #     print get_Nc(taxidmap_file,'1267413')
    #     print get_Nc(taxidmap_file,'150436')
    #     acc= get_Nc(taxidmap_file,'84350')
    #     print get_sequence_PCgenes(acc,'cox1')#     sys.stderr.write("load data\n")

    #     model= get_model (t&'6072')
    #     hmmscan_call(model,'6072')

    #     print get_Nc(taxidmap_file,'72672')

    #     print get_sequence_PCgenes('NC_020025','cox1',fasta_files_dir,data_gene)
    #     print get_sequence_PCgenes('NC_017868','cox1',fasta_files_dir,data_gene)

    #     print end-start2
    #     print get_Nc(taxidmap_file,'10195')
    #     print end -start2
    #     id =get_id(taxidmap_file,'NC_010232')
    #     node= t.search_nodes(name=id)[0]
    #     computeModels(node, 'cox1')
    #     print get_sequence_PCgenes('NC_010232','cox1',fasta_files_dir,data_gene)

    #     hmmbuild_call(outp_dir,'NC_010232','cox1')

    #     for file in os.listdir('/homes/brauerei2/marwa/phd/tool/mtdb/data/trees_and_data/fasta_files/atp8/'):

    #     l=[]
    #     for file in os.listdir('/homes/brauerei2/marwa/phd/tool/mtdb/data/trees_and_data/fasta_files/atp8/'):
    #         if os.path.getsize('/homes/brauerei2/marwa/phd/tool/mtdb/data/trees_and_data/fasta_files/atp8/'+file) ==0:
    #             node = file.split('_atp8')[0]
    #             n= t.search_nodes(name=node)[0]
    #             if not n.is_leaf():
    #                 for leaf in n.get_leaves():
    #                     if found(get_Nc(taxidmap_file,leaf.name),'atp8.fas'):
    #                         if not leaf.name in l:
    #                             l.append(leaf.name)
    #
    #     for e in l:
    #         print e, get_Nc(taxidmap_file,e)
    #     print len(l)
    #     fpos = 'NC_016056-2.fas-cox1-pos.out'
    #     l=len(SeqIO.read(fasta_files_dir+"NC_002779.fas", "fasta").seq)
    #     with open(work_dir+'prot6frames-test/Ecdysozoa/'+fpos,'r')as fp:
    #         nuc_s=-0.99
    #         for line in fp:
    #             if not line.startswith('#'):
    #                 s=line.split()[17]
    #                 end=int(line.split()[18])
    #
    #                 nuc= get_nuc_pos('NC_002779-4.fas-cox1-pos.out',s,end,l)
    #                 print s,end,nuc,l
    end = time.time()
    #     n = t&'32523't
    #     print n.get_ascii(show_internal =True)
    print(end - start)
#     print load_features('NC_000860')

# ###find files with no root hit #############

#     keys = data_gene.keys()
# # #     print len(keys)
#     from subprocess import Popen, PIPE
#     cmd = "awk '{print $5}' /homes/brauerei2/marwa/phd/tool/mtdb/data/trees_and_data/prot6frames-test/all-cox1-deltas.data | uniq"
#     p = Popen(cmd, stdout=PIPE, stderr=PIPE,shell=True)
#     stdout, stderr = p.communicate()
#     l = stdout.split()
#
#     for i in range(len(l)):
#         l[i]=l[i].split('-')[0]
#
#     temp = [item for item in keys if item not in l]
#     print temp
#     print t&'104431'
#     print t&'INT_4929'

# seq = SeqIO.read(fasta_files_dir+"NC_003367.fas", "fasta")
# seq=seq.seq
# l_genome=len(seq)
# n=t&'104431'
# print get_b_s(n.up.name,'NC_003367-2.fas-cox1-pos.out','Ecdysozoa',1142,l_genome)
# print get_b_s('104431','NC_003367-2.fas-cox1-pos.out','Ecdysozoa',1142,l_genome)

# print (t&"INT_17").get_ascii(show_internal =True)

# ['NC_017612', 'NC_000931', 'NC_022847', 'NC_012899', 'NC_018344', 'NC_015091', 'NC_020311']

#     with open(work_dir+ "prot6frames-test/Chordata/NC_015238-3.fas-atp8-pos.out") as inf:
#         data = []
#         for line in inf:
#             line = line.split()
#             if len(line)==23:
#                 data.append(line)
#     with open(work_dir+ "prot6frames-test/Chordata/NC_015238-0.fas-atp8-pos.out") as inf:
#         for line in inf:
#             line = line.split()
#             if len(line)==23:
#                 data.append(line)
#     f_h = file('sorted.dat','a')
#     m = sorted(data, key=lambda k: float(k[6]))
#
#     numpy.savetxt(f_h, m, fmt='%s', delimiter='    ')
#     f_h.close()
#     table = [[0,14,0.3],[0,14,0.2],[0.002,14,0],[0.003,13,0.1],[0.006,12,0.5],[0.007,13,0.6]]
#     n=sorted(table, key=lambda k:int(k[1]), reverse =True)
#     print n
#     m =sorted(n, key=lambda k: float(k[0]))
#     print m
#     maximum = max(table, key=lambda k:k[1])
#     print maximum
#     minimum = min(table, key=lambda k:k[0])
#     print minimum,table.index(minimum)
#     min2= min(table, key=lambda k:k[2])
#     print min2
#     ind=[]
#     for x in table:
#         if x[0]==minimum[0]:
#             ind.append(table.index(x))
#     print ind
#     print get_b_s('6213','/homes/brauerei2/marwa/phd/tool/mtdb/data/trees_and_data/prot6frames-test/Platyhelminthes/NC_021145-merged.out','Platyhelminthes',0,16700)
#     with open(work_dir+'prot6frames-test/debuging-cox1.out','r') as f :
#         for line in f:
#             if not line.startswith('#'):
#                 n= (line.split()[0]).split('_cox1')[0]
#                 print n
#                 n= t&n
#                 with open(work_dir+'prot6frames-test/debuging-cox1.out','a') as f2 :
#                     f2.write('#')
#                     f2.write(str(get_path(n,t)))
#                     f2.write('\n')
#

# --------------generate metazoa map---------------
#     map=[]
#     with open ('metazoa-69.map','a') as map:
#         for file in glob.glob(outp_dir+'refseq69-gb-test-all/*.gb'):
#             print os.path.basename(file),
#             fh= open(file)
#             for gb_record in SeqIO.parse(fh,'genbank'):
#                 acc = gb_record.annotations['accessions'][0]
#                 organism = gb_record.annotations['organism']
#                 tax_line = (" ").join(gb_record.annotations['taxonomy'])
#
#                 line= acc+' '+ tax_line
#                 map.write(str(line)+'\n')
# #

# -----------copy random files-----------
#     for f in glob.glob('/homes/brauerei2/marwa/phd/gc/RefSeq/refseq63-gb-train/*'):
#         b = os.path.basename(f)
#         if os.path.exists('/homes/brauerei2/marwa/phd/gc/RefSeq/refseq63-gb-test/'+b):
#             print b
#             os.system('rm '+f)
#         shuf -zen200 source/* | xargs -0 cp -t dest

#     al=align [:,:i-1]+align[:,i:]
#     print len(al[0]),len(align[0]),

#     align=al
#     nd=t&'8504'
#     print nd.get_children()[0].name,nd.get_children()[1].name

#     cmd='/opt/bin/hmmalign --mapali  ' + findSTH('8509') + ' -o testnd5.sto ' + work_dir+'result_HMM_refseq63/nad5/8509_nad5.hm' + ' ' +work_dir+'fasta_files/'+ nd.get_children()[1].name + '_' + 'nad5' + '.fas '
#     print cmd
#     print nd.up.get_ascii(show_internal=True)

#     for qresult in SearchIO.parse('test2.out', 'hmmer2-text'):
#         print qresult.id

# print get_Nc(taxidmap_file,'486152')
