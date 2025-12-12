import pytest
from assertpy import assert_that

from ghanon.domain.workflow import Container, Environment, NormalJob, RunnerGroup


@pytest.fixture
def minimal_config() -> dict[str, str]:
    """Provide a minimal configuration for NormalJob."""
    return {
        "runs-on": "ubuntu-latest",
    }


class TestNormalJob:
    def test_minimal(self, minimal_config) -> None:
        job = NormalJob.model_validate(minimal_config)
        assert_that(job.runs_on).is_equal_to(minimal_config["runs-on"])

    def test_with_steps(self, minimal_config) -> None:
        command = "echo test"

        job = NormalJob.model_validate(
            {
                **minimal_config,
                "steps": [{"run": command}],
            },
        )

        assert job.steps is not None
        assert_that(job.steps[0].run).is_equal_to(command)

    def test_name(self, minimal_config) -> None:
        name = "Build Job"
        job = NormalJob.model_validate({**minimal_config, "name": name})
        assert_that(job.name).is_equal_to(name)

    def test_needs_single(self, minimal_config) -> None:
        needs = "build"
        job = NormalJob.model_validate({**minimal_config, "needs": needs})
        assert_that(job.needs).is_equal_to(needs)

    def test_needs_multiple(self, minimal_config) -> None:
        needs = ["build", "test"]
        job = NormalJob.model_validate({**minimal_config, "needs": needs})
        assert_that(job.needs).is_equal_to(needs)

    def test_if_condition(self, minimal_config) -> None:
        condition = "github.ref == 'refs/heads/main'"

        job = NormalJob.model_validate(
            {
                **minimal_config,
                "if": condition,
            },
        )

        assert_that(job.if_).is_equal_to(condition)

    def test_environment_string(self, minimal_config) -> None:
        environment = "production"
        job = NormalJob.model_validate({**minimal_config, "environment": environment})
        assert_that(job.environment).is_equal_to(environment)

    def test_environment_object(self, minimal_config) -> None:
        environment = "production"
        url = "https://example.com"

        job = NormalJob.model_validate(
            {
                **minimal_config,
                "environment": {"name": environment, "url": url},
            },
        )

        assert isinstance(job.environment, Environment)
        assert_that(job.environment.name).is_equal_to(environment)
        assert_that(job.environment.url).is_equal_to(url)

    def test_outputs(self, minimal_config) -> None:
        version = "${{ steps.get_version.outputs.version }}"

        job = NormalJob.model_validate(
            {
                **minimal_config,
                "outputs": {"version": version},
            },
        )

        assert isinstance(job.outputs, dict)
        assert_that(job.outputs["version"]).is_equal_to(version)

    def test_env(self, minimal_config) -> None:
        port = 3000

        job = NormalJob.model_validate(
            {
                **minimal_config,
                "env": {"DEBUG": "true", "PORT": port},
            },
        )

        assert_that(job.env).contains_entry({"DEBUG": "true"})
        assert_that(job.env).contains_entry({"PORT": port})

    def test_timeout_minutes(self, minimal_config) -> None:
        timeout = 30
        job = NormalJob.model_validate({**minimal_config, "timeout-minutes": timeout})
        assert_that(job.timeout_minutes).is_equal_to(timeout)

    def test_continue_on_error(self, minimal_config) -> None:
        job = NormalJob.model_validate({**minimal_config, "continue-on-error": True})
        assert_that(job.continue_on_error).is_true()

    def test_container_string(self, minimal_config) -> None:
        job = NormalJob.model_validate({**minimal_config, "container": "node:18"})
        assert_that(job.container).is_equal_to("node:18")

    def test_container_object(self, minimal_config) -> None:
        image = "node:24"
        ports = [80, "443:443"]
        env = {"NODE_ENV": "test"}
        volumes = ["/tmp:/tmp"]
        options = "--cpus 2"

        job = NormalJob.model_validate(
            {
                **minimal_config,
                "container": {
                    "image": image,
                    "ports": ports,
                    "env": env,
                    "volumes": volumes,
                    "options": options,
                },
            },
        )

        assert isinstance(job.container, Container)
        assert_that(job.container.image).is_equal_to(image)
        assert_that(job.container.ports).is_equal_to(ports)
        assert_that(job.container.env).is_equal_to(env)
        assert_that(job.container.volumes).is_equal_to(volumes)
        assert_that(job.container.options).is_equal_to(options)

    def test_services(self, minimal_config) -> None:
        job = NormalJob.model_validate(
            {
                **minimal_config,
                "services": {
                    "postgres": {
                        "image": "postgres:15",
                        "env": {"POSTGRES_PASSWORD": "test"},
                    },
                    "redis": {"image": "redis:7"},
                },
            },
        )

        assert_that(job.services).contains_key("postgres", "redis")

    def test_runs_on_array(self) -> None:
        labels = ["self-hosted", "linux", "x64"]
        job = NormalJob.model_validate({"runs-on": labels})
        assert_that(job.runs_on).is_equal_to(labels)

    def test_runs_on_group(self) -> None:
        labels = ["ubuntu-latest"]
        group = "large-runners"

        job = NormalJob.model_validate(
            {
                "runs-on": {"group": group, "labels": labels},
            },
        )

        assert isinstance(job.runs_on, RunnerGroup)
        assert_that(job.runs_on.group).is_equal_to(group)
        assert_that(job.runs_on.labels).is_equal_to(labels)

    def test_runs_on_expression(self) -> None:
        label = "${{ matrix.os }}"
        job = NormalJob.model_validate({"runs-on": label})
        assert_that(job.runs_on).is_equal_to(label)

    def test_expression_in_timeout(self, minimal_config) -> None:
        timeout = "${{ inputs.timeout }}"

        job = NormalJob.model_validate(
            {
                **minimal_config,
                "timeout-minutes": timeout,
            },
        )

        assert_that(job.timeout_minutes).is_equal_to(timeout)
