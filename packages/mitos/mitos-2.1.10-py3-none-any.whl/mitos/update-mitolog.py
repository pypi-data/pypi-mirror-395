"""
@author: M. Bernt

update the log files to the latest format, i.e. from |-separated to json.
at the same time
- check that fragovl and maxovl are in [0:1] and not in [0:100] (fix if necessary)
- if jobid is not set yet, then set it to filename or hash
- get fastacontent and seqlen from sequence.fas files if possible
"""

import io
import json
import logging
import os
import shutil
import sys

from mitos import sequence


def loadjson(p):

    try:
        f = open(p, "r")
        job = json.load(f)
    except Exception:
        job = None
    finally:
        f.close()

    return job


def loadline(p):

    f = open(p, "r")
    line = f.readline().split("|")
    f.close()
    try:

        job = {
            "hsh": line[0],
            "name": line[1],
            "email": line[2],
            "code": int(line[3]),
            "filename": line[4],
            "clipfac": float(line[5]),
            "evalue": float(line[6]),
            "ststrange": int(line[7]),
            "finovl": float(line[8]),
            "fragovl": float(line[9]) / 100,
            "fragfac": float(line[10]),
            "maxovl": float(line[11]) / 100,
            "prot": int(line[12]),
            "trna": int(line[13]),
            "rrna": int(line[14]),
            "cutoff": "%" + line[15],
        }
    except Exception:
        job = None
    return job


def updatelog(p, restart):

    stat = os.stat(p)
    res = False
    job = loadjson(p)
    if job is None:
        job = loadline(p)
    if job is None:
        print("could not read ", p)
        return

    #     print job["clipfac"]    # : 10.0,
    #     print job["code"]    #: 2,

    if not str(job["cutoff"]).startswith("%"):
        job["cutoff"] = "%{c}".format(c=job["cutoff"])
        res = True
    if job["cutoff"].find(".") != -1:
        job["cutoff"] = job["cutoff"][: job["cutoff"].find(".")]

    #     print job["cutoff"] #[ "%50",
    #     print job["email"]#[ "bernt@informatik.uni-leipzig.de",
    #     print job["evalue"]#[ 2.0,
    job["finovl"] = int(job["finovl"])
    #     print job["finovl"]#[ 35,
    job["ststrange"] = int(job["ststrange"])
    #     print job["ststrange"]#[ 6,
    #     print job["fragfac"]#[ 10.0,
    if job["fragovl"] > 1:
        job["fragovl"] /= 100.0
        res = True

    if job["maxovl"] > 1:
        job["maxovl"] /= 100.0
        res = True

    #     print job["maxovl"]#[ 0.2,
    #     print job["fragovl"]#[ 0.2,
    #     print job["hsh"]#[ "DzwcZzzI",
    #     print job["name"]#[ "Matthias Bernt",
    if job["prot"]:
        job["prot"] = True
    else:
        job["prot"] = False
    #     print job["prot"], type(job["trna"])#[ true,
    if job["rrna"]:
        job["rrna"] = True
    else:
        job["rrna"] = False
    #     print job["rrna"]#[ false,
    if job["trna"]:
        job["trna"] = True
    else:
        job["trna"] = False
    #     print job["trna"]#[ false

    #     print job["fasta"]#[
    sequences = None
    pb = os.path.splitext(p)[0]
    if os.path.isfile(pb + "/sequence.fas"):
        f = open(pb + "/sequence.fas", "r")
        fasta = f.read()
        f.close()

        f = io.StringIO(fasta)
        sequences = sequence.sequence_info_fromfilehandle(f, circular=False)
        f.close()

        job["seqlen"] = len(sequences[0]["sequence"])
        job["fastacontent"] = fasta
    #         print job["seqlen"]
    #         print job["fastacontent"]

    if "jobid" not in job:
        if "fastacontent" in job:
            sequences[0]["description"]
        elif "filename" in job:
            job["jobid"] = job["filename"]
        else:
            job["jobid"] = job["hsh"]

    f = open(p, "w")

    for x in job:
        if isinstance(job[x], str):
            job[x] = job[x].decode("utf-8", "replace")
        json.dump(job, f, indent=3, sort_keys=True)
    f.close()

    if res and "fastacontent" in job:
        if restart:
            print("restart ", p)
            shutil.move(p, os.path.splitext(p)[0] + ".job")
        else:
            print(p)

    os.utime(p, (stat.st_atime, stat.st_mtime))
    return


if __name__ == "__main__":

    from optparse import OptionParser

    usage = "usage: %prog [options]"
    parser = OptionParser(usage)

    parser.add_option(
        "-d",
        "--dir",
        dest="dir",
        action="store",
        type="str",
        help="the dir file containing the log files",
    )
    parser.add_option(
        "-r",
        "--restart",
        dest="restart",
        action="store_true",
        default=False,
        help="restart jobs with erroneous data and sequence available",
    )
    (args, argss) = parser.parse_args()

    if args.dir is None:
        logging.error("no input dir given")
    sys.exit()

    for fn in os.listdir(args.dir):
        if not os.path.isfile(args.dir + "/" + fn):
            continue
        if os.path.splitext(fn)[1] != ".log":
            continue
        updatelog(args.dir + "/" + fn, args.restart)
