from assertpy import assert_that

from ghanon.domain.workflow import Container


class TestContainer:
    def test_image_only(self) -> None:
        container = Container.model_validate({"image": "node:24"})
        assert_that(container.image).is_equal_to("node:24")

    def test_with_credentials(self) -> None:
        container = Container.model_validate(
            {
                "image": "ghcr.io/owner/image",
                "credentials": {
                    "username": "user",
                    "password": "${{ secrets.TOKEN }}",
                },
            },
        )

        assert container.credentials is not None
        assert_that(container.credentials.username).is_equal_to("user")

    def test_with_env(self) -> None:
        container = Container.model_validate({"image": "node:24", "env": {"NODE_ENV": "test"}})
        assert_that(container.env).contains_entry({"NODE_ENV": "test"})

    def test_with_ports(self) -> None:
        ports = [80, 443, "8080:80"]
        container = Container.model_validate({"image": "nginx", "ports": ports})
        assert_that(container.ports).contains(*ports)

    def test_with_volumes(self) -> None:
        volumes = ["/tmp:/tmp", "my-vol:/data"]
        container = Container.model_validate(
            {
                "image": "node:24",
                "volumes": volumes,
            },
        )
        assert_that(container.volumes).contains(*volumes)

    def test_with_options(self) -> None:
        container = Container.model_validate({"image": "node:24", "options": "--cpus 2 --memory 4g"})
        assert_that(container.options).contains("--cpus 2", "--memory 4g")
