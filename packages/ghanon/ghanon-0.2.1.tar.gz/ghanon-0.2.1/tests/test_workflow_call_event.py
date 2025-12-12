from assertpy import assert_that

from ghanon.domain.workflow import WorkflowCallEvent, WorkflowCallInputType


class TestWorkflowCallEvent:
    def test_inputs(self) -> None:
        event = WorkflowCallEvent.model_validate(
            {
                "inputs": {
                    "environment": {"type": "string", "required": True},
                    "debug": {"type": "boolean", "default": False},
                },
            },
        )

        assert event.inputs is not None
        assert_that(event.inputs["environment"].type).is_equal_to(WorkflowCallInputType.STRING)
        assert_that(event.inputs["debug"].default).is_false()

    def test_outputs(self) -> None:
        event = WorkflowCallEvent.model_validate(
            {
                "outputs": {
                    "version": {
                        "description": "v1.2.3",
                        "value": "${{ jobs.build.outputs.version }}",
                    },
                },
            },
        )

        assert event.outputs is not None
        assert_that(event.outputs["version"].description).is_equal_to("v1.2.3")
        assert_that(event.outputs["version"].value).is_equal_to("${{ jobs.build.outputs.version }}")

    def test_secrets(self) -> None:
        event = WorkflowCallEvent.model_validate(
            {
                "secrets": {
                    "API_KEY": {"description": "API key", "required": True},
                },
            },
        )

        assert event.secrets is not None
        assert_that(event.secrets["API_KEY"].required).is_true()
        assert_that(event.secrets["API_KEY"].description).is_equal_to("API key")
