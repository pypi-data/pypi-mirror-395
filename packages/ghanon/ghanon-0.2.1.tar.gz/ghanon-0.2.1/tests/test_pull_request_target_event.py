from assertpy import assert_that
from pydantic import ValidationError

from ghanon.domain.workflow import PullRequestActivityType, PullRequestTargetEvent


class TestPullRequestTargetEvent:
    def test_types(self) -> None:
        types = [PullRequestActivityType.LABELED, PullRequestActivityType.OPENED]
        event = PullRequestTargetEvent.model_validate({"types": types})
        assert_that(event.types).contains(*types)

    def test_filter_exclusivity(self) -> None:
        assert_that(PullRequestTargetEvent.model_validate).raises(ValidationError).when_called_with(
            {
                "branches": ["main"],
                "branches-ignore": ["feature/*"],
            },
        )
