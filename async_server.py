#!/usr/bin/env python3
# coding: utf-8

from aiohttp import web
import aiohttp_jinja2
import asyncio
import functools
import jinja2
import os
import sys
import time
import webbrowser

from pypi_top_packages_async import get_from_pypi
from pypi_top_packages_async import get_packages_info

# from pypi_create_index_html import enhance_packages
from pypi_create_index_html import build_template_values

START_TIME = time.time()
MAX_PKGS = 200  # user can override this by entering a value on the commandline
PORT = int(os.getenv('PORT', 8000))  # Cloud will provide PORT id

# Immediately change current directory to avoid exposure of control files
try:
    os.chdir('static_parent_dir')
except FileNotFoundError:
    pass

try:  # Did the user enter a number on the commandline?
    max_pkgs = int(sys.argv[1])
except (IndexError, ValueError):
    max_pkgs = MAX_PKGS

app = web.Application()
'''
app['data_datetime'] = None  # set in get_from_pypi
app['max_pkgs'] = max_pkgs   # read in get_from_pypi
app['packages'] = None       # set in get_from_pypi
# app['port'] = PORT = int(os.getenv('PORT', 8000))  # Cloud will provide PORT
app['start'] = START_TIME    # read in get_from_pypi
'''

'''
def get_from_pyp(app, max_pkgs, START_TIME):
    for i in range(15):
        app['packages'] = (i + 1) * 200
        app['data_datetime'] = time.time()
        print('{packages}, {data_datetime}'.format(**app))
        # print(app.__dict__)
        # print(app._asdict())
        # asyncio.sleep(1)
    return max_pkgs, START_TIME
'''


def done_callback(fut, app=None):
    print('done_callback:', time.time() - START_TIME)
    app = app or {}
    app['packages'], app['data_datetime'] = fut.result()

# fut = app.loop.run_in_executor(None, get_from_pypi, app.loop, max_pkgs, START_TIME)
fut = asyncio.run_coroutine_threadsafe(get_packages_info(max_pkgs, START_TIME),
                                       app.loop)
fut.add_done_callback(functools.partial(done_callback, app=app))

# Read port selected by the cloud for our application
# PORT = int(os.getenv('PORT', 8000))

'''
def create_html_from_pypi(max_pkgs=MAX_PKGS):
    p = multiprocessing.current_process()
    print('Starting process:', p.name, p.pid)
    sys.stdout.flush()

    try:
        max_pkgs = int(sys.argv[1])
    except (IndexError, ValueError):
        max_pkgs = MAX_PKGS
    print(max_pkgs)
    packages = get_from_pypi(max_pkgs)
    print(time.time() - start, 'seconds,', len(packages), 'packages.')
    # with open('index.html', 'w') as out_file:
    #     out_file.write(create_html(packages))  # read_packages(max_pkgs)))
    print(time.time() - start, 'seconds')

    print('Exiting :', p.name, p.pid)
    sys.stdout.flush()
    return 42


# start a separate process to gather data from PyPI in the background
multiprocessing.Process(name='PyPI Scan', target=create_html_from_pypi).start()
'''


async def index_handler(request):
    try:  # return index.html if it exists
        with open('index.html') as in_file:
            return web.Response(body=in_file.read().encode())
    except FileNotFoundError:
        return web.Response(text='Processing: Please refresh this page')


@aiohttp_jinja2.template('index_db.html')
async def handler(request):
    packages = request.app.get('packages', None)
    if not packages:  # if data capture still ongoing, default to index.html
        return await index_handler(request)
    max_pkgs = request.match_info.get('max_pkgs', '').split('.')[0]
    max_pkgs = ''.join(c for c in max_pkgs if c.isdigit())
    max_pkgs = max(int(max_pkgs) if max_pkgs else 0, 200)
    return build_template_values(packages[:max_pkgs],
                                 request.app.get('data_datetime'))


def run_webserver(app, port=PORT):
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(os.curdir))
    app.router.add_route('GET', '/', index_handler)
    app.router.add_route('GET', '/{max_pkgs}', handler)
    app.router.add_static('/static/', path='./static', name='static')
    web.run_app(app, port=PORT)


def launch_browser(port=PORT):
    asyncio.sleep(0.1)  # give the server a tenth of a second to come up
    webbrowser.open('localhost:{}'.format(port))


if PORT == 8000:  # we are running the server on localhost
    app.loop.run_in_executor(None, launch_browser, PORT)
run_webserver(app, port=PORT)
