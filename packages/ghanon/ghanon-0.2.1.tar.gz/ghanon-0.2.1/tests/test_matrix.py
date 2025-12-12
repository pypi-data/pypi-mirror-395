import pytest
from assertpy import assert_that

from ghanon.domain.workflow import Matrix, Strategy


@pytest.fixture
def minimal_config() -> dict[str, dict[str, list[str]]]:
    """Provide a minimal matrix strategy configuration."""
    return {
        "matrix": {
            "os": ["ubuntu-latest", "macos-latest", "windows-latest"],
        },
    }


class TestMatrix:
    def test_simple_matrix(self, minimal_config) -> None:
        strategy = Strategy.model_validate(minimal_config)
        assert_that(strategy.matrix).is_instance_of(Matrix)

    def test_matrix_with_include(self, minimal_config) -> None:
        include = [{"os": "ubuntu-latest", "node": "21", "experimental": True}]

        strategy = Strategy.model_validate(
            {
                **minimal_config,
                "matrix": {
                    "node": ["18", "20"],
                    "include": include,
                },
            },
        )

        assert isinstance(strategy.matrix, Matrix)
        assert_that(strategy.matrix.include).is_equal_to(include)

    def test_matrix_with_exclude(self, minimal_config) -> None:
        exclude = [{"os": "windows-latest", "node": "18"}]

        strategy = Strategy.model_validate(
            {
                **minimal_config,
                "matrix": {
                    "node": ["22", "24"],
                    "exclude": exclude,
                },
            },
        )

        assert isinstance(strategy.matrix, Matrix)
        assert_that(strategy.matrix.exclude).is_equal_to(exclude)

    def test_fail_fast_true(self, minimal_config) -> None:
        strategy = Strategy.model_validate({**minimal_config, "fail-fast": True})
        assert_that(strategy.fail_fast).is_true()

    def test_fail_fast_false(self, minimal_config) -> None:
        strategy = Strategy.model_validate({**minimal_config, "fail-fast": False})
        assert_that(strategy.fail_fast).is_false()

    def test_max_parallel(self, minimal_config) -> None:
        parallel_jobs = 2
        strategy = Strategy.model_validate({**minimal_config, "max-parallel": parallel_jobs})
        assert_that(strategy.max_parallel).is_equal_to(parallel_jobs)

    def test_matrix_expression(self, minimal_config) -> None:
        expression = "${{ fromJson(needs.setup.outputs.matrix) }}"
        strategy = Strategy.model_validate({**minimal_config, "matrix": expression})
        assert_that(strategy.matrix).is_equal_to(expression)
