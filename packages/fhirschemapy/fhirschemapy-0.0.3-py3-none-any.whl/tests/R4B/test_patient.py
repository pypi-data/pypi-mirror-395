import pytest
from fhirschemapy.R4B.register import register_fhir_models
from fhirschemapy.R4B.patient import Patient
from fhirschemapy.R4B.base import (
    HumanName,
    Identifier,
    Address,
    ContactPoint,
    Reference,
)

register_fhir_models()


def test_patient_minimal() -> None:
    patient = Patient.model_construct(resource_type="Patient")
    assert patient.resource_type == "Patient"
    assert patient.to_json() is not None


def test_patient_full() -> None:
    patient = Patient.model_construct(
        resource_type="Patient",
        active=True,
        name=[HumanName.model_construct(family="Doe", given=["John"])],
        identifier=[
            Identifier.model_construct(system="http://hospital.org", value="12345")
        ],
        gender="male",
        birth_date="1980-01-01",
        address=[Address.model_construct(city="Testville")],
        telecom=[ContactPoint.model_construct(system="phone", value="555-1234")],
        managing_organization=Reference.model_construct(reference="Organization/1"),
    )
    assert patient.active is True
    assert patient.name is not None and patient.name[0].family == "Doe"
    assert patient.identifier is not None and patient.identifier[0].value == "12345"
    assert patient.gender == "male"
    assert patient.birth_date == "1980-01-01"
    assert patient.address is not None and patient.address[0].city == "Testville"
    assert patient.telecom is not None and patient.telecom[0].value == "555-1234"
    assert (
        patient.managing_organization is not None
        and patient.managing_organization.reference == "Organization/1"
    )
    # Test serialization/deserialization
    json_str = patient.to_json()
    patient2 = Patient.from_json(json_str)
    assert patient2.name is not None and patient2.name[0].family == "Doe"


def test_patient_invalid_gender() -> None:
    with pytest.raises(ValueError):
        Patient.model_construct(resource_type="Patient", gender="invalid")  # type: ignore[arg-type]
