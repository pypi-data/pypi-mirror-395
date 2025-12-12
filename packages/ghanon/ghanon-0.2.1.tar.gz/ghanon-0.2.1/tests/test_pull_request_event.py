from assertpy import assert_that

from ghanon.domain.workflow import PullRequestActivityType, PullRequestEvent


class TestPullRequestEvent:
    """Tests for pull_request event configuration."""

    def test_types(self) -> None:
        types = [
            PullRequestActivityType.OPENED,
            PullRequestActivityType.SYNCHRONIZE,
            PullRequestActivityType.REOPENED,
        ]
        event = PullRequestEvent.model_validate({"types": types})
        assert_that(event.types).contains(*types)

    def test_all_filters(self) -> None:
        event = PullRequestEvent.model_validate(
            {
                "types": [PullRequestActivityType.OPENED],
                "branches": ["main"],
                "paths": ["src/**"],
            },
        )
        assert_that(event.types).is_equal_to([PullRequestActivityType.OPENED])
        assert_that(event.branches).is_equal_to(["main"])
        assert_that(event.paths).is_equal_to(["src/**"])
