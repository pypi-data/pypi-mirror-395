"""YAML parsing utilities for GitHub Actions Workflows."""

from __future__ import annotations

import yaml
from yaml.nodes import MappingNode, Node, ScalarNode, SequenceNode

__all__ = [
    "YamlLoader",
]


class YamlLoader:
    """Load and parse YAML content with line number tracking."""

    def load(self, yaml_content: str) -> dict:
        """Load YAML content into a dictionary.

        Args:
            yaml_content: The YAML content to parse.

        Returns:
            A dictionary representation of the YAML content.

        Raises:
            yaml.YAMLError: If the YAML content is invalid.

        """
        data = yaml.safe_load(yaml_content)

        # Handle YAML 1.1 quirk: 'on' key is parsed as boolean True
        # This is a known issue with GitHub Actions workflows
        if isinstance(data, dict) and True in data:
            data["on"] = data.pop(True)

        return data

    def build_line_map(self, yaml_content: str) -> dict[str, int]:
        """Build a mapping from location paths to line numbers in the YAML.

        Args:
            yaml_content: The YAML content to analyze.

        Returns:
            A dictionary mapping dotted paths to line numbers (1-indexed).

        """
        try:
            node = yaml.compose(yaml_content)
            if node is None:
                return {}
            return self._traverse_node(node, [])
        except yaml.YAMLError:
            return {}

    def _traverse_node(
        self,
        node: Node,
        path: list[str],
    ) -> dict[str, int]:
        """Recursively traverse YAML nodes to build line number mapping.

        Args:
            node: The current YAML node to traverse.
            path: The current path in the document as a list of keys.

        Returns:
            A dictionary mapping paths to line numbers.

        """
        if isinstance(node, MappingNode):
            return self._traverse_mapping_node(node, path)
        if isinstance(node, SequenceNode):
            return self._traverse_sequence_node(node, path)
        if isinstance(node, ScalarNode):
            return self._traverse_scalar_node(node, path)

        return {}  # pragma: no cover

    def _traverse_mapping_node(
        self,
        node: MappingNode,
        path: list[str],
    ) -> dict[str, int]:
        line_map: dict[str, int] = {}

        for key_node, value_node in node.value:
            if isinstance(key_node, ScalarNode):
                key = str(key_node.value)
                new_path = [*path, key]

                key_path = ".".join(new_path)
                line_map[key_path] = key_node.start_mark.line + 1
                line_map.update(self._traverse_node(value_node, new_path))

        return line_map

    def _traverse_sequence_node(
        self,
        node: SequenceNode,
        path: list[str],
    ) -> dict[str, int]:
        line_map: dict[str, int] = {}

        for index, item_node in enumerate(node.value):
            new_path = [*path, str(index)]
            line_map.update(self._traverse_node(item_node, new_path))

        return line_map

    def _traverse_scalar_node(
        self,
        node: ScalarNode,
        path: list[str],
    ) -> dict[str, int]:
        current_path = ".".join(path) if path else ""

        if current_path:
            return {current_path: node.start_mark.line + 1}

        return {}
