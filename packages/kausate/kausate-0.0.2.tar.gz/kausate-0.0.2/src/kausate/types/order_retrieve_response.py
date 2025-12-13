# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Union, Optional
from datetime import datetime
from typing_extensions import Literal, Annotated, TypeAlias

from pydantic import Field as FieldInfo

from .._utils import PropertyInfo
from .._models import BaseModel
from .currency import Currency
from .date_info import DateInfo
from .interest_type import InterestType
from .company_report import CompanyReport
from .percentage_share import PercentageShare
from .companies.address import Address
from .companies.identifier import Identifier
from .shareholder_report_data import ShareholderReportData
from .companies.document_result import DocumentResult
from .companies.live_search_response import LiveSearchResponse
from .ultimate_beneficial_owner_report import UltimateBeneficialOwnerReport

__all__ = [
    "OrderRetrieveResponse",
    "Result",
    "ResultShareholderReport",
    "ResultShareholderGraphResult",
    "ResultShareholderGraphResultGraph",
    "ResultShareholderGraphResultGraphEdge",
    "ResultShareholderGraphResultGraphEdgeData",
    "ResultShareholderGraphResultGraphNode",
    "ResultShareholderGraphResultGraphNodeData",
    "ResultShareholderGraphResultGraphNodeDataCompanyNodeData",
    "ResultShareholderGraphResultGraphNodeDataPersonNodeData",
    "ResultShareholderGraphResultGraphNodeDataFreeFloatNodeData",
]


class ResultShareholderReport(BaseModel):
    shareholder_report: ShareholderReportData = FieldInfo(alias="shareholderReport")

    type: Optional[Literal["shareholderReport"]] = None


class ResultShareholderGraphResultGraphEdgeData(BaseModel):
    interest_details: Optional[str] = FieldInfo(alias="interestDetails", default=None)
    """
    Additional details about the interest, such as the specific role name (e.g.,
    'Komplementär', 'Managing Director')
    """

    interest_type: Optional[InterestType] = FieldInfo(alias="interestType", default=None)
    """
    Describes the nature of the interest or control that an entity or person has in
    another entity.
    """

    number_of_shares: Optional[int] = FieldInfo(alias="numberOfShares", default=None)

    percentage: Optional[PercentageShare] = None
    """
    The proportion of this type of interest held by the interested party, where an
    interest is countable.
    """

    share_class: Optional[str] = FieldInfo(alias="shareClass", default=None)

    total_nominal_value: Optional[Currency] = FieldInfo(alias="totalNominalValue", default=None)
    """Total nominal value with amount and ISO 4217 currency code"""


class ResultShareholderGraphResultGraphEdge(BaseModel):
    id: str
    """Unique identifier for the edge"""

    source: str
    """ID of the source node (owner)"""

    target: str
    """ID of the target node (owned)"""

    data: Optional[ResultShareholderGraphResultGraphEdgeData] = None
    """Data for an edge in the shareholder graph."""


class ResultShareholderGraphResultGraphNodeDataCompanyNodeData(BaseModel):
    kausate_id: str = FieldInfo(alias="kausateId")

    legal_name: str = FieldInfo(alias="legalName")

    cumulative_ownership: Optional[PercentageShare] = FieldInfo(alias="cumulativeOwnership", default=None)
    """
    The proportion of this type of interest held by the interested party, where an
    interest is countable.
    """

    has_more_shareholders: Optional[bool] = FieldInfo(alias="hasMoreShareholders", default=None)

    identifiers: Optional[List[Identifier]] = None
    """
    List of identifiers found for this company (e.g., registration numbers, tax IDs)
    """

    is_expanded: Optional[bool] = FieldInfo(alias="isExpanded", default=None)

    jurisdiction_code: Optional[str] = FieldInfo(alias="jurisdictionCode", default=None)

    shareholder_count: Optional[int] = FieldInfo(alias="shareholderCount", default=None)

    shareholder_report: Optional[ShareholderReportData] = FieldInfo(alias="shareholderReport", default=None)
    """Full shareholder report data if extracted"""


class ResultShareholderGraphResultGraphNodeDataPersonNodeData(BaseModel):
    name: str

    address: Optional[Address] = None
    """Address of a company or person."""

    contact: Optional[Dict[str, str]] = None

    cumulative_ownership: Optional[PercentageShare] = FieldInfo(alias="cumulativeOwnership", default=None)
    """
    The proportion of this type of interest held by the interested party, where an
    interest is countable.
    """

    date_of_birth: Optional[DateInfo] = FieldInfo(alias="dateOfBirth", default=None)

    gender: Optional[str] = None

    identifiers: Optional[List[Identifier]] = None

    jurisdiction_code: Optional[str] = FieldInfo(alias="jurisdictionCode", default=None)

    nationality: Optional[str] = None

    role: Optional[str] = None


class ResultShareholderGraphResultGraphNodeDataFreeFloatNodeData(BaseModel):
    cumulative_ownership: Optional[PercentageShare] = FieldInfo(alias="cumulativeOwnership", default=None)
    """
    The proportion of this type of interest held by the interested party, where an
    interest is countable.
    """

    description: Optional[str] = None
    """Description of the free float"""

    name: Optional[str] = None
    """Display name for the free float"""


ResultShareholderGraphResultGraphNodeData: TypeAlias = Union[
    ResultShareholderGraphResultGraphNodeDataCompanyNodeData,
    ResultShareholderGraphResultGraphNodeDataPersonNodeData,
    ResultShareholderGraphResultGraphNodeDataFreeFloatNodeData,
]


class ResultShareholderGraphResultGraphNode(BaseModel):
    id: str
    """Unique identifier for the node"""

    data: ResultShareholderGraphResultGraphNodeData
    """Node-specific data"""

    type: Literal["company", "person", "rootEntity", "freeFloat"]
    """Type of node"""


class ResultShareholderGraphResultGraph(BaseModel):
    edges: Optional[List[ResultShareholderGraphResultGraphEdge]] = None

    extraction_timestamp: Optional[str] = FieldInfo(alias="extractionTimestamp", default=None)

    max_depth: Optional[int] = FieldInfo(alias="maxDepth", default=None)

    nodes: Optional[List[ResultShareholderGraphResultGraphNode]] = None

    root_company_id: Optional[str] = FieldInfo(alias="rootCompanyId", default=None)


class ResultShareholderGraphResult(BaseModel):
    graph: ResultShareholderGraphResultGraph
    """Graph structure with nodes and edges"""

    type: Optional[Literal["shareholderGraph"]] = None


Result: TypeAlias = Annotated[
    Union[
        DocumentResult,
        CompanyReport,
        ResultShareholderReport,
        ResultShareholderGraphResult,
        UltimateBeneficialOwnerReport,
        LiveSearchResponse,
        None,
    ],
    PropertyInfo(discriminator="type"),
]


class OrderRetrieveResponse(BaseModel):
    order_id: str = FieldInfo(alias="orderId")
    """Order ID (temporal workflow id)"""

    request_time: datetime = FieldInfo(alias="requestTime")

    status: Literal["running", "completed", "failed", "canceled", "terminated", "timedOut"]
    """Order status"""

    current_activity: Optional[str] = FieldInfo(alias="currentActivity", default=None)
    """Currently running activity name"""

    customer_reference: Optional[str] = FieldInfo(alias="customerReference", default=None)
    """Customer reference"""

    error: Optional[str] = None
    """Error message if the order failed"""

    partner_customer_id: Optional[str] = FieldInfo(alias="partnerCustomerId", default=None)
    """Partner customer ID"""

    response_time: Optional[datetime] = FieldInfo(alias="responseTime", default=None)

    result: Optional[Result] = None
    """Document download result."""
