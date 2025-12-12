import json
import os
from typing import Any

import requests
from anthropic import Anthropic

from trajectory import Tracer, wrap

# Initialize tracer from environment
trajectory = Tracer(
    api_key=(os.environ.get("TRAJECTORY_API_KEY")),
    organization_id=(os.environ.get("TRAJECTORY_ORG_ID")),
    project_name=os.environ.get("TRAJECTORY_PROJECT", "workday_eval_project"),
    enable_monitoring=True,
    enable_evaluations=False,
    enable_local_tracing=True,  # Required for per-task scoring in evaluations
)

anthropic_client = None
try:
    anthropic_key = os.environ.get("ANTHROPIC_API_KEY")
    if anthropic_key:
        anthropic_client = wrap(Anthropic(api_key=anthropic_key))
except Exception:
    anthropic_client = None


def _base():
    """Get the Workday API base URL (already includes instance_id from base_evaluation)"""
    return os.environ.get("WORKDAY_API_BASE", "http://localhost:8003/test_eval")


@trajectory.observe(span_type="tool")
def wd_get_health() -> dict:
    r = requests.get(f"{_base()}/health", timeout=10)
    r.raise_for_status()
    return (
        r.json()
        if r.headers.get("content-type", "").startswith("application/json")
        else {"text": r.text}
    )


@trajectory.observe(span_type="tool")
def wd_get_metrics() -> str:
    r = requests.get(f"{_base()}/metrics", timeout=10)
    r.raise_for_status()
    return r.text  # usually text/plain


@trajectory.observe(span_type="tool")
def wd_get_worker(worker_id: str) -> dict:
    """Get detailed information about a specific worker by ID"""
    url = f"{_base()}/common/v1/workers/{worker_id}"
    print(f"GETting worker from {url}")
    r = requests.get(url, timeout=10)
    if r.status_code >= 400:
        return {"error": f"API returned {r.status_code}", "detail": r.text}
    return r.json()


@trajectory.observe(span_type="tool")
def wd_list_workers(
    limit: int = 50, offset: int = 0, search: str | None = None
) -> dict:
    """List all workers with optional search filter"""
    params = {"limit": limit, "offset": offset}
    if search:
        params["search"] = search
    url = f"{_base()}/common/v1/workers"
    print(f"GETting workers from {url} with params={params}")
    r = requests.get(url, params=params, timeout=10)
    if r.status_code >= 400:
        return {"error": f"API returned {r.status_code}", "detail": r.text}
    return r.json()


@trajectory.observe(span_type="tool")
def wd_list_currencies(limit: int = 50, offset: int = 0) -> dict:
    """List all available currencies in the system"""
    params = {"limit": limit, "offset": offset}
    url = f"{_base()}/common/v1/currencies"
    print(f"GETting currencies from {url}")
    r = requests.get(url, params=params, timeout=10)
    if r.status_code >= 400:
        return {"error": f"API returned {r.status_code}", "detail": r.text}
    return r.json()


@trajectory.observe(span_type="tool")
def wd_get_currency(currency_id: str) -> dict:
    """Get detailed information about a specific currency"""
    url = f"{_base()}/common/v1/currencies/{currency_id}"
    print(f"GETting currency from {url}")
    r = requests.get(url, timeout=10)
    if r.status_code >= 400:
        return {"error": f"API returned {r.status_code}", "detail": r.text}
    return r.json()


@trajectory.observe(span_type="tool")
def wd_list_job_change_reasons(limit: int = 50, offset: int = 0) -> dict:
    """List all job change reasons (e.g., Promotion, Transfer, etc.)"""
    params = {"limit": limit, "offset": offset}
    url = f"{_base()}/common/v1/jobChangeReasons"
    print(f"GETting job change reasons from {url}")
    r = requests.get(url, params=params, timeout=10)
    if r.status_code >= 400:
        return {"error": f"API returned {r.status_code}", "detail": r.text}
    return r.json()


@trajectory.observe(span_type="tool")
def wd_get_job_change_reason(reason_id: str) -> dict:
    """Get detailed information about a specific job change reason"""
    url = f"{_base()}/common/v1/jobChangeReasons/{reason_id}"
    print(f"GETting job change reason from {url}")
    r = requests.get(url, timeout=10)
    if r.status_code >= 400:
        return {"error": f"API returned {r.status_code}", "detail": r.text}
    return r.json()


@trajectory.observe(span_type="tool")
def wd_list_organizations(
    organization_type: str, limit: int = 50, offset: int = 0
) -> dict:
    """List organizations filtered by type (required parameter)"""
    params = {"organizationType": organization_type, "limit": limit, "offset": offset}
    url = f"{_base()}/common/v1/organizations"
    print(f"GETting organizations from {url} with params={params}")
    r = requests.get(url, params=params, timeout=10)
    if r.status_code >= 400:
        return {"error": f"API returned {r.status_code}", "detail": r.text}
    return r.json()


@trajectory.observe(span_type="tool")
def wd_list_organization_types(limit: int = 50, offset: int = 0) -> dict:
    """List all organization types (e.g., Company, Cost Center, Department)"""
    params = {"limit": limit, "offset": offset}
    url = f"{_base()}/common/v1/organizationTypes"
    print(f"GETting organization types from {url}")
    r = requests.get(url, params=params, timeout=10)
    if r.status_code >= 400:
        return {"error": f"API returned {r.status_code}", "detail": r.text}
    return r.json()


@trajectory.observe(span_type="tool")
def wd_list_supervisory_organizations(limit: int = 50, offset: int = 0) -> dict:
    """List all supervisory organizations (teams with managers)"""
    params = {"limit": limit, "offset": offset}
    url = f"{_base()}/common/v1/supervisoryOrganizations"
    print(f"GETting supervisory orgs from {url}")
    r = requests.get(url, params=params, timeout=10)
    if r.status_code >= 400:
        return {"error": f"API returned {r.status_code}", "detail": r.text}
    return r.json()


@trajectory.observe(span_type="tool")
def wd_get_supervisory_org_workers(
    sup_org_id: str, limit: int = 50, offset: int = 0
) -> dict:
    """Get all workers in a specific supervisory organization"""
    params = {"limit": limit, "offset": offset}
    url = f"{_base()}/common/v1/supervisoryOrganizations/{sup_org_id}/workers"
    print(f"GETting workers from supervisory org {url}")
    r = requests.get(url, params=params, timeout=10)
    if r.status_code >= 400:
        return {"error": f"API returned {r.status_code}", "detail": r.text}
    return r.json()


@trajectory.observe(span_type="tool")
def wd_get_customer_activities(
    customer_id: str,
    from_date: str | None = None,
    to_date: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> dict:
    """Get activities (transactions, invoices, payments) for a specific customer"""
    params = {"limit": limit, "offset": offset}
    if from_date:
        params["fromDate"] = from_date
    if to_date:
        params["toDate"] = to_date
    url = f"{_base()}/common/v1/customers/{customer_id}/activities"
    print(f"GETting customer activities from {url}")
    r = requests.get(url, params=params, timeout=10)
    if r.status_code >= 400:
        return {"error": f"API returned {r.status_code}", "detail": r.text}
    return r.json()


@trajectory.observe(span_type="tool")
def wd_get_time_off_balances(worker_id: str, limit: int = 50, offset: int = 0) -> dict:
    """Get time off balances for a worker (vacation days, PTO, etc.)"""
    params = {"worker": worker_id, "limit": limit, "offset": offset}
    url = f"{_base()}/absenceManagement/v1/balances"
    print(f"GETting time off balances from {url}")
    r = requests.get(url, params=params, timeout=10)
    if r.status_code >= 400:
        return {"error": f"API returned {r.status_code}", "detail": r.text}
    return r.json()


@trajectory.observe(span_type="tool")
def wd_get_eligible_absence_types(
    worker_id: str, limit: int = 50, offset: int = 0
) -> dict:
    """Get absence types a worker is eligible to request (vacation, sick leave, etc.)"""
    params = {"limit": limit, "offset": offset}
    url = f"{_base()}/absenceManagement/v1/workers/{worker_id}/eligibleAbsenceTypes"
    print(f"GETting eligible absence types from {url}")
    r = requests.get(url, params=params, timeout=10)
    if r.status_code >= 400:
        return {"error": f"API returned {r.status_code}", "detail": r.text}
    return r.json()


@trajectory.observe(span_type="tool")
def wd_get_leaves_of_absence(
    worker_id: str,
    from_date: str | None = None,
    to_date: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> dict:
    """Get leaves of absence for a worker (extended leave periods)"""
    params = {"limit": limit, "offset": offset}
    if from_date:
        params["fromDate"] = from_date
    if to_date:
        params["toDate"] = to_date
    url = f"{_base()}/absenceManagement/v1/workers/{worker_id}/leavesOfAbsence"
    print(f"GETting leaves of absence from {url}")
    r = requests.get(url, params=params, timeout=10)
    if r.status_code >= 400:
        return {"error": f"API returned {r.status_code}", "detail": r.text}
    return r.json()


@trajectory.observe(span_type="tool")
def wd_get_worker_pay_slips(worker_id: str, limit: int = 50, offset: int = 0) -> dict:
    """Get pay slips for a worker"""
    params = {"limit": limit, "offset": offset}
    url = f"{_base()}/common/v1/workers/{worker_id}/paySlips"
    print(f"GETting pay slips from {url}")
    r = requests.get(url, params=params, timeout=10)
    if r.status_code >= 400:
        return {"error": f"API returned {r.status_code}", "detail": r.text}
    return r.json()


@trajectory.observe(span_type="function")
def run_agent(prompt: str) -> str:
    """
    Simple agent that routes to different tools based on prompt keywords
    """
    prompt_lower = prompt.lower()

    # Extract worker ID if present
    worker_id = None
    for tok in str(prompt).split():
        # Strip common punctuation
        clean_tok = tok.strip("()[]{},.;:!?\"'")
        if clean_tok.startswith("WID_") or (
            len(clean_tok) == 32 and clean_tok.isalnum()
        ):
            worker_id = clean_tok
            break

    # Route based on keywords in prompt
    if (
        "time off" in prompt_lower
        or "balance" in prompt_lower
        or "vacation" in prompt_lower
        or "pto" in prompt_lower
    ):
        if worker_id:
            result = wd_get_time_off_balances(worker_id)
            return json.dumps(result)
        else:
            return json.dumps({"error": "Worker ID required for time off balances"})

    elif "eligible" in prompt_lower and (
        "absence" in prompt_lower or "leave" in prompt_lower
    ):
        if worker_id:
            result = wd_get_eligible_absence_types(worker_id)
            return json.dumps(result)
        else:
            return json.dumps(
                {"error": "Worker ID required for eligible absence types"}
            )

    elif "leave" in prompt_lower and "absence" in prompt_lower:
        if worker_id:
            result = wd_get_leaves_of_absence(worker_id)
            return json.dumps(result)
        else:
            return json.dumps({"error": "Worker ID required for leaves of absence"})

    elif (
        "pay slip" in prompt_lower
        or "payslip" in prompt_lower
        or "paycheck" in prompt_lower
    ):
        if worker_id:
            result = wd_get_worker_pay_slips(worker_id)
            return json.dumps(result)
        else:
            return json.dumps({"error": "Worker ID required for pay slips"})

    elif "currency" in prompt_lower or "currencies" in prompt_lower:
        if "list" in prompt_lower or "all" in prompt_lower:
            result = wd_list_currencies()
            return json.dumps(result)
        else:
            # Look for currency ID in prompt
            for tok in str(prompt).split():
                if len(tok) == 32 and tok.isalnum():
                    result = wd_get_currency(tok)
                    return json.dumps(result)
            result = wd_list_currencies()
            return json.dumps(result)

    elif "job change reason" in prompt_lower or (
        "reason" in prompt_lower and "job" in prompt_lower
    ):
        result = wd_list_job_change_reasons()
        return json.dumps(result)

    elif "organization type" in prompt_lower:
        result = wd_list_organization_types()
        return json.dumps(result)

    elif "supervisory" in prompt_lower and "organization" in prompt_lower:
        result = wd_list_supervisory_organizations()
        return json.dumps(result)

    elif "leave" in prompt_lower and "absence" in prompt_lower:
        if worker_id:
            result = wd_get_leaves_of_absence(worker_id)
            return json.dumps(result)
        else:
            return json.dumps({"error": "Worker ID required for leaves of absence"})

    elif (
        "pay slip" in prompt_lower
        or "payslip" in prompt_lower
        or "payment history" in prompt_lower
    ):
        if worker_id:
            result = wd_get_worker_pay_slips(worker_id)
            return json.dumps(result)
        else:
            return json.dumps({"error": "Worker ID required for pay slips"})

    elif "eligible" in prompt_lower and (
        "absence" in prompt_lower or "time off" in prompt_lower
    ):
        if worker_id:
            result = wd_get_eligible_absence_types(worker_id)
            return json.dumps(result)
        else:
            return json.dumps(
                {"error": "Worker ID required for eligible absence types"}
            )

    elif (
        "time off balance" in prompt_lower
        or "vacation days" in prompt_lower
        or "sick days" in prompt_lower
    ):
        if worker_id:
            result = wd_get_time_off_balances(worker_id)
            return json.dumps(result)
        else:
            return json.dumps({"error": "Worker ID required for time off balances"})

    elif "worker" in prompt_lower or "employee" in prompt_lower:
        if worker_id:
            result = wd_get_worker(worker_id)
            return json.dumps(result)
        elif "search" in prompt_lower or "find" in prompt_lower:
            # Extract search term (simplified)
            search_term = None
            for word in ["Bob", "Alice", "Carol", "Dave", "Eve"]:
                if word.lower() in prompt_lower:
                    search_term = word
                    break
            result = wd_list_workers(search=search_term)
            return json.dumps(result)
        else:
            result = wd_list_workers()
            return json.dumps(result)

    # Default: check health and list workers
    health = wd_get_health()
    workers = wd_list_workers(limit=5)
    return json.dumps({"health": health, "workers_count": workers.get("total", 0)})


if __name__ == "__main__":
    print(run_agent("GET worker WID_000001"))
