"""
@author: M. Bernt
"""

import glob
import logging
import os
import re
import subprocess
import sys

from mitos import extprog
from mitos.feature import trnafeature
from mitos.gb import gbfromfile
from mitos.trna import L1, L2, S1, S2, codon, trna_nameaamap


class trnascanparm(extprog.parm):
    def __init__(self, name, tpe, rng=[]):
        extprog.parm.__init__(self, name, tpe, rng)
        self.infix = " "
        self.prefix = "-"


class StderrError(Exception):
    def __init__(self, prog, stderr):
        self.prog = prog
        self.stderr = stderr

    def __str__(self):
        return "%s has returned an error message:\n %s\n" % (
            repr(self.prog),
            repr(self.stderr),
        )


def getGencodeFromTranl_tableNumber(tableno):

    # print pars
    p = subprocess.Popen(
        "which tRNAscan-SE",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        close_fds=True,
    )

    err = ""
    for i in p.stderr.readlines():
        err += i + "\n"

    if p.returncode != 0 or err != "":
        raise extprog.StderrError("Could not determine tRNAscan-SE path: %s" % (err))

    trnadir = p.stdout.readline()
    table2files = {
        "2": trnadir + "gcode.vertmito",
        "4": trnadir + "gcode.invmito",
        "5": trnadir + "gcode.invmito",
        "9": trnadir + "gcode.echdmito",
        "13": trnadir + "gcode.invmito",
    }
    return table2files[tableno]


def singletrnascan(f, **keywords):
    """
    call trnascan
    param f fastafile for a species, e.g. NC_010202.fas

    -O
        search for organellar (mitochondrial/chloroplast) tRNAs

        This parameter bypasses the fast first-pass scanners that are
        poor at detecting organellar tRNAs and runs Cove analysis only.
        Since true organellar tRNAs have been found to have  Cove  scores
        between  15  and 20 bits, the search cutoff is lowered from 20 to
        15 bits.  Also, pseudogene checking is disabled since it is  only
        applicable  to  eukaryotic  cytoplasmic  tRNA pseudogenes.  Since
        Cove-only mode is used, searches will be very slow (see -C option
        below) relative to the default mode.

    -f  <file>
        save results and Cove tRNA secondary structures  to <file>

        This option saves results and secondary structure information (as
        predicted by the coves program) in <file>.  Use '$' in  place  of
        <file> to send to standard output. An example of the output for-
        mat for one tRNA appears below:

        CELF22B7.trna4 (26992-26920)    Length: 73 bp Type: Phe       Anticodon: GAA at 34-36 (26959-26957)   Score: 73.88
                   *    |    *    |    *    |    *    |    *    |    *    |     *     |
        Seq:   GCCTCGATAGCTCAGTTGGGAGAGCGTACGACTGAAGATCGTAAGGtCACCAGTTCGATCCTGGTTCGGGGCA
        Str:   >>>>>>>..>>>>........<<<<.>>>>>.......<<<<<.....>>>>>.......<<<<<<<<<<<<.

    -q
        quiet mode (credits & run  option  selections  suppressed)

        This  option suppresses the program credits and run option selec-
        tions normally printed to standard error at the beginning of each
        run.
    -b
        brief output format (no column headers)

        This option eliminates column headers that appear by default when
        writing results in tabular output format.  Useful if results  are
        to be parsed or sent to another program.

    -X  <score>

        set Cove cutoff  score  for  reporting  tRNAs  (default=20)

        This  option  allows  the  user to specify a different Cove score
        threshold for reporting tRNAs.  It is not recommended that novice
        users  change  this cutoff, as a lower cutoff score will increase
        the number of pseudogenes and other false positives found by  tR-
        NAscan-SE  (especially when used with the "Cove only" scan mode).
        Conversely, a higher cutoff than 20.0 bits will likely cause true
        tRNAs  to  be missed by tRNAscan (numerous "real" tRNAs have been
        found just above the 20.0 cutoff).  Knowledgable users  may  wish
        to  experiment with this parameter to find unusual tRNAs or pseu-
        dogenes beyond the normal range of detection, keeping the preced-
        ing caveats in mind.

    -g  <file>
        use alternate genetic codes specified in <file> for determining tRNA type

        By  default,  tRNAscan-SE  uses a standard universal codon->amino
        acid translation table that is specified at the end  of  the  tR-
        NAscan-SE.src source file.  In many mitochondrial and a number of
        other microbial organisms, there are exceptions to this universal
        translation  code.  This option allows the user to specify excep-
        tions to the universal code.  Several alternate translation  code
        files are included in this package for convenience:

        gcode.cilnuc
            for Ciliates, Dasycladacean, & Hexamita nuclear tRNAs
        gcode.echdmito
            for Echinoderm mitochondrial tRNAs
        gcode.invmito
            for Invertibrate mitochondrial tRNAs
        gcode.othmito
            for Mold, Protozoans, & Coelenterate mitochondrial tRNAs
        gcode.vertmito
            for Vertibrate mitochondrial tRNAs
        gcode.ystmito
            for Yeast mitochondrial tRNAs

    -Q
        do not prompt user before overwriting  pre-existing files

        By default, if an output result file to be written to already ex-
        ists, the user is prompted whether the file should be  over-writ-
        ten  or  appended  to.   Using this options forces overwriting of
        pre-existing files without an interactive  prompt.   This  option
        may  be handy for batch-processing and running tRNAscan-SE in the
        background.



    """

    cfile = None  # constraints file

    par = [
        trnascanparm("O", "flag"),
        trnascanparm("g", "file"),
        trnascanparm("b", "flag"),
        trnascanparm("q", "flag"),
        trnascanparm("X", "int"),
        trnascanparm("f", "file"),
        trnascanparm("Q", "flag"),
    ]
    cl = extprog.cmdline(keywords, par)

    pars = str(cl) + f
    # print pars
    p = subprocess.Popen(
        "tRNAscan-SE %s" % (pars),
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.PIPE,
        close_fds=True,
    )
    if cfile is not None:
        p.stdin.write(cfile.read())

    if cl.get("C") is True:
        cfile.close()

    err = ""
    for i in p.stderr.readlines():
        if (
            i == ""
            or re.match(r"^\d+ sequences; length of alignment \d+\.$", i) is not None
        ):
            continue
        else:
            err += i + "\n"

    if err != "":
        raise extprog.StderrError("trnascan %s" % (pars), err)


def trnascan(d):
    """
    see singletrnascan
    """

    files = glob.glob(d + "*.fas")
    scanpath = d + "tRNAScan"
    if not os.path.exists(scanpath):
        os.mkdir(scanpath)

    i = 0
    for f in files:
        i += 1
        print(f)
        print("%s/%s" % (i, len(files)))
        acc = os.path.basename(f).split(".")[0]
        gbfile = d + acc + ".gb"
        gbdata = gbfromfile(gbfile)
        outfile = d + "tRNAScan/" + os.path.basename(f) + ".ss"
        try:
            gencode = getGencodeFromTranl_tableNumber(str(gbdata.transl_table))
        except Exception:
            logging.debug("Could not determine genetic code for %s" % (f))
            gencode = None

        if gencode is not None:
            singletrnascan(f, Q=True, O=True, b=True, X=5, q=True, f=outfile, g=gencode)
        else:
            singletrnascan(f, Q=True, O=True, b=True, X=5, q=True, f=outfile)


def parse(fh, code):
    """
    parse a tRNAscan output file
    - skip tRNAs reported with introns
    - skip tRNAs reported with unknown anticodon

    @param[in] fh a file handle
    @param genetic code (table number), if not given the tRNAs given in the file are just taken
    @return list of tRNA features
    """

    trnas = []

    intronstart = 0
    intronstop = 0
    skip = False
    start = None
    stop = None
    strand = None
    score = None
    seq = None
    dotbracket = None
    name = None
    anticodonpos = None
    anticodon = None

    for line in fh.readlines():
        line = line.lstrip().rstrip().split()

        # empty line marks start of a new feature
        if not line:
            if skip is False:
                trnas.append(
                    trnafeature(
                        name=name,
                        tpe="tRNA",
                        start=start,
                        stop=stop,
                        strand=strand,
                        method="tRNAscan",
                        score=score,
                        sequence=seq,
                        struct=dotbracket,
                        anticodonpos=anticodonpos,
                        anticodon=anticodon,
                    )
                )
            intronstart = 0
            intronstop = 0
            skip = False
            continue
            # datensatz fertig, schreiben

        # if l[0].startswith('NC_'): #USE THIS LINE
        if (
            line[0].startswith("NC_")
            or line[0].startswith("As_mt_")
            or line[0].startswith("Bc_mt")
            or line[0].startswith("Ec1-6")
            or line[0].startswith("Gg_cons")
            or line[0].startswith("Hf_mt")
            or line[0].startswith("On_mt")
        ):
            #            number = l[0].split( '.' )[-1][4:]

            # trnascan: positions are counted from 1 the first and the last
            # position belongs to the trna
            start = int(line[1].split("-")[0][1:]) - 1
            stop = int(line[1].split("-")[1][:-1]) - 1

            # is start < stop then the sequence if on the reverse complement
            if start > stop:
                start, stop = stop, start
                strand = -1
            else:
                strand = 1

        elif line[0].startswith("Type:"):
            if line[3] == "???":
                skip = True

            anticodon = codon(line[3], "anticodon")
            anticodonpos = int(line[5].split("-")[0])

            if code is not None:
                name = anticodon.get_aa(code)
            else:
                if line[1] in trna_nameaamap:
                    name = trna_nameaamap[line[1]]
                else:
                    name = line[1]

            score = float(line[8])

            if name == "S":
                if anticodon == S1:
                    name = "S1"
                elif anticodon == S2:
                    name = "S2"
                else:
                    name = "S"
                    logging.warning("warning non standard Ser %s" % line[3])

            if name == "L":
                if anticodon == L1:
                    name = "L1"
                elif anticodon == L2:
                    name = "L2"
                else:
                    name = "L"
                    logging.warning("warning non standard Leu %s" % line[3])

            continue

        elif line[0].startswith("Possible"):
            skip = True
            intronstart = int(line[2].split("-")[0][1:]) - 1
            intronstop = int(line[2].split("-")[1][:-1]) - 1
            if intronstart > intronstop:
                intronstart, intronstop = intronstop, intronstart
            continue

        elif line[0].startswith("*"):
            continue

        elif line[0].startswith("Seq"):
            seq = line[1]
            continue

        elif line[0].startswith("Str"):
            # read struckture
            dotbracket = re.sub(">", "(", re.sub("<", ")", line[1]))
            # printing anticodon position in struckture
            #            dotbracket = dotbracket[:anticodonpos-1]+"AAA"+dotbracket[anticodonpos+2:]
            continue

        else:
            logging.error("unexpected line in tRNAscan output {line}".format(line=line))
            sys.exit()

    #    trnas.sort( key = lambda x : x.start )

    return trnas
