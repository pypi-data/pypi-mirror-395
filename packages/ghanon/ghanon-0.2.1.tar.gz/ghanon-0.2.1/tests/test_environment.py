from assertpy import assert_that
from pydantic import ValidationError

from ghanon.domain.workflow import Environment


class TestEnvironment:
    def test_name_only(self) -> None:
        environment = Environment.model_validate({"name": "production"})
        assert_that(environment.name).is_equal_to("production")

    def test_with_url(self) -> None:
        url = "https://staging.example.com"
        environment = Environment.model_validate({"name": "staging", "url": url})
        assert_that(environment.url).is_equal_to(url)

    def test_name_required(self) -> None:
        assert_that(Environment.model_validate).raises(ValidationError).when_called_with({"url": "https://example.com"})
