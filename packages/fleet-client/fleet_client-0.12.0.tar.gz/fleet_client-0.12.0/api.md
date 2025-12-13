# Health

Methods:

- <code title="get /health/">client.health.<a href="./src/fleet/resources/health.py">check</a>() -> object</code>

# Workflows

Types:

```python
from fleet.types import WorkflowDescribeResponse, WorkflowResultsResponse
```

Methods:

- <code title="get /workflows/describe/{workflow_id}">client.workflows.<a href="./src/fleet/resources/workflows/workflows.py">describe</a>(workflow_id) -> <a href="./src/fleet/types/workflow_describe_response.py">WorkflowDescribeResponse</a></code>
- <code title="get /workflows/results/{workflow_id}">client.workflows.<a href="./src/fleet/resources/workflows/workflows.py">results</a>(workflow_id) -> <a href="./src/fleet/types/workflow_results_response.py">WorkflowResultsResponse</a></code>

## Request

Types:

```python
from fleet.types.workflows import SearchEngine, WaitUntil, RequestCreateResponse
```

Methods:

- <code title="post /workflows/request/scrape">client.workflows.request.<a href="./src/fleet/resources/workflows/request/request.py">create</a>(\*\*<a href="src/fleet/types/workflows/request_create_params.py">params</a>) -> <a href="./src/fleet/types/workflows/request_create_response.py">RequestCreateResponse</a></code>
- <code title="post /workflows/request/business-owner">client.workflows.request.<a href="./src/fleet/resources/workflows/request/request.py">create_business_owner</a>(\*\*<a href="src/fleet/types/workflows/request_create_business_owner_params.py">params</a>) -> <a href="./src/fleet/types/workflows/request/workflow_result_with_message.py">WorkflowResultWithMessage</a></code>
- <code title="post /workflows/request/personal-email">client.workflows.request.<a href="./src/fleet/resources/workflows/request/request.py">create_personal_email_request</a>(\*\*<a href="src/fleet/types/workflows/request_create_personal_email_request_params.py">params</a>) -> <a href="./src/fleet/types/workflows/request/workflow_result_with_message.py">WorkflowResultWithMessage</a></code>

### Mass

Types:

```python
from fleet.types.workflows.request import WorkflowResultWithMessage
```

Methods:

- <code title="post /workflows/request/mass/company-scrape">client.workflows.request.mass.<a href="./src/fleet/resources/workflows/request/mass.py">create_company_scrape</a>(\*\*<a href="src/fleet/types/workflows/request/mass_create_company_scrape_params.py">params</a>) -> <a href="./src/fleet/types/workflows/request/workflow_result_with_message.py">WorkflowResultWithMessage</a></code>
- <code title="post /workflows/request/mass/link-extraction">client.workflows.request.mass.<a href="./src/fleet/resources/workflows/request/mass.py">create_link_extraction</a>(\*\*<a href="src/fleet/types/workflows/request/mass_create_link_extraction_params.py">params</a>) -> <a href="./src/fleet/types/workflows/request/workflow_result_with_message.py">WorkflowResultWithMessage</a></code>

# Vnc

Methods:

- <code title="get /vnc/health">client.vnc.<a href="./src/fleet/resources/vnc/vnc.py">check_health</a>() -> object</code>

## Sessions

Types:

```python
from fleet.types.vnc import VncSession, SessionRetrieveResponse, SessionListResponse
```

Methods:

- <code title="get /vnc/sessions/{browser_id}">client.vnc.sessions.<a href="./src/fleet/resources/vnc/sessions.py">retrieve</a>(browser_id) -> <a href="./src/fleet/types/vnc/session_retrieve_response.py">SessionRetrieveResponse</a></code>
- <code title="get /vnc/sessions">client.vnc.sessions.<a href="./src/fleet/resources/vnc/sessions.py">list</a>(\*\*<a href="src/fleet/types/vnc/session_list_params.py">params</a>) -> <a href="./src/fleet/types/vnc/session_list_response.py">SessionListResponse</a></code>
- <code title="get /vnc/sessions/{browser_id}/raw">client.vnc.sessions.<a href="./src/fleet/resources/vnc/sessions.py">retrieve_raw</a>(browser_id) -> <a href="./src/fleet/types/vnc/vnc_session.py">VncSession</a></code>

## Discovery

Methods:

- <code title="post /vnc/discovery/trigger">client.vnc.discovery.<a href="./src/fleet/resources/vnc/discovery.py">trigger</a>() -> object</code>

# Sessions

Types:

```python
from fleet.types import (
    BrowserConfiguration,
    SessionParameters,
    SessionCreateResponse,
    SessionRetrieveResponse,
    SessionListResponse,
    SessionDeleteResponse,
    SessionVisitPageResponse,
    SessionWarmUpResponse,
)
```

Methods:

- <code title="post /sessions/">client.sessions.<a href="./src/fleet/resources/sessions/sessions.py">create</a>(\*\*<a href="src/fleet/types/session_create_params.py">params</a>) -> <a href="./src/fleet/types/session_create_response.py">SessionCreateResponse</a></code>
- <code title="get /sessions/{session_id}">client.sessions.<a href="./src/fleet/resources/sessions/sessions.py">retrieve</a>(session_id) -> <a href="./src/fleet/types/session_retrieve_response.py">SessionRetrieveResponse</a></code>
- <code title="get /sessions/">client.sessions.<a href="./src/fleet/resources/sessions/sessions.py">list</a>() -> <a href="./src/fleet/types/session_list_response.py">SessionListResponse</a></code>
- <code title="delete /sessions/{session_id}">client.sessions.<a href="./src/fleet/resources/sessions/sessions.py">delete</a>(session_id) -> <a href="./src/fleet/types/session_delete_response.py">SessionDeleteResponse</a></code>
- <code title="post /sessions/{session_id}/visit">client.sessions.<a href="./src/fleet/resources/sessions/sessions.py">visit_page</a>(session_id, \*\*<a href="src/fleet/types/session_visit_page_params.py">params</a>) -> <a href="./src/fleet/types/session_visit_page_response.py">SessionVisitPageResponse</a></code>
- <code title="post /sessions/warm-up">client.sessions.<a href="./src/fleet/resources/sessions/sessions.py">warm_up</a>() -> <a href="./src/fleet/types/session_warm_up_response.py">SessionWarmUpResponse</a></code>

## Start

Types:

```python
from fleet.types.sessions import StartExistingResponse, StartNewResponse
```

Methods:

- <code title="post /sessions/{session_id}/start">client.sessions.start.<a href="./src/fleet/resources/sessions/start.py">existing</a>(session_id, \*\*<a href="src/fleet/types/sessions/start_existing_params.py">params</a>) -> <a href="./src/fleet/types/sessions/start_existing_response.py">StartExistingResponse</a></code>
- <code title="post /sessions/start">client.sessions.start.<a href="./src/fleet/resources/sessions/start.py">new</a>(\*\*<a href="src/fleet/types/sessions/start_new_params.py">params</a>) -> <a href="./src/fleet/types/sessions/start_new_response.py">StartNewResponse</a></code>

## Page

Types:

```python
from fleet.types.sessions import PageGetResponse, PageGetFullResponse, PageGetTextResponse
```

Methods:

- <code title="get /sessions/{session_id}/page">client.sessions.page.<a href="./src/fleet/resources/sessions/page.py">get</a>(session_id) -> <a href="./src/fleet/types/sessions/page_get_response.py">PageGetResponse</a></code>
- <code title="get /sessions/{session_id}/page/full">client.sessions.page.<a href="./src/fleet/resources/sessions/page.py">get_full</a>(session_id) -> <a href="./src/fleet/types/sessions/page_get_full_response.py">PageGetFullResponse</a></code>
- <code title="get /sessions/{session_id}/page/text">client.sessions.page.<a href="./src/fleet/resources/sessions/page.py">get_text</a>(session_id) -> <a href="./src/fleet/types/sessions/page_get_text_response.py">PageGetTextResponse</a></code>

## Responses

Types:

```python
from fleet.types.sessions import (
    ResponseListResponse,
    ResponseClearResponse,
    ResponseGetFilteredResponse,
    ResponseGetLatestResponse,
    ResponseGetSummaryResponse,
    ResponseToggleTrackingResponse,
)
```

Methods:

- <code title="get /sessions/{session_id}/responses">client.sessions.responses.<a href="./src/fleet/resources/sessions/responses.py">list</a>(session_id) -> <a href="./src/fleet/types/sessions/response_list_response.py">ResponseListResponse</a></code>
- <code title="delete /sessions/{session_id}/responses">client.sessions.responses.<a href="./src/fleet/resources/sessions/responses.py">clear</a>(session_id) -> <a href="./src/fleet/types/sessions/response_clear_response.py">ResponseClearResponse</a></code>
- <code title="get /sessions/{session_id}/responses/filter">client.sessions.responses.<a href="./src/fleet/resources/sessions/responses.py">get_filtered</a>(session_id, \*\*<a href="src/fleet/types/sessions/response_get_filtered_params.py">params</a>) -> <a href="./src/fleet/types/sessions/response_get_filtered_response.py">ResponseGetFilteredResponse</a></code>
- <code title="get /sessions/{session_id}/responses/latest">client.sessions.responses.<a href="./src/fleet/resources/sessions/responses.py">get_latest</a>(session_id) -> <a href="./src/fleet/types/sessions/response_get_latest_response.py">ResponseGetLatestResponse</a></code>
- <code title="get /sessions/{session_id}/responses/summary">client.sessions.responses.<a href="./src/fleet/resources/sessions/responses.py">get_summary</a>(session_id) -> <a href="./src/fleet/types/sessions/response_get_summary_response.py">ResponseGetSummaryResponse</a></code>
- <code title="post /sessions/{session_id}/responses/toggle">client.sessions.responses.<a href="./src/fleet/resources/sessions/responses.py">toggle_tracking</a>(session_id, \*\*<a href="src/fleet/types/sessions/response_toggle_tracking_params.py">params</a>) -> <a href="./src/fleet/types/sessions/response_toggle_tracking_response.py">ResponseToggleTrackingResponse</a></code>

## Scrape

Types:

```python
from fleet.types.sessions import (
    BrowserSelectionStrategy,
    VisitRequest,
    ScrapeCleanupJobsResponse,
    ScrapeGetBrowserStatsResponse,
)
```

Methods:

- <code title="post /sessions/{session_id}/scrape/cleanup">client.sessions.scrape.<a href="./src/fleet/resources/sessions/scrape/scrape.py">cleanup_jobs</a>(session_id, \*\*<a href="src/fleet/types/sessions/scrape_cleanup_jobs_params.py">params</a>) -> <a href="./src/fleet/types/sessions/scrape_cleanup_jobs_response.py">ScrapeCleanupJobsResponse</a></code>
- <code title="get /sessions/{session_id}/scrape/browser-stats">client.sessions.scrape.<a href="./src/fleet/resources/sessions/scrape/scrape.py">get_browser_stats</a>(session_id) -> <a href="./src/fleet/types/sessions/scrape_get_browser_stats_response.py">ScrapeGetBrowserStatsResponse</a></code>
- <code title="post /sessions/{session_id}/scrape">client.sessions.scrape.<a href="./src/fleet/resources/sessions/scrape/scrape.py">page</a>(session_id, \*\*<a href="src/fleet/types/sessions/scrape_page_params.py">params</a>) -> object</code>

### Async

Types:

```python
from fleet.types.sessions.scrape import (
    JobStatus,
    AsyncCreateJobResponse,
    AsyncDeleteJobResponse,
    AsyncGetJobStatusResponse,
    AsyncListJobsResponse,
)
```

Methods:

- <code title="post /sessions/{session_id}/scrape/async">client.sessions.scrape.async*.<a href="./src/fleet/resources/sessions/scrape/async*.py">create_job</a>(session_id, \*\*<a href="src/fleet/types/sessions/scrape/async_create_job_params.py">params</a>) -> <a href="./src/fleet/types/sessions/scrape/async_create_job_response.py">AsyncCreateJobResponse</a></code>
- <code title="delete /sessions/{session_id}/scrape/async/{job_id}">client.sessions.scrape.async*.<a href="./src/fleet/resources/sessions/scrape/async*.py">delete_job</a>(job_id, \*, session_id) -> <a href="./src/fleet/types/sessions/scrape/async_delete_job_response.py">AsyncDeleteJobResponse</a></code>
- <code title="get /sessions/{session_id}/scrape/async/{job_id}">client.sessions.scrape.async*.<a href="./src/fleet/resources/sessions/scrape/async*.py">get_job_status</a>(job_id, \*, session_id) -> <a href="./src/fleet/types/sessions/scrape/async_get_job_status_response.py">AsyncGetJobStatusResponse</a></code>
- <code title="get /sessions/{session_id}/scrape/async">client.sessions.scrape.async*.<a href="./src/fleet/resources/sessions/scrape/async*.py">list_jobs</a>(session_id) -> <a href="./src/fleet/types/sessions/scrape/async_list_jobs_response.py">AsyncListJobsResponse</a></code>

### BrowserStrategy

Types:

```python
from fleet.types.sessions.scrape import Response
```

Methods:

- <code title="get /sessions/{session_id}/scrape/browser-strategy">client.sessions.scrape.browser_strategy.<a href="./src/fleet/resources/sessions/scrape/browser_strategy.py">get</a>(session_id) -> <a href="./src/fleet/types/sessions/scrape/response.py">Response</a></code>
- <code title="post /sessions/{session_id}/scrape/browser-strategy">client.sessions.scrape.browser_strategy.<a href="./src/fleet/resources/sessions/scrape/browser_strategy.py">set</a>(session_id, \*\*<a href="src/fleet/types/sessions/scrape/browser_strategy_set_params.py">params</a>) -> <a href="./src/fleet/types/sessions/scrape/response.py">Response</a></code>
