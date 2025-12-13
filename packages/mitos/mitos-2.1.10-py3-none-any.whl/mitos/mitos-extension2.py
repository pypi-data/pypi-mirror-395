import argparse
import glob
import multiprocessing as mp
import os
import time

from Bio import SeqIO

from mitos.feature import feature
from mitos.sequence import sequence

# fasta_files_dir = "/Users/Abdullah/Documents/PhD/work/mitos-extension/test2/fasta_files/non-metazoa/"
fasta_files_dir = "/work/abdul/mitos-extension/fasta_files/"
# tab_files_dir = "/Users/Abdullah/Documents/PhD/work/mitos-extension/test2/fasta_files/tab_output/non-metazoa"
tab_files_dir = "/work/abdul/mitos-extension/Blast_tab_output/"
out_dir = "/work/abdul/mitos-extension/"


NUM_CPUS = None


def get_features(gbfile):
    gbhandle = open(gbfile, "r")
    record = SeqIO.read(gbhandle, "gb")
    gbhandle.close()

    return record.features, record.seq


def get_sequences(gbfiles):
    """
    MB comment the functions: should contain:
    1) what the function does : get all sequences, and features of a specific type from all the genbank files
    2) the input parameters : gb files
    3) the output : array which contains all features of the chosen types taken from the genbank files
    """
    all_seq_features = []
    fseq = ""
    for fl in args.gbfiles:
        seq = ""

        record = SeqIO.read(fl, "genbank")
        accession = record.name

        all_features, gbseq = get_features(fl)

        seq = sequence(str(gbseq))

        for feat in all_features:
            if feature.type in ["rRNA", "CDS"]:
                # print feature
                log_features_locations = _parse_feature_locations(feat)

                log_features_name = _parse_feature_name(feat)

                if len(log_features_locations) > 1:
                    for li in range(len(log_features_locations)):
                        start = log_features_locations[li][0]
                        end = log_features_locations[li][1]
                        strand = log_features_locations[li][2]
                        fseq += str(seq.subseq(start, end, strand))
                else:
                    start = log_features_locations[0][0]
                    end = log_features_locations[0][1]
                    strand = log_features_locations[0][2]
                    fseq = str(seq.subseq(start, end, strand))

                all_seq_features.append(
                    (accession, set(log_features_name), fseq, start, end)
                )
    return all_seq_features


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


# ## delete a couple of files which have < threshold nb of seq
# # if there is a feature that has for which all qualifiers that it has, don't have a file


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
            (feature.location.start.position, feature.location.end.position - 1, strand)
        )
    return loc


def save_to_fasta(all_features_arr):
    global fasta_files_dir
    """

    """
    # create a dict of file pointer, and whenever i find a new feature name, i added it to the dict and i open a new file and add the sequences to the correpsonding file, at the end i should close all the file pointers
    names = {}
    specials = [";", ",", "(", ")", "/", "\\", "+", "-", ">", "<", "|", "%", "="]
    for i in range(len(all_features_arr)):
        name_list = list(all_features_arr[i][1])
        for name in name_list:
            # print name
            if "TAA" not in name:
                name = name.replace(" ", "_")
                for i in range(len(specials)):
                    if specials[i] in name:
                        name = name.replace(specials[i], "")
                if name not in names:
                    names[name] = []
                names[name].append(all_features_arr[i][2])
    for n in names:
        f = open(fasta_files_dir + n + ".fas", "w")
        for j in range(len(names[n])):
            f.write("> " + n + "_" + str(j) + "\n" + names[n][j] + "\n")
    f.close()

    # blastn -subject fasta_files/NADH_dehydrogenase_subunit_4.fas -evalue 1e-10 -outfmt 5 -query fasta_files/ND4.fas -out test_NADH_dehydrogenase_subunit_4_nd4.xml


def blast_call(f1, f2, f1n, f2n):
    global fasta_files_dir
    # os.system("blastn -subject "+f1+" -evalue 1e-18 -task blastn -outfmt '6 qseqid sseqid' -query "+ f2+" -out " +fasta_files_dir+"tab_output/"+f1n+","+f2n+".tab")
    # print "blastn -subject "+f1+" -evalue 1e-18 -task blastn -outfmt '6 qseqid sseqid' -query "+ f2+" -out " +fasta_files_dir+"tab_output/"+f1n+","+f2n+".tab"

    os.system(
        "blastn -subject "
        + f1
        + " -evalue 1e-18 -task blastn -outfmt '6 qseqid sseqid' -query "
        + f2
        + " -out "
        + tab_files_dir
        + f1n
        + ","
        + f2n
        + ".tab"
    )


def blast_run(pool):

    global fasta_files_dir

    files = os.listdir(fasta_files_dir)

    for f1 in files:
        if f1.endswith(".fas"):
            file1 = os.path.join(fasta_files_dir, f1)

            f1records = list(SeqIO.parse(file1, "fasta"))
            if len(f1records) <= 10:
                continue
            else:

                for f2 in files:
                    f1n, ext1 = os.path.splitext(f1)
                    f2n, ext1 = os.path.splitext(f2)
                    if f2.endswith(".fas"):
                        file2 = os.path.join(fasta_files_dir, f2)

                        f2records = list(SeqIO.parse(file2, "fasta"))

                        if len(f2records) <= 10:
                            continue
                        else:
                            if f1n != f2n:
                                # print len(f1records), len(f2records)
                                # os.system("blastn -subject "+file1+" -evalue 1e-18 -task blastn -outfmt '6 qseqid sseqid' -query "+ file2+" -out " +fasta_files_dir+"tab_output/"+f1n+","+f2n+".tab")
                                pool.apply_async(
                                    blast_call, args=(file1, file2, f1n, f2n)
                                )


#                                if os.stat(fasta_files_dir+"tab_output/"+f1n+","+f2n+".tab").st_size == 0:
#                                    print "deleting empty file "+ f1n+","+f2n+".tab"
#                                    os.remove(fasta_files_dir+"tab_output/"+f1n+","+f2n+".tab")


def blast_tab_handle():
    global tab_files_dir
    global fasta_files_dir
    results = {}
    """

     """
    for blastfile in os.listdir(tab_files_dir):
        i = 0
        # print blastfile
        if blastfile.endswith(".tab"):
            fname, ext = os.path.splitext(blastfile)
            fnames = fname.split(",")
            f1name = fnames[0]
            f2name = fnames[1]

            if fname not in results:
                results[fname] = {}

            # print len(f1records), len(f2records)
            tabhandle = open(os.path.join(tab_files_dir, blastfile), "r")

            # # fasta file A : 100 seq , and fasta file B : 100 seq
            # # search all seq from A for seq in B
            # # count how many seq in A have at least one blast hit with any seq of B and if this is 95% of the seq in A then we accept it
            # # and the same way should apply in the other way around
            # # count the query sequences from fastafile1 that have at least 1 subject hit from fastafile2 --important
            if f1name != f2name:
                for line in tabhandle:
                    line = line.split("\t")
                    # # query is from the file (f2name)
                    query_name = str(line[0])
                    subject_name = str(line[1])

                    # # not store results for all files, u empty the results dict after each loop of this for loop...
                    # # process each file, process it (next for loop) and then empty to save memory .. all wthin the for blastfile in os.... for loop (21 JAN)
                    if query_name not in results[fname]:
                        results[fname][query_name].append(subject_name)

            #                    if not subject_name in results[fname][query_name]:
            #                        results[fname][query_name][subject_name] = {}
            # print query_name, subject_name
            else:
                print("identical files")
                continue
        else:
            print("Non XML file found, skipping ...")
            continue

    # print results['small_subunit_ribosomal_RNA,s-rRNA']
    res = []
    singletons = []
    for fs in results:
        count = 0
        nfnames = fs.split(",")

        # fastafile1 = os.path.join(fasta_files_dir, nfnames[0] + ".fas")
        fastafile2 = os.path.join(fasta_files_dir, nfnames[1] + ".fas")

        # f1records = list(SeqIO.parse(fastafile1, "fasta"))
        f2records = list(SeqIO.parse(fastafile2, "fasta"))

        singletons.append(nfnames[0])

        for q in results[fs]:

            if len(results[fs][q]) >= 1:
                count += 1

        f2_seq_perc = (count * 100) / len(f2records)

        res.append((nfnames[0], nfnames[1], f2_seq_perc))
        # print fs, count,len(f2records), f2_seq_perc

        # # initialize the sets with the singletons of all possible names, files with 1 seq should not appear a singletons
    arr = []
    for i in range(len(res)):
        for j in range(len(res)):
            if (
                res[i][0] == res[j][1]
                and res[j][0] == res[i][1]
                and res[i][2] >= 95
                and res[j][2] >= 95
            ):
                arr.append(res[i])
            # if res[i][0] == "ATP8" and res[i][1] == "ATPase8" and res[j][0] == "ATPase8" and res[j][1] == "ATP8":
            #    print res[i], res[j]
    sets = []
    for sn in set(singletons):
        sets.append(set([sn]))
    # print len(sets)
    for u in range(len(arr)):
        # 2 indices for arr[u][0] and arr[u][1]
        ind0 = None
        ind1 = None
        for x in range(len(sets)):
            if arr[u][0] in sets[x]:
                ind0 = x

            if arr[u][1] in sets[x]:
                ind1 = x

        if ind0 is None and ind1 is None:
            sets.append(set([arr[u][0], arr[u][1]]))

        elif ind0 is not None and ind1 is None:
            sets[ind0].add(arr[u][1])

        elif ind0 is None and ind1 is not None:
            sets[ind1].add(arr[u][0])

        elif ind0 is not None and ind1 is not None and ind0 != ind1:
            sets[ind0].add(arr[u][1])
            del sets[ind1]
        # ## combine sets together and delete one of them
        # # check the name of CYTB which contain only 1 seq, find in which specie, and look if it has the other name

    # print len(sets)
    # sets = list(set(list(sets)))
    fout = open(out_dir + "final_res.txt", "w")
    for t in range(len(sets)):
        fout.write(sets[t] + "\n")
    fout.close()


#
#                continue
#            if res[i][1] == "ATP6" and res[j][0]=="ATPase_subunit_8":
#                print res[i]
#


def qualifier_check(gbfiles, res_sets):
    """
    go through all features and check if there is a qualifier with a name that is included in 1 of our sets -- to implement
    """

    features_set = []
    for fl in gbfiles:
        all_features, gbseq = get_features(fl)
        for feat in all_features:
            if feat.type in ["rRNA", "CDS"]:
                log_features_name = _parse_feature_name(feat)
        features_set.append(set(log_features_name))


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
    # parser.add_argument('fastafile', help = 'output file')
    args = parser.parse_args()

    start = time.time()
    allgbfiles = list(f for arg in args.gbfiles for f in glob.glob(arg))

    print("loading sequences and features ... \n")
    # to_fasta_features=get_sequences(allgbfiles)
    print("sequences and features successfully loaded \n")

    print("creating fasta files ... \n")
    # allnames = save_to_fasta(to_fasta_features)
    print("fasta files successfully created ... \n")

    print("running blast all vs all and generating tabular output... \n")
    pool = mp.Pool(12)
    blast_run(pool)
    pool.close()
    pool.join()
    print("blast run finished and blast tabular files successfully created ... \n")

    print("analysing blast tabular files and generating the results ... \n")
    blast_tab_handle()
    print("script finished sucessfully")


end = time.time()
print("elapsed time", end - start)
