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

import pypi_create_index_html  # noqa
from pypi_top_packages_async import get_packages_info
from pypi_create_index_html import build_template_values

f'Python 3.6 or better is required'  # f-string will be a syntax error pre-3.6
START_TIME = time.time()
MAX_PKGS = 500  # User can override this by entering a value on the commandline
PORT = int(os.getenv('PORT', 8000))  # Cloud will provide a web server PORT id

try:  # Immediately change current directory to avoid exposure of control files
    os.chdir('static_parent_dir')
except FileNotFoundError:
    pass

try:  # See if the user entered a maximum packages number on the commandline
    max_pkgs = int(sys.argv[1])
except (IndexError, ValueError):
    max_pkgs = MAX_PKGS

app = web.Application()


def done_callback(fut, app=None):  # Called when PyPI data capture is complete
    app = app or {}
    elapsed = time.time() - START_TIME
    app['packages'], app['data_datetime'] = fut.result()
    fmt = ' Gathered Python 3 support info on {:,} PyPI packages in {:.2f} seconds.'
    print(fmt.format(len(app['packages']), elapsed))


fut = asyncio.run_coroutine_threadsafe(get_packages_info(max_pkgs, START_TIME),
                                       asyncio.get_event_loop())
fut.add_done_callback(functools.partial(done_callback, app=app))


async def index_handler(request):
    # try:  # return index.html if it exists
    #    with open('index.html') as in_file:
    #        return web.Response(text=in_file.read())
    # except FileNotFoundError:
    return web.Response(text='Processing: Please wait a few seconds and then refresh this page')


@aiohttp_jinja2.template('index_db.html')
async def handler(request):
    packages = request.app.get('packages')
    if not packages:  # if data capture still ongoing, default to index.html
        return await index_handler(request)
    print('len(packages): {}'.format(len(packages)))
    max_pkgs = request.match_info.get('max_pkgs', '').split('.')[0]
    max_pkgs = ''.join(c for c in max_pkgs if c.isdigit())
    max_pkgs = max(int(max_pkgs) if max_pkgs else 0, 500)
    return build_template_values(packages[:max_pkgs],
                                 request.app.get('data_datetime'))


def run_webserver(app, port=PORT):
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(os.curdir))
    app.router.add_route('GET', '/', handler)
    app.router.add_route('GET', '/{max_pkgs}', handler)
    app.router.add_static('/static/', path='./static')
    web.run_app(app, port=PORT)


async def launch_browser(port=PORT):
    asyncio.sleep(0.2)  # give the server a fifth of a second to come up
    webbrowser.open('localhost:{}'.format(port))


if PORT == 8000:  # we are running the server on localhost
    asyncio.run_coroutine_threadsafe(launch_browser(PORT), app.loop)

run_webserver(app, port=PORT)
