"""
@author: M. Bernt

does the protein prediction and writes fasta output
(let ABC be the base name of the input file and XYZ the name of a predicted gene)

input/output files:
- ABC/blast/prot/ABC.XYZ.blast (the original BLAST output)
  if not present these files are created, otherwise they are used
- XYZ.aa.fas: aminoacid sequence of the (best) prediction
  sequences are appended
- XYZ.nt.fas: nucleotide sequence of the (best) prediction
  sequences are appended
- genes.tab: absence/presence tabular
  data is appended
- ABC/ABC.bed bed output of the best predictions
- ABC/blast/prot/plot/XYZ/[+-123]
  ABC/blast/prot/plot/XYZ_[+-123].ps
  of --plot then plots and original output per reading frame

@author: maze
"""

from optparse import OptionGroup, OptionParser
from os import listdir, mkdir
from os.path import basename, exists, isdir, isfile, splitext
from random import choice, shuffle
from sys import exit, stderr

from Bio import Data

from mitos import mito
from mitos.bedfile import bedwriter
from mitos.blast import blastx
from mitos.gb import gbfromfile
from mitos.sequence import sequence, sequence_info_fromfile
from mitos.update import singleblastx

usage = """%prog [options] fasta files/fasta directory"
    predicts proteins with blastx, and writes the aminoacid sequences

genetic code:
- if genbank file with same name is found the code specified there is assumed
- otherwise the genetic code specified with --code is assumed
circularity is assumed to circular per default:
- if genbank file with same name is found the circularity is taken from there
- otherwise default circularity is assumed (can be set to linear with --linear)
"""
parser = OptionParser(usage)
parser.add_option(
    "--code",
    action="store",
    type="int",
    metavar="CODE",
    help="assume genetic code CODE, must be given or genbank file with same name ",
)
parser.add_option(
    "--linear",
    dest="circular",
    action="store_false",
    default=True,
    help="set default circularity to linear",
)
parser.add_option(
    "-r",
    "--refdir",
    dest="refdir",
    action="store",
    type="str",
    default="",
    help="the dir where the reference data is found",
)

blastopt = OptionGroup(parser, "blast input, position creation")
blastopt.add_option(
    "-e",
    "--minevalue",
    action="store",
    type="int",
    default=2,
    metavar="P",
    help="accept only blast hits with log(e-value) >= p (default: 2)",
)
blastopt.add_option(
    "-c",
    "--cutoff",
    action="store",
    type="string",
    default="%50",
    metavar="X",
    help="cutoff value; if an integer is given then the value is used as cutoff value, if the integer is preceeded with '%' the cutoff is computed for each initial hit as percentage of the maximum height (default %50)",
)
blastopt.add_option(
    "-s",
    "--score",
    dest="scoresel",
    action="store",
    type="string",
    default="e",
    help="what is to be used as score of a position. e:evalue, b:bitscore, h:height (default: e)",
)
blastopt.add_option(
    "--pavg",
    action="store_true",
    default=False,
    help="take value at a position as average (default: sum)",
)
parser.add_option_group(blastopt)

inithitopt = OptionGroup(parser, "initial hit creation")
inithitopt.add_option(
    "--havg",
    action="store_true",
    default=False,
    help="compute score of the initial hits as average (default: sum)",
)
parser.add_option_group(inithitopt)

outopt = OptionGroup(parser, "output options")
outopt.add_option(
    "-d",
    "--dir",
    action="store",
    type="string",
    default="/tmp/",
    metavar="DIR",
    help="use temporary directory DIR (default: /tmp/)",
)
outopt.add_option(
    "--plot", action="store_true", default=False, help="create plots (default: off)"
)
outopt.add_option(
    "--debug",
    action="store_true",
    default=False,
    help="print debug messages (default: off)",
)
parser.add_option_group(outopt)

(options, args) = parser.parse_args()

files = []  # input files
for arg in args:
    if isfile(arg):
        if not arg.endswith(".fas"):
            stderr.write("ignore %s: no fasta file\n")
            continue
        files.append(arg)
    elif isdir(arg):
        for f in listdir(arg):
            if isfile(arg + "/" + f) and f.endswith(".fas"):
                files.append(arg + "/" + f)

if len(files) == 0:
    stderr.write("no files given\n")
    exit()

files = [splitext(x)[0] for x in files]
shuffle(files)

directory = options.dir

minevalue = options.minevalue
cutoff = options.cutoff

i = 0

aafiles = {}
ntfiles = {}

tab = open("%s/genes.tab" % (directory), "a")
# tab.write( "%s\n" % ( " ".join( sorted( mito.prot ) ) ) )

for f in files:
    stderr.write("%s\n" % f)

    gb = None
    if exists(f + ".gb"):
        gb = gbfromfile(f + ".gb")

    if options.code is not None:
        code = options.code
    elif gb is not None:
        code = gb.transl_table
    else:
        stderr.write("no genbank file and no code specified for %s -> skipping\n" % f)
        continue

    if options.circular is not None:
        circ = options.circular
    elif gb is not None:
        circ = gb.circular
    else:
        stderr.write(
            "no genbank file and no circularity specified for %s -> assuming circular\n"
            % f
        )
        circ = True

    seq = sequence_info_fromfile(f + ".fas", circular=circ)
    if len(seq) > 1:
        stderr.write(
            "%d fasta sequeces found in %s -> only taking first\n" % (len(seq), f)
        )
    if len(seq) == 0:
        stderr.write("no fasta sequences found in %s -> skipping\n" % (f))
        continue
    seq = seq[0]

    if gb is not None:
        name = gb.name
        acc = gb.accession
    else:
        name = seq["name"]
        acc = seq["id"]

    seq = seq["sequence"]

    base = basename(f)
    brpath = "%s/%s/" % (directory, base)

    # check for too many N's in the sequence
    freq = seq.nucleotide_frequency(osb=False)
    freqsum = 0.0
    for letter in freq:
        if letter in Data.IUPACData.unambiguous_dna_letters:
            continue
        freqsum += freq[letter]
    if freqsum > 0.05:
        stderr.write("%s %f%% non standard bases -> abort\n" % (acc, freqsum))
        exit()
    elif freqsum > 0:
        stderr.write("%s %f%% non standard bases\n" % (acc, freqsum))

    # start blast if blast output directory does not exist
    if 1:
        if not exists(brpath + "/blast/prot/"):
            mkdir("%s/%s" % (directory, base))
            brpath = singleblastx(f + ".fas", code, brpath, options.refdir)
        else:
            brpath = brpath + "/blast/prot/"
        protlist = blastx(
            brpath,
            cutoff=cutoff,
            minevalue=minevalue,
            acc=None,
            code=code,
            fastafile=f + ".fas",
            sqn=acc,
            circular=circ,
            plot=options.plot,
            debug=options.debug,
            scoresel=options.scoresel,
            pavg=options.pavg,
            havg=options.havg,
        )

    #    except:
    #        stderr.write( "%s: BLAST error\n" % ( f ) )
    #        continue

    #    dump = open( brpath + ".out", "w" )
    protdict = dict()
    for p in range(len(protlist)):
        # stdout.write( "%s\n" % protlist[p] )
        if protlist[p].copy is None:
            copy = 0
        else:
            copy = protlist[p].copy
        if protlist[p].part is None:
            part = 0
        else:
            part = protlist[p].part

        if protlist[p].name not in protdict:
            protdict[protlist[p].name] = dict()
        if copy not in protdict[protlist[p].name]:
            protdict[protlist[p].name][copy] = dict()
        protdict[protlist[p].name][copy][part] = p

    #    dump.close()

    # write tabular file indicating which gene was found
    for n in sorted(mito.prot):
        if n in protdict:
            tab.write("%d," % (len(protdict[n])))
        else:
            tab.write("0,")
    tab.write(" %s " % f)
    if exists(f + ".gb"):
        tab.write("%s" % (",".join(gb.taxonomy[2:5])))
    tab.write("\n")
    tab.flush()

    for name in list(protdict.keys()):

        if len(protdict[name]) == 1:
            continue

        bestcopy = []
        bestval = 0  # best score
        for copy in list(protdict[name].keys()):
            v = 0.0
            el = 0
            for part in list(protdict[name][copy].keys()):
                el += protlist[protdict[name][copy][part]].length(circ, len(seq))
                v += protlist[protdict[name][copy][part]].score

            if options.havg:
                v /= el

            if v >= bestval:
                if v > bestval:
                    bestval = v
                    bestcopy = []
                bestcopy.append(copy)

        for copy in list(protdict[name].keys()):
            if copy not in bestcopy:
                del protdict[name][copy]

    # write bed file
    bedlist = []
    for name in list(protdict.keys()):
        for copy in list(protdict[name].keys()):
            for part in list(protdict[name][copy].keys()):
                bedlist.append(protlist[protdict[name][copy][part]])
    bedlist.sort(key=lambda x: x.start)
    bedwriter(bedlist, base, outfile="%s/%s/%s.bed" % (directory, base, base))
    del bedlist

    # write fasta files
    for name in protdict:
        # choose a random of the remaining copies
        copy = choice(list(protdict[name].keys()))
        p = protlist[protdict[name][copy][0]]
        ntseq = sequence("")
        for part in protdict[name][copy]:
            q = protlist[protdict[name][copy][part]]
            # get nucleotide sequence
            ntseq += seq.subseq(q.start, q.stop, q.strand)

        # write nucleotid sequence
        if p.name not in ntfiles:
            ntfiles[p.name] = open("%s/%s.nt.fas" % (directory, p.name), "a")
        ntfiles[p.name].write(
            ">%s %s %d %d %d (%d)\n"
            % (acc, p.name, p.start, p.stop, p.strand, len(protdict[name][copy]))
        )
        ntfiles[p.name].write("%s\n" % (ntseq.data))
        ntfiles[p.name].flush()

        if len(ntseq) % 3 != 0:
            stderr.write("%s %s %d%%3=%d\n" % (f, p, len(ntseq), len(ntseq) % 3))

        # get aminoacid translation
        # and remove final stop if there is one (internal stops are left in the
        # seq
        aaseq = ntseq.translate(table=code, stop_symbol="*", to_stop=False)
        if aaseq[-1] == "*":
            aaseq = aaseq[:-1]

        stpcnt = aaseq.count("*")
        stppos = aaseq.find("*")
        if stpcnt != 0 and stppos != len(aaseq) - 1:
            stderr.write("%s %s has internal stop codons\t" % (f, p.name))
            stderr.write("%s\t" % (str(ntseq)))
            stderr.write("%s\n" % (str(aaseq)))

        # write aminoacid sequence
        if p.name not in aafiles:
            aafiles[p.name] = open("%s/%s.aa.fas" % (directory, p.name), "a")
        aafiles[p.name].write(
            ">%s %s %d %d %d (%d)\n"
            % (acc, p.name, p.start, p.stop, p.strand, len(protdict[name][copy]))
        )
        aafiles[p.name].write("%s\n" % (aaseq.data))
        aafiles[p.name].flush()

        # TODO if there is an internal stop codon then mark as pseudo -> in the
        # blast x function

        # TODO use length statistic of the data base to determine too
        # short/long gene

    i += 1

tab.close()

for p in ntfiles:
    ntfiles[p].close()
for p in aafiles:
    aafiles[p].close()
