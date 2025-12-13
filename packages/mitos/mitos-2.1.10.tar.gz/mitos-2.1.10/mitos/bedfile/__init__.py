"""
@author: maze
"""

from re import match
from sys import stderr, stdout

from mitos import mito, trna
from mitos.feature import feature
from mitos.gb import gb


class bedfromfile(gb):
    def __init__(self, bedfile):
        """
        copy and part number can be hidden in the feature name of the form
        NAME_COPY_PART with:
        NAME in [a-zA-Z0-9]+
        COPY in [0-9]+ (can be omitted)
        PART in [a-zA-Z] (can be omitted)
        the delimiter can be chosen arbitrarily (but must be the same at both positions and ofcourse non-alnum)

        @param bedfile filename string
        """
        gb.__init__(self)

        bedhandle = open(bedfile)
        for line in bedhandle:
            line = line.split()

            if self.name != "" and self.name != line[0]:
                pass
            self.name = line[0]
            self.accession = line[0]

            if line[5] == "+":
                strand = 1
            else:
                strand = -1

            try:
                score = float(line[4])
            except Exception:
                score = None

            anticodon = None
            #            nsplit = line[3].split('_')

            # parse name, copy, and part
            prm = match(
                r"([a-zA-Z0-9]+)(\([\-atucg]{3}\))?([\-_])?([0-9]+)?([\-_])?([a-zA-Z])?",
                line[3],
            )
            #            tm = match(r"(trn[A-Z])(\([\-atugc]{3}\))?", line[3])
            if prm is None:
                stderr.write("%s: malformed feature name %s\n" % (bedfile, line[3]))
            name = prm.group(1)
            anticodon = prm.group(2)
            if anticodon is not None:
                if anticodon[1:-1] == "---":
                    anticodon = None
                else:
                    anticodon = trna.codon(anticodon[1:-1], "anticodon")

            if prm.group(4) is not None:
                copy = int(prm.group(4))
            else:
                copy = None
            if prm.group(6) is not None:
                part = ord(prm.group(6).lower()) - 97
            else:
                part = None

            #            if tm is not None:
            #                name = tm.group(1)
            #                if tm.group(2) != "---":
            #                    anticodon = tm.group(2)
            nf = feature(
                name=name,
                tpe=mito.type_from_name(name),
                method="bedfile",
                start=int(line[1]),
                stop=int(line[2]) - 1,
                strand=strand,
                score=score,
                anticodon=anticodon,
            )

            #            print nf

            nf.copy = copy
            nf.part = part

            self.features.append(nf)

        bedhandle.close()


def bedwriter(featurelist, acc, outfile=None, mode="w"):
    """
    write a bed file
       chrom - The name of the chromosome (e.g. chr3, chrY, chr2_random) or scaffold (e.g. scaffold10671).
       chromStart - The starting position of the feature in the chromosome or scaffold. The first base in a chromosome is numbered 0.
       chromEnd - The ending position of the feature in the chromosome or scaffold. The chromEnd base is not included in the display of the feature. For example, the first 100 bases of a chromosome are defined as chromStart=0, chromEnd=100, and span the bases numbered 0-99.
       name - Defines the name of the BED line. This label is displayed to the left of the BED line in the Genome Browser window when the track is open to full display mode or directly to the left of the item in pack mode.
       score - A score between 0 and 1000.
       strand - Defines the strand - either '+' or '-'.
    @param[in] featurelist the list of features to be written in the bed file
    @param[in] acc string to be prepended to each line (e.g. accession)
    @param[in] outfile file to write into, if None: write to stdout
    @param[in] mode file write mode, e.g. a, w, ...
    """

    featurelist.sort(key=lambda x: x.start)

    if isinstance(outfile, str):
        file = open(outfile, mode)
        for f in featurelist:
            file.write("%s\n" % f.bedstr(acc))
        file.close()
    elif outfile is None:
        for f in featurelist:
            stdout.write("%s\n" % f.bedstr(acc))
    else:
        for f in featurelist:
            outfile.write("%s\n" % f.bedstr(acc))
