#!/usr/bin/env python3
# coding: utf-8

import collections
import json
import os
import sys
import time

start = time.time()

MAX_PKGS = 200
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


def main(max_pkgs=MAX_PKGS):
    filename = 'pypi_top{}_async.json'.format(max_pkgs)
    with open(filename) as in_file:
        tuples = json.load(in_file)

    assert tuples, 'No data read from {}.'.format(filename)
    print('{} pkg_info records read from {}.'.format(len(tuples), filename))
    return [pkg_info(*x) for x in tuples]


def write_packages(packages):
    if packages:
        pkg_count = len(packages)
        filename = 'pypi_top{}_async.json'.format(pkg_count)
        with open(filename, 'w') as out_file:
            json.dump(packages, out_file)  # , indent=2)
        print('Info for {} packages written to {}'.format(pkg_count, filename))
    else:
        print('No data was written!!')


if __name__ == '__main__':
    try:
        max_pkgs = int(sys.argv[1])
    except (IndexError, ValueError):
        max_pkgs = MAX_PKGS
    packages = main(max_pkgs)
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
