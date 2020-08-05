from hitchstory import InfoDefinition, InfoProperty
from strictyaml import Seq, Enum
import hitchpylibrarytoolkit
import hitchchrome
import os


class Engine(hitchpylibrarytoolkit.Engine):
    info_definition = InfoDefinition(
        environments=InfoProperty(Seq(Enum([
            "gui", "mac", "docker", "headless", "wsl"
        ]))),
    )
        
    def set_up(self):
        super().set_up()
        self._chrome = hitchchrome.ChromeBuild(
            self._build._paths.gen / "devchrome"
        )
        self._chrome.ensure_built()
        if "EXTERNAL_CHROME" not in os.environ:
            os.environ["EXTERNAL_CHROME"] = str(self._chrome.chrome_bin)

    def screenshot_exists(self, filename):
        assert self._build.working.joinpath(filename).exists()
