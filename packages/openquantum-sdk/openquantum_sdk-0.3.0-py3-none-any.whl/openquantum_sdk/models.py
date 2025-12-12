from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

# ---------------------------------------------------------------------------
#  Generic models
# ---------------------------------------------------------------------------


@dataclass
class PaginationInfo:
    next_cursor: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict, repr=False)


@dataclass
class ErrorResponse:
    status_code: int
    message: List[str]
    error_code: Optional[str] = None


class APIError(Exception):
    def __init__(self, error_response: ErrorResponse):
        self.error_response = error_response
        msg = "; ".join(error_response.message)
        super().__init__(f"API Error {error_response.status_code}: {msg} (Request ID: {error_response.error_code})")


# ---------------------------------------------------------------------------
#  Management API models
# ---------------------------------------------------------------------------
@dataclass
class OrganizationRead:
    id: str
    name: str
    extra: Dict[str, Any] = field(default_factory=dict, repr=False)


@dataclass
class PaginatedOrganizations:
    organizations: List[OrganizationRead] = field(default_factory=list)
    pagination: PaginationInfo = field(default_factory=PaginationInfo)
    extra: Dict[str, Any] = field(default_factory=dict, repr=False)


@dataclass
class ProviderRead:
    id: str
    name: str
    description: str
    short_code: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict, repr=False)


@dataclass
class PaginatedProviders:
    providers: List[ProviderRead] = field(default_factory=list)
    pagination: PaginationInfo = field(default_factory=PaginationInfo)
    extra: Dict[str, Any] = field(default_factory=dict, repr=False)


@dataclass
class BackendClassRead:
    id: str
    name: str
    description: str
    type: str
    provider_id: str
    short_code: Optional[str] = None
    queue_depth: Optional[int] = None
    accepting_jobs: Optional[bool] = None
    status: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict, repr=False)


@dataclass
class PaginatedBackendClasses:
    backend_classes: List[BackendClassRead] = field(default_factory=list)
    pagination: PaginationInfo = field(default_factory=PaginationInfo)
    extra: Dict[str, Any] = field(default_factory=dict, repr=False)


# ---------------------------------------------------------------------------
#  Scheduler API models
# ---------------------------------------------------------------------------
@dataclass
class JobCategoryRead:
    id: str
    name: str
    short_code: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict, repr=False)


@dataclass
class PaginatedJobCategories:
    categories: List[JobCategoryRead] = field(default_factory=list)
    pagination: PaginationInfo = field(default_factory=PaginationInfo)
    extra: Dict[str, Any] = field(default_factory=dict, repr=False)


@dataclass
class JobPreparationCreate:
    organization_id: str
    backend_class_id: str
    name: str
    upload_endpoint_id: str
    job_subcategory_id: str
    shots: int
    configuration_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class JobPreparationUploadResponse:
    id: str
    url: str
    extra: Dict[str, Any] = field(default_factory=dict, repr=False)


@dataclass
class JobPreparationResponse:
    id: str
    extra: Dict[str, Any] = field(default_factory=dict, repr=False)


@dataclass
class QueuePriority:
    name: str
    description: str
    price_increase: int
    queue_priority_id: str
    extra: Dict[str, Any] = field(default_factory=dict, repr=False)


@dataclass
class QuotePlan:
    name: str
    price: int
    description: str
    execution_plan_id: str
    queue_priorities: List[QueuePriority] = field(default_factory=list)
    extra: Dict[str, Any] = field(default_factory=dict, repr=False)


@dataclass
class JobPreparationResultResponse:
    organization_id: str
    backend_class_id: str
    status: str
    name: str
    input_data_url: str
    job_category_id: str
    job_subcategory_id: str
    shots: int
    quote: List[QuotePlan]
    message: Optional[str] = None
    configuration_data: Dict[str, Any] = field(default_factory=dict)
    extra: Dict[str, Any] = field(default_factory=dict, repr=False)


@dataclass
class JobCreate:
    organization_id: str
    job_preparation_id: str
    execution_plan_id: str
    queue_priority_id: str


@dataclass
class JobRead:
    id: str
    status: str
    input_data_url: str
    job_preparation_id: str
    execution_plan_id: str
    queue_priority_id: str
    message: Optional[str] = None
    output_data_url: Optional[str] = None
    transaction_id: Optional[str] = None
    submitted_at: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict, repr=False)


@dataclass
class JobList:
    id: str
    backend_class_id: str
    name: str
    status: str
    backend_name: Optional[str] = None
    output_data_url: Optional[str] = None
    credits_used: Optional[float] = None
    submitted_at: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict, repr=False)


@dataclass
class PaginatedJobs:
    jobs: List[JobList] = field(default_factory=list)
    pagination: PaginationInfo = field(default_factory=PaginationInfo)
    extra: Dict[str, Any] = field(default_factory=dict, repr=False)
