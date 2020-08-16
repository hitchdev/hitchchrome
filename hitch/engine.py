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
        self._build.ensure_built()

        for filename, contents in self.given.get('files', {}).items():
            filepath = self._build.working.parent.joinpath(filename)
            if not filepath.dirname().exists():
                filepath.dirname().makedirs()
            filepath.write_text(contents)

    def screenshot_exists(self, filename):
        assert self._build.working.joinpath(filename).exists()
