from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from commandlib import Command
from hitchchrome import utils
from path import Path
import hitchbuild
import stat
import json
import sys

VERSIONS_PATH = Path(__file__).dirname().abspath() / "versions.json"

class ChromeBuild(hitchbuild.HitchBuild):
    def __init__(self, path, version=None):
        if version is None:
            version = "84"
        assert version == "84"
        self.buildpath = Path(path).abspath()
        self.fingerprint_path = self.buildpath / "fingerprint.txt"
        self.version = version
    
    @property
    def chrome_bin(self):
        if self.os_name == "linux":
            return Command(self.buildpath / "chrome-linux" / "chrome")
        else:
            return Command(self.buildpath / "chrome-mac" / "Chromium.app" / "Contents" / "MacOS" / "Chromium")

    @property
    def chromedriver_bin(self):
        if self.os_name == "linux":
            return Command(self.buildpath / "chromedriver_linux64" / "chromedriver")
        else:
            return Command(self.buildpath / "chromedriver_mac64" / "chromedriver")
    
    def clean(self):
        self.buildpath.rmtree(ignore_errors=True)
    
    @property
    def os_name(self):
        if sys.platform == "linux2" or sys.platform == "linux":
            return "linux"
        elif sys.platform == "darwin":
            return "mac"
        else:
            raise Exception("Platform {} not supported :(".format(sys.platform))

    def ensure_built(self):
        if self.incomplete():
            self.buildpath.rmtree(ignore_errors=True)
            self.buildpath.mkdir()
            
            download_urls = json.loads(VERSIONS_PATH.text())[self.version]
            
            if self.os_name == "linux":
                chrome_download_url = download_urls["linux_chrome"]
                chromedriver_download_url = download_urls["linux_chromedriver"]
            elif self.os_name == "mac":
                chrome_download_url = download_urls["mac_chrome"]
                chromedriver_download_url = download_urls["mac_chromedriver"]
            
            # Install chrome
            download_to = self.tmp / "chrome-{}.zip".format(self.version)
            utils.download_file(download_to, chrome_download_url)

            if self.os_name == "mac":
                # patool has a bug on mac that breaks chromium
                Command("unzip", download_to).in_dir(self.buildpath).run()
            else:
                utils.extract_archive(download_to, self.buildpath)

            download_to.remove()

            # Install chromedriver
            download_to = self.tmp / "chromedriver-{}.zip".format(self.version)
            utils.download_file(download_to, chromedriver_download_url)
            utils.extract_archive(download_to, self.buildpath)
            download_to.remove()
            
            chromedriver_bin = Path(self.chromedriver_bin)
            chromedriver_bin.chmod(
                chromedriver_bin.stat().st_mode | stat.S_IEXEC
            )
            chrome_bin = Path(self.chrome_bin)
            chrome_bin.chmod(
                chrome_bin.stat().st_mode | stat.S_IEXEC
            )
            
            self.verify()
            self.refingerprint()
    
    def verify(self):
        assert self.version in self.chrome_bin("--version").output()
        assert self.version in self.chromedriver_bin("--version").output()
    
    def webdriver(self, headless=False, arguments=None):
        options = Options()
        options.binary_location = str(self.chrome_bin)
        options.headless = headless

        if arguments is not None:
            assert isinstance(arguments, list), 'arguments must be a list - e.g. ["--nosandbox"]'
            for argument in arguments:
                options.add_argument(argument)

        return webdriver.Chrome(
            options=options,
            executable_path=str(self.chromedriver_bin),
        )
                                      
