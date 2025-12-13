"""
@author: M. Bernt
"""

import os
import shlex
import shutil
import subprocess
import tempfile

from mitos import extprog


def RNAplot(sequence, structure, fname, **keywords):
    """
    RNAplot [-t 0|1] [-o ps|gml|xrna|svg]
    """
    # todo parameters [--pre string] [--post string]

    plotpar = [
        extprog.shortparm("t", "int", [0, 1]),
        extprog.shortparm("o", "str", ["ps", "gml", "xrna", "svg"]),
    ]
    cl = extprog.cmdline(keywords, plotpar)
    if cl.get("o") is not None:
        ext = cl.get("o")
    else:
        ext = "ps"
    cmd = ["RNAplot"] + shlex.split(str(cl))

    with tempfile.TemporaryDirectory() as tmpdir:
        p = subprocess.Popen(
            cmd,
            cwd=tmpdir,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            close_fds=True,
            universal_newlines=True,
        )
        p.stdin.write(sequence + "\n")
        p.stdin.write(structure + "\n")
        p.stdin.write("@\n")
        p.stdin.close()
        p.wait()

        if os.path.exists(f"{tmpdir}/rna.{ext}"):
            shutil.move(f"{tmpdir}/rna.{ext}", fname)
        else:
            print("warning: RNAplot did not produced a %s file" % (ext))
            for line in p.stderr.readlines():
                print("stderr", line.strip())
            for line in p.stdout.readlines():
                print("stdout", line.strip())
    return
