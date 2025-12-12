import pytest
from assertpy import assert_that
from pydantic import ValidationError

from ghanon.domain.workflow import Step

command = "echo hello"
uses = "actions/checkout@v4"


class TestStep:
    def test_run_only(self) -> None:
        step = Step.model_validate({"run": command})
        assert_that(step.run).is_equal_to(command)

    def test_uses_only(self) -> None:
        step = Step.model_validate({"uses": uses})
        assert_that(step.uses).is_equal_to(uses)

    def test_requires_uses_or_run(self) -> None:
        assert_that(Step.model_validate).raises(ValidationError).when_called_with({"name": "Invalid"})

    def test_cannot_have_both(self) -> None:
        assert_that(Step.model_validate).raises(ValidationError).when_called_with(
            {"uses": uses, "run": command},
        )

    def test_id(self) -> None:
        identifier = "my-step"
        step = Step.model_validate({"id": identifier, "run": command})
        assert_that(step.id).is_equal_to(identifier)

    def test_name(self) -> None:
        name = "Build"
        step = Step.model_validate({"name": name, "run": command})
        assert_that(step.name).is_equal_to(name)

    def test_if_string(self) -> None:
        condition = "success()"
        step = Step.model_validate({"run": command, "if": condition})
        assert_that(step.if_).is_equal_to(condition)

    def test_if_true(self) -> None:
        step = Step.model_validate({"run": command, "if": True})
        assert_that(step.if_).is_true()

    def test_if_false(self) -> None:
        step = Step.model_validate({"run": command, "if": False})
        assert_that(step.if_).is_false()

    def test_with(self) -> None:
        options = {"node-version": "24", "cache": "npm"}

        step = Step.model_validate(
            {
                "uses": "actions/setup-node@v4",
                "with": options,
            },
        )

        assert_that(step.with_).is_equal_to(options)

    def test_env(self) -> None:
        environment = {"VAR": "value"}
        step = Step.model_validate({"run": command, "env": environment})
        assert_that(step.env).is_equal_to(environment)

    def test_shell(self) -> None:
        shell = "bash"
        step = Step.model_validate({"run": command, "shell": shell})
        assert_that(step.shell).is_equal_to(shell)

    def test_working_directory(self) -> None:
        working_directory = "./app"
        step = Step.model_validate({"run": command, "working-directory": working_directory})
        assert_that(step.working_directory).is_equal_to(working_directory)

    def test_shell_requires_run(self) -> None:
        assert_that(Step.model_validate).raises(ValidationError).when_called_with(
            {"uses": "actions/checkout@v4", "shell": "bash"},
        )

    def test_working_directory_requires_run(self) -> None:
        assert_that(Step.model_validate).raises(ValidationError).when_called_with(
            {"uses": "actions/checkout@v4", "working-directory": "./app"},
        )

    def test_continue_on_error_true(self) -> None:
        step = Step.model_validate({"run": "echo", "continue-on-error": True})
        assert_that(step.continue_on_error).is_true()

    def test_continue_on_error_false(self) -> None:
        step = Step.model_validate({"run": "echo", "continue-on-error": False})
        assert_that(step.continue_on_error).is_false()

    def test_timeout_minutes(self) -> None:
        timeout = 60
        step = Step.model_validate({"run": "long-task", "timeout-minutes": timeout})
        assert_that(step.timeout_minutes).is_equal_to(timeout)

    def test_multiline_run(self) -> None:
        step = Step.model_validate(
            {
                "run": """|
                    echo "Line 1"
                    echo "Line 2"
                    echo "Line 3"
                """,
            },
        )

        assert_that(step.run).contains("|", "Line 1", "Line 2", "Line 3")

    @pytest.mark.parametrize("shell", ["bash", "pwsh", "python", "sh", "cmd", "powershell"])
    def test_shell_types(self, shell) -> None:
        step = Step.model_validate({"run": "echo", "shell": shell})
        assert_that(step.shell).is_equal_to(shell)
