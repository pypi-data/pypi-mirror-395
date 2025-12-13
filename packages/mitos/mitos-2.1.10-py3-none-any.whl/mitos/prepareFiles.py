"""
@author: M. Bernt
"""

import glob
import os
import sys
from optparse import OptionParser

from mitos.gb import gbfromfile

usage = "usage: %prog dir"
parser = OptionParser(usage)

parser.add_option(
    "-d",
    "--dir",
    action="store",
    type="string",
    metavar="DIR",
    help="directory with *.gb files",
)
(options, args) = parser.parse_args()

if options.dir is None:
    print("no input directory given")
    print(usage)
    sys.exit(1)

feature_nuc_path = options.dir + "/featureNuc/"
feature_prot_path = options.dir + "/featureProt/"

# create nuc and prot directories
print(
    "create directories for nucleotide features (%s) and for protein features (%s)"
    % (feature_nuc_path, feature_prot_path)
)
if os.path.exists(feature_nuc_path):
    print("directory %s already exists - removing old files" % (feature_nuc_path))
    # remove all outdated files in this directory
    os.system("rm %s*" % (feature_nuc_path))
else:
    os.system("mkdir %s" % (feature_nuc_path))

if os.path.exists(feature_prot_path):
    print("directory %s already exists - removing old files" % (feature_prot_path))
    # remove all outdated files in this directory
    os.system("rm %s*" % (feature_prot_path))
else:
    os.system("mkdir %s" % (feature_prot_path))

print("done")

for file in glob.glob("%s*.gb" % (options.dir)):
    print(file)

    gbdata = gbfromfile(file)

    # build fasta file for genbank file
    acc = gbdata.accession
    name = gbdata.name
    sequence = str(gbdata.sequence)
    output = ">%s %s\n%s" % (acc, name, sequence)
    out_file = "%s.fas" % acc

    #    try:
    #        f = open(out_file, "w")
    #        f.write(output)
    #        f.close()
    #    except:
    #        sys.stderr.write("error: could not write to file %s" % out_file)
    #        sys.exit()

    # formatdb fastafile
    os.system("formatdb -i %s -o -p F" % (out_file))

    # prepare featurefiles - all sequences for one gene gathered in one multifasta file
    #    features = gbdata.getfeatures()
    #    for feature in features:
    #        fname = feature.name
    #        fstart = feature.start
    #        fstop = feature.stop
    #        fstrand = feature.strand
    #        feature_nuc_file = feature_nuc_path + fname + ".fas"
    #
    #        seq = gbdata.sequence.subseq(fstart, fstop, fstrand)
    #        output = ">%s:%d-%d %s\n%s\n" % (acc, fstart, fstop, name, str(seq))
    #
    #        fh = open(feature_nuc_file, "a")
    #        fh.write(output)
    #        fh.close
    #
    #        #prepare fastafiles with proteins
    #        if feature.translation != None:
    #            feature_prot_file = feature_prot_path + fname + ".fas"
    #            prot_output = ">%s:%d-%d %s\n%s\n" % (acc, fstart, fstop, name, str(feature.translation))
    #            fh = open(feature_prot_file, "a")
    #            fh.write(prot_output)
    #            fh.close

    print("%s done" % file)

# formatdb new created fastafiles

# featureNuc
os.system("for i in %s/*.fas; do formatdb -i $i -o -p F; done" % (feature_nuc_path))
print("formatdb for feature nucs done")

# featureProt
os.system(
    "for i in %s/*.fas; do formatdb -i $i -o; done" % (feature_prot_path)
)  # -p T is default
print("formatdb for feature prots done")
