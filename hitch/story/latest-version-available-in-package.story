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
