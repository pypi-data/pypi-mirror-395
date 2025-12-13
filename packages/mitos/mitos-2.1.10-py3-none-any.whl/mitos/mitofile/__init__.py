"""
@author: M. Bernt
"""

from sys import stdout

from mitos import trna
from mitos.feature import feature, mitfifeature
from mitos.gb import gb


def mitowriter(featurelist, acc, outfile, mode="w"):

    featurelist.sort(key=lambda x: x.start)

    if isinstance(outfile, str) or isinstance(outfile, str):
        f = open(outfile, mode)
        for feat in featurelist:
            f.write("%s\n" % feat.mitostr(acc))
        f.close()
    elif outfile is None:
        for feat in featurelist:
            stdout.write("%s\n" % feat.mitostr(acc))
    else:
        for feat in featurelist:
            outfile.write("%s\n" % feat.mitostr(acc))


class mitofromfile(gb):
    def __init__(self, mitofile):
        gb.__init__(self)

        cnf = {
            # 11: {"acc":0, "type":1, "name":2, "method":3, "start":4, "stop":5, "strand":6, "score":7, "anticodon":8, "part":9, "copy":10},
            # 12: {"acc":0, "type":1, "name":2, "method":3, "start":4, "stop":5, "strand":6, "score":7, "anticodon":8, "part":9, "copy":10, "struct":11},
            13: {
                "acc": 0,
                "type": 1,
                "name": 2,
                "method": 3,
                "start": 4,
                "stop": 5,
                "strand": 6,
                "score": 7,
                "anticodon": 8,
                "part": 9,
                "copy": 10,
                "struct": 11,
                "anticodonpos": 12,
            },
            14: {
                "acc": 0,
                "type": 1,
                "name": 2,
                "method": 3,
                "start": 4,
                "stop": 5,
                "strand": 6,
                "score": 7,
                "bitscore": 8,
                "anticodon": 9,
                "anticodonpos": 10,
                "part": 11,
                "copy": 12,
                "struct": 13,
            },
        }

        # ACC    type    name    method    start    stop    strand    score/.    anticodon/-    part/.    copy/.
        # ACC    type    name    method    start    stop    strand    score/.    anticodon/-    part/.    copy/. structure
        # ACC    type    name    method    start    stop    strand    score/. bitscore/.   anticodon/-    part/.    copy/. structure

        data = {
            "acc": None,
            "type": None,
            "name": None,
            "method": None,
            "start": None,
            "stop": None,
            "strand": None,
            "score": None,
            "bitscore": None,
            "anticodon": None,
            "anticodonpos": None,
            "part": None,
            "copy": None,
            "struct": None,
        }

        ncol = None

        mitohandle = open(mitofile)
        for line in mitohandle:
            line = [x.strip() for x in line.split()]

            if ncol is not None and ncol != len(line):
                raise Exception("inconsistent column number")
            ncol = len(line)
            for f in data:
                try:
                    data[f] = line[cnf[ncol][f]]
                except KeyError:
                    data[f] = None

                if data[f] == "." or data[f] == "-" or data[f] == "None":
                    data[f] = None

            data["start"] = int(data["start"])
            data["stop"] = int(data["stop"])
            data["strand"] = int(data["strand"])

            if data["copy"] is not None:
                data["copy"] = int(data["copy"])
            if data["part"] is not None:
                data["part"] = int(data["part"])

            data["score"] = float(data["score"])
            if data["bitscore"] is not None:
                data["bitscore"] = float(data["bitscore"])

            if data["anticodon"] is not None:
                data["anticodon"] = trna.codon(data["anticodon"], "anticodon")
            if data["anticodonpos"] == "None":
                data["anticodonpos"] = None
            elif data["anticodonpos"] is not None:
                data["anticodonpos"] = int(data["anticodonpos"])
            self.accession = data["acc"]
            #             type = line[1]
            #             name = line[2]
            #             method = line[3]
            #             start = int(line[4])
            #             stop = int(line[5])
            #             strand = int(line[6])
            #             if line[7] == ".":
            #                 score = None
            #             else:
            #                 score = float(line[7])
            #             if line[8] == "-":
            #                 anticodon = None
            #             else:
            #                 anticodon = line[8]
            #
            #             if len(line) >= 12 and line[11] != ".":
            #                 structure = line[11]
            #             else:
            #                 structure = None

            #             print data
            if data["type"] == "tRNA" or data["type"] == "rRNA":
                nf = mitfifeature(
                    name=data["name"],
                    tpe=data["type"],
                    start=data["start"],
                    stop=data["stop"],
                    strand=data["strand"],
                    score=data["score"],
                    sequence=None,
                    struct=data["struct"],
                    anticodonpos=data["anticodonpos"],
                    anticodon=data["anticodon"],
                    qstart=None,
                    qstop=None,
                    evalue=data["score"],
                    bitscore=data["bitscore"],
                    model=None,
                )
                #                 print nf
                nf.copy = data["copy"]
                nf.part = data["part"]
            else:
                nf = feature(
                    name=data["name"],
                    tpe=data["type"],
                    method=data["method"],
                    start=data["start"],
                    stop=data["stop"],
                    strand=data["strand"],
                    score=data["score"],
                    anticodon=data["anticodon"],
                    copy=data["copy"],
                    part=data["part"],
                )

            #                 nf.part = int(line[9])
            #             if line[10] != ".":
            #                 nf.copy = int(line[10])

            self.features.append(nf)
        mitohandle.close()
