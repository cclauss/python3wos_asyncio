# python3wos_asyncio

__Which of the top 5,000 most downloadd PyPI package are Python 3 compatible?__  The code in this repo should be running at: http://python3wos.mybluemix.net

This is Python 3 version of https://github.com/ubershmekel/python3wos which adds `asyncio` in order to gather the Python 3 support data from PyPI [trove classifiers].  The use of asyncio lowers the time required to gather data on 5,000 PyPI packages to about 25 seconds on [Bluemix](http://www.ibm.com/cloud-computing/bluemix/).

Static webpages are also generated just to get a sense of how Python 3 compatibility drops on larger slices:
* [Top 200](http://python3wos.mybluemix.net/index_0200.html), 
[Top 400](http://python3wos.mybluemix.net/index_0400.html), 
[Top 600](http://python3wos.mybluemix.net/index_0600.html), 
[Top 800](http://python3wos.mybluemix.net/index_0800.html), 
[Top 1000](http://python3wos.mybluemix.net/index_1000.html), 
[Top 1200](http://python3wos.mybluemix.net/index_1200.html), 
[Top 1400](http://python3wos.mybluemix.net/index_1400.html),
[Top 1600](http://python3wos.mybluemix.net/index_1600.html), 
[Top 1800](http://python3wos.mybluemix.net/index_1800.html)
* [Top 2000](http://python3wos.mybluemix.net/index_2000.html), 
[Top 2200](http://python3wos.mybluemix.net/index_2200.html), 
[Top 2400](http://python3wos.mybluemix.net/index_2400.html), 
[Top 2600](http://python3wos.mybluemix.net/index_2600.html), 
[Top 2800](http://python3wos.mybluemix.net/index_2800.html), 
[Top 3000](http://python3wos.mybluemix.net/index_3000.html), 
[Top 3200](http://python3wos.mybluemix.net/index_3200.html), 
[Top 3400](http://python3wos.mybluemix.net/index_3400.html), 
[Top 3600](http://python3wos.mybluemix.net/index_3600.html)
* < 50% Python 3 compatible ;-(  [Top 3800](http://python3wos.mybluemix.net/index_3800.html), 
[Top 4000](http://python3wos.mybluemix.net/index_4000.html), 
[Top 4200](http://python3wos.mybluemix.net/index_4200.html), 
[Top 4400](http://python3wos.mybluemix.net/index_4400.html), 
[Top 4600](http://python3wos.mybluemix.net/index_4600.html), 
[Top 4800](http://python3wos.mybluemix.net/index_4800.html), 
[Top 5000](http://python3wos.mybluemix.net/index_5000.html).

I plan to roll these changes back into upstream and then delete this repo.  I just needed a place to experiment with ideas.
