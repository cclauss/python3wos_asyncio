# python3wos_asyncio

The code in this repo should be running at: http://python3wos.mybluemix.net

This is Python 3 version of https://github.com/ubershmekel/python3wos which adds `asyncio` in order to gather the Python 3 support data on the top 200 packages on PyPI.  Asyncio lowers that data gathering time to gather data on 5000 PyPI packages to about 25 seconds on Bluemix.

Static webpages are also generated just to get a sense of how Python 3 compatibility drops on larger slices:
* [Top 200](http://python3wos.mybluemix.net/index_0200.html),
[Top 400](http://python3wos.mybluemix.net/index_0400.html),
[Top 600](http://python3wos.mybluemix.net/index_0600.html),
[Top 800](http://python3wos.mybluemix.net/index_0800.html)
* [Top 1000](http://python3wos.mybluemix.net/index_1000.html),
[Top 1000](http://python3wos.mybluemix.net/index_1000.html),
[Top 1000](http://python3wos.mybluemix.net/index_1000.html),
[Top 1000](http://python3wos.mybluemix.net/index_1000.html),
[Top 1000](http://python3wos.mybluemix.net/index_1000.html), 
* http://python3wos.mybluemix.net/index_500.html
* http://python3wos.mybluemix.net/index_1000.html
* http://python3wos.mybluemix.net/index_2000.html

I plan to roll these changes back into upstream and then delete this repo.  I just needed a place to experiment with ideas.
