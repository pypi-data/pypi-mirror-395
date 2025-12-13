import asyncio
import json
import logging
import time
import typing
import warnings

import httpx

from py_jsearch._types import (
    APIResponse,
    CompanySalaryInfo,
    CompanySalarySearchParams,
    DataT,
    Job,
    JobDetailsParams,
    JobSalaryInfo,
    JobSalarySearchParams,
    JobSearchParams,
)
from py_jsearch.errors import JSearchAuthError, JSearchClientError, JSearchResponseError

logger = logging.getLogger(__name__)

__all__ = ["JSearchAsyncClient", "JSearchClient"]


class JSearchAsyncClient:
    """Asynchronous client for interacting with the JSearch API."""

    base_url = "https://api.openwebninja.com/jsearch"
    """Default base URL for the JSearch API."""
    url_paths = {
        "search_jobs": "/search",
        "get_job": "/job-details",
        "get_job_salary": "/estimated-salary",
        "get_company_salary": "/company-job-salary",
    }

    def __init__(
        self,
        access_key: str,
        base_url: typing.Optional[str] = None,
        timeout: typing.Union[float, httpx.Timeout] = 30.0,
    ):
        """
        Initialize the client with access key.

        :param access_key: Your JSearch API access key.
        :param base_url: Optional base URL for the API (defaults to JSearch API URL).
        """
        self.access_key = access_key
        self.base_url = base_url or self.base_url
        self._session: typing.Optional[httpx.AsyncClient] = None
        self.timeout = timeout
        logger.debug(
            f"Initialized {self.__class__.__name__} with base URL: {self.base_url}"
        )

    @property
    def session(self) -> httpx.AsyncClient:
        """Get or create the HTTP client session."""
        if self._session is None:
            logger.debug("Creating new HTTP session for JSearch client")
            self._session = httpx.AsyncClient(
                base_url=self.base_url,
                headers=self.get_headers(),
                timeout=self.timeout,
            )
        return self._session

    def get_headers(self) -> typing.Dict[str, str]:
        """Get the headers for the API requests."""
        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.access_key}",
            "x-api-key": self.access_key,
        }

    @typing.overload
    async def _call(
        self,
        url: str,
        params: typing.Dict[str, typing.Any],
        data_model: typing.Type[DataT],
        **kwargs: typing.Any,
    ) -> APIResponse[DataT]: ...

    @typing.overload
    async def _call(
        self,
        url: str,
        params: typing.Dict[str, typing.Any],
        data_model: None = None,
        **kwargs: typing.Any,
    ) -> APIResponse[typing.Any]: ...

    async def _call(
        self,
        url: str,
        params: typing.Dict[str, typing.Any],
        data_model: typing.Optional[typing.Type[DataT]] = None,
        _method: str = "GET",
        **kwargs: typing.Any,
    ) -> typing.Union[APIResponse[DataT], APIResponse]:
        """
        Make an API call to the JSearch API.

        :param url: The endpoint URL (relative to base_url).
        :param params: Query parameters for the request.
        :param data_model: Pydantic model class to parse the 'data' field of the response.
        :param kwargs: Additional arguments to pass to httpx.AsyncClient.get().
        :return: An APIResponse instance containing the API response data.
        """
        logger.debug(f"Making {_method} request to {url} with {len(params)} parameters")
        start_time = asyncio.get_event_loop().time()

        if data_model is None:
            data_model = typing.cast(typing.Type[DataT], typing.Any)

        response_model = self.get_response_model(data_model)
        try:
            response = await self.session.request(
                _method, url=url, params=params, **kwargs
            )
            elapsed_time = asyncio.get_event_loop().time() - start_time
            code = response.status_code

            logger.debug(f"API response: {code} in {elapsed_time:.3f}s")

            if code != 200:
                logger.warning(f"API request failed with status {code}")
                try:
                    error_data = response.json()
                    logger.info(f"Error response JSON: {error_data}")
                    api_response = response_model.model_validate(error_data)
                    logger.error(
                        f"JSearch API error: {api_response.status} - Request ID: {api_response.request_id}"
                    )
                except json.JSONDecodeError as exc:
                    logger.error(
                        f"Failed to decode error response JSON: {exc}",
                        exc_info=True,
                    )
                    api_response = None
                except Exception as exc:
                    logger.error(
                        f"Failed to parse error response: {exc}", exc_info=True
                    )
                    api_response = None

                if code in (401, 403):
                    logger.error("Authentication error: Invalid access key")
                    raise JSearchAuthError(code=code, response=api_response)
                raise JSearchClientError(code=code, response=api_response)

            try:
                response_data = response.json()
                logger.debug(f"API response JSON: {response_data}")
                model_name = getattr(data_model, "__name__", str(data_model))
                logger.debug(f"Parsing response into `APIResponse[{model_name}]`")
                api_response = response_model.model_validate(response_data)

                # Check status after parsing
                if api_response.status.lower() != "ok":
                    logger.error(f"API response status not OK: {api_response.status}")
                    raise JSearchClientError(
                        f"Invalid response status: {api_response.status}",
                        response=api_response,
                        code=code,
                    )

                return api_response
            except Exception as exc:
                logger.error(f"Failed to parse API response: {exc}", exc_info=True)
                raise JSearchResponseError(f"Failed to parse response: {exc}") from exc

        except Exception as exc:
            elapsed_time = asyncio.get_event_loop().time() - start_time
            logger.error(
                f"API request failed after {elapsed_time:.3f}s: {type(exc).__name__}: {exc}"
            )
            raise

    def get_response_model(
        self, data_model: typing.Type[DataT]
    ) -> typing.Type[APIResponse[DataT]]:
        """Get a parameterized `APIResponse` model for the given data model."""
        return typing.cast(typing.Type[APIResponse[DataT]], APIResponse[data_model])  # type: ignore

    async def close(self):
        """Close the underlying HTTP session."""
        if self._session is not None:
            logger.debug("Closing HTTP session")
            await self._session.aclose()
            self._session = None
            logger.debug("HTTP session closed successfully")

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    def __del__(self):
        if self._session is not None and not self._session.is_closed:
            logger.warning("client session not properly closed")
            warnings.warn(
                "Unclosed client session. Please use 'async with' or call 'await close()' to close the session properly.",
                ResourceWarning,
            )
            try:
                loop = asyncio.get_running_loop()
                loop.create_task(self.close())
            except RuntimeError:
                pass

    async def search_jobs(
        self, params: JobSearchParams
    ) -> typing.Iterator[Job[JobSearchParams]]:
        """
        Search for jobs using the JSearch API.

        :param params: `JobSearchParams` object containing search parameters.
        :return: An iterator of Job objects matching the search criteria.
        """
        url = type(self).url_paths["search_jobs"]
        query_params = params.as_query_params()
        logger.debug(f"Searching jobs using url: {url} with params: {query_params}")

        result = await self._call(
            url, params=query_params, data_model=typing.Dict[str, typing.Any]
        )

        raw_jobs = result.data
        if not isinstance(raw_jobs, list):
            logger.error("API response 'data' field is not a list")
            raise JSearchClientError("Invalid response format: 'data' is not a list")

        def _jobs_gen(
            jobs: typing.List[typing.Dict[str, typing.Any]],
        ) -> typing.Iterator[Job[JobSearchParams]]:
            for raw_job in jobs:
                try:
                    # Attach search params to each job for reference
                    raw_job["search_params"] = params
                    yield Job.model_validate(raw_job)
                except Exception as exc:
                    logger.warning(f"Failed to parse job data: {exc}")
                    continue

        return _jobs_gen(raw_jobs)

    async def get_job(
        self, params: JobDetailsParams
    ) -> typing.Optional[Job[JobDetailsParams]]:
        """
        Get detailed information for a specific job.

        :param params: `JobDetailsParams` object containing job_id.
        :return: Job object with detailed information.
        """
        url = type(self).url_paths["get_job"]
        query_params = params.as_query_params()
        logger.debug(
            f"Getting job details using url: {url} with job_id: {params.job_id}"
        )
        result = await self._call(
            url, params=query_params, data_model=Job[JobDetailsParams]
        )

        job_data = result.data
        if not isinstance(job_data, list):
            logger.error("Invalid job data format - expected list")
            raise JSearchClientError("Invalid job data format in response")

        if len(job_data) == 0:
            logger.debug("No job found with the given job_id")
            return None

        job = job_data[0]
        job.search_params = params
        return job

    async def get_job_salary(
        self, params: JobSalarySearchParams
    ) -> typing.Optional[JobSalaryInfo[JobSalarySearchParams]]:
        """
        Get estimated salary information for a job title and location.

        :param params: `JobSalarySearchParams` object containing job_title, location, and optional radius.
        :return: `JobSalaryInfo` object with salary estimates if available.
        """
        url = type(self).url_paths["get_job_salary"]
        query_params = params.as_query_params()
        logger.debug(
            f"Getting salary estimates using url: {url} with params: {query_params}"
        )
        result = await self._call(
            url, params=query_params, data_model=JobSalaryInfo[JobSalarySearchParams]
        )

        salary_data = result.data
        if not isinstance(salary_data, list):
            logger.error("API response 'data' field is not a list")
            raise JSearchClientError("Invalid response format: 'data' is not a list")

        if not salary_data:
            logger.debug("")
            return None

        salary_info = salary_data[0]
        salary_info.search_params = params
        return salary_info

    async def get_company_salary(
        self, params: CompanySalarySearchParams
    ) -> typing.Optional[CompanySalaryInfo[CompanySalarySearchParams]]:
        """
        Get estimated salary information for a company and job title.

        :param params: `CompanySalarySearchParams` object containing company_name and job_title.
        :return: `CompanySalaryInfo` object with salary estimates if available.
        """
        url = type(self).url_paths["get_company_salary"]
        query_params = params.as_query_params()
        logger.debug(
            f"Getting company salary estimates using url: {url} with params: {query_params}"
        )
        result = await self._call(
            url,
            params=query_params,
            data_model=CompanySalaryInfo[CompanySalarySearchParams],
        )

        salary_data = result.data
        if not salary_data:
            return None
        if not isinstance(salary_data, list):
            logger.error("API response 'data' field is not a list")
            raise JSearchClientError("Invalid response format: 'data' is not a list")

        salary_info = salary_data[0]
        salary_info.search_params = params
        return salary_info


class JSearchClient:
    """Synchronous client for interacting with the JSearch API."""

    base_url = "https://api.openwebninja.com/jsearch"
    """Default base URL for the JSearch API."""
    url_paths = {
        "search_jobs": "/search",
        "get_job": "/job-details",
        "get_job_salary": "/estimated-salary",
        "get_company_salary": "/company-job-salary",
    }

    def __init__(
        self,
        access_key: str,
        base_url: typing.Optional[str] = None,
        timeout: typing.Union[float, httpx.Timeout] = 30.0,
    ):
        """
        Initialize the client with access key.

        :param access_key: Your JSearch API access key.
        :param base_url: Optional base URL for the API (defaults to JSearch API URL).
        :param timeout: Request timeout in seconds or httpx.Timeout object.
        """
        self.access_key = access_key
        self.base_url = base_url or self.base_url
        self._session: typing.Optional[httpx.Client] = None
        self.timeout = timeout
        logger.debug(
            f"Initialized {self.__class__.__name__} with base URL: {self.base_url}"
        )

    @property
    def session(self) -> httpx.Client:
        """Get or create the HTTP client session."""
        if self._session is None:
            logger.debug("Creating new HTTP session for JSearch client")
            self._session = httpx.Client(
                base_url=self.base_url,
                headers=self.get_headers(),
                timeout=self.timeout,
            )
        return self._session

    def get_headers(self) -> typing.Dict[str, str]:
        """Get the headers for the API requests."""
        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.access_key}",
            "x-api-key": self.access_key,
        }

    @typing.overload
    def _call(
        self,
        url: str,
        params: typing.Dict[str, typing.Any],
        data_model: typing.Type[DataT],
        **kwargs: typing.Any,
    ) -> APIResponse[DataT]: ...

    @typing.overload
    def _call(
        self,
        url: str,
        params: typing.Dict[str, typing.Any],
        data_model: None = None,
        **kwargs: typing.Any,
    ) -> APIResponse[typing.Any]: ...

    def _call(
        self,
        url: str,
        params: typing.Dict[str, typing.Any],
        data_model: typing.Optional[typing.Type[DataT]] = None,
        _method: str = "GET",
        **kwargs: typing.Any,
    ) -> typing.Union[APIResponse[DataT], APIResponse]:
        """
        Make an API call to the JSearch API.

        :param url: The endpoint URL (relative to base_url).
        :param params: Query parameters for the request.
        :param data_model: Pydantic model class to parse the 'data' field of the response.
        :param _method: HTTP method to use (default: GET).
        :param kwargs: Additional arguments to pass to httpx.Client.request().
        :return: An APIResponse instance containing the API response data.
        """
        logger.debug(f"Making {_method} request to {url} with {len(params)} parameters")
        start_time = time.time()

        if data_model is None:
            data_model = typing.cast(typing.Type[DataT], typing.Any)

        response_model = self.get_response_model(data_model)
        try:
            response = self.session.request(_method, url=url, params=params, **kwargs)
            elapsed_time = time.time() - start_time
            code = response.status_code

            logger.debug(f"API response: {code} in {elapsed_time:.3f}s")

            if code != 200:
                logger.warning(f"API request failed with status {code}")
                try:
                    error_data = response.json()
                    logger.info(f"Error response JSON: {error_data}")
                    api_response = response_model.model_validate(error_data)
                    logger.error(
                        f"JSearch API error: {api_response.status} - Request ID: {api_response.request_id}"
                    )
                except json.JSONDecodeError as exc:
                    logger.error(
                        f"Failed to decode error response JSON: {exc}",
                        exc_info=True,
                    )
                    api_response = None
                except Exception as exc:
                    logger.error(
                        f"Failed to parse error response: {exc}", exc_info=True
                    )
                    api_response = None

                if code in (401, 403):
                    logger.error("Authentication error: Invalid access key")
                    raise JSearchAuthError(code=code, response=api_response)
                raise JSearchClientError(code=code, response=api_response)

            try:
                response_data = response.json()
                logger.debug(f"API response JSON: {response_data}")

                model_name = getattr(data_model, "__name__", str(data_model))
                logger.debug(f"Parsing response into `APIResponse[{model_name}]`")
                api_response = response_model.model_validate(response_data)

                # Check status after parsing
                if api_response.status.lower() != "ok":
                    logger.error(f"API response status not OK: {api_response.status}")
                    raise JSearchClientError(
                        f"Invalid response status: {api_response.status}",
                        response=api_response,
                        code=code,
                    )

                return api_response
            except JSearchClientError:
                raise
            except Exception as exc:
                logger.error(f"Failed to parse API response: {exc}", exc_info=True)
                raise JSearchResponseError(f"Failed to parse response: {exc}") from exc

        except JSearchClientError:
            raise
        except Exception as exc:
            elapsed_time = time.time() - start_time
            logger.error(
                f"API request failed after {elapsed_time:.3f}s: {type(exc).__name__}: {exc}"
            )
            raise

    def get_response_model(
        self, data_model: typing.Type[DataT]
    ) -> typing.Type[APIResponse[DataT]]:
        """Get a parameterized `APIResponse` model for the given data model."""
        return typing.cast(typing.Type[APIResponse[DataT]], APIResponse[data_model])  # type: ignore

    def close(self):
        """Close the underlying HTTP session."""
        if self._session is not None:
            logger.debug("Closing HTTP session")
            self._session.close()
            self._session = None
            logger.debug("HTTP session closed successfully")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __del__(self):
        if self._session is not None and not self._session.is_closed:
            logger.warning("client session not properly closed")
            warnings.warn(
                "Unclosed client session. Please use 'with' or call 'close()' to close the session properly.",
                ResourceWarning,
            )

    def search_jobs(
        self, params: JobSearchParams
    ) -> typing.Iterator[Job[JobSearchParams]]:
        """
        Search for jobs using the JSearch API.

        :param params: `JobSearchParams` object containing search parameters.
        :return: An iterator of Job objects matching the search criteria.
        """
        url = type(self).url_paths["search_jobs"]
        query_params = params.as_query_params()
        logger.debug(f"Searching jobs using url: {url} with params: {query_params}")

        result = self._call(
            url, params=query_params, data_model=typing.Dict[str, typing.Any]
        )

        raw_jobs = result.data
        if not isinstance(raw_jobs, list):
            logger.error("API response 'data' field is not a list")
            raise JSearchClientError("Invalid response format: 'data' is not a list")

        def _jobs_gen(
            jobs: typing.List[typing.Dict[str, typing.Any]],
        ) -> typing.Iterator[Job[JobSearchParams]]:
            for raw_job in jobs:
                try:
                    # Attach search params to each job for reference
                    raw_job["search_params"] = params
                    yield Job.model_validate(raw_job)
                except Exception as exc:
                    logger.warning(f"Failed to parse job data: {exc}")
                    continue

        return _jobs_gen(raw_jobs)

    def get_job(
        self, params: JobDetailsParams
    ) -> typing.Optional[Job[JobDetailsParams]]:
        """
        Get detailed information for a specific job.

        :param params: `JobDetailsParams` object containing job_id.
        :return: Job object with detailed information.
        """
        url = type(self).url_paths["get_job"]
        query_params = params.as_query_params()
        logger.debug(
            f"Getting job details using url: {url} with job_id: {params.job_id}"
        )
        result = self._call(url, params=query_params, data_model=Job[JobDetailsParams])

        job_data = result.data
        if not isinstance(job_data, list):
            logger.error("Invalid job data format: expected list")
            raise JSearchClientError("Invalid job data format in response")

        if len(job_data) == 0:
            logger.debug("No job found with the given `job_id`")
            return None

        job = job_data[0]
        job.search_params = params
        return job

    def get_job_salary(
        self, params: JobSalarySearchParams
    ) -> typing.Optional[JobSalaryInfo[JobSalarySearchParams]]:
        """
        Get estimated salary information for a job title and location.

        :param params: `JobSalarySearchParams` object containing job_title, location, and optional parameters.
        :return: `JobSalaryInfo` object with salary estimates if available.
        """
        url = type(self).url_paths["get_job_salary"]
        query_params = params.as_query_params()
        logger.debug(
            f"Getting salary estimates using url: {url} with params: {query_params}"
        )
        result = self._call(
            url, params=query_params, data_model=JobSalaryInfo[JobSalarySearchParams]
        )

        salary_data = result.data
        if not isinstance(salary_data, list):
            logger.error("API response 'data' field is not a list")
            raise JSearchClientError("Invalid response format: 'data' is not a list")

        if not salary_data:
            logger.debug("")
            return None

        salary_info = salary_data[0]
        salary_info.search_params = params
        return salary_info

    def get_company_salary(
        self, params: CompanySalarySearchParams
    ) -> typing.Optional[CompanySalaryInfo[CompanySalarySearchParams]]:
        """
        Get estimated salary information for a company and job title.

        :param params: `CompanySalarySearchParams` object containing company_name and job_title.
        :return: `CompanySalaryInfo` object with salary estimates if available.
        """
        url = type(self).url_paths["get_company_salary"]
        query_params = params.as_query_params()
        logger.debug(
            f"Getting company salary estimates using url: {url} with params: {query_params}"
        )
        result = self._call(
            url,
            params=query_params,
            data_model=CompanySalaryInfo[CompanySalarySearchParams],
        )

        salary_data = result.data
        if not salary_data:
            return None
        if not isinstance(salary_data, list):
            logger.error("API response 'data' field is not a list")
            raise JSearchClientError("Invalid response format: 'data' is not a list")

        salary_info = salary_data[0]
        salary_info.search_params = params
        return salary_info
