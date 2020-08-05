Headless:
  based on: latest version available in package
  environments:
  - mac
  - docker
  - headless
  steps:
  - run: |
      driver = chrome_build.webdriver(headless=True)

      snapshot_ponies(driver, "headless.png")
  - screenshot exists: headless.png
