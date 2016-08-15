#!/usr/bin/env python3

import asyncio
import aiohttp

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


async def fetch(session, url):
    with aiohttp.Timeout(60 * 4):
        async with session.get(url) as response:
            return await response.text()


async def fetch_many(urls):
    loop = asyncio.get_event_loop()
    with aiohttp.ClientSession(loop=loop) as session:
        return await asyncio.gather(*[fetch(session, url) for url in urls])


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    urls = [url_fmt.format(i) for i in get_numbers()]
    print('\n'.join(urls))
    pages = loop.run_until_complete(fetch_many(urls))
    for page in pages:
        print('{:>73}'.format(page.split('Status: ')[-1].split('. ')[0]))
