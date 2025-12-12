from __future__ import annotations

from assertpy import assert_that

from ghanon.yaml import YamlLoader


class TestYamlLoader:
    loader = YamlLoader()

    def test_build_regular_line_map(self) -> None:
        yaml_content = "name: Example Workflow"

        result = self.loader.build_line_map(yaml_content)

        assert_that(result).contains_entry({"name": 1})

    def test_build_empty_line_map(self) -> None:
        yaml_content = "name"

        result = self.loader.build_line_map(yaml_content)

        assert_that(result).is_empty()

    def test_build_line_map_with_empty_yaml(self) -> None:
        yaml_content = ""

        result = self.loader.build_line_map(yaml_content)

        assert_that(result).is_empty()
