"""Tests for JSearchClient (synchronous client)."""

from typing import Any, Dict

from httpx import Response
import pytest
import respx

from py_jsearch import (
    CompanySalarySearchParams,
    JSearchAuthError,
    JSearchClient,
    JSearchClientError,
    JobDetailsParams,
    JobSalarySearchParams,
    JobSearchParams,
)


@pytest.mark.unit
class TestJSearchClientInit:
    """Test client initialization."""

    def test_init_with_api_key(self, api_key: str) -> None:
        """Test client initialization with API key."""
        client = JSearchClient(access_key=api_key)
        assert client.access_key == api_key
        assert client.base_url == "https://api.openwebninja.com/jsearch"
        assert client._session is None

    def test_init_with_custom_base_url(self, api_key: str) -> None:
        """Test client initialization with custom base URL."""
        custom_url = "https://custom.api.com"
        client = JSearchClient(access_key=api_key, base_url=custom_url)
        assert client.base_url == custom_url

    def test_init_with_timeout(self, api_key: str) -> None:
        """Test client initialization with custom timeout."""
        client = JSearchClient(access_key=api_key, timeout=60.0)
        assert client.timeout == 60.0

    def test_get_headers(self, api_key: str) -> None:
        """Test headers generation."""
        client = JSearchClient(access_key=api_key)
        headers = client.get_headers()

        assert headers["Content-Type"] == "application/json"
        assert headers["Accept"] == "application/json"
        assert headers["Authorization"] == f"Bearer {api_key}"
        assert headers["x-api-key"] == api_key

    def test_session_lazy_initialization(self, api_key: str) -> None:
        """Test session is lazily initialized."""
        client = JSearchClient(access_key=api_key)
        assert client._session is None

        # Access session property
        session = client.session
        assert session is not None
        assert client._session is session

    def test_context_manager(self, api_key: str) -> None:
        """Test context manager usage."""
        with JSearchClient(access_key=api_key) as client:
            assert client.access_key == api_key

        # Session should be closed after context
        if client._session is not None:
            assert client._session.is_closed


@pytest.mark.unit
class TestJSearchClientSearchJobs:
    """Test job search functionality."""

    def test_search_jobs_success(
        self,
        api_key: str,
        base_url: str,
        mock_search_response: Dict[str, Any],
    ):
        """Test successful job search."""
        with respx.mock:
            respx.get(f"{base_url}/search").mock(
                return_value=Response(200, json=mock_search_response)
            )

            with JSearchClient(access_key=api_key) as client:
                params = JobSearchParams(query="python developer")
                jobs = list(client.search_jobs(params))

                assert len(jobs) == 1
                assert jobs[0].job_title == "Senior Python Developer"
                assert jobs[0].employer_name == "Tech Corp"
                assert jobs[0].job_is_remote is True
                assert jobs[0].search_params == params

    def test_search_jobs_with_filters(
        self,
        api_key: str,
        base_url: str,
        mock_search_response: Dict[str, Any],
    ):
        """Test job search with filters."""
        with respx.mock:
            respx.get(f"{base_url}/search").mock(
                return_value=Response(200, json=mock_search_response)
            )

            with JSearchClient(access_key=api_key) as client:
                params = JobSearchParams(
                    query="python developer",
                    page=1,
                    num_pages=2,
                    date_posted="week",
                    work_from_home=True,
                    employment_types=["FULLTIME", "CONTRACTOR"],  # type: ignore[list-item]
                    job_requirements=["under_3_years_experience"],  # type: ignore[list-item]
                    country="us",
                )

                jobs = list(client.search_jobs(params))
                assert len(jobs) >= 0

    def test_search_jobs_empty_results(
        self,
        api_key: str,
        base_url: str,
    ) -> None:
        """Test job search with empty results."""
        empty_response = {
            "status": "OK",
            "request_id": "test-empty",
            "parameters": {"query": "nonexistent job"},
            "data": [],
        }

        with respx.mock:
            respx.get(f"{base_url}/search").mock(
                return_value=Response(200, json=empty_response)
            )

            with JSearchClient(access_key=api_key) as client:
                params = JobSearchParams(query="nonexistent job")
                jobs = list(client.search_jobs(params))
                assert len(jobs) == 0

    def test_search_jobs_invalid_data_format(
        self,
        api_key: str,
        base_url: str,
    ):
        """Test job search with invalid data format."""
        invalid_response = {
            "status": "OK",
            "request_id": "test-invalid",
            "parameters": {},
            "data": "not a list",  # Invalid: should be a list
        }

        with respx.mock:
            respx.get(f"{base_url}/search").mock(
                return_value=Response(200, json=invalid_response)
            )

            with JSearchClient(access_key=api_key) as client:
                params = JobSearchParams(query="test")

                with pytest.raises(JSearchClientError, match="not a list"):
                    list(client.search_jobs(params))


@pytest.mark.unit
class TestJSearchClientGetJob:
    """Test get job details functionality."""

    def test_get_job_success(
        self,
        api_key: str,
        base_url: str,
        mock_job_details_response: Dict[str, Any],
    ):
        """Test successful job details retrieval."""
        with respx.mock:
            respx.get(f"{base_url}/job-details").mock(
                return_value=Response(200, json=mock_job_details_response)
            )

            with JSearchClient(access_key=api_key) as client:
                params = JobDetailsParams(job_id="test_job_123")
                job = client.get_job(params)

                assert job is not None
                assert job.job_id == "test_job_123"
                assert job.job_title == "Senior Python Developer"
                assert job.search_params == params

    def test_get_job_not_found(
        self,
        api_key: str,
        base_url: str,
    ):
        """Test job not found scenario."""
        empty_response = {
            "status": "OK",
            "request_id": "test-not-found",
            "parameters": {"job_id": "nonexistent"},
            "data": [],
        }

        with respx.mock:
            respx.get(f"{base_url}/job-details").mock(
                return_value=Response(200, json=empty_response)
            )

            with JSearchClient(access_key=api_key) as client:
                params = JobDetailsParams(job_id="nonexistent")
                job = client.get_job(params)
                assert job is None

    def test_get_job_with_fields(
        self,
        api_key: str,
        base_url: str,
        mock_job_details_response: Dict[str, Any],
    ):
        """Test job details with field projection."""
        with respx.mock:
            respx.get(f"{base_url}/job-details").mock(
                return_value=Response(200, json=mock_job_details_response)
            )

            with JSearchClient(access_key=api_key) as client:
                params = JobDetailsParams(
                    job_id="test_job_123",
                    fields=["job_title", "employer_name", "job_apply_link"],
                )
                job = client.get_job(params)

                assert job is not None
                assert job.job_title == "Senior Python Developer"


@pytest.mark.unit
class TestJSearchClientGetSalary:
    """Test salary estimation functionality."""

    def test_get_job_salary_success(
        self,
        api_key: str,
        base_url: str,
        mock_salary_response: Dict[str, Any],
    ):
        """Test successful salary retrieval."""
        with respx.mock:
            respx.get(f"{base_url}/estimated-salary").mock(
                return_value=Response(200, json=mock_salary_response)
            )

            with JSearchClient(access_key=api_key) as client:
                params = JobSalarySearchParams(
                    job_title="Python Developer",
                    location="San Francisco",
                )
                salary = client.get_job_salary(params)

                assert salary is not None
                assert salary.job_title == "Python Developer"
                assert salary.location == "San Francisco, CA"
                assert salary.median_salary == 140000.0
                assert salary.salary_currency == "USD"
                assert salary.search_params == params

    def test_get_job_salary_with_filters(
        self,
        api_key: str,
        base_url: str,
        mock_salary_response: Dict[str, Any],
    ):
        """Test salary retrieval with filters."""
        with respx.mock:
            respx.get(f"{base_url}/estimated-salary").mock(
                return_value=Response(200, json=mock_salary_response)
            )

            with JSearchClient(access_key=api_key) as client:
                params = JobSalarySearchParams(
                    job_title="Python Developer",
                    location="San Francisco",
                    location_type="CITY",
                    years_of_experience="FOUR_TO_SIX",
                )
                salary = client.get_job_salary(params)

                assert salary is not None
                assert salary.median_base_salary == 120000.0
                assert salary.median_additional_pay == 20000.0

    def test_get_job_salary_not_found(
        self,
        api_key: str,
        base_url: str,
    ):
        """Test salary not found scenario."""
        empty_response = {
            "status": "OK",
            "request_id": "test-salary-not-found",
            "parameters": {},
            "data": [],
        }

        with respx.mock:
            respx.get(f"{base_url}/estimated-salary").mock(
                return_value=Response(200, json=empty_response)
            )

            with JSearchClient(access_key=api_key) as client:
                params = JobSalarySearchParams(
                    job_title="Nonexistent Job",
                    location="Nowhere",
                )
                salary = client.get_job_salary(params)
                assert salary is None


@pytest.mark.unit
class TestJSearchClientGetCompanySalary:
    """Test company salary functionality."""

    def test_get_company_salary_success(
        self,
        api_key: str,
        base_url: str,
        mock_company_salary_response: Dict[str, Any],
    ):
        """Test successful company salary retrieval."""
        with respx.mock:
            respx.get(f"{base_url}/company-job-salary").mock(
                return_value=Response(200, json=mock_company_salary_response)
            )

            with JSearchClient(access_key=api_key) as client:
                params = CompanySalarySearchParams(
                    company="Google",
                    job_title="Software Engineer",
                )
                salary = client.get_company_salary(params)

                assert salary is not None
                assert salary.company == "Google"
                assert salary.job_title == "Software Engineer"
                assert salary.median_salary == 195000.0
                assert salary.search_params == params

    def test_get_company_salary_with_location(
        self,
        api_key: str,
        base_url: str,
        mock_company_salary_response: Dict[str, Any],
    ):
        """Test company salary with location filter."""
        with respx.mock:
            respx.get(f"{base_url}/company-job-salary").mock(
                return_value=Response(200, json=mock_company_salary_response)
            )

            with JSearchClient(access_key=api_key) as client:
                params = CompanySalarySearchParams(
                    company="Google",
                    job_title="Software Engineer",
                    location="United States",
                    location_type="COUNTRY",
                    years_of_experience="ONE_TO_THREE",
                )
                salary = client.get_company_salary(params)

                assert salary is not None
                assert salary.confidence == "CONFIDENT"
                assert salary.salary_count == 500


@pytest.mark.unit
class TestJSearchClientErrorHandling:
    """Test error handling."""

    def test_auth_error_401(
        self,
        api_key: str,
        base_url: str,
    ):
        """Test 401 authentication error."""
        error_response = {
            "status": "ERROR",
            "request_id": "test-auth-error",
            "parameters": {},
            "data": [],
        }

        with respx.mock:
            respx.get(f"{base_url}/search").mock(
                return_value=Response(401, json=error_response)
            )

            with JSearchClient(access_key="invalid-key") as client:
                params = JobSearchParams(query="test")

                with pytest.raises(JSearchAuthError):
                    list(client.search_jobs(params))

    def test_client_error_500(
        self,
        api_key: str,
        base_url: str,
    ):
        """Test 500 server error."""
        with respx.mock:
            respx.get(f"{base_url}/search").mock(
                return_value=Response(500, json={"error": "Internal Server Error"})
            )

            with JSearchClient(access_key=api_key) as client:
                params = JobSearchParams(query="test")

                with pytest.raises(JSearchClientError):
                    list(client.search_jobs(params))

    def test_invalid_json_response(
        self,
        api_key: str,
        base_url: str,
    ):
        """Test invalid JSON response."""
        with respx.mock:
            respx.get(f"{base_url}/search").mock(
                return_value=Response(200, text="Not JSON")
            )

            with JSearchClient(access_key=api_key) as client:
                params = JobSearchParams(query="test")

                with pytest.raises(Exception):  # JSONDecodeError or similar
                    list(client.search_jobs(params))

    def test_invalid_status_in_response(
        self,
        api_key: str,
        base_url: str,
    ):
        """Test invalid status in response."""
        error_response = {
            "status": "ERROR",
            "request_id": "test-error-status",
            "parameters": {},
            "data": [],
        }

        with respx.mock:
            respx.get(f"{base_url}/search").mock(
                return_value=Response(200, json=error_response)
            )

            with JSearchClient(access_key=api_key) as client:
                params = JobSearchParams(query="test")

                with pytest.raises(JSearchClientError, match="Invalid response status"):
                    list(client.search_jobs(params))


@pytest.mark.unit
class TestJobSearchParams:
    """Test JobSearchParams model."""

    def test_required_query(self) -> None:
        """Test query parameter is required."""
        with pytest.raises(Exception):  # Pydantic validation error
            JobSearchParams()  # type: ignore

    def test_as_query_params(self) -> None:
        """Test conversion to query parameters."""
        params = JobSearchParams(
            query="python developer",
            page=2,
            num_pages=3,
            date_posted="week",
            work_from_home=True,
            employment_types=["FULLTIME", "CONTRACTOR"],  # type: ignore
            job_requirements=["under_3_years_experience"],  # type: ignore
            country="us",
            language="en",
        )

        query_params = params.as_query_params()

        assert query_params["query"] == "python developer"
        assert query_params["page"] == 2
        assert query_params["num_pages"] == 3
        assert query_params["date_posted"] == "week"
        assert query_params["work_from_home"] == "true"
        assert query_params["employment_types"] == "FULLTIME,CONTRACTOR"
        assert query_params["job_requirements"] == "under_3_years_experience"
        assert query_params["country"] == "us"
        assert query_params["language"] == "en"

    def test_exclude_job_publishers(self) -> None:
        """Test exclude_job_publishers parameter."""
        params = JobSearchParams(
            query="test",
            exclude_job_publishers=["Indeed", "ZipRecruiter"],
        )

        query_params = params.as_query_params()
        assert query_params["exclude_job_publishers"] == "Indeed,ZipRecruiter"

    def test_fields_projection(self) -> None:
        """Test fields parameter."""
        params = JobSearchParams(
            query="test",
            fields=["job_title", "employer_name", "job_apply_link"],
        )

        query_params = params.as_query_params()
        assert query_params["fields"] == "job_title,employer_name,job_apply_link"
