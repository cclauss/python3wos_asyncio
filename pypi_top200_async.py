#!/usr/bin/env python3
# coding: utf-8

import aiohttp
import asyncio
import collections
import json
import time
from xmlrpc.client import ServerProxy

MAX_PKGS = 5000  # or try 1000
PYPI_URL = 'https://pypi.python.org/pypi'
PYPI_FMT = 'https://pypi.python.org/pypi/{}/json'

fields = 'pkg_name downloads py2only py3 release url'
pkg_info = collections.namedtuple('pkg_info', fields)
FMT = '{pkg_name:30}{release:13}{py3}  {py2only}'
py2_only_classifier = 'Programming Language :: Python :: 2 only'
py3_classifier = 'Programming Language :: Python :: 3'


def header():
    fmt = '{:30}{:13}{}'
    return '\n'.join((fmt.format('Module name', 'Latest', 'Python 3?'),
                      fmt.format('=' * 11, '=' * 6, '=' * 9)))


'''
def get_pkg_info(pkg_name, downloads=0):
    # multiple asyncio jobs can not share a client
    client = ServerProxy(PYPI_URL)
    try:
        release = client.package_releases(pkg_name)[0]
    except IndexError:  # marionette-transport, ll-orasql, and similar
        print(pkg_name, 'has no releases in PyPI!!')
        return pkg_info(pkg_name, downloads, False, False, 'PyPI error!!', '')
    troves = '\n'.join(client.release_data(pkg_name, release)['classifiers'])
    py2only = py2_only_classifier in troves
    py3 = py3_classifier in troves
    url = client.release_data(pkg_name, release)['package_url']
    return pkg_info(pkg_name, downloads, py2only, py3, release, url)
'''

async def fetch_json(session, url):
    with aiohttp.Timeout(10):
        async with session.get(url) as response:
            assert response.status == 200
            return await response.json()

async def get_package_info(session, pkg_name, downloads):
    d = await fetch_json(session, PYPI_FMT.format(pkg_name))
    info = d['info']
    classifiers = '\n'.join(info['classifiers'])
    py2only = py2_only_classifier in classifiers
    py3 = py3_classifier in classifiers
    release = info['version']
    url = info['package_url']
    return pkg_info(pkg_name, downloads, py2only, py3, release, url)

'''
@asyncio.coroutine
def async_main(max_pkgs=MAX_PKGS):  # ~ 32 secs for 200 pkgs on my MacBookPro
    loop = asyncio.get_event_loop()
    client = ServerProxy(PYPI_URL)
    futures = [loop.run_in_executor(None, get_pkg_info, pkg_name, downloads)
               for pkg_name, downloads in client.top_packages(max_pkgs)]
    return [(yield from fut) for fut in futures]


async def get_packages_info(max_pkgs=MAX_PKGS):  # ~ 32 secs for 200 pkgs on my MacBookPro
    loop = asyncio.get_event_loop()
    client = ServerProxy(PYPI_URL)
    with aiohttp.ClientSession(loop=loop) as session:
        futures = [get_pkg_info_II(session, pkg_name, downloads)
                   for pkg_name, downloads in client.top_packages(max_pkgs)]
    return await [fut() for fut in futures]
'''

# async def get_packages_names_and_downloads(max_pkgs=MAX_PKGS):
#     return ServerProxy(PYPI_URL).top_packages(max_pkgs)


def create_tasks(session, max_pkgs=MAX_PKGS):
    client = ServerProxy(PYPI_URL)
    return [get_package_info(session, pkg_name, downloads)
            for pkg_name, downloads in client.top_packages(max_pkgs)]

async def main(max_pkgs=MAX_PKGS):
    fmt = 'Gathering Python 3 support info on the top {} PyPI packages...'
    print(fmt.format(max_pkgs))
    packages = []
    with aiohttp.ClientSession() as session:
        tasks = create_tasks(session, max_pkgs)
        while tasks:
            current_block, tasks = tasks[:200], tasks[200:]
            packages += await asyncio.gather(*current_block)
            if len(packages) == 200:
                from pypi_create_index_html import main as create_index
                with open('index.html', 'w') as out_file:
                    out_file.write(create_index(packages))
            filename = 'index_{:0>4}.html'.format(len(packages))
            with open(filename, 'w') as out_file:
                out_file.write(create_index(packages))
            print('.')
    return packages

#    packages_info = []
    '''
    results = []
    tasks = ServerProxy(PYPI_URL).top_packages(max_pkgs)
    while names_and_downloads:
        current_block = names_and_downloads[:200]
        names_and_downloads = names_and_downloads[200:]
        # results +=

    with aiohttp.ClientSession() as session:
        # print(await fetch_json(session, 'https://pypi.python.org/pypi/aiohttp/json'))
        # pkg_name = 'aiohttp'
        # print(await get_pkg_info_II(session, pkg_name, downloads=0))
        # client = ServerProxy(PYPI_URL)
        return await asyncio.gather(*create_tasks(session, max_pkgs))
#        for pkg_name, downloads in client.top_packages(max_pkgs):
#            packages_info.append(await get_pkg_info_II(session, pkg_name,
#                                                       downloads))
#    return packages_info

    loop = asyncio.get_event_loop()
    with aiohttp.ClientSession(loop=loop) as session:
        print(loop.run_until_complete(get_packages_info(max_pkgs=MAX_PKGS)))
    return

    '-''
    loop = asyncio.get_event_loop()
    with aiohttp.ClientSession(loop=loop) as session:
        d = [(yield from get_pkg_info_II(session, 'aiohttp', 0)) for mod in 'pip requests aiohttp'.split()]
        ## d = loop.run_until_complete(get_pkg_info_II(session, 'aiohttp', 0))
        #    fetch_json(session, 'https://pypi.python.org/pypi/aiohttp/json'))
    import pprint
    # pprint.pprint(d)
    for x in d:
        pprint.pprint(x)
    exit()
    '-''

    start = time.time()
    loop = asyncio.get_event_loop()
    packages = loop.run_until_complete(async_main_II(10))  # max_pkgs))
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
   '''

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
    start = time.time()
    packages = asyncio.get_event_loop().run_until_complete(main(MAX_PKGS))
    print(time.time() - start, 'seconds')  # ~ 32 sec if asyncio else ~ 105 sec
    write_packages(packages)
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
