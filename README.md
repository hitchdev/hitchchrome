# HitchChrome

HitchChrome is a self contained package that will download
and install an isolated version of of Chrome/ChromeDriver that
will be more likely to work consistently with selenium
than your system packages.

## How?

First, build into a directory of your choice:

```python
from hitchchrome import ChromeBuild

chrome_build = ChromeBuild("./chrome", "83")
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

## Caveats

* Only works with Chromium stable version 83.
* Only works with linux.
* Not super heavily tested.
* Requires aria2 to be installed (to download chrome/chromedriver).

## Why?

* Ubuntu/Debian aren't very good at ensuring chromedriver/chrome versions are kept in sync.
* You can "freeze" the version of chrome available this way, and avoid indeterminacy in your tests.
* Your version of chrome shouldn't randomly stop working.
* Making docker work with UI is a pain.
