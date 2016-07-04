#!/usr/bin/env python3
# coding: utf-8

import inspect, platform

print('platform:')
for name, value in inspect.getmembers(platform):
    if name[0] != '_' and callable(value):
        try:
            value = value()
        except (IndexError, TypeError):
            continue
        if str(value).strip("( ,')"):
            print('{:>21}() = {}'.format(name, value))
'''
platform:
architecture() = ('64bit', 'ELF')
dist() = ('debian', 'jessie/sid', '')
libc_ver() = ('glibc', '2.3.4')
linux_distribution() = ('debian', 'jessie/sid', '')
machine() = x86_64
node() = 19i82gna94j
platform() = Linux-3.19.0-25-generic-x86_64-with-debian-jessie-sid
processor() = x86_64
python_build() = ('default', 'Sep 14 2015 18:02:56')
python_compiler() = GCC 4.8.4
python_implementation() = CPython
python_version() = 3.5.0
python_version_tuple() = ('3', '5', '0')
release() = 3.19.0-25-generic
system() = Linux
uname() = uname_result(system='Linux', node='19i82gna94j', release='3.19.0-25-generic', version='#26~14.04.1-Ubuntu SMP Fri Jul 24 21:16:20 UTC 2015', machine='x86_64', processor='x86_64')  # flake8: noqa
version() = #26~14.04.1-Ubuntu SMP Fri Jul 24 21:16:20 UTC 2015
'''
print('sys:')
import sys
print(sys.platform)  # linux
print(sys.version)   # GCC 4.8.4

print('os:')
import os
print(os.path.abspath(os.curdir))  # /home/vcap/app/static
print('')
print(os.listdir(os.curdir))  # index.html, etc.
print('')
print(os.listdir(os.pardir))  # server_old.py, etc.
