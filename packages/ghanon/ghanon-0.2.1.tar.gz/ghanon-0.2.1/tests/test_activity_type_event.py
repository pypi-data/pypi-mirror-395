import pytest
from assertpy import assert_that

from ghanon.domain.workflow import (
    BranchProtectionRuleActivityType,
    BranchProtectionRuleEvent,
    CheckRunActivityType,
    CheckRunEvent,
    CheckSuiteActivityType,
    CheckSuiteEvent,
    DiscussionActivityType,
    DiscussionCommentActivityType,
    DiscussionCommentEvent,
    DiscussionEvent,
    IssueCommentActivityType,
    IssueCommentEvent,
    IssuesActivityType,
    IssuesEvent,
    LabelActivityType,
    LabelEvent,
    MergeGroupActivityType,
    MergeGroupEvent,
    MilestoneActivityType,
    MilestoneEvent,
    ProjectActivityType,
    ProjectCardActivityType,
    ProjectCardEvent,
    ProjectColumnActivityType,
    ProjectColumnEvent,
    ProjectEvent,
    PullRequestReviewActivityType,
    PullRequestReviewCommentActivityType,
    PullRequestReviewCommentEvent,
    PullRequestReviewEvent,
    RegistryPackageActivityType,
    RegistryPackageEvent,
    ReleaseActivityType,
    ReleaseEvent,
)


class TestActivityTypeEvent:
    @pytest.mark.parametrize(
        ("event_class", "types"),
        [
            (
                BranchProtectionRuleEvent,
                [
                    BranchProtectionRuleActivityType.CREATED,
                    BranchProtectionRuleActivityType.EDITED,
                    BranchProtectionRuleActivityType.DELETED,
                ],
            ),
            (
                CheckRunEvent,
                [
                    CheckRunActivityType.CREATED,
                    CheckRunActivityType.REREQUESTED,
                    CheckRunActivityType.COMPLETED,
                ],
            ),
            (
                CheckSuiteEvent,
                [CheckSuiteActivityType.COMPLETED, CheckSuiteActivityType.REQUESTED],
            ),
            (
                DiscussionEvent,
                [DiscussionActivityType.CREATED, DiscussionActivityType.ANSWERED],
            ),
            (
                DiscussionCommentEvent,
                [DiscussionCommentActivityType.CREATED, DiscussionCommentActivityType.EDITED],
            ),
            (
                IssueCommentEvent,
                [IssueCommentActivityType.CREATED, IssueCommentActivityType.DELETED],
            ),
            (
                IssuesEvent,
                [IssuesActivityType.OPENED, IssuesActivityType.CLOSED, IssuesActivityType.LABELED],
            ),
            (LabelEvent, [LabelActivityType.CREATED, LabelActivityType.DELETED]),
            (MergeGroupEvent, [MergeGroupActivityType.CHECKS_REQUESTED]),
            (
                MilestoneEvent,
                [MilestoneActivityType.CREATED, MilestoneActivityType.CLOSED],
            ),
            (ProjectEvent, [ProjectActivityType.CREATED, ProjectActivityType.CLOSED]),
            (
                ProjectCardEvent,
                [ProjectCardActivityType.CREATED, ProjectCardActivityType.MOVED],
            ),
            (
                ProjectColumnEvent,
                [ProjectColumnActivityType.CREATED, ProjectColumnActivityType.MOVED],
            ),
            (
                PullRequestReviewEvent,
                [
                    PullRequestReviewActivityType.SUBMITTED,
                    PullRequestReviewActivityType.DISMISSED,
                ],
            ),
            (
                PullRequestReviewCommentEvent,
                [
                    PullRequestReviewCommentActivityType.CREATED,
                    PullRequestReviewCommentActivityType.EDITED,
                ],
            ),
            (
                RegistryPackageEvent,
                [RegistryPackageActivityType.PUBLISHED, RegistryPackageActivityType.UPDATED],
            ),
            (
                ReleaseEvent,
                [ReleaseActivityType.PUBLISHED, ReleaseActivityType.RELEASED],
            ),
        ],
    )
    def test_activity_types(self, event_class, types) -> None:
        event = event_class.model_validate({"types": types})
        assert_that(event.types).contains(*types)
