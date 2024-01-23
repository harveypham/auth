import os
import sys


def _expand_parent_path(current_file):
    curdir, _ = os.path.split(current_file)
    parentdir = os.path.abspath(os.path.dirname(curdir))
    sys.path.insert(0, parentdir)

_expand_parent_path(__file__)
