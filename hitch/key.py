from hitchstory import HitchStoryException, StoryCollection
from hitchrun import expected
from commandlib import CommandError
from strictyaml import Str, Map, Bool, load
from pathquery import pathquery
from hitchrun import DIR
import dirtemplate
import hitchpylibrarytoolkit
from path import Path
from versionbullshit import get_versions
from engine import Engine
import json

PROJECT_NAME = "hitchchrome"

toolkit = hitchpylibrarytoolkit.ProjectToolkit(
    "hitchchrome",
    DIR,
)

build = hitchpylibrarytoolkit.PyLibraryBuild(
    "hitchchrome",
    DIR,
)


@expected(CommandError)
def run(name=""):
    """Run example.py with python 3.7.0"""
    examples = DIR.key / "examples"
    if name == "":
        for example in examples.listdir():
            print(example.basename().replace(".py", ""))
        return

    if DIR.gen.joinpath("screenshot.png").exists():
        DIR.gen.joinpath("screenshot.png").remove()

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
    python(DIR.key.joinpath("examples", "{}.py".format(name))).in_dir(DIR.gen).run()
    assert DIR.gen.joinpath("screenshot.png").exists(), "screenshot should have been created"


@expected(HitchStoryException)
def bdd(*keywords):
    """Run single story."""
    toolkit.bdd(Engine(build), keywords)


@expected(CommandError)
def clean():
    """Clean out built chrome and temp directory"""
    DIR.gen.joinpath("chrome").rmtree(ignore_errors=True)
    DIR.gen.joinpath("tmp").rmtree(ignore_errors=True)


@expected(CommandError)
def test(name):
    """Clean and run to check the package works in current environment"""
    clean()
    run(name)

def deploy(version):
    """
    Deploy to pypi as specified version.
    """
    toolkit.deploy(version)


def checkversioner():
    """
    Check version getting works.
    """
    print(json.dumps(get_versions(), indent=4))


def writeversions():
    """
    Write new versions JSON.
    """
    versionsjson = DIR.project.joinpath("hitchchrome", "versions.json")
    versionsjson.write_text(json.dumps(get_versions(), indent=4))
    print(versionsjson.text())
    
