# -*- coding: utf-8 -*-
#
# Copyright (c) 2015 Eduardo Klosowski
# License: MIT (see LICENSE for details)
#

from __future__ import unicode_literals

from hashlib import sha1
import os


# Global Vars

CACHE_DIR = os.path.join(os.path.expanduser('~'), '.deduplicated')


# Utils

def sha1_file(filename):
    with open(filename, 'rb') as fp:
        s = sha1()
        block = True
        while block:
            block = fp.read(2 ** 10)
            s.update(block)
        return s.hexdigest()


def str_size(size):
    if size < 2 ** 10:
        return '%d B' % size
    if size < 2 ** 20:
        return '%.2f KB' % (size / (2 ** 10))
    if size < 2 ** 30:
        return '%.2f MB' % (size / (2 ** 20))
    if size < 2 ** 40:
        return '%.2f GB' % (size / (2 ** 30))
    return '%.2f TB' % (size / (2 ** 40))


# Directory

class Directory(object):
    def __init__(self, path):
        path = os.path.abspath(path)
        if not os.path.isdir(path):
            raise IOError('%s is not valid directory' % path)

        self._path = path
        self._hashfile = os.path.join(
            CACHE_DIR,
            self.get_hash(),
        )

    def __str__(self):
        return self._path

    def get_hash(self):
        return sha1(self._path.encode('utf-8')).hexdigest()


# Create user directory if not exists

if not os.path.exists(CACHE_DIR):
    os.mkdir(CACHE_DIR)