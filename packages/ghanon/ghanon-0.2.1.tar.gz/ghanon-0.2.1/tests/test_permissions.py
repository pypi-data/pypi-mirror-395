from assertpy import assert_that

from ghanon.domain.workflow import PermissionLevel, PermissionsEvent


class TestPermissions:
    def test_all_permissions(self) -> None:
        permissions = {
            "actions": PermissionLevel.READ,
            "attestations": PermissionLevel.WRITE,
            "checks": PermissionLevel.WRITE,
            "contents": PermissionLevel.READ,
            "deployments": PermissionLevel.WRITE,
            "discussions": PermissionLevel.READ,
            "id-token": PermissionLevel.WRITE,
            "issues": PermissionLevel.WRITE,
            "models": PermissionLevel.READ,
            "packages": PermissionLevel.WRITE,
            "pages": PermissionLevel.WRITE,
            "pull-requests": PermissionLevel.WRITE,
            "repository-projects": PermissionLevel.READ,
            "security-events": PermissionLevel.WRITE,
            "statuses": PermissionLevel.WRITE,
        }

        result = PermissionsEvent.model_validate(permissions)

        assert_that(result.actions).is_equal_to(PermissionLevel.READ)
        assert_that(result.attestations).is_equal_to(PermissionLevel.WRITE)
        assert_that(result.checks).is_equal_to(PermissionLevel.WRITE)
        assert_that(result.contents).is_equal_to(PermissionLevel.READ)
        assert_that(result.deployments).is_equal_to(PermissionLevel.WRITE)
        assert_that(result.discussions).is_equal_to(PermissionLevel.READ)
        assert_that(result.id_token).is_equal_to(PermissionLevel.WRITE)
        assert_that(result.issues).is_equal_to(PermissionLevel.WRITE)
        assert_that(result.models).is_equal_to(PermissionLevel.READ)
        assert_that(result.packages).is_equal_to(PermissionLevel.WRITE)
        assert_that(result.pages).is_equal_to(PermissionLevel.WRITE)
        assert_that(result.pull_requests).is_equal_to(PermissionLevel.WRITE)
        assert_that(result.repository_projects).is_equal_to(PermissionLevel.READ)
        assert_that(result.security_events).is_equal_to(PermissionLevel.WRITE)
        assert_that(result.statuses).is_equal_to(PermissionLevel.WRITE)
