from hitchstory import HitchStoryException, StoryCollection
from hitchrun import expected
from commandlib import CommandError
from strictyaml import Str, Map, Bool, load
from pathquery import pathquery
from hitchrun import DIR
import dirtemplate
import hitchpylibrarytoolkit
from path import Path
#from engine import Engine

PROJECT_NAME = "hitchchrome"

@expected(CommandError)
def run():
    python_path = DIR.gen / "venv"
    if not python_path.exists():
        python = hitchpylibrarytoolkit.project_build(
            "hitchchrome",
            DIR,
            "3.7.0",
        ).bin.python
    else:
        python = Path(python_path) / "bin" / "python"
    assert Path(python).exists()
    DIR.gen.joinpath("example.py").write_text(DIR.key.joinpath("example.py").text())
    python(DIR.gen.joinpath("example.py")).in_dir(DIR.gen).run()


def deploy(version):
    """
    Deploy to pypi as specified version.
    """
    hitchpylibrarytoolkit.deploy(DIR.project, PROJECT_NAME, version)
