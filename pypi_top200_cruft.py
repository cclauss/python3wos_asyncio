'''
def get_pkg_info(pkg_name, downloads=0):
    # multiple asyncio jobs can not share a client
    client = ServerProxy(PYPI_URL)
    try:
        release = client.package_releases(pkg_name)[0]
    except IndexError:  # marionette-transport, ll-orasql, and similar
        print(pkg_name, 'has no releases in PyPI!!')
        return pkg_info(pkg_name, downloads, False, False, 'PyPI error!!', '')
    troves = '\n'.join(client.release_data(pkg_name, release)['classifiers'])
    py2only = py2_only_classifier in troves
    py3 = py3_classifier in troves
    url = client.release_data(pkg_name, release)['package_url']
    return pkg_info(pkg_name, downloads, py2only, py3, release, url)

@asyncio.coroutine
def async_main(max_pkgs=MAX_PKGS):  # ~ 32 secs for 200 pkgs on my MacBookPro
    loop = asyncio.get_event_loop()
    client = ServerProxy(PYPI_URL)
    futures = [loop.run_in_executor(None, get_pkg_info, pkg_name, downloads)
               for pkg_name, downloads in client.top_packages(max_pkgs)]
    return [(yield from fut) for fut in futures]


async def get_packages_info(max_pkgs=MAX_PKGS):  # ~ 32 secs for 200 pkgs on my MacBookPro
    loop = asyncio.get_event_loop()
    client = ServerProxy(PYPI_URL)
    with aiohttp.ClientSession(loop=loop) as session:
        futures = [get_pkg_info_II(session, pkg_name, downloads)
                   for pkg_name, downloads in client.top_packages(max_pkgs)]
    return await [fut() for fut in futures]
'''

# async def get_packages_names_and_downloads(max_pkgs=MAX_PKGS):
#     return ServerProxy(PYPI_URL).top_packages(max_pkgs)

packages_info = []
  '''
  results = []
  tasks = ServerProxy(PYPI_URL).top_packages(max_pkgs)
  while names_and_downloads:
      current_block = names_and_downloads[:200]
      names_and_downloads = names_and_downloads[200:]
      # results +=

  with aiohttp.ClientSession() as session:
      # print(await fetch_json(session, 'https://pypi.python.org/pypi/aiohttp/json'))
      # pkg_name = 'aiohttp'
      # print(await get_pkg_info_II(session, pkg_name, downloads=0))
      # client = ServerProxy(PYPI_URL)
      return await asyncio.gather(*create_tasks(session, max_pkgs))
#        for pkg_name, downloads in client.top_packages(max_pkgs):
#            packages_info.append(await get_pkg_info_II(session, pkg_name,
#                                                       downloads))
#    return packages_info

  loop = asyncio.get_event_loop()
  with aiohttp.ClientSession(loop=loop) as session:
      print(loop.run_until_complete(get_packages_info(max_pkgs=MAX_PKGS)))
  return

  '-''
  loop = asyncio.get_event_loop()
  with aiohttp.ClientSession(loop=loop) as session:
      d = [(yield from get_pkg_info_II(session, 'aiohttp', 0)) for mod in 'pip requests aiohttp'.split()]
      ## d = loop.run_until_complete(get_pkg_info_II(session, 'aiohttp', 0))
      #    fetch_json(session, 'https://pypi.python.org/pypi/aiohttp/json'))
  import pprint
  # pprint.pprint(d)
  for x in d:
      pprint.pprint(x)
  exit()
  '-''

  start = time.time()
  loop = asyncio.get_event_loop()
  packages = loop.run_until_complete(async_main_II(10))  # max_pkgs))
  print(time.time() - start, 'seconds')  # ~ 32 sec if asyncio else ~ 105 sec
  filename = 'pypi_top{}_async.json'.format(max_pkgs)
  if packages:
      with open(filename, 'w') as out_file:
          json.dump(packages, out_file)  # , indent=2)
      print('Info for {} packages written to {}'.format(len(packages),
                                                        filename))
  else:
      print('No data was written!!')
  return packages
 '''
