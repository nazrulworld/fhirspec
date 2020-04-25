# -*- coding: utf-8 -*-
import fhirspec

def test_fhirspec_init(settings):
    """"""
    config, sources = settings
    fhirspec.FHIRSpec(config, sources[0])
