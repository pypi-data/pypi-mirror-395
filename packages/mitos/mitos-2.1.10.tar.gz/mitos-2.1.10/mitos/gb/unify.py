"""
@author: M. Bernt
"""

import logging
import re

from Bio.Data import IUPACData

from mitos import mito, trna


def unify_name_intron(name, default):
    """
    identify intron type
    @param default default name (function is supposed to be called only for intron features)
    """
    nm = name.lower().strip()
    m = re.search("^group (?P<type>[i]{1,2})", nm)
    if m is not None:
        d = m.groupdict()
        return "gp" + d["type"].upper()
    m = re.search("^type (?P<type>[i]{1,2})", nm)
    if m is not None:
        d = m.groupdict()
        return "gp" + d["type"].upper()

    return default


def unify_name_orf(name):
    """
    identify orfs
    """
    nm = name.lower().strip()

    m = re.search(r"^(?P<type>[hfm]{0,1})[ -]{0,1}orf(?P<number>\d*)", nm)
    if m is not None:
        d = m.groupdict()
        return d["type"] + "orf" + d["number"]

    return None


def unify_name_origin(name, default, isori=False):
    """
    try to get a unified name for the origins

    @param name the name to parse
    @param default default origin type if isori=True
    @param is_ori indicate if this is supposed to be an origin
                  if set the parser will try to add the type
    """

    nm = name.upper()
    # print "?ORI", nm, isori

    m = re.search("ORI[ -]{0,1}(L|H)", nm)
    if m is not None:
        # print m.re.pattern
        if m.group(1) == "H":
            return "OH"
        elif m.group(1) == "L":
            return "OL"

    # this would be to loss if searched (e.g. OL in polymerase)
    m = re.match("O[ -]{0,1}(L|H)", nm)
    if m is not None:
        # print m.re.pattern
        if m.group(1) == "H":
            return "OH"
        elif m.group(1) == "L":
            return "OL"

    m = re.search("D-LOOP", nm)
    if m is not None:
        # print m.re.pattern
        isori = True

    m = re.search("CONTR?OL.*REGION", nm)
    if m is not None:
        # print m.re.pattern
        isori = True

    # replication|replicating origin
    m = re.search("REPLI.*(ORIGIN|START)", nm)
    if m is not None:
        # print m.re.pattern
        isori = True

    # origin replication|replicating
    m = re.search("(START|ORIGIN).*REPLI", nm)
    if m is not None:
        # print m.re.pattern
        isori = True

    # AT (rich) region ... but not repeat region
    m = re.search(r"(^|\s)A[+-/ ]{0,1}T[ -](RICH|REGION|DOMAIN)", nm)
    if m is not None:
        # print m.re.pattern
        isori = True

    if isori:
        m = re.search("([HL])[ -]{0,1}STRAND", nm)
        if m is not None:
            # print m.re.pattern
            if m.group(1) == "H":
                return "OH"
            elif m.group(1) == "L":
                return "OL"

        m = re.search("(LIGHT|HEAVY|LEADING|LAGGING)", nm)
        if m is not None:
            # print m.re.pattern
            if m.group(1) in ["HEAVY", "LEADING"]:
                return "OH"
            elif m.group(1) in ["LIGHT", "LAGGING"]:
                return "OL"

        return default

    return None


def unify_name_protein(name):
    """
    get a unified name for rRNAs if possible
    param name a gbfile gene name
    return gene name (atp6|8, cox1|2|3, cob, nad1|2|3|4|4l|5|6, heg, mttb, msh1, polB)
    """

    nm = name.lower().strip()

    # ATP
    m = re.match("^atp.*([689])$", nm)
    if m is not None:
        # print "^ATP.*(\d+$)"
        return "atp" + m.group(1)

    # COX
    #    COI CO1
    #    COII CO2
    #    COIII CO3
    #    COX1 CO1
    #    COX2 CO2
    #    COX3 CO3
    #    cytochrome c oxidase subunit 1 CO1
    #    cytochrome c oxidase subunit 2 CO2
    #    cytochrome c oxidase subunit 3 CO3
    #    cytochrome c oxidase subunit I CO1
    #    cytochrome c oxidase subunit II CO2
    #    cytochrome c oxidase subunit III CO3
    #    cytochrome c subunit I CO1
    #    cytochrome c subunit II CO2
    #    cytochrome c subunit III CO3
    #    cytochrome c subunit subunit I CO1
    #    cytochrome c subunit subunit II CO2
    #    cytochrome c subunit subunit III CO3
    #    cytochrome oxidase 1 CO1
    #    cytochrome oxidase 2 CO2
    #    cytochrome oxidase 3 CO3
    #    cytochrome oxidase I CO1
    #    cytochrome oxidase II CO2
    #    cytochrome oxidase III CO3
    #    cytochrome oxidase subunit 1 CO1
    #    cytochrome oxidase subunit 2 CO2
    #    cytochrome oxidase subunit 3 CO3
    #    cytochrome oxidase subunit I CO1
    #    cytochrome oxidase subunit II CO2
    #    cytochrome oxidase subunit III CO3

    m = re.search(r"^cox?([i]+|[123])$", nm)
    if m is not None:
        # print "COX?([I]+|[123])", nm, m.group(1)
        if m.group(1)[0] == "i":
            return "cox" + str(len(m.group(1)))
        else:
            return "cox" + m.group(1)

    # c followed by a non digit character and i..i|123 at the end separated by dash or space
    m = re.match(r"^(c\D*)[ -]([i]+|[123])$", nm)
    if m is not None and not (
        m.group(1).startswith("copy") or m.group(1).startswith("cpoy")
    ):
        # print "^(C\D*)[ -]([I]+|[123]).*$", nm, m.group(2)
        if m.group(2)[0] == "i":
            return "cox" + str(len(m.group(2)))
        else:
            return "cox" + m.group(2)

    #    cytochome b CYTB
    #    cytochrome b CYTB
    #    cob CYTB
    #    Cyt b CYTB
    #    CYTB CYTB
    m = re.match(r"^(apo)?[cyt]{3}.*b$|[cob]{3}$", nm)
    if m is not None:
        # print "^[CYT]{3}|[COB]{3}.*$"
        return "cob"

    # NAD
    m = re.match(r"(nad|nd)\D*(\d+[l]{0,1})$", nm)
    if m is not None:
        # print "[NAD]{2,3}.*([123456][L]*)$"
        return "nad" + str(m.group(2))

    # mttb
    m = re.search(r"mttb", nm)
    if m is not None:
        # print "mttb"
        return "mttb"

    # mutS
    m = re.search(r"muts", nm)
    if m is not None:
        # print "mutS"
        return "msh1"

    # msh1
    m = re.search(r"msh1", nm)
    if m is not None:
        # print "msh1"
        return "msh1"

    # dnaB
    m = re.search(r"dnab|polb|dpob", nm)
    if m is not None:
        # print "dnab"
        return "dpo"

    # polB
    m = re.search(r"(r|d)na[ -]?pol", nm)
    if m is not None:
        if m.group(1)[0] == "r":
            return "rpo"
        else:
            return "dpo"

    # HEG
    m = re.search(r"heg", nm)
    if m is not None:
        # print "heg"
        return "lagli"

    # LAGLIDADG_endonuclease
    # LAGLIDADG
    # putative LAGLI-DADG endonuclease
    # putative LAGLIDADG endonuclease
    m = re.search(r"(la[dg]li|putative la[dg]li.*)", nm)
    if m is not None:
        return "lagli"

    # GIY_endonuclease
    # GIYYIG
    # GIY-YIG_endonuclease
    # putative GIY endonuclease
    # putative GIY-YIG endonuclease
    m = re.search(r"(giy|putative giy.*)", nm)
    if m is not None:
        return "giy"

    # rps3
    # ribosomal_protein_S3
    # mitochondrial_ribosomal_protein_Var1/Rps3
    # var1
    # VAR1
    # var1_ribosomal_protein
    # ribosomal protein 3
    # ribosomal protein subunit 3

    m = re.match(r"^var1|.*(s3|var1)|ribosomal.*(3)", nm)
    if m is not None:
        return "rps3"

    # rsp5
    # ribosomal_protein_S5
    m = re.match(r"^.*s5$", nm)
    if m is not None:
        return "rps5"

    return None


def unify_name_rrna(name, rRNAs):
    """
    get a unified name for rRNAs if possible
    @param name a gbfile gene name
    @param rRNAs the present rRNAs
    """
    # @todo: allow 15S 21S etcpp???
    nm = name.upper().strip()

    # RRNA
    m = re.search(r".*(12S|15S|16S|21S|23S).*", nm)
    if m is not None:
        if rRNAs is None:
            return m.group(1)

        # this assigns the following cases to rrnS and rrnL
        # 12S 16S
        # 16S 23S
        # 15S 21S
        # if 16S is found but not 23S then rrnL is assumed
        if m.group(1) == "12S":
            return "rrnS"
        elif m.group(1) == "16S":
            if "23S" in rRNAs:
                return "rrnS"
            else:
                return "rrnL"
        elif m.group(1) == "23S":
            return "rrnL"
        elif m.group(1) == "15S":
            return "rrnS"
        elif m.group(1) == "21S":
            return "rrnL"
        else:
            logging.error("unknown rRNA type %s" % m.group(1))

    #         if m.group(1) == "12S":
    #             return "rrnS"
    #         elif m.group(1) == "16S":
    #             return "rrnL"

    m = re.search("([SL]{1})-?R?RNA", nm)
    if m is not None:
        if m.group(1) == "S":
            return "rrnS"
        elif m.group(1) == "L":
            return "rrnL"

    m = re.match(r"^R?RNR?([LS12]{1})\b", nm)
    if m is not None:
        if m.group(1) == "S" or m.group(1) == "1":
            return "rrnS"
        elif m.group(1) == "L" or m.group(1) == "2":
            return "rrnL"

    m = re.search("(SMALL|LARGE).*RNA.*", nm)
    if m is not None:
        if m.group(1) == "SMALL":
            return "rrnS"
        elif m.group(1) == "LARGE":
            return "rrnL"

    m = re.search(".*RNA.*(SMALL|LARGE)", nm)
    if m is not None:
        if m.group(1) == "SMALL":
            return "rrnS"
        elif m.group(1) == "LARGE":
            return "rrnL"

    m = re.search("(L|S)SU", nm)
    if m is not None:
        if m.group(1) == "S":
            return "rrnS"
        elif m.group(1) == "L":
            return "rrnL"

    return None


def unify_name_trna(name, transl_table):
    """
    get a unified name for rRNAs if possible
    param name a gbfile gene name
    return (name, anticodon) where the components are None if they can not be determined
    """
    nm = name.upper().strip()

    if nm in list(mito.trnamap.keys()):
        return mito.trnamap[nm], None

    #    print "->", nm

    re_anticodon = r"[ -]{0,1}[(]{0,1}(?P<ac>[%s]{3}){0,1}[)]{0,1}[EF]{0,1}" % (
        IUPACData.ambiguous_dna_letters + "U"
    )
    re_name_long = r"\[{0,1}(?P<trna>%s)(?P<number>\d{0,1})\]{0,1}" % (
        "|".join([x.upper() for x in list(mito.trnamap.keys())])
    )
    re_name_short = r"(?P<trna>[%s])(?P<number>\d{0,1})" % (IUPACData.protein_letters)

    retn = None
    reta = None
    # tRNA specified with 3 letter aa code (e.g. Ser)
    # tRNA[Asn]
    for pfx in ["TRNA", "TRN"]:
        m = re.match("^" + pfx + "[ -]{0,1}" + re_name_long + re_anticodon + "$", nm)
        if m is not None:
            d = m.groupdict()
            #            print m.re.pattern, d
            if d["trna"] + d["number"] in mito.trnamap:
                retn = mito.trnamap[d["trna"] + d["number"]]
            elif d["trna"] in mito.trnamap:
                retn = mito.trnamap[d["trna"]]

            if d["ac"] is not None:
                reta = trna.codon(d["ac"], "anticodon", retn, transl_table)

            return retn, reta

    # tRNA specified with 1 letter aa code
    for pfx in ["TRNA", "TRN"]:
        m = re.match("^" + pfx + "[ -]{0,1}" + re_name_short + re_anticodon + "$", nm)
        if m is not None:
            d = m.groupdict()
            #            print m.re.pattern, d
            if "trn" + d["trna"] + d["number"] in mito.trna:
                retn = "trn" + d["trna"] + d["number"]
            elif "trn" + d["trna"] in mito.trna:
                retn = "trn" + d["trna"]

            if d["ac"] is not None:
                reta = trna.codon(d["ac"], "anticodon", retn, transl_table)

            return retn, reta

    return None, None


def feature_type(name):
    """
    determine the type of a feature given its unified name
    param name the unified name
    return "gene" (for proteins), "rRNA", "tRNA", "rep_origin", or None if unknown
    """

    if name is None:
        return None

    return mito.type_from_name(name)


#    elif name.startswith("ATP" ) or name.startswith("COX" ) or name.startswith("ND" ) or name == "CYTB":
#        return "gene"
#    elif name == "12S" or name == "16S":
#        return "rRNA"
#    elif name == "OL" or name == "OH":
#        return "rep_origin"
#    elif name in trnamap.values():
#        return "tRNA"
#    else:
#        return None
