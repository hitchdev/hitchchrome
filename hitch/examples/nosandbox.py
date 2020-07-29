from hitchchrome import ChromeBuild

chrome_build = ChromeBuild("./chrome", "84")

chrome_build.ensure_built()

driver = chrome_build.webdriver(arguments=["--nosandbox"])
driver.get("http://www.google.com")
driver.quit()

print("With nosandbox run")
