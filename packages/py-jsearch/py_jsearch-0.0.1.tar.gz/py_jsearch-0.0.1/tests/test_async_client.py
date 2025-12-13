from typing import Any, Dict

from httpx import Response
import pytest
import respx

from py_jsearch import (
    CompanySalarySearchParams,
    JSearchAsyncClient,
    JSearchAuthError,
    JSearchClientError,
    JobDetailsParams,
    JobSalarySearchParams,
    JobSearchParams,
)


@pytest.mark.async_test
@pytest.mark.unit
class TestJSearchAsyncClientInit:
    """Test async client initialization."""

    async def test_init_with_api_key(self, api_key: str):
        """Test async client initialization with API key."""
        client = JSearchAsyncClient(access_key=api_key)
        assert client.access_key == api_key
        assert client.base_url == "https://api.openwebninja.com/jsearch"
        assert client._session is None
        await client.close()

    async def test_init_with_custom_base_url(self, api_key: str):
        """Test async client initialization with custom base URL."""
        custom_url = "https://custom.api.com"
        client = JSearchAsyncClient(access_key=api_key, base_url=custom_url)
        assert client.base_url == custom_url
        await client.close()

    async def test_context_manager(self, api_key: str):
        """Test async context manager usage."""
        async with JSearchAsyncClient(access_key=api_key) as client:
            assert client.access_key == api_key

        # Session should be closed after context
        if client._session is not None:
            assert client._session.is_closed


@pytest.mark.async_test
@pytest.mark.unit
class TestJSearchAsyncClientSearchJobs:
    """Test async job search functionality."""

    async def test_search_jobs_success(
        self,
        api_key: str,
        base_url: str,
        mock_search_response: Dict[str, Any],
    ):
        """Test successful async job search."""
        with respx.mock:
            respx.get(f"{base_url}/search").mock(
                return_value=Response(200, json=mock_search_response)
            )

            async with JSearchAsyncClient(access_key=api_key) as client:
                params = JobSearchParams(query="python developer")
                jobs_iterator = await client.search_jobs(params)
                jobs = list(jobs_iterator)

                assert len(jobs) == 1
                assert jobs[0].job_title == "Senior Python Developer"
                assert jobs[0].employer_name == "Tech Corp"
                assert jobs[0].job_is_remote is True

    async def test_search_jobs_with_filters(
        self,
        api_key: str,
        base_url: str,
        mock_search_response: Dict[str, Any],
    ):
        """Test async job search with filters."""
        with respx.mock:
            respx.get(f"{base_url}/search").mock(
                return_value=Response(200, json=mock_search_response)
            )

            async with JSearchAsyncClient(access_key=api_key) as client:
                params = JobSearchParams(
                    query="python developer",
                    work_from_home=True,
                    employment_types=["FULLTIME"],  # type: ignore
                    date_posted="week",
                )

                jobs_iterator = await client.search_jobs(params)
                jobs = list(jobs_iterator)
                assert len(jobs) >= 0

    async def test_search_jobs_empty_results(
        self,
        api_key: str,
        base_url: str,
    ):
        """Test async job search with empty results."""
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

            async with JSearchAsyncClient(access_key=api_key) as client:
                params = JobSearchParams(query="nonexistent job")
                jobs_iterator = await client.search_jobs(params)
                jobs = list(jobs_iterator)
                assert len(jobs) == 0


@pytest.mark.async_test
@pytest.mark.unit
class TestJSearchAsyncClientGetJob:
    """Test async get job details functionality."""

    async def test_get_job_success(
        self,
        api_key: str,
        base_url: str,
        mock_job_details_response: Dict[str, Any],
    ):
        """Test successful async job details retrieval."""
        with respx.mock:
            respx.get(f"{base_url}/job-details").mock(
                return_value=Response(200, json=mock_job_details_response)
            )

            async with JSearchAsyncClient(access_key=api_key) as client:
                params = JobDetailsParams(job_id="test_job_123")
                job = await client.get_job(params)

                assert job is not None
                assert job.job_id == "test_job_123"
                assert job.job_title == "Senior Python Developer"

    async def test_get_job_not_found(
        self,
        api_key: str,
        base_url: str,
    ):
        """Test async job not found scenario."""
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

            async with JSearchAsyncClient(access_key=api_key) as client:
                params = JobDetailsParams(job_id="nonexistent")
                job = await client.get_job(params)
                assert job is None


@pytest.mark.async_test
@pytest.mark.unit
class TestJSearchAsyncClientGetSalary:
    """Test async salary estimation functionality."""

    async def test_get_job_salary_success(
        self,
        api_key: str,
        base_url: str,
        mock_salary_response: Dict[str, Any],
    ):
        """Test successful async salary retrieval."""
        with respx.mock:
            respx.get(f"{base_url}/estimated-salary").mock(
                return_value=Response(200, json=mock_salary_response)
            )

            async with JSearchAsyncClient(access_key=api_key) as client:
                params = JobSalarySearchParams(
                    job_title="Python Developer",
                    location="San Francisco",
                )
                salary = await client.get_job_salary(params)

                assert salary is not None
                assert salary.job_title == "Python Developer"
                assert salary.median_salary == 140000.0

    async def test_get_job_salary_with_experience(
        self,
        api_key: str,
        base_url: str,
        mock_salary_response: Dict[str, Any],
    ):
        """Test async salary retrieval with experience filter."""
        with respx.mock:
            respx.get(f"{base_url}/estimated-salary").mock(
                return_value=Response(200, json=mock_salary_response)
            )

            async with JSearchAsyncClient(access_key=api_key) as client:
                params = JobSalarySearchParams(
                    job_title="Python Developer",
                    location="San Francisco",
                    location_type="CITY",
                    years_of_experience="FOUR_TO_SIX",
                )
                salary = await client.get_job_salary(params)

                assert salary is not None


@pytest.mark.async_test
@pytest.mark.unit
class TestJSearchAsyncClientGetCompanySalary:
    """Test async company salary functionality."""

    async def test_get_company_salary_success(
        self,
        api_key: str,
        base_url: str,
        mock_company_salary_response: Dict[str, Any],
    ):
        """Test successful async company salary retrieval."""
        with respx.mock:
            respx.get(f"{base_url}/company-job-salary").mock(
                return_value=Response(200, json=mock_company_salary_response)
            )

            async with JSearchAsyncClient(access_key=api_key) as client:
                params = CompanySalarySearchParams(
                    company="Google",
                    job_title="Software Engineer",
                )
                salary = await client.get_company_salary(params)

                assert salary is not None
                assert salary.company == "Google"
                assert salary.job_title == "Software Engineer"


@pytest.mark.async_test
@pytest.mark.unit
class TestJSearchAsyncClientErrorHandling:
    """Test async error handling."""

    async def test_auth_error_401(
        self,
        api_key: str,
        base_url: str,
    ):
        """Test async 401 authentication error."""
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

            async with JSearchAsyncClient(access_key="invalid-key") as client:
                params = JobSearchParams(query="test")

                with pytest.raises(JSearchAuthError):
                    await client.search_jobs(params)

    async def test_client_error_500(
        self,
        api_key: str,
        base_url: str,
    ):
        """Test async 500 server error."""
        with respx.mock:
            respx.get(f"{base_url}/search").mock(
                return_value=Response(500, json={"error": "Internal Server Error"})
            )

            async with JSearchAsyncClient(access_key=api_key) as client:
                params = JobSearchParams(query="test")

                with pytest.raises(JSearchClientError):
                    await client.search_jobs(params)

    async def test_invalid_status_in_response(
        self,
        api_key: str,
        base_url: str,
    ):
        """Test async invalid status in response."""
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

            async with JSearchAsyncClient(access_key=api_key) as client:
                params = JobSearchParams(query="test")

                with pytest.raises(JSearchClientError, match="Invalid response status"):
                    await client.search_jobs(params)


@pytest.mark.async_test
@pytest.mark.unit
class TestAsyncConcurrentRequests:
    """Test concurrent async requests."""

    async def test_concurrent_searches(
        self,
        api_key: str,
        base_url: str,
        mock_search_response: Dict[str, Any],
    ):
        """Test multiple concurrent job searches."""
        import asyncio

        with respx.mock:
            respx.get(f"{base_url}/search").mock(
                return_value=Response(200, json=mock_search_response)
            )

            async with JSearchAsyncClient(access_key=api_key) as client:
                queries = ["python developer", "data scientist", "devops engineer"]

                tasks = [client.search_jobs(JobSearchParams(query=q)) for q in queries]

                results = await asyncio.gather(*tasks)

                assert len(results) == 3
                for result in results:
                    jobs = list(result)
                    assert len(jobs) >= 0
