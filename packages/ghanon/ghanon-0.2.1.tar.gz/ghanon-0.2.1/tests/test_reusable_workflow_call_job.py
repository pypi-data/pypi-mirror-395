import pytest
from assertpy import assert_that

from ghanon.domain.matrix import Matrix, Strategy
from ghanon.domain.workflow import ReusableWorkflowCallJob


@pytest.fixture
def minimal_config() -> dict[str, str]:
    """Provide a minimal configuration for a reusable workflow call job."""
    return {
        "uses": "owner/repo/.github/workflows/workflow.yml@main",
    }


class TestReusableWorkflowCallJob:
    def test_minimal(self, minimal_config) -> None:
        job = ReusableWorkflowCallJob.model_validate(
            minimal_config,
        )
        assert_that(job.uses).is_equal_to(minimal_config["uses"])

    def test_with_inputs(self, minimal_config) -> None:
        environment = "production"

        job = ReusableWorkflowCallJob.model_validate(
            {
                **minimal_config,
                "with": {"environment": environment},
            },
        )

        assert_that(job.with_).contains_entry({"environment": environment})

    def test_secrets_explicit(self, minimal_config) -> None:
        value = "${{ secrets.API_KEY }}"
        key = "API_KEY"

        job = ReusableWorkflowCallJob.model_validate(
            {
                **minimal_config,
                "secrets": {key: value},
            },
        )

        assert_that(job.secrets).contains_entry({key: value})

    def test_with_strategy(self, minimal_config) -> None:
        matrix = {"env": ["dev", "staging"]}

        job = ReusableWorkflowCallJob.model_validate(
            {
                **minimal_config,
                "strategy": {"matrix": matrix},
            },
        )

        assert isinstance(job.strategy, Strategy)
        assert isinstance(job.strategy.matrix, Matrix)
        assert_that(job.strategy.matrix.model_dump()).contains_entry(matrix)
