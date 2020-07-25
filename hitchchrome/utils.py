from commandlib import Command, CommandError
from path import Path
import patoolib
import shutil
import os


def log(message):
    print(message)


def extract_archive(filename, directory):
    patoolib.extract_archive(filename, outdir=directory)


class DownloadError(Exception):
    pass


def download_file(downloaded_file_path, url, max_connections=2, max_concurrent=5):
    """Download file to specified location."""
    file_path = Path(downloaded_file_path)
    assert file_path.isabs(), "download file path must be absolute, not relative"
    if file_path.exists():
        log("{} already downloaded".format(file_path))
        return

    log("Downloading: {}\n".format(url))
    aria2c = Command("aria2c")
    aria2c = aria2c("--max-connection-per-server={}".format(max_connections))
    aria2c = aria2c("--max-concurrent-downloads={}".format(max_concurrent))

    try:
        aria2c(
            "--dir={}".format(file_path.dirname()),
            "--out={}.part".format(file_path.basename()),
            url
        ).run()
    except CommandError:
        raise DownloadError(
            "Failed to download {}. Re-running may fix the problem.".format(url)
        )

    shutil.move(file_path + ".part", file_path)
