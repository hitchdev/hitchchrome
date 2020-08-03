GUI:
  based on: latest version available in package
  steps:
  - run: |
      driver = chrome_build.webdriver()
      
      snapshot_ponies(driver, "non_headless.png")
  - screenshot exists: non_headless.png
