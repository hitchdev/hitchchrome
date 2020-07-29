from hitchchrome import ChromeBuild

chrome_build = ChromeBuild("./chrome")

chrome_build.ensure_built()

driver = chrome_build.webdriver(
    headless=True,
    arguments=[
        "--window-size=1024,768",
        "--disable-dev-shm-usage",
        "--no-sandbox",
    ],
)

from selenium.webdriver.common.keys import Keys
driver.get("http://www.google.com")
driver.find_element_by_name("q").send_keys("ponies")
driver.find_element_by_name("q").send_keys(Keys.ENTER)
driver.save_screenshot("screenshot.png")
driver.quit()

print("Chrome arguments ran")
