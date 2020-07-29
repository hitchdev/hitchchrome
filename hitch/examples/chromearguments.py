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
driver.get("http://www.google.com")
driver.quit()

print("Chrome arguments ran")
