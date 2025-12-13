import argparse
import ast
import logging
import os
import pickle
import random
import re
import sys

from Bio import AlignIO, SeqIO
from Bio.Align.Applications import ClustalwCommandline
from ete2 import Tree

from mitos import mitofile
from mitos.sequence import sequence

####
# - Tree taken from : http://itol.embl.de/ncbi_tree_generator.cgi


# ##
# Office:
# ---------
taxidmap_file = "/homes/brauerei/abdullah/Desktop/PhD/python/mtdbnew/src/RNAremold/tRNA-phylo/004/tRNA-CM/RefSeq/new_taxidtoacc-refseq63.txt"

# tree_file = sys.argv[2]
# work_dir = sys.argv[2]
tree_file = "/homes/brauerei/abdullah/Desktop/PhD/python/mtdbnew/src/RNAremold/tRNA-phylo/004/tRNA-CM/data/Metazoa/Metazoa_mitochondrial_tree.nw"

fasta_files_dir = "/homes/brauerei/abdullah/Desktop/PhD/python/mtdbnew/src/RNAremold/tRNA-phylo/004/tRNA-CM/RefSeq/refseq63-fasta/"


# work_dir = "/homes/brauerei/abdullah/Desktop/PhD/python/mtdbnew/src/RNAremold/tRNA-phylo/004/Tree_Conversion/"
work_dir = "/scratch/abdullah/data/Metazoa/"
outp_dir = "/homes/brauerei/abdullah/Desktop/PhD/python/mtdbnew/src/RNAremold/tRNA-phylo/004/tRNA-CM/data/Metazoa/"


# MAC
# -------

# taxidmap_file = "/Users/Abdullah/Documents/PhD/work/Others/mtdb/src/RNAremold/tRNA-phylo/004/tRNA-CM/taxidtoacc-refseq58.txt"

# tree_file = "/Users/Abdullah/Documents/PhD/work/Others/mtdb/src/RNAremold/tRNA-phylo/004/tRNA-CM/Acariformes/Chelicerata.nw"

# fasta_files_dir = "/Users/Abdullah/Documents/PhD/scripts/mtDNA20121205_refseq56/metazoa/"

# work_dir = "/Users/Abdullah/Documents/PhD/work/Others/mtdb/src/RNAremold/tRNA-phylo/004/tRNA-CM/Acariformes/"
# def find_id(tax_file,id):
#
#     f= open(tax_file)
#     s = open(tax_file).read()
#     id='^%s'%id+'\s'
#     if re.search(id,s,re.MULTILINE):
#         found= True
#     else:
#         found= False
#     f.close()
#     return found

# def get_Nc(taxf,id):
#     acc=''
#     if find_id(taxf,id):
#         with open(taxf) as f:
#             id='^%s'%id+'\s'
#             for line in f:
#                 if re.search(id,line,re.MULTILINE):
#                     id,acc = line.split()
#
#     return acc


#
# def recursive_bifurcate(nd,dat_gene):
#
#     """
#      just order them by median length i.e nad5, cox1, nad4, cob ... try one after the other .. and take the first that is available in at least one sequence in all subtrees
#
#
#     ### tree bifurcation should be done by taking one sequence from each children, when childrens are subtrees, we take a random sequence from these sequences.
#
#     check for internal nodes with more than 2 children, creates a fasta file with the sequences in the leafs of this internal node then it generates a Stockholm alignment using 'align_generate'.
#     'align_generate' creates an alignment in stockholm alignment which is passed to quicktree call to bifurcate this subtree and output the new subtree of this node in new hampshire format (NH)
#     @param[in] node in the tree
#
#     """
#
#     if nd.is_leaf():
#         return
#
#     elif len(nd.get_children()) > 2:
#         fasta=""
#
#         for chld in nd.get_children():
#
#             if chld.is_leaf():
#
#                 if found_gene(chld.name, "nad5", data_gene) == True:
#                     fasta+=chld.seq
#                 else:
#                     print(nd.name + " does not have nad5 gene")
#                     continue
#             else:
#                 records=SeqIO.parse(work_dir+"fasta_files/"+chld.name+".fas", 'fasta')
#                 record = list(records)[0]
#                 random_seq = record.seq
#                 fasta += "> "+chld.name+"\n"+record.seq+"\n"
#                 recursive_bifurcate(chld, dat_gene)
#
#         if not fasta ==  '':
#
#             #print nd.name
#             fasta_file = open(work_dir+'nad5_fasta_files/' + nd.name + '.fas', 'w')
#             fasta_file.write(str(fasta))
#             fasta_file.close()
#
#
# #             if not os.path.isfile()
#             align_generate(work_dir+'nad5_fasta_files/' + nd.name + '.fas')
#             os.system("quicktree -upgma "+work_dir+'stockholm_alignments/' + nd.name + '.sth > '+work_dir+"Newick_trees/"+nd.name+".nh")
#
#
#     elif nd.is_root() and len(nd.get_children()) <=2:
#         tmpt = t.copy("newick")
#         nlist = []
#         for td in tmpt.traverse():
#             if td.is_root():
#                 for chld in td.get_children():
#                     nlist.append(chld)
#                 tmpt.prune(nlist,"root")
#
#                 tmpt.write(format=8,outfile=work_dir+"Newick_trees/root.nh")
#
#     else:
#         print nd.name
#         if not nd.is_leaf():
#             for ch in nd.get_children():
#                 recursive_bifurcate(ch, dat_gene)
#
#


#
# def bifurcate(t,dat_gene):
#
#     """
#      just order them by median length i.e nad5, cox1, nad4, cob ... try one after the other .. and take the first that is available in at least one sequence in all subtrees
#
#
#     ### tree bifurcation should be done by taking one sequence from each children, when childrens are subtrees, we take a random sequence from these sequences.
#
#     check for internal nodes with more than 2 children, creates a fasta file with the sequences in the leafs of this internal node then it generates a Stockholm alignment using 'align_generate'.
#     'align_generate' creates an alignment in stockholm alignment which is passed to quicktree call to bifurcate this subtree and output the new subtree of this node in new hampshire format (NH)
#     @param[in] node in the tree
#
#     """
#     for nd in t.traverse():
#         if not nd.is_leaf() and len(nd.get_children()) > 2:
#             fasta=""
#
#             for chld in nd.get_children():
#                 #print "!!! WTF", chld.name
#                 if chld.is_leaf():
#
#                     if found_gene(chld.name, "nad5", data_gene) == True:
#                         fasta+=chld.seq
#                     else:
#                         print nd.name + " does not have nad5 gene"
#                         continue
#                 else:
#                     records=SeqIO.parse(work_dir+"fasta_files/"+chld.name+".fas", 'fasta')
#                     record = list(records)[0]
#                     random_seq = record.seq
#                     fasta += "> "+chld.name+"\n"+record.seq+"\n"
#
# #             print "----------------------------"
# #             print nd.name, fasta
# #             print "----------------------------"
#             if not fasta ==  '':
#
#                 #print nd.name
#                 fasta_file = open(work_dir+'nad5_fasta_files/' + nd.name + '.fas', 'w')
#                 fasta_file.write(str(fasta))
#                 fasta_file.close()
#
#                 #print "I'm here yo !!! " + nd.name
#                 #print fasta
#                 align_generate(work_dir+'nad5_fasta_files/' + nd.name + '.fas')
#                 os.system("quicktree -upgma "+work_dir+'stockholm_alignments/' + nd.name + '.sth > '+work_dir+"Newick_trees/"+nd.name+".nh")
# #
#         elif nd.is_root() and len(nd.get_children()) <=2:
#             tmpt = t.copy("newick")
#             nlist = []
#             for td in tmpt.traverse():
#                 if td.is_root():
#                     for chld in td.get_children():
#                         nlist.append(chld)
#                     tmpt.prune(nlist,"root")
#                     #print tmpt.get_ascii(show_internal=True)
#                     tmpt.write(format=8,outfile=work_dir+"Newick_trees/root.nh")
#             #print t
#         else:
#             print nd.name
#             if not nd.is_leaf():
#                 nd.write(format=8,outfile=work_dir+"Newick_trees/"+nd.name+".nh")
#
#             continue
#             #else:
#             #    nd.delete()
#     return t


#
# def quicktree_handle(NH_trees_dir):
#
#     """
#     it replace each internal node with the bifurcated tree generated from quicktree
#     @param[in] directory of NH trees
#
#     """
#
#     nodes_tmp = []
#     all_tree = Tree(os.path.join(NH_trees_dir,"root.nh"))
#     text="INT_"
#     i=0
#     all_tree.get_tree_root().name == "root"
#     #print all_tree
#     for tr in os.listdir(NH_trees_dir):
#         fname, ext = os.path.splitext(tr)
#         for nd in all_tree.traverse():
#             i+=1
#             #if nd.name in nodes_tmp:
#             #    tmp_node.name = text+str(i)
#             #    continue
#             if not nd.is_leaf() and nd.name == "NoName":
#                 nd.name = text+str(i)
#             if nd.name == fname:
#                 #print nd.name
#                 tmp_tree = Tree(os.path.join(NH_trees_dir,nd.name+".nh"))
#                 nd.add_child(tmp_tree)
#              #   tmp_node = nd
#              #   nodes_tmp.append(nd.name)
#             #print nd.name
#
#     return all_tree
#
#


# nodes_tmp = []
def load_data(dirs):
    """ """
    data_trna = {}
    data_gene = {}
    # extract all tRNAs from the MITOS results that have an annotated
    # anticodon (and discard the others) + replace nonstandard bases with
    # random bases(ACGTU)
    for dr in dirs:
        # print dr.split("/")
        # if dr.split("/")[-1] == "NC_023272":
        #    print dr
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

        tmp = [x for x in features if (x.type == "tRNA" and x.anticodon is None)]
        for t in tmp:
            logging.warning("remove degenerated tRNA: %s %s" % (gb.accession, t.name))

        # data_trna[ gb.accession ] = [ x for x in features if ( x.type == "tRNA" and x.anticodon is not None )]
        data_trna[gb.accession] = [x for x in features if (x.type == "tRNA")]
        data_gene[gb.accession] = [x for x in features if (x.type == "gene")]

        for i in range(len(data_trna[gb.accession])):
            while 1:
                r = random.choice(["A", "U", "C", "G"])
                (data_trna[gb.accession][i].sequence, cnt) = re.subn(
                    "[^ACGTU]", r, data_trna[gb.accession][i].sequence, count=1
                )
                if cnt == 0:
                    break
                else:
                    logging.warning("replaced nonstandard base by random: %s" % r)
    return data_trna, data_gene


def find_id(id):

    tax_file = taxidmap_file
    found = False
    # i = 0
    with open(tax_file, "r") as inF:
        for line in inF:
            line = line.split()
            # i+=1
            # print i,line
            #             if id == "1246979":
            #                 print line[0]
            if str(id) == str(line[0]):
                found = True
                break
    return found


def get_Nc(tax_file, id):
    acc = ""
    with open(tax_file, "r") as inFile:
        for line in inFile:
            line = line.split()
            if id == line[0]:
                acc = line[1].strip()
                break
    # print "1",id, acc
    return acc


def missing_leafs():
    ndel = open(outp_dir + "deleted.txt", "r")
    all_deleted = []
    for line in ndel:
        line = line.split("  ")
        lst = ast.literal_eval(line[1])
        for i in range(len(lst)):
            if find_id(lst[i]) is True:
                all_deleted.append(lst[i])
    ndel.close()
    return lst


# ## remove leafs which does not have an accession i.e non-mitochondrial leafs
def remove_leaf_no_acc(t):
    #     not_deleted = open(outp_dir+"not_deleted.txt","w")
    #     deleted = open(outp_dir+"deleted.txt","w")
    for nd in t.traverse("postorder"):
        if find_id(nd.name) is False and nd.is_leaf():

            # deleted.write(str(nd.name)+" "+get_Nc(taxidmap_file,nd.name)+" "+str(nd.get_leaf_names())+"\n")
            nd.delete(prevent_nondicotomic=False)

    #         else:
    #             not_deleted.write(str(nd.name) +" "+get_Nc(taxidmap_file,nd.name) +"\n")
    #
    #     not_deleted.close()
    #     deleted.close()
    return t


#


def convert_dict_PCG(dicti):
    d = {}
    for acc in dicti:
        if acc not in d:
            d[acc] = {}
        for g in range(len(dicti[acc])):
            # print dicti[acc][g].name
            # print dict[acc][g].name
            if dicti[acc][g].name not in d[acc]:
                d[acc][dicti[acc][g].name] = {}
                # anti_codon=str(dicti[acc][g].anticodon).replace('T','U')
            # d[acc][dicti[acc][g].name]['seq']=dicti[acc][g].sequence+anti_codon
            if "start" not in d[acc][dicti[acc][g].name]:
                d[acc][dicti[acc][g].name]["start"] = []

            if "stop" not in d[acc][dicti[acc][g].name]:
                d[acc][dicti[acc][g].name]["stop"] = []

            if "score" not in d[acc][dicti[acc][g].name]:
                d[acc][dicti[acc][g].name]["score"] = []

            d[acc][dicti[acc][g].name]["start"].append(dicti[acc][g].start)
            d[acc][dicti[acc][g].name]["stop"].append(dicti[acc][g].stop)
            d[acc][dicti[acc][g].name]["score"].append(dicti[acc][g].score)
            d[acc][dicti[acc][g].name]["strand"] = dicti[acc][g].strand

    return d


def aff_seq(nd, data_gene):

    if nd.is_leaf():
        if found_gene(nd.name, "nad5", data_gene) is True:
            # if not nd.seq =='':
            fasta = nd.seq
            nd.seq = fasta
            return fasta
        else:
            print("Bleeeeh! " + get_Nc(taxidmap_file, nd.name))
            return ""

    if not nd.is_leaf():
        fasta = ""
        for chld in nd.get_children():

            fasta += aff_seq(chld, data_gene)
            nd.seq = fasta

    seq = open(work_dir + "fasta_files/" + nd.name + ".fas", "w")
    seq.write(fasta)
    seq.close()

    return fasta


def which_gene(t, dat_gene):
    """
    check which gene is available in at least one sequence in all subtree of the metazoan tree. the order of the check should be based on the median of the gene length (genes_stats.pdf)

    # uses data gene before convert                #### we choose nad5
    """
    ofile = open(outp_dir + "summary_tree_genes.txt", "w")
    i = 0
    for nd in t.traverse():
        if not nd.is_leaf() and len(nd.get_children()) > 2:
            # print nd.name
            for chld in nd.get_children():
                if chld.is_leaf():
                    if found_gene(chld.name, "nad5", dat_gene) is True:
                        i = 0
                        break
                    else:
                        i = 1
            if i == 1:
                ofile.write("no nad5 gene in any leaf of subtree " + nd.name + "\n")


def nd_strcut(node):
    """
    get a subtree with only first children of the internal node
    """
    chlds = node.get_children()
    test = "(" + chlds[0].name + "," + chlds[1].name + ")" + node.name + ";"

    return test


def recursive_bifurcate(t, nd, dat_gene):
    """
     just order them by median length i.e nad5, cox1, nad4, cob ... try one after the other .. and take the first that is available in at least one sequence in all subtrees


    ### tree bifurcation should be done by taking one sequence from each children, when childrens are subtrees, we take a random sequence from these sequences.

    check for internal nodes with more than 2 children, creates a fasta file with the sequences in the leafs of this internal node then it generates a Stockholm alignment using 'align_generate'.
    'align_generate' creates an alignment in stockholm alignment which is passed to quicktree call to bifurcate this subtree and output the new subtree of this node in new hampshire format (NH)
    @param[in] node in the tree

    """

    if nd.is_leaf():
        # fasta=nd.seq
        return

    elif len(nd.get_children()) > 2:
        fasta = ""
        print("1    ", nd.name)
        for chld in nd.get_children():

            if chld.is_leaf():

                if found_gene(chld.name, "nad5", data_gene) is True:
                    fasta += chld.seq
                else:
                    # what should we do with the leaf with no nad5 ??
                    print(nd.name + " does not have nad5 gene")
                    continue
            else:

                records = SeqIO.parse(
                    work_dir + "fasta_files/" + chld.name + ".fas", "fasta"
                )
                record = list(records)[0]
                # random_seq = record.seq
                fasta += "> " + chld.name + "\n" + record.seq + "\n"

    else:
        print("2    ", nd.name, nd_strcut(nd))
        tfile = open(work_dir + "Newick_trees/" + nd.name + ".nh", "w")
        tfile.write(nd_strcut(nd))
        tfile.close()
        fasta = ""

    # print nd.name, fasta
    if not fasta == "" and not nd.is_leaf():

        # print nd.name
        fasta_file = open(work_dir + "nad5_fasta_files/" + nd.name + ".fas", "w")
        fasta_file.write(str(fasta))
        fasta_file.close()

        #             if not os.path.isfile()
        align_generate(work_dir + "nad5_fasta_files/" + nd.name + ".fas")
        os.system(
            "quicktree -upgma "
            + work_dir
            + "stockholm_alignments/"
            + nd.name
            + ".sth > "
            + work_dir
            + "Newick_trees/"
            + nd.name
            + ".nh"
        )

    for cld in nd.get_children():
        if not cld.is_leaf():
            recursive_bifurcate(t, cld, dat_gene)


def dict_tree_files(NH_trees_dir):
    """

    put the bifurcated tree files in a dictionary based on the name
    """

    trees_dict = {}
    for tr in os.listdir(NH_trees_dir):
        fname, ext = os.path.splitext(tr)
        if fname not in trees_dict:

            trees_dict[fname] = Tree(os.path.join(NH_trees_dir, fname + ".nh"))

    return trees_dict


def quicktree_handle(nd, trdict):
    """
    it replace each internal node with the bifurcated tree generated from quicktree
    @param[in] directory of NH trees

    """
    nodes_tmp = []
    nodes_tmp.append(nd.name)
    if not nd.is_root():
        if nd.is_leaf():
            if nd.name in trdict:
                nd.add_child(trdict[nd.name])
                for c in nd.get_children():
                    quicktree_handle(c, trdict)
            # else:
            #    quicktree_handle(nd.get_sisters()[0], trdict)

        else:
            for cl in nd.get_children():
                quicktree_handle(cl, trdict)

        # if not nd.get_sisters()[0].name in nodes_tmp:
        #    quicktree_handle(nd.get_sisters()[0], trdict)
    else:
        for cld in nd.get_children():
            quicktree_handle(cld, trdict)


def internal_node_check(some_tree):
    """
    checks if some internal nodes are actually species, and add them to the leafs and replace the name with random name
    @param[in] tree

    """

    for nd in some_tree.traverse():
        if not nd.is_leaf() and find_id(nd.name) is True:
            # print nd.name
            become_root = nd
            nd.add_child(name=nd.name)
            become_root.name = "INT_" + str(become_root.name)

    return some_tree


def remove_strains(some_tree):
    global taxidmap_file
    tax_file = taxidmap_file
    for nd in some_tree.traverse():
        if not nd.is_leaf() and not get_Nc(tax_file, nd.name) == "":
            for chld in nd.get_children():
                nd.remove_child(chld)
    return some_tree


def remove_internals(rnode):
    """
    solve the problem where some internal nodes have only one child
    """
    # print rnode.name

    if len(rnode.get_children()) == 1:
        if not rnode.get_children()[0].is_leaf():
            rnode.get_children()[0].delete(prevent_nondicotomic=False)
            remove_internals(rnode)
        else:
            rnode.delete(prevent_nondicotomic=False)
            return

    if len(rnode.get_children()) > 1:
        for chld in rnode.get_children():
            remove_internals(chld)

    # elif rnode.is_leaf


def align_generate(fasta_file):
    fn = fasta_file.split("/")[-1].split(".")[0]
    # fn,ext = os.path.splitext(fasta_file)
    clustalw_cline = ClustalwCommandline(
        "clustalw2",
        infile=fasta_file,
        outfile=work_dir + "clustal_alignments/" + fn + ".aln",
    )
    clustalw_cline()
    # convert alignment file to stockholm in order to use it with quick tree
    AlignIO.convert(
        work_dir + "clustal_alignments/" + fn + ".aln",
        "clustal",
        work_dir + "stockholm_alignments/" + fn + ".sth",
        "stockholm",
    )


def found_gene(node_id, gene, data):
    # using the dict before convert
    found = False
    accession = get_Nc(taxidmap_file, node_id)
    if accession in data:
        row = data[accession]
        for i in range(len(row)):
            if gene == row[i].name:
                found = True
                break
            else:
                found = False
    return found


def genes_sort_check(data_gene):

    # using the dict after convert

    outfile = open(outp_dir + "genes_length.txt", "w")

    # toignore = ['atp9', 'msh1', 'mttb', 'polB', 'heg']

    j = 0
    for acc in data_gene:
        j += 1
        seq = ""
        record = SeqIO.read(fasta_files_dir + acc + ".fas", "fasta")
        seq = sequence(str(record.seq))

        # row = {data_gene[acc][k] for k in data_gene[acc].keys() and k not in toignore}

        for g in data_gene[acc]:

            fseq = ""
            el = 0
            if len(data_gene[acc][g]["start"]) > 1:
                # print g
                for i in range(len(data_gene[acc][g]["start"])):

                    start = data_gene[acc][g]["start"][i]
                    end = data_gene[acc][g]["stop"][i]
                    strand = data_gene[acc][g]["strand"]
                    # print g, start, end
                    try:
                        fseq += str(seq.subseq(start, end, strand))
                    except Exception:
                        print("Bleeeeeeeeeeh !!!")

                        if len(seq) - start > end:
                            fseq += str(seq.subseq(start, len(seq), strand))

                        else:
                            fseq += str(seq.subseq(0, end, strand))
                    # else:
                    # print "1"

                    #    fseq += str(seq.subseq( start,end , strand ))
                    el += 1
            elif len(data_gene[acc][g]["start"]) == 1:

                start = data_gene[acc][g]["start"][0]
                end = data_gene[acc][g]["stop"][0]
                strand = data_gene[acc][g]["strand"]
                # print g, start, end

                try:
                    fseq = str(seq.subseq(start, end, strand))
                except Exception:
                    print("Bleeeeeeeeeeh !!!")

                    if len(seq) - start > end:
                        fseq = str(seq.subseq(start, len(seq), strand))
                    else:
                        fseq = str(seq.subseq(0, end, strand))
                # else:
                #    fseq = str(seq.subseq( start,end , strand ))
                el += 1

            outfile.write(acc + "    " + g + "    " + str(len(fseq) - el) + "\n")
    outfile.close()

    print("number of tested species " + str(j))


def get_sequence_PCgenes(node_id, gene, fasta_files_dir, data):
    # # using the dict before convert

    row = []
    accession = get_Nc(taxidmap_file, node_id)
    gene_location = []
    gene_seq = ""

    record = SeqIO.read(fasta_files_dir + accession + ".fas", "fasta")
    seq = sequence(str(record.seq))
    if accession in data:
        row = data[accession]
        for i in range(len(row)):
            if gene == row[i].name:
                gene_location.append((row[i].start, row[i].stop))
                strand = row[i].strand

        for li in range(len(gene_location)):
            gene_start = gene_location[li][0]
            gene_end = gene_location[li][1]

            gene_seq += str(seq.subseq(gene_start, gene_end, strand))

        return gene_seq

    else:
        sys.stderr.write("accession not found in the data table " + accession + "\n")
        return


def intialize_non_leaves(t):
    for n in t.traverse(strategy="postorder"):
        if not n.is_leaf():
            n.add_feature("seq", "")
    return t


def initialize_leaves(t, data_array):
    global taxidmap_file
    tax_file = taxidmap_file

    for n in t.traverse(strategy="postorder"):
        # and n.is_leaf(): might be important
        if get_Nc(tax_file, n.name) in data_array:
            if found_gene(n.name, "nad5", data_array) is True:
                n.add_feature(
                    "seq",
                    "> "
                    + n.name
                    + "\n"
                    + get_sequence_PCgenes(n.name, "nad5", fasta_files_dir, data_array)
                    + "\n",
                )
            else:
                # print n.name
                n.add_feature("seq", "")
                print("missing nad5 gene from " + get_Nc(tax_file, n.name))

    return t


if __name__ == "__main__":
    usage = "usage: %prog dirs"

    # ast.literal_eval(x)
    # office:
    parser = argparse.ArgumentParser(description=usage)
    # parser.add_argument( 'dirs', metavar = 'DIRS', nargs = '+', help = 'directories' )
    parser.add_argument("dirs", metavar="DIRS", help="directories")
    # parser.add_argument( 'outdir', help = 'outputdir' )
    args = parser.parse_args()

    tr = Tree(tree_file, format=8)
    # getting all directories
    all_directory = [os.path.join(args.dirs, f) for f in os.listdir(args.dirs)]
    data_trna, data_gene = load_data(all_directory)

    conv_data_gene = convert_dict_PCG(data_gene)
    # for a in sorted(data_gene.keys()):
    #    print a
    #     ##### sometimes i have an accession and a taxid, but i don't have mitos
    #     #data, thats why the tree is now limited to the amount of MITOS data i have
    #     #for this group that im testing
    #
    #
    # print tr.get_ascii(show_internal=True)
    #     tr = Tree(tree_file, format = 8)
    #
    #
    #     n=tr.get_tree_root()
    #     n.name = "root"
    #
    #     print "checking for strains within the tree and replacing the names..."
    #     tr = internal_node_check(tr)
    #
    #     print "\nremoving leafs with no accession..."
    #     tr=remove_leaf_no_acc(tr)
    #
    #      #which_gene(tr, data_gene)
    #
    #
    #     print tr.get_ascii(show_internal=True)
    #
    #
    #
    #     print "\nremoving internal nodes with only one child..."
    #     remove_internals(n)
    #

    # tr.write(format=8,outfile=outp_dir+"Metazoa_mitochondrial_tree.nw")
    # ff = open(outp_dir+"leafs_after_removal.txt","w")
    print(tr.get_ascii(show_internal=True))
    n = tr.get_tree_root()
    n.name = "root"
    i = 0
    for nd in tr:
        # ff.write(str(nd.name)+"\n")
        i += 1
    print(
        "after removing the non-mitochondrial leafs, the tree has " + str(i) + " leafs"
    )
    # ff.close()

    #     tr=Tree(work_dir+"Metazoa_mitochondrial_tree.nw", format=8)

    print("initializing tree internal nodes...")
    tr = intialize_non_leaves(tr)  # intialize internal nodes in the tree
    print("initializing tree leaf nodes...")
    tr = initialize_leaves(tr, data_gene)  # initialize leaf nodes

    aff_seq(n, data_gene)

    recursive_bifurcate(tr, n, data_gene)  # working correctly
    #
    # #     for nn in tr.traverse():
    #         if not nn.is_leaf():
    #             print nn.name, len(nn.get_children())

    # print "3",tr.get_ascii(show_internal=True)
    # genes_sort_check(data_gene)
    # for nd in tr.traverse():
    #    if not nd.is_leaf():
    #        print nd.name,"\n",nd.seq
    # tr=bifurcate(tr,data_gene)

    print(
        "replacing internal nodes on the multifurcated tree, with the bifurcated version"
    )

    all_tree = Tree(os.path.join(work_dir + "Newick_trees/", "root.nh"))
    rt = all_tree.get_tree_root()
    rt.name = "root"
    tr_dict = dict_tree_files(work_dir + "Newick_trees/")

    quicktree_handle(rt, tr_dict)

    nr = all_tree.get_tree_root()
    nr.name = "root"
    remove_internals(nr)
    # print "2",tr.get_ascii(show_internal=True)

    #

    # print all_tree.get_ascii(show_internal=True)
    j = 0
    for nnn in all_tree:
        j += 1

    print("after tree bifurcation, the new tree has " + str(j) + " leafs")

    nc = 0
    for nnd in all.traverse():
        nc += 1
        if nnd.name == "NoName":
            nnd.name = "INT_" + str(nc)
    all_tree.write(format=8, outfile=work_dir + "Metazoa_bifurcated_tree.nw")


#
#
