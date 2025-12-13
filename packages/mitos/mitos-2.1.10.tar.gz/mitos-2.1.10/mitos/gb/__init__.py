"""
@author: M. Bernt
"""

import logging
import re
import sys
from os.path import splitext
from typing import TYPE_CHECKING

from Bio import Data, Seq, SeqIO

from mitos import feature, sequence
from mitos.gb import unify
from mitos.trna import L1, L2, S1, S2, CodonError, codon

if TYPE_CHECKING:
    from Bio.SeqFeature import SeqFeature


class gb:
    def __init__(self):

        self.accession = None
        self.circular = False
        self.comment = ""
        self.commonname = ""
        self.complete = False
        self.data_file_division = ""  # INV MAM PRI ROD VRT
        self.date = ""
        self.features = []
        self.name = None
        self.references = []  # list of references .. use biopython class
        # data members: number, bases, authors, consrtm, title, journal,
        # medline_id, pubmed_id, remark
        self.sequence = None
        self.size = 0
        self.taxid = None
        self.strain = ""
        self.taxonomy = []  # taxonomy list
        self.transl_table = 0
        self.version = 0

        return

    def _add_feature(self, nf):
        """
        add a feature ..
        """
        self.features.append(nf)

    def abspre(self, genes):
        """
        return a string describing the absence or presence of genes
        @param genes the genes to check for (a list of names)
        @return comma separated list giving the number of occurences of the genes (sorted by name)
        """

        gdict = {}
        for g in genes:
            gdict[g] = 0

        for f in self.features:
            try:
                gdict[f.name] += 1
            except KeyError:
                gdict[f.name] = 1

        return ",".join([str(gdict[g]) for g in sorted(genes)])

    def dellowscoreparts(self):
        """
        delete all parts except one of the same name (those with best score)
        """

        bestscores = {}
        for f in self.features:
            if f.name not in bestscores or (
                (f.type == "gene" and bestscores[f.name] < f.score)
                or (f.type != "gene" and bestscores[f.name] > f.score)
            ):
                bestscores[f.name] = f.score

        i = 0
        while i < len(self.features):
            if (
                self.features[i].name in bestscores
                and bestscores[self.features[i].name] != self.features[i].score
            ):
                #                print self.features[i]
                del self.features[i]
            else:
                i += 1

    def getfeatures(
        self, anames=None, fnames=None, atypes=None, ftypes=None, astrand=None
    ):
        """
        get a list of features
        param anames list of allowed feature names (None: everything allowed)
        param fnames list of forbidden feature names (None: nothing forbidden)
        param atypes list of allowed feature types (None: everything allowed)
        param ftypes list of forbidden feature types (None: nothing forbidden)
        param astrand allowed strand (None: both strands allowed)
        return list of features
        """

        return [
            x
            for x in self.features
            if x.is_allowed(anames, fnames, atypes, ftypes, astrand)
        ]
        # return [ x for x in self.features if (x.name in name) or (x.type in
        # name) ]

    def geneorder(
        self, anames=None, fnames=None, atypes=None, ftypes=None, signed=True
    ):
        """
        get the gene order as list
        param atypes list of allowed feature types (None: everything allowed)
        param ftypes list of forbidden feature types (None: nothing forbidden)
        param signed make the gene order signed (default: True)
        """

        features = self.getfeatures(
            anames=anames, fnames=fnames, atypes=atypes, ftypes=ftypes
        )
        order = []
        for f in features:
            if signed is True and f.strand < 0:
                # order.append( "-" + f.getname() )
                order.append("-" + f.name)
            else:
                # order.append( f.getname() )
                order.append(f.name)
        return order

    def is_allowed(self, atax=None, ftax=None):
        """
        checks if the gb file to certain taxonomic groups
        param atax list of allowed taxonomic groups or a string of a group
        param ftax forbidden taxonomic groups
        return true iff gb in atax and gb not in ftax
        """

        if isinstance(atax, str):
            atax = [atax]
        if isinstance(ftax, str):
            ftax = [ftax]

        if atax is not None and len([x for x in atax if x in self.taxonomy]) == 0:
            return False
        elif ftax is not None and len([x for x in ftax if x in self.taxonomy]) > 0:
            return False

        return True

    def start_stop_subsequence(self, mx=False):
        """
        get (start,stop, strand) tuples of the sequence such that at start is a
        start codon and at end a end codon
        param max only return maximal sequences, i.e. if there are two sequences
        (s1,e) and (s2,e) with s1<s2 then only (s1,e) will be returned
        """
        return self.sequence.start_stop_subsequence(self.transl_table, mx)


class gbfromfile(gb):
    def __init__(self, gbfile):
        """
        @param gbfile: filename string

        1. parse circular/linear (from residue_type)
           circular iff residue_type ends with "circular"
        2. parse accession and version (from accession, version, and locus)
           accession is taken directly, version is parsed from the string given
           by accession.version, additional warnings are printed if the accession
           is not equal to the locus or the accession part of the version string
        3. parse the complete property and the name of the species
           (from definition, organism, and source)
           - if definition contains the string "complete" the complete property is set
           - name is set to the content of organism
           - a warning is written if source does not start with 'mitochondrion '+name
           - if source ends with ')' then the common name is taken from the
             parenthesised part
        4. size, comment, data_file_division, date, references, taxonomy  is taken directly
           from the corresponding entries of the record
        5. sequence is taken directly from sequence with ambiguous DNA (IUPAC) alphabet
        6. transl_table is parsed from all features with a key "transl_table"
           - if not exactly one is found (but different or none) a warning is printed
           - the one of the found translation tables is returned
        7. the taxid is parsed from source feature (as the qualifier of the key db_xref)
        8. for each of features (parts):
        8a. the locations are parsed recursively given some string describing the location
            and the currently active strand initialized to +1:
           - for a string join(x) or order(x) the method is recursively called
             for each part of the contained comma separated list x (keeping the active strand as is)
           - for a string complement(x) the method is recursively called for x
             (with the currently active strand inverted)
           - otherwise all numbers are parsed from the string and a position is added
               on the currently active strand
             * if one number n is found a location [n,n]
             * if two numbers n,m are found a location [n,m] is added on
             * otherwise an error message is printed
        8b. get the translation from the key "translation" as a linear sequence
            with extended amino acid alphabet (IUPAC)
        8c. get a list of possible names
            specialized methods for the extraction of the name of tRNA, rRNA, proteins,
            and origins are applied on certain values (of key,value pairs) depending
            on the feature type:
            - qualifier key "gene" or "product" and feature type
              * feature type is "tRNA" or "gene"  -> tRNA function
              * feature type is "rRNA" or "gene"  -> rRNA function
              * feature type is "CDS" or "gene"  -> protein function
            - qualifier key "standard_name", "note", or "direction"
              * feature type either "rep_origin", "D-loop", "misc_feature"
            each function checks a list of regular expressions. if one matches the
            corresponding name is appended to a list of possible names of the feature.
            - if the list has length 0
              * if feature type is "rep_origin" or "D-loop"
                -> OH is returned if strand is +1 and OL if it is -1
              * else None is returned
            - if the list is longer than 1 None is returned
            - if the list has length 1
              - if the name is L or S it is tries to parse the anticodon
                from the feature to distinguish L1, L2, S1, S2
              the name is returned
        8d. depending on the determined name the feature type is determined
        8e. if the feature part name could be determined  then the parts (all determined
            locations) are appended to the list of features as follows:
            - all previously added features of the same name are checked
            i) if there is a feature which is included in the new feature then the
              new feature is not added to the list (idea: we take the parts of the
              features, instead of the complete one)
            ii) if there is a feature which is included the new one then the feature
              is deleted (and the new feature might be appended depending on
               the following checks)
            if all checks are done and i) never applied then the feature is added
        """
        gb.__init__(self)

        #        record = GenBank.RecordParser().parse( gbhandle )
        extparsemap = {".gb": "genbank", ".gbk": "genbank", ".embl": "embl"}
        extension = splitext(gbfile)[1]
        if extension in extparsemap:
            parser = extparsemap[extension]
        else:
            raise Exception("Unknown Extension", extension)
        gbhandle = open(gbfile, "r")
        record = SeqIO.read(gbhandle, parser)
        gbhandle.close()
        #        print dir( record )
        #        print "annotations", record.annotations
        #        print "dbxref", record.dbxrefs
        #        print "descriptions", record.description

        #        print "format", record.format
        #        print "id", record.id
        #        print "letter_annotations", record.letter_annotations
        #        print "lower", record.lower
        #        print "name", record.name
        #        print "seq", record.seq
        #        print "upper", record.upper
        #        self._parse_circular( record.residue_type )

        # logging.warning( "using True as default for circular" )
        self.circular = True
        self._parse_accession_version(record.annotations)
        # print self.accession

        self._parse_complete(record.description)
        self._parse_names(record.annotations)

        # size of the chromosome = length of the sequence
        # thus, sequence[size-1] gives the last element of the sequence
        self.size = int(len(record.seq))
        try:
            self.sequence = sequence.sequence(str(record.seq), self.circular)
        except Seq.UndefinedSequenceError:
            self.sequence = sequence.sequence("N" * self.size, self.circular)

        try:
            self.comment = record.annotations["comment"]
        except Exception:
            self.comment = ""

        self.data_file_division = record.annotations["data_file_division"]
        try:
            self.date = record.annotations["date"]
        except Exception:
            self.date = ""

        self.references = record.annotations["references"]

        self.taxonomy = record.annotations["taxonomy"]

        # get the coding table
        self._parse_transl_table(record.features)

        #        print "features", record.features

        # determine in a first round the set of features that are present
        # this is needed to decide which or the rRNA is the small and which the
        # large
        rRNAs = set()
        for f in record.features:
            name = self._parse_feature_name(f, 1, None)
            if name is None or (name not in ["12S", "15S", "16S", "21S", "23S"]):
                continue
            rRNAs.add(name)
        #         print "rRNAs", rRNAs

        _cpymap = {}
        for f in record.features:

            if f.type == "source":
                self._parse_source(f)
                continue
            # print "============="
            # feature types found in metazoan gb files
            # - definitely of interest
            #    CDS
            #    * D-loop                displacement loop; a region within mitochondrial DNA in which a short stretch of RNA is paired with one strand of DNA, displacing the original partner DNA strand in this region; also used to describe the displacement of a region of one strand of duplex DNA by a single stranded invader in the reaction catalyzed by RecA protein
            #    gene                region of biological interest identified as a gene and for which a name has been assigned;
            #    * rRNA                mature ribosomal RNA; RNA component of the ribonucleoprotein particle (ribosome) which assembles amino acids into proteins.
            #     * rep_origin            origin of replication; starting site for duplication of nucleic acid to give two identical copies
            #    * tRNA                mature transfer RNA, a small RNA molecule (75-85 bases long) that mediates the translation of a nucleic acid sequence into an amino acid sequence;
            # - maybe of interest
            #    misc_feature        region of biological interest which cannot be described by any other feature key; a new or rare feature;
            #    repeat_region        region of genome containing repeating units;
            #    repeat_unit            single repeat element;
            #    source                identifies the biological source of the specified span of the sequence; this key is mandatory; more than one source key per sequence is allowed; every entry/record will have, as a minimum, either a single source key spanning the entire sequence or multiple source keys, which together, span the entire sequence.
            #    stem_loop            hairpin; a double-helical region formed by base-pairing between adjacent (inverted) complementary sequences in a single strand of RNA or DNA.
            # - most likely uninteresting
            #    3'UTR                region at the 3' end of a mature transcript (following the stop codon) that is not translated into a protein;
            #    conflict             independent determinations of the "same" sequence differ at this site or region;
            #    exon                region of genome that codes for portion of spliced mRNA, rRNA and tRNA; may contain 5'UTR, all CDSs and 3' UTR;
            #    gap                    gap in the sequence
            #    intron                a segment of DNA that is transcribed, but removed from within the transcript by splicing together the sequences (exons) on either side of it;
            #    misc_difference        feature sequence is different from that presented in the entry and cannot be described by any other Difference key (conflict, unsure, old_sequence, variation, or modified_base);
            #    promoter            region on a DNA molecule involved in RNA polymerase binding to initiate transcription;
            #    STS                    sequence tagged site; short, single-copy DNA sequence that characterizes a mapping landmark on the genome and can be detected by PCR; a region of the genome can be mapped by determining the order of a series of STSs;
            #    unsure                author is unsure of exact sequence in this region;
            # variation            a related strain contains stable mutations
            # from the same gene (e.g., RFLPs, polymorphisms, etc.) which
            # differ from the presented sequence at this location (and possibly
            # others);

            #            strand, start, stop = self._parse_feature_location( f.location )

            loc = self._parse_feature_locations(f)

            #            copy = None
            # print f

            for i in range(len(loc)):
                start = loc[i][0]
                stop = loc[i][1]
                strand = loc[i][2]

                name = self._parse_feature_name(f, strand, rRNAs)
                # anticodon = self._parse_feature_anticodon(f, strand)
                tpe = unify.feature_type(name)
                #                 for x in ["gene", "product", "standard_name", "note", "direction", "anticodon", "codon_recognized"]:
                #                     try:
                #                         print f.qualifiers[x], "|",
                #                     except:
                #                         print "|",
                #                 print "->"
                #                 print "->", self.accession, start, stop, strand
                # print "->", "name: ", name, tpe, strand, start, stop

                # ignore features if name or type could not be determined
                if name is None or tpe is None:
                    continue

                #                # ignore protein (related) features which are not CDS
                #                # like exons, introns, ...
                #                if name in mito.prot and f.type != "CDS":
                #                    continue

                if i == 0 or tpe == "intron":
                    if name not in _cpymap:
                        _cpymap[name] = 0
                    else:
                        _cpymap[name] += 1
                if _cpymap[name] > 0:
                    copy = _cpymap[name]
                else:
                    copy = None

                # introns are not present as joins but have a /number qualifier
                #                 number = self._parse_number( f )
                # print number
                # set the part number for multi part features
                #                 if number is not None:
                #                     part = number
                if tpe != "intron" and len(loc) > 1:
                    part = i
                else:
                    part = None

                # set the translation for the first part of a feature
                # otherwise the translation might be reported multiple times
                if part is None or part == 0:
                    translation = self._parse_translation(f)
                else:
                    translation = None

                if tpe == "tRNA":
                    codon = self._parse_feature_codon(f, strand, True)
                    if len(codon) == 1:
                        acodon = codon[0]
                    else:
                        acodon = None

                else:
                    acodon = None

                nf = feature.feature(
                    name,
                    tpe,
                    start,
                    stop,
                    strand,
                    "GenBank",
                    translation,
                    anticodon=acodon,
                    copy=copy,
                    part=part,
                )
                #                self._add_smaller_feature( nf )
                self._add_feature(nf)
                # print "newlen", len( self.features )

        # correct copy numbers
        for n in set([x.name for x in self.features]):
            copies = set([x.copy for x in self.features if x.name == n])
            copies = list(copies)

            copymap = {}
            if len(copies) == 0:
                raise Exception("parser error 0 copies of a gene")
            elif len(copies) == 1 and copies[0] is None:
                continue
            elif len(copies) == 1 and copies[0] is not None:
                copymap[copies[0]] = None
            else:
                nc = 0
                for c in copies:
                    copymap[c] = nc
                    nc += 1

            for g in self.features:
                if g.name != n:
                    continue
                g.copy = copymap[g.copy]

        #                print "===> ", len( self.features ), nf
        #            print "-----------------    "

        # else:
        #    print nf, "==", self.features[-1]

        # if name is None:
        #    if f.key in ["CDS","gene","tRNA"]:
        #        print f
        # print name, tpe
        # self._control_features()
        # print len(self.features)
        # if len(self.features) > 39:
        #    print self.accession, len(self.features)
        #    for f in self.features:
        #        print f

        #         for f in self.features:
        #             print f
        return

    def _add_smaller_feature(self, nf):
        """
        add a feature:
        - the feature is added if it does not include feature with the same
          name and strand
        - features that include the new feature are deleted

        the feature will be inserted such that the list of features is sorted in increasing order (by start positions)
        """

        #        print "add", nf
        i = 0
        while i < len(self.features):
            #            print i
            if not self.features[i].equal_name_type(nf):
                i += 1
                continue

            if self.features[i].name != nf.name:
                if nf.name.startswith(self.features[i].name):
                    self.features[i].name = nf.name
                #                    print self.features[i].name, "<-", nf.name
                if self.features[i].name.startswith(nf.name):
                    nf.name = self.features[i].name
            #                    print nf.name, "<-", self.features[i].name

            cap, cup = self.features[i].capcup(nf, self.circular, self.size)
            # features[i] included in nf
            # => nf will not be inserted
            if cap == self.features[i].length(
                self.circular, self.size
            ) and cup == nf.length(self.circular, self.size):
                #                print nf, "includes", self.features[i]
                return

            # nf included in features[i]
            # => features[i] will be deleted
            if cap == nf.length(self.circular, self.size) and cup == self.features[
                i
            ].length(self.circular, self.size):
                #                print self.features[i], "includes", nf
                del self.features[i]
                continue

            # correct position is found
            if self.features[i].start > nf.start:
                break
            else:
                i += 1

        self.features.insert(i + 1, nf)
        return

    def _add_feature(self, nf):
        """
        add a new feature to the already existing features
        """
        # logging.warning( "try %s" % nf )
        i = 0
        while i < len(self.features):

            # current feature is left of the new feature
            # => this is not the right position
            if self.features[i].stop < nf.start:
                i += 1
                continue

            cap, cup = self.features[i].capcup(nf, self.circular, self.size)

            # logging.warning( "%s %s %s %d %d" % ( self.accession, str( self.features[i] ), str( nf ), cap, cup ) )

            # if feature[i] == new feature
            # => merge info and abort
            if cap == cup:
                try:
                    self.features[i] = self.features[i].merge(nf)
                except feature.FeatureUnAddable:
                    logging.warning(
                        "%s unmergeable %s %s discard later"
                        % (self.accession, str(self.features[i]), str(nf))
                    )
                    return
                else:
                    #                     logging.warning( "merged %s" % ( self.features[i] ) )
                    return

            # special treatment of ORFs. if an ORF and is completely included
            # or includes completely another feature. then remove the orf.
            # applies to potential new features and already present features
            elif (
                nf.name.startswith("orf")
                and not self.features[i].name.startswith("orf")
                and (
                    cap == nf.length(self.circular, self.size)
                    or cup == nf.length(self.circular, self.size)
                )
            ):
                # print "discarded", nf, "for", self.features[i]
                return
            elif (
                self.features[i].name.startswith("orf")
                and not nf.name.startswith("orf")
                and (
                    cap == self.features[i].length(self.circular, self.size)
                    or cup == self.features[i].length(self.circular, self.size)
                )
            ):
                # print "discarding", self.features[i], "for", nf
                del self.features[i]
                continue

            # if the new feature is (truly) included in feature[i]
            # => discard the new feature (strategy is to take the parts)
            elif (
                nf.name == self.features[i].name
                and cap == nf.length(self.circular, self.size)
                and cup == self.features[i].length(self.circular, self.size)
            ):
                # logging.warn( "discarding %s for %s" % ( self.features[i], nf ) )
                del self.features[i]
                continue

            # else if feature[i] is truly included in the new feature
            # => discard feature[i] (i.e. delete it and restart current iteration)
            elif (
                nf.name == self.features[i].name
                and cap == self.features[i].length(self.circular, self.size)
                and cup == nf.length(self.circular, self.size)
            ):
                # logging.warn( "discarding %s for %s" % ( nf, self.features[i] ) )
                return

            # current feature is right of the new feature
            # => correct position is found
            if self.features[i].start > nf.start or (
                self.features[i].start == nf.start and self.features[i].stop > nf.stop
            ):
                break
            else:
                i += 1

        # logging.warn( "adding %s" % ( nf ) )
        self.features.insert(i, nf)
        return

    def _parse_accession_version(self, annotations):
        """
        parse accession and version from the accession, version string
        """

        if len(annotations["accessions"]) != 1:
            sys.stderr.write("warning: accession list not of length 1\n")
            sys.stderr.write("         %s\n" % str(annotations["accessions"]))
            # sys.exit()

        self.accession = annotations["accessions"][0]

        #        if self.accession != locus:
        #            sys.stderr.write( "warning: accession (%s) != locus (%s)\n" % ( self.accession, locus ) )
        #            #sys.exit()

        try:
            self.version = annotations["sequence_version"]
        except KeyError:
            self.version = -1

    #        m = re.match( "^([\w]{2}_{0,1}[\d]+)\.(\d+)$", version )
    #        if m is not None:
    #            if m.group( 1 ) != self.accession:
    #                sys.stderr.write( "error: accession in version string (%s) does not match accession (%s)\n" % ( version, self.accession ) )
    #                #sys.exit()
    #            self.version = int( m.group( 2 ) )
    #        else:
    #            sys.stderr.write( "error: version string (%s) does not match\n" % ( version ) )
    #            sys.exit()

    def _parse_anticodon(self, v, strand):
        """
        try to get a codon from value
        \return the anticodon
        """

        cdn = None
        nam = None

        v = v.upper()

        m = re.search(
            r"POS:(?P<comp>COMPLEMENT){0,1}[\(]{0,1}(?P<start>[\d]+)\.\.(?P<end>[\d]+)[\)]{0,1}",
            v,
        )
        if m is not None:
            d = m.groupdict()
            # print m.re.pattern, d

            s = int(d["start"]) - 1
            e = int(d["end"]) - 1

            if not (
                (d["comp"] is None and strand == 1)
                or (d["comp"] == "COMPLEMENT" and strand == -1)
            ):
                logging.warn(
                    "%s anticodon strand differs from feature strand %d %s"
                    % (self.accession, strand, v)
                )

            #            print str(self.sequence.subseq( s, e, strand ))
            try:
                cdn = codon(str(self.sequence.subseq(s, e, strand)), "anticodon")
            except CodonError:
                # print "invalid codon", self.sequence.subseq(s, e, strand)
                pass

        m = re.match(
            r"^ANTICODON[ :\s]{1,2}([U%s]{3}).*" % Data.IUPACData.ambiguous_dna_letters,
            v,
        )
        if m is not None:
            try:
                cdn = codon(m.group(1), "anticodon")
            except CodonError:
                # print "invalid codon", m.group(1)
                pass

        nam = unify.unify_name_trna(v, self.transl_table)[0]
        if cdn is not None and nam is not None:
            cdn = unify.unify_name_trna(v, self.transl_table)[1]

        if cdn is not None and nam is None:
            return cdn
        elif cdn is not None and nam is not None:
            aa = cdn.get_aa(self.transl_table)
            # print cdn, aa, nam
            if aa is not None and nam.startswith("trn" + aa[0]):
                # print "ACDN MATCH"
                return cdn
        else:
            return None

    def _parse_codon_recognized(self, v, strand):
        """
        try to get a codon from value
        return anticodon (initialized as codon)
        """

        cdn = None
        nam = None

        v = v.upper()

        m = re.match("^([U%s]{3})$" % Data.IUPACData.ambiguous_dna_letters, v)
        if m is not None:
            try:
                cdn = codon(v, "codon")
            except CodonError:
                # print "invalid codon", v
                pass

        m = re.match(
            r"^CODONS? RECOGN[IZ]{2}ED[\s:]+([U%s]{3}$)"
            % Data.IUPACData.ambiguous_dna_letters,
            v,
        )
        if m is not None:
            try:
                cdn = codon(m.group(1), "codon")
            except CodonError:
                # print "invalid codon", m.group(1)
                pass

        nam = unify.unify_name_trna(v, self.transl_table)[0]
        if cdn is not None and nam is not None:
            cdn = unify.unify_name_trna(v, self.transl_table)[1]

        if cdn is not None and nam is None:
            return cdn
        elif cdn is not None and nam is not None:
            aa = cdn.get_aa(self.transl_table)
            if aa is not None and nam.startswith("trn" + aa[0]):
                return cdn
        else:
            return None

    def _parse_circular(self, rt):
        """
        parse circularity from residuetype string
        param rt residuetype string
        """

        if rt.endswith("circular"):
            self.circular = True
        else:
            self.circular = False
        return

    def _parse_complete(self, description):
        if description.find("complete") != -1:
            self.complete = True

    def _parse_feature_codon(self, f, strand, unambiguous=False):
        """
        try to parse the anticodon from a feature
        /anticodon=/codon_recognized
        @param f the feature
        @param strand the strand
        @param unambiguous prefer unambiguous anticodons
        """

        if f.type != "gene" and f.type != "tRNA":
            return None

        #        print f
        #        print f.qualifiers
        codons = []
        for q in ["anticodon", "codon_recognized", "product", "gene", "note"]:

            # if codon / anticodon could be extracted from the
            # qualifiers "anticodon" or "codon_recognized", then we trust these
            if q not in ["anticodon", "codon_recognized"] and len(codons) > 0:
                break

            if q not in f.qualifiers:
                continue

            for x in f.qualifiers[q]:
                if q in ["product", "gene"]:
                    codons.append(unify.unify_name_trna(x, self.transl_table)[1])
                #                    codons.append( self._parse_codon_from_product( x ) )
                elif q == "anticodon":
                    c = self._parse_anticodon(x, strand)
                    codons.append(c)
                elif q == "codon_recognized":
                    c = self._parse_codon_recognized(x, strand)
                    codons.append(c)
                elif q in ["note"]:
                    c = self._parse_anticodon(x, strand)
                    codons.append(c)
                    c = self._parse_codon_recognized(x, strand)
                    codons.append(c)
                codons = [x for x in codons if x is not None]

        uacodons = []
        for c in codons:
            if (
                c[0] in ["A", "T", "C", "G"]
                and c[1] in ["A", "T", "C", "G"]
                and c[2] in ["A", "T", "C", "G"]
            ):
                uacodons.append(c)

        if unambiguous and len(uacodons) > 0:
            return uacodons
        else:
            return codons

        # print clean
        # t = [ Seq.translate( c, table = self.transl_table ) for c in codons ]

        # if len(s) != 1:
        #   if len(s) > 1:
        #        print "anticodon ???"
        #        print f
        #        print s
        #        print "================"
        #    return None
        # else:
        #    return list(s)[0]

        # todo return
        # todo codon, anticodon identities

    #    def _parse_feature_location( self, location ):
    #        """
    #        (simple) parse a location string and return strand, start, and end
    #
    #        @param[in] location the genbank location string
    #        @return triple (start, stop, strand):
    #            strand = -1 iff location string starts with complement
    #            start & stop = smallest and largest number found in the location
    #        """
    #
    #        return

    def _parse_feature_locations(self, feature):
        """
        parse location(s) from subfeatures
        @return list of locations, i.e. list of triples (start, stop, strand)
        """

        # print feature, dir( feature )
        loc = []

        for f in feature.location.parts:
            if f.strand is None or f.strand >= 0:
                strand = 1
            else:
                strand = -1

            # biopython gets the positions 0-based with the stop excluded
            # -> subtract 1 from the stop
            loc.append((int(f.start), int(f.end) - 1, strand))

        return loc

    def _parse_feature_name(self, f: "SeqFeature", strand, rRNAs):
        """
        try to determine the name of a feature
        for trna, rrna, and genes try to guess the name from the gene or product qualifier

        in order to get the origins additionally:
        for rep_origin, D-loop, misc_feature try to guess the name from standard_name, note, direction"

        if there are several different guesses -> return None
        otherwise assign OH/OL to an origin feature
        and try to get the number of Leu/Ser tRNAs

        if rRNAs is None only potential rRNA features are considered

        @param[in] f the feature
        @param[in] strand the strand of the feature
        @param[in] rRNAs names of the present rRNAs (should be determined in a 1st run over the features with the same function using rRNA=None)
        @return the name of None (if could not be determined)
        """

        candidates = set()
        for q in f.qualifiers:
            for x in f.qualifiers[q]:
                if q in ["gene", "product", "note"]:
                    if rRNAs is not None and f.type in ["tRNA", "gene"]:
                        candidates.add(unify.unify_name_trna(x, self.transl_table)[0])
                    if f.type in ["rRNA", "gene"]:
                        candidates.add(unify.unify_name_rrna(x, rRNAs))
                    # Note gene is currently not parsed for proteins otherwise
                    # the exons are not reported
                    if rRNAs is not None and f.type in ["CDS"]:
                        candidates.add(unify.unify_name_protein(x))
                        candidates.add(unify.unify_name_orf(x))
                if q in ["standard_name", "note", "direction", "product", "gene"]:
                    if rRNAs is not None and f.type in [
                        "rep_origin",
                        "D-loop",
                        "misc_feature",
                        "stem_loop",
                        "repeat_region",
                        "misc_signal",
                    ]:
                        if f.type == "rep_origin":
                            candidates.add(unify.unify_name_origin(x, "OL", True))
                        elif f.type == "D-loop":
                            candidates.add(unify.unify_name_origin(x, "OH", True))
                        else:
                            candidates.add(unify.unify_name_origin(x, "OH", False))
                #                         qal.add( x )
                if q in ["note"]:
                    if rRNAs is not None and f.type == "intron":
                        candidates.add(unify.unify_name_intron(x, "intron"))

        candidates.discard(None)

        if rRNAs is not None and len(candidates) == 0:
            if f.type == "D-loop":
                candidates.add("OH")
            elif f.type == "rep_origin":
                candidates.add("OL")

        # if we have L and L1 or L2 remove L
        if "trnL" in candidates and (
            ("trnL1" in candidates) or ("trnL2" in candidates)
        ):
            candidates.remove("trnL")
        # if we have S and S1 or S2 remove S
        if "trnS" in candidates and (
            ("trnS1" in candidates) or ("trnS2" in candidates)
        ):
            candidates.remove("trnS")

        # if we have intron and intron_gpI or intron_gpII remove intron
        if "intron" in candidates and (("gpI" in candidates) or ("gpII" in candidates)):
            candidates.remove("intron")

        # if there is orf and orfNR included -> remove orf
        if (
            "orf" in candidates
            and len([x for x in candidates if (x.startswith("orf") and x != "orf")]) > 0
        ):
            candidates.remove("orf")

        # if there is a gene and orf included -> remove orf
        if (
            len([x for x in candidates if (x.startswith("orf"))]) >= 1
            and len([x for x in candidates if (not x.startswith("orf"))]) == 1
        ):
            candidates = {x for x in candidates if (not x.startswith("orf"))}

        # if we have rrnL and  23S, 21S, 16S
        if (
            len(candidates) == 2
            and ("rrnL" in candidates)
            and (
                ("23S" in candidates) or ("21S" in candidates) or ("16S" in candidates)
            )
        ):
            candidates = {"rrnL"}
        # if we have rrnL and  16S 15S 12S
        if (
            len(candidates) == 2
            and ("rrnS" in candidates)
            and (
                ("16S" in candidates) or ("15S" in candidates) or ("12S" in candidates)
            )
        ):
            candidates = {"rrnS"}

        if len(candidates) == 2:
            if "giy" in candidates and "lagli" not in candidates:
                candidates = {"giy"}
            elif "lagli" in candidates and "giy" not in candidates:
                candidates = {"lagli"}

        # check if there is exactly one element in s
        # 0 .. could not determine the name
        #      this is ok for origins because they often do not have a name
        #      and are only identified by its type
        # > 1 .. could not determine a unique name
        if len(candidates) != 1:
            name = None
        else:
            name = candidates.pop()
            if name.startswith("trnL") or name.startswith("trnS"):
                candidates = set()
                codons = self._parse_feature_codon(f, strand)
                for c in codons:
                    if name.startswith("trnL") and c.isequal(
                        L1,
                        maxac=1,
                        ambiguous_nucleotide_values=Data.IUPACData.ambiguous_dna_values,
                    ):
                        candidates.add("trnL1")
                    elif name.startswith("trnL") and c.isequal(
                        L2,
                        maxac=1,
                        ambiguous_nucleotide_values=Data.IUPACData.ambiguous_dna_values,
                    ):
                        candidates.add("trnL2")
                    elif name.startswith("trnS") and c.isequal(
                        S1,
                        maxac=1,
                        ambiguous_nucleotide_values=Data.IUPACData.ambiguous_dna_values,
                    ):
                        candidates.add("trnS1")
                    elif name.startswith("trnS") and c.isequal(
                        S2,
                        maxac=1,
                        ambiguous_nucleotide_values=Data.IUPACData.ambiguous_dna_values,
                    ):
                        candidates.add("trnS2")
                #                print c, s
                if len(candidates) == 1:
                    # if the codon determined tRNA differs from the one given in the gb file
                    # then we take the one in the genbank file, otherwise there is a conflict
                    # with the other tRNA feature which always has no given
                    # codon
                    if not list(candidates)[0].startswith(name):
                        logging.warn(
                            "%s ignoring %s determined by codon for %s"
                            % (self.accession, list(candidates)[0], name)
                        )
                    else:
                        name = candidates.pop()
                #    print name
                # print f
                # print "===================="
                # else:

        #         print name, f.type, s, list( qal )
        return name

        # now we have a uniq name
        # name = s[0]
        # tpe = unify.feature_type(name)
        # if tpe == "tRNA":
        #
        #    for c in codons:
        #        if c is not None:
        #            s += c.get_aa(self.transl_table)

        # rint self.accession
        # rint f
        # f len(set(s)) != 1:
        #   print "FAIL ", s
        # lse:
        #   print "OKAY ", s
        # rint "=========================="
        # print s
        # clean.append( str(c) )
        # return aa

        # if f.key != tpe and ( f.key != "gene" or (tpe != "rRNA" and tpe != "tRNA") ) and ( f.key != "CDS" or tpe != "gene" ) :
        #    print "%s!=%s %s"%(f.key, tpe, name)

    def _parse_names(self, annotations):
        """
        parse the name, common name, and completeness from the definition
        organism and source lines
        """

        #        gb 'organism': 'Daphnia pulex'
        #        embl 'organism': 'Astropecten polyacanthus (seastar)'
        #        gb: 'source': 'mitochondrion Daphnia pulex (water flea)'
        #        embl:no source

        # take organism as name
        try:
            self.name = annotations["organism"]
        except Exception:
            raise Exception("NoName", str(annotations))

        # try to get common name from source

        n = self.name.replace("(", "\\(").replace(")", "\\)")

        if "source" in annotations:
            m = re.match(
                r"mitochondrion %s(?P<commonname> \(.*\)){0,1}$" % n,
                annotations["source"],
            )

            if m is not None:
                if m.group("commonname") is not None:
                    self.commonname = m.group("commonname")[2:-1]
                else:
                    self.commonname = ""
            else:
                logging.warning(
                    "%s malformed source %s %s"
                    % (self.accession, annotations["source"], n)
                )

    #                raise Exception( "Malformed", "source", annotations["source"], n )
    #        for i in ['source', 'organism']:
    #            try:
    #                a = annotations[i]
    #            except:
    #                continue
    #
    #            m = re.match( '(mitochondrion ){0,1}(?P<name>.*)(?P<commonname> \([^(]*\)){0,1}$', a )
    #            if m is None:
    #                raise Exception( "Malformed", i, annotations[i] )
    #
    #            if self.name == "" or self.name == m.group( 'name' ):
    #                self.name = m.group( 'name' )
    #            else:
    #                raise Exception( "Name mismatch in source/organism", self.name, m.group( 'name' ) )
    #
    #            if m.group( 'commonname' ) is not None:
    #                cn = m.group( 'commonname' )[2:-1]
    #                if self.commonname == "" or self.commonname == cn:
    #                    self.commonname = cn
    #                else:
    #                    logging.info( "CommonName mismatch in source/organism %s %s" % ( self.commonname, cn ) )

    def _parse_number(self, feature):
        """
        get the /number property of features if absent return None
        @param[in] feature the feature
        @return the number or None
        """
        try:
            return int(feature.qualifiers["number"][0]) - 1
        except Exception:
            return None

    def _parse_source(self, feature):
        """
        parse entries from the source feature
        currently this is the taxid and strain
        @param[in] feature the source feature
        @return nothing
        """

        #        print "key", feature.key
        #        print "location", feature.location
        try:
            dbxref = feature.qualifiers["db_xref"][0]
        except KeyError:
            dbxref = ""

        if dbxref.startswith("taxon:"):
            self.taxid = int(dbxref[6:])

        if self.taxid is None:
            sys.stderr.write("warning: %s could not determine taxid\n" % self.accession)

        try:
            self.strain = feature.qualifiers["strain"][0]
        except KeyError:
            self.strain = ""

    def _parse_translation(self, feature):
        """
        if the given feature has a translation entry get it
        @param[in] feature a feature
        @return the translation of the feature, or None if it has none
        """

        try:
            return sequence.sequence(feature.qualifiers["translation"][0], False)
        except KeyError:
            return None

    def _parse_transl_table(self, features):
        """
        get the translation table which is stored in the CDS features
        ensure that the codon table is unique for the species
        """

        s = set()
        for f in features:
            if "transl_table" in f.qualifiers:
                s.update(set(f.qualifiers["transl_table"]))

        if len(s) != 1:
            if len(s) == 0:
                logging.warning(
                    "warning (%s) no translation table found" % self.accession
                )
            else:
                logging.warning(
                    "warning (%s) more than one translation table found (%s)"
                    % (self.accession, str(s))
                )
            self.transl_table = 2
        else:
            self.transl_table = int(list(s)[0])

        if self.transl_table not in Data.CodonTable.unambiguous_dna_by_id:
            logging.warning(
                "warning (%s) has unknown translation table %d"
                % (self.accession, self.transl_table)
            )
            self.transl_table = 1
