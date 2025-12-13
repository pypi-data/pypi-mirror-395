import pytest

from fhirschemapy.R4B.medication_request import MedicationRequest
from fhirschemapy.R4B.base import CodeableConcept, Reference, Identifier


def test_medication_request_minimal() -> None:
    med_req = MedicationRequest.model_construct(
        resource_type="MedicationRequest",
        status="active",
        intent="order",
        subject=Reference.model_construct(reference="Patient/1"),
    )
    assert med_req.resource_type == "MedicationRequest"
    assert med_req.status == "active"
    assert med_req.intent == "order"
    assert med_req.subject is not None and med_req.subject.reference == "Patient/1"
    assert med_req.to_json() is not None


def test_medication_request_full() -> None:
    med_req = MedicationRequest.model_construct(
        resource_type="MedicationRequest",
        status="completed",
        intent="order",
        subject=Reference.model_construct(reference="Patient/1"),
        identifier=[
            Identifier.model_construct(system="http://hospital.org", value="rx123")
        ],
        medication_codeable_concept=CodeableConcept.model_construct(text="Aspirin"),
        priority="routine",
    )
    assert med_req.status == "completed"
    assert med_req.identifier is not None and med_req.identifier[0].value == "rx123"
    assert (
        med_req.medication_codeable_concept is not None
        and med_req.medication_codeable_concept.text == "Aspirin"
    )
    assert med_req.priority == "routine"
    # Test serialization/deserialization
    json_str = med_req.to_json()
    med_req2 = MedicationRequest.from_json(json_str)
    assert (
        med_req2.medication_codeable_concept is not None
        and med_req2.medication_codeable_concept.text == "Aspirin"
    )


def test_medication_request_invalid_status() -> None:
    with pytest.raises(ValueError):
        MedicationRequest.model_construct(
            resource_type="MedicationRequest",
            status="not-a-status",  # type: ignore[arg-type]
            intent="order",
            subject=Reference.model_construct(reference="Patient/1"),
        )
