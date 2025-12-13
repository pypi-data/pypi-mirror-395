"""
@author: M. Bernt

extract gene orders from Boore's mitochondrial data base in html format
"""

import re
import sys
from optparse import OptionParser

# gene map for all genes (protein coding, rRNA, tRNA)
gene_map = {
    "cox1": "COX1",
    "cox2": "COX2",
    "cox3": "COX3",
    "cob": "CYTB",
    "atp6": "ATP6",
    "atp8": "ATP8",
    "rrnS": "12S",
    "rrnL": "16S",
    "nad1": "ND1",
    "nad2": "ND2",
    "nad3": "ND3",
    "nad4": "ND4",
    "nad4L": "ND4L",
    "nad5": "ND5",
    "nad6": "ND6",
    "A": "A",
    "C": "C",
    "D": "D",
    "E": "E",
    "F": "F",
    "G": "G",
    "H": "H",
    "I": "I",
    "K": "K",
    "L(nag)": "L1",
    "L(yaa)": "L2",
    "N": "N",
    "M": "M",
    "P": "P",
    "Q": "Q",
    "R": "R",
    "S(nct)": "S1",
    "S(nga)": "S2",
    "T": "T",
    "V": "V",
    "W": "W",
    "Y": "Y",
}

usage = "usage: %prog [options] MGAfile.html"
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
parser.add_option(
    "-f",
    dest="format",
    action="store",
    type="string",
    default=">%a\n%g",
    metavar="FORMAT",
    help="output format: %n=name, %a=accession, %g=gene order",
)
parser.add_option(
    "--allowls",
    dest="allowls",
    action="store_true",
    default=False,
    help="allow L and S",
)
parser.add_option(
    "--ignore",
    action="append",
    type="string",
    metavar="NAME",
    help="ignore genes with name NAME",
)

(options, args) = parser.parse_args()

if len(args) != 1:
    sys.stderr.write("MGAfile must be specified\n")
    sys.exit()
filename = args[0]
f = open(filename, "r")

# outfile and outdir given ?
if options.outfile is None:
    ohandle = sys.stdout
else:
    ohandle = open(options.outfile, "w")

if options.ignore is not None:
    for i in options.ignore:
        try:
            gene_map[i] = ""
        except Exception:
            sys.stderr("can't ignore %s, no such gene\n" % i)
            sys.exit()

# ~ log = open(logfilename, 'w')
data = f.read()
data = re.split("<table", data)[3]
data = re.split("<tr", data)

# read the data
extract = []
cnt = 0
for d in data:
    cnt += 1
    if cnt < 3:
        continue

        # reinitialize variables needed per iteration
    error = []
    gene_cnt = {}
    for c in list(gene_map.values()):
        gene_cnt[c] = 0

        # split the data in the current row of the table, and remove spaces etc. as far as possible
    lined = re.split("<td>", d)
    sci_nm = (
        lined[1][: lined[1].find("(complete)</td>")].lstrip().rstrip().replace(" ", "_")
    )
    phylum = lined[2][: lined[2].find("</td>")].lstrip().rstrip()
    taxono = lined[3][: lined[3].find("</td>")].lstrip().rstrip()
    com_nm = lined[4][: lined[4].find("</td>")].lstrip().rstrip()
    accession = lined[5][: lined[5].find("</td>")].lstrip().rstrip()
    geneor = re.split(",", lined[6][: lined[6].find("</td>")])
    notes = lined[7][: lined[7].find("</td>")]

    taxono = taxono.split()
    for t in range(len(taxono)):
        taxono[t] = re.sub(r"[\s,;]", "", taxono[t])

    metaidx = taxono.index("Metazoa")

    if len(taxono) - metaidx < metaidx:
        taxono = taxono[: metaidx + 1]
        taxono.reverse()
    else:
        taxono = taxono[metaidx:]

    # remove spaces from the genes and empty genes ,
    # remove genes which are not in gene_map
    # and count the number of occurences of each gene in the genome
    for g in range(len(geneor) - 1, -1, -1):
        geneor[g] = geneor[g].lstrip().rstrip()
        if len(geneor[g]) < 1:
            del geneor[g]
            continue
        if geneor[g][0] == "-":
            sign = "-"
            x = geneor[g][1:]
        else:
            sign = ""
            x = geneor[g]

        if x in gene_map:
            if gene_map[x] == "":
                # sys.stderr.write("%s\n"% x)
                # sys.stderr.write("%s\n"% str(geneor))
                geneor.remove(geneor[g])
                continue
            geneor[g] = sign + gene_map[x]
            gene_cnt[gene_map[x]] += 1

        elif options.allowls is True and (x == "L" or x == "S"):
            geneor[g] = sign + x
            try:
                gene_cnt[x] += 1
            except KeyError:
                gene_cnt[x] = 1

        else:
            error.append("unk %s, " % x)

        # ~ # check if there is a gene which has not exactly one occurence in the genome
    if options.allowls is True:
        if (
            "S" in gene_cnt
            and gene_cnt["S"] <= 2
            and gene_cnt["S1"] <= 1
            and gene_cnt["S2"] <= 1
            and gene_cnt["S"] + gene_cnt["S1"] + gene_cnt["S2"] == 2
        ):
            del gene_cnt["S"]
            gene_cnt["S1"] = 1
            gene_cnt["S2"] = 1
        if (
            "L" in gene_cnt
            and gene_cnt["L"] <= 2
            and gene_cnt["L1"] <= 1
            and gene_cnt["L2"] <= 1
            and gene_cnt["L"] + gene_cnt["L1"] + gene_cnt["L2"] == 2
        ):
            del gene_cnt["L"]
            gene_cnt["L1"] = 1
            gene_cnt["L2"] = 1

    for g in list(gene_map.values()):
        if g == "":
            continue
        if gene_cnt[g] > 1:
            error.append("mul %s, " % g)
        if gene_cnt[g] == 0:
            error.append("miss %s, " % g)

    # geneor = " ".join(geneor)
    extract.append(
        {
            "sciname": sci_nm,
            "phylum": phylum,
            "taxonomy": taxono,
            "comname": com_nm,
            "accession": accession,
            "geneorder": geneor,
            "error": error,
        }
    )

extract.sort(lambda x, y: x["taxonomy"] < y["taxonomy"])


for i in range(len(extract)):
    if options.ftax is not None:
        found = False
        for t in options.ftax:
            if t in extract[i]["taxonomy"]:
                found = True
                break
        if found:
            sys.stderr.write("%s forbidden taxonomy\n" % (extract[i]["accession"]))
            continue

    if options.atax is not None:
        found = False
        for t in options.atax:
            if t in extract[i]["taxonomy"]:
                found = True
                break
        if not found:
            sys.stderr.write("%s not allowed taxonomy\n" % (extract[i]["accession"]))
            continue

    if len(extract[i]["error"]) != 0:
        for e in extract[i]["error"]:
            sys.stderr.write("%s %s\n" % (extract[i]["accession"], e))
        continue

    out = options.format
    out = out.replace("%a", extract[i]["accession"])
    out = out.replace("%n", extract[i]["sciname"])
    out = out.replace("%g", " ".join(extract[i]["geneorder"]))
    out = out.replace("%t", " ".join(extract[i]["taxonomy"]))

    #    if gb.feature_number(atypes=["gene","rRNA","tRNA"]) != 37\
    #        or not gb.uniq_genes(atypes=["gene","rRNA","tRNA"]) \
    #        or not gb.resolved_LS():

    #        sys.stderr.write("%s\n"%out)
    #        continue
    #
    ohandle.write("%s\n" % out)

f.close()

# outfile and outdir given ?
if options.outfile is not None:
    ohandle.close()
