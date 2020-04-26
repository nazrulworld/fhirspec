# -*- coding: utf-8 -*-
import fhirspec
import tempfile
import shutil
import pathlib
import pytest


def test_configuration_from_module():
    """ """
    from . import baseconfig
    config = fhirspec.Configuration.from_module(baseconfig)
    assert config.BASE_PATH == baseconfig.BASE_PATH


@pytest.mark.skipif(1 == 1, reason="Only runs in Travis Environment.")
def test_download():
    """ """
    temp_dir = pathlib.Path(tempfile.mkdtemp())
    text_file = (
        "https://raw.githubusercontent.com/"
        "nazrulworld/fhir-parser/master/archives/"
        "HL7/FHIR/STU3/3.0.1-version.info"
    )
    html_file = ""
    json_file = ""
    zip_file = (
        "https://github.com/nazrulworld/fhir-parser/"
        "raw/master/archives/HL7/FHIR/STU3/3.0.2-examples-json.zip"
    )
    file1 = fhirspec.download(text_file, temp_dir)
    assert file1.exists()
    file2 = fhirspec.download(zip_file, temp_dir)
    assert file2.exists()
    shutil.rmtree(temp_dir)
