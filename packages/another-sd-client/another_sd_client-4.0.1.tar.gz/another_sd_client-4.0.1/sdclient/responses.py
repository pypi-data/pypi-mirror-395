from __future__ import annotations

from datetime import date
from uuid import UUID

from pydantic import BaseModel
from pydantic import PositiveInt
from pydantic.types import Decimal

from sdclient.date_utils import sd_date_to_str


class DefaultDates(BaseModel):
    ActivationDate: date
    DeactivationDate: date


class PostalAddress(BaseModel):
    StandardAddressIdentifier: str | None = None
    PostalCode: str | None = None
    DistrictName: str | None = None
    MunicipalityCode: PositiveInt | None = None
    CountryIdentificationCode: str | None = None


class ContactInformation(BaseModel):
    TelephoneNumberIdentifier: list[str] | None = None
    EmailAddressIdentifier: list[str] | None = None


class Department(DefaultDates):
    DepartmentIdentifier: str
    DepartmentLevelIdentifier: str
    DepartmentName: str | None = None
    DepartmentUUIDIdentifier: UUID | None = None
    PostalAddress: PostalAddress | None = None
    ProductionUnitIdentifier: int | None = None
    ContactInformation: ContactInformation | None = None


class EmploymentStatus(DefaultDates):
    # TODO: add constraint
    EmploymentStatusCode: str

    def __str__(self):
        return (
            f"({sd_date_to_str(self.ActivationDate)}, "
            f"{sd_date_to_str(self.DeactivationDate)}) "
            f"Status{{{self.EmploymentStatusCode}}}"
        )


class EmploymentDepartment(DefaultDates):
    DepartmentIdentifier: str
    DepartmentUUIDIdentifier: UUID | None = None

    def __str__(self):
        return (
            f"({sd_date_to_str(self.ActivationDate)}, "
            f"{sd_date_to_str(self.DeactivationDate)}) "
            f"Dep{{{str(self.DepartmentUUIDIdentifier)}, {self.DepartmentIdentifier}}}"
        )


class Profession(DefaultDates):
    JobPositionIdentifier: str
    EmploymentName: str | None = None
    AppointmentCode: str | None = None

    def __str__(self):
        return (
            f"({sd_date_to_str(self.ActivationDate)}, "
            f"{sd_date_to_str(self.DeactivationDate)}) "
            f"{self.EmploymentName}{{{self.JobPositionIdentifier}}}"
        )


class WorkingTime(DefaultDates):
    OccupationRate: Decimal
    SalaryRate: Decimal
    SalariedIndicator: bool
    FullTimeIndicator: bool | None = None


class Employment(BaseModel):
    EmploymentIdentifier: str
    EmploymentDate: date
    AnniversaryDate: date
    EmploymentStatus: EmploymentStatus
    EmploymentDepartment: EmploymentDepartment | None = None
    Profession: Profession | None = None
    WorkingTime: WorkingTime | None = None


class EmploymentWithLists(BaseModel):
    EmploymentIdentifier: str
    EmploymentDate: date | None = None
    AnniversaryDate: date | None = None
    EmploymentStatus: list[EmploymentStatus] | None = None
    EmploymentDepartment: list[EmploymentDepartment] | None = None
    Profession: list[Profession] | None = None
    WorkingTime: list[WorkingTime] | None = None

    def __str__(self) -> str:
        def get_attr_list(attr: str) -> str:
            return (
                "\n  ".join(str(attr) for attr in getattr(self, attr))
                if getattr(self, attr)
                else ""
            )

        return (
            f"--------------------------\n"
            f"EmploymentIdentifier={self.EmploymentIdentifier}\n"
            f"EmploymentStatus=[\n  "
            f"{get_attr_list('EmploymentStatus')}\n"
            f"]\n"
            f"EmploymentDepartment=[\n  "
            f"{get_attr_list('EmploymentDepartment')}\n"
            f"]\n"
            f"Profession=[\n  "
            f"{get_attr_list('Profession')}\n"
            f"]"
        )


class EmploymentPerson(BaseModel):
    """
    An SD (GetEmployment) person... can maybe be generalized
    """

    # TODO: add constraint
    PersonCivilRegistrationIdentifier: str
    Employment: list[Employment]


class PersonEmployment(BaseModel):
    EmploymentIdentifier: str | None = None
    ContactInformation: ContactInformation | None = None


class Person(BaseModel):
    """
    An SD (GetPerson, GetPersonChangedAtDate) person.
    """

    PersonCivilRegistrationIdentifier: str
    PersonGivenName: str | None = None
    PersonSurnameName: str | None = None

    PostalAddress: PostalAddress | None = None
    ContactInformation: ContactInformation | None = None

    Employment: list[PersonEmployment]


class EmploymentPersonWithLists(BaseModel):
    """
    An SD (GetEmployment) person... can maybe be generalized
    """

    # TODO: add constraint
    PersonCivilRegistrationIdentifier: str
    Employment: list[EmploymentWithLists]


class GetDepartmentResponse(BaseModel):
    """
    Response model for SDs GetDepartment20111201
    """

    # TODO: add missing fields
    RegionIdentifier: str
    RegionUUIDIdentifier: UUID | None = None
    InstitutionIdentifier: str
    InstitutionUUIDIdentifier: UUID | None = None
    Department: list[Department] = []


class GetPersonResponse(BaseModel):
    """
    Response model for SDs GetPerson20111201
    """

    Person: list[Person] = []


class GetEmploymentResponse(BaseModel):
    """
    Response model for SDs GetEmployment20111201
    """

    Person: list[EmploymentPerson] = []


class GetEmploymentChangedResponse(BaseModel):
    """
    Response model for SDs GetEmploymentChanged20111201
    """

    Person: list[EmploymentPersonWithLists] = []


class GetEmploymentChangedAtDateResponse(GetEmploymentChangedResponse):
    """
    Response model for SDs GetEmploymentChangedAtDate20111201
    """

    pass


class GetPersonChangedAtDateResponse(BaseModel):
    """
    Response model for SDs GetPersonChangedAtDate20111201
    """

    Person: list[Person] = []


class DepartmentLevelReference(BaseModel):
    DepartmentLevelIdentifier: str | None = None
    DepartmentLevelReference: DepartmentLevelReference | None = None
    # TODO: add validator?


class DepartmentReference(BaseModel):
    DepartmentIdentifier: str
    DepartmentUUIDIdentifier: UUID | None = None
    DepartmentLevelIdentifier: str
    DepartmentReference: list[DepartmentReference] = []


class OrganizationModel(DefaultDates):
    DepartmentReference: list[DepartmentReference] = []


class GetOrganizationResponse(BaseModel):
    """
    Response model for SDs GetOrganisation20111201
    """

    RegionIdentifier: str
    RegionUUIDIdentifier: UUID | None = None
    InstitutionIdentifier: str
    InstitutionUUIDIdentifier: UUID | None = None
    DepartmentStructureName: str

    OrganizationStructure: DepartmentLevelReference
    Organization: list[OrganizationModel] = []


class DepartmentParent(BaseModel):
    DepartmentUUIDIdentifier: UUID


class GetDepartmentParentResponse(BaseModel):
    """
    Response model for SDs GetDepartmentParent20190701
    """

    DepartmentParent: DepartmentParent


class DepartmentParentHistoryObj(BaseModel):
    startDate: date
    endDate: date
    parentUuid: UUID


class ProfessionObj(BaseModel):
    # The JobPositionIdentifier is guaranteed unique *within* each level, not
    # across levels!
    JobPositionIdentifier: str
    # A name is only required at level 0. It can be empty at other levels.
    JobPositionName: str | None
    # An employment always refers to a profession on level 0. Level 1-3 are
    # groupings of codes that can be used for statistics or budgeting, e.g.
    # "all nurses" or "all doctors", i.e. unused in OS2mo.
    JobPositionLevelCode: str
    Profession: list[ProfessionObj] = []


class GetProfessionResponse(BaseModel):
    Profession: list[ProfessionObj]


class Institution(BaseModel):
    InstitutionIdentifier: str
    InstitutionUUIDIdentifier: UUID | None = None
    InstitutionName: str


class Region(BaseModel):
    RegionIdentifier: str
    RegionUUIDIdentifier: UUID | None = None
    RegionName: str
    Institution: Institution


class GetInstitutionResponse(BaseModel):
    Region: Region
