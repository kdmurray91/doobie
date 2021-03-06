#!/usr/bin/env python

# Copyright 2014 Kevin Murray
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import print_function
import hashlib
import os
import sys

# versioneer version import
from ._version import get_versions
__version__ = get_versions()['version']
del get_versions


def human_size(num, exp=1024.0):
    exp = float(exp)
    for x in ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB']:
        if num < exp:
            return "{:3.1f}{}".format(num, x)
        num /= exp
    return "{:3.1f}{}".format(num, 'YB')


class Doobie(object):
    """Doobie: Hash in a pipe
    """
    hasher = None

    def __init__(self, verbosity=0):
        self.verbosity = verbosity

    def hash(self, input_fh=sys.stdin, output_fh=sys.stderr):
        # Never print messages to a file
        if not os.isatty(sys.stderr.fileno()):
            self.verbosity = 0
        # if we're supposed to print to stderr, don't print verbose stuff
        if output_fh is sys.stderr:
            self.verbosity = 0
        hasher_inst = self.hasher()
        bytes_proc = 0
        buf = input_fh.read(1024)
        while len(buf) > 0:
            bytes_proc += 1024
            hasher_inst.update(buf)
            # emit buffer again on stderr
            sys.stdout.write(buf)
            sys.stdout.flush()
            if self.verbosity > 0:
                if bytes_proc % (1024 * 1024) == 0:
                    print("Processed", human_size(bytes_proc).rjust(8),
                          end='\r', file=sys.stderr)
            buf = input_fh.read(1024)
        if self.verbosity > 0:
            print(file=sys.stderr)
        output_fh.write(hasher_inst.hexdigest())
        input_fh.close()
        output_fh.close()


class DoobieMD5(Doobie):
    hasher = hashlib.md5


class DoobieSHA1(Doobie):
    hasher = hashlib.sha1


class DoobieSHA224(Doobie):
    hasher = hashlib.sha224


class DoobieSHA256(Doobie):
    hasher = hashlib.sha256


class DoobieSHA384(Doobie):
    hasher = hashlib.sha384


class DoobieSHA512(Doobie):
    hasher = hashlib.sha512


HASH_CLASS_MAP = {
    "md5": DoobieMD5,
    "sha1": DoobieSHA1,
    "sha224": DoobieSHA224,
    "sha256": DoobieSHA256,
    "sha384": DoobieSHA384,
    "sha512": DoobieSHA512,
}
