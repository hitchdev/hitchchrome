Larger window size disable dev shm usage and sandbox:
  based on: latest version available in package
  environments:
  - mac
  - gui
  steps:
  - run: |
      driver = chrome_build.webdriver(
          headless=True,
          arguments=[
              "--window-size=1024,768",
              "--disable-dev-shm-usage",
              "--no-sandbox",
          ],
      )
      
      snapshot_ponies(driver, "additional_arguments.png")
  - screenshot exists: additional_arguments.png
