from hitchchrome import ChromeBuild

chrome_build = ChromeBuild("./chrome", "84")
chrome_build.ensure_built()

driver = chrome_build.webdriver(headless=True)

from selenium.webdriver.common.keys import Keys
driver.get("http://www.google.com")
driver.find_element_by_name("q").send_keys("ponies")
driver.find_element_by_name("q").send_keys(Keys.ENTER)
driver.save_screenshot("screenshot.png")
driver.quit()

print("Headless driver loaded google")
