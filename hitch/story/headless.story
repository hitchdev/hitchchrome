Headless:
  based on: latest version available in package
  steps:
  - run: |
      driver = chrome_build.webdriver(headless=True)
      
      snapshot_ponies(driver, "headless.png")
  - screenshot exists: headless.png
