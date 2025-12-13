#!/usr/bin/venv python

"""
@author: M. Bernt
"""


import sys
from optparse import OptionParser
from os.path import isfile

from mitos.bedfile import bedfromfile
from mitos.gb import gbfromfile
from mitos.mitofile import mitofromfile
from mitos.sequence import sequence_info_fromfile


def parse_args(argv=None):
    """Parse command-line arguments and return options, args."""

    usage = "usage: %prog [options] gb/bed and possibly fas file"
    parser = OptionParser(usage)

    parser.add_option(
        "--linear",
        dest="circular",
        action="store_false",
        default=True,
        help="consider genome circular",
    )
    # parser.add_option( "--code", dest = "code", action = "store", type = "int", help = "genetic code (overwirites the code in gb/embl files)" )
    # parser.add_option( "-o", "--outfile", action = "store", type = "string", metavar = "FILE", help = "write values to FILE (default: stdout)" )

    parser.add_option(
        "-p",
        dest="atype",
        action="append",
        type="string",
        metavar="TYPE",
        help="allow only features of type TYPE",
    )
    parser.add_option(
        "-P",
        dest="ftype",
        action="append",
        type="string",
        metavar="TYPE",
        help="forbid all features of type TYPE",
    )

    parser.add_option(
        "-n",
        dest="aname",
        action="append",
        type="string",
        metavar="NAME",
        help="allow only features with name NAME",
    )
    parser.add_option(
        "-N",
        dest="fname",
        action="append",
        type="string",
        metavar="NAME",
        help="forbid all features with name NAME",
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

    # parser.add_option( "-r", dest = "rot", action = "store", type = "string", metavar = "ROT", default = None, help = "make ROT the 1st feature" )
    parser.add_option(
        "-o",
        dest="offset",
        action="store",
        type="int",
        default=0,
        metavar="OFFSET",
        help="shift coordinates by OFFSET",
    )

    parser.add_option(
        "--gff", dest="gff", action="store_true", default=False, help="output gff"
    )
    parser.add_option(
        "-f",
        dest="format",
        action="store",
        type="string",
        default="> %strand %start %stop %a %name\n%s\n",
        metavar="FORMAT",
        help="output format: %name=feature name, %type=feature type, %start=feature start, %stop=feature end, %strand=feature strand, %s=sequence, %a=accession, %n=name",
    )
    parser.add_option(
        "--max",
        action="store_true",
        default=False,
        help="consider only max score part per gene",
    )
    return parser.parse_args(argv)


def run(options, args):
    """
    Core logic of getfeatures.
    Args:
        options: parsed CLI options (from parse_args)
        args (list[str]): parsed arguments (should be only one input file)

    Returns:
        str: formatted output (FASTA/GFF/etc.)
    """
    output_lines = []
    gbk = None
    fasta_seqs = []

    if options.gff:
        options.format = "%gff\n"

    # check arguments
    # no input files / dirs given?
    if len(args) == 0:
        raise ValueError("no input file given")

    for arg in args:
        if isfile(arg):
            if arg.endswith(".bed"):
                gbk = bedfromfile(arg)
                gbk.circular = options.circular
            elif arg.endswith(".gb") or arg.endswith(".embl"):
                gbk = gbfromfile(arg)
            elif arg.endswith(".fas"):
                seq = sequence_info_fromfile(arg, circular=options.circular)
                if len(seq) == 0:
                    raise RuntimeError(f"no sequence found in {arg}")
                if len(seq) > 1:
                    sys.stderr.write(
                        "Error: more than one sequence found in %s -> taking the first\n"
                        % (arg)
                    )
                fasta_seqs.append(seq[0]["sequence"])
            else:
                gbk = mitofromfile(arg)
        else:
            sys.stderr.write("no such file or directory %s -> skipping\n" % arg)

    if gbk is None:
        raise RuntimeError("no gb/bed/embl input file given (required)")

    if fasta_seqs:
        if len(fasta_seqs) > 1:
            sys.stderr.write(
                "Error: more than one FASTA file given -> taking the first\n"
            )
        gbk.sequence = fasta_seqs[0]
        gbk.size = len(gbk.sequence)

    # if options.code is not None:
    #    gbk.transl_table = options.code

    if not gbk.is_allowed(atax=options.atax, ftax=options.ftax):
        return ""

    if options.gff:
        output_lines.append("#gff-version 3\n")
        output_lines.append("#sequence-region\t%s\t1\t%d\n" % (gbk.accession, gbk.size))

    # #sequence-region    NC_037973    1    16920
    if options.max:
        gbk.dellowscoreparts()

    # ncfeatures = []
    # cpy = 1
    # for i in range( len( gbk.features ) ):
    #     start = ( gbk.features[i].stop + 1 ) % gbk.size
    #     stop = ( ( gbk.features[( i + 1 ) % len( gbk.features )].start ) - 1 ) % gbk.size
    #     name = "nc_" + gbk.features[i].name + "_" + gbk.features[( i + 1 ) % len( gbk.features )].name
    #     if feature.length( start, stop, gbk.circular, gbk.size ) >= feature.length( stop, start, gbk.circular, gbk.size ):
    #         continue
    #     ncfeatures.append( feature.feature( name, "nc", start, stop, 1, "NA",
    #         translation = None, score = None, rf = None, anticodon = None,
    #         copy = cpy, part = None, mito = None ) )
    #     cpy += 1
    # gbk.features += ncfeatures
    # gbk.features.sort( key = lambda x: x.start )

    features = gbk.getfeatures(
        options.aname, options.fname, options.atype, options.ftype
    )

    # if options.rot is not None:
    #
    #     frot = [ x for x in features if x.name == options.rot ]
    #     if len( frot ) > 0:
    #         offset = frot[0].start
    #         for i in range( len( features ) ):
    #             features[i].start = ( features[i].start - offset ) % gbk.size
    #             features[i].stop = ( features[i].stop - offset ) % gbk.size
    #
    #         features = sorted( features, key = lambda k: k.start )

    for f in features:
        part_lists = [x for x in features if x.name == f.name and x.copy == f.copy]
        sorted_part_lists = sorted(part_lists, key=lambda feat: feat.part)

        #     if f.part is not None and f.part > 0:
        #         continue

        # # only for tRNAs, needed so we can add +-10 to split tRNAs ##
        # sorted_part_lists[0].start = sorted_part_lists[0].start-10
        # sorted_part_lists[len(sorted_part_lists)-1].stop = sorted_part_lists[len(sorted_part_lists)-1].stop+10

        if options.offset != 0:
            if options.offset > 0:
                f.start = (f.start + options.offset) % gbk.size
                f.stop = (f.stop + options.offset) % gbk.size
            else:
                f.start = (gbk.size - f.start - options.offset) % gbk.size
                f.stop = (gbk.size - f.stop - options.offset) % gbk.size
                f.start, f.stop = f.stop - 1, f.start - 1

        fin_seq = ""
        out = options.format
        out = out.replace("%taxid", str(gbk.taxid))
        out = out.replace("%name", f.name)
        out = out.replace("%n", gbk.name)
        out = out.replace("%feature", str(f))
        out = out.replace("%type", f.type)
        out = out.replace("%start", str(f.start))
        out = out.replace("%stop", str(f.stop))

        out = out.replace("%strand", str(f.strand))
        if "%trans" in out and f.translation is None:
            continue
        out = out.replace("%trans", str(f.translation))
        out = out.replace("%bed", str(f.bedstr(gbk.accession)))
        out = out.replace("%gff", str(f.gffstr(gbk.accession, features, gbk.size)))
        # out = out.replace( "%tax", gbk.taxonomy[2] )
        out = out.replace("%a", gbk.accession)
        #    out = out.replace( "%n", gbk.name )
        out = out.replace("%c", str(gbk.transl_table))

        if gbk.sequence is not None:
            for p in sorted_part_lists:
                fin_seq += str(gbk.sequence.subseq(p.start, p.stop, p.strand))
        # fin_seq += "\n"

        #     out = out.replace( "%s", str( gbk.sequence.subseq( f.start , f.stop, f.strand ) ) )
        out = out.replace("%s", fin_seq)
        out = out.replace("%len", str(len(fin_seq)))
        #        ss = str( gbk.sequence.subseq( f.start, f.stop, f.strand ) )
        #        out = out.replace( "%s", ss[ 3 * ( len( ss ) / 3 ) :] )

        output_lines.append(out)

    return "".join(output_lines)


def main(argv=None):
    options, args = parse_args(argv)
    try:
        result = run(options, args)
        sys.stdout.write(result)
        return 0
    except Exception as e:
        sys.stderr.write(str(e) + "\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
