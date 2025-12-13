"""
@author: M. Bernt
"""

import logging
import os
import re
import subprocess

from mitos import extprog
from mitos.feature import feature, trnafeature
from mitos.trna import L1, L2, S1, S2, codon, trna_nameaamap


# TODO REMOVE THIS BULLSHIT :)
# and derive from something usefull
class arwenscan:
    def __init__(self):

        self.accession = ""
        self.circular = False
        self.features = []
        self.transl_table = 0

        return

    def _add_feature(
        self,
        name,
        tpe,
        start,
        stop,
        strand,
        translation,
        anticodon,
        anticodonpos,
        sequence,
        score,
        dotbracket,
    ):
        """
        add a feature ..

        """

        nf = feature(
            name,
            tpe,
            start,
            stop,
            strand,
            "arwen",
            translation=translation,
            score=score,
        )
        self.features.append(nf)


class arwenscanparm(extprog.parm):
    def __init__(self, name, tpe, rng=[]):
        extprog.parm.__init__(self, name, tpe, rng)
        self.infix = ""
        self.prefix = "-"


def singleArwenScan(f, **keywords):
    """
    call singleArwenScan
    @param file fastafile for a species, e.g. NC_010202.fas

    Detects metazoan mitochondrial tRNA genes in nucleotide sequences

    -mtmam        Search for Mammalian mitochondrial tRNA
                  genes. -tv switch set.
                  Mammalian mitochondrial genetic code used.
    -mtx          Low scoring tRNA genes are not reported.
    -gcmam        Use Mammalian mitochondrial genetic code.
    -gcmet        Use composite Metazoan mitochondrial genetic code.
    -gcstd        Use standard genetic code.
    -tv           Do not search for mitochondrial TV replacement
                  loop tRNA genes.
    -c7           Search for tRNA genes with 7 base C-loops only.
    -c            Assume that each sequence has a circular
                  topology. Search wraps around each end.
                  Default setting.
    -l            Assume that each sequence has a linear
                  topology. Search does not wrap.
    -d            Double. Search both strands of each
                  sequence. Default setting.
    -s  or -s+    Single. Do not search the complementary
                  (antisense) strand of each sequence.
    -sc or -s-    Single complementary. Do not search the sense
                  strand of each sequence.
    -ps           Lower scoring thresholds to 95% of default levels
    -ps<num>      Change scoring thresholds to <num> percent of default levels
    -rp           Report possible pseudogenes (normalised score < 100).
    -seq          Print out primary sequence.
    -v            Verbose. Prints out information during
                  search to STDERR.
    -a7           Restrict tRNA astem length to a maximum of 7 bases
    -aa           Display message if predicted iso-acceptor species
                  does not match species in sequence name (if present).
    -j            Display 4-base sequence on 3' end of astem
                  regardless of predicted amino-acyl acceptor length.
    -jr           Allow some divergence of 3' amino-acyl acceptor
                  sequence from NCCA.
    -jr4          Allow some divergence of 3' amino-acyl acceptor
                  sequence from NCCA, and display 4 bases.
    -q            Dont print configuration line (which switchs
                  and files were used).
    -rn           Repeat sequence name before summary information.
    -w            Print out in Batch mode.
    -O <outfile>  Print output to <outfile>. If <outfile>
                  already exists, it is overwritten.  By default
                  all output goes to stdout.
    -es           print score
    """

    par = [
        arwenscanparm("O", "file"),
        arwenscanparm("c", "flag"),
        arwenscanparm("seq", "flag"),
        arwenscanparm("w", "flag"),
        arwenscanparm("es", "flag"),
        arwenscanparm("br", "flag"),
        arwenscanparm("gc", "int"),
    ]

    cl = extprog.cmdline(keywords, par)
    pars = str(cl) + f

    p = subprocess.Popen(
        "arwen %s" % (pars),
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.PIPE,
        close_fds=True,
    )

    #     if cl.get("C") == True:
    #         cfile.close()

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
        #        raise extprog.StderrError( "arwenscan %s" % pars, err )
        logging.warning("[arwen] error with file %s: see err.log" % (f))

        errlog = f + "\n" + err
        with open(os.path.dirname(f) + "/arwenScan/err.log", "a") as errfile:
            errfile.write(errlog)


def parse(arwenhandler, code):
    """
    parse single arwenfile (arwen1.2.3) and returns list of tRNAfeatures
    @parm arwenhandler filehandler arwenfile
    @param genetic code (table number), if not given the tRNAs given in the file are just taken
    @return list of trnas
    """
    # set the default variables
    trnas = []
    name = ""
    start = 0
    stop = 0
    strand = 0
    score = 0
    sequence = ""
    struct = ""
    anticodonpos = 0
    anticodon = None

    #    trnas.append( trnafeature( name = "", tpe = "tRNA", start = 0, stop = 0, \
    #                              strand = 0, method = "arwen", score = 0, \
    #                              sequence = "", struct = "", anticodonpos = 0, anticodon = None ) )
    # read the First line and get acc
    line = arwenhandler.readline()
    # check if its normal arwenfile
    if line.startswith(">"):
        # acc = line.split()[0][1:]
        # skip line "N genes found" (no need of information)
        arwenhandler.readline()
    else:
        # If not normal arwen error end exit funktion
        logging.error("arwenfile error")
        return []
    # counts in witch line is next
    # 1 = first line of feature
    # 2 = sequence of feature
    # 3 = struct of feature
    linecounter = 1
    # read the 3. line
    line = arwenhandler.readline()
    while line != "":
        line = line.strip()
        cols = line.split()
        # check it is a new feature
        if linecounter == 1:
            # get start and stop
            start, stop = cols[2].strip("c[]").split(",")
            start, stop = int(start) - 1, int(stop) - 1
            # check if it is a complement strand
            if cols[2][0] == "c":
                strand = -1
            else:
                strand = 1
            # get score
            score = float(cols[3])
            # get anticodon start position
            anticodonpos = int(cols[4])
            # get anticodon
            try:
                anticodon = codon(cols[5].strip("()").upper(), "anticodon")
            except Exception:
                anticodon = None

            # get trna name
            if code is not None and anticodon is not None:
                # get the name from the anticodon
                name = anticodon.get_aa(code)
            else:
                # cols[1] hase format mtRNA-"NAME"
                if cols[1][6:] in trna_nameaamap:
                    name = trna_nameaamap[cols[1][6:]]
                else:
                    name = cols[1][6:]

            # parse name of S
            if name == "S":
                if anticodon == S1:
                    name = "S1"
                elif anticodon == S2:
                    name = "S2"
                else:
                    logging.warning("Non standard Ser %s" % anticodon)

            # parse name of L
            if name == "L":
                if anticodon == L1:
                    name = "L1"
                elif anticodon == L2:
                    name = "L2"
                else:
                    logging.warning("Non standard Leu %s" % anticodon)
            linecounter = 2
        elif linecounter == 2:
            # set sequence
            sequence = line.strip()
            linecounter = 3
        else:
            # read the struckture
            struct = re.sub(r"[ dtvA]", ".", line.strip())
            # Append not displayd point at the end of struckture
            while len(struct) < len(sequence):
                struct += "."

            # create the feature
            trnas.append(
                trnafeature(
                    name=name,
                    tpe="tRNA",
                    start=start,
                    stop=stop,
                    strand=strand,
                    method="arwenscan",
                    score=score,
                    sequence=sequence,
                    struct=struct,
                    anticodonpos=anticodonpos,
                    anticodon=anticodon,
                )
            )
            # set the variables of default
            name = ""
            start = 0
            stop = 0
            strand = 0
            score = 0
            sequence = ""
            struct = ""
            anticodonpos = 0
            anticodon = None
            linecounter = 1
        # read the next line
        line = arwenhandler.readline()
    return trnas
