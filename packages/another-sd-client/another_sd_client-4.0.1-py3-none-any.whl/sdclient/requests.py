from datetime import date
from datetime import time
from uuid import UUID

from pydantic import BaseModel
from pydantic import root_validator


class SDRequest(BaseModel):
    class Config:
        frozen = True

    def get_name(self):
        raise NotImplementedError("Method must be implemented in subclasses")

    def to_query_params(self):
        params = self.dict()

        # Convert dates to SD date strings
        date_fields = {
            k: v.strftime("%d.%m.%4Y") for k, v in params.items() if isinstance(v, date)
        }
        params.update(date_fields)

        # Convert times into SD time strings
        time_fields = {
            k: v.strftime("%H:%M") for k, v in params.items() if isinstance(v, time)
        }
        params.update(time_fields)

        # Remove empty fields and convert remaining fields to strings
        params = {k: str(v) for k, v in params.items() if v is not None}

        return params


class GetDepartmentRequest(SDRequest):
    """
    Query parameters for SDs GetDepartment20111201 endpoint
    """

    InstitutionIdentifier: str | None = None
    InstitutionUUIDIdentifier: UUID | None = None
    DepartmentIdentifier: str | None = None
    DepartmentUUIDIdentifier: UUID | None = None
    ActivationDate: date
    DeactivationDate: date
    ContactInformationIndicator: bool = False
    DepartmentNameIndicator: bool = False
    # EmploymentDepartmentIndicator: bool = False
    PostalAddressIndicator: bool = False
    ProductionUnitIndicator: bool | None = None
    UUIDIndicator: bool = False

    # TODO: check what is actually required
    @root_validator  # type: ignore
    def check_values(cls, values):
        institution_identifier = values.get("InstitutionIdentifier")
        institution_uuid_identifier = values.get("InstitutionUUIDIdentifier")
        department_identifier = values.get("DepartmentIdentifier")
        department_uuid_identifier = values.get("DepartmentUUIDIdentifier")
        postal_address_indicator = values.get("PostalAddressIndicator")
        production_unit_indicator = values.get("ProductionUnitIndicator")

        if institution_identifier is None and institution_uuid_identifier is None:
            raise ValueError(
                "Exactly one of InstitutionIdentifier or InstitutionUUIDndentifier can be set"
            )
        if (
            institution_identifier is not None
            and institution_uuid_identifier is not None
        ):
            raise ValueError(
                "Only one of InstitutionIdentifier and InstitutionUUIDIdentifier can be set"
            )
        if department_identifier is not None and department_uuid_identifier is not None:
            raise ValueError(
                "Only one of DepartmentIdentifier and DepartmentUUIDIdentifier can be set"
            )
        if production_unit_indicator and not postal_address_indicator:
            raise ValueError(
                "ProductionUnitIndicator requires PostalAddressIndicator to be true"
            )

        return values

    def get_name(self):
        return "GetDepartment20111201"


class GetPersonRequest(SDRequest):
    """
    Query parameters for SDs GetPerson20111201 endpoint
    """

    InstitutionIdentifier: str
    EffectiveDate: date

    PersonCivilRegistrationIdentifier: str | None = None
    EmploymentIdentifier: str | None = None
    DepartmentIdentifier: str | None = None
    DepartmentLevelIdentifier: str | None = None

    StatusActiveIndicator: bool = True
    StatusPassiveIndicator: bool = False
    ContactInformationIndicator: bool = False
    PostalAddressIndicator: bool = False

    def get_name(self):
        return "GetPerson20111201"


class GetEmploymentRequest(SDRequest):
    """
    Query parameters for SDs GetEmployment20111201 endpoint
    """

    InstitutionIdentifier: str
    EffectiveDate: date

    PersonCivilRegistrationIdentifier: str | None = None
    EmploymentIdentifier: str | None = None
    DepartmentIdentifier: str | None = None
    DepartmentLevelIdentifier: str | None = None
    StatusActiveIndicator: bool = True
    StatusPassiveIndicator: bool = False
    DepartmentIndicator: bool = False
    EmploymentStatusIndicator: bool = False
    ProfessionIndicator: bool = False
    SalaryAgreementIndicator: bool = False
    SalaryCodeGroupIndicator: bool = False
    WorkingTimeIndicator: bool = False
    UUIDIndicator: bool = False

    # TODO: add validator (not enough to set StatusActiveIndicator...)
    def get_name(self):
        return "GetEmployment20111201"


class GetEmploymentChangedRequest(SDRequest):
    """
    Query parameters for SDs GetEmploymentChanged20111201 endpoint
    """

    InstitutionIdentifier: str
    PersonCivilRegistrationIdentifier: str | None = None
    EmploymentIdentifier: str | None = None
    DepartmentIdentifier: str | None = None
    DepartmentLevelIdentifier: str | None = None

    ActivationDate: date
    DeactivationDate: date
    DepartmentIndicator: bool = False
    EmploymentStatusIndicator: bool = False
    ProfessionIndicator: bool = False
    SalaryAgreementIndicator: bool = False
    SalaryCodeGroupIndicator: bool = False
    WorkingTimeIndicator: bool = False
    UUIDIndicator: bool = False

    # TODO: add validator
    def get_name(self):
        return "GetEmploymentChanged20111201"


class GetEmploymentChangedAtDateRequest(SDRequest):
    """
    Query parameters for SDs GetEmploymentChangedAtDate20111201 endpoint
    """

    InstitutionIdentifier: str
    PersonCivilRegistrationIdentifier: str | None = None
    EmploymentIdentifier: str | None = None
    DepartmentIdentifier: str | None = None
    DepartmentLevelIdentifier: str | None = None

    ActivationDate: date
    DeactivationDate: date
    ActivationTime: time = time(0, 0, 0)
    DeactivationTime: time = time(23, 59, 59)
    DepartmentIndicator: bool = False
    EmploymentStatusIndicator: bool = False
    ProfessionIndicator: bool = False
    SalaryAgreementIndicator: bool = False
    SalaryCodeGroupIndicator: bool = False
    WorkingTimeIndicator: bool = False
    UUIDIndicator: bool = False
    FutureInformationIndicator: bool = False

    # TODO: add validator
    def get_name(self):
        return "GetEmploymentChangedAtDate20111201"


class GetPersonChangedAtDateRequest(SDRequest):
    """
    Query parameters for SDs GetPersonChangedAtDate20111201 endpoint
    """

    InstitutionIdentifier: str
    PersonCivilRegistrationIdentifier: str | None = None
    EmploymentIdentifier: str | None = None
    DepartmentIdentifier: str | None = None
    DepartmentLevelIdentifier: str | None = None

    ActivationDate: date
    DeactivationDate: date
    ActivationTime: time = time(0, 0, 0)
    DeactivationTime: time = time(23, 59, 59)

    ContactInformationIndicator: bool = False
    PostalAddressIndicator: bool = False

    def get_name(self):
        return "GetPersonChangedAtDate20111201"


class GetOrganizationRequest(SDRequest):
    """
    Query parameters for SDs GetOrganization20111201 endpoint
    """

    InstitutionIdentifier: str | None = None
    InstitutionUUIDIdentifier: UUID | None = None
    ActivationDate: date
    DeactivationDate: date
    UUIDIndicator: bool = False

    @root_validator  # type: ignore
    def check_values(cls, values):
        institution_identifier = values.get("InstitutionIdentifier")
        institution_uuid_identifier = values.get("InstitutionUUIDIdentifier")
        activation_date = values.get("ActivationDate")
        deactivation_date = values.get("DeactivationDate")

        # Ensure that exactly one of "InstitutionIdentifier" and
        # "InstitutionUUIDIdentifier" is set
        if institution_identifier is None and institution_uuid_identifier is None:
            raise ValueError(
                "Exactly one of InstitutionIdentifier or InstitutionUUIDndentifier can be set"
            )
        if (
            institution_identifier is not None
            and institution_uuid_identifier is not None
        ):
            raise ValueError(
                "Only one of InstitutionIdentifier and InstitutionUUIDIdentifier can be set"
            )

        # Ensure that "ActivationDate" is before "DeactivationDate"
        if not activation_date <= deactivation_date:
            raise ValueError(
                "ActivationDate must be less than or equal to DeactivationDate"
            )

        return values

    def get_name(self):
        return "GetOrganization20111201"


class GetDepartmentParentRequest(SDRequest):
    """
    Query parameters for the GetDepartmentParent20190701 endpoint
    """

    EffectiveDate: date
    DepartmentUUIDIdentifier: UUID

    def get_name(self):
        return "GetDepartmentParent20190701"


class GetProfessionRequest(SDRequest):
    """
    Query parameters for the GetProfession20080201 endpoint
    """

    InstitutionIdentifier: str
    JobPositionIdentifier: str | None = None

    def get_name(self) -> str:
        return "GetProfession20080201"


class GetInstitutionRequest(SDRequest):
    """
    Query parameters for the GetInstitution20111201 endpoint
    """

    RegionIdentifier: str
    InstitutionIdentifier: str

    AdministrationIndicator: bool = False
    ContactInformationIndicator: bool = False
    PostalAddressIndicator: bool = False
    ProductionUnitIndicator: bool = False
    UUIDIndicator: bool = False

    def get_name(self):
        return "GetInstitution20111201"
