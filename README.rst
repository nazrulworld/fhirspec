=========================
FHIR Specification Parser
=========================

.. image:: https://img.shields.io/pypi/v/fhirspec.svg
        :target: https://pypi.org/project/fhirspec/

.. image:: https://img.shields.io/pypi/pyversions/fhirspec.svg
        :target: https://pypi.org/project/fhirspec/
        :alt: Supported Python Versions

.. image:: https://img.shields.io/travis/com/nazrulworld/fhirspec.svg
        :target: https://app.travis-ci.com/github/nazrulworld/fhirspec

.. image:: https://codecov.io/gh/nazrulworld/fhirspec/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/nazrulworld/fhirspec/branch/master
   :alt: Test Coverage

.. image:: https://img.shields.io/pypi/l/fhirspec.svg
   :target: https://pypi.org/project/fhirspec/
   :alt: License

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

.. image:: https://www.hl7.org/fhir/assets/images/fhir-logo-www.png
        :target: https://www.hl7.org/fhir/
        :alt: HL7® FHIR®

Python representation of FHIR® https://www.hl7.org/fhir/ specification. Idea and class structure based
on https://github.com/smart-on-fhir/fhir-parser.

Usages
======

``fhirspec.Configuration``
--------------------------
A class that is controlling the behavior of  ``fhirspec.FHIRSpec``, powerful but very convenient.
In several ways it is possible to construct the instance, ie. from ``JSON`` file (has support for `json5 <https://json5.org/>`_),
from python module, from ``TOML`` file, from plain text file, and so on.
**Only capital letter's variables are accepted**


>>> import pathlib
>>> import os
>>> from foo.module import bar
>>> from fhirspec import Configuration
>>> config1 = Configuration.from_module(bar)
>>> config2 = Configuration.from_json_file(pathlib.Path("/json/file/location"))
>>> data_dict = {
... "BASE_URL": pathlib.Path(os.path.abspath(__file__))
... }
>>> config3 = Configuration(data_dict=data_dict)



``fhirspec.FHIRSpec``
---------------------

The main loader class, to construct this instance, ``Configuration:`` is required parameter and additionally
source of json files. Bellows variables should have to be present in configuration.


	required_variables = [
		"WRITE_RESOURCES", "CLASS_MAP", "REPLACE_MAP", "NATIVES",
		"JSON_MAP", "JSON_MAP_DEFAULT", "RESERVED_MAP", "ENUM_MAP",
		"ENUM_NAME_MAP", "DEFAULT_BASES", "MANUAL_PROFILES", "CAMELCASE_CLASSES",
		"CAMELCASE_ENUMS", "BACKBONE_CLASS_ADDS_PARENT", "RESOURCE_MODULE_LOWERCASE",]


>>> from fhirspec import Configuration
>>> from fhirspec import FHIRSpec
>>> config = Configuration(
... {
...   "BASE_PATH": "",
      "WRITE_RESOURCES": True
... }
... )
>>> spec = FHIRSpec(config)
>>> "patient" in spec.profiles
True


``download``
------------

A perfect tool to download any file from server, no dependency on third-party library.

>>> from fhirspec import download
>>> url = "http://www.africau.edu/images/default/sample.pdf"
>>> download_directory = pathlib.Path(os.path.expanduser("~/Downloads"))
>>> download(url, download_directory)
>>> (download_directory / "sample.pdf").exists()
True


History
=======
0.5.0 (03-07-2025)
------------------

- Added support for ``summary`` mode.

- FHIR R5 specification support has been added.


0.4.0 (22-12-2022)
------------------

- FHIR R4B specification support has been added.

0.3.0 (18-03-2021)
------------------

- Now each ``FHIRClass`` contains original sequence of it's properties(elements) defined in specification.
- Additionally ``FHIRClass.expanded_properties_sequence`` returns all available properties (combined with parent) sequentially.


0.2.5 (02-11-2020)
------------------

- This release contains full fixes of ``FHIRStructureDefinitionElement.represents_class`` issues.


0.2.4 (02-11-2020)
------------------

- No more improvements, just same release of  ``0.2.1`` and overrides to the faulty release of ``0.2.3``.


0.2.3 (24-09-2020)
------------------

**Update to version ``0.2.4`` is recommended**

- use ``FHIRStructureDefinitionElement.is_main_profile_element`` instead of ``FHIRStructureDefinitionElement.represents_class``

0.2.1 (15-06-2020)
------------------

- Minor improvement on ``FHIRUnitTest`` handling empty value.

0.2.0 (06-06-2020)
------------------

- ``FHIRClass.known`` property has been changed to ``FHIRClass.__know_classes__`` and ``FHIRClass.is_known_class``.

- Make supports for Python 3.6 and 3.9

0.1.0 (28-04-2020)
------------------

- Initial release [nazrulworld]


------------

© Copyright HL7® logo, FHIR® logo and the flaming fire are registered trademarks
owned by `Health Level Seven International <https://www.hl7.org/legal/trademarks.cfm?ref=https://pypi.org/project/fhir-resources/>`_

**"FHIR® is the registered trademark of HL7 and is used with the permission of HL7.
Use of the FHIR trademark does not constitute endorsement of this product by HL7"**
