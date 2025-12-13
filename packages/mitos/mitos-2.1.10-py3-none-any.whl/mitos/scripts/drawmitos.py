#!/usr/bin/env python

"""
@author: M. Bernt
"""

from mitos.bedfile import bedfromfile
from mitos.draw import draw3


def main():
    # TODOs remove glength parameter from mitfi system call and length
    # parameter from cmsearch function

    import argparse

    usage = "%(prog)s [options]"
    parser = argparse.ArgumentParser(prog="drawmitos.py", usage=usage)

    parser.add_argument(
        "-i",
        "--input",
        dest="input",
        action="store",
        help="the input BED file",
        required=True,
    )
    parser.add_argument(
        "-o",
        "--output",
        dest="output",
        action="store",
        required=True,
        help="output PNG file",
    )
    parser.add_argument(
        "-l",
        "--length",
        dest="length",
        type=int,
        action="store",
        required=True,
        help="genome length",
    )
    args = parser.parse_args()

    bed = bedfromfile(args.input)
    draw3(bed.features, args.length, args.output)


if __name__ == "__main__":
    main()
