
from importlib.resources import files, as_file
from platform import system
import subprocess
import sys
from typing import Iterable, Optional


def main(args: Optional[Iterable[str]] = None):
    if args is None:
        args = sys.argv[1:]
    with as_file(files("cmconfig") / 'bin') as bin:
        exe = str(bin / system().lower() / 'cmconfig')
        raise SystemExit(subprocess.call([exe, *args], close_fds=False))
