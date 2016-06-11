#!/usr/bin/env python3
# coding: utf-8

import collections
import json
import os
import time

start = time.time()

FILENAME = 'pypi_top200_async.json'
fields = 'pkg_name downloads py2only py3 release url'
pkg_info = collections.namedtuple('pkg_info', fields)
FMT = '{pkg_name:30}{release:13}{py3}  {py2only}'

# Change current directory to avoid exposure of control files
# if PORT != 8000:  # if we are on Bluemix
try:
    os.chdir('static_parent_dir')
except FileNotFoundError:
    pass

def header():
    fmt = '{:30}{:13}{}'
    return '\n'.join((fmt.format('Module name', 'Latest', 'Python 3?'),
                      fmt.format('=' * 11, '=' * 6, '=' * 9)))


def main(filename=FILENAME):
    with open(filename) as in_file:
        tuples = json.load(in_file)

    assert tuples, 'No data read from {}.'.format(filename)
    print('{} pkg_info records read from {}.'.format(len(tuples), filename))
    return [pkg_info(*x) for x in tuples]


if __name__ == '__main__':
    packages = main()
    print(time.time() - start, 'seconds')

    print(header())
    for package in packages:
        print(FMT.format(**package._asdict()))

    losers = [package for package in packages if not package.py3]
    print('\n{} Python 2 ONLY packages:'.format(len(losers)))
    if losers:
        print(header())
        print('\n'.join(FMT.format(**pkg._asdict()) for pkg in losers))

    print(time.time() - start, 'seconds')
