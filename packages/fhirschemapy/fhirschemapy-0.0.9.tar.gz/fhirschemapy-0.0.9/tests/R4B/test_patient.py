import pytest


from fhirschemapy.R4B.base import (
    HumanName,
    Identifier,
    Address,
    ContactPoint,
    Reference,
)
from fhirschemapy.R4B.patient import Patient


def test_patient_minimal() -> None:
    patient = Patient()
    assert patient.resource_type == "Patient"
    assert patient.to_json() is not None


def test_patient_full() -> None:
    patient = Patient(
        active=True,
        name=[HumanName(family="Doe", given=["John"])],
        identifier=[Identifier(system="http://hospital.org", value="12345")],
        gender="male",
        birthDate="1980-01-01",
        address=[Address(city="Testville")],
        telecom=[ContactPoint(system="phone", value="555-1234")],
        managingOrganization=Reference(reference="Organization/1"),
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
        Patient(gender="invalid")  # type: ignore[arg-type]
