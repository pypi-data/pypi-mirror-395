import pytest
from assertpy import assert_that
from pydantic import ValidationError

from ghanon.domain.workflow import Workflow


class TestWorkflowModel:
    @pytest.mark.parametrize(
        "job_id",
        [
            "123-job",
            "job.name",
            "-job",
            "job name",
            "job@test",
        ],
    )
    def test_invalid_job_id(self, job_id) -> None:
        workflow_data = {
            "name": "Test",
            "on": "push",
            "jobs": {
                job_id: {
                    "runs-on": "ubuntu-latest",
                    "steps": [{"run": "echo hello"}],
                },
            },
        }

        with pytest.raises(
            ValidationError,
            match=r"Invalid job ID '.+': must start with a letter or underscore and "
            r"contain only alphanumeric characters, dashes, or underscores",
        ):
            Workflow.model_validate(workflow_data)

    @pytest.mark.parametrize(
        "job_id",
        [
            "build",
            "_private",
            "test-unit",
            "test_integration",
            "Deploy_123",
            "Build_And_Deploy-v2",
        ],
    )
    def test_valid_job_id(self, job_id) -> None:
        workflow_data = {
            "name": "Test",
            "on": "push",
            "permissions": {"contents": "read"},
            "jobs": {
                job_id: {
                    "runs-on": "ubuntu-latest",
                    "steps": [{"run": "echo hello"}],
                },
            },
        }

        workflow = Workflow.model_validate(workflow_data)

        assert_that(workflow.jobs).contains_key(job_id)
