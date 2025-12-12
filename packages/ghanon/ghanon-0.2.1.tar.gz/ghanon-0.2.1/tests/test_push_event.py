from assertpy import assert_that
from pydantic import ValidationError

from ghanon.domain.workflow import PushEvent


class TestPushEvent:
    def test_empty(self) -> None:
        event = PushEvent.model_validate({})
        assert_that(event.branches).is_none()

    def test_branches(self) -> None:
        branches = ["main", "develop"]
        event = PushEvent.model_validate({"branches": branches})
        assert_that(event.branches).is_equal_to(branches)

    def test_branches_ignore(self) -> None:
        ignored_branches = ["feature/*"]
        event = PushEvent.model_validate({"branches-ignore": ignored_branches})
        assert_that(event.branches_ignore).is_equal_to(ignored_branches)

    def test_branches_exclusive(self) -> None:
        assert_that(PushEvent.model_validate).raises(ValidationError).when_called_with(
            {"branches": ["main"], "branches-ignore": ["dev"]},
        )

    def test_tags(self) -> None:
        tags = ["v*"]
        event = PushEvent.model_validate({"tags": tags})
        assert_that(event.tags).is_equal_to(tags)

    def test_tags_ignore(self) -> None:
        tags = ["v0.*"]
        event = PushEvent.model_validate({"tags-ignore": tags})
        assert_that(event.tags_ignore).is_equal_to(tags)

    def test_tags_exclusive(self) -> None:
        assert_that(PushEvent.model_validate).raises(ValidationError).when_called_with(
            {"tags": ["v*"], "tags-ignore": ["v0.*"]},
        )

    def test_paths(self) -> None:
        paths = ["src/**", "*.py"]
        event = PushEvent.model_validate({"paths": paths})
        assert_that(event.paths).is_equal_to(paths)

    def test_paths_ignore(self) -> None:
        paths_ignore = ["docs/**", "*.md"]
        event = PushEvent.model_validate({"paths-ignore": paths_ignore})
        assert_that(event.paths_ignore).is_equal_to(paths_ignore)

    def test_paths_exclusive(self) -> None:
        assert_that(PushEvent.model_validate).raises(ValidationError).when_called_with(
            {"paths": ["src/**"], "paths-ignore": ["test/**"]},
        )
