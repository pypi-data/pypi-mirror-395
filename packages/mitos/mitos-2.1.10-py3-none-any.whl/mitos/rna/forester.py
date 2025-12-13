"""
@author: M. Bernt
"""

import logging
import subprocess

import mitos.extprog as extprog


def RNAforester(sequences, structures, **keywords):
    """
    call RNAforester
    @param sequences a list of sequences
    @param structures a list of structures
    @param keywords parameters for RNAforester
    @return alignment score
       -d                        calculate distance instead of similarity
       -r                        calculate relative score
       -l                        local similarity
       -so=int                   local suboptimal alignments within int%
       -s                        small-in-large similarity
       -m                        multiple alignment mode
       -mt=double                clustering threshold
       -mc=double                clustering cutoff
       -p                        predict structures from sequences
       -pmin=num                 minimum basepair frequency for prediction
       -pm=int                   basepair(bond) match score
       -pd=int                   basepair bond indel score
       -bm=int                   base match score
       -br=int                   base mismatch score
       -bd=int                   base indel score
       --RIBOSUM                 RIBOSUM85-60 scoring matrix
       -cmin=double              minimum basepair frequency for consensus structure
       -2d                       generate alignment 2D plots in postscript format
       --2d_hidebasenum          hide base numbers in 2D plot
       --2d_basenuminterval=n    show every n-th base number
       --2d_grey                 use only grey colors in 2D plots
       --2d_scale=double         scale factor for the 2d plots
       --score                   compute only scores, no alignment
       --fasta                   generate fasta output of alignments
       -f=file                   read input from file
       --noscale                 suppress output of scale
    """
    # print sequences
    # print structures
    evalpar = [
        extprog.shortparm("d", "flag"),
        extprog.shortparm("r", "flag"),
        extprog.shortparm("l", "flag"),
        extprog.shortparm("so", "int"),
        extprog.shortparm("s", "flag"),
        extprog.shortparm("m", "flag"),
        extprog.shortparm("mt", "float"),
        extprog.shortparm("mc", "float"),
        extprog.shortparm("p", "flag"),
        extprog.shortparm("pmin", "int"),
        extprog.shortparm("pm", "float"),
        extprog.shortparm("pd", "float"),
        extprog.shortparm("bm", "float"),
        extprog.shortparm("br", "float"),
        extprog.shortparm("bd", "float"),
        extprog.shortparm("cmin", "float"),
        extprog.shortparm("2d", "flag"),
        extprog.shortparm("f", "file"),
        extprog.longparm("RIBOSUM", "flag"),
        extprog.longparm("2d_hidebasenum", "flag"),
        extprog.longparm("2d_basenuminterval", "int"),
        extprog.longparm("2d_grey", "flag"),
        extprog.longparm("2d_scale", "float"),
        extprog.longparm("score", "flag"),
        extprog.longparm("fasta", "flag"),
        extprog.longparm("noscale", "flag"),
    ]

    iput = ""
    if len(sequences) != len(structures):
        raise Exception(
            "RNAforester need equal number of sequences and structures or one of them has to be single"
        )

    for i in range(len(sequences)):
        iput += sequences[i] + "\n" + structures[i] + "\n"
    iput += "@\n"

    cl = extprog.cmdline(keywords, evalpar)
    pars = str(cl)
    p = subprocess.Popen(
        "RNAforester %s" % (pars),
        shell=True,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, stderr = p.communicate(iput)

    # evaluate the output
    err = stderr.splitlines()
    if len(err) > 0:
        logging.error(
            "RNAforester returned an error message for:\n%s\n%s" % (iput, err)
        )

    lines = stdout.splitlines()

    score = []
    for i in range(len(lines)):

        if lines[i].find("score") == -1:
            continue

        if cl.get("r") is not None:
            score.append(float(lines[i + 1]))
        else:
            score.append(float((lines[i].split())[-1]))

    return score
