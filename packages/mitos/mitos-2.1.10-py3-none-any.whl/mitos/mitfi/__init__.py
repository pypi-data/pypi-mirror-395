"""
@author: M. Bernt
"""

import glob
import logging
import os
import re
from shutil import rmtree
from tempfile import mkdtemp

from mitos import feature, mito, trna, util


class InfernalException(Exception):
    def __init__(self, command_line, exit_code, stderr):
        self.command_line = command_line
        self.exit_code = exit_code
        self.stderr = stderr

    def __str__(self):
        return "command: %s exit code %s stderr %s" % (
            self.command_line,
            self.exit_code,
            self.stderr,
        )


def cmsearch(
    seqfile,
    outpath,
    code,
    refdir,
    evalue,
    sensitive,
    length,
    gl=True,
    RNAlist=None,
    trna=True,
    rrna=True,
    ori=True,
    intron=True,
    trnaovl=10,
    rrnaovl=10,
):
    """
    run
    1. cmsearch (infernal) on one given file using available models in refdir
    2. mitfi for the tRNAs and rRNAs

    @param[in] seqfile input file name
    @param[in] outpath output file name
    @param[in] code genetic code table to use for tRNA naming
    @param[in] refdir refdir directory containing reference data
    @param[in] evalue evalue threshold to apply to cmsearch
    @param[in] sensitive if true run cmsearch in sensitive mode
    @param[in] length original sequence length to be used for e-value computation
    @param[in] gl if true then run cmsearch with option -g
    @param[in] RNAlist list of RNAs to check (e.g. "rrnS", "rrnL")
            - if this option is set only the specified models are run
            - trna or rrna must be set to true if mitfi should be run
              for tRNAs or rRNA

    @param[in] trna iff True run mitfi for tRNA models
    @param[in] rrna iff True run mitfi for rRNA models
    @param[in] ori iff True run mitfi on OL model
    @param[in] intron iff True run mitfi on intron models
    @param[in] trnaovl max overlap allowed between trna
    @param[in] rrnaovl max overlap allowed between rrna
    """
    #     import inspect
    #     frame = inspect.currentframe()
    #     args, _, _, values = inspect.getargvalues( frame )
    #     logging.debug( 'function name "%s"' % inspect.getframeinfo( frame )[2] )
    #     for i in args:
    #         logging.debug( "    %s = %s" % ( i, values[i] ) )

    #     logging.debug( "start cmsearch %s trna %s rrna %s sens %s" % ( str( RNAlist ), str( trna ), str( rrna ), str( sensitive ) ) )

    # set infernal variables
    cmsargs = ["cmsearch", "--cpu", "1"]  # enforce serial processing
    cmsargs.append("--notextw")  # unlimited textwidth in output
    # get more memory otherwise we get an error from cmsearch for the rRNA
    cmsargs += ["--smxsize", "80000"]

    # turn off the HMM glocal Fwd composition bias filter if the hmm
    # filters are used, i.e. in insensitive mode.
    # (because --noF4b and --nohmm / --max are incompatible)
    if not sensitive:
        cmsargs.append("--noF4b")

    mitfipath = os.path.join(os.path.dirname(__file__), "parser", "mitfi_import.jar")
    mitfficodepath = os.path.join(
        os.path.dirname(__file__), "parser", "mitfiGeneticCodes"
    )
    mitfiargs = ["java", "-jar", mitfipath]

    # general arguments for mitfi and cmsearch
    # - infernal e-value treshold (applies to infernal 1.0 and 1.1)
    # - and mitfi parameters code, codefile, "structure wanted", and genome file
    cmsargs += ["-E", "%e" % (evalue)]
    mitfiargs += [
        "-code",
        str(code),
        "-codefile",
        mitfficodepath,
        "-structure",
        "-genome",
        seqfile,
        "-glength",
        str(length),
        "-evalue",
        str(evalue),
    ]

    # add additional parameters for glocal or local search
    if gl:
        mitfiargs += ["-method", "g"]
        cmsargs += ["-g"]
    else:
        mitfiargs += ["-method", "l"]

    # determine the models that should be run
    files = []
    if RNAlist is not None:
        for r in RNAlist:
            files.append("{refdir}/ncRNA/{rna}.cm".format(refdir=refdir, rna=r))
            if not os.path.exists(files[-1]):
                logging.error("ignoring non-existent model %s " % (files[-1]))
                del files[-1]
    else:
        files += glob.glob("{refdir}/ncRNA/*.cm".format(refdir=refdir))

    # sort the files (for debugging its easier to check whether a certain
    # model was executed if the list is sorted :) )
    files.sort()
    if len(files) == 0:
        raise Exception("No model found in {refdir}".format(refdir=refdir))

    mitfi_spec = {}
    mitfi_spec["rRNA"] = ["-overlap", str(rrnaovl), "-ribosomal"]
    mitfi_spec["tRNA"] = ["-overlap", str(trnaovl)]
    mitfi_spec["rep_origin"] = ["-overlap", str(trnaovl), "-ribosomal"]
    mitfi_spec["intron"] = ["-overlap", str(trnaovl), "-ribosomal"]

    # run cmsearch for each model and collect the -in parameters for mitfi
    for m in files:
        #         logging.debug( "cmsearch %s" % ( m ) )
        ms = os.path.splitext(os.path.basename(m))[0]
        outfile = "%s/%s_%s.cmout" % (outpath, os.path.basename(seqfile), ms)

        cmsargssen = []
        if sensitive:
            if ms.startswith("rrn"):
                cmsargssen.append("--nohmm")
            else:
                cmsargssen.append("--max")

        if ms.startswith("rrn") and rrna:
            mitfi_spec["rRNA"] += ["-in", outfile]
        elif ms.startswith("trn") and trna:
            mitfi_spec["tRNA"] += ["-in", outfile]
        elif ms.startswith("OL") and ori:
            mitfi_spec["rep_origin"] += ["-in", outfile]
        elif ms.startswith("Intron") and intron:
            mitfi_spec["intron"] += ["-in", outfile]
        else:
            continue

        if os.path.exists(outfile):
            continue

        # set sensitivity depending of tRNA or rRNA
        out, err = util.execute(cmsargs + cmsargssen + [m, seqfile], InfernalException)
        with open(outfile, "wb") as f:
            f.write(out)

    # run mitfi
    for t in mitfi_spec:
        if mitfi_spec[t].count("-in") == 0:
            continue
        #         if os.path.exists( "%s/%s_%sout.nc" % ( outpath, t, os.path.basename( seqfile ) ) ):
        #             continue

        logging.debug("mitfi for %s" % t)
        out, err = util.execute(mitfiargs + mitfi_spec[t], InfernalException)
        with open(
            "%s/%s_%sout.nc" % (outpath, os.path.basename(seqfile), t), "wb"
        ) as f:
            f.write(out)

    #     # run mitfi for tRNAs
    #     # - trnas are to be predicted (and not only the rRNAs)
    #     # - mitfi output does not exist
    #     if trna and ( not os.path.exists( "%s/%s_tRNAout.nc" % ( outpath, os.path.basename( seqfile ) ) ) ):
    #         logging.debug( "mitfi for tRNA" )
    #         logging.debug( " ".join( mitfiargs + mitfitRNA ) )
    #         proc = subprocess.Popen( mitfiargs + mitfitRNA, \
    #                                      stdout = subprocess.PIPE, \
    #                                      stderr = subprocess.PIPE )
    #         out, err = proc.communicate()
    #         if proc.returncode != 0 or len( err ) > 0:
    #             logging.error( "mitfi exception\n%s" % err )
    #             raise InfernalException( err )
    #         else:
    #             f = open( "%s/%s_tRNAout.nc" % ( outpath, os.path.basename( seqfile ) ), "w" )
    #             f.write( out )
    #             f.close()
    #
    #     # run mitfi for rRNAs
    #     if ( ori or rrna ) and ( not os.path.exists( "%s/%s_rRNAout.nc" % ( outpath, os.path.basename( seqfile ) ) ) ):
    #         logging.debug( "mitfi for rRNA" )
    #         logging.debug( " ".join( mitfiargs + mitfirRNA ) )
    #         proc = subprocess.Popen( mitfiargs + mitfirRNA , \
    #                                      stdout = subprocess.PIPE, \
    #                                      stderr = subprocess.PIPE )
    #         out, err = proc.communicate()
    #         if proc.returncode != 0 or len( err ) > 0:
    #             logging.error( "mitfi exception\n%s" % err )
    #             raise InfernalException( err )
    #         else:
    #             f = open( "%s/%s_rRNAout.nc" % ( outpath, os.path.basename( seqfile ) ), "w" )
    #             f.write( out )
    #             f.close()
    #        print "java -jar %s -method %s -code %d -codefile %s -structure -ribosomal -genome %s %s > %s/rRNAout.nc"\
    #               % ( mitfi, glopt, code, CONFIG.MITFICODE, seqfile, rRNAinline, outpath )
    #        subprocess.call( "java -jar %s -method %s -code %d -codefile %s -structure -ribosomal -genome %s %s > %s/rRNAout.nc"\
    #               % ( mitfi, glopt, code, CONFIG.MITFICODE, seqfile, rRNAinline, outpath ), shell = True )
    logging.debug("end cmsearch")


def cmrealign(sequence, rRNA, refdir):
    """
    function to realign a subsequence to a model in order to get the structure.

    @param[in] sequence sequence to realign
    @param[in] rRNA type of rRNA to realign (rrnS/rrnL)
    @param[in] refdir directory containing reference data
    @return structure
    """

    # set infernal version specific variables
    args = ["cmalign", "--cpu", "0", "--mxsize", "8192"]

    tdir = mkdtemp()

    # write sequence to tmp file
    f = open(tdir + "/cmrealign.fas", "w")
    f.write("> rnasubsequence\n")
    f.write("%s\n" % str(sequence))
    f.close()

    if rRNA == "rrnS" or rRNA == "rrnL":
        model = "{refdir}/ncRNA/{name}.cm".format(refdir=refdir, name=rRNA)
    else:
        logging.error("cmrealign: unknown model %s" % rRNA)
        return

    # realign
    args += ["-o", "%s/cmrealign.stk" % tdir, model, "%s/cmrealign.fas" % tdir]
    # print " ".join( args )

    out, err = util.execute(args, InfernalException)

    with open("%s/cmrealign.out" % tdir, "w") as f:
        f.write(str(out))

    mitfiimppath = os.path.join(
        os.path.dirname(__file__), "parser", "improve_infernal_structure.jar"
    )

    # improve structure
    out, err = util.execute(
        ["java", "-jar", mitfiimppath, tdir, "%s/cmrealign.stk" % (tdir)],
        InfernalException,
    )
    with open("%s/cmrealign.str" % tdir, "w") as f:
        f.write(str(out))
    # get structure
    with open(tdir + "/cmrealign.str") as f:
        structure = f.readlines()[2].strip()

    rmtree(tdir)

    return structure


def mitfi(
    fastafiles,
    offsets,
    outpath,
    code,
    refdir,
    evalue,
    sensitive,
    length,
    gl=True,
    RNAlist=None,
    trna=True,
    rrna=True,
    ori=True,
    intron=True,
    trnaovl=10,
    rrnaovl=10,
):
    """
    wrapper calling
    1. cmserach
    2. parse
    for a list of offsets. returned positions are corrected for the offset.

    @return the list of features fount for all offsets
    """

    features = []
    if len(fastafiles) != len(offsets):
        raise Exception("mitfi.mitfi called with |sequences|!=|offsets|")

    for i in range(len(offsets)):

        cmsearch(
            fastafiles[i],
            outpath,
            code,
            refdir,
            evalue,
            sensitive,
            length,
            gl,
            RNAlist,
            trna,
            rrna,
            ori,
            intron,
            trnaovl,
            rrnaovl,
        )
        tfl = parse(outpath, fastafiles[i], trna, rrna, ori, intron)

        for f in tfl:

            f.start = (f.start + offsets[i]) % length
            f.stop = (f.stop + offsets[i]) % length
            features.append(f)
            # logging.debug( "offset %d %s" %(offsets[i], f))

    return features


def remove_empty(trna, rrna, ori, intron, rnalist, mitfipath, offsets):
    """
    remove cmsearch output of models that are not included in the given list of rnas

    @param[in] trna do trna prediction (dont remove old results if in this run no tRNAs are to be predicted)
    @param[in] rrna do rrna prediction (dont remove old results if in this run no rRNAs are to be predicted)
    @param[in] rnalist list of rnas
    @param[in] mitfipath the path to delete the cmoutput in
    @param[in] offsets the offsets to remove the empty files

    @return True iff something was removed
    """

    ret = False

    for o in offsets:
        mitfidel = set()
        for t in mito.metazoa_trna + mito.rrna + mito.rep_origin + mito.intron:
            if not (t in [x.name for x in rnalist]):
                files = glob.glob("%s/*-%d_%s.cmout" % (mitfipath, o, t))
                for f in files:
                    # delete file if it was not already computed in sensitive mode
                    # and also delete the mitfi output if necessary
                    dlt = True
                    fh = open(f)
                    for line in fh:
                        if ("Max sensitivity mode" in line) or ("CM-only mode" in line):
                            dlt = False
                    fh.close()

                    if dlt:
                        # delete cmserach mark mitfi output for deletion
                        if trna and "trn" in t:
                            mitfidel.add("tRNA")
                            logging.debug("recompute %s" % f)
                            os.remove(f)
                        elif rrna and "rrn" in t:
                            mitfidel.add("rRNA")
                            logging.debug("recompute %s" % f)
                            os.remove(f)
                        elif ori and "OL" in t:
                            mitfidel.add("rep_origin")
                            logging.debug("recompute %s" % f)
                            os.remove(f)
                        elif intron and "intron" in t:
                            mitfidel.add("intron")
                            logging.debug("recompute %s" % f)
                            os.remove(f)

        # delete mitfi output if necessary, e.g., NC_014578.fas-0_rRNAout.nc
        for x in ["tRNA", "rRNA", "rep_origin", "intron"]:
            files = glob.glob("%s/*-%d_%sout.nc" % (mitfipath, o, x))
            for f in files:
                os.remove(f)
                ret = True

    return ret


def parse(inpath, seqfile, incl_trna, incl_rrna, incl_ori, incl_intron, minmito=1):
    """
    parses all mitfifiles in a given directory and returns list of features
    @parm inpath filehandler mitfifile
    @param seqfile get only the mitfi output from the results belonging to seqfile
    @param trna accept trnas
    @param rrna accept rrna
    @param intron accept introns
    @param minmito minimum value of the mito property to accept a feature
    @return feature list
    """

    features = []
    files = glob.glob(inpath + "/%s_*.nc" % (os.path.basename(seqfile)))
    for resultfile in files:
        mitfihandle = open(resultfile)
        # counts in witch line is next
        # 1 = first line of feature
        # 2 = sequence of feature
        # 3 = struct of feature
        linecounter = 1
        # read the 3. line
        for line in mitfihandle:
            line = line.strip()
            if line == "":
                continue
            if linecounter == 1:
                # logging.debug( line )
                cols = line[1:].split("|")
                # print cols
                # cols:
                # acc = cols[0]                               #ID
                # code = int( cols[1] )                       #code
                start = int(cols[2]) - 1  # genom-start-position
                stop = int(cols[3]) - 1  # genom-ende-position
                strand = int(cols[4])  # strand
                qstart = int(cols[5]) - 1  # model-start-position
                qstop = int(cols[6]) - 1  # model-ende-position
                bitscore = float(cols[7])  # infernal-bitscore
                evalue = float(cols[8])  # e-value
                # pvalue was only set in the 1.0 version .. later on ignored and set to 0 for output compatibility
                # pvalue = float( cols[9] )  # p-value
                # gccontent = int( cols[10] )                 #GC-content
                anticodonpos = int(cols[11]) - 1  # Anticodon-start-position
                if anticodonpos >= 0:  # Anticodon
                    anticodon = trna.codon(cols[12], "anticodon")
                else:
                    anticodon = None
                    anticodonpos = None

                # TODO: this regex is a workaround to the new model names
                # which are not correctly treated by mitfi
                mt = re.match(r"trn(\w\d*)", cols[13])
                mr = re.match(r"(rrn[SL])", cols[13])
                if mt is not None:
                    name = mt.group(1)
                elif mr is not None:
                    name = mr.group(1)
                else:
                    name = cols[13]  # amino acid name

                model = cols[14]  # model
                tophit = int(cols[15])  # tophit=1
                kopie = int(cols[16])  # Kopie=1

                if cols[17].strip() == "g":  # g(lobal) oder l(okal)
                    local = 0
                else:
                    local = 1

                if tophit:
                    mito = 2
                elif kopie:
                    mito = 1
                else:
                    mito = 0

                if model.startswith("OL"):
                    tpe = "rep_origin"
                    name = "OL"
                    model = "OL"
                elif model.startswith("rrnS"):
                    tpe = "rRNA"
                    name = "rrnS"
                    model = "rrnS"
                elif model.startswith("rrnL"):
                    tpe = "rRNA"
                    name = "rrnL"
                    model = "rrnL"
                elif model.startswith("Intron"):
                    tpe = "intron"
                    model = model.split(".")[0]
                    name = model.split("_")[1]
                else:
                    tpe = "tRNA"
                    model = model[8:-7]
                    name = "trn%s" % (name)
                linecounter = 2
            elif linecounter == 2:
                sequence = line.strip()
                linecounter = 3
            else:
                structure = re.sub(r"[-]", ".", line.strip())
                linecounter = 1

                if (
                    (not incl_trna and tpe == "tRNA")
                    or (not incl_rrna and tpe == "rRNA")
                    or (not incl_ori and tpe == "rep_origin")
                    or (not incl_intron and tpe == "intron")
                ):
                    continue
                # remove t/r-RNA conflicting with other t/r-RNA features
                if mito < minmito:
                    continue
                # probably due to a bug in infernat (1.1.1) extremely short features
                # are reported (e.g. 1nt) => we ignore them until fixed
                nf = feature.mitfifeature(
                    name=name,
                    tpe=tpe,
                    start=start,
                    stop=stop,
                    strand=strand,
                    score=evalue,
                    sequence=sequence,
                    struct=structure,
                    anticodonpos=anticodonpos,
                    anticodon=anticodon,
                    qstart=qstart,
                    qstop=qstop,
                    evalue=evalue,
                    bitscore=bitscore,
                    model=model,
                    local=local,
                    mito=mito,
                )
                if (nf.length(False, 0)) <= 10:
                    #                     logging.warn( "mitfi: ignoring feature <= 10nt %s" % ( str( nf ) ) )
                    continue

                #                 logging.debug( "add %d %s" % ( mito, str( nf ) ) )

                features.append(nf)
    #         mitfihandle.close()

    return features


def parse_feature(inpath, seqfile, local, name, start, stop, strand):
    """
    get a certain feature from the mitfi file

    @param name name of the feature
    @param start start position of the feature
    @param stop stop position of the feature
    @param strand strand of the feature
    """

    # get the feature(s) matching the name, start, stop, and strand
    features = [
        x
        for x in parse(inpath, seqfile, local)
        if (
            x.name == name
            and x.start == start
            and x.stop == stop
            and x.strand == x.strand
        )
    ]

    if len(features) == 1:
        return features[0]
    elif len(features) == 0:
        logging.error(
            "no feature %s %d %d %d found in %s" % (name, start, stop, strand, inpath)
        )
        return None
    else:
        logging.error(
            "more than one feature %s %d %d %d found in %s"
            % (name, start, stop, strand, inpath)
        )
        return features[0]
