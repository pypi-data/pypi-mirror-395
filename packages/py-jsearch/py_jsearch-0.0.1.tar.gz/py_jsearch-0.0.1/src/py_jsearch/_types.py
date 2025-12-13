import typing

import pydantic
from typing_extensions import Annotated

__all__ = [
    "JobSearchParams",
    "JobDetailsParams",
    "JobSalarySearchParams",
    "CompanySalarySearchParams",
    "APIResponse",
    "Job",
    "JobRequiredExperience",
    "JobRequiredEducation",
    "JobHighlights",
    "ApplyOption",
    "JobSalaryInfo",
    "CompanySalaryInfo",
]


DataT = typing.TypeVar("DataT")


class APIResponse(pydantic.BaseModel, typing.Generic[DataT]):
    """JSearch API response model."""

    status: Annotated[str, pydantic.StringConstraints(to_lower=True)]
    """The status of the API response, e.g., 'ok' or 'error'."""
    request_id: str
    """Unique identifier for tracking the API request."""
    parameters: typing.Dict[str, typing.Any] = pydantic.Field(default_factory=dict)
    """The parameters used in the request (includes query, page, num_pages, date_posted, country, language, etc.)."""
    data: typing.List[DataT] = pydantic.Field(default_factory=list)
    """The main data payload of the response (array of items)."""


class JobSearchParams(pydantic.BaseModel):
    """JSearch job search parameters model."""

    query: str = pydantic.Field(
        ...,
        description="[Required] Free-form jobs search query. It is highly recommended to include job title and location as part of the query (e.g., 'web development jobs in chicago', 'marketing manager in new york via linkedin').",
    )
    page: typing.Optional[int] = pydantic.Field(
        default=1,
        description="Optional Page to return (each page includes up to 10 results). Allowed values: 1-100.",
        ge=1,
        le=100,
    )
    num_pages: typing.Optional[int] = pydantic.Field(
        default=1,
        description="Optional Number of pages to return, starting from page. Allowed values: 1-20. Note: requests for more than one page and up to 10 pages are charged x2 and requests for more than 10 pages are charged 3x.",
        ge=1,
        le=20,
    )
    country: typing.Optional[str] = pydantic.Field(
        default="us",
        description="Optional Country code (ISO 3166-1 alpha-2) from which to return job postings. This parameter must be set to get jobs in a specific country (e.g., 'us', 'de', 'gb'). See: https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2",
    )
    language: typing.Optional[str] = pydantic.Field(
        default=None,
        description="Optional Language code (ISO 639) in which to return job postings. Leave empty to use the primary language in the specified country. See: https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes",
    )
    date_posted: typing.Optional[
        typing.Literal["all", "today", "3days", "week", "month"]
    ] = pydantic.Field(
        default="all",
        description="Optional Find jobs posted within the time you specify. Allowed values: 'all', 'today', '3days', 'week', 'month' (default: 'all').",
    )
    work_from_home: typing.Optional[bool] = pydantic.Field(
        default=False,
        description="Optional Only return work from home / remote jobs (default: False).",
    )
    employment_types: typing.Optional[
        typing.Sequence[typing.Literal["FULLTIME", "CONTRACTOR", "PARTTIME", "INTERN"]]
    ] = pydantic.Field(
        default=None,
        description="Optional Find jobs of particular employment types, specified as a comma delimited list of the following values: 'FULLTIME', 'CONTRACTOR', 'PARTTIME', 'INTERN'.",
    )
    job_requirements: typing.Optional[
        typing.Sequence[
            typing.Literal[
                "under_3_years_experience",
                "more_than_3_years_experience",
                "no_experience",
                "no_degree",
            ]
        ]
    ] = pydantic.Field(
        default=None,
        description="Optional Find jobs with specific requirements, specified as a comma delimited list of the following values: 'under_3_years_experience', 'more_than_3_years_experience', 'no_experience', 'no_degree'.",
    )
    radius: typing.Optional[float] = pydantic.Field(
        default=None,
        description="Optional Return jobs within a certain distance from location as specified as part of the query (in km). This is sent as the Google 'lrad' parameter and although it might affect the results, it is not strictly followed by Google for Jobs.",
        ge=0,
    )
    exclude_job_publishers: typing.Optional[typing.Sequence[str]] = pydantic.Field(
        default=None,
        description="Optional Exclude jobs published by specific publishers, specified as a comma separated list of publishers to exclude.",
    )
    fields: typing.Optional[typing.Sequence[str]] = pydantic.Field(
        default=None,
        description="Optional A comma separated list of job fields to include in the response (field projection). By default all fields are returned.",
    )

    def as_query_params(self) -> typing.Dict[str, typing.Any]:
        """Convert the search parameters to a dictionary suitable for API query parameters."""
        params = self.model_dump(mode="json", exclude_none=True)
        if "work_from_home" in params:
            params["work_from_home"] = str(params["work_from_home"]).lower()
        if "employment_types" in params:
            params["employment_types"] = ",".join(params["employment_types"])
        if "job_requirements" in params:
            params["job_requirements"] = ",".join(params["job_requirements"])
        if "exclude_job_publishers" in params:
            params["exclude_job_publishers"] = ",".join(
                params["exclude_job_publishers"]
            )
        if "fields" in params:
            params["fields"] = ",".join(params["fields"])
        return params


class JobDetailsParams(pydantic.BaseModel):
    """JSearch job details parameters model."""

    job_id: str = pydantic.Field(
        ...,
        description="[Required] Job Id of the job for which to get details. Batching of up to 20 Job Ids is supported by separating multiple Job Ids by comma (,). Note that each Job Id in a batch request is counted as a request for quota calculation.",
    )
    country: typing.Optional[str] = pydantic.Field(
        default="us",
        description="Optional Country code (ISO 3166-1 alpha-2) from which to return job posting (e.g., 'us', 'de', 'gb'). See: https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2",
    )
    language: typing.Optional[str] = pydantic.Field(
        default=None,
        description="Optional Language code (ISO 639) in which to return job postings. Leave empty to use the primary language in the specified country. See: https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes",
    )
    fields: typing.Optional[typing.Sequence[str]] = pydantic.Field(
        default=None,
        description="Optional A comma separated list of job fields to include in the response (field projection). By default all fields are returned.",
    )

    def as_query_params(self) -> typing.Dict[str, typing.Any]:
        """Convert the job details parameters to a dictionary suitable for API query parameters."""
        params = self.model_dump(mode="json", exclude_none=True)
        if "fields" in params:
            params["fields"] = ",".join(params["fields"])
        return params


class JobSalarySearchParams(pydantic.BaseModel):
    """JSearch job salary search parameters model."""

    job_title: str = pydantic.Field(
        ...,
        description="[Required] Job title for which to get salary estimation.",
    )
    location: str = pydantic.Field(
        ...,
        description="[Required] Location in which to get salary estimation.",
    )
    location_type: typing.Optional[
        typing.Literal["ANY", "CITY", "STATE", "COUNTRY"]
    ] = pydantic.Field(
        default="ANY",
        description="Optional Specify the type of the location you are looking to get salary estimation for additional accuracy. Allowed values: 'ANY', 'CITY', 'STATE', 'COUNTRY' (default: 'ANY').",
    )
    years_of_experience: typing.Optional[
        typing.Literal[
            "ALL",
            "LESS_THAN_ONE",
            "ONE_TO_THREE",
            "FOUR_TO_SIX",
            "SEVEN_TO_NINE",
            "TEN_TO_FOURTEEN",
            "ABOVE_FIFTEEN",
        ]
    ] = pydantic.Field(
        default="ALL",
        description="Optional Get job estimation for a specific experience level range (years). Allowed values: 'ALL', 'LESS_THAN_ONE', 'ONE_TO_THREE', 'FOUR_TO_SIX', 'SEVEN_TO_NINE', 'TEN_TO_FOURTEEN', 'ABOVE_FIFTEEN' (default: 'ALL').",
    )
    fields: typing.Optional[typing.Sequence[str]] = pydantic.Field(
        default=None,
        description="Optional A comma separated list of job salary fields to include in the response (field projection). By default all fields are returned.",
    )

    def as_query_params(self) -> typing.Dict[str, typing.Any]:
        """Convert the salary search parameters to a dictionary suitable for API query parameters."""
        params = self.model_dump(mode="json", exclude_none=True)
        if "fields" in params:
            params["fields"] = ",".join(params["fields"])
        return params


class CompanySalarySearchParams(pydantic.BaseModel):
    """JSearch company salary search parameters model."""

    company: str = pydantic.Field(
        ...,
        description="[Required] The company name for which to get salary information (e.g., Amazon).",
    )
    job_title: str = pydantic.Field(
        ...,
        description="[Required] Job title for which to get salary estimation.",
    )
    location: typing.Optional[str] = pydantic.Field(
        default=None,
        description="Optional Free-text location/area in which to get salary estimation.",
    )
    location_type: typing.Optional[
        typing.Literal["ANY", "CITY", "STATE", "COUNTRY"]
    ] = pydantic.Field(
        default="ANY",
        description="Optional Specify the type of the location you are looking to get salary estimation for additional accuracy. Allowed values: 'ANY', 'CITY', 'STATE', 'COUNTRY' (default: 'ANY').",
    )
    years_of_experience: typing.Optional[
        typing.Literal[
            "ALL",
            "LESS_THAN_ONE",
            "ONE_TO_THREE",
            "FOUR_TO_SIX",
            "SEVEN_TO_NINE",
            "TEN_TO_FOURTEEN",
            "ABOVE_FIFTEEN",
        ]
    ] = pydantic.Field(
        default="ALL",
        description="Optional Get job estimation for a specific experience level range (years). Allowed values: 'ALL', 'LESS_THAN_ONE', 'ONE_TO_THREE', 'FOUR_TO_SIX', 'SEVEN_TO_NINE', 'TEN_TO_FOURTEEN', 'ABOVE_FIFTEEN' (default: 'ALL').",
    )

    def as_query_params(self) -> typing.Dict[str, typing.Any]:
        """Convert the company salary search parameters to a dictionary suitable for API query parameters."""
        return self.model_dump(mode="json", exclude_none=True)


class JobRequiredExperience(pydantic.BaseModel):
    """Job required experience model."""

    no_experience_required: typing.Optional[bool] = None
    required_experience_in_months: typing.Optional[int] = None
    experience_mentioned: typing.Optional[bool] = None
    experience_preferred: typing.Optional[bool] = None


class JobRequiredEducation(pydantic.BaseModel):
    """Job required education model."""

    postgraduate_degree: typing.Optional[bool] = None
    professional_certification: typing.Optional[bool] = None
    high_school: typing.Optional[bool] = None
    associates_degree: typing.Optional[bool] = None
    bachelors_degree: typing.Optional[bool] = None
    degree_mentioned: typing.Optional[bool] = None
    degree_preferred: typing.Optional[bool] = None
    professional_certification_mentioned: typing.Optional[bool] = None


class JobHighlights(pydantic.BaseModel):
    """Job highlights model."""

    qualifications: typing.Optional[typing.List[str]] = pydantic.Field(
        default=None, alias="Qualifications"
    )
    responsibilities: typing.Optional[typing.List[str]] = pydantic.Field(
        default=None, alias="Responsibilities"
    )
    benefits: typing.Optional[typing.List[str]] = pydantic.Field(
        default=None, alias="Benefits"
    )

    class Config:
        populate_by_name = True


class ApplyOption(pydantic.BaseModel):
    """Apply option model for different job application publishers."""

    publisher: typing.Optional[str] = None
    """Name of the job publisher/board."""

    apply_link: typing.Optional[str] = None
    """URL to apply for the job through this publisher."""

    is_direct: typing.Optional[bool] = None
    """Whether the application goes directly to the employer."""


SearchParamT = typing.TypeVar("SearchParamT", bound=pydantic.BaseModel)


class Job(pydantic.BaseModel, typing.Generic[SearchParamT]):
    """JSearch job model."""

    employer_name: typing.Optional[str] = None
    """Name of the employer/company."""

    employer_logo: typing.Optional[str] = None
    """URL to employer's logo."""

    employer_website: typing.Optional[str] = None
    """Employer's website URL."""

    employer_company_type: typing.Optional[str] = None
    """Type of company/employer."""

    job_publisher: typing.Optional[str] = None
    """The job board/publisher where this job was found."""

    job_id: str
    """Unique identifier for the job."""

    job_employment_type: typing.Optional[str] = None
    """Employment type (e.g., FULLTIME, PARTTIME, CONTRACTOR, INTERN)."""

    job_employment_types: typing.Optional[typing.List[str]] = None
    """List of employment types for the job."""

    job_title: typing.Optional[str] = None
    """Title of the job."""

    job_apply_link: typing.Optional[str] = None
    """URL to apply for the job."""

    job_apply_is_direct: typing.Optional[bool] = None
    """Whether the apply link goes directly to the employer."""

    apply_options: typing.Optional[typing.List[ApplyOption]] = None
    """List of different application options from various publishers."""

    job_apply_quality_score: typing.Optional[float] = None
    """Quality score for the job application link."""

    job_description: typing.Optional[str] = None
    """Full job description."""

    job_is_remote: typing.Optional[bool] = None
    """Whether the job is remote."""

    job_posted_at: typing.Optional[str] = None
    """Human-readable string indicating when the job was posted (e.g., '2 days ago')."""

    job_posted_at_timestamp: typing.Optional[int] = None
    """Unix timestamp when the job was posted."""

    job_posted_at_datetime_utc: typing.Optional[str] = None
    """ISO datetime string when the job was posted (UTC)."""

    job_location: typing.Optional[str] = None
    """Combined location string (e.g., 'Chicago, IL')."""

    job_city: typing.Optional[str] = None
    """City where the job is located."""

    job_state: typing.Optional[str] = None
    """State/province where the job is located."""

    job_country: typing.Optional[str] = None
    """Country where the job is located."""

    job_latitude: typing.Optional[float] = None
    """Latitude coordinate of job location."""

    job_longitude: typing.Optional[float] = None
    """Longitude coordinate of job location."""

    job_benefits: typing.Optional[typing.List[str]] = None
    """List of job benefits."""

    job_google_link: typing.Optional[str] = None
    """Google Jobs link for this job."""

    job_offer_expiration_datetime_utc: typing.Optional[str] = None
    """ISO datetime string when the job offer expires (UTC)."""

    job_offer_expiration_timestamp: typing.Optional[int] = None
    """Unix timestamp when the job offer expires."""

    job_required_experience: typing.Optional[JobRequiredExperience] = None
    """Required experience information."""

    job_required_skills: typing.Optional[typing.List[str]] = None
    """List of required skills."""

    job_required_education: typing.Optional[JobRequiredEducation] = None
    """Required education information."""

    job_experience_in_place_of_education: typing.Optional[bool] = None
    """Whether experience can substitute for education."""

    job_salary: typing.Optional[float] = None
    """Salary amount for the job (if available as a single value)."""

    job_min_salary: typing.Optional[float] = None
    """Minimum salary for the job."""

    job_max_salary: typing.Optional[float] = None
    """Maximum salary for the job."""

    job_salary_currency: typing.Optional[str] = None
    """Currency code for the salary."""

    job_salary_period: typing.Optional[str] = None
    """Salary period (e.g., YEAR, MONTH, HOUR)."""

    job_highlights: typing.Optional[JobHighlights] = None
    """Structured job highlights including qualifications, responsibilities, and benefits."""

    job_job_title: typing.Optional[str] = None
    """Alternative job title field."""

    job_posting_language: typing.Optional[str] = None
    """Language code of the job posting."""

    job_onet_soc: typing.Optional[str] = None
    """O*NET SOC (Standard Occupational Classification) code."""

    job_onet_job_zone: typing.Optional[str] = None
    """O*NET job zone classification."""

    job_occupational_categories: typing.Optional[typing.List[str]] = None
    """List of occupational category codes."""
    search_params: typing.Optional[SearchParamT] = None
    """Search parameters used to find this job."""


class JobSalaryInfo(pydantic.BaseModel, typing.Generic[SearchParamT]):
    """JSearch salary information model."""

    location: typing.Optional[str] = None
    """Location for the salary information."""

    job_title: typing.Optional[str] = None
    """Job title for the salary information."""

    publisher_name: typing.Optional[str] = None
    """Name of the salary data publisher."""

    publisher_link: typing.Optional[str] = None
    """URL to the publisher's salary page."""

    min_salary: typing.Optional[float] = None
    """Minimum salary amount."""

    max_salary: typing.Optional[float] = None
    """Maximum salary amount."""

    median_salary: typing.Optional[float] = None
    """Median salary amount."""

    min_base_salary: typing.Optional[float] = None
    """Minimum base salary amount (excluding additional pay)."""

    max_base_salary: typing.Optional[float] = None
    """Maximum base salary amount (excluding additional pay)."""

    median_base_salary: typing.Optional[float] = None
    """Median base salary amount (excluding additional pay)."""

    min_additional_pay: typing.Optional[float] = None
    """Minimum additional pay (bonuses, commissions, etc.)."""

    max_additional_pay: typing.Optional[float] = None
    """Maximum additional pay (bonuses, commissions, etc.)."""

    median_additional_pay: typing.Optional[float] = None
    """Median additional pay (bonuses, commissions, etc.)."""

    salary_period: typing.Optional[str] = None
    """Salary period (e.g., YEAR, MONTH, HOUR)."""

    salary_currency: typing.Optional[str] = None
    """Currency code for the salary amounts."""

    salary_count: typing.Optional[int] = None
    """Number of salary data points used for this estimation."""

    salaries_updated_at: typing.Optional[str] = None
    """ISO datetime string when the salary data was last updated."""

    confidence: typing.Optional[str] = None
    """Confidence level of the salary estimation (e.g., CONFIDENT)."""

    search_params: typing.Optional[SearchParamT] = None
    """Search parameters used to find this salary information."""


class CompanySalaryInfo(pydantic.BaseModel, typing.Generic[SearchParamT]):
    """JSearch company salary information model."""

    location: typing.Optional[str] = None
    """Location for the salary information."""

    job_title: typing.Optional[str] = None
    """Job title for the salary information."""

    company: typing.Optional[str] = None
    """Company name for the salary information."""

    min_salary: typing.Optional[float] = None
    """Minimum salary amount."""

    max_salary: typing.Optional[float] = None
    """Maximum salary amount."""

    median_salary: typing.Optional[float] = None
    """Median salary amount."""

    min_base_salary: typing.Optional[float] = None
    """Minimum base salary amount (excluding additional pay)."""

    max_base_salary: typing.Optional[float] = None
    """Maximum base salary amount (excluding additional pay)."""

    median_base_salary: typing.Optional[float] = None
    """Median base salary amount (excluding additional pay)."""

    min_additional_pay: typing.Optional[float] = None
    """Minimum additional pay (bonuses, commissions, etc.)."""

    max_additional_pay: typing.Optional[float] = None
    """Maximum additional pay (bonuses, commissions, etc.)."""

    median_additional_pay: typing.Optional[float] = None
    """Median additional pay (bonuses, commissions, etc.)."""

    salary_period: typing.Optional[str] = None
    """Salary period (e.g., YEAR, MONTH, HOUR)."""

    salary_currency: typing.Optional[str] = None
    """Currency code for the salary amounts."""

    confidence: typing.Optional[str] = None
    """Confidence level of the salary estimation (e.g., CONFIDENT)."""

    salary_count: typing.Optional[int] = None
    """Number of salary data points used for this estimation."""

    search_params: typing.Optional[SearchParamT] = None
    """Search parameters used to find this salary information."""
