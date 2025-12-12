from assertpy import assert_that

from ghanon.domain.workflow import ScheduleItem


class TestScheduleEvent:
    """Tests for schedule event configuration."""

    def test_single_cron(self) -> None:
        pattern = "0 0 * * *"
        item = ScheduleItem.model_validate({"cron": pattern})
        assert_that(item.cron).is_equal_to(pattern)
