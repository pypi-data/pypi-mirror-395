import re
from typing import OrderedDict
from typing import Tuple
from uuid import UUID

import httpx
import structlog.stdlib
import xmltodict
from httpx import HTTPError
from httpx import StreamError
from pydantic import parse_obj_as
from pydantic import ValidationError

from sdclient.exceptions import SDCallError
from sdclient.exceptions import SDEmploymentNotFound
from sdclient.exceptions import SDParentNotFound
from sdclient.exceptions import SDParseResponseError
from sdclient.exceptions import SDRootElementNotFound
from sdclient.requests import GetDepartmentParentRequest
from sdclient.requests import GetDepartmentRequest
from sdclient.requests import GetEmploymentChangedAtDateRequest
from sdclient.requests import GetEmploymentChangedRequest
from sdclient.requests import GetEmploymentRequest
from sdclient.requests import GetInstitutionRequest
from sdclient.requests import GetOrganizationRequest
from sdclient.requests import GetPersonChangedAtDateRequest
from sdclient.requests import GetPersonRequest
from sdclient.requests import GetProfessionRequest
from sdclient.requests import SDRequest
from sdclient.responses import DepartmentParentHistoryObj
from sdclient.responses import GetDepartmentParentResponse
from sdclient.responses import GetDepartmentResponse
from sdclient.responses import GetEmploymentChangedAtDateResponse
from sdclient.responses import GetEmploymentChangedResponse
from sdclient.responses import GetEmploymentResponse
from sdclient.responses import GetInstitutionResponse
from sdclient.responses import GetOrganizationResponse
from sdclient.responses import GetPersonChangedAtDateResponse
from sdclient.responses import GetPersonResponse
from sdclient.responses import GetProfessionResponse

REGEX_EMPLOYMENT_NOT_FOUND = re.compile(".*The stated.*does not exist.*")

logger = structlog.stdlib.get_logger()


class SDClient:
    def __init__(
        self,
        sd_username: str,
        sd_password: str,
        timeout: int = 120,
        url_subpath_xml_endpoints: str = "",
        url_subpath_json_endpoints: str = "",
    ):
        self.username = sd_username
        self.password = sd_password
        self.timeout = timeout
        self.url_subpath_xml_endpoints = url_subpath_xml_endpoints
        self.url_subpath_json_endpoints = url_subpath_json_endpoints

    def _call_sd(
        self, query_params: SDRequest, xml_force_list: Tuple[str, ...] = tuple()
    ) -> OrderedDict:
        """
        Call SD endpoint.

        Easiest way to obtain a Pydantic instance (which is created based on
        the OrderedDict returned from this method) seems to be
        XML -> OrderedDict (via xmltodict) -> Pydantic instance
        instead of using the lxml library, since we can use the Pydantic method
        parse_obj to generate to instances directly from OrderedDicts.

        Args:
            query_params: The HTTP query parameters to set in the request
            xml_force_list: A tuple of elements in the returned OrderedDict
                which MUST be lists. This ensures that the SD OrderedDicts
                are compatible with the SD response Pydantic models
        Returns:
            XML response from SD in the form of an OrderedDict
        """

        # Get the endpoint name, e.g. "GetEmployment20111201"
        endpoint_name = query_params.get_name()
        url = f"https://service.sd.dk{self.url_subpath_xml_endpoints}/sdws/"

        try:
            response = httpx.get(
                url + endpoint_name,
                params=query_params.to_query_params(),
                auth=(self.username, self.password),
                timeout=self.timeout,
            )
            response.raise_for_status()
        except (HTTPError, StreamError) as err:
            raise SDCallError("There was a problem calling SD") from err

        # When the SD API is closed, we still get a HTTP 200, so we will have to
        # settle for checking this string
        if "The webservice has failed" in response.text:
            raise SDCallError("There was a problem calling SD")

        # Nice for debugging
        # import lxml.etree
        # sd_xml_resp = lxml.etree.XML(response.text.split(">", maxsplit=1)[1])
        # xml = lxml.etree.tostring(sd_xml_resp, pretty_print=True).decode("utf-8")
        # print(xml)

        try:
            xml_to_ordered_dict = xmltodict.parse(
                response.text, force_list=xml_force_list, xml_attribs=False
            )
        except Exception as err:
            raise SDParseResponseError(
                "XML response from SD could not be parsed"
            ) from err

        sd_api_error_msg: str | None = (
            xml_to_ordered_dict.get("Envelope", dict())
            .get("Body", dict())
            .get("Fault", dict())
            .get("detail", dict())
            .get("string")
        )
        if (
            sd_api_error_msg is not None
            and REGEX_EMPLOYMENT_NOT_FOUND.match(sd_api_error_msg)
            and query_params.get_name()
            in (
                "GetEmployment20111201",
                "GetEmploymentChanged20111201",
            )
        ):
            raise SDEmploymentNotFound(f"SD employment not found: {str(query_params)}")

        root_elem = xml_to_ordered_dict.get(endpoint_name)
        if root_elem is None:
            logger.error("Could not find XML root element", response=response.text)
            raise SDRootElementNotFound(
                "Could not find XML root element",
                error=dict(xml_to_ordered_dict),
            )

        return root_elem

    def get_department(
        self, query_params: GetDepartmentRequest
    ) -> GetDepartmentResponse:
        """
        Call the SD endpoint GetDepartment.

        Args:
            query_params: The HTTP query parameters to set in the request

        Returns:
            XML response from SD converted to Pydantic
        """
        root_elem = self._call_sd(query_params, xml_force_list=("Department",))
        return GetDepartmentResponse.parse_obj(root_elem)

    def get_person(self, query_params: GetPersonRequest) -> GetPersonResponse:
        """
        Call the SD endpoint GetPerson.

        Args:
            query_params: The HTTP query parameters to set in the request

        Returns:
            XML response from SD converted to Pydantic
        """
        root_elem = self._call_sd(
            query_params,
            xml_force_list=(
                "Person",
                "Employment",
                "TelephoneNumberIdentifier",
                "EmailAddressIdentifier",
            ),
        )
        return GetPersonResponse.parse_obj(root_elem)

    def get_employment(
        self, query_params: GetEmploymentRequest
    ) -> GetEmploymentResponse:
        """
        Call the SD endpoint GetEmployment.

        Args:
            query_params: The HTTP query parameters to set in the request

        Returns:
            XML response from SD converted to Pydantic
        """

        root_elem = self._call_sd(query_params, xml_force_list=("Person", "Employment"))
        return GetEmploymentResponse.parse_obj(root_elem)

    def get_employment_changed(
        self, query_params: GetEmploymentChangedRequest
    ) -> GetEmploymentChangedResponse:
        """
        Call the SD endpoint GetEmploymentChanged.

        Args:
            query_params: The HTTP query parameters to set in the request

        Returns:
            XML response from SD converted to Pydantic
        """

        root_elem = self._call_sd(
            query_params,
            xml_force_list=(
                "Person",
                "Employment",
                "EmploymentStatus",
                "EmploymentDepartment",
                "Profession",
                "WorkingTime",
            ),
        )
        return GetEmploymentChangedResponse.parse_obj(root_elem)

    def get_employment_changed_at_date(
        self, query_params: GetEmploymentChangedAtDateRequest
    ) -> GetEmploymentChangedAtDateResponse:
        """
        Call the SD endpoint GetEmploymentChangedAtDate.

        Args:
            query_params: The HTTP query parameters to set in the request

        Returns:
            XML response from SD converted to Pydantic
        """

        root_elem = self._call_sd(
            query_params,
            xml_force_list=(
                "Person",
                "Employment",
                "EmploymentStatus",
                "EmploymentDepartment",
                "Profession",
                "WorkingTime",
            ),
        )
        return GetEmploymentChangedAtDateResponse.parse_obj(root_elem)

    def get_person_changed_at_date(
        self, query_params: GetPersonChangedAtDateRequest
    ) -> GetPersonChangedAtDateResponse:
        """
        Call the SD endpoint GetPersonChangedAtDate.

        Args:
            query_params: The HTTP query parameters to set in the request

        Returns:
            XML response from SD converted to Pydantic
        """

        root_elem = self._call_sd(
            query_params,
            xml_force_list=(
                "Person",
                "Employment",
                "TelephoneNumberIdentifier",
                "EmailAddressIdentifier",
            ),
        )
        return GetPersonChangedAtDateResponse.parse_obj(root_elem)

    def get_organization(
        self, query_params: GetOrganizationRequest
    ) -> GetOrganizationResponse:
        """
        Call the SD endpoint GetEmployment.

        Args:
            query_params: The HTTP query parameters to set in the request

        Returns:
            XML response from SD converted to Pydantic
        """

        root_elem = self._call_sd(
            query_params, xml_force_list=("DepartmentReference", "Organization")
        )
        return GetOrganizationResponse.parse_obj(root_elem)

    def get_department_parent(
        self, query_params: GetDepartmentParentRequest
    ) -> GetDepartmentParentResponse | None:
        """
        Call the SD endpoint GetDepartmentParent.

        Args:
            query_params: The HTTP query parameters to set in the request

        Returns:
            XML response from SD converted to Pydantic
        """

        root_elem = self._call_sd(query_params)
        try:
            resp = GetDepartmentParentResponse.parse_obj(root_elem)
        except ValidationError:
            resp = None
        return resp

    def get_department_parent_history(
        self, org_unit_uuid: UUID
    ) -> list[DepartmentParentHistoryObj]:
        """
        Get the parent history for a department.

        Args:
            org_unit_uuid: UUID of the org unit

        Returns:
            JSON response from SD converted to Pydantic
        """
        try:
            response = httpx.get(
                f"https://service.sd.dk{self.url_subpath_json_endpoints}/api-gateway/organization/public/api/v1/organizations/uuids/{str(org_unit_uuid)}/department-parent-history",
                auth=(self.username, self.password),
                timeout=self.timeout,
            )
            if response.status_code == 404:
                raise SDParentNotFound("Parent history not found!")
            response.raise_for_status()
        except (HTTPError, StreamError) as err:
            raise SDCallError("There was a problem calling SD") from err

        return parse_obj_as(list[DepartmentParentHistoryObj], response.json())

    def get_profession(
        self, query_params: GetProfessionRequest
    ) -> GetProfessionResponse:
        """
        Call the SD endpoint GetProfession.

        Args:
            query_params: The HTTP query parameters to set in the request

        Returns:
            XML response from SD converted to Pydantic
        """
        root_elem = self._call_sd(query_params, xml_force_list=("Profession",))
        return GetProfessionResponse.parse_obj(root_elem)

    def get_institution(
        self, query_params: GetInstitutionRequest
    ) -> GetInstitutionResponse:
        """
        Call the SD endpoint GetInstitution.

        Args:
            query_params: The HTTP query parameters to set in the request

        Returns:
            XML response from SD converted to Pydantic
        """
        root_elem = self._call_sd(query_params)
        return GetInstitutionResponse.parse_obj(root_elem)
