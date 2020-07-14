# HitchChrome

If you've ever had a problem with not having a chromedriver installed or
your version of chromedriver not matching your installed version of chrome or
some annoying obscure "browser fails to start with selenium" error that only
starts happening randomly a *day* before you want to release because somebody
ran a system upgrade, this is the package for you.

HitchChrome is a self contained package that will download
and install its own isolated version of of Chrome *and* ChromeDriver that
will work together and won't randomly break when somebody upgrades
something.

HitchChrome is part of the [hitchdev framework](http://hitchdev.com) -
an attempt to introduce a whole new philosophy of testing, specifying and
developing python code.

## How?

First, build into a directory of your choice:

```python
from hitchchrome import ChromeBuild

chrome_build = ChromeBuild("./chrome83", "83")
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

## Work to be done soon

* Currently only works with Chromium stable version 83. Should work with multiple stable versions.
* Only works with linux (should "just work" with mac soon).

## Caveats

Requires aria2 to be installed (to download chrome + chromedriver).
You need apt-get install aria2.
