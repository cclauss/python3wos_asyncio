#!/usr/bin/env python3

import datetime
import requests

filename = 'status/Status_{:%Y_%m_%d}.txt'.format(datetime.date.today())
url_fmt = 'http://python3wos.mybluemix.net/{}'


def get_numbers(max=80000):
    incr = 100
    i = 200
    while i <= max:
        yield i
        if i == 1000:
            incr *= 5
        elif i == 10000:
            incr *= 10
        i += incr


with open(filename, 'w') as out_file:
    for i in get_numbers():
        html = requests.get(url_fmt.format(i)).text
        text = '{:>73}'.format(html.split('Status: ')[-1].split('. ')[0])
        out_file.write(text + '\n')
        print(text)
