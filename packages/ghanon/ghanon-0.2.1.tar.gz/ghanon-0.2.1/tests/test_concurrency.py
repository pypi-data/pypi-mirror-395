from assertpy import assert_that
from pydantic import ValidationError

from ghanon.domain.workflow import Concurrency


class TestConcurrency:
    def test_group_only(self) -> None:
        concurrency = Concurrency.model_validate({"group": "ci-${{ github.ref }}"})
        assert_that(concurrency.group).is_equal_to("ci-${{ github.ref }}")
        assert_that(concurrency.cancel_in_progress).is_none()

    def test_with_cancel(self) -> None:
        concurrency = Concurrency.model_validate({"group": "deploy", "cancel-in-progress": True})
        assert_that(concurrency.cancel_in_progress).is_true()

    def test_cancel_expression(self) -> None:
        concurrency = Concurrency.model_validate(
            {
                "group": "ci",
                "cancel-in-progress": "${{ github.event_name == 'pull_request' }}",
            },
        )
        assert_that(concurrency.cancel_in_progress).contains("${{")

    def test_group_required(self) -> None:
        assert_that(Concurrency.model_validate).raises(ValidationError).when_called_with({"cancel-in-progress": True})
