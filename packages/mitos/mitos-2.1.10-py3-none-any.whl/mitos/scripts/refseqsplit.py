#!/usr/bin/venv python

"""
@author: M. Bernt

program to split a given refseq file (containing the concatenation of all
genbank files) into its components
additionally a prefix and taxonomy filter can be applied
"""


import argparse
import logging
from sys import exit

from mitos import update


def main():
    usage = "splits a genbank file"
    parser = argparse.ArgumentParser(description=usage)

    parser.add_argument(
        "-f", "--file", action="store", metavar="FILE", help="read from FILE"
    )
    parser.add_argument(
        "-d", "--dir", action="store", metavar="DIR", help="write files to DIR"
    )
    parser.add_argument(
        "-p",
        "--prefix",
        action="store",
        metavar="PFX",
        help="only take accession with prefix PFX (default: NC)",
    )
    parser.add_argument(
        "-t",
        dest="atax",
        action="append",
        metavar="TAX",
        help="allow only entries with TAX in the taxonomy",
    )
    parser.add_argument(
        "-T",
        dest="ftax",
        action="append",
        metavar="TAX",
        help="forbid all entries with TAX in the taxonomy",
    )
    parser.add_argument(
        "-v",
        dest="verbose",
        default=0,
        action="count",
        help="increment output verbosity; may be specified multiple times",
    )

    # parser.add_argument( "-v", action = "store_true", dest = "verbose", default = False, help = "be verbose" )
    args = parser.parse_args()

    logging.basicConfig(level=max(logging.WARNING - (args.verbose * 10), 10))

    if args.file is None:
        logging.error("no file given")
        exit(1)
    if args.dir is None:
        logging.error("error: no dir given")
        exit(1)

    update.refseqsplit(
        args.file,
        args.dir,
        prefix=args.prefix,
        atax=args.atax,
        ftax=args.ftax,
        maxentries=False,
    )


if __name__ == "__main__":
    main()
