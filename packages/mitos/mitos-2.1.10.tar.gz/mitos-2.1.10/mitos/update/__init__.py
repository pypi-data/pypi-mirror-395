"""
@author: M. Bernt
"""

import glob
import json
import logging
import math
import os
import re
import sys
import traceback
from io import StringIO

from Bio import Data, GenBank

from mitos import sequence, util
from mitos.trna import trnascan


def _add_one_codonstats(cod_stat, tpe, code, name, codon):
    try:
        cod_stat[tpe][code][name][str(codon)] += 1
    except KeyError:
        cod_stat[tpe][code][name][str(codon)] = 1


def _init_codonstats(cod_stat, code, name):
    for t in ["start", "stop", "inner"]:
        if code not in cod_stat[t]:
            cod_stat[t][code] = {}
        if name not in cod_stat[t][code]:
            cod_stat[t][code][name] = {}

            if str(code).endswith("*"):
                continue

            # init also standard tables with unit counts
            if t == "start":
                for c in Data.CodonTable.unambiguous_dna_by_id[int(code)].start_codons:
                    cod_stat[t][code][name][c] = 1
            if t == "stop":
                for c in Data.CodonTable.unambiguous_dna_by_id[int(code)].stop_codons:
                    cod_stat[t][code][name][c] = 1


def _append_len_list(len_lists, code, name, ln):

    if code not in len_lists:
        len_lists[code] = {}
    if name not in len_lists[code]:
        len_lists[code][name] = []
    len_lists[code][name].append(ln)


def prepareFiles(data, outdir, codss, codin, delinner):
    """
    - create sub directories 'featureNuc' and 'featureProt' (old data is
      removed if existent)
    - for each genbank file in files:
      * write nucleotide sequences of the features annotated in the genbank
        file to the corresponding file in 'featureNuc'
      * write amino acid sequences of the features annotated in the genbank
        file file to the corresponding file in 'featureProt' (take the given
        amino acid sequence, NOT the translation of the annotated range)
    - create BLAST data bases of all created fasta
    - create the data file for non-canonical start codons and gene length statistics
    @param data list of genbank data
    @param outdir the directory where the BLAST data bases and
        the non-canonical start codon file should be written
    @param codss minimum fraction of appearances of a codon (per gene and code)
        as start/stop to be accepted as start/stop
    @param codin maximum fraction of appearances of a codon (per gene and code)
        as inner codon to be accepted as stop
    @param delinner remove statistics on inner codons from data before dumping

    """

    if not os.path.exists(outdir):
        os.mkdir(outdir)

    feature_nuc_path = outdir + "/featureNuc/"
    feature_prot_path = outdir + "/featureProt/"

    auxinfo_path = outdir + "/auxinfo.json"

    # (start/stop/inner) codon statistics
    cod_stat = {"start": {}, "stop": {}, "inner": {}}
    # mapping of fasta header to gene length
    fas2len = {}

    # feature length statistics
    len_lists = {}
    len_pval = {}

    # create nuc and prot directories
    logging.debug(
        "create directories for nucleotide features (%s) and for protein features (%s)"
        % (feature_nuc_path, feature_prot_path)
    )
    if os.path.exists(feature_nuc_path):
        logging.debug(
            "directory %s already exists - removing old files" % (feature_nuc_path)
        )
        # remove all outdated files in this directory
        os.system("rm -rf %s*" % (feature_nuc_path))
    else:
        os.mkdir(feature_nuc_path)

    if os.path.exists(feature_prot_path):
        logging.debug(
            "directory %s already exists - removing old files" % (feature_prot_path)
        )
        # remove all outdated files in this directory
        os.system("rm -rf %s*" % (feature_prot_path))
    else:
        os.mkdir(feature_prot_path)

    if os.path.exists(auxinfo_path):
        logging.debug("file %s already exists - removing old file" % (auxinfo_path))
        # remove all outdated files in this directory
        os.system("rm -f %s*" % (auxinfo_path))
    logging.debug("done")

    i = 0
    for gbdata in data:

        i += 1
        if i % 100 == 0:
            logging.debug("%d/%d" % (i, len(data)))

        # gbdata = gbfromfile( filename )

        # build fasta file for genbank file
        acc = gbdata.accession
        name = gbdata.name
        code_emp = "%d*" % (gbdata.transl_table)
        code_org = str(gbdata.transl_table)

        #         if len( set( ["Platyhelminthes", "Nematoda", "Nemertea"] ) & set( gbdata.taxonomy ) ) > 0:
        #             tax14 = True
        #         else:
        #             tax14 = False

        # prepare featurefiles - all sequences for one gene gathered in one
        # multifasta file
        features = gbdata.getfeatures()
        for feature in features:
            if feature.type in ["tRNA", "rRNA"]:
                continue

            if not (feature.part is None or feature.part == 0):
                continue

            parts = [
                x for x in features if x.name == feature.name and x.copy == feature.copy
            ]
            parts.sort(key=lambda x: x.part)

            fname = feature.name
            fstart = parts[0].start
            fstop = parts[-1].stop
            fstrand = feature.strand
            feature_nuc_file = feature_nuc_path + fname + ".fas"

            seq = ""
            for p in parts:
                seq = seq + str(gbdata.sequence.subseq(p.start, p.stop, p.strand))
            seq = sequence.sequence(seq)
            if len(seq) < 6:
                continue

            if fname not in fas2len:
                fas2len[fname] = {}

            output = ">%s:%s-%d-%d-%d %s\n%s\n" % (
                acc,
                feature.getname(),
                fstrand,
                fstart,
                fstop,
                name,
                str(seq),
            )

            # get the frequency of standard nucleotides (makeblastdb requires >
            # 60%)
            nfreq = seq.nucleotide_frequency()
            stdf = 0
            for letter in Data.IUPACData.unambiguous_dna_letters:
                if letter in nfreq:
                    stdf += nfreq[letter]

            if stdf >= 0.6:
                fh = open(feature_nuc_file, "a")
                fh.write(output)
                fh.close
            else:
                logging.warning(
                    "skipping {gene} ({acc}): has only {std} unambiguous_dna_letters".format(
                        gene=fname, acc=gbdata.accession, std=stdf
                    )
                )

            # prepare fasta files with proteins
            if feature.translation is not None:
                feature_prot_file = feature_prot_path + fname + ".fas"
                prot_output = ">%s:%s-%d-%d-%d %s\n%s\n" % (
                    acc,
                    feature.getname(),
                    fstrand,
                    fstart,
                    fstop,
                    name,
                    str(feature.translation),
                )
                fh = open(feature_prot_file, "a")
                fh.write(prot_output)
                fh.close

                fas2len[fname][
                    "%s:%s-%d-%d-%d" % (acc, feature.getname(), fstrand, fstart, fstop)
                ] = 3 * len(feature.translation)
            else:
                fas2len[fname][
                    "%s:%s-%d-%d-%d" % (acc, feature.getname(), fstrand, fstart, fstop)
                ] = len(seq)

            # add the length of the gene to the list of gene lengths

            if feature.type == "gene":
                _append_len_list(len_lists, code_org, fname, len(seq))
            #                 if tax14:
            #                     _append_len_list( len_lists, "14", fname, len( seq ) )

            # count starts/stop/inner codons (only if there are no duplicates)
            if (
                feature.type == "gene"
                and len([x for x in features if x.name == fname]) == 1
            ):
                # init data structures

                _init_codonstats(cod_stat, code_org, fname)
                _init_codonstats(cod_stat, code_emp, fname)
                #                 if tax14:
                #                     _init_codonstats( cod_stat, "14", fname )
                #                     _init_codonstats( cod_stat, "14*", fname )

                # start
                codon = str(seq.subseq(0, 2, 1))
                _add_one_codonstats(cod_stat, "start", code_emp, fname, codon)
                #                 if tax14:
                #                     _add_one_codonstats( cod_stat, "start", "14*", fname, codon )
                #      ---|||---|||
                # len  123456789012
                #      1112223334
                #      0001112223
                #      0003336669
                #
                stopf = 3 * (int(math.ceil(len(seq) / 3.0)) - 1)
                codon = list(seq.subseq(stopf, len(seq) - 1, 1))
                while len(codon) < 3:
                    codon.append("N")
                codon = "".join(codon)
                _add_one_codonstats(cod_stat, "stop", code_emp, fname, codon)
                #                 if tax14:
                #                     _add_one_codonstats( cod_stat, "stop", "14*", fname, codon )

                # inner
                for j in range(3, stopf, 3):
                    codon = str(seq.subseq(j, j + 2, 1))
                    if not (
                        codon[0] in Data.IUPACData.unambiguous_dna_letters
                        and codon[1] in Data.IUPACData.unambiguous_dna_letters
                        and codon[2] in Data.IUPACData.unambiguous_dna_letters
                    ):
                        continue

                    #                     sys.stdout.write( "%s %s\n" % ( gbdata.accession, codon ) )
                    _add_one_codonstats(cod_stat, "inner", code_emp, fname, codon)
    #                     if tax14:
    #                         _add_one_codonstats( cod_stat, "inner", "14*", fname, codon )
    # sys.stderr.write( "# %s %s %s %s\n" % ( str( codon ),
    # gbdata.accession, code_org, " ".join( gbdata.taxonomy ) )
    # )

    # formatdb new created fastafiles
    # featureNuc
    for fname in glob.glob("%s/*.fas" % (feature_nuc_path)):
        cmd = ["makeblastdb", "-dbtype", "nucl", "-in", fname]
        out, err = util.execute(cmd)
    # os.system( "for i in %s*.fas; do formatdb -i $i -o -p F; done" % feature_nuc_path )
    logging.debug("formatdb for feature nucs done")

    # featureProt
    for fname in glob.glob("%s/*.fas" % (feature_prot_path)):
        cmd = ["makeblastdb", "-dbtype", "prot", "-in", fname]
        out, err = util.execute(cmd)
    # os.system( "for i in %s*.fas; do formatdb -i $i -o -p T; done" % feature_prot_path )
    logging.debug("formatdb for feature prots done")

    # get frequencies from counts (! inner 1st because data needed for stop)
    for t in ["inner", "start", "stop"]:
        for code in list(cod_stat[t].copy().keys()):
            for name in list(cod_stat[t][code].copy().keys()):
                # sum for computing averages
                summ = 0
                for codon in cod_stat[t][code][name]:
                    summ += cod_stat[t][code][name][codon]

                # remove stops that are annotated only infrequently
                # remove start that are annotated only infrequently
                # or are annotated as inner codons
                for codon in list(cod_stat[t][code][name].copy().keys()):
                    cod_stat[t][code][name][codon] = float(
                        cod_stat[t][code][name][codon]
                    ) / float(summ)

                    if t == "start" and cod_stat[t][code][name][codon] < codss:
                        del cod_stat["start"][code][name][codon]
                    if t == "stop":
                        try:  # get usage of the codon inside the gene
                            uai = cod_stat["inner"][code][name][codon]
                        except KeyError:
                            uai = 0

                        if cod_stat[t][code][name][codon] < codss or uai >= codin:
                            del cod_stat["stop"][code][name][codon]

                # recalculate averages
                if t != "inner":
                    summ = 0
                    for codon in cod_stat[t][code][name]:
                        summ += cod_stat[t][code][name][codon]
                    for codon in cod_stat[t][code][name]:
                        cod_stat[t][code][name][codon] = cod_stat[t][code][name][
                            codon
                        ] / float(summ)

                if len(cod_stat[t][code][name]) == 0:
                    del cod_stat[t][code][name]

            if len(cod_stat[t][code]) == 0:
                del cod_stat[t][code]

    # get gene length statistics, i.e., p-values
    for code in len_lists:
        len_pval[code] = {}
        for fname in len_lists[code]:
            len_pval[code][fname] = {}

            mnl = min(len_lists[code][fname])
            mxl = max(len_lists[code][fname])
            n = float(len(len_lists[code][fname]))

            #             if fname == "cox1":
            #                 logging.error( "code %d" % code )
            #                 logging.error( "length %s" % str( len_lists[code][fname] ) )
            #                 logging.error( "n %f min %d max %d" % ( n, mnl, mxl ) )

            for i in range(mnl, mxl + 1):
                lt = len([x for x in len_lists[code][fname] if x >= i])
                gt = len([x for x in len_lists[code][fname] if x <= i])
                n = float(
                    len(len_lists[code][fname])
                    + len([x for x in len_lists[code][fname] if x == i])
                )
                len_pval[code][fname][i] = 2 * min(gt / n, lt / n)

    # init code 14 as copy of code 9 (for data sets that have code 9)
    if "9" in len_pval:
        cod_stat["start"]["14*"] = cod_stat["start"]["9*"]
        cod_stat["stop"]["14*"] = cod_stat["stop"]["9*"]
        cod_stat["inner"]["14*"] = cod_stat["inner"]["9*"]

        if "14" not in cod_stat["start"]:
            cod_stat["start"]["14"] = {}
        if "14" not in cod_stat["stop"]:
            cod_stat["stop"]["14"] = {}
        for name in cod_stat["start"]["9"]:
            if name not in cod_stat["start"]["14"]:
                cod_stat["start"]["14"][name] = {}
            if name not in cod_stat["stop"]["14"]:
                cod_stat["stop"]["14"][name] = {}

            for c in Data.CodonTable.unambiguous_dna_by_id[int(code)].start_codons:
                cod_stat["start"]["14"][name][c] = 1
            for c in Data.CodonTable.unambiguous_dna_by_id[int(code)].stop_codons:
                cod_stat["stop"]["14"][name][c] = 1
        len_pval["14"] = len_pval["9"]

    # add the len_pval and fas2len data to the cod_stat dict
    cod_stat["fas2len"] = fas2len
    cod_stat["len_pval"] = len_pval

    f = open(auxinfo_path, "w")
    json.dump(cod_stat, f, indent=3, sort_keys=True)
    f.close()


def refseqsplit(fname, dname, prefix=None, atax=None, ftax=None, maxentries=False):
    """
    split a given genbank file containing multiple genbank records into single files
    @param fname input multi genbank file
    @param dname directory for writing the output
    @param prefix only accession numbers with this prefix (e.g. NC) are allowed
          (default: None, i.e. allow all prefixes)
    @param atax a list of taxonomic entities, only species belonging to one of
           the taxonomix groups are accepted (default: None, i.e. allow everything)
    @param ftax a list of taxonomic entities, reject species belonging to one of
           the taxonomix groups (default: None, i.e. reject nothing)
    @param maxentries  maximum number of genbank files to write
    """
    n = 0
    N = 0

    try:
        fhandle = open(fname, "r")
    except Exception:
        logging.error("error: could not open %s for reading\n" % (fname))
        sys.exit(1)

    cgb = ""
    # read line by line
    while 1:
        nxt = fhandle.readline()  # read a one-line string
        if not nxt:  # or an empty string at EOF
            break

        cgb += nxt
        if re.match("^//$", nxt) is not None:
            gb_iterator = GenBank.Iterator(StringIO(cgb), GenBank.FeatureParser())

            try:
                cur_record = next(gb_iterator)
            except Exception:
                logging.error("parser error: %s" % cgb.split()[1])

                stream = StringIO()
                exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
                traceback.print_exception(
                    exceptionType, exceptionValue, exceptionTraceback, file=stream
                )
                logging.error(stream.getvalue())
                stream.close()

                cgb = ""
                N += 1
                continue

            # #            print cur_record
            #            print "ann", cur_record.annotations
            #            print "dbx", cur_record.dbxrefs
            #            print "des", cur_record.description
            # #            print "fea", cur_record.features
            #            print "fmt", cur_record.format
            #            print "id ", cur_record.id
            #            print "lan", cur_record.letter_annotations
            # #            print "low", cur_record.lower
            # #            print "nam", cur_record.name
            # #            print "rev", cur_record.reverse_complement
            # #            print "seq", cur_record.seq
            # #            print "upp", cur_record.upper
            #            sys.exit()

            tax = cur_record.annotations["taxonomy"]
            #            print tax
            #            print atax
            #            if atax != None:
            #                print filter( lambda x:x in tax, atax )
            #            print ftax
            #            if ftax != None:
            #                print filter( lambda x:x in tax, ftax )

            skip = False
            if prefix is not None and not cur_record.name.startswith(prefix):
                logging.debug("%s prefix skip" % cur_record.name)
                skip = True
            if atax is not None and len([x for x in atax if x in tax]) == 0:
                logging.debug("%s allowed tax skip (%s)" % (cur_record.name, str(tax)))
                skip = True
            if ftax is not None and len([x for x in ftax if x in tax]) > 0:
                logging.debug(
                    "%s forbidden tax skip (%s)" % (cur_record.name, str(tax))
                )
                skip = True

            if not skip:
                logging.debug("%s writing entry" % cur_record.name)
                ofile = dname + "/" + cur_record.name + ".gb"
                try:
                    ohandle = open(ofile, "w")
                except Exception:
                    logging.error("error: could not write to %s\n" % ofile)
                    sys.exit()

                ohandle.write(cgb)
                ohandle.close()
                n += 1

            cgb = ""
            N += 1
            # break
            if maxentries and maxentries <= n:
                logging.info("Max entries found")
                break

    logging.info("%d gb entries found %d written" % (N, n))


def singleblastx(seqfile, code, outputdir, refdir):
    """
    run blastall blastx
    store results in OUTPUTDIR/blast/prot/(absname of seqfile)
    @param seqfile a (single) fasta sequenz file
    @param code genetic code
    @param outputdir directory for writing the results
    @param[in] refseqver version of refseq to use
    @param[in] refdir directory containing reference data
    @return path where the result files can be found
    """

    #    print "singleblastx", sequenzfile, code, outputdir

    # file = open(sequenzfile,"r")
    # file.readlines()[1]
    # file.close()

    prot_path = "{refdir}/featureProt/".format(refdir=refdir)
    prot_files = glob.glob(prot_path + "*.fas")

    # acc = splitext(basename(seqfile))[0]

    # create directories
    if not os.path.exists("%s/blast" % (outputdir)):
        os.mkdir("%s/blast" % (outputdir))
    if not os.path.exists("%s/blast/prot" % (outputdir)):
        os.mkdir("%s/blast/prot" % (outputdir))

    # blasts
    for f in prot_files:

        outfile = "%s/blast/prot/%s.%s.blast" % (
            outputdir,
            os.path.basename(seqfile),
            os.path.basename(f)[:-4],
        )
        # check if outfile already exists
        if os.path.exists(outfile):
            continue

        # cmd = 'blastx -query_gencode %d -db %s -query %s -soft_masking true -seg yes -outfmt 6 -lcase_masking -threshold 12 -num_alignments %d -evalue 1e-1 -out %s/blast/prot/%s.%s.blast' % \
        # , "-outfmt", "6"
        param = [
            "-query_gencode",
            "%d" % code,
            "-db",
            f,
            "-outfmt",
            "6",  #                 "-comp_based_stats", "0", \
            #                    "-soft_masking", "true", \
            "-seg",
            "no",  #                    "-lcase_masking", \
            #               "-threshold", "12", \
            "-num_alignments",
            "1000000000",  #                "-evalue", "10", \
            "-out",
            outfile,
        ]

        cmd = ["blastx", "-query", seqfile] + param
        out, err = util.execute(cmd)
    #             # -F "m S" filter SEG (aa low complexity filter) allow extension through low complexity regions
    #             # -U filter lower case
    #             # -f 12 Threshold for extending hits
    #             cmd = 'blastall -p blastx -Q %d -d %s -i %s -F "m S" -m 8 -U -f 12 -b %d -e 1e-1 -o %s/blast/prot/%s.%s.blast' % \
    #             ( code, f, sequenzfile, maxint / 2, outputdir, acc, os.path.basename( f )[:-4] )
    #             # print( "blastx\n%s" % cmd )
    #             os.system( cmd )

    return "%s/blast/prot/" % (outputdir)


def singleblastn(seqfile, outputdir, refdir):
    """
    @param seqfile a (single) fasta sequenz file
    @param outputdir directory for writing the results
    @param[in] refseqver version of refseq to use
    @param[in] refdir directory containing reference data
    """

    nuc_path = "{refdir}/featureNuc/".format(refdir=refdir)
    nuc_files = glob.glob(nuc_path + "*.fas")
    # maxint = 2147483647  # realy big number to make sure blast reports all
    # results

    # acc = splitext(basename(seqfile))[0]

    # Creat Dirs
    if not os.path.exists("%s/blast" % (outputdir)):
        os.mkdir("%s/blast" % (outputdir))
    if not os.path.exists("%s/blast/nuc" % (outputdir)):
        os.mkdir("%s/blast/nuc" % (outputdir))
    #    if not os.path.exists( '%s/blast/nuc/%s' % ( outputdir, acc ) ):
    #        os.mkdir( '%s/blast/nuc/%s' % ( outputdir, acc ) )

    # blast
    for f in nuc_files:
        outfile = "%s/blast/nuc/%s.%s.blast" % (
            outputdir,
            os.path.basename(seqfile),
            os.path.basename(f)[:-4],
        )
        if os.path.exists(outfile):
            continue

        # cmd = 'blastn -task blastn -query %s -db %s -outfmt 6 -reward 1
        # -penalty -1 -gapopen 1 -gapextend 2 -word_size 9 -soft_masking true
        # -dust yes -lcase_masking -out %s/blast/nuc/%s.%s.blast' % \
        param = [
            "-task",
            "blastn",
            "-db",
            f,
            "-outfmt",
            "6",  #                  "-reward", "1", \
            #                  "-penalty", "-1", \
            #                  "-gapopen", "1", \
            #                  "-gapextend", "2", \
            #                  "-word_size", "9", \
            #                  "-soft_masking", "true", \
            "-dust",
            "no",  #                  "-lcase_masking", \
            "-num_alignments",
            "1000000000",
            "-out",
            outfile,
        ]

        cmd = ["blastn", "-query", seqfile] + param
        out, err = util.execute(cmd)


#         cmd = 'blastall -p blastn -i %s -d %s -m 8 -r 1 -q -1 -G 1 -E 2 -W 9 -F "m D" -U -o %s/blast/nuc/%s.%s.blast' % \
#         ( sequenzfile, file, outputdir, acc , os.path.basename( file )[:-4] )
# #        print cmd
#         os.system( cmd )

# def singleblastrRNA( sequenzfile, outputdir ):
#     try:
#         file = open( sequenzfile, "r" )
#         file.readlines()[1]
#         file.close()
#         nuc_path = "%s/featureNuc/" % ( CONFIG.DATAPATH )
#         nuc_files = glob.glob( nuc_path + "1*.fas" )
#         maxint = sys.maxint
#         acc = sequenzfile.split( '/' )[-1][:-4]
#
#         # Creat Dirs
#         if not os.path.exists( '%s/blast' % ( outputdir ) ):
#             os.mkdir( '%s/blast' % ( outputdir ) )
#         if not os.path.exists( '%s/blast/nuc' % ( outputdir ) ):
#             os.mkdir( '%s/blast/nuc' % ( outputdir ) )
#         if not os.path.exists( '%s/blast/nuc/%s' % ( outputdir, acc ) ):
#             os.mkdir( '%s/blast/nuc/%s' % ( outputdir, acc ) )
#
#         # blast
#         for file in nuc_files:
#             # TODO
#             # => cmd = 'blastn -task blastn -query %s -db %s -outfmt 6 -evalue 1e-5 -num_alignments %d -dust no -out %s/blast/nuc/%s/%s.%s.blast' % \
#             cmd = 'blastall -p blastn -i %s -d %s -m8 -e 1e-5 -b %d -F F -o %s/blast/nuc/%s/%s.%s.blast' % \
#             ( sequenzfile, file, maxint / 2, outputdir, acc , acc, os.path.basename( file )[:-4] )
#             os.system( cmd )
#     except:
#         pass


def singletrnascan(sequenzfile, code, outdir):
    # make trnascan folder
    if not os.path.exists(outdir + "/tRNAScan"):
        os.mkdir(outdir + "/tRNAScan")

    outfile = outdir + "/tRNAScan/" + os.path.basename(sequenzfile) + ".ss"
    # Start scan
    try:
        gencode = trnascan.getGencodeFromTranl_tableNumber(str(code))
    except Exception:
        logging.debug("Could not determine genetic code for %s" % (sequenzfile))
        gencode = None

    if gencode is not None:
        trnascan.singletrnascan(
            sequenzfile, Q=True, O=True, b=True, X=5, q=True, f=outfile, g=gencode
        )
    else:
        trnascan.singletrnascan(
            sequenzfile, Q=True, O=True, b=True, X=5, q=True, f=outfile
        )
