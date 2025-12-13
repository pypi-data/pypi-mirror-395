#!/usr/bin/venv python

"""
@author: M. Bernt

get infos from a set of gb-files
"""


import sys
from optparse import OptionParser
from os import listdir
from os.path import isdir, isfile

from mitos.gb import gbfromfile

# import pickle


def main():
    usage = "usage: %prog [options] gbfiles"
    parser = OptionParser(usage)
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
        dest="format",
        action="store",
        type="string",
        default=">%a\n%seq",
        metavar="FORMAT",
        help="output format: %n=name, %a=accession, %taxid=taxid, %strain=strain, %c=code table, %seq=sequence, %s=size, %t=taxonomy string, %r=references, %pmid=pubmed ids",
    )
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

    (options, args) = parser.parse_args()

    # check arguments
    # no input files / dirs given?
    if len(args) == 0:
        print("no input file given")
        print(usage)
        sys.exit(1)

    files = []  # input files
    for arg in args:
        if isfile(arg):
            files.append(arg)
        elif isdir(arg):
            for f in listdir(arg):
                if isfile(arg + "/" + f):
                    files.append(arg + "/" + f)
        else:
            sys.stderr.write("skipping %s\n" % arg)

    if len(files) == 0:
        sys.stderr.write("no files given\n")
        sys.exit()

    # outfile and outdir given ?
    if options.outfile is None:
        ohandle = sys.stdout
    else:
        ohandle = open(options.outfile, "w")

    for arg in files:
        if arg.endswith(".gb") or arg.endswith(".embl"):
            gb = gbfromfile(arg)
        else:
            sys.stderr.write("skipping %s\n" % arg)
        #    sys.stderr.write( "%s\n" % arg )
        if not gb.is_allowed(options.atax, options.ftax):
            continue

        out = options.format
        out = out.replace("%a", gb.accession)
        out = out.replace("%n", gb.name)
        out = out.replace("%taxid", str(gb.taxid))
        out = out.replace("%strain", gb.strain)
        out = out.replace("%c", str(gb.transl_table))
        out = out.replace("%seq", str(gb.sequence))
        out = out.replace("%s", str(gb.size))
        out = out.replace("%t", " ".join(gb.taxonomy))
        out = out.replace("%r", "\n".join([str(x) for x in gb.references]))
        out = out.replace(
            "%pmid",
            "\n".join([x.pubmed_id for x in gb.references if x.pubmed_id != ""]),
        )

        pids = []
        for x in gb.references:
            if x.pubmed_id != "":
                pids.append(x.pubmed_id)

        out = out.replace("%pid", "\n".join([str(x) for x in pids]))
        ohandle.write("%s\n" % out)

        # for r in gb.references:
        #    print r.authors, r.journal, r.title

    # outfile and outdir given ?
    if options.outfile is not None:
        ohandle.close()


if __name__ == "__main__":
    main()
