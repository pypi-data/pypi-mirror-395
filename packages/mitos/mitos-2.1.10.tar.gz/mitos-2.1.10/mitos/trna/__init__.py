"""
@author: M. Bernt
"""

from Bio import Data
from Bio.Seq import Seq

from mitos.sequence import sequence

trna_nameaamap = {
    "Ala": "A",
    "Arg": "R",
    "Asn": "N",
    "Asp": "D",
    "Cys": "C",
    "Glu": "E",
    "Gln": "Q",
    "Gly": "G",
    "His": "H",
    "Ile": "I",
    "Leu": "L",
    "Lys": "K",
    "Met": "M",
    "Phe": "F",
    "Pro": "P",
    "Ser": "S",
    "Thr": "T",
    "Trp": "W",
    "Tyr": "Y",
    "Val": "V",
}


class CodonError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "Invalid Anticodon / Codon " + self.value


# note for codons
# annotated strand     : codon
# mRNA                 : codon

# tRNA                 : anticodon
# sense strand tRNAgene: anticodon !!!

# in the code table also the codon is given
class codon(sequence):
    def __init__(self, seq, tpe, name=None, transl_table=None):
        """
        init a codon from codon / anticodon sequence
        a) name==None: set seq and type explicitely
        b) name!=None: given seq and name guess the type
           in this case tpe will be used as default if the name did
           not help

        param seq a D/RNA sequence of length 3 (a string)
        param tpe specify if seq is the codon or anticodon
        param name get the type with the help of the name
        param transl_table
        """

        # codon must be of length 3
        if len(seq) != 3:
            raise CodonError(seq)

        # get forward and complement of the sequence
        seq = seq.replace("U", "T").replace("u", "t")

        # print "codon init", tpe, seq, name
        if name is not None and transl_table is not None:

            # start with the anti codon, since in the trnX(...) format
            # more often the anticodon is given.
            # this reduces errors for trnS where for UCU it can not be
            # determined if it is anticodon NCT (L1) or codon TCN (L2)
            for t in ["anticodon", "codon"]:
                c = codon(seq, t)
                aa = c.get_aa(transl_table)
                #                print c, aa, name
                if aa is not None and name.startswith("trn" + aa):
                    tpe = t
                    #                    print "GUESS", t, c
                    break

        # replace possible Us .. this is unfortunately inconsistent
        # in the genbankfile .. but be want to have it as DNA .. so ..
        if tpe == "anticodon":
            seq = str(sequence(seq, circular=False, upper=True).reverse_complement())
        elif tpe != "codon":
            raise Exception("InvalidType" + str(tpe))

        sequence.__init__(self, seq, circular=False, upper=True)

    def get_anticodon(self):
        """
        return the anticodon as string
        """
        return str(Seq(str(self)).reverse_complement())

    def get_codon(self):
        """
        return the codon as string
        """
        return str(self._data)

    def get_aa(self, transl_table):
        """
        determine for which aminoacid the stored codon codes
        @param[in] transl_table int
        @return - the corresponding aa
            - '*' for stop codons
            - '?' else
        """
        # print "get_aa", str(self)

        table = Data.CodonTable.ambiguous_dna_by_id[transl_table]
        # aa = ""

        try:
            return table.forward_table.get(self._data)
        except Data.CodonTable.TranslationError:
            pass

        #        if self._data in table.start_codons:
        #            aa += "start"

        if self._data in table.stop_codons:
            return "*"

        return "?"

    def isstart(self, transl_table):
        """
        check if the codon is a start codon
        """

        table = Data.CodonTable.unambiguous_dna_by_id[transl_table]
        if str(self) in table.start_codons:
            return True
        else:
            return False

    def isstop(self, transl_table):
        """
        check if the codon is a stop codon
        """

        table = Data.CodonTable.unambiguous_dna_by_id[transl_table]
        if str(self) in table.stop_codons:
            return True
        else:
            return False


L1 = codon("CTN", "codon")
L2 = codon("TTR", "codon")

S1 = codon("AGN", "codon")
S2 = codon("TCN", "codon")
