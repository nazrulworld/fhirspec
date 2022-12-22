# -*- coding: utf-8 -*-
import os
import pathlib
import shutil
import tempfile
import typing
import zipfile

import pytest

import fhirspec
from fhirspec import Configuration

STATIC_DIR = pathlib.Path(os.path.dirname(os.path.abspath(__file__))) / "static"
DEFINITION_DIR = STATIC_DIR / "HL7" / "FHIR"


def extract_archive(extract_location: pathlib.Path, archive_file: pathlib.Path):
    """ """
    with zipfile.ZipFile(str(archive_file), "r") as zip_ref:
        zip_ref.extractall(extract_location)


def ensure_static_files() -> typing.Dict[str, typing.List[pathlib.Path]]:
    """ """
    base_url = "https://github.com/nazrulworld/hl7-archives/raw/0.3.2/FHIR"
    files = ("definitions-json.zip", "examples-json.zip", "version.info")
    results: typing.Dict[str, typing.List[pathlib.Path]] = {}
    for item in (("R4B", "4.3.0"), ("R4", "4.0.1"), ("STU3", "3.0.2")):
        release, version = item
        directory = DEFINITION_DIR / release / version
        if not directory.exists():
            directory.mkdir(parents=True)
        results[release] = list()
        for file_suffix in files:
            filename = version + "-" + file_suffix
            if not (directory / filename).exists():
                file_location = fhirspec.download(
                    base_url + "/" + release + "/" + filename, directory
                )
                results[release].append(file_location)
            else:
                results[release].append(directory / filename)

    return results


@pytest.fixture(scope="session")
def settings():
    """ """
    src_container = pathlib.Path(tempfile.mkdtemp())
    releases = ensure_static_files()
    config = Configuration.from_json_file(STATIC_DIR / "testconfig.json")
    sources = list()
    for release in releases:
        src_dir = src_container / release
        for file_ in releases[release]:
            if file_.suffix == ".zip":
                filename = file_.name[6:-9]
                extract_archive(src_dir / filename, file_)
            elif file_.suffix == ".info":
                shutil.copy(file_, (src_dir / "version.info"))
        sources.append(src_dir)

    yield config, sources
    # do teardown
    shutil.rmtree(src_container)
