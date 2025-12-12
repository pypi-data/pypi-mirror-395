from datetime import date

from whatnext.models import MarkdownFile, Priority, Task, State


class TestTask:
    task = Task(
        # filename
        None,

        # header
        "# Indicating the state of a task / Multiline tasks and indentation",

        # text
        "Lorem ipsum dolor sit amet, consectetur adipisicing elit, "
        "sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",

        # state
        State.OPEN,

        # priority
        Priority.NORMAL,
    )

    def test_wraps_at_40_chars(self):
        assert self.task.wrapped_task(width=40) == [
            "    - [ ] Lorem ipsum dolor sit amet,",
            "          consectetur adipisicing elit,",
            "          sed do eiusmod tempor",
            "          incididunt ut labore et dolore",
            "          magna aliqua.",
        ]
        assert self.task.wrapped_heading(width=40) == [
            "    # Indicating the state of a task /",
            "      Multiline tasks and indentation",
        ]

    def test_no_wrap_at_120_chars(self):
        assert self.task.wrapped_task(width=120) == [
            "    - [ ] Lorem ipsum dolor sit amet, consectetur adipisicing elit, "
            "sed do eiusmod tempor incididunt ut labore et dolore",
            "          magna aliqua.",
        ]
        assert self.task.wrapped_heading(width=120) == [
            "    # Indicating the state of a task / Multiline tasks and indentation"
        ]

    def test_default_width_80_chars(self):
        assert self.task.wrapped_task() == [
            "    - [ ] Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do",  # noqa: E501
            "          eiusmod tempor incididunt ut labore et dolore magna aliqua.",
        ]
        assert self.task.wrapped_heading() == [
            "    # Indicating the state of a task / Multiline tasks and indentation"
        ]


class TestOverdueHeading:
    def test_overdue_by_1_day(self):
        file = MarkdownFile(
            source_string="# Tasks\n- [ ] do thing @2025-01-01",
            today=date(2025, 1, 2),
        )
        task = file.tasks[0]
        assert task.wrapped_heading() == ["    # Tasks / OVERDUE 1d"]

    def test_overdue_by_3_days(self):
        file = MarkdownFile(
            source_string="# Tasks\n- [ ] do thing @2025-01-01",
            today=date(2025, 1, 4),
        )
        task = file.tasks[0]
        assert task.wrapped_heading() == ["    # Tasks / OVERDUE 3d"]

    def test_overdue_by_1_week(self):
        file = MarkdownFile(
            source_string="# Tasks\n- [ ] do thing @2025-01-01",
            today=date(2025, 1, 11),
        )
        task = file.tasks[0]
        assert task.wrapped_heading() == ["    # Tasks / OVERDUE 10d"]

    def test_overdue_by_2_weeks(self):
        file = MarkdownFile(
            source_string="# Tasks\n- [ ] do thing @2025-01-01",
            today=date(2025, 1, 17),
        )
        task = file.tasks[0]
        assert task.wrapped_heading() == ["    # Tasks / OVERDUE 2w 2d"]

    def test_overdue_by_5_weeks(self):
        file = MarkdownFile(
            source_string="# Tasks\n- [ ] do thing @2025-01-01",
            today=date(2025, 2, 10),
        )
        task = file.tasks[0]
        assert task.wrapped_heading() == ["    # Tasks / OVERDUE 1m 1w"]

    def test_overdue_by_10_years(self):
        file = MarkdownFile(
            source_string="# Tasks\n- [ ] do thing @2015-01-01",
            today=date(2025, 11, 1),
        )
        task = file.tasks[0]
        assert task.wrapped_heading() == ["    # Tasks / OVERDUE 10y 10m"]


class TestImminentHeading:
    def test_imminent_1_day_left(self):
        file = MarkdownFile(
            source_string="# Tasks\n- [ ] do thing @2025-01-10",
            today=date(2025, 1, 9),
        )
        task = file.tasks[0]
        assert task.wrapped_heading() == ["    # Tasks / IMMINENT 1d"]

    def test_imminent_3_days_left(self):
        file = MarkdownFile(
            source_string="# Tasks\n- [ ] do thing @2025-01-10",
            today=date(2025, 1, 7),
        )
        task = file.tasks[0]
        assert task.wrapped_heading() == ["    # Tasks / IMMINENT 3d"]

    def test_imminent_2_weeks_left(self):
        file = MarkdownFile(
            source_string="# Tasks\n- [ ] do thing @2025-01-20/3w",
            today=date(2025, 1, 4),
        )
        task = file.tasks[0]
        assert task.wrapped_heading() == ["    # Tasks / IMMINENT 2w 2d"]

    def test_imminent_on_deadline_day(self):
        file = MarkdownFile(
            source_string="# Tasks\n- [ ] do thing @2025-01-10",
            today=date(2025, 1, 10),
        )
        task = file.tasks[0]
        assert task.wrapped_heading() == ["    # Tasks / IMMINENT TODAY"]
