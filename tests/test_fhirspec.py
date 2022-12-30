# -*- coding: utf-8 -*-
import fhirspec


def test_fhirspec_init(settings):
    """"""
    config, sources = settings
    spec = fhirspec.FHIRSpec(config, sources[0])
    assert "Patient" in fhirspec.FHIRClass.__known_classes__
    assert "PatientCommunication" in fhirspec.FHIRClass.__known_classes__
    assert "patient" in spec.profiles
    assert_binding_uri(spec)


def assert_binding_uri(spec):
    """Ensure that binding.uri binding.version set."""
    assert "address" in spec.profiles, "Expected to find address in spec."
    structure_def = next(
        iter(
            [
                e_
                for e_ in spec.profiles["address"].elements
                if e_.path == "Address.type"
            ]
        ),
        None,
    )
    assert structure_def, "Expected to find StructureDefinition for Address.type."
    assert (
        structure_def.definition.binding.uri
        == "http://hl7.org/fhir/ValueSet/address-type"
    )
    assert structure_def.definition.binding.version, "Should be set."

    # also check that it was included in the FHIRClassProperty
    property_ = next(
        iter(
            [
                p_
                for p_ in spec.profiles["address"].classes[0].properties
                if p_.path == "Address.type"
            ]
        ),
        None,
    )
    assert property_, "Expected to find a property for Address.type"
    assert property_.binding, "Expected binding to be set"
    assert property_.binding.uri == "http://hl7.org/fhir/ValueSet/address-type"
    assert property_.binding.version, "Should be set."
