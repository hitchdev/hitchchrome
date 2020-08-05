Without sandbox:
  based on: latest version available in package
  environments:
  - gui
  - mac
  - docker
  steps:
  - run: |
      driver = chrome_build.webdriver(arguments=["--nosandbox"])
      
      snapshot_ponies(driver, "without_sandbox.png")

  - screenshot exists: without_sandbox.png
