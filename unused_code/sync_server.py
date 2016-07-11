#!/usr/bin/env python3
# coding: utf-8

import multiprocessing
import os
import sys
import time

from pypi_top_packages_async import get_from_pypi

from http.server import SimpleHTTPRequestHandler as Handler
from http.server import HTTPServer as Server

start = time.time()
MAX_PKGS = 200

# Read port selected by the cloud for our application
PORT = int(os.getenv('PORT', 8000))
# Change current directory to avoid exposure of control files
try:
    os.chdir('static_parent_dir')
except FileNotFoundError:
    pass


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

# while the main process runs a webserver
httpd = Server(("", PORT), Handler)
if PORT == 8000:  # we are running the server on localhost
    import webbrowser
    webbrowser.open('localhost:8000')
try:
    print("Start serving at port %i" % PORT)
    httpd.serve_forever()
except KeyboardInterrupt:
    pass
httpd.server_close()
