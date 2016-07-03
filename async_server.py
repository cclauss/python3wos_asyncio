#!/usr/bin/env python3
# coding: utf-8

import asyncio
from aiohttp import web
import aiohttp_jinja2
import jinja2
import webbrowser
# import multiprocessing
import os
# import sys
import time

from pypi_top_packages_async import get_from_pypi
from pypi_create_index_html import enhance_packages, build_template_values

# from http.server import SimpleHTTPRequestHandler as Handler
# from http.server import HTTPServer as Server

start = time.time()
MAX_PKGS = 200

# Read port selected by the cloud for our application
PORT = int(os.getenv('PORT', 8000))
# Change current directory to avoid exposure of control files
try:
    os.chdir('static_parent_dir')
except FileNotFoundError:
    pass

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
# while the main process runs a webserver
# httpd = Server(("", PORT), Handler)
# if PORT == 8000:  # we are running the server on localhost
#    import webbrowser
#    webbrowser.open('localhost:8000')
# try:
#    print("Start serving at port %i" % PORT)
#    httpd.serve_forever()
# except KeyboardInterrupt:
#    pass
# httpd.server_close()


def launch_browser(host_and_port='localhost:8081'):
    asyncio.sleep(0.1)  # give the server a second to come up
    webbrowser.open(host_and_port)


async def index_handler(request):
    '''
    try:
        with open('index.html') as in_file:
            return web.Response(text=in_file.read())
    except FileNotFoundError:
        return web.Response(text='Processing: Please refresh this page')
    '''
    # print(request)
    # print(dir(request))
    return web.Response(body=b'Hello, world')


async def other_handler(request):
    value = request.match_info.get('value', 'Anonymous')
    txt = "Hello, {}".format(value)
    return web.Response(text=txt)

d = get_from_pypi(200)
print('On your mark...')
# print(str(d)[:100])
d = enhance_packages(d)
print('Get set...')
d = build_template_values(d)
print('Go!')


@aiohttp_jinja2.template('index_db.html')
async def handler(request):
    return d  # get_from_pypi(200)
    # return await get_packages_info(200)


def run_webserver(port=8080):
    app = web.Application()
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(os.curdir))
    app.router.add_route('GET', '/', index_handler)
    app.router.add_route('GET', '/{value}', handler)
    web.run_app(app, port=port)


if True:  # PORT == 8000:  # we are running the server on localhost
    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, launch_browser, 'localhost:{}'.format(PORT))
run_webserver(port=PORT)
