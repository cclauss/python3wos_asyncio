#!/usr/bin/env python

with open('pypi_top200_async.json') as in_file:
    print(in_file.read().replace('], ', '],\n'))
