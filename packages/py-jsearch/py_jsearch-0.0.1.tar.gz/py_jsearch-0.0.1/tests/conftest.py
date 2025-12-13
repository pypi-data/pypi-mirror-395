import typing

from httpx import Response
import pytest
import respx

from py_jsearch import JSearchAsyncClient, JSearchClient


@pytest.fixture
def api_key() -> str:
    """Return a test API key."""
    return "test_api_key_12345"


@pytest.fixture
def base_url() -> str:
    """Return the API base URL."""
    return "https://api.openwebninja.com/jsearch"


@pytest.fixture
def jsearch_client(api_key: str) -> JSearchClient:
    """Create a synchronous JSearch client for testing."""
    return JSearchClient(access_key=api_key)


@pytest.fixture
def jsearch_async_client(api_key: str) -> JSearchAsyncClient:
    """Create an async JSearch client for testing."""
    return JSearchAsyncClient(access_key=api_key)


@pytest.fixture
def sample_job_data() -> typing.Dict[str, typing.Any]:
    """Sample job data for testing."""
    return {
        "job_id": "test_job_123",
        "job_title": "Senior Python Developer",
        "employer_name": "Tech Corp",
        "employer_logo": "https://example.com/logo.png",
        "employer_website": "https://techcorp.com",
        "employer_company_type": "Technology",
        "job_publisher": "LinkedIn",
        "job_employment_type": "Full-time",
        "job_employment_types": ["FULLTIME"],
        "job_apply_link": "https://example.com/apply",
        "job_apply_is_direct": False,
        "apply_options": [
            {
                "publisher": "LinkedIn",
                "apply_link": "https://linkedin.com/apply",
                "is_direct": False,
            },
            {
                "publisher": "Indeed",
                "apply_link": "https://indeed.com/apply",
                "is_direct": True,
            },
        ],
        "job_apply_quality_score": 0.85,
        "job_description": "We are looking for a senior Python developer...",
        "job_is_remote": True,
        "job_posted_at": "2 days ago",
        "job_posted_at_timestamp": 1701388800,
        "job_posted_at_datetime_utc": "2023-12-01T00:00:00.000Z",
        "job_location": "San Francisco, CA",
        "job_city": "San Francisco",
        "job_state": "California",
        "job_country": "US",
        "job_latitude": 37.7749,
        "job_longitude": -122.4194,
        "job_benefits": ["health_insurance", "dental_coverage", "paid_time_off"],
        "job_google_link": "https://www.google.com/search?q=jobs",
        "job_offer_expiration_datetime_utc": "2024-01-01T00:00:00.000Z",
        "job_offer_expiration_timestamp": 1704067200,
        "job_required_experience": {
            "no_experience_required": False,
            "required_experience_in_months": 60,
            "experience_mentioned": True,
            "experience_preferred": True,
        },
        "job_required_skills": ["Python", "Django", "REST APIs"],
        "job_required_education": {
            "postgraduate_degree": False,
            "professional_certification": False,
            "high_school": False,
            "associates_degree": False,
            "bachelors_degree": True,
            "degree_mentioned": True,
            "degree_preferred": True,
            "professional_certification_mentioned": False,
        },
        "job_experience_in_place_of_education": True,
        "job_salary": None,
        "job_min_salary": 120000.0,
        "job_max_salary": 180000.0,
        "job_salary_currency": "USD",
        "job_salary_period": "YEAR",
        "job_highlights": {
            "Qualifications": [
                "5+ years of Python experience",
                "Strong knowledge of Django",
            ],
            "Responsibilities": [
                "Design and implement backend services",
                "Collaborate with frontend team",
            ],
            "Benefits": [
                "Competitive salary",
                "Health insurance",
                "401k matching",
            ],
        },
        "job_job_title": None,
        "job_posting_language": "en",
        "job_onet_soc": "15113200",
        "job_onet_job_zone": "4",
        "job_occupational_categories": ["15-1132.00"],
    }


@pytest.fixture
def mock_search_response(
    sample_job_data: typing.Dict[str, typing.Any],
) -> typing.Dict[str, typing.Any]:
    """Sample job search API response."""
    return {
        "status": "OK",
        "request_id": "test-request-123",
        "parameters": {
            "query": "python developer",
            "page": 1,
            "num_pages": 1,
            "date_posted": "all",
            "country": "us",
            "language": "en",
        },
        "data": [sample_job_data],
    }


@pytest.fixture
def mock_job_details_response(
    sample_job_data: typing.Dict[str, typing.Any],
) -> typing.Dict[str, typing.Any]:
    """Sample job details API response."""
    return {
        "status": "OK",
        "request_id": "test-request-456",
        "parameters": {"job_id": "test_job_123", "country": "us"},
        "data": [sample_job_data],
    }


@pytest.fixture
def mock_salary_data() -> typing.Dict[str, typing.Any]:
    """Sample salary data for testing."""
    return {
        "location": "San Francisco, CA",
        "job_title": "Python Developer",
        "publisher_name": "Glassdoor",
        "publisher_link": "https://glassdoor.com/salaries",
        "min_salary": 100000.0,
        "max_salary": 180000.0,
        "median_salary": 140000.0,
        "min_base_salary": 90000.0,
        "max_base_salary": 150000.0,
        "median_base_salary": 120000.0,
        "min_additional_pay": 10000.0,
        "max_additional_pay": 30000.0,
        "median_additional_pay": 20000.0,
        "salary_period": "YEAR",
        "salary_currency": "USD",
        "salary_count": 250,
        "salaries_updated_at": "2023-12-01T00:00:00.000Z",
        "confidence": "CONFIDENT",
    }


@pytest.fixture
def mock_salary_response(
    mock_salary_data: typing.Dict[str, typing.Any],
) -> typing.Dict[str, typing.Any]:
    """Sample salary API response."""
    return {
        "status": "OK",
        "request_id": "test-request-789",
        "parameters": {
            "job_title": "Python Developer",
            "location": "San Francisco",
            "location_type": "CITY",
            "years_of_experience": "ALL",
        },
        "data": [mock_salary_data],
    }


@pytest.fixture
def mock_company_salary_data() -> typing.Dict[str, typing.Any]:
    """Sample company salary data for testing."""
    return {
        "location": "United States",
        "job_title": "Software Engineer",
        "company": "Google",
        "min_salary": 140000.0,
        "max_salary": 250000.0,
        "median_salary": 195000.0,
        "min_base_salary": 120000.0,
        "max_base_salary": 200000.0,
        "median_base_salary": 160000.0,
        "min_additional_pay": 20000.0,
        "max_additional_pay": 50000.0,
        "median_additional_pay": 35000.0,
        "salary_period": "YEAR",
        "salary_currency": "USD",
        "confidence": "CONFIDENT",
        "salary_count": 500,
    }


@pytest.fixture
def mock_company_salary_response(
    mock_company_salary_data: typing.Dict[str, typing.Any],
) -> typing.Dict[str, typing.Any]:
    """Sample company salary API response."""
    return {
        "status": "OK",
        "request_id": "test-request-012",
        "parameters": {
            "company": "Google",
            "job_title": "Software Engineer",
            "location": "United States",
            "location_type": "COUNTRY",
            "years_of_experience": "ALL",
        },
        "data": [mock_company_salary_data],
    }


@pytest.fixture
def mock_error_response() -> typing.Dict[str, typing.Any]:
    """Sample error API response."""
    return {
        "status": "ERROR",
        "request_id": "test-request-error",
        "parameters": {},
        "data": [],
    }


@pytest.fixture
def mock_respx_router(
    mock_search_response: typing.Dict[str, typing.Any],
    mock_job_details_response: typing.Dict[str, typing.Any],
    mock_salary_response: typing.Dict[str, typing.Any],
    mock_company_salary_response: typing.Dict[str, typing.Any],
    base_url: str,
) -> respx.MockRouter:
    """Configure respx router with mock responses."""
    router = respx.mock(assert_all_called=False)

    # Mock job search endpoint
    router.get(f"{base_url}/search").mock(
        return_value=Response(200, json=mock_search_response)
    )
    # Mock job details endpoint
    router.get(f"{base_url}/job-details").mock(
        return_value=Response(200, json=mock_job_details_response)
    )
    # Mock salary endpoint
    router.get(f"{base_url}/estimated-salary").mock(
        return_value=Response(200, json=mock_salary_response)
    )
    # Mock company salary endpoint
    router.get(f"{base_url}/company-job-salary").mock(
        return_value=Response(200, json=mock_company_salary_response)
    )
    return router


@pytest.fixture
def mock_auth_error_router(base_url: str) -> respx.MockRouter:
    """Configure respx router with auth error responses."""
    router = respx.mock(assert_all_called=False)

    error_response = {
        "status": "ERROR",
        "request_id": "test-request-auth-error",
        "parameters": {},
        "data": [],
    }
    router.get(f"{base_url}/search").mock(
        return_value=Response(401, json=error_response)
    )
    return router


# Aliases for backward compatibility
@pytest.fixture
def sample_salary_data(
    mock_salary_data: typing.Dict[str, typing.Any],
) -> typing.Dict[str, typing.Any]:
    """Alias for mock_salary_data."""
    return mock_salary_data


@pytest.fixture
def sample_company_salary_data(
    mock_company_salary_data: typing.Dict[str, typing.Any],
) -> typing.Dict[str, typing.Any]:
    """Alias for mock_company_salary_data."""
    return mock_company_salary_data
