"""
@author: M. Bernt

Generate the files needed for blasting
"""

import argparse
import glob
import logging
import os.path
import sys

from mitos import bedfile, gb
from mitos.update import prepareFiles


def main():
    usage = "generate blast data bases from the genbank files in a directory"

    parser = argparse.ArgumentParser(description=usage)

    parser.add_argument(
        "--indir", action="append", required=True, metavar="DIR", help="input directory"
    )
    parser.add_argument(
        "--beddir",
        action="append",
        required=False,
        metavar="DIR",
        help="input bed directory",
    )

    parser.add_argument(
        "--outdir",
        action="store",
        required=True,
        metavar="DIR",
        help="output directory",
    )
    parser.add_argument(
        "--codss",
        action="store",
        type=float,
        metavar="FRACTION",
        default=0.01,
        help="minimum fraction of appearances of a codon (per gene and code) as start/stop to be accepted as start/stop",
    )
    parser.add_argument(
        "--codin",
        action="store",
        type=float,
        metavar="FRACTION",
        default=0.001,
        help="maximum fraction of appearances of a codon (per gene and code) as inner codon to be accepted as stop",
    )
    parser.add_argument(
        "--keepin",
        action="store_true",
        default=False,
        help="keep statistics on inner codons in dumped data",
    )
    parser.add_argument(
        "--maxentries",
        action="store",
        type=int,
        metavar="N",
        default=None,
        help="maximum number of sequences to store in the database (only used for testing)",
    )

    args = parser.parse_args()

    logging.basicConfig(format="%(levelname)s - %(message)s", level=logging.DEBUG)

    gbfiles = []
    bedfiles = []

    for id in args.indir:
        gbfiles += glob.glob("%s/*.gb" % (id))
    if args.beddir:
        for id in args.beddir:
            bedfiles += glob.glob("%s/*.bed" % (id))

    data = []
    for i, gbfile in enumerate(gbfiles):
        if args.maxentries is not None and i >= args.maxentries:
            logging.warning("abort after %d entries" % args.maxentries)
            break

        data.append(gb.gbfromfile(gbfile))

        if args.beddir is None:
            continue

        b = os.path.splitext(os.path.basename(gbfile))[0]
        bed = None
        for bedf in bedfiles:
            if b in bedf:
                bed = bedf
                break
        if bed is None:
            sys.stderr.write("no bed found for %s" % b)
            sys.exit()
        beddata = bedfile.bedfromfile(bed)
        data[-1].features = beddata.features

    prepareFiles(data, args.outdir, args.codss, args.codin, args.keepin)


if __name__ == "__main__":
    main()
