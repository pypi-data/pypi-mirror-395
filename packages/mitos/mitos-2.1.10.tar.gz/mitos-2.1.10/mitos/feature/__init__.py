"""
@author: M. Bernt
"""

import copy
import logging
import math
from sys import stderr, stdout
from typing import Iterator, Optional

from mitos.mito import revprot, revtrnamap, rrnamap

# TODO documentation


class FeatureUnAddable(Exception):
    """
    exception that is raised if non equal features are added
    """

    def __init__(self, s, o):
        self._self = s
        self._other = o

    def __str__(self):
        return "%s, %s" % (str(self._self), (self._other))


class LinearSequenceIndexError(Exception):
    """
    exception to be raised when a feature with stop < start is found for linear sequences
    """

    def __init__(self, start, stop):
        self.start = start
        self.stop = stop

    def __str__(self):
        return repr((self.start, self.stop))


def cap(start1, stop1, start2, stop2, circular, size):
    """ """
    if start1 <= stop1 and start2 <= stop2:
        # check if overlap at all
        # self |---|                       |---|
        # other      |---|           |---|
        if stop1 < start2 or stop2 < start1:
            return 0

        # if overlap return percentage
        # 1  |------------|                |---...
        # 2      |--...              |------------|
        elif (start1 <= start2 <= stop1) or (start2 <= start1 <= stop2):
            return min(stop1, stop2) - max(start2, start1) + 1

        else:
            stderr.write(
                "error: unhandled feature position case for overlap computation\n"
            )
            stderr.write("%%(%d,%d) (%d,%d)\n" % (start1, stop1, start2, stop2))
            return 0, 0
    else:
        if not circular:
            if start1 > stop1:
                raise LinearSequenceIndexError(start1, stop1)
            else:
                raise LinearSequenceIndexError(start2, stop2)

        if start1 > stop1 and start2 <= stop2:
            return cap(start1, size - 1, start2, stop2, circular, size) + cap(
                0, stop1, start2, stop2, circular, size
            )
        elif start1 <= stop1 and start2 > stop2:
            return cap(start1, stop1, start2, size - 1, circular, size) + cap(
                start1, stop1, 0, stop2, circular, size
            )
        else:
            return cap(start1, size - 1, start2, size - 1, circular, size) + cap(
                0, stop1, 0, stop2, circular, size
            )


def cup(start1, stop1, start2, stop2, circular, size):
    """ """
    if start1 <= stop1 and start2 <= stop2:
        # check if overlap at all
        # self |---|                       |---|
        # other      |---|           |---|
        if stop1 < start2 or stop2 < start1:
            return length(start1, stop1, circular, size) + length(
                start2, stop2, circular, size
            )

        # if overlap return percentage
        # 1  |------------|                |---...
        # 2      |--...              |------------|
        elif (start1 <= start2 <= stop1) or (start2 <= start1 <= stop2):
            return max(stop1, stop2) - min(start1, start2) + 1

        else:
            stderr.write(
                "error: unhandled feature position case for overlap computation\n"
            )
            stderr.write("%%(%d,%d) (%d,%d)\n" % (start1, stop1, start2, stop2))
            return 0, 0
    else:
        if not circular:
            if start1 > stop1:
                raise LinearSequenceIndexError(start1, stop1)
            else:
                raise LinearSequenceIndexError(start2, stop2)

        if start1 > stop1 and start2 <= stop2:
            return cup(start1, size - 1, start2, stop2, circular, size) + cup(
                0, stop1, start2, stop2, circular, size
            )
        elif start1 <= stop1 and start2 > stop2:
            return cup(start1, stop1, start2, size - 1, circular, size) + cup(
                start1, stop1, 0, stop2, circular, size
            )
        else:
            return cup(start1, size - 1, start2, size - 1, circular, size) + cup(
                0, stop1, 0, stop2, circular, size
            )


def capcup(start1, stop1, start2, stop2, circular, size):
    """
    compute the size (i.e. nr of positions) of the intersection and union of two features

    @param start1 first position of feature 1 in [0:size-1]
    @param stop1 last position of feature 1 in [0:size-1]
    @param start2 first position of feature 2 in [0:size-1]
    @param stop2 last position of feature 2 in [0:size-1]
    @param circularity True iff the chromosome housing the feature is circular
    @param size size of the chromosome housing the feature
    """

    if start1 <= stop1 and start2 <= stop2:
        # check if overlap at all
        # self |---|                       |---|
        # other      |---|           |---|
        if stop1 < start2 or stop2 < start1:
            return 0, length(start1, stop1, circular, size) + length(
                start2, stop2, circular, size
            )

        # if overlap return percentage
        # 1  |------------|                |---...
        # 2      |--...              |------------|
        elif (start1 <= start2 <= stop1) or (start2 <= start1 <= stop2):
            return (min(stop1, stop2) - max(start2, start1) + 1), (
                max(stop1, stop2) - min(start1, start2) + 1
            )

        else:
            stderr.write(
                "error: unhandled feature position case for overlap computation\n"
            )
            stderr.write("%%(%d,%d) (%d,%d)\n" % (start1, stop1, start2, stop2))
            return 0, 0
    else:
        if not circular:
            if start1 > stop1:
                raise LinearSequenceIndexError(start1, stop1)
            else:
                raise LinearSequenceIndexError(start2, stop2)

        if start1 > stop1 and start2 <= stop2:
            a1, u1 = capcup(start1, size - 1, start2, stop2, circular, size)
            a2, u2 = capcup(0, stop1, start2, stop2, circular, size)
        elif start1 <= stop1 and start2 > stop2:
            a1, u1 = capcup(start1, stop1, start2, size - 1, circular, size)
            a2, u2 = capcup(start1, stop1, 0, stop2, circular, size)
        else:
            a1, u1 = capcup(start1, size - 1, start2, size - 1, circular, size)
            a2, u2 = capcup(0, stop1, 0, stop2, circular, size)
        return a1 + a2, u1 + u2


def crange(
    start: int, stop: int, step: int, circular: bool, length: int
) -> Iterator[int]:
    """
    Generator for a range from start to stop (exclusive) with given step size.
    Handles both linear and circular sequences robustly.

    @param start: Start index (int)
    @param stop: Stop index (exclusive, int)
    @param step: Step size (int ≠ 0)
    @param circular: Whether the sequence should wrap around
    @param length: Length of the underlying sequence space (int > 0)

    @yield int: Sequence of indices according to parameters
    """

    if circular:
        if step > 0:
            if start <= stop:
                # Simple forward range
                yield from range(start, stop, step)
            else:
                # Wrap-around: from start to end, then from 0 to stop
                restart = (step - 1) - ((length - 1 - start) % step)
                yield from range(start, length, step)
                yield from range(restart, stop, step)
        else:
            if start >= stop:
                # Simple backward range
                yield from range(start, stop, step)
            else:
                # Wrap-around: from start down to 0, then from length-1 to stop
                restart = (length + step) + (start % abs(step))
                yield from range(start, -1, step)
                yield from range(restart, stop, step)

    else:  # linear sequence
        # Check for valid direction
        if (step > 0 and start > stop) or (step < 0 and start < stop):
            raise LinearSequenceIndexError(start, stop)

        # Yield linear range
        yield from range(start, stop, step)


def length(start: int, stop: int, circular: bool, size: int) -> int:
    """
    get the length of a feature with 1st position at start and last position
    at stop, circularity and size of the chromosome are regarded

    @param start 1st position
    @param stop last position
    @param circular circularity of the chromosome homing the feature
    @param size length of the chromosome homing the feature
    """

    if circular:
        if start <= stop:
            return stop - start + 1
        else:
            # ((size-1)-self.start+1) + ((self.stop-0) + 1)
            return size - start + stop + 1
    else:
        if start <= stop:
            return stop - start + 1
        else:
            raise LinearSequenceIndexError(start, stop)


def genorderwriter(featurelist, acc, outfile, mode="w", start=None, signed=True):
    featurelist.sort(key=lambda x: x.start)

    if start is not None:
        i = 0
        while i < len(featurelist) and featurelist[i].outputname(False) != start:
            i += 1

        featurelist = featurelist[i:] + featurelist[:i]

    out = ">%s\n" % (acc)
    for feat in featurelist:
        if signed is True and feat.strand < 0:
            out += "-%s " % (feat.outputname(False))
        else:
            out += "%s " % (feat.outputname(False))
    out += "\n"

    if isinstance(outfile, str):
        with open(outfile, mode) as f:
            f.write(out)
    elif outfile is None:
        stdout.write(out)
    else:
        outfile.write(out)


def remove_circular_duplicates2(flist, length, extlength):
    if len(flist) == 0:
        return flist

    # determine the length of (one of) the longtest features
    maxlenf = max(flist, key=lambda p: p.length(False, 0))
    maxlen = maxlenf.length(False, 0)

    mid = int(round(extlength / 2.0))
    left = mid - (length / 2) - (maxlen / 2) - (maxlen % 2)
    right = mid + (length / 2) + (length % 2) + (maxlen / 2)

    left = max(left, 0)
    right = min(right, length - 1)

    nflist = [x for x in flist if (x.start >= left and x.stop <= right)]

    # adapt the start and stop modulo length
    for i in range(len(nflist)):
        nflist[i].start %= length
        nflist[i].stop %= length

    # due to the extension by maxlen there might be duplicates
    # -> remove equal (same start, stop, strand, name) adjacent
    # features in the list sorted by start position
    nflist.sort(key=lambda p: (p.start, p.stop))
    i = 0
    while i + 1 < len(nflist):
        if nflist[i] == nflist[i + 1]:
            del nflist[i + 1]
        else:
            i += 1

    return nflist


def remove_circular_duplicates(flist, length):
    """
    remove redundant hits from a list of features that have
    been determined for a duplicated genome (in order to treat circularity)

    - it determines the features spanning the end of the linearized genome,
      i.e. spanning the position length
    - if no such feature is present
      -> the features in [length:]are removed
    - else:
      the feature C of those spanning the end with maximum stop position is determined
      -> features starting after C (i.e. C.stop % lenght)
         and stopping before C+ the lenghth x of the longest fecture in flist
         (i.e. C.start + x) are accepted

    assumptions:
    - 0 based positions, end position excluded
    - non-overlapping features, i.e. only one spans the end of the genome

    @param[in] flist list of features
    @param[in] length length of the genome

    @return feature list without duplicates
    """

    if len(flist) == 0:
        return flist

    # determine the length of (one of) the longtest features
    maxlenf = max(flist, key=lambda p: p.length(False, 0))
    maxlen = maxlenf.length(False, 0)

    # determine features overlapping L
    cfeat = [x for x in flist if (x.start < length and x.stop >= length)]

    if len(cfeat) == 0:
        mn = 0
        mx = length
    else:
        mcfeat = max(cfeat, key=lambda p: p.stop)
        mn = mcfeat.stop % length
        mx = mcfeat.stop + maxlen
        logging.error("circextend %s: %d %d" % (mcfeat.name, mcfeat.start, length))

    # remove features outside mn and mx
    nflist = [x for x in flist if (x.start >= mn and x.stop <= mx)]

    # adapt the start and stop modulo length
    for i in range(len(nflist)):
        nflist[i].start %= length
        nflist[i].stop %= length

    # due to the extension by maxlen there might be duplicates
    # -> remove equal (same start, stop, strand, name) adjacent
    # features in the list sorted by start position
    nflist.sort(key=lambda p: (p.start, p.stop))
    i = 0
    while i + 1 < len(nflist):
        if nflist[i] == nflist[i + 1]:
            del nflist[i + 1]
        else:
            i += 1

    return nflist


class feature:
    rf: Optional[int]

    def __init__(
        self,
        name,
        tpe,
        start,
        stop,
        strand,
        method,
        translation=None,
        score=None,
        rf=None,
        anticodon=None,
        copy=None,
        part=None,
        mito=None,
    ):
        """
        create a new feature
        @param name name of the feature, i.e. the gene's name
        @param tpe type of the feature, e.g. tRNA, gene, rRNA
        @param start start position (counting starts at 0, start position belongs to the gene)
        @param stop stop position (counting starts at 0, stop position belongs to the gene)
        @param strand strand (+1/-1)
        @param method method used for predicting the gene
        @param translation
        @param score some raw score, e.g.  bitscore
        @param rf
        @param anticodon the anticodon: of type trna.codon
        @param copy copy number of the feature
        @param part part number of the feature
        @param mito 1 if to be annotated in the 1st round of mitos and 2 otherwise
        """

        # TODO score is method dependent
        # TODO translation and rf are only useful for protein coding genes, create derived feature
        # TODO make checks (rf\in\{1,-1\}, start < stop/ circular, len<size/2)

        self.name = name
        self.type = tpe
        self.start = start
        self.stop = stop
        self.strand = strand
        self.method = method

        self.translation = translation
        self.score = score
        self.rf = rf
        self.anticodon = anticodon

        self.copy = copy
        self.part = part
        self.mito = mito

    def __eq__(self, other):
        """
        check two features for equality
        @param self the feature
        @param other another feature
        @return False if name, start, stop, strand, or translation are different True otherwise
        """

        if other is None:
            return False

        if not self.equal_name_type(other):
            return False
        if self.start != other.start:
            return False
        if self.stop != other.stop:
            return False
        if self.strand != other.strand:
            return False
        if self.translation != other.translation:
            return False

        return True

    def __ne__(self, other):
        """
        check for unequality
        @param self the feature
        @param other another feature
        @return True if name, start, stop, strand, or translation are different False otherwise
        """
        return not self == other

    def __repr__(self):
        """
        get a string
        """
        return "%s(%s, %d, %d..%d)" % (
            self.type,
            self.getname(),
            self.strand,
            self.start,
            self.stop,
        )

    def __str__(self):
        """
        get a string
        """
        return "{0:4}({1:>4},{2:1},{3:5d},{4:5d},{5:5}, {6})".format(
            self.type,
            self.getname(),
            self.plusminus(),
            self.start,
            self.stop,
            self.method,
            self.score,
        )

    def length(self, circular, size):
        """
        get the length of a feature

        @param self the feature
        @param circular circularity of the chromosome homing the feature
        @param size length of the chromosome homing the feature
        """

        return length(self.start, self.stop, circular, size)

    def capcup(self, other, circular, size):
        """
        compute the size (i.e. nr of positions) of the intersection and union of two features
        @param self the feature
        @param other another feature
        @param circularity True iff the chromosome housing the feature is circular
        @param size size of the chromosome housing the feature

        """

        return capcup(self.start, self.stop, other.start, other.stop, circular, size)

    #        # if one of the features spans the 0 -> shift it
    #        # assuming that this only happens for features on circular chromosomes
    #        if self.start > self.stop:
    #            selfstop = self.stop + size
    #        else:
    #            selfstop = self.stop
    #
    #        if other.start > other.stop:
    #            otherstop = other.stop + size
    #        else:
    #            otherstop = other.stop
    #
    #        # check if overlap at all
    #        # self |---|                       |---|
    #        # other      |---|           |---|
    #        if selfstop < other.start or otherstop < self.start:
    #            return 0, self.len( circular, size ) + other.len( circular, size )
    #
    #        # if overlap return percentage
    #        # self  |------------|                |---...
    #        # other      |--...              |------------|
    #        elif ( self.start <= other.start and other.start <= selfstop ) or ( other.start <= self.start and self.start <= otherstop ):
    #            return ( min( selfstop, otherstop ) - max( other.start, self.start ) + 1 ) , ( max( selfstop, otherstop ) - min( self.start, other.start ) + 1 )
    #
    #        else:
    #            stderr.write( "error: unhandled feature position case for overlap computation\n" )
    #            stderr.write( "%s\n" % str( self ) )
    #            stderr.write( "%s\n" % str( other ) )
    #            return 0, 0

    def equal_name_type(self, other):
        """
        check if two features have equal name and type
        L is treated as equal to L1 and L2 (same for S)
        @param self the feature
        @param other another feature
        @return False if name or type differ, True otherwise
        """
        if self.name != other.name:
            if not (
                (
                    self.name == "trnL"
                    and (other.name == "trnL1" or other.name == "trnL2")
                )
                or (
                    other.name == "trnL"
                    and (self.name == "trnL1" or self.name == "trnL2")
                )
                or (
                    self.name == "trnS"
                    and (other.name == "trnS1" or other.name == "trnS2")
                )
                or (
                    other.name == "trnS"
                    and (self.name == "trnS1" or self.name == "trnS2")
                )
            ):
                return False
            # return False
        if self.type != other.type:
            return False

        return True

    def is_allowed(
        self,
        aname=None,
        fname=None,
        atype=None,
        ftype=None,
        astrand=None,
        amethod=None,
        fmethod=None,
    ):
        """
        checks if the feature is of a certain type or name
        @param atype list of allowed types or a string of a type
        @param ftype forbidden types
        @param aname list of allowed names or a string of a name
        @param fname forbidden names
        @param astrand allowed strand
        @param fmethod forbidden method
        @param amethod allowed method
        @return true if feature in atype and feature not in ftype and name in aname and name not in fname
        """

        if isinstance(atype, str):
            atype = [atype]
        if isinstance(ftype, str):
            ftype = [ftype]

        if atype is not None and self.type not in atype:
            return False
        elif ftype is not None and self.type in ftype:
            return False

        if isinstance(aname, str):
            aname = [aname]
        if isinstance(fname, str):
            fname = [fname]

        if aname is not None and "S" in aname:
            aname.append("S1")
            aname.append("S2")
        if fname is not None and "S" in fname:
            fname.append("S1")
            fname.append("S2")
        if aname is not None and "L" in aname:
            aname.append("L1")
            aname.append("L2")
        if fname is not None and "L" in fname:
            fname.append("L1")
            fname.append("L2")

        if aname is not None and self.name not in aname:
            return False
        elif fname is not None and self.name in fname:
            return False
        elif astrand is not None and self.strand != astrand:
            return False

        if isinstance(amethod, str):
            amethod = [amethod]
        if isinstance(fmethod, str):
            fmethod = [fmethod]

        # need to get the local and global difference
        if self.method == "mitfi" and "local" in self.__dict__:
            if self.local and amethod is not None and "lmitfi" in amethod:
                return True
            elif not self.local and amethod is not None and "gmitfi" in amethod:
                return True
            elif self.local and fmethod is not None and "lmitfi" in fmethod:
                return False
            elif not self.local and fmethod is not None and "fmitfi" in fmethod:
                return False

        if amethod is not None and self.method not in amethod:
            return False
        elif fmethod is not None and self.method in fmethod:
            return False

        return True

    def merge(self, other):
        """
        this functions merges the info of two features and returns a new feature
        the new feature will be of the same type as the calling feature
        the features need to have equal
        - type, strand, start, stop, and method
        - and name (up to L1/L2/L and S1/S2/S)
          L/S is overwitten if the other feature is L/S1/2
        - minimum of copy and part is chosen
        - all other properties need to be equal or one equal to None
          then the non None property is taken

        raises FeatureUnAddable in case of error

        @param other the second feature
        @return a new feature
        """

        #        print "merge", str( self ), str( other )

        f = copy.deepcopy(self)

        # update of name is special
        if (
            self.name is None
            or other.name.startswith(self.name)
            or f.name.startswith("orf")
            and not other.name.startswith("orf")
        ):
            f.name = other.name
            f.type = other.type
        elif (
            other.name is None
            or self.name.startswith(other.name)
            or not f.name.startswith("orf")
            and other.name.startswith("orf")
        ):
            other.name = f.name
            other.type = f.type
        elif f.type == "tRNA" and f.length(False, 0) > 100:
            logging.warn(
                f"ignoring to long {f.name} (length={f.length(False, 0)}) in favour of {other.name}"
            )
            f.type = other.type
            f.name = other.name
        elif other.type == "tRNA" and other.length(False, 0) > 100:
            logging.warn(
                f"ignoring to long {other.name} (length={other.length(False, 0)}) in favour of {f.name}"
            )
            other.type = f.type
            other.name = f.name
        else:
            raise FeatureUnAddable(self, other)

        # some properties are required to be equal already
        for m in ["type", "strand", "start", "stop", "method"]:
            if f.__dict__[m] != other.__dict__[m]:
                # print "becausE", m, f.__dict__[m], other.__dict__[m]
                raise FeatureUnAddable(self, other)

        for m in f.__dict__:
            if m not in other.__dict__:
                continue

            if f.__dict__[m] is None and other.__dict__[m] is not None:
                f.__dict__[m] = other.__dict__[m]
            elif f.__dict__[m] is not None and other.__dict__[m] is None:
                pass
            else:
                if f.__dict__[m] == other.__dict__[m]:
                    pass
                elif m in ["copy", "part"]:
                    f.__dict__[m] = min(f.__dict__[m], other.__dict__[m])
                elif m == "anticodon":
                    fdeambig = set(f.__dict__[m].deambig())
                    odeambig = set(other.__dict__[m].deambig())
                    if fdeambig.issubset(odeambig):
                        pass
                    elif odeambig.issubset(fdeambig):
                        f.__dict__[m] = other.__dict__[m]
                    else:
                        raise FeatureUnAddable(self, other)
                # print "because ", f.__dict__[m], other.__dict__[m], fdeambig, odeambig
                else:
                    # print "because ", m, f.__dict__[m], other.__dict__[m],
                    # fdeambig, odeambig
                    raise FeatureUnAddable(self, other)

        return f

    #     def merge( self, other ):
    #         """
    #         this functions merges the info of two features and returns a new feature
    #         the features need to have equal
    #         - type, strand, start, stop, and method
    #         - and name (up to L1/L2/L and S1/S2/S)
    #
    #         @param other the second feature
    #         @return a new feature
    #         """
    #
    # #        print "merge", str( self ), str( other )
    #
    #         prop = {}
    #
    #         # update of name is special
    #         if other.name.startswith( self.name ) or self.name is None:
    #             prop["name"] = other.name
    #         elif self.name.startswith( other.name ) or other.name is None:
    #             prop["name"] = self.name
    #         else:
    #             raise FeatureUnAddable( self, other )
    #
    #         # some properties are required to be equal already
    #         for m in ["type", "strand", "start", "stop", "method"]:
    #             if self.__dict__[m] != other.__dict__[m]:
    #                 raise FeatureUnAddable( self, other )
    #             else:
    #                 prop[m] = self.__dict__[m]
    #
    #         # properties that should be updated
    #         for m in ["translation", "anticodon", "score", "rf", "copy", "part", "mito"]:
    #             if self.__dict__[m] is None and other.__dict__[m] is not None:
    #                 prop[m] = other.__dict__[m]
    #             elif self.__dict__[m] is not None and other.__dict__[m] is None:
    #                 prop[m] = self.__dict__[m]
    #             else:  # both eq None or both are not eq None
    #                 if self.__dict__[m] == other.__dict__[m]:
    #                     prop[m] = self.__dict__[m]
    #                 elif m in ["copy", "part"]:
    #                     prop[m] = min( self.__dict__[m], other.__dict__[m] )
    #                 else:
    #                     raise FeatureUnAddable( self, other )
    #
    #         # print translation
    #         return feature( name = prop["name"], tpe = prop["type"], start = prop["start"], \
    #                         stop = prop["stop"], strand = prop["strand"], method = prop["method"],
    #                         translation = prop["translation"], score = prop["score"], \
    #                         rf = prop["rf"], anticodon = prop["anticodon"],
    # copy = prop["copy"], part = prop["part"], mito = prop["mito"] )

    def midposition(self, circular, size):
        """
        get the mid position of a feature
        @param[in] circular circularity of the genome where the feature is located
        @param[in] size size of the genome where the feature is located
        @return midddle position
        """
        mid = self.start + int(math.ceil(self.length(circular, size) / 2.0))
        if circular:
            mid %= size
        return mid

    def overlap(self, other, circular, size):
        """
        check if two features overlap and return the overlap percentage, i.e.
        length of the intersection of the intervals / length of the union of the intervals

        @param self the feature
        @param other another feature
        @param size of the chromosom housing the feature
        @return overlap percentage (i.e. 100*cap/cup)
        """

        cap, cup = self.capcup(other, circular, size)

        return 100.0 * float(cap) / cup

    def getname(self):
        """
        get a printable represenation of the gene name including the copy and
        part information
        @return X_Y_Z where X is the gene name, Y the copy number, and the part number (as character)
        """

        return self.outputname()

    def bedstr(self, acc):
        """
        this function returns the string to be written in a bed file
        """
        if self.score is not None:
            s = str(self.score)
        else:
            s = "."

        return "%s\t%d\t%d\t%s\t%s\t%s" % (
            acc,
            self.start,
            self.stop + 1,
            self.getname(),
            s,
            self.plusminus(),
        )

    def gffstr(self, acc, features, size):
        """
                @param acc accession for col 1
                @param features all other features

                this function returns the string to be written in a ggf3 file
                http://gmod.org/wiki/GFF3#GFF3_Format).

        MT    insdc    ncRNA_gene    16039    16107    .    +    .    ID=gene:ENSGALG00000032370;biotype=Mt_tRNA;gene_id=ENSGALG00000032370;logic_name=mt_genbank_import;version=1
        MT    insdc    tRNA    16039    16107    .    +    .    ID=transcript:ENSGALT00000054114;Parent=gene:ENSGALG00000032370;biotype=Mt_tRNA;transcript_id=ENSGALT00000054114;version=1
        MT    insdc    exon    16039    16107    .    +    .    Parent=transcript:ENSGALT00000054114;Name=ENSGALE00000337021;constitutive=1;ensembl_end_phase=0;ensembl_phase=0;exon_id=ENSGALE00000337021;rank=1;version=1

        MT      insdc   ncRNA_gene      1297    2272    .       +       .       ID=gene:ENSGALG00000036956;biotype=Mt_rRNA;gene_id=ENSGALG00000036956;logic_name=mt_genbank_import;version=1
        MT      insdc   rRNA    1297    2272    .       +       .       ID=transcript:ENSGALT00000065851;Parent=gene:ENSGALG00000036956;biotype=Mt_rRNA;transcript_id=ENSGALT00000065851;version=1
        MT      insdc   exon    1297    2272    .       +       .       Parent=transcript:ENSGALT00000065851;Name=ENSGALE00000370359;constitutive=1;ensembl_end_phase=1;ensembl_phase=0;exon_id=ENSGALE00000370359;rank=1;version=1

        MT      insdc   gene    5241    6281    .       +       .       ID=gene:ENSGALG00000043768;Name=ND2;biotype=protein_coding;description=NADH dehydrogenase subunit 2 [Source:NCBI gene%3BAcc:807645];gene_id=ENSGALG00000043768;logic_name=mt_genbank_import;version=1
        MT      insdc   mRNA    5241    6281    .       +       .       ID=transcript:ENSGALT00000082968;Parent=gene:ENSGALG00000043768;Name=ND2-201;biotype=protein_coding;transcript_id=ENSGALT00000082968;version=1
        MT      insdc   exon    5241    6281    .       +       .       Parent=transcript:ENSGALT00000082968;Name=ENSGALE00000418957;constitutive=1;ensembl_end_phase=0;ensembl_phase=0;exon_id=ENSGALE00000418957;rank=1;version=1
        MT      insdc   CDS     5241    6281    .       +       0       ID=CDS:ENSGALP00000051543;Parent=transcript:ENSGALT00000082968;protein_id=ENSGALP00000051543

        origin?
        origin_of_replication

        """
        gff = []

        trnstype = None
        if self.part == 0 or self.part is None:
            parts = [x for x in features if x.name == self.name and x.copy == self.copy]
            genestart = parts[0].start
            genestop = parts[-1].stop
            if genestart > genestop:
                genestop += size
            if self.type == "gene":
                genetype = "gene"
                trnstype = None
            elif self.type in ["tRNA", "rRNA"]:
                genetype = "ncRNA_gene"
                trnstype = self.type
            elif self.type == "rep_origin":
                genetype = "origin_of_replication"
                trnstype = None
            elif self.type == "intron":
                genetype = self.type
                trnstype = None
            elif self.type == "orf":
                genetype = "ORF"
                trnstype = None
            else:
                raise Exception("Unknown type %s" % (self.type))

            gff.append(
                "{seqid}\t{source}\t{type}\t{start}\t{end}\t{score}\t{strand}\t{phase}\tID=gene_{name};Name={name};gene_id={name}".format(
                    seqid=acc,
                    source=self.method,
                    type=genetype,
                    start=genestart + 1,
                    end=genestop + 1,
                    score=".",
                    strand=self.plusminus(),
                    phase=".",
                    name=self.outputname(anticodon=False, part=False),
                )
            )
            if trnstype is not None:
                gff.append(
                    "{seqid}\t{source}\t{type}\t{start}\t{end}\t{score}\t{strand}\t{phase}\tID=transcript_{name};Name={name};Parent=gene_{name};gene_id={name}".format(
                        seqid=acc,
                        source=self.method,
                        type=trnstype,
                        start=genestart + 1,
                        end=genestop + 1,
                        score=".",
                        strand=self.plusminus(),
                        phase=".",
                        name=self.outputname(anticodon=True, part=False),
                    )
                )

            if self.type not in ["tRNA", "rRNA", "gene"]:
                return "\n".join(gff)

        if self.score is not None:
            s = str(self.score)
        else:
            s = "."

        # using rf as indicator for PCGs, phase is 0
        if self.rf is None:
            phase = "."
        else:
            phase = 0

        # exon
        start, stop = self.start, self.stop
        if start > stop:
            stop += size

        gff.append(
            "{seqid}\t{source}\t{type}\t{start}\t{end}\t{score}\t{strand}\t{phase}\tParent=transcript_{namep};Name={name}".format(
                seqid=acc,
                source=self.method,
                type="exon",
                start=start + 1,
                end=stop + 1,
                score=s,
                strand=self.plusminus(),
                phase=phase,
                namep=self.outputname(anticodon=False, part=False),
                name=self.outputname(anticodon=False),
            )
        )
        return "\n".join(gff)

    def tblstr(self):
        """
        this function returns the string to be written in a mito file
        """

        if int(self.strand) == 1:
            pos = "%d\t%d" % (self.start + 1, self.stop + 1)
        elif int(self.strand) == -1:
            pos = "%d\t%d" % (self.stop + 1, self.start + 1)
        else:
            raise Exception("Strand Error")
        if self.type == "gene":
            out = "%s\tgene\n" % (pos)
            out += "\t\t\tgene\t%s\n" % self.getname()
            out += "%s\tCDS\n" % (pos)
            out += "\t\t\tproduct\t%s\n" % (revprot[self.name])
        elif self.type == "tRNA":
            out = "%s\tgene\n" % (pos)
            out += "\t\t\tgene\t%s\n" % self.getname()
            out += "%s\ttRNA\n" % (pos)
            out += "\t\t\tproduct\ttRNA-%s\n" % (revtrnamap(self.name))
        elif self.type == "rRNA":
            out = "\t\t\tgene\t%s\n" % self.getname()
            out += "%s\trRNA\n" % (pos)
            out += "\t\t\tproduct\t%s-rRNA\n" % (rrnamap[self.name])
        elif self.type == "rep_origin" and self.name == "OH":
            out = "%s\tD-loop\n" % (pos)
            out += "\t\t\tnote\tcontrol region\n"
        elif self.type == "rep_origin" and self.name == "OL":
            out = "%s\trep_origin\n" % (pos)
            out += "\t\t\tnote\torigin of L-strand replication\n"
        elif self.type == "intron":
            out = "%s\tintron\n" % (pos)
            out += "\t\t\tnote\t%s\n" % self.getname()
        else:
            raise Exception("type error %s" % self.type)
        return out

    def mitostr(self, acc):
        """
        this function returns the string to be written in a mito file
        """
        if self.score is not None:
            s = str(self.score)
        else:
            s = "."

        if "bitscore" in self.__dict__:
            bs = self.bitscore
        else:
            bs = "."

        if self.anticodon is not None:
            acodon = self.anticodon.get_anticodon()
        else:
            acodon = "-"

        try:
            acpos = str(self.anticodonpos)
        except Exception:
            acpos = "-"

        if self.part is not None:
            part = str(self.part)
        else:
            part = "."
        if self.copy is not None:
            copy = str(self.copy)
        else:
            copy = "."

        try:
            struct = self.structure
        except Exception:
            struct = "."

        return "{acc}\t{tpe}\t{name}\t{meth}\t{start}\t{stop}\t{strand}\t{score}\t{bitscore}\t{anticodon}\t{anticodonpos}\t{part}\t{copy}\t{struct}".format(
            acc=acc,
            tpe=self.type,
            name=self.name,
            meth=self.method,
            start=self.start,
            stop=self.stop,
            strand=self.strand,
            score=s,
            bitscore=bs,
            anticodon=acodon,
            anticodonpos=acpos,
            part=part,
            copy=copy,
            struct=struct,
        )

    def outputname(self, anticodon=True, copy=True, part=True):
        """
        generate the name output name NAME(AC)_COPY-PART
        @param anticodon include anticodon
        @param copy include copy
        @param part include part
        """
        #        if self.name.startswith( "ND" ):
        #            return "nad%s" % self.name[2:].upper()
        #        if self.name == "CYTB":
        #            return "cob"
        #        if self.name == "12S":
        #            return "rrnS"
        #        if self.name == "16S":
        #           return "rrnL"
        #        if self.type == "gene":
        #            if self.name[-1] == "l" or self.name[-1] == "L":
        #                return self.name[:-1].lower() + "L"
        #            return self.name.lower()

        name = ""
        if self.type == "tRNA" and not self.name.startswith("trn"):
            name += "trn"

        name += self.name

        if copy and self.copy is not None:
            name += "_" + str(self.copy)
        if part and self.part is not None:
            name += "-" + chr(97 + self.part)
        if anticodon and self.type == "tRNA":
            if self.anticodon is not None:
                name += "(%s)" % self.anticodon.get_anticodon().lower()
            else:
                name += "(---)"

        return name

    def plusminus(self):
        """
        @return '+' if on positive strand, '-' else
        """
        if self.strand > 0:
            return "+"
        else:
            return "-"


class blast_feature(feature):
    """
    a feature predicted with blast;
    derived from feature with the additional properties:
    - qstart: avg. relative start position in the query
    - qstop : avg. relative stop position in the query
    """

    def __init__(
        self,
        name,
        tpe,
        strand,
        positions,
        mito,
        rf,
        scoresel="e",
        havg=False,
        pavg=False,
    ):
        """
        a feature determined from a list of consecutive positions with
        quality > 0, stores
        - _positions the positions
        - _evalue the evalue     determined as sum or average over all positions
        - _bitscore bitscore     --------------------"--------------------------
        - _height numer of hits  --------------------"--------------------------

        @param name the name of the feature
        @param tpe the type of the feature
        @param strand strandedness (+1/-1)
        @param positions: a list of positions, the first and the last in the list
            must be really the first and last position
        @param ascore: specify which value at the position should be used for
            the calculation of the score, 'h': height, 'e': (exponent of) evalue,
            'b': bitscore
        @param havg: if False then get the sum of the values at the positions,
            if True then get the average of the summed values (i.e. divided by length)
        @param pavg: False: Sum of the values at a position
            True: the average values at each position are summed
            (does not apply for height)
        @param mito
        @param rf
        """
        self._evalue = 0.0
        self._bitscore = 0.0
        self._height = 0.0
        self._positions = []

        self._havg = havg
        self._pavg = pavg
        self._scoresel = scoresel

        s = self.init_score(positions)
        feature.__init__(
            self,
            name,
            tpe,
            start=positions[0].get_position(),
            stop=positions[-1].get_position(),
            strand=strand,
            method="mitos",
            score=s,
            rf=rf,
        )

        self.update(positions, name, tpe, strand, mito, rf)

    def init_score(self, positions):
        """ """
        self._evalue = 0.0
        self._bitscore = 0.0
        self._height = 0.0
        self._positions = positions

        # number of positions
        ln = float(len(positions))
        # ln = float( len( positions[-1].get_position() - positions[0].get_position() + 1 ) )

        for p in positions:
            self._evalue += p.get_evalue(self._pavg)
            self._bitscore += p.get_bitscore(self._pavg)
            self._height += p.get_height()

        self._evalue /= ln
        self._bitscore /= ln
        self._height /= ln

        if self._scoresel == "h":
            s = self._height
        elif self._scoresel == "e":
            s = self._evalue
        elif self._scoresel == "b":
            s = self._bitscore
        else:
            raise Exception("init_score got invalid scoresel: %s" % self._scoresel)

        if self._havg is False:
            s *= ln

        s = round(s, 1)
        return s

    def update(self, positions, name=None, tpe=None, strand=None, mito=None, rf=None):
        """
        update the feature with a new set of positions
        see init for options

        the current value is kept for name, tpe, strand, mito, rf if parameter is None
        """
        s = self.init_score(positions)

        if rf is None:
            rf = self.rf
        if name is None:
            name = self.name
        if tpe is None:
            tpe = self.type
        if strand is None:
            strand = self.strand

        feature.__init__(
            self,
            name,
            tpe,
            start=positions[0].get_position(),
            stop=positions[-1].get_position(),
            strand=strand,
            method="mitos",
            score=s,
            rf=rf,
            copy=self.copy,
            part=self.part,
        )

        self.qstart = positions[0].get_query()
        self.qstop = positions[-1].get_query()

        if self.qstart > self.qstop:
            self.qstart, self.qstop = self.qstop, self.qstart

        if mito is not None:
            self.mito = mito

    def __str__(self):
        return "{0} {1:6.1f} {2:5.1f} {3:5.1f} {4:>4.3f}-{5:<4.3f} RF {RF}".format(
            feature.__str__(self),
            round(self._height, 1),
            round(self._evalue, 1),
            round(self._bitscore, 1),
            round(self.qstart),
            round(self.qstop),
            RF=self.rf,
        )


class blasthit_feature(feature):
    """
    a feature for blast data; derived from feature with the additional properties:
    - query name
    - evalue:
    - bitscore
    - qstart:
    - qstop :
    """

    def __init__(
        self, name, tpe, qname, start, stop, strand, rf, qstart, qstop, evalue, bitscore
    ):
        """
        constructor
        """

        feature.__init__(self, name, tpe, start, stop, strand, "BLAST", rf=rf)
        self.qname = qname
        self.qstart = qstart
        self.qstop = qstop
        self.evalue = evalue
        self.bitscore = bitscore

    def __str__(self):
        """
        get a string
        """
        return "{0:4}({1:>4},{2:1},{3:5d},{4:5d},{5:5}, {6}, {7})".format(
            self.type,
            self.getname(),
            self.plusminus(),
            self.start + 1,
            self.stop + 1,
            self.method,
            self.score,
            self.evalue,
        )


class trnafeature(feature):
    """
    a feature predicted with trna; derived from feature with the additional properties:
    @param score some raw score, e.g.  bitscore
    - structure:
    - anticodonpos:
    - anticdon :
    - sequence:
    """

    def __init__(
        self,
        name,
        tpe,
        start,
        stop,
        strand,
        method,
        score,
        sequence,
        struct,
        anticodonpos,
        anticodon,
    ):
        feature.__init__(self, name, tpe, start, stop, strand, method, score=score)

        self.structure = struct
        self.anticodonpos = anticodonpos
        self.anticodon = anticodon
        self.sequence = sequence
        return

    def __str__(self):

        if self.anticodon is not None:
            ac = " " + self.anticodon.get_anticodon()
        else:
            ac = ""

        return "{0}{1} score:{2:6.1f}\n{3}\n{4}".format(
            feature.__str__(self),
            ac,
            round(self.score, 1),
            self.structure,
            self.sequence,
        )


class mitfifeature(trnafeature):
    """
    a trnafeature predicted with mitfi; derived from trnafeature with the additional properties:
    - qstart:
    - qstop:
    - evalue
    - pvalue:
    - model:
    - local: It is 0 if it is a global hit and it is 1 if it is a local hit
    - mito: If we belive it is 2 if it is a copy it is 1 and if it is crap it is 0
    """

    def __init__(
        self,
        name,
        tpe,
        start,
        stop,
        strand,
        score,
        sequence,
        struct,
        anticodonpos,
        anticodon,
        qstart,
        qstop,
        evalue,
        bitscore,
        model,
        local=None,
        mito=None,
    ):
        trnafeature.__init__(
            self,
            name,
            tpe,
            start,
            stop,
            strand,
            "mitfi",
            score,
            sequence,
            struct,
            anticodonpos,
            anticodon,
        )

        self.qstart = qstart
        self.qstop = qstop
        self.evalue = evalue
        self.bitscore = bitscore
        self.model = model
        self.local = local
        self.mito = mito
        return
