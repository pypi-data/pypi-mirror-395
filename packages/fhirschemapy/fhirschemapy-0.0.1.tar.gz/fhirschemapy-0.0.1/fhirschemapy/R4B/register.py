from fhirschemapy.R4B.base import Extension
from fhirschemapy.R4B.medication_request import MedicationRequest
from fhirschemapy.R4B.patient import Patient


def register_fhir_models() -> None:
    print("Registering FHIR models")
    Extension.model_rebuild()
    Patient.model_rebuild()
    MedicationRequest.model_rebuild()
