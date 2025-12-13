"""Tests for type models and validation."""

from typing import Any, Dict

from pydantic import ValidationError
import pytest

from py_jsearch import (
    ApplyOption,
    CompanySalaryInfo,
    CompanySalarySearchParams,
    Job,
    JobDetailsParams,
    JobSalaryInfo,
    JobSalarySearchParams,
    JobSearchParams,
)


@pytest.mark.unit
class TestJobSearchParams:
    """Test JobSearchParams model validation."""

    def test_required_field(self) -> None:
        """Test that query is required."""
        params = JobSearchParams(query="python developer")
        assert params.query == "python developer"

    def test_default_values(self) -> None:
        """Test default parameter values."""
        params = JobSearchParams(query="test")
        assert params.page == 1
        assert params.num_pages == 1

    def test_as_query_params(self) -> None:
        """Test conversion to query parameters."""
        params = JobSearchParams(
            query="python developer",
            page=2,
            work_from_home=True,
            employment_types=["FULLTIME", "CONTRACTOR"],  # type: ignore[list-item]
        )
        query_dict = params.as_query_params()

        assert query_dict["query"] == "python developer"
        assert query_dict["page"] == 2
        assert query_dict["work_from_home"] == "true"
        assert query_dict["employment_types"] == "FULLTIME,CONTRACTOR"

    def test_work_from_home_mapping(self) -> None:
        """Test work_from_home maps to string."""
        params = JobSearchParams(query="test", work_from_home=True)
        query_dict = params.as_query_params()
        assert "work_from_home" in query_dict
        assert query_dict["work_from_home"] == "true"

    def test_date_posted_validation(self) -> None:
        """Test date_posted accepts valid values."""
        valid_values = ["all", "today", "3days", "week", "month"]
        for value in valid_values:
            params = JobSearchParams(query="test", date_posted=value)  # type: ignore[arg-type]
            assert params.date_posted == value

    def test_employment_types_validation(self) -> None:
        """Test employment_types validation."""
        params = JobSearchParams(
            query="test",
            employment_types=["FULLTIME", "PARTTIME"],  # type: ignore[list-item]
        )
        assert len(params.employment_types) == 2  # type: ignore[arg-type]

    def test_radius_validation(self) -> None:
        """Test radius parameter."""
        params = JobSearchParams(query="test", radius=50)
        assert params.radius == 50

    def test_country_and_language(self) -> None:
        """Test country and language parameters."""
        params = JobSearchParams(
            query="test",
            country="us",
            language="en",
        )
        assert params.country == "us"
        assert params.language == "en"


@pytest.mark.unit
class TestJobDetailsParams:
    """Test JobDetailsParams model validation."""

    def test_required_field(self) -> None:
        """Test that job_id is required."""
        params = JobDetailsParams(job_id="abc123")
        assert params.job_id == "abc123"

    def test_extended_publisher_details(self) -> None:
        """Test that fields parameter works."""
        params = JobDetailsParams(
            job_id="abc123",
            fields=["job_title", "employer_name"],
        )
        assert params.fields == ["job_title", "employer_name"]

    def test_as_query_params(self) -> None:
        """Test conversion to query parameters."""
        params = JobDetailsParams(
            job_id="abc123",
            country="us",
            language="en",
        )
        query_dict = params.as_query_params()

        assert query_dict["job_id"] == "abc123"
        assert query_dict["country"] == "us"
        assert query_dict["language"] == "en"


@pytest.mark.unit
class TestJobSalarySearchParams:
    """Test JobSalarySearchParams model validation."""

    def test_required_fields(self) -> None:
        """Test that job_title and location are required."""
        params = JobSalarySearchParams(
            job_title="Software Engineer",
            location="San Francisco, CA",
        )
        assert params.job_title == "Software Engineer"
        assert params.location == "San Francisco, CA"

    def test_location_type_validation(self) -> None:
        """Test location_type validation."""
        valid_types = ["CITY", "STATE", "COUNTRY"]
        for loc_type in valid_types:
            params = JobSalarySearchParams(
                job_title="Engineer",
                location="California",
                location_type=loc_type,  # type: ignore[arg-type]
            )
            assert params.location_type == loc_type

    def test_years_of_experience_validation(self) -> None:
        """Test years_of_experience validation."""
        valid_values = [
            "ALL",
            "LESS_THAN_ONE",
            "ONE_TO_THREE",
            "FOUR_TO_SIX",
            "SEVEN_TO_NINE",
            "TEN_TO_FOURTEEN",
            "ABOVE_FIFTEEN",
        ]
        for exp in valid_values:
            params = JobSalarySearchParams(
                job_title="Engineer",
                location="California",
                years_of_experience=exp,  # type: ignore[arg-type]
            )
            assert params.years_of_experience == exp

    def test_as_query_params(self) -> None:
        """Test conversion to query parameters."""
        params = JobSalarySearchParams(
            job_title="Software Engineer",
            location="San Francisco",
            location_type="CITY",
            years_of_experience="FOUR_TO_SIX",
        )
        query_dict = params.as_query_params()

        assert query_dict["job_title"] == "Software Engineer"
        assert query_dict["location"] == "San Francisco"
        assert query_dict["location_type"] == "CITY"
        assert query_dict["years_of_experience"] == "FOUR_TO_SIX"


@pytest.mark.unit
class TestCompanySalarySearchParams:
    """Test CompanySalarySearchParams model validation."""

    def test_required_fields(self) -> None:
        """Test that company and job_title are required."""
        params = CompanySalarySearchParams(
            company="Google",
            job_title="Software Engineer",
        )
        assert params.company == "Google"
        assert params.job_title == "Software Engineer"

    def test_location_optional(self) -> None:
        """Test that location is optional."""
        params = CompanySalarySearchParams(
            company="Google",
            job_title="Engineer",
            location="Mountain View, CA",
        )
        assert params.location == "Mountain View, CA"

    def test_as_query_params(self) -> None:
        """Test conversion to query parameters."""
        params = CompanySalarySearchParams(
            company="Google",
            job_title="Software Engineer",
            location="California",
        )
        query_dict = params.as_query_params()

        assert query_dict["company"] == "Google"
        assert query_dict["job_title"] == "Software Engineer"
        assert query_dict["location"] == "California"


@pytest.mark.unit
class TestApplyOption:
    """Test ApplyOption model."""

    def test_required_fields(self) -> None:
        """Test ApplyOption required fields."""
        option = ApplyOption(
            publisher="LinkedIn",
            apply_link="https://linkedin.com/jobs/apply",
            is_direct=True,
        )
        assert option.publisher == "LinkedIn"
        assert option.apply_link == "https://linkedin.com/jobs/apply"
        assert option.is_direct is True

    def test_optional_is_direct(self) -> None:
        """Test that is_direct defaults to None."""
        option = ApplyOption(
            publisher="Indeed",
            apply_link="https://indeed.com/apply",
        )
        assert option.is_direct is None


@pytest.mark.unit
class TestJob:
    """Test Job model."""

    def test_minimal_job(self) -> None:
        """Test Job with minimal required fields."""
        job = Job(
            job_id="test123",
            job_title="Python Developer",
            employer_name="Tech Corp",
            job_country="US",
        )
        assert job.job_id == "test123"
        assert job.job_title == "Python Developer"
        assert job.employer_name == "Tech Corp"
        assert job.job_country == "US"

    def test_job_with_all_fields(self, sample_job_data: Dict[str, Any]) -> None:
        """Test Job with all fields."""
        job = Job(**sample_job_data)
        assert job.job_id == "test_job_123"
        assert job.job_title == "Senior Python Developer"
        assert job.job_is_remote is True
        assert len(job.apply_options) == 2  # type: ignore[arg-type]
        assert job.job_employment_types == ["FULLTIME"]

    def test_apply_options_parsing(self, sample_job_data: Dict[str, Any]) -> None:
        """Test that apply_options are parsed correctly."""
        job = Job(**sample_job_data)
        assert job.apply_options is not None
        assert len(job.apply_options) == 2
        assert isinstance(job.apply_options[0], ApplyOption)
        assert job.apply_options[0].publisher == "LinkedIn"


@pytest.mark.unit
class TestJobSalaryInfo:
    """Test JobSalaryInfo model."""

    def test_required_fields(self) -> None:
        """Test JobSalaryInfo required fields."""
        salary = JobSalaryInfo(
            job_title="Software Engineer",
            location="San Francisco, CA",
            median_salary=140000.0,
        )
        assert salary.job_title == "Software Engineer"
        assert salary.location == "San Francisco, CA"
        assert salary.median_salary == 140000.0

    def test_all_fields(self, sample_salary_data: Dict[str, Any]) -> None:
        """Test JobSalaryInfo with all fields."""
        salary = JobSalaryInfo(**sample_salary_data)
        assert salary.job_title == "Python Developer"
        assert salary.min_salary == 100000.0
        assert salary.max_salary == 180000.0
        assert salary.median_salary == 140000.0
        assert salary.publisher_link is not None

    def test_optional_base_salary_fields(self, sample_salary_data: Dict[str, Any]) -> None:
        """Test optional base salary breakdown fields."""
        salary = JobSalaryInfo(**sample_salary_data)
        assert salary.min_base_salary == 90000.0
        assert salary.max_base_salary == 150000.0
        assert salary.median_base_salary == 120000.0


@pytest.mark.unit
class TestCompanySalaryInfo:
    """Test CompanySalaryInfo model."""

    def test_required_fields(self) -> None:
        """Test CompanySalaryInfo required fields."""
        salary = CompanySalaryInfo(
            company="Google",
            job_title="Software Engineer",
            median_salary=180000.0,
        )
        assert salary.company == "Google"
        assert salary.job_title == "Software Engineer"
        assert salary.median_salary == 180000.0

    def test_all_fields(self, sample_company_salary_data: Dict[str, Any]) -> None:
        """Test CompanySalaryInfo with all fields."""
        salary = CompanySalaryInfo(**sample_company_salary_data)
        assert salary.company == "Google"
        assert salary.job_title == "Software Engineer"
        assert salary.location == "United States"
        assert salary.min_salary == 140000.0
        assert salary.max_salary == 250000.0


@pytest.mark.unit
class TestParameterValidation:
    """Test parameter validation edge cases."""

    def test_invalid_date_posted(self) -> None:
        """Test that invalid date_posted values are rejected."""
        # Pydantic will validate against Literal types
        with pytest.raises(ValidationError):
            JobSearchParams(query="test", date_posted="invalid")  # type: ignore[arg-type]

    def test_invalid_employment_type(self) -> None:
        """Test that invalid employment_types are rejected."""
        with pytest.raises(ValidationError):
            JobSearchParams(
                query="test",
                employment_types=["INVALID_TYPE"],  # type: ignore[arg-type]
            )

    def test_negative_page_number(self) -> None:
        """Test that negative page numbers are rejected."""
        with pytest.raises(ValidationError):
            JobSearchParams(query="test", page=-1)

    def test_invalid_radius(self) -> None:
        """Test that invalid radius values are rejected."""
        with pytest.raises(ValidationError):
            JobSearchParams(query="test", radius=-10)
