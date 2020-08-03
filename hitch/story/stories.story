Latest version available in package:
  given:
    setup: |
      from hitchchrome import ChromeBuild
      from selenium.webdriver.common.keys import Keys
      
      def snapshot_ponies(driver, screenshot_filename):
          driver.get("http://www.google.com")
          driver.find_element_by_name("q").send_keys("ponies")
          driver.find_element_by_name("q").send_keys(Keys.ENTER)
          driver.save_screenshot(screenshot_filename)
          driver.quit()
      
      chrome_build = ChromeBuild("../../chrome")
  steps:
  - run: |
      chrome_build.ensure_built()

Run chrome with additional arguments:
  based on: latest version available in package
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

Run chrome headless:
  based on: latest version available in package
  steps:
  - run: |
      driver = chrome_build.webdriver(headless=True)
      
      snapshot_ponies(driver, "headless.png")
  - screenshot exists: headless.png
  
  
Run chrome with gui:
  based on: latest version available in package
  steps:
  - run: |
      driver = chrome_build.webdriver()
      
      snapshot_ponies(driver, "non_headless.png")
  - screenshot exists: non_headless.png
  
  
Run chrome without sandbox:
  based on: latest version available in package
  steps:
  - run: |
      driver = chrome_build.webdriver(arguments=["--nosandbox"])
      
      snapshot_ponies(driver, "without_sandbox.png")
  - screenshot exists: without_sandbox.png
