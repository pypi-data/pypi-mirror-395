#!/usr/bin/venv python

"""
@author: M. Bernt

create a nice output of genetic codes
"""

import sys
from optparse import OptionParser

from Bio.Data import CodonTable


class MinimalTerminalController:
    """
    A class to generate formatted output to a terminal using ANSI escape sequences.
    For simplicity, only the features which are used by gcpp.py are implemented
    """

    def __init__(self, term_stream=sys.stdout):
        if term_stream.isatty():
            self.REVERSE = "\033[7m"  # inverted colours
            self.RED = "\033[31m"  # red
            self.NORMAL = "\033[0m"  # reset format
        else:
            # no formatting for non-TTY
            self.REVERSE = ""
            self.RED = ""
            self.NORMAL = ""


def main():
    usage = """%prog [OPTIONS] list of genetic codes
    gcpp outputs the given or all standard genetic codes:
    - first 3 lines gives the codons
    - then one line per genetic code (*: stop, inverted text: start)

    if a reference genetic code is given, the differences are shown
    """
    parser = OptionParser(usage)
    parser.add_option(
        "-r",
        "--ref",
        action="store",
        type="int",
        metavar="CODE",
        help="reference genetic code",
    )
    (options, args) = parser.parse_args()

    term = MinimalTerminalController()
    bases = ["T", "C", "A", "G"]
    for i in range(3):
        sys.stdout.write("   ")
        for x in bases:
            for y in bases:
                for z in bases:
                    triple = x + y + z
                    sys.stdout.write(triple[i])
        sys.stdout.write("\n")

    codes = []
    for a in args:
        try:
            CodonTable.unambiguous_dna_by_id[int(a)]
            codes.append(int(a))
        except (KeyError, ValueError):
            sys.stderr.write("unknown genetic code", a)

    if len(codes) == 0:
        codes = list(range(1, 24))

    for i in codes:
        try:
            CodonTable.unambiguous_dna_by_id[i]
        except KeyError:
            continue

        sys.stdout.write("%.2d " % i)
        for x in bases:
            for y in bases:
                for z in bases:
                    if x + y + z in CodonTable.unambiguous_dna_by_id[i].start_codons:
                        sys.stdout.write(term.REVERSE)

                    if options.ref is not None and (
                        (
                            x + y + z
                            in CodonTable.unambiguous_dna_by_id[
                                options.ref
                            ].start_codons
                        )
                        != (
                            x + y + z
                            in CodonTable.unambiguous_dna_by_id[i].start_codons
                        )
                    ):
                        sys.stdout.write(term.RED)

                    try:
                        if (
                            options.ref is not None
                            and CodonTable.unambiguous_dna_by_id[
                                options.ref
                            ].forward_table[x + y + z]
                            != CodonTable.unambiguous_dna_by_id[i].forward_table[
                                x + y + z
                            ]
                        ):

                            sys.stdout.write(term.RED)

                        sys.stdout.write(
                            CodonTable.unambiguous_dna_by_id[i].forward_table[x + y + z]
                        )

                    except KeyError:
                        sys.stdout.write("*")
                    sys.stdout.write(term.NORMAL)

        sys.stdout.write("\n")


if __name__ == "__main__":
    main()
