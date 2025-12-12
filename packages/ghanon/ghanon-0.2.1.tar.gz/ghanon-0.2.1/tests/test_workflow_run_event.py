from assertpy import assert_that

from ghanon.domain.workflow import WorkflowRunActivityType, WorkflowRunEvent


class TestWorkflowRunEvent:
    def test_types(self) -> None:
        event = WorkflowRunEvent.model_validate(
            {
                "types": [WorkflowRunActivityType.COMPLETED],
                "workflows": ["CI"],
            },
        )

        assert_that(event.types).contains(WorkflowRunActivityType.COMPLETED)
        assert_that(event.workflows).contains("CI")

    def test_branches(self) -> None:
        event = WorkflowRunEvent.model_validate(
            {
                "workflows": ["Build"],
                "branches": ["main"],
            },
        )

        assert_that(event.branches).is_equal_to(["main"])
        assert_that(event.workflows).contains("Build")
