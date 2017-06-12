#!/usr/bin/env python3
# coding: utf-8

import collections
import datetime
import json
import os
import time

from jinja2 import Environment, FileSystemLoader

start = time.time()

try:
    os.chdir('static_parent_dir')
except FileNotFoundError:
    pass

with open('equivalent_modules.json') as in_file:
    EQUIVALENTS = json.load(in_file)
print('> {}'.format(len(EQUIVALENTS)))

# fields = 'pkg_name downloads version py2only py3'
flds = ('pkg_name downloads equivalent_url has_py3_fork py2only py3 '
        'py3_percentage release url')
pkg_info = collections.namedtuple('pkg_info', flds)


def enhance_packages(packages):
    print('< {}'.format(len(EQUIVALENTS)))
    print('pyrax:', 'pyrax' in EQUIVALENTS)
    py3_total = 0

    def enhance_package(i, package):
        nonlocal py3_total
        downloads = '{:,}'.format(package.downloads)  # add commas
        equivalent_url = EQUIVALENTS.get(package.pkg_name, '')
        has_py3_fork = equivalent_url.startswith('https://pypi.')
        if package.py3 or equivalent_url:
            py3_total += 1
        py3_percentage = '{:.2%}'.format(py3_total / (i + 1))
        return pkg_info(package.pkg_name, downloads, equivalent_url,
                        has_py3_fork, package.py2only, package.py3,
                        py3_percentage, package.release, package.url)
    return [enhance_package(i, package) for i, package in enumerate(packages)]

    # url = client.release_data(pkg_name, release)['package_url']


# def build_html(packages):
#    html = '''<table><tr><th>Package</th><th>Downloads</th></tr>%s</table>'''
#    row = ('<tr class="py3{py3}"><td><a href="{url}" timestamp="{timestamp}">'
#           '{pkg_name}</a></td><td>{downloads:,}</td></tr>')
#    return html % '\n'.join(row.format(**pkg._asdict()) for pkg in packages)


# def count_py3_packages(packages):
#    return len([pkg for pkg in packages if pkg.py3 or pkg.equivalent_url])


# =====

def build_template_values(packages, data_datetime=None):
    data_datetime = data_datetime or datetime.datetime.utcnow()
    total = len(packages)
    py3_count = len([pkg for pkg in packages if pkg.py3 or pkg.equivalent_url])
    py3_percent = py3_count / total if total else 0
    return {'title': 'Python 3 Wall of ' + ('Shame' if py3_percent < 0.5 else
                                            'Superpowers'),
            'py3_days': '{:,}'.format((datetime.date.today() -
                                       datetime.date(2008, 12, 3)).days),
            'packages': packages,  # [pkg._asdict() for pkg in packages],
            'count': '{}/{} or {:.2%}'.format(py3_count, total, py3_percent),
            'min_time': '{:%Y-%m-%d %H:%M} UTC'.format(data_datetime)}


def get_html(packages):  # uncomment the next line to see the Wall of Shame!
    # packages=[pkg for pkg in packages if not (pkg.py3 or pkg.equivalent_url)]
    env = Environment(loader=FileSystemLoader(os.curdir))
    template = env.get_template('index_db.html')
    return template.render(build_template_values(packages))


def main(packages):
    assert packages, 'No packages!!  {}.'.format(packages)
    return get_html(enhance_packages(packages))


if __name__ == '__main__':
    from pypi_io_utils import read_packages
    html = main(read_packages(5000))
    print(html)
    print(time.time() - start, 'seconds')
    with open('index.html', 'w') as out_file:
        out_file.write(html)
    print(time.time() - start, 'seconds')
