#!/usr/bin/env python3
# coding: utf-8

import os
import time
from pypi_top200_async import main as get_from_pypi
from pypi_read_from_file import main as read_from_file
from pypi_create_index_html import main as create_html

try:
    from http.server import SimpleHTTPRequestHandler as Handler
    from http.server import HTTPServer as Server
except ImportError:
    from SimpleHTTPServer import SimpleHTTPRequestHandler as Handler
    from SocketServer import TCPServer as Server

start = time.time()
MAX_PKGS = 2500
filename = 'pypi_top{}_async.json'.format(MAX_PKGS)

# Read port selected by the cloud for our application
PORT = int(os.getenv('PORT', 8000))
# Change current directory to avoid exposure of control files
# if PORT != 8000:  # if we are on Bluemix
try:
    os.chdir('static_parent_dir')
except FileNotFoundError:
    pass

# =================================

packages = get_from_pypi(MAX_PKGS)
print(time.time() - start, 'seconds')
with open('index.html', 'w') as out_file:
    out_file.write(create_html(read_from_file(filename)))
print(time.time() - start, 'seconds')

# =================================

httpd = Server(("", PORT), Handler)
if PORT == 8000:  # we are running server on localhost
    import webbrowser
    webbrowser.open('localhost:8000')
try:
    print("Start serving at port %i" % PORT)
    httpd.serve_forever()
except KeyboardInterrupt:
    pass
httpd.server_close()
