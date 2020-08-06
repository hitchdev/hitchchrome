Only chromedriver:
  environments:
  - mac
  - gui
  - headless
  given:
    setup: |
        from hitchchrome import ChromeBuild
        from selenium.webdriver.common.keys import Keys
        from os import getenv
        
        def snapshot_ponies(driver, screenshot_filename):
            driver.get("http://www.google.com")
            driver.find_element_by_name("q").send_keys("ponies")
            driver.find_element_by_name("q").send_keys(Keys.ENTER)
            driver.save_screenshot(screenshot_filename)
            driver.quit()
        
        chrome_build = ChromeBuild(
            "../../chrome",
            version=getenv("EXTERNAL_VERSION", "84"),
            only_driver=True
        )

  steps:
  - run: |
      chrome_build.ensure_built()

      driver = chrome_build.webdriver(headless=True, chrome=getenv("EXTERNAL_CHROME"))
      
      snapshot_ponies(driver, "only_webdriver.png")
  - screenshot exists: only_webdriver.png
