Download old version:
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
      
      chrome_build = ChromeBuild("../../chrome80", version="80")
  steps:
  - run: |
      chrome_build.ensure_built()

      driver = chrome_build.webdriver(headless=True)
      
      snapshot_ponies(driver, "version80.png")

  - screenshot exists: version80.png
