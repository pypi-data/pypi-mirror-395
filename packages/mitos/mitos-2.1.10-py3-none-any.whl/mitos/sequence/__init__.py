"""
@author: M. Bernt
"""
from random import choice, shuffle
from sys import stdout
from typing import Dict, List, Optional

from Bio import Data, SeqIO
from Bio.Seq import Seq, translate
from Bio.SeqRecord import SeqRecord


class NoFastaException(Exception):
    """
    Exception to be raised when no Fasta is found.
    """

    def __str__(self):
        """
        print exception
        """
        return "The File is not a Fasta!"


class MultiFastaException(Exception):
    """
    Exception to be raised when a multi Fasta is found.
    """

    def __str__(self):
        """
        print exception
        """
        return "Can not parse multi Fasta!"


class sequence(Seq):
    """
    overwritten from biopython
    - handle circular sequences
    """

    def __init__(self, data, circular=False, upper=False):
        """
        @param[in] upper if true: transform each letter to upper case, else: leave as is
        """

        data = data.strip().upper()
        Seq.__init__(self, data)
        self.circular = circular

    #    def __neq__( self, other ):
    #        """
    #        check two sequences for inequality
    #        """
    #        return ( not self == other )

    def __repr__(self):
        """
        Returns a (truncated) representation of the sequence for debugging.
        """
        if self.circular:
            mode = "circular"
        else:
            mode = "linear"

        if len(self) > 60:
            # Shows the last three letters as it is often useful to see if there
            # is a stop codon at the end of a sequence.
            # Note total length is 54+3+3=60
            return f"{self.__class__.__name__}('{self[:54]}...{self[-3:]}', {mode})"
        else:
            return f"{self.__class__.__name__}({str(self)}, mode)"

    #     def __str__(self):
    #         """
    #         print sequence in fasta format
    #         """
    #         return "%s" %(self.__data)

    def __lshift__(self, other):
        """
        shift the sequence by other (int) to the left
        """
        if not isinstance(other, int):
            raise TypeError(
                "sequence shift with "
                + repr(other)
                + " "
                + repr(type(other))
                + " is impossible"
            )
        if self.circular is False:
            raise TypeError("sequence shift of linear sequence is impossible")

        rdata = "".join([self[(i + other) % len(self)] for i in range(len(self))])
        return sequence(rdata, self.circular)

    def __rshift__(self, other):
        """
        shift the sequence by other (int) to the right
        """
        if not isinstance(other, int):
            raise TypeError(
                "sequence shift with "
                + repr(other)
                + " "
                + repr(type(other))
                + " is impossible"
            )
        if self.circular is False:
            raise TypeError("sequence shift of linear sequence is impossible")

        rdata = "".join([self[(i - other) % len(self)] for i in range(len(self))])
        return sequence(rdata, self.circular)

    def dinucleotide_count(self, osb=True):
        """
        get the dinucleotide count of the sequence
        param osb if true consider only standard bases (ATCG)
        return a dictionary containing the counts
        """
        dn = {}

        for sb1 in Data.IUPACData.unambiguous_dna_letters:
            for sb2 in Data.IUPACData.unambiguous_dna_letters:
                dn[sb1 + sb2] = 0.0

        for i in range(len(self)):
            if not self.circular and (i + 1) >= len(self):
                continue

            ip = (i + 1) % len(self)
            if osb and (
                self[i] not in Data.IUPACData.unambiguous_dna_letters
                or self[ip] not in Data.IUPACData.unambiguous_dna_letters
            ):
                continue
            if not self[i] + self[ip] in dn:
                dn[self[i] + self[ip]] = 0.0
            dn[self[i] + self[ip]] += 1.0
        return dn

    def dinucleotide_frequency(self, osb=True):
        """
        get the dinucleotide count of the sequence
        param osb if true consider only standard bases (ATCG)
        return a dictionary containing the frequencies
        """
        dn = self.dinucleotide_count(osb)
        if self.circular:
            sm = len(self)
        else:
            sm = len(self) - 1

        for k in dn:

            dn[k] /= float(sm)

        return dn

    def isambig(self):
        if "N" in str(self):
            return True
        else:
            return False

    def isequal(
        self,
        other,
        maxac: Optional[int] = None,
        ambiguous_nucleotide_values: Optional[Dict[str, str]] = None,
    ) -> bool:
        """
        check two sequences for equality
        - same type (two sequences)
        - same circularity
        - same data (ambiguities are checkes, i.e. N=A, ...)
        @param self seq
        @param other another seq
        @param maxac maximum number of allowed ambigous positions (in either sequence)
        """

        if not isinstance(self, sequence) or not isinstance(other, sequence):
            return False

        if self.circular != other.circular:
            return False

        if maxac is None or ambiguous_nucleotide_values is None:
            return str(self) == str(other)

        ac = 0
        for i in range(len(self)):
            #            print self[i], other[i]
            # print self[i], other[i], ambiguous_nucleotide_values[other[i] ],
            # ambiguous_nucleotide_values[self[i] ]

            try:
                oa = set(ambiguous_nucleotide_values[other[i]])
            except KeyError:
                oa = set()

            try:
                sa = set(ambiguous_nucleotide_values[self[i]])
            except KeyError:
                sa = set()

            if self[i] == other[i]:
                continue
            elif (self[i] in oa) or (other[i] in sa):
                ac += 1
                continue
            elif not oa.isdisjoint(sa):
                ac += 1
                continue
            else:
                #                print "RETURN FALSE"
                return False
        #         print "RETURN TRUE"

        if maxac is not None and ac > maxac:
            return False
        else:
            return True

    def nucleotide_count(self, osb=True):
        """
        count the number of occurences of a,t,c,g,...
        @param osb iff true only count unambigous dna letters (ATGC)
        """

        nc = {}
        for sb in Data.IUPACData.unambiguous_dna_letters:
            nc[sb] = 0.0

        for i in range(len(self)):
            if osb and (self[i] not in Data.IUPACData.unambiguous_dna_letters):
                continue
            if not self[i] in nc:
                nc[self[i]] = 0.0
            nc[self[i]] += 1.0
            # print "x", self[i]
        return nc

    def nucleotide_frequency(self, osb=True):
        """
        get the frequency of the nucleotides in the sequence
        """
        nc = self.nucleotide_count(osb)
        sm = len(self)
        for k in nc:
            try:
                nc[k] /= float(sm)
            except ZeroDivisionError:
                nc[k] = 0.0

        return nc

    def shuffle(self):
        """
        random shuffle the sequence
        """
        tdata = [x for x in self.data]
        shuffle(tdata)
        self.data = "".join(tdata)

    def subseq(self, start, stop, strand):
        """
        get the subsequence between start and stop
        note: subsequences are always linear

        @param start start index, note counting starts at 0
        @param stop end index, note element at the stop index is included in the sequence
        @param strand +1/-1 get the reverse complement of the sequence if -1 and the sequence if 1
        """

        if strand != 1 and strand != -1:
            #            stderr.write( "Strans" )
            raise Exception("StrandError", "strand is", strand)

        if not self.circular and (start < 0 or stop < 0):
            raise Exception("error: [%d,%d] of linear sequence\n" % (start, stop))

        if not self.circular and (start >= len(self) or stop >= len(self)):
            raise Exception(
                "error: [%d,%d] of linear sequence of length %d\n"
                % (start, stop, len(self))
            )

        if self.circular:
            while start < 0 or stop < 0:
                start += len(self)
                stop += len(self)
            start %= len(self)
            stop %= len(self)

        if self.circular and start > len(self):
            start %= len(self)
        if self.circular and stop > len(self):
            stop %= len(self)

        if start <= stop:
            seq = self.__class__(str(self[start : stop + 1]), circular=False)
        else:
            if self.circular:
                seq = self.__class__(
                    str(self[start:] + self[: stop + 1]), circular=False
                )
            else:
                raise Exception("error: [%d,%d] of linear sequence\n" % (start, stop))

        if strand == -1:
            seq = seq.reverse_complement()
            # @TODO crude fix .. biopython 1.49 complement function returns Seq not sequence
            seq = self.__class__(str(seq), circular=False)

        return seq

    def start_stop_subsequence(self, transl_table, mx=False):
        """
        get (start,stop, strand) tuples of the sequence such that at start is a
        start codon and at end a end codon
        param transl_table the id of the translation table
        param mx only return maximal sequences, i.e. if there are two sequences
        (s1,e) and (s2,e) with s1<s2 then only (s1,e) will be returned
        todo subsequences crossing the 0 .. attention the reading frame calculations
        get tricky
        """

        ret = []
        table = Data.CodonTable.unambiguous_dna_by_id[transl_table]

        # print table

        start_codons = table.start_codons
        stop_codons = table.stop_codons

        # first +strand
        stack = [[], [], []]
        for i in range(len(self) - 2):
            subs = str(self.subseq(i, i + 3, 1))
            if subs in start_codons:
                stack[i % 3].append(i)
            elif subs in stop_codons:
                for s in stack[i % 3]:
                    ret.append((s, (i + 2) % len(self), 1))
                    if mx:
                        break

                stack[i % 3] = []

        # first -strand
        if self.circular is False:
            return ret

        stack = [[], [], []]
        for i in range(len(self) - 1, -1, -1):
            subs = str(self.subseq(i, i + 3, -1))

            if subs in start_codons:
                stack[i % 3].append(i)

            if subs in stop_codons:
                for s in stack[i % 3]:
                    ret.append(((i + 2) % len(self), s, -1))
                    if mx:
                        break
                stack[i % 3] = []

        return ret

    def translate(
        self, table="Standard", stop_symbol="*", to_stop=False, cds=False, gap=None
    ):
        """
        little helper to translate the nucleotide sequence
        adds N until multiple of three and calls biopythons translate foo
        """
        seq = str(self)
        while len(seq) % 3 != 0:
            seq += "N"
        return translate(seq, table, stop_symbol, to_stop, cds)

    def deambig(self) -> List[str]:
        """
        return a list of sequences

        ambiguous_nucleotide_values dictionary mapping characters to strings (sets of characters)
            e.g. Bio.Data.IUPACData.ambiguous_dna_values
        """

        ambiguous_nucleotide_values = {
            "A": "A",
            "C": "C",
            "G": "G",
            "T": "T",
            "U": "U",
            "M": "AC",
            "R": "AG",
            "W": "ATU",
            "S": "CG",
            "Y": "CTU",
            "K": "GTU",
            "V": "ACG",
            "H": "ACTU",
            "D": "AGTU",
            "B": "CGTU",
            "X": "GATUC",
            "N": "GATUC",
        }

        da = []
        for y1 in ambiguous_nucleotide_values[self[0]]:
            for y2 in ambiguous_nucleotide_values[self[1]]:
                for y3 in ambiguous_nucleotide_values[self[2]]:
                    da.append(y1 + y2 + y3)

        return da

    def heavyStrand(self):
        return float(self.count("A") + self.count("G")) / len(self) >= 0.5


class randsequence(sequence):
    def __init__(self, length, alphabet: str, circular=False):
        """
        generate a random sequence of a certain alphabet
        param length how long should the sequence be
        param alphabet
        param circular init as circular
        """
        data = []
        for i in range(length):
            data.append(choice(alphabet))
        data = "".join(data).strip().upper()
        sequence.__init__(self, data, circular)


def sequences_fromfilehandle(handle, circular=False):

    seq = []
    for seq_record in SeqIO.parse(handle, "fasta"):
        #        print seq_record
        #        print dir(seq_record)
        #        print 'annotations', seq_record.annotations
        #        print 'dbxrefs', seq_record.dbxrefs
        #        print 'description' , seq_record.description
        #        print 'features', seq_record.features
        #        print 'format', seq_record.format
        #        print 'id', seq_record.id
        #        print 'name', seq_record.nameSeqIO
        seq.append(sequence(str(seq_record.seq), circular=circular))
        # print seq[-1]

    return seq


def sequences_fromfile(fname, circular=False):
    """
    get a list of sequences found in a fasta file
    """
    handle = open(fname, "r")
    seq = sequences_fromfilehandle(handle, circular)
    handle.close()
    return seq


def sequence_info_fromfilehandle(handle, circular=False):

    seqlist = []
    for seq_record in SeqIO.parse(handle, "fasta"):
        #        raise Exception( str( seq_record ) )
        #        print dir(seq_record)
        #        print 'annotations', seq_record.annotations
        #        print 'dbxrefs', seq_record.dbxrefs
        #        print 'description' , seq_record.description
        #        print 'features', seq_record.features
        #        print 'format', seq_record.format
        #        print 'id', seq_record.id
        #        print 'name', seq_record.name
        seqlist.append(
            {
                "name": seq_record.name.strip(),
                "description": seq_record.description.strip(),
                "sequence": sequence(str(seq_record.seq), circular=circular),
                "id": seq_record.id,
            }
        )

    return seqlist


def sequence_info_fromfile(fname, circular=False):
    """
    get a list of sequences and their names found in a fasta file
    """

    handle = open(fname, "r")
    seqlist = sequence_info_fromfilehandle(handle, circular)
    handle.close()
    return seqlist


def seqlistmaker(sequence, start, stop, strand, acc, name="", code=None, seqlist=[]):
    """
    @param sequence the whole sequence where the part is from. (Bio.Seq.Seq format)
    @param start the start of the part
    @param stop the stop of the part
    @param acc the acc of the species
    @param name the name of the part if ther is a name.
    @param code translate with code, do not translate if None
    @param seqlist A list of sequences, online needet if this sequenz is only a part of bigger list.

    This method cut a part of a big sequence and append it in a list.
    It is needed for a fasta writing with parts of genoms.
    """

    if int(strand) == 1:
        ts = "+"
    else:
        ts = "-"

    # header with or without a name; coordinates as in gff
    out = "{acc}; {start}-{stop}; {strand}; {name}".format(
        acc=acc, start=start + 1, stop=stop + 1, strand=ts, name=name
    )
    #     out += "%s: %d-%d" % ( acc, start + 1, stop + 1 )
    #     if int( strand ) == 1:
    #         out += "+"
    #     else:
    #         out += "-"
    #
    #     if name != "":
    #         out += "; %s" % ( name )

    # set the subsequnc, need a Bio.Seq.Seq format
    mito_frag = sequence.subseq(start, stop, int(strand))

    if code is not None:
        mito_frag = Seq(mito_frag.translate(table=code))

    # Set record with header
    record = SeqRecord(mito_frag, out, "", "")

    seqlist.append(record)
    return seqlist


def fastawriter(featurelist, sequence, code, acc, outputtype, outfile=None, mode="w"):
    """
    @param outputtype fas / faa
    """
    featurelist.sort(key=lambda x: x.start)
    seqlist = []
    for feat in featurelist:
        if outputtype == "faa" and feat.type != "gene":
            continue

        seqlistmaker(
            sequence=sequence,
            acc=acc,
            start=feat.start,
            stop=feat.stop,
            strand=feat.strand,
            name=feat.outputname(),
            code=code,
            seqlist=seqlist,
        )

    if isinstance(outfile, str):
        with open(outfile, mode) as f:
            SeqIO.write(seqlist, f, "fasta")
    elif outfile is None:
        SeqIO.write(seqlist, stdout, "fasta")
    else:
        SeqIO.write(seqlist, outfile, "fasta")
