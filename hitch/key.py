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


toolkit = hitchpylibrarytoolkit.ProjectToolkit(
    "hitchchrome",
    DIR,
)


@expected(HitchStoryException)
def bdd(*keywords):
    """Run single story."""
    toolkit.bdd(Engine(toolkit.build), keywords)
    

@expected(HitchStoryException)
def regression():
    """Run all stories."""
    clean()
    toolkit.regression(Engine(toolkit.build))


@expected(CommandError)
def clean():
    """Clean out built chrome and temp directory"""
    DIR.gen.joinpath("chrome").rmtree(ignore_errors=True)
    DIR.gen.joinpath("tmp").rmtree(ignore_errors=True)


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
    
