from assertpy import assert_that
from pydantic import ValidationError

from ghanon.domain.workflow import (
    WorkflowDispatchEvent,
    WorkflowDispatchInput,
    WorkflowDispatchInputType,
)


class TestWorkflowDispatchEvent:
    def test_empty(self) -> None:
        event = WorkflowDispatchEvent.model_validate({})
        assert_that(event.inputs).is_none()

    def test_string_input(self) -> None:
        event = WorkflowDispatchEvent.model_validate(
            {
                "inputs": {
                    "name": {
                        "description": "Name",
                        "type": "string",
                        "default": "world",
                    },
                },
            },
        )

        assert event.inputs is not None
        assert_that(event.inputs["name"].type).is_equal_to(WorkflowDispatchInputType.STRING)

    def test_boolean_input(self) -> None:
        event = WorkflowDispatchEvent.model_validate(
            {
                "inputs": {
                    "debug": {
                        "description": "Debug",
                        "type": "boolean",
                        "default": False,
                    },
                },
            },
        )

        assert event.inputs is not None
        assert_that(event.inputs["debug"].type).is_equal_to(WorkflowDispatchInputType.BOOLEAN)

    def test_choice_input(self) -> None:
        event = WorkflowDispatchEvent.model_validate(
            {
                "inputs": {
                    "env": {
                        "description": "Environment",
                        "type": "choice",
                        "options": ["dev", "staging", "prod"],
                    },
                },
            },
        )

        assert event.inputs is not None
        assert_that(event.inputs["env"].options).is_equal_to(["dev", "staging", "prod"])

    def test_choice_requires_options(self) -> None:
        assert_that(WorkflowDispatchInput.model_validate).raises(ValidationError).when_called_with(
            {
                "description": "Env",
                "type": "choice",
            },
        )

    def test_required_input(self) -> None:
        event = WorkflowDispatchEvent.model_validate(
            {
                "inputs": {"token": {"description": "API Token", "required": True}},
            },
        )

        assert event.inputs is not None
        assert_that(event.inputs["token"].required).is_true()
