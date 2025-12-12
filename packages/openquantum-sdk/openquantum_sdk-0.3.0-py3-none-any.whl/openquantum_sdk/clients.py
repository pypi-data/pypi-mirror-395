from __future__ import annotations

from dataclasses import dataclass, asdict
import sys
from typing import Optional, Dict, Any, List, Union, Tuple
from urllib.parse import urljoin
import requests

from .enums import AutoChoice, ExecutionPlanType, QueuePriorityType
from .models import (
    APIError,
    BackendClassRead,
    ErrorResponse,
    JobCategoryRead,
    JobCreate,
    JobList,
    JobPreparationCreate,
    JobPreparationResponse,
    JobPreparationResultResponse,
    JobPreparationUploadResponse,
    JobRead,
    OrganizationRead,
    PaginatedBackendClasses,
    PaginatedJobCategories,
    PaginatedJobs,
    PaginatedOrganizations,
    PaginatedProviders,
    PaginationInfo,
    ProviderRead,
    QueuePriority,
    QuotePlan,
)
from .auth import ClientCredentialsAuth
from .utils import poll_for_status


# ---------------------------------------------------------------------------
#  High-level config
# ---------------------------------------------------------------------------
@dataclass
class JobSubmissionConfig:
    """User-facing config for one-call job submission."""

    backend_class_id: str
    name: str
    job_subcategory_id: str
    shots: int
    organization_id: Optional[str] = None
    configuration_data: Optional[Dict[str, Any]] = None

    # User choices
    execution_plan: Union[ExecutionPlanType, AutoChoice] = "auto"
    queue_priority: Union[QueuePriorityType, AutoChoice] = "auto"
    auto_approve_quote: bool = True
    verbose: bool = False  # For CLI/Notebook feedback

    # USER-CONTROLLABLE: How long to wait for job to finish
    job_timeout_seconds: int = 86_400  # 1 day

    # INTERNAL: Fixed preparation timeout and polling
    _preparation_timeout_seconds: int = 300  # 5 minutes
    _preparation_poll_interval: float = 2.0
    _job_poll_interval: float = 5.0


# ---------------------------------------------------------------------------
#  Base Client
# ---------------------------------------------------------------------------
class BaseClient:
    def __init__(
        self,
        base_url: str,
        token: Optional[str] = None,
        auth: Optional[ClientCredentialsAuth] = None,
        session: Optional[requests.Session] = None,
    ):
        if token and auth:
            raise ValueError("Provide either 'token' or 'auth', not both.")
        self.base_url = base_url.rstrip("/")
        self._fixed_token = token
        self._auth = auth
        self.session = session or requests.Session()
        if token:
            self.session.headers.update({"Authorization": f"Bearer {token}"})

    def _authorized_headers(self, extra: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        headers = dict(self.session.headers)
        if self._auth:
            headers = self._auth.apply_auth_header(headers)
        if extra:
            headers.update(extra)
        return headers

    def _do_request(self, method: str, url: str, **kwargs) -> requests.Response:
        return self.session.request(method, url, **kwargs)

    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        url = urljoin(self.base_url + "/", endpoint.lstrip("/"))
        headers = self._authorized_headers(kwargs.pop("headers", None))
        resp = self._do_request(method, url, params=params, json=json, headers=headers, **kwargs)

        if resp.status_code == 401 and self._auth:
            headers = self._auth.apply_auth_header(
                {k: v for k, v in headers.items() if k.lower() != "authorization"}
            )
            resp = self._do_request(method, url, params=params, json=json, headers=headers, **kwargs)

        if resp.status_code >= 400:
            try:
                payload = resp.json()
                if "status_code" in payload and "message" in payload:
                    err = ErrorResponse(
                        status_code=payload.get("status_code", resp.status_code),
                        message=payload.get("message", []),
                        error_code=payload.get("error_code"),
                    )
                    raise APIError(err)
            except ValueError:
                pass
            resp.raise_for_status()

        return {} if resp.status_code == 204 else resp.json()

    def close(self):
        self.session.close()


# ---------------------------------------------------------------------------
#  Management Client
# ---------------------------------------------------------------------------
class ManagementClient(BaseClient):
    def __init__(
        self,
        base_url: str = "https://management.openquantum.com",
        token: Optional[str] = None,
        auth: Optional[ClientCredentialsAuth] = None,
    ):
        super().__init__(base_url, token=token, auth=auth)

    def list_user_organizations(
        self, limit: int = 20, cursor: Optional[str] = None
    ) -> PaginatedOrganizations:
        params = {"limit": limit}
        if cursor:
            params["cursor"] = cursor
        data = self._request("GET", "/v1/users/organizations", params=params)
        orgs = [OrganizationRead(**o) for o in data.get("organizations", [])]
        pagination = PaginationInfo(**data.get("pagination", {}))
        return PaginatedOrganizations(organizations=orgs, pagination=pagination)

    def list_backend_classes(
        self, limit: int = 20, cursor: Optional[str] = None, provider_id: Optional[str] = None
    ) -> PaginatedBackendClasses:
        params = {"limit": limit}
        if cursor:
            params["cursor"] = cursor
        if provider_id:
            params["provider_id"] = provider_id
        data = self._request("GET", "/v1/backends/classes", params=params)
        bcs = [BackendClassRead(**bc) for bc in data.get("backend_classes", [])]
        pagination = PaginationInfo(**data.get("pagination", {}))
        return PaginatedBackendClasses(backend_classes=bcs, pagination=pagination)

    def list_providers(
        self, limit: int = 20, cursor: Optional[str] = None
    ) -> PaginatedProviders:
        params = {"limit": limit}
        if cursor:
            params["cursor"] = cursor
        data = self._request("GET", "/v1/backends/providers", params=params)
        providers = [ProviderRead(**p) for p in data.get("providers", [])]
        pagination = PaginationInfo(**data.get("pagination", {}))
        return PaginatedProviders(providers=providers, pagination=pagination)


# ---------------------------------------------------------------------------
#  Scheduler Client
# ---------------------------------------------------------------------------
class SchedulerClient(BaseClient):
    def __init__(
        self,
        base_url: str = "https://scheduler.openquantum.com",
        token: Optional[str] = None,
        auth: Optional[ClientCredentialsAuth] = None,
        management_client: Optional[ManagementClient] = None,
    ):
        super().__init__(base_url, token=token, auth=auth)
        self.management = management_client or ManagementClient(auth=self._auth)

    def get_job_categories(
        self, limit: int = 20, cursor: Optional[str] = None
    ) -> PaginatedJobCategories:
        params = {"limit": limit}
        if cursor:
            params["cursor"] = cursor
        data = self._request("GET", "/v1/jobs/categories", params=params)
        cats = [JobCategoryRead(**c) for c in data.get("categories", [])]
        pagination = PaginationInfo(**data.get("pagination", {}))
        return PaginatedJobCategories(categories=cats, pagination=pagination)

    def get_job_subcategories(
        self, category_id: str, limit: int = 20, cursor: Optional[str] = None
    ) -> PaginatedJobCategories:
        params = {"limit": limit}
        if cursor:
            params["cursor"] = cursor
        data = self._request(
            "GET", f"/v1/jobs/categories/{category_id}/subcategories", params=params
        )
        cats = [JobCategoryRead(**c) for c in data.get("categories", [])]
        pagination = PaginationInfo(**data.get("pagination", {}))
        return PaginatedJobCategories(categories=cats, pagination=pagination)

    def upload_job_input(
        self, file_content: Optional[bytes] = None, file_path: Optional[str] = None
    ) -> str:
        if (file_content is None) == (file_path is None):
            raise ValueError("Provide exactly one of file_content or file_path.")

        if file_path:
            with open(file_path, "rb") as f:
                data_to_upload = f.read()
        else:
            if isinstance(file_content, str):
                raise TypeError("file_content must be bytes, not str.")
            data_to_upload = file_content

        resp = self._request("POST", "/v1/jobs/upload")
        upload = JobPreparationUploadResponse(**resp)

        put_resp = requests.put(upload.url, data=data_to_upload)
        put_resp.raise_for_status()
        return upload.id

    def download_job_output(self, job: JobRead) -> Any:
        if not job.output_data_url:
            raise RuntimeError(
                f"Job {job.id} has no output_data_url. "
                "It may not be completed yet or produced no output."
            )

        resp = requests.get(job.output_data_url)
        resp.raise_for_status()

        try:
            return resp.json()
        except ValueError as exc:
            raise ValueError(
                f"Failed to parse output of job {job.id} as JSON. "
                "Content may not be JSON or is malformed."
            ) from exc

    def prepare_job(self, preparation: JobPreparationCreate) -> JobPreparationResponse:
        data = self._request("POST", "/v1/jobs/prepare", json=asdict(preparation))
        return JobPreparationResponse(**data)

    def get_preparation_result(self, preparation_id: str) -> JobPreparationResultResponse:
        data = self._request("GET", f"/v1/jobs/prepare/{preparation_id}")

        # --- quote is List[dict] (real objects) ---
        raw_quote = data.get("quote", [])

        quote: List[QuotePlan] = []
        for item in raw_quote:
            if not isinstance(item, dict):
                continue

            try:
                priorities = [
                    QueuePriority(
                        name=q.get("name", "Unknown"),
                        description=q.get("description", ""),
                        price_increase=q.get("price_increase", 0),
                        queue_priority_id=q.get("queue_priority_id", ""),
                    )
                    for q in item.get("queue_priorities", [])
                ]

                quote.append(QuotePlan(
                    name=item.get("name", "Unknown Plan"),
                    price=item.get("price", 0),
                    description=item.get("description", ""),
                    execution_plan_id=item.get("execution_plan_id", ""),
                    queue_priorities=priorities,
                ))
            except Exception as e:
                # Log but don't crash
                print(f"[SDK] Failed to parse quote item: {e}", file=sys.stderr)

        return JobPreparationResultResponse(
            organization_id=data["organization_id"],
            backend_class_id=data["backend_class_id"],
            status=data["status"],
            name=data["name"],
            input_data_url=data["input_data_url"],
            job_category_id=data["job_category_id"],
            job_subcategory_id=data["job_subcategory_id"],
            shots=data["shots"],
            message=data.get("message"),
            quote=quote,
            configuration_data=data.get("configuration_data", {}),
        )

    def create_job(self, job: JobCreate) -> JobRead:
        data = self._request("POST", "/v1/jobs", json=asdict(job))
        return JobRead(**data)

    def get_job(self, job_id: str) -> JobRead:
        data = self._request("GET", f"/v1/jobs/{job_id}")
        return JobRead(**data)

    def cancel_job(self, job_id: str) -> None:
        self._request("DELETE", f"/v1/jobs/{job_id}")

    def list_jobs(
        self,
        organization_id: Optional[str] = None,
        limit: int = 20,
        cursor: Optional[str] = None,
        status: Optional[str] = None,
    ) -> PaginatedJobs:
        org_id = self._resolve_organization_id(organization_id)
        params = {"limit": limit}
        if cursor:
            params["cursor"] = cursor
        if status:
            params["status"] = status
        data = self._request(
            "GET", f"/v1/organizations/{org_id}/jobs", params=params
        )
        jobs = [JobList(**j) for j in data.get("jobs", [])]
        pagination = PaginationInfo(**data.get("pagination", {}))
        return PaginatedJobs(jobs=jobs, pagination=pagination)

    # ---------------------------------------------------------------------------
    #  HIGH-LEVEL: submit_job()
    # ---------------------------------------------------------------------------
    def submit_job(
        self,
        config: JobSubmissionConfig,
        *,
        file_content: Optional[bytes] = None,
        file_path: Optional[str] = None,
    ) -> JobRead:
        # Resolve organization ID
        organization_id = self._resolve_organization_id(config.organization_id)

        if config.verbose:
            print("Step 1/5: Uploading job input...")
        upload_id = self.upload_job_input(file_content=file_content, file_path=file_path)

        prep = JobPreparationCreate(
            organization_id=organization_id,
            backend_class_id=config.backend_class_id,
            name=config.name,
            upload_endpoint_id=upload_id,
            job_subcategory_id=config.job_subcategory_id,
            shots=config.shots,
            configuration_data=config.configuration_data or {},
        )
        if config.verbose:
            print("Step 2/5: Preparing job and fetching quote...")
        prep_resp = self.prepare_job(prep)

        result = self._wait_for_preparation(
            preparation_id=prep_resp.id,
            timeout=config._preparation_timeout_seconds,
            interval=config._preparation_poll_interval,
            verbose=config.verbose,
        )

        if config.verbose:
            print("Step 3/5: Processing quote...")

        # Resolve execution plan + queue priority
        exec_plan_id, queue_prio_id = self._choose_plan_and_priority(result, config)

        # Compute total cost
        total_credits = self._compute_total_cost(result.quote, exec_plan_id, queue_prio_id)

        # Auto-approve if free OR user allowed it
        auto_approve = config.auto_approve_quote or total_credits == 0

        if not auto_approve:
            print(f"\nTotal cost: {total_credits} credit{'s' if total_credits != 1 else ''}")
            self._print_quote(result.quote, exec_plan_id, queue_prio_id)
            if not self._confirm_submission():
                raise RuntimeError("Job submission cancelled by user.")
        elif config.verbose:
            reason = "free" if total_credits == 0 else "auto_approve_quote=True"
            print(f"Step 3/5: Quote approved automatically ({reason})")

        job_create = JobCreate(
            organization_id=organization_id,
            job_preparation_id=prep_resp.id,
            execution_plan_id=exec_plan_id,
            queue_priority_id=queue_prio_id,
        )
        if config.verbose:
            plan = next(p for p in result.quote if p.execution_plan_id == exec_plan_id)
            priority = next(
                q for p in result.quote for q in p.queue_priorities
                if q.queue_priority_id == queue_prio_id
            )
            print(f"Step 4/5: Submitting job ({plan.name} + {priority.name})...")

        job = self.create_job(job_create)

        if config.verbose:
            print(f"Step 5/5: Job '{job.id}' created. Waiting for completion (timeout: {config.job_timeout_seconds}s)...")
        return self._wait_for_job_completion(
            job_id=job.id,
            timeout=config.job_timeout_seconds,
            interval=config._job_poll_interval,
            verbose=config.verbose,
        )

    # ---------------------------------------------------------------------------
    #  Private helpers
    # ---------------------------------------------------------------------------
    def _resolve_organization_id(self, organization_id: Optional[str]) -> str:
        if organization_id:
            return organization_id

        orgs = self.management.list_user_organizations(limit=1)
        if not orgs.organizations:
            raise ValueError("No organizations found for user and none was specified.")

        resolved_id = orgs.organizations[0].id
        return resolved_id

    def _wait_for_preparation(
        self,
        preparation_id: str,
        timeout: int,
        interval: float,
        verbose: bool = False,
    ) -> JobPreparationResultResponse:
        def _status_fn(pid: str) -> Tuple[bool, Optional[JobPreparationResultResponse]]:
            try:
                resp = self.get_preparation_result(pid)
                if verbose:
                    print(f"  > Preparation status: {resp.status}")
                done = resp.status in ("Completed", "Failed")
                return done, resp
            except APIError as e:
                if e.error_response.status_code == 404:
                    if verbose:
                        print("  > Preparation status: Not found (retrying...)")
                    return False, None
                raise

        result = poll_for_status(
            get_status_fn=_status_fn,
            resource_id=preparation_id,
            interval=interval,
            timeout=timeout,
        )
        if result.status == "Failed":
            if result.message:
                raise RuntimeError(f"Job preparation failed: {result.message}")
            error_str = "Unknown preparation error"
            raise RuntimeError(f"Job preparation failed: {error_str}")
        if verbose:
            print("  > Preparation complete.")
        return result

    def _wait_for_job_completion(
        self,
        job_id: str,
        timeout: int,
        interval: float,
        verbose: bool = False,
    ) -> JobRead:
        def _status_fn(jid: str):
            job = self.get_job(jid)
            if verbose:
                print(f"  > Job status: {job.status}")
            done = job.status in ("Completed", "Failed", "Canceled")
            return done, job

        result = poll_for_status(
            get_status_fn=_status_fn,
            resource_id=job_id,
            interval=interval,
            timeout=timeout,
        )
        if result.status in ("Failed", "Canceled"):
            msg = result.message or f"Job finished with status: {result.status}"
            raise RuntimeError(msg)
        if verbose:
            print(f"  > Job finished with status: {result.status}")
        return result

    @staticmethod
    def _print_quote(
        quote: List[QuotePlan],
        selected_plan_id: str,
        selected_priority_id: str,
    ) -> None:
        print("\n=== JOB QUOTE (credits) ===")
        for plan in quote:
            is_selected = plan.execution_plan_id == selected_plan_id
            marker = " (SELECTED)" if is_selected else ""
            print(f" • {plan.name} — Base: {plan.price} credit{'s' if plan.price != 1 else ''}{marker}")
            for qp in plan.queue_priorities:
                total = plan.price + qp.price_increase
                prio_marker = " (SELECTED)" if is_selected and qp.queue_priority_id == selected_priority_id else ""
                print(f"    ├ {qp.name}: +{qp.price_increase} → Total: {total} credit{'s' if total != 1 else ''}{prio_marker}")
            print(f"    └ Plan ID: {plan.execution_plan_id}")
        print("============================\n")

    @staticmethod
    def _confirm_submission() -> bool:
        while True:
            ans = input("Approve and submit? (y/n): ").strip().lower()
            if ans in ("y", "yes"):
                return True
            if ans in ("n", "no"):
                return False

    def _choose_plan_and_priority(
        self,
        result: JobPreparationResultResponse,
        config: JobSubmissionConfig,
    ) -> Tuple[str, str]:
        quote = result.quote
        if not quote:
            raise ValueError("Quote is empty")

        # Choose execution plan
        if config.execution_plan == "auto":
            plan = min(quote, key=lambda p: p.price)
            if config.verbose:
                print(f"  > Auto-selected plan: {plan.name} ({plan.price} credits)")
        else:
            exec_id = config.execution_plan.value
            plan = next((p for p in quote if p.execution_plan_id == exec_id), None)
            if not plan:
                raise ValueError(f"Requested execution plan {exec_id} not available")

        # Choose queue priority
        if config.queue_priority == "auto":
            priority = min(plan.queue_priorities, key=lambda q: q.price_increase)
            if config.verbose:
                print(f"  > Auto-selected priority: {priority.name} (+{priority.price_increase})")
        else:
            prio_id = config.queue_priority.value
            priority = next((q for q in plan.queue_priorities if q.queue_priority_id == prio_id), None)
            if not priority:
                raise ValueError(f"Requested queue priority {prio_id} not available")

        return plan.execution_plan_id, priority.queue_priority_id

    @staticmethod
    def _compute_total_cost(
        quote: List[QuotePlan],
        execution_plan_id: str,
        queue_priority_id: str,
    ) -> int:
        for plan in quote:
            if plan.execution_plan_id != execution_plan_id:
                continue
            base = plan.price
            for qp in plan.queue_priorities:
                if qp.queue_priority_id == queue_priority_id:
                    return base + qp.price_increase
        raise ValueError("Selected plan/priority not found in quote")
