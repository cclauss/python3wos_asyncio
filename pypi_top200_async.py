#!/usr/bin/env python3
# coding: utf-8

import asyncio
import collections
import json
import time
from xmlrpc.client import ServerProxy

MAX_PKGS = 200  # or try 1000
PYPI_URL = 'https://pypi.python.org/pypi'

fields = 'pkg_name downloads py2only py3 release url'
pkg_info = collections.namedtuple('pkg_info', fields)
FMT = '{pkg_name:30}{release:13}{py3}  {py2only}'
py2_only_classifier = 'Programming Language :: Python :: 2 only'
py3_classifier = 'Programming Language :: Python :: 3'


def header():
    fmt = '{:30}{:13}{}'
    return '\n'.join((fmt.format('Module name', 'Latest', 'Python 3?'),
                      fmt.format('=' * 11, '=' * 6, '=' * 9)))


def get_pkg_info(pkg_name, downloads=0):
    # multiple asyncio jobs can not share a client
    client = ServerProxy(PYPI_URL)
    try:
        release = client.package_releases(pkg_name)[0]
    except IndexError:  # marionette-transport, ll-orasql, and similar
        print(pkg_name, 'has no releases in PyPI!!')
        return pkg_info(pkg_name, 'PyPI error!!', False, False, '', '')
    troves = '\n'.join(client.release_data(pkg_name, release)['classifiers'])
    py2only = py2_only_classifier in troves
    py3 = py3_classifier in troves
    url = client.release_data(pkg_name, release)['package_url']
    return pkg_info(pkg_name, downloads, py2only, py3, release, url)


@asyncio.coroutine
def async_main(max_pkgs=MAX_PKGS):  # ~ 32 secs for 200 pkgs on my MacBookPro
    loop = asyncio.get_event_loop()
    client = ServerProxy(PYPI_URL)
    futures = [loop.run_in_executor(None, get_pkg_info, pkg_name, downloads)
               for pkg_name, downloads in client.top_packages(max_pkgs)]
    return [(yield from fut) for fut in futures]


def main(max_pkgs=MAX_PKGS):
    fmt = 'Gathering Python 3 support info on the top {} PyPI packages...'
    print(fmt.format(max_pkgs))
    start = time.time()
    loop = asyncio.get_event_loop()
    packages = loop.run_until_complete(async_main(max_pkgs))
    print(time.time() - start, 'seconds')  # ~ 32 sec if asyncio else ~ 105 sec
    filename = 'pypi_top{}_async.json'.format(max_pkgs)
    if packages:
        with open(filename, 'w') as out_file:
            json.dump(packages, out_file)  # , indent=2)
        print('Info for {} packages written to {}'.format(len(packages),
                                                          filename))
    else:
        print('No data was written!!')
    return packages

if __name__ == '__main__':
    packages = main(MAX_PKGS)
    print(header())
    for package in packages:
        # print(FMT.format(**package_info._asdict()))
        # print(package._asdict())
        print(tuple(package))

    losers = [package for package in packages if not package.py3]
    print('\n{} Python 2 ONLY packages:'.format(len(losers)))
    if losers:
        print(header())
        print('\n'.join(FMT.format(**package._asdict()) for package in losers))

    # print(time.time() - start, 'seconds')
