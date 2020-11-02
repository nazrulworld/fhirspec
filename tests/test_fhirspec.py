# -*- coding: utf-8 -*-
import fhirspec


def test_fhirspec_init(settings):
    """"""
    config, sources = settings
    spec = fhirspec.FHIRSpec(config, sources[0])
    assert "Patient" in fhirspec.FHIRClass.__known_classes__
    assert "PatientCommunication" in fhirspec.FHIRClass.__known_classes__
    assert "patient" in spec.profiles
