#!/usr/bin/env python3
# coding: utf-8

import os
import time
# from pypi_top200_async import main as get_from_pypi
from pypi_read_from_file import main as read_from_file
from pypi_create_index_html import main as create_html

try:
    from http.server import SimpleHTTPRequestHandler as Handler
    from http.server import HTTPServer as Server
except ImportError:
    from SimpleHTTPServer import SimpleHTTPRequestHandler as Handler
    from SocketServer import TCPServer as Server

start = time.time()

# Read port selected by the cloud for our application
PORT = int(os.getenv('PORT', 8000))
# Change current directory to avoid exposure of control files
# if PORT != 8000:  # if we are on Bluemix
os.chdir('static')

# =================================

# packages = get_from_pypi(1000)
# print(start - time.time(), 'seconds')
with open('index.html', 'w') as out_file:
    out_file.write(create_html(read_from_file('pypi_top200_async.json')))
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
