The [Bluemix default Buildpack for Python](https://console.ng.bluemix.net/docs/runtimes/python/index.html) is often [several releases out-of-date](https://github.com/cloudfoundry/python-buildpack/releases) from the [Cloud Foundry Buildpack for Python](https://github.com/cloudfoundry/python-buildpack).  This means that your Python project will probably not have access to the latest CPython or pip builds.  To fix this issue, I make the following tweeks to modernize my Bluemix Python projects:

1. Edit [manifest.yml](manifest.yml) to add a `buildpack` line at the end:
    *  `buildpack: https://github.com/cloudfoundry/python-buildpack.git`
2. For Python 3 apps, I add a [runtime.txt](runtime.txt) file at the root of the project which contains:
    * `python-3.6.x`

These changes will give your project access to the current [Cloud Foundery Buildpack for Python](https://github.com/cloudfoundry/python-buildpack) and the most current Cloud Foundry supported implementation of CPython2 or CPython3.

04 April 2017: Bluemix defaults to release [v1.5.5](https://github.com/cloudfoundry/python-buildpack/releases/tag/v1.5.5) while Cloud Foundry is at release [v1.5.17](https://github.com/cloudfoundry/python-buildpack/releases/tag/v1.5.17).
