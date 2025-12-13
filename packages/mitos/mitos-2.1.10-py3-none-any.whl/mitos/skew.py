"""
@author: M. Bernt

get nucleotide frequencies (or some math. expression of the frequencies) from a
sequence in a fasta or genbank file

input files:

you can input one or more fasta or genbank files. In case a genbank file is given
the circularity is taken from the genbank file. For fasta files the circularity
has to be specified on the command line (-c --circular).

input options:

for each of the files certain subsequences are collected depending on the parameters
a) a window size w is specified with the --window option
   for each position p in the sequence the window [p - w/2 + 1: p + w/2]
   is added to the list of subsequences. if the sequence is circular then p
   is iterated in [0:len-1] and in [w:len-w-1] otherwiss.
   in other words: all substrings of length w are enumerated
   in even other words: all overlapping windows of size w are enumerated
   - its possible to visit consider not every position. with the parameter
     --offset a step size can be given
   - the reverse complement of the windows is taken if --strand -1 is given.
b) genbank file is given and allowed types or allowed names are specified
   with combinations of the parameters -y -Y -n -N arbitrary subsets of the
   features given in the genbank file can be specified. The subsequences
   corresponding to these features on the corresponding strand are extraced*.
   -y allows features of a certain type (gene, rRNA, tRNA, or rep_origin)
   -n allows features of a certain name (e.g. rrnL, cox1, atp8, trnA, ...)
   -Y and -N forbids certain features types or names
   by combining several of these options feature subsets are selected.
   additionally it is possible to skip certain genbank files depending on
   the taxonomy of the corresponding species with options -t and -T.
   -t Arthropoda -t Chordata will output all Arthropoda and Chordata
   -t Arthropoda -T Hexapoda will output data for all non Hexapod Arthropods

   * if the --strand option is given, then the strandedness of the features
     is overwritten and the value specified by the parameter is used.

   * if the window option is given the sequence of the window is split in windows
     here: if Xfold is given the actual window size is determined dynamically such
     that at least window size X-fold degenerate codons are included, note offset
     needs to be specified as multiple of three

c) otherwise the compete sequence is added.
   the reverse complement of the windows is taken if --strand -1 is given.

postprocessing:

after the subsequences have been collected for a file the following postprocessing
options are possible:
1) if --third is given only every third position is taken from the sequences
   (probably this is only usefull for proteins (use -y gene))
   - if the values are counted for the one strand, but the gene os coded on the
     other strand then the 1st position is taken (only for gb files)
2) only output data for X-fold degenerated codons.
   - if the data in from genbank file the genetic code is taken from there.
     otherwise it has to be specified with the --code parameter.
   - ATTENTION: the user needs to take care that only protein coding sequences
     are specified
3) if --random is given then subsequences are replaced by random or randomised
   sequences of the same length
   2a) mode "shuffle" shuffles the collected sequences
   2b) mode "random" takes new random sequences
   note 2a) is only useful for dinucleotides.

output options:

for each of the resulting sequences the nucleotide (and dinucleotide)
frequencies are calculated and the specified expressions are calculated
and printed in column on a single line. this is, each subsequence generates
one line.
the output is in columns each column gives the values computed with an
expression specified with option -e. With the option you specify a mathematical
expression computing a value from the frequencies of A,T,C, and G. For example
* -e "A" -e "T" -e "C" -e "G" will output 4 columns with the 4 frequencies
* -e "(A-T)/(A+T)" -e "(G-C)/(G+C)" -e "(A+T)/(G+C)" outputs the
  AT- and GC- skews and strand bias
dinucleotide frequencies are accessed with two letter codes:
* -e "AG" -e "AT" ...

additional information extracted from the genbank or fasta file can be printed at
the end of each line. currently this is the accession (gb only) and the name
(fasta and gb). the information to be printed can be specified with the --format
option. --format "%a" prints accession and --format "%n" the name. if "%a %n" is
given both information is printed.
"""

# get skewness values for genes

import glob
import os.path
import random
import sys
from optparse import OptionGroup, OptionParser

from mitos.gb import gbfromfile
from mitos.sequence import randsequence, sequence, sequence_info_fromfile
from mitos.sequence.degenerate import degenerated_subseq

usage = "usage: %prog [options] file"
parser = OptionParser(usage)
parser.add_option(
    "-e",
    "--expr",
    action="append",
    type="string",
    metavar="EXPR",
    help="add expression to evaluate and print",
)
parser.add_option(
    "--third",
    action="store_true",
    default=False,
    help="only consider third codon position",
)
parser.add_option(
    "-X",
    "--Xfold",
    action="store",
    type="int",
    metavar="X",
    help="count only X fold dedenerate codes of genes",
)
parser.add_option(
    "--code", action="store", type="string", metavar="CT", help="use code table X"
)

parser.add_option("--svm", action="store_true", default=False, help="output format svm")
parser.add_option(
    "-o",
    "--outfile",
    action="store",
    type="string",
    metavar="FILE",
    help="write values to FILE (default: stdout)",
)
parser.add_option(
    "-f",
    "--format",
    dest="format",
    action="store",
    type="string",
    default=" ",
    metavar="FORMAT",
    help="output format: % a=accession, % n=name",
)

parser.add_option(
    "-r",
    "--random",
    action="store",
    type="string",
    metavar="MODE",
    help="generate random subsequences of the same length, valid MODEs: shuffle & random",
)
parser.add_option(
    "-c",
    "--circular",
    action="store_true",
    default=False,
    help="treat sequence(s) as circular (doeas not apply to gb files)",
)
parser.add_option(
    "-s",
    "--strand",
    action="store",
    type="int",
    metavar="STRAND",
    help="get values for +/ -strand",
)

group = OptionGroup(
    parser,
    "select a subset of the features in the genbank file for calculations. "
    "(type can be tRNA, rRNA, and gene) "
    "Note:-y, -Y, -n, -N can be specified more than once, combinations are possible.",
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

parser.add_option(
    "-t",
    dest="atax",
    action="append",
    type="string",
    metavar="TAX",
    help="allow only entries with TAX in the taxonomy",
)
parser.add_option(
    "-T",
    dest="ftax",
    action="append",
    type="string",
    metavar="TAX",
    help="forbid all entries with TAX in the taxonomy",
)
parser.add_option(
    "-w",
    "--window",
    action="store",
    type="int",
    metavar="SIZE",
    help="use windows of size SIZE",
)
parser.add_option(
    "--offset",
    action="store",
    type="int",
    default=1,
    metavar="OFF",
    help="set offset to OFF",
)

(options, args) = parser.parse_args()

args = list(f for arg in args for f in glob.glob(arg))

# check arguments
# no input files / dirs given?
if len(args) == 0:
    sys.stderr.write("no input file(s) given\n")
    print(usage)
    sys.exit()

# nothing to evaluate
if options.expr is None:
    sys.stderr.write("no expression given\n")
    print(usage)
    sys.exit()

if (
    options.random is not None
    and options.random != "random"
    and options.random != "shuffle"
):
    sys.stderr.write("invalid mode for random: % s\n" % options.random)
    sys.exit()

# outfile and outdir given ?
if options.outfile is None:
    ohandle = sys.stdout
else:
    ohandle = open(options.outfile, "w")

if random is not None:
    random.seed()

# for e in options.expr:
#    ohandle.write("\"%s\"\t" % e)
# ohandle.write("\n")

for arg in args:
    gb = None
    seq = None
    base, ext = os.path.splitext(arg)

    if ext == ".gb":
        gb = gbfromfile(arg)
        if not gb.is_allowed(options.atax, options.ftax):
            continue

        acc = gb.accession
        tax = " ".join(gb.taxonomy)
        name = gb.name
        seq = gb.sequence
        circ = gb.circular
        code = gb.transl_table

    elif ext == ".fas" or ext == ".fa":
        tmp = sequence_info_fromfile(arg, circular=circ)[0]

        acc = ""
        tax = ""
        name = tmp["name"]
        seq = tmp["sequence"]
        circ = options.circular
        code = options.code

    subs = []
    if options.window is None and gb is None:
        subs.append(
            {
                "seq": seq.subseq(0, len(seq), options.strand),
                "strand": options.strand,
                "name": "complete",
                "start": 0,
                "stop": len(seq),
            }
        )

    elif gb is not None:  # and window or not window
        if options.aname is None and options.atype is None:
            subs.append(
                {
                    "seq": seq.subseq(0, len(seq), options.strand),
                    "strand": options.strand,
                    "name": "complete",
                    "start": 0,
                    "stop": gb.size,
                }
            )
        else:
            features = gb.getfeatures(
                anames=options.aname,
                fnames=options.fname,
                atypes=options.atype,
                ftypes=options.ftype,
            )
            for f in features:

                if options.strand is not None:
                    strand = options.strand
                else:
                    strand = f.strand

                seq = gb.sequence.subseq(f.start, f.stop, strand)

                if options.window is None:
                    subs.append(
                        {
                            "seq": seq,
                            "fstrand": f.strand,
                            "strand": strand,
                            "name": f.name,
                            "start": f.start,
                            "stop": f.stop,
                        }
                    )

                else:
                    # print f, 0, len(seq) - options.window, options.offset
                    for start in range(0, len(seq) - options.window, options.offset):
                        if options.Xfold is not None:
                            w = 3
                            sseq = None
                            while (
                                sseq is None or len(sseq) < options.window
                            ) and start + w <= len(seq):
                                sseq = degenerated_subseq(
                                    seq.subseq(start, start + w, 1),
                                    options.Xfold,
                                    gb.transl_table,
                                )
                                w += 3
                            if w < options.window:
                                continue

                        else:
                            w = options.window

                        sseq = seq.subseq(start, start + w, 1)
                        subs.append(
                            {
                                "seq": sseq,
                                "fstrand": f.strand,
                                "strand": strand,
                                "name": f.name,
                                "start": f.start + start,
                                "stop": f.start + start + w,
                            }
                        )

    elif options.window is not None and gb is None:
        if circ:
            start = 0
            stop = len(seq)
        else:
            start = options.window
            stop = len(seq) - options.window

        for s in range(start, stop, options.offset):
            subs.append(
                {
                    "seq": seq.subseq(
                        s - options.window / 2 + 1,
                        s + options.window / 2,
                        options.strand,
                    ),
                    "strand": options.strand,
                    "name": "window",
                    "start": s - options.window / 2 + 1,
                    "stop": s + options.window / 2,
                }
            )

    else:
        sys.stderr.write("Something is wrong here\n")
        sys.exit()

    #    conseq = sequence("")
    #    for seq, strand in subs:
    #        if options.third:
    #            seq = sequence(seq.data[2::3])
    #        conseq = sequence(conseq.data + seq.data)
    #
    #    if len(conseq) == 0:
    #        sys.stderr.write("error: no sequence selected for the given parameters\n")
    #        exit()
    #
    #    nf = conseq.nucleotide_frequency()
    #    dn = conseq.dinucleotide_frequency()

    for f in subs:
        # if f["name"] != "nad6" :
        #     continue
        # print f["name"], f["seq"]

        if options.Xfold is not None:
            if "fstrand" in f and f["fstrand"] != f["strand"]:
                f["seq"] = str(sequence(f["seq"].reverse_complement()))

            f["seq"] = sequence(
                degenerated_subseq(f["seq"], options.Xfold, gb.transl_table)
            )

            if "fstrand" in f and f["fstrand"] != f["strand"]:
                f["seq"] = str(sequence(f["seq"].reverse_complement()))

        if options.third:
            if "fstrand" in f and f["fstrand"] != f["strand"]:
                f["seq"] = str(sequence(f["seq"])[0::3])
            else:
                f["seq"] = str(sequence(f["seq"])[2::3])

        if options.random == "shuffle":
            f["seq"].shuffle()
        elif options.random == "random":
            f["seq"] = randsequence(len(seq))

        if len(f["seq"]) == 0:
            sys.stderr.write("Warning: skipping empty sequence for %s\n" % (f["name"]))
            continue

        nf = f["seq"].nucleotide_frequency()
        dn = f["seq"].dinucleotide_frequency()

        cmb = {}
        cmb.update(nf)
        cmb.update(dn)

        i = 1
        if options.svm:
            ohandle.write("%d\t" % f["strand"])

        for e in range(len(options.expr)):
            if options.svm:
                ohandle.write("%d:" % i)
            try:
                ohandle.write("%f" % (eval(options.expr[e], cmb)))
                ohandle.write("\t")

            except Exception:
                ohandle.write("NA\t")
                sys.stderr.write("\ncould not eval expr %s\n" % (options.expr[e]))
                sys.stderr.write("for %s\n" % (str(s)))
                for c in list(nf.keys()) + list(dn.keys()):
                    sys.stderr.write("%s:" % c)
                    sys.stderr.write("%s " % (str(cmb[c])))
                sys.stderr.write("\n")
            i += 1

        if options.format != "":
            out = options.format
            out = out.replace("%a", acc)
            out = out.replace("%t", tax)
            out = out.replace("%name", f["name"])
            out = out.replace("%start", str(f["start"]))
            out = out.replace("%stop", str(f["stop"]))
            out = out.replace("%strand", str(f["strand"]))
            out = out.replace("%n", name)

            ohandle.write("%s\t" % out)
        ohandle.write("\n")
    del subs
