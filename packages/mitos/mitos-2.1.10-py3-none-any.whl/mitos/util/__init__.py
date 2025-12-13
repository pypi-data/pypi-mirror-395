import logging
from subprocess import PIPE, Popen
from typing import List, Tuple


def execute(
    cmd: List[str], supress_warning=False, exception=Exception
) -> Tuple[str, str]:
    exception = exception or Exception
    executable = cmd[0]
    cmd_str = " ".join(cmd)
    logging.debug(cmd_str)
    proc = Popen(cmd, stdout=PIPE, stderr=PIPE)
    out, err = proc.communicate()
    if proc.returncode:
        logging.error(f"{cmd_str} had exit code {proc.returncode}\n{err}")
        raise exception(err)
    elif len(err) > 0 and not supress_warning:
        logging.warning(f"{executable} wrote to stderr: {err}")
    return out, err
