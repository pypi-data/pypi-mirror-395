# SPDX-License-Identifier: LGPL-2.1-or-later

""" Various tools """

import subprocess
import sys

# pylint: disable=redefined-builtin
def run_command(cmdargs, sysexit=False, canfail=False, input=None, text=True):
    """ Run a command """

    res = subprocess.run(cmdargs, check=False, capture_output=True, text=text, input=input)
    if res.returncode != 0 and not canfail:
        print(f"{res.args} returned {res.returncode}, stdout: {res.stdout} stderr: {res.stderr}", file=sys.stderr)
        if sysexit:
            sys.exit(1)
        else:
            raise RuntimeError(f"{cmdargs[0]} command failed")
    return res
