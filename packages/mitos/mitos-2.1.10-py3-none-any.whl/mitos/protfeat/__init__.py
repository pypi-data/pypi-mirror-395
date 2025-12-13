"""
Protein coding genes annotation, using enhanced HMMs guided by phylogeny
as described in http://dx.doi.org/10.1016/j.ympev.2016.09.024
"""

import copy
import glob
import logging
import math
import os

from mitos import feature, mito, sequence, util
from mitos.blast import (
    _create_protplotdata,
    _improve_start_stop,
    _improve_start_stop_old,
    position_values,
)
from mitos.mergefeature import _copy_part


def create_blast_feature(
    gene,
    seqstart,
    seqstop,
    strand,
    score,
    evalue,
    rf,
    hmstart,
    hmstop,
    mlen,
    method="mitos",
    tpe="gene",
):
    """
    function to create blast feature
    @param gene name of the gene
    @param seqstart sequence start
    @param seqstop sequence stop
    @param strand hit strand
    @param score hit score
    @param evalue hit evalue
    @param rf reading frame
    @param hmstart hit start
    @param hmstop hit stop
    @param mlen model length
    @param method  #MB ?
    @param tpe  type of feature (gene, tRNA or rRNA #MB ?)
    """
    try:
        evalue = -1 * math.log10(evalue)
    except ValueError:
        evalue = 300
    bitscore = score
    pvl = []
    for p in range(seqstart, seqstop + 1):
        pv = position_values(p)
        query = estimate_dis(mlen, hmstart, hmstop, seqstart, seqstop, p, strand)
        pv.add(evalue, bitscore, query, 1 - query)
        pvl.append(pv)
    bf = feature.blast_feature(gene, tpe, strand, pvl, 1, rf, "e", True, True)

    return bf


def hmmscan_call(seqfile, gene, dbfile, tmpDir):
    """
    function to call hmmscan from hmmer
    @param seqfile fasta file contains the sequences
    @param gene  name of the gene
    @param dbfile database file contains the models
    @param tmpDir directory for hmmscan output
    """
    outFile = tmpDir + "-" + gene + ".tbl"

    if os.path.exists(outFile):
        return

    cmd = [
        "hmmscan",
        "--domE",
        "0.999999",
        "--max",
        "--notextw",
        "--noali",
        "--domtblout",
        outFile,
        dbfile,
        seqfile,
    ]
    out, err = util.execute(cmd)
    with open(tmpDir + "-" + gene + ".out", "wb") as f:
        f.write(out)


def estimate_dis(mlen, hmstart, hmstop, seqstart, seqstop, p, strand):
    """
    function to estimate distance  to start or stop
    @param mlen model length
    @param hmstart hit start
    @param hmstop  hit stop
    @param seqstop sequence stop
    @param p position
    @param strand feature strand
    """
    fac = feature.length(hmstart, hmstop, False, 0) / float(
        feature.length(seqstart, seqstop, False, 0)
    )

    if strand == 1:
        ret = (hmstart + (p - seqstart) * fac) / float(mlen)
    else:
        ret = (hmstop - (p - seqstart) * fac) / float(mlen)
    return ret


def get_best_hits(mergedF, gene, seqLen, evalTh, finovl, circular):
    """
    function to return best hmmscan hit (minimum evalue, if equal then max bitscore)
    @param mergedF merged file contains all hmmscan hits
    @param gene name of the gene
    @param seqLen sequence length
    @param evalTh e-value threshold
    @param finovl overlap threshold (fraction of the shorter gene)
    @param circular is the sequence to be treated as circular (True / False)
    """

    data = []
    with open(mergedF, "r") as fp:
        for line in fp:
            if not line or line.startswith("#"):
                continue

            line = line.split()

            evalue = float(line[11])
            cevalue = float(line[12])
            bits = float(line[13])

            if bits <= 0 or (float(cevalue) >= evalTh and float(evalue) >= evalTh):
                continue

            end = int(line[18])  # prot end
            mend = int(line[16])  # model end
            a = line[0]
            start = int(line[17])  # prot start
            mstart = int(line[15])  # model start
            mlen = int(line[2])
            frame = int(line[-1])

            strand = get_strand(frame)
            nuc_s, nuc_e = get_nuc_pos(frame, start, end, seqLen)

            data.append(
                {
                    "nuc_e": nuc_e,
                    "mend": mend,
                    "evalue": evalue,
                    "cevalue": cevalue,
                    "a": a,
                    "bits": bits,
                    "nuc_s": nuc_s,
                    "mstart": mstart,
                    "mlen": mlen,
                    "frame": frame,
                    "strand": strand,
                }
            )

    data.sort(key=lambda k: (k["cevalue"], -1 * k["bits"], k["evalue"]))

    featlist = []
    for d in data:
        overlap = False

        t = create_blast_feature(
            gene,
            seqstart=d["nuc_s"],
            seqstop=d["nuc_e"],
            strand=d["strand"],
            score=d["bits"],
            evalue=d["evalue"],
            rf=d["frame"],
            hmstart=d["mstart"],
            hmstop=d["mend"],
            mlen=d["mlen"],
        )

        if t.length(circular, seqLen) % 3 != 0:
            raise Exception("Got blast feature %3 != 0")

        for f in featlist:
            cap, cup = f.capcup(t, circular, seqLen)
            if cap > finovl:
                overlap = True
                break

        if overlap is False:
            featlist.append(t)

    return featlist


def get_nuc_pos(frame, start, end, length):
    """
    function to transform amino acid position to nucleotide position
    @param frame frame from 0 to 5. 0 is +1 frame, 1 is -1, 2 is +2 ...
    @param start start of hit in amino acid position
    @param end end of hit in amino acid position
    @param length length of the genome
    """

    # make coordinates 0 based
    start -= 1
    end -= 1

    # positive frames
    if frame < 3:
        nuc_s = 3 * start + frame
        nuc_e = 3 * (end + 1) - 1 + frame

    # negative frames
    else:
        nuc_s = length - 1 - (3 * (end + 1) - 1) - (frame - 3)
        nuc_e = length - 1 - (3 * start) - (frame - 3)
    return nuc_s, nuc_e


#     01234567890123    l=14
# F5  333222111000      (0,3) ->
# F4   333222111000
# F3    333222111000    (1,2) -> (13-3*3-1, 13-3*1) = (5, 10)

# F0   000111222333
# F1    000111222333
# F2     000111222333

#     if frame == 0:
#         nuc_s = 3 * s
#         nuc_e = 3 * ( end + 1 )
#     elif frame == 1:
#         nuc_s = l - ( 3 * ( end + 1 ) )
#         nuc_e = l - ( 3 * s ) - 1
#     elif frame == 2:
#         nuc_s = 3 * s + 1
#         nuc_e = 3 * ( end + 1 ) + 1
#     elif frame == 3:
#         nuc_s = l - ( 3 * ( end + 1 ) + 1 )
#         nuc_e = l - ( 3 * s ) - 1 - 1
#     elif frame == 4:
#         nuc_s = 3 * ( s ) + 2
#         nuc_e = 3 * ( end + 1 ) + 2
#     elif frame == 5:
#         nuc_s = l - ( 3 * ( end + 1 ) + 2 )
#         nuc_e = l - ( 3 * s ) - 2 - 1
#     return nuc_s, nuc_e


def get_strand(frame):
    """
    function to return the strand of the prediction
    @param frame from 0 to 5. 0 is +1 frame, 1 is -1, 2 is +2 ...
    """
    if frame < 3:
        return 1
    else:
        return -1


def get_transtable(fname):
    with open(fname, "r") as inF:
        for line in inF:
            if "/transl_table" in line:
                return int(line.split("=")[1])
    return 1


def merge_frames(gene, fList, tmpDir):
    """
    function to read the hmmscan output for 6 frames and merge in one file
    append frame number to each line
    @param gene name of the gene
    @param fList list of files
    @param level phylogenetic level (root,class,phylum,order,family)
    @param tmpDir directory for hmmscan output
    """

    # todo split on regex 22 number
    fname = tmpDir + "-" + gene + "-" + "merged.tbl"
    with open(fname, "w") as outfile:
        header = open(fList[0], "r")
        head = [str(next(header)).rstrip() for x in range(3)]
        for line in head:
            outfile.write(str(line) + "\t" + "frame\n")
        header.close()
        for f in fList:
            frame = f.split("-")[-2][0]
            with open(f, "r") as infile:
                for line in infile:
                    if not line.startswith("#"):
                        line = line.rstrip() + "    " + frame + "\n"
                        outfile.write(str(line))
    return fname


def prot_feat_wrap(
    fastafiles,
    offsets,
    filepath,
    circular,
    startcod,
    stopcod,
    len_pval,
    trnas,
    refdir,
    minevalue=0,
    code=None,
    plot=False,
    finovl=100,
    fragfac=0.2,
    fragovl=0.2,
    oldstst=False,
):
    """
    wrapper function to call
    prot_feat for the different offsets

    @param fastafiles list of fastafiles, 1 per offset
    @param offsets list of offsets for the fastafiles
    @param filepath
    @param circular
    @param startcod start codon statistics
    @param stopcod stop codon statistics
    @param len_pval a dictionary containing for each gene the length pvalues
    @param trnas forbidden regions (for start stop)
    @param refdir directory with reference data
    @param minevalue
    @param code genetic code
    @param plot create plot data
    @param finovl maximum allowed overlap nt
    @param fragfac factor by which parts of the same feature may differ in quality
    @param fragovl overlap (fraction of the shorter) of query range that is allowed for parts of the same feature
    @param[in] oldstst use the old start stop prediction method of MITOS1
    @return feature list
    """

    features = []
    idx = {}
    values = []

    if len(fastafiles) != len(offsets):
        raise Exception("blast.blast called with |sequences|!=|offsets|")

    for i in range(len(offsets) - 1, -1, -1):
        logging.debug("prot_feat for offset %d" % offsets[i])

        oidx = dict()
        oval = []

        fasta = sequence.sequence_info_fromfile(fastafiles[i], circular=circular)
        seq = fasta[0]["sequence"]

        otrnas = copy.deepcopy(trnas)
        for t in otrnas:
            t.start = (t.start - offsets[i]) % len(seq)
            t.stop = (t.stop - offsets[i]) % len(seq)

        base = os.path.basename(fastafiles[i])
        tfl = prot_feat(
            seq,
            code,
            startcod,
            stopcod,
            len_pval,
            otrnas,
            oidx,
            oval,
            refdir,
            base,
            evalTh=minevalue,
            finovl=finovl,
            circular=circular,
            tmpDir=filepath,
            fragfac=fragfac,
            fragovl=fragovl,
            plot=plot,
            oldstst=oldstst,
        )

        # correct the feature positions for the offset
        for f in tfl:
            f.start = (f.start + offsets[i]) % len(seq)
            f.stop = (f.stop + offsets[i]) % len(seq)

            f.rf = math.copysign(((abs(f.rf) - 1) + (offsets[i] % 3)) % 3 + 1, f.rf)

            # the positions of the feature need not to be updated. this is done
            # below via values and the idx
            # for p in f._positions:
            #       p._position = ( p._position + offsets[i] ) % length
            features.append(f)

        # correct the idx and the values for the offset
        logging.debug("offset %d" % (offsets[i]))
        for n in oidx:  # names
            if n not in idx:
                idx[n] = dict()

            for of in oidx[n]:  # frames
                if abs(of) == 4:
                    f = of
                else:
                    f = math.copysign(((abs(of) - 1) + (offsets[i] % 3)) % 3 + 1, of)

                if f not in idx[n]:
                    idx[n][f] = dict()

                for op in oidx[n][of]:  # positions
                    p = (op + offsets[i]) % len(seq)
                    v = oval[oidx[n][of][op]]
                    v.set_position((v.get_position() + offsets[i]) % len(seq))

                    if p in idx[n][f]:
                        if v.get_score() > values[idx[n][f][p]].get_score():
                            values[idx[n][f][p]] = v
                    else:
                        idx[n][f][p] = len(values)
                        values.append(v)

    # output for plot histograms
    if plot:
        _create_protplotdata(filepath + "/hmm.dat", idx, values)

    return features


def prot_feat(
    seq,
    code,
    startcod,
    stopcod,
    len_pval,
    trnas,
    idx,
    values,
    refdir,
    filename="file",
    evalTh=0.006,
    finovl=100,
    circular=True,
    tmpDir="../tmpdir/",
    fragfac=0.2,
    fragovl=0.2,
    plot=True,
    oldstst=False,
):
    """
    main function for the protein prediction
    @param seq nucleotide sequence
    @param code genetic code
    @param startcod start codon statistics
    @param stopcod stop codon statistics
    @param len_pval a dictionary containing for each gene the length pvalues
    @param trnas forbidden regions (for start stop)
    @param idx dict analogous to blast based methods
    @param values list analogous to blast based methods
    @param filename name of the output file
    @param evalTh e-value threshold
    @param circular is the sequence to be treated as circular (True / False)
    @param finovl overlap threshold in nt
    @param fragfac factor by which parts of the same feature may differ in quality
    @param fragovl overlap (fraction of the shorter) of query range that is allowed for parts of the same feature
    @param plot create plot data
    @param[in] oldstst use the old start stop prediction method of MITOS1
    """
    #     if os.path.exists( tmpDir ):
    #         os.system( 'rm -r ' + tmpDir )
    if not os.path.exists(tmpDir):
        os.system("mkdir " + tmpDir)

    seqLen = len(seq)
    translations = trans_six_frames(seq, code)
    for rfidx, rf in enumerate(translations):
        protFile = tmpDir + filename + "-" + str(rfidx) + ".fas"
        with open(protFile, "w") as prot:
            prot.write(">" + filename + "-" + str(rfidx) + "\n")
            prot.write(str(rf))

        for gene in mito.metazoa_prot:
            dbFile = refdir + "/featureProtHMM/" + gene + ".db"
            if not os.path.exists(dbFile):
                logging.warning("skipping nonexistent hmmdb for %s" % gene)
                continue
            hmmscan_call(protFile, gene, dbFile, protFile)

    featlist = []

    for gene in mito.metazoa_prot:
        outDir = tmpDir + filename + "-?.fas-" + gene + ".tbl"
        outList = glob.glob(outDir)
        if len(outList) == 0:
            continue
        merged = merge_frames(gene, outList, tmpDir + filename)
        featlist += get_best_hits(merged, gene, seqLen, evalTh, finovl, circular)

    featlist.sort(key=lambda f: float(f.score), reverse=True)

    fixedlist = []
    for f in featlist:
        logging.debug("trying %s" % str(f))
        ov = False
        for g in fixedlist:
            cap, cup = f.capcup(g, circular, seqLen)
            if cap > finovl:
                logging.debug("\tovl with %s" % str(g))
                ov = True
                break
        if not ov:
            fixedlist.append(f)

    cpyprt = _copy_part(fixedlist, fragovl, fragfac)

    # improve start stop and create idx/values data structures
    # analogously to blast based methods
    f = open("%s/stst.dat" % (tmpDir), "w")
    for n in cpyprt:
        if n not in idx:
            idx[n] = {}
        for cpy in cpyprt[n]:
            if cpyprt[n][cpy][0].type != "gene":
                continue

            for part in range(len(cpyprt[n][cpy])):
                if not cpyprt[n][cpy][part].rf in idx[n]:
                    idx[n][cpyprt[n][cpy][part].rf] = {}
                for p in cpyprt[n][cpy][part]._positions:
                    idx[n][cpyprt[n][cpy][part].rf][p.get_position()] = len(values)
                    values.append(p)

            if oldstst:
                _improve_start_stop_old(
                    cpyprt[n][cpy], code, seq, len(seq), idx[n], values
                )
            else:
                plotdat = _improve_start_stop(
                    cpyprt[n][cpy],
                    seq,
                    code,
                    startcod,
                    stopcod,
                    len_pval,
                    idx[n],
                    values,
                    cpyprt,
                    trnas,
                    circular,
                )
                f.write(plotdat)
    f.close()

    return fixedlist


def trans_six_frames(seq, table):
    """
    function to translate the sequence in the six frames
    @param seq the sequence (string)
    @param table genetic code
    """

    ret = []
    rev = seq.reverse_complement()
    for i in range(3):
        if ((len(seq) - i) % 3) == 0:
            e = len(seq)
        else:
            e = -1 * ((len(seq) - i) % 3)
        ret.append(seq[i:e].translate(table, stop_symbol="X"))

    for i in range(3):
        if ((len(seq) - i) % 3) == 0:
            e = len(seq)
        else:
            e = -1 * ((len(seq) - i) % 3)
        ret.append(rev[i:e].translate(table, stop_symbol="X"))
    return ret


# def get_hit_val( mod, mergedF, seqLen ):
#     """
#     function to return sequence id (a), bitscore(b), a.a start(s), a.a end(end), frame(from 0 to 5), nucleotide start(nuc_s) , nuc end(nuc_e)
#     ceval(ceval), eval (eval), model start (ms), model end (mend), model length (mlen)
#
#     @param mod the hmmscan hit (model name+hit start + hit stop + frame)
#     @param mergedF merged file contains all hmmscan hits
#     @param seqLen sequence length
#     """
#     b = -1
#     s = -1
#     a = ''
#     with open( mergedF, 'r' )as fp:
#         nuc_s = -10  # nuc start
#         nuc_e = -10  # nuc end
#         eval = 20
#         data = []
#
#         for line in fp:
#             if not line.startswith( '#' ):
# #                 line.split()[0] + line.split()[-1] + '--' + line.split()[17] + '--' + line.split()[18])
# #                 print mod
#                 if mod.startswith( line.split()[0] ) and line.split()[-1].rstrip() == mod.split( '--' )[1] and line.split()[17] == mod.split( '--' )[2] and line.split()[18] == mod.split( '--' )[-1] :
#                     data.append( line.split() )
#                     break
#
#         if data:
#             if len( data ) == 1:
#                 end = data[0][18]  # prot end
#                 mend = data[0][16]  # model end
#                 eval = data[0][11]
#                 ceval = data[0][12]
#                 a = data[0][0]
#                 b = data[0][13]
#                 s = data[0][17]  # prot start
#                 ms = data[0][15]  # model start
#                 mlen = data[0][2]
#                 frame = data[0][-1]
#             # Me I think no need for this since we will get one hit because of appending start , stop and frame to the model name
#             elif len( data ) > 1:
#
#                 print " LEN >>> 1 "
#                 m = min( data, key = lambda x: float( x[11] ) )
#                 ind = []
#                 for x in data:
#                     if x[11] == m[11]:
#                         ind.append( data.index( x ) )
#
#                 if len ( ind ) == 1:
#                     end = data[ind[0]][18]
#                     mend = data[ind[0]][16]
#                     eval = data[ind[0]][11]
#                     ceval = data[ind[0]][12]
#                     a = data[ind[0]][0]
#                     b = data[ind[0]][13]
#                     s = data[ind[0]][17]
#                     ms = data[ind[0]][15]
#                     mlen = data[ind[0]][2]
#                     frame = data[ind[0]][-1]
#
#                 elif len( ind ) > 1:
#                     tmp = []
#                     for x in data:
#                         if data.index( x ) in ind:
#                             tmp.append( x )
#                     maxi = max( tmp, key = lambda x : float( x[7] ) )
#                     ind2 = []
#                     for x in data:
#                         if data.index( x ) in ind:
#                             if x[13] == maxi[13]:
#                                 ind2.append( data.index( x ) )
#                     if len( ind2 ) == 1:
#                         end = data[ind2[0]][18]
#                         mend = data[ind2[0]][16]
#                         eval = data[ind2[0]][11]
#                         ceval = data[ind2[0]][12]
#                         frame = data[ind2[0]][-1]
#                         a = data[ind2[0]][0]
#                         s = data[ind2[0]][17]
#                         ms = data[ind2[0]][15]
#                         b = data[ind2[0]][13]
#                         mlen = data[ind2[0]][2]
#
#                     if len( ind2 ) > 1:
#                         tmp2 = []
#                         for x in data:
#                             if data.index( x ) in ind2:
#                                 tmp2.append( x )
#                         mini = min( tmp2, key = lambda x : float( x[12] ) )
#                         ind3 = data.index( mini )
#                         end = data[ind3][18]
#                         mend = data[ind3][16]
#                         eval = data[ind3][11]
#                         ceval = data[ind3][12]
#                         frame = data[ind3][-1]
#                         s = data[ind3][17]
#                         ms = data[ind3][15]
#                         a = data[ind3][0]
#                         b = data[ind3][13]
#                         mlen = data[ind3][2]
#
#
# #             frame = frame.split('-')[1]
#             if s > 0:
#                 nuc_s, nuc_e = get_nuc_pos( frame, s, end, seqLen )
#
#             if s < 0:
#                 print 'Record not found!'
#                 return
#
# return a, b, s, frame, nuc_s, nuc_e, float( eval ), float( ceval ), end,
# ms, mend, mlen

# def floatequal( f1, f2 ):
#     """
#     function to check if two float numbers are equal
#     @param f1 float number
#     @list list of data
#     """
# #     print " floatequal ", f1, list
#     equal = False
# #     for f2 in list:
# #         if abs( Decimal( f1 ) - Decimal( f2 ) ) < 0.00001:
# #             equal = True
#     if abs( float( f1 ) - float( f2 ) ) < 0.000001:
#         equal = True
#     return equal

# def index_2d( myList, v, bs ):
#     """
#     function to return the index of a decimal value
#     @param myList dat list contains the values of the hits
#     @param v value to return the index for
#     @param bs True if it's bitscore or False if it is evalue
#     """
#     ind = []
# #     if v == 0.0:
# #         v = 0
# #     if '-' in str( v ):
# #         if len( str( v ).split( '-' )[1] ) == 1:
# #             print str( v ).split( '-' )[1]
# #             v = str( v ).split( '-' )[0] + '-0' + str( v ).split( '-' )[1]
# #     for i, x in enumerate( myList ):
# #         if str( v ).lower() in x or floatequal( v, x ) :
# #             ind.append( i )
#     for i , x in enumerate( myList ):
#         if bs:
#             if floatequal ( float( x[0] ), v ):  # x[0] is the bitscore, x[1] is the evalue
#                 ind.append( i )
#         else:
#             if floatequal( float( x[1] ), v ) :  # x[0] is the bitscore, x[1] is the evalue
#                 ind.append( i )
#
#     return ind


# def get_rf( f ):
#     """
#     function to return the reading frame
#     NOTE: FRAME NUMBERING NOT IN ACCORDANCE TO BLAST module
#     @param f frame take values from 0 to 5.
#     """
#     if f == 0 :
#         return 1
#     elif f == 1:
#         return -1
#     elif f == 2:
#         return 2
#     elif f == 3:
#         return -2
#     elif f == 4:
#         return 3
#     elif f == 5:
#         return -3


#     mod = []
#     with open( mergedF, 'r' ) as fp:
#         for line in fp:
#             if not line or line.startswith( '#' ):
#                 continue
#             # construct string name, start, stop, frame
#             mod.append( line.split()[0] + '--' + line.split()[-1] + '--' + line.split()[17] + '--' + line.split()[18] )
#
#     mod = set( mod )
#     data = []
#     best = []
#     featlist = []
#     if mod:
#         for m in mod:
#             # b  = bitscore
#             a, b, s, frame, nuc_s, nuc_e, eval, ceval, end, hmstart, hmstop, mlen = get_hit_val( m, mergedF, seqLen, evalTh )
#             if frame:
#                 strand = get_strand( int( frame ) )
#                 rf = get_rf( int( frame ) )
#
#                 if b > 0 and ( float( ceval ) < evalTh or float( eval ) < evalTh ):
#                     data.append( [b, ceval, nuc_s, nuc_e, strand, s, end, frame, hmstart, hmstop, mlen, rf] )
#
#         if data:
#             if len( data ) == 1:
#                 ind = [0]
#             else:
#                 mi = min( float( c[1] ) for c in data )
#                 ind = index_2d( data, mi, False )
#               #     print srt
#             ind2 = -1
#             ma = -10
#
#             if len( ind ) > 1:
#
#                 for i in ind:
#                     if float( data[i][0] ) > ma:
#                         ma = float( data[i][0] )
#
#                 ind2 = random.choice( index_2d( data, ma, True ) )
#                 best = data[ind2]
#                 best_ind = ind2
#             else:
#                 best = data[ind[0]]
#                 best_ind = ind[0]
#
#             # sort according to ceval TODo bitscore, evalue
#             srt = sorted( data, key = lambda k: float( k[1] ) )
# #             print srt , gene
#             res = []
#             res.append( data[best_ind] )
# #             f1 = feature(gene,'gene',int(best[2]),int(best[3]),best[4],'mitos',score = best[0])
#             f1 = create_blast_feature( gene, int( best[2] ), int ( best[3] ), best[4], best[0], best[1], int( best[11] ), int( best[8] ), int( best[9] ), int( best[10] ) )
# #             print f1._bitscore
#             featlist.append( f1 )
#             for d in srt:
#                 overlap = False
# #                 f2 = feature(gene,'gene',int(d[2]),int(d[3]),int(d[4]),'mitos',score = d[0])
#                 f2 = create_blast_feature( gene, int( d[2] ), int( d[3] ), d[4], d[0], d[1], int( d[11] ), int ( d[8] ), int ( d[9] ), int( d[10] ) )
# #                 print f2._bitscore
#                 cap12, cup12 = f1.capcup( f2, circular, seqLen )
#                 for r in res:
# #                     f3 = feature(gene,'gene',int(r[2]),int(r[3]),int(r[4]),'mitos', score = r[0])
#                     f3 = create_blast_feature( gene, int( r[2] ), int( r[3] ), r[4], r[0], r[1], int( r[11] ), int ( r[8] ), int ( r[9] ), int ( r[10] ) )
# #                     print f3._bitscore
#                     cap23, cup23 = f2.capcup( f3, circular, seqLen )
#                     if float( cap23 ) / f2.length( circular, seqLen ) > ovTh or float( cap23 ) / f3.length( circular, seqLen ) > ovTh:
#                         overlap = True
#                 if overlap == False:
#                     res.append( d )
#                     featlist.append( f2 )
#
#     return featlist

# def test () :
#     for f in glob.glob('/homes/brauerei2/marwa/phd/tool/mtdb/data/trees_and_data/prot6frames-test/bedroot/root-final-ov25/*.bed'):
#         acc = os.path.basename(f).split('.')[0]
#         gb ="/homes/brauerei2/marwa/phd/gc/RefSeq/outputdir1/refseq69-gb/"+acc +'.gb'
#         fas ='/scr/k61san/marwa/RefSeq-h2/refseq69-fasta/'+acc+'.fas'
#         seq = str(SeqIO.read(fas, "fasta").seq)
#         gc = get_transtable(gb)
#
#         fxlist = prot_feat( seq, gc, filename = acc, level = 'root', tmpDir = "../tmpdir/")
#
#         bedwriter( fxlist, acc, outfile = "../tmpdir/bed/"+acc+'.bed', mode = "w" )
