from hitchchrome import ChromeBuild

chrome_build = ChromeBuild("./chrome", "84")

chrome_build.ensure_built()

driver = chrome_build.webdriver()
driver.get("http://www.google.com")
driver.quit()

driver = chrome_build.webdriver(headless=True, nosandbox=True)
driver.get("http://www.google.com")
driver.quit()
