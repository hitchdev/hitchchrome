# HitchChrome

If you have used python with selenium more than a small amount you
may have run into a problem caused by one of these three not
being compatible with one or more of the others:

* The browser version.
* The selenium driver version.
* The selenium version.

This package is a way to install all three of these *together*
to avoid this problem not only when you first set selenium up
but also to prevent this scenario, which has happened to me:

1. You've got a big release planned for tomorrow.
2. Google chrome/chromium is upgraded by your OS or inside your docker container somehow.
3. Your regression test suite breaks because the new version of the browser is incompatible and your tests break.
4. You're up all night trying to fix it.

HitchChrome is part of the [hitchdev framework](http://hitchdev.com).

Please note that this package is intended FOR TESTING ONLY. The
browser does NOT receive security updates and is potentially unsafe.

## How?

First, build into a directory of your choice:

```python
from hitchchrome import ChromeBuild

chrome_build = ChromeBuild("./chrome84", "84")
chrome_build.ensure_built()
```

Then use, either with GUI:

```python
driver = chrome_build.webdriver()
driver.get("http://www.google.com")
driver.quit()
```

Or headless:

```python
driver = chrome_build.webdriver(headless=True)
driver.get("http://www.google.com")
driver.quit()
```

## Package Status

* Alpha state. No rigorous regression testing applied yet.
* Currently only works with Chromium stable version 84. Should work with multiple stable versions.

## Why not X?

* Docker. Either you run the browser headless or you will potentially spend more time trying to get it to work than it took me to build this package. That said, you could potentially run this package in docker (see caveats below though).
* pyderman - only downloads chromedriver. Unless all three versions are controlled and kept in sync (browser, driver, selenium), something will likely get out of sync eventually.
* chromedriver-binary -- same. Also, you have to manually update it in your requirements.txt when your OS upgrades chrome or chromium or you want to upgrade selenium.

## Caveats

* Requires aria2 to be installed (to download). You will need to "apt-get install aria2" or "brew install aria2" or equivalent.
* Avoid using this package for regular browsing and/or scraping. It fixes the version of chromium which does NOT receive security updates. If you get hacked because of this package that is on you. This package comes with NO warranty, implied or otherwise. Use entirely at your own risk. It is suggested that it be used solely for testing your OWN code.
* This package fixes the version of selenium in setup.py. This is done deliberately to ensure that the version being used has been tested with the version of chromium/chromedriver downloaded. If you have a later version of selenium in a requirements file or as a dependency of other packages it may conflict with this one.

## Docker caveats

* ensure_built() will download and install chromium + driver the first time it is run and use it subsequent times it is run. If you run this in a docker container, unless you run it during the build step, it will try to download chrome (~150MB) *each time you run it*. It'll work, but that will get annoying quickly.
* If you use this package headless, inside a docker container, the user must not be root (i.e. default user). Chrome will refuse to run.
