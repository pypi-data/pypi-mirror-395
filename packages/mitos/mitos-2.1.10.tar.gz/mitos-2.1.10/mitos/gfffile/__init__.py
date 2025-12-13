"""
@author: M. Bernt
"""

from sys import stdout


def gffwriter(featurelist, acc, size, circular, outfile=None, mode="w"):
    """
    write the gff string for each feature
    @param[in] featurelist a list of features to be written
    @param[in] acc string to be prepended to each line (e.g. accession)
    @param[in] outfile file to write into, if None: write to stdout
    @param[in] mode file write mode, e.g. a, w, ...
    """

    featurelist.sort(key=lambda x: x.start)

    if isinstance(outfile, str):
        outhandle = open(outfile, mode)
    elif outfile is None:
        outhandle = stdout
    else:
        outhandle = outfile

    outhandle.write(
        f"""##gff-version 3
#!gff-spec-version 1.21
{acc}	mitos	region	1	{size}	.	+	.	ID={acc}:1..{size};Is_circular={circular};Name={acc};genome=mitochondrion;mol_type=genomic DNA
"""
    )

    for feature in featurelist:
        outhandle.write("%s\n" % feature.gffstr(acc, featurelist, size))

    if isinstance(outfile, str):
        outhandle.close()
