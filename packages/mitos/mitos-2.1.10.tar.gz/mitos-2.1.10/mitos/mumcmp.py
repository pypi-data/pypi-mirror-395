import pickle
import string
import sys

from mitos import feature

rsdir = sys.argv[1]
mumfile = sys.argv[2]

print(rsdir)
print(mumfile)

rs = {}

# for f in os.listdir(rsdir):
#     if os.path.isfile(rsdir + "/" + f) and f.endswith(".gb"):
#         x = gb.gbfromfile(rsdir + "/" + f)
#         rs[x.accession] = x.features
#         if len(x.features) == 0:
#             raise Exception(x.accession)
# f = open("/tmp/rs.dump", "w")
# pickle.dump(rs, f)
# f.close()

f = open("/tmp/rs.dump", "r")
rs = pickle.load(f)
f.close()

avglen = 0
i = 0
equal = 0
nequal = 0
f = open(mumfile)
for line in f:
    line = line.strip()
    if line.startswith(">"):
        if line.endswith("Reverse"):
            frstr = -1
        else:
            frstr = 1
        fracc = string.replace(line, ">", "").strip()
        fracc = string.replace(fracc, "Reverse", "").strip()
        fr = rs[fracc]
        if line.endswith("Reverse"):
            frstr = -1
        else:
            frstr = 1
    else:
        line = line.split()
        if len(line) == 1:
            avglen += len(line[0].strip())
            continue

        toacc = line[0]
        if fracc == toacc:
            continue

        to = rs[toacc]
        tostart = int(line[2]) - 1
        toend = int(line[2]) - 1 + int(line[3])
        to.sort(key=lambda x: (feature.cap(x.start, x.stop, tostart, toend, False, 0)))

        frstart = int(line[1]) - 1
        frend = int(line[1]) - 1 + int(line[3])
        fr.sort(key=lambda x: (feature.cap(x.start, x.stop, frstart, frend, False, 0)))

        if feature.cap(to[-1].start, to[-1].stop, tostart, toend, False, 0) == 0:
            toname = "NA"
        else:
            toname = to[-1].name

        if feature.cap(fr[-1].start, fr[-1].stop, frstart, frend, False, 0) == 0:
            frname = "NA"
        else:
            frname = fr[-1].name

        if frname == toname:
            equal += 1
        else:
            nequal += 1
    i += 1
    if i % 100000 == 0:
        print((i, equal, nequal, avglen / float(i)))

print((equal, nequal, avglen / float(i)))

f.close()
