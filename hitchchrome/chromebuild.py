from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from commandlib import Command
from hitchchrome import utils
from path import Path
import hitchbuild


CHROME_LINUX_URL = "https://www.googleapis.com/download/storage/v1/b/chromium-browser-snapshots/o/Linux_x64%2F756066%2Fchrome-linux.zip?generation=1585871012733067&alt=media"

CHROMEDRIVER_URL = "https://www.googleapis.com/download/storage/v1/b/chromium-browser-snapshots/o/Linux_x64%2F756066%2Fchromedriver_linux64.zip?generation=1585871017688644&alt=media"


class ChromeBuild(hitchbuild.HitchBuild):
    def __init__(self, path, version):
        assert version == "83"
        self.buildpath = Path(path).abspath()
        self.fingerprint_path = self.buildpath / "fingerprint.txt"
        self.version = version
    
    @property
    def chrome_bin(self):
        return Command(self.buildpath / "chrome-linux" / "chrome")

    @property
    def chromedriver_bin(self):
        return Command(self.buildpath / "chromedriver_linux64" / "chromedriver")
    
    def clean(self):
        self.buildpath.rmtree(ignore_errors=True)

    def ensure_built(self):
        if self.incomplete():
            self.buildpath.rmtree(ignore_errors=True)
            self.buildpath.mkdir()
            
            # Install chrome
            download_to = self.tmp / "chrome-{}.tar.gz".format(self.version)
            utils.download_file(
                download_to,
                CHROME_LINUX_URL
            )
            utils.extract_archive(download_to, self.buildpath)
            download_to.remove()
                                      
            # Install chromedriver
            download_to = self.tmp / "chromedriver-{}.tar.gz".format(self.version)
            utils.download_file(
                download_to,
                CHROMEDRIVER_URL,
            )
            utils.extract_archive(download_to, self.buildpath)
            download_to.remove()
            self.verify()
            self.refingerprint()
    
    def verify(self):
        assert self.version in self.chrome_bin("--version").output()
        assert self.version in self.chromedriver_bin("--version").output()
    
    def webdriver(self, headless=False):
        options = Options()
        options.binary_location = str(self.chrome_bin)
        options.headless = headless

        return webdriver.Chrome(
            options=options,
            executable_path=str(self.chromedriver_bin),
        )
                                      
