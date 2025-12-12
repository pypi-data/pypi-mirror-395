from datetime import date
from textwrap import dedent

from whatnext.models import MarkdownFile, Priority, State


class TestFileParsing:
    def test_open_task(self):
        file = MarkdownFile(
            source_string="- [ ] open, this task is outstanding",
            today=date(2025, 1, 1),
        )
        assert len(file.tasks) == 1
        assert file.tasks[0].as_dict() == {
            "heading": None,
            "state": State.OPEN,
            "text": "open, this task is outstanding",
            "priority": Priority.NORMAL,
            "due": None,
            "imminent": None,
            "annotation": None,
        }

    def test_in_progress_task(self):
        file = MarkdownFile(
            source_string="- [/] in progress, this task is partially complete",
            today=date(2025, 1, 1),
        )
        assert file.tasks[0].as_dict() == {
            "heading": None,
            "state": State.IN_PROGRESS,
            "text": "in progress, this task is partially complete",
            "priority": Priority.NORMAL,
            "due": None,
            "imminent": None,
            "annotation": None,
        }

    def test_complete_task(self):
        file = MarkdownFile(
            source_string="- [X] complete, this task has been finished",
            today=date(2025, 1, 1),
        )
        assert file.tasks[0].as_dict() == {
            "heading": None,
            "state": State.COMPLETE,
            "text": "complete, this task has been finished",
            "priority": None,
            "due": None,
            "imminent": None,
            "annotation": None,
        }

    def test_cancelled_task(self):
        file = MarkdownFile(
            source_string="- [#] cancelled, this task has been scratched",
            today=date(2025, 1, 1),
        )
        assert file.tasks[0].as_dict() == {
            "heading": None,
            "state": State.CANCELLED,
            "text": "cancelled, this task has been scratched",
            "priority": None,
            "due": None,
            "imminent": None,
            "annotation": None,
        }

    def test_blocked_task(self):
        file = MarkdownFile(
            source_string="- [<] blocked, this task needs more input",
            today=date(2025, 1, 1),
        )
        assert file.tasks[0].as_dict() == {
            "heading": None,
            "state": State.BLOCKED,
            "text": "blocked, this task needs more input",
            "priority": Priority.NORMAL,
            "due": None,
            "imminent": None,
            "annotation": None,
        }

    def test_multiline_task(self):
        file = MarkdownFile(
            source_string=dedent("""\
                - [ ] Lorem ipsum dolor sit amet,
                      consectetur adipisicing elit,
                      sed do  eiusmod  tempor   incididunt
                      ut labore et     dolore magna aliqua.
            """),
            today=date(2025, 1, 1),
        )
        assert file.tasks[0].as_dict() == {
            "heading": None,
            "state": State.OPEN,
            "text": (
                "Lorem ipsum dolor sit amet, "
                "consectetur adipisicing elit, "
                "sed do eiusmod tempor incididunt "
                "ut labore et dolore magna aliqua."
            ),
            "priority": Priority.NORMAL,
            "due": None,
            "imminent": None,
            "annotation": None,
        }

    def test_multiline_task_wrong_indent(self):
        file = MarkdownFile(
            source_string=dedent("""\
                - [ ] Ut enim ad minim veniam,
                     quis nostrud exercitation ullamco laboris
            """),
            today=date(2025, 1, 1),
        )
        assert file.tasks[0].as_dict() == {
            "heading": None,
            "state": State.OPEN,
            "text": "Ut enim ad minim veniam,",
            "priority": Priority.NORMAL,
            "due": None,
            "imminent": None,
            "annotation": None,
        }

    def test_normal_priority(self):
        file = MarkdownFile(
            source_string="- [ ] top, but not urgent, task",
            today=date(2025, 1, 1),
        )
        assert file.tasks[0].as_dict() == {
            "heading": None,
            "state": State.OPEN,
            "text": "top, but not urgent, task",
            "priority": Priority.NORMAL,
            "due": None,
            "imminent": None,
            "annotation": None,
        }

    def test_medium_priority(self):
        file = MarkdownFile(
            source_string="- [ ] _semi-urgent task_",
            today=date(2025, 1, 1),
        )
        assert file.tasks[0].as_dict() == {
            "heading": None,
            "state": State.OPEN,
            "text": "semi-urgent task",
            "priority": Priority.MEDIUM,
            "due": None,
            "imminent": None,
            "annotation": None,
        }

    def test_high_priority(self):
        file = MarkdownFile(
            source_string="- [ ] **super-urgent task**",
            today=date(2025, 1, 1),
        )
        assert file.tasks[0].as_dict() == {
            "heading": None,
            "state": State.OPEN,
            "text": "super-urgent task",
            "priority": Priority.HIGH,
            "due": None,
            "imminent": None,
            "annotation": None,
        }

    def test_priority_from_header_and_precedence(self):
        file = MarkdownFile(
            source_string=dedent("""\
                - [/] not a high priority task

                # **do these first**

                - [ ] inherently high priority task, because of the header
                - [ ] **no extra priority, still listed second**

                ## grouped, but still highest priority

                - [X] header priority cascades down

                # more tasks

                - [#] normal priority, new header resets that
            """),
            today=date(2025, 1, 1),
        )
        assert len(file.tasks) == 5
        assert file.tasks[0].as_dict() == {
            "heading": None,
            "state": State.IN_PROGRESS,
            "text": "not a high priority task",
            "priority": Priority.NORMAL,
            "due": None,
            "imminent": None,
            "annotation": None,
        }
        assert file.tasks[1].as_dict() == {
            "heading": "# do these first",
            "state": State.OPEN,
            "text": "inherently high priority task, because of the header",
            "priority": Priority.HIGH,
            "due": None,
            "imminent": None,
            "annotation": None,
        }
        assert file.tasks[2].as_dict() == {
            "heading": "# do these first",
            "state": State.OPEN,
            "text": "no extra priority, still listed second",
            "priority": Priority.HIGH,
            "due": None,
            "imminent": None,
            "annotation": None,
        }
        assert file.tasks[3].as_dict() == {
            "heading": "# do these first / grouped, but still highest priority",
            "state": State.COMPLETE,
            "text": "header priority cascades down",
            "priority": None,
            "due": None,
            "imminent": None,
            "annotation": None,
        }
        assert file.tasks[4].as_dict() == {
            "heading": "# more tasks",
            "state": State.CANCELLED,
            "text": "normal priority, new header resets that",
            "priority": None,
            "due": None,
            "imminent": None,
            "annotation": None,
        }

    def test_high_task_under_medium_header(self):
        file = MarkdownFile(
            source_string=dedent("""\
                # _Medium section_

                - [ ] **high priority task**
            """),
            today=date(2025, 1, 1),
        )
        assert file.tasks[0].as_dict() == {
            "heading": "# Medium section",
            "state": State.OPEN,
            "text": "high priority task",
            "priority": Priority.HIGH,
            "due": None,
            "imminent": None,
            "annotation": None,
        }

    def test_medium_task_under_high_header(self):
        file = MarkdownFile(
            source_string=dedent("""\
                # **High section**

                - [ ] _medium priority task_
            """),
            today=date(2025, 1, 1),
        )
        assert file.tasks[0].as_dict() == {
            "heading": "# High section",
            "state": State.OPEN,
            "text": "medium priority task",
            "priority": Priority.HIGH,
            "due": None,
            "imminent": None,
            "annotation": None,
        }

    def test_medium_subsection_under_high_header(self):
        file = MarkdownFile(
            source_string=dedent("""\
                # **High section**

                ## _Medium subsection_

                - [ ] task in medium subsection
            """),
            today=date(2025, 1, 1),
        )
        assert file.tasks[0].as_dict() == {
            "heading": "# High section / Medium subsection",
            "state": State.OPEN,
            "text": "task in medium subsection",
            "priority": Priority.HIGH,
            "due": None,
            "imminent": None,
            "annotation": None,
        }

    def test_simple_deadline(self):
        file = MarkdownFile(
            source_string=dedent("""\
                # version 0.5
                - [ ] complete and release @2025-12-05
            """),
            today=date(2025, 1, 1),
        )
        assert file.tasks[0].as_dict() == {
            "heading": "# version 0.5",
            "state": State.OPEN,
            "text": "complete and release",
            "priority": Priority.NORMAL,
            "due": date(2025, 12, 5),
            "imminent": date(2025, 11, 21),
            "annotation": None,
        }

    def test_deadline_outside_urgency_window_no_priority(self):
        file = MarkdownFile(
            source_string=dedent("""\
                # Christmas dinner
                - [ ] book Christmas delivery @2025-12-23/3w
                - [ ] _prep the make-ahead gravy_ @2025-12-25/1d
                - [ ] **roast the potatoes** @2025-12-25/0d
            """),
            today=date(2025, 12, 1),
        )
        assert file.tasks[0].as_dict() == {
            "heading": "# Christmas dinner",
            "state": State.OPEN,
            "text": "book Christmas delivery",
            "priority": Priority.NORMAL,
            "due": date(2025, 12, 23),
            "imminent": date(2025, 12, 2),
            "annotation": None,
        }
        assert file.tasks[1].as_dict() == {
            "heading": "# Christmas dinner",
            "state": State.OPEN,
            "text": "prep the make-ahead gravy",
            "priority": Priority.NORMAL,
            "due": date(2025, 12, 25),
            "imminent": date(2025, 12, 24),
            "annotation": None,
        }
        assert file.tasks[2].as_dict() == {
            "heading": "# Christmas dinner",
            "state": State.OPEN,
            "text": "roast the potatoes",
            "priority": Priority.NORMAL,
            "due": date(2025, 12, 25),
            "imminent": date(2025, 12, 25),
            "annotation": None,
        }

    def test_deadline_inside_urgency_gains_imminent_priority(self):
        file = MarkdownFile(
            source_string=dedent("""\
                # Christmas dinner
                - [ ] book Christmas delivery @2025-12-23/3w
                - [ ] _prep the make-ahead gravy_ @2025-12-25/1d
                - [ ] **roast the potatoes** @2025-12-25/0d
            """),
            today=date(2025, 12, 15),
        )
        assert file.tasks[0].priority == Priority.IMMINENT
        assert file.tasks[1].priority == Priority.NORMAL
        assert file.tasks[2].priority == Priority.NORMAL

    def test_deadline_inside_urgency_regains_priority(self):
        file = MarkdownFile(
            source_string=dedent("""\
                # Christmas dinner
                - [ ] book Christmas delivery @2025-12-23/3w
                - [ ] _prep the make-ahead gravy_ @2025-12-25/1d
                - [ ] **roast the potatoes** @2025-12-25/0d
            """),
            today=date(2025, 12, 24),
        )
        assert file.tasks[0].priority == Priority.OVERDUE
        assert file.tasks[1].priority == Priority.MEDIUM
        assert file.tasks[2].priority == Priority.NORMAL

    def test_deadline_past_deadline_always_overdue(self):
        file = MarkdownFile(
            source_string=dedent("""\
                # Christmas dinner
                - [ ] book Christmas delivery @2025-12-22/3w
                - [ ] _prep the make-ahead gravy_ @2025-12-25/1d
                - [ ] **roast the potatoes** @2025-12-25/0d
            """),
            today=date(2025, 12, 26),
        )
        assert file.tasks[0].priority == Priority.OVERDUE
        assert file.tasks[1].priority == Priority.OVERDUE
        assert file.tasks[2].priority == Priority.OVERDUE

    def test_invalid_date_ignored(self):
        file = MarkdownFile(
            source_string="- [ ] task with bad date @2025-13-45",
            today=date(2025, 1, 1),
        )
        assert file.tasks[0].as_dict() == {
            "heading": None,
            "state": State.OPEN,
            "text": "task with bad date @2025-13-45",
            "priority": Priority.NORMAL,
            "due": None,
            "imminent": None,
            "annotation": None,
        }

    def test_non_date_format_ignored(self):
        file = MarkdownFile(
            source_string="- [ ] task with text @december-25",
            today=date(2025, 1, 1),
        )
        assert file.tasks[0].as_dict() == {
            "heading": None,
            "state": State.OPEN,
            "text": "task with text @december-25",
            "priority": Priority.NORMAL,
            "due": None,
            "imminent": None,
            "annotation": None,
        }

    def test_invalid_urgency_invalidates_deadline(self):
        file = MarkdownFile(
            source_string="- [ ] promote Random Task @2025-12-15/3m",
            today=date(2025, 1, 1),
        )
        assert file.tasks[0].as_dict() == {
            "heading": None,
            "state": State.OPEN,
            "text": "promote Random Task @2025-12-15/3m",
            "priority": Priority.NORMAL,
            "due": None,
            "imminent": None,
            "annotation": None,
        }

    def test_email_not_deadline(self):
        file = MarkdownFile(
            source_string="- [ ] email user@2025-12-15.com",
            today=date(2025, 1, 1),
        )
        assert file.tasks[0].as_dict() == {
            "heading": None,
            "state": State.OPEN,
            "text": "email user@2025-12-15.com",
            "priority": Priority.NORMAL,
            "due": None,
            "imminent": None,
            "annotation": None,
        }


class GroupedTasksTestCase:
    def tasks(self, grouped_tasks):
        return tuple(
            [
                (task.heading, task.text, task.state, task.priority)
                for task in group
            ]
            for group in grouped_tasks
        )


class TestGroupedTasksBasics(GroupedTasksTestCase):
    file = MarkdownFile(source="docs/basics.md", today=date.today())

    def test_no_args_returns_all_grouped_by_priority(self):
        assert self.tasks(self.file.grouped_tasks()) == (
            [],
            [],
            [],
            [],
            [
                (
                    "# Indicating the state of a task",
                    "in progress, this task is partially complete",
                    State.IN_PROGRESS,
                    Priority.NORMAL
                ),
                (
                    "# Indicating the state of a task",
                    "open, this task is outstanding",
                    State.OPEN,
                    Priority.NORMAL
                ),
                (
                    "# Indicating the state of a task",
                    "blocked, this task needs more input",
                    State.BLOCKED,
                    Priority.NORMAL
                ),
                (
                    "# Indicating the state of a task / Multiline tasks and indentation",  # noqa: E501
                    "Lorem ipsum dolor sit amet, consectetur adipisicing elit, "
                    "sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",  # noqa: E501
                    State.OPEN,
                    Priority.NORMAL
                ),
                (
                    "# Indicating the state of a task / Multiline tasks and indentation",  # noqa: E501
                    "Ut enim ad minim veniam,",
                    State.OPEN,
                    Priority.NORMAL
                ),
            ],
            [
                (
                    "# Indicating the state of a task",
                    "complete, this task has been finished",
                    State.COMPLETE,
                    None
                ),
                (
                    "# Indicating the state of a task",
                    "cancelled, this task has been scratched",
                    State.CANCELLED,
                    None
                ),
            ],
        )

    def test_state_two_selected(self):
        assert self.tasks(
            self.file.grouped_tasks(states={State.IN_PROGRESS, State.BLOCKED})
        ) == (
            [],
            [],
            [],
            [],
            [
                (
                    "# Indicating the state of a task",
                    "in progress, this task is partially complete",
                    State.IN_PROGRESS,
                    Priority.NORMAL
                ),
                (
                    "# Indicating the state of a task",
                    "blocked, this task needs more input",
                    State.BLOCKED,
                    Priority.NORMAL
                ),
            ],
            [],
        )

    def test_search_terms(self):
        assert self.tasks(self.file.grouped_tasks(search_terms=["multiline"])) == (
            [],
            [],
            [],
            [],
            [
                (
                    "# Indicating the state of a task / Multiline tasks and indentation",  # noqa: E501
                    "Lorem ipsum dolor sit amet, consectetur adipisicing elit, "
                    "sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",  # noqa: E501
                    State.OPEN,
                    Priority.NORMAL
                ),
                (
                    "# Indicating the state of a task / Multiline tasks and indentation",  # noqa: E501
                    "Ut enim ad minim veniam,",
                    State.OPEN,
                    Priority.NORMAL
                ),
            ],
            [],
        )

    def test_search_terms_and_state(self):
        assert self.tasks(
            self.file.grouped_tasks(
                states={State.COMPLETE, State.CANCELLED},
                search_terms=["task"],
            )
        ) == (
            [],
            [],
            [],
            [],
            [],
            [
                (
                    "# Indicating the state of a task",
                    "complete, this task has been finished",
                    State.COMPLETE,
                    None
                ),
                (
                    "# Indicating the state of a task",
                    "cancelled, this task has been scratched",
                    State.CANCELLED,
                    None
                ),
            ],
        )

    def test_search_terms_and_state_no_overlap(self):
        assert self.tasks(
            self.file.grouped_tasks(
                states={State.COMPLETE},
                search_terms=["lorem"],
            )
        ) == ([], [], [], [], [], [])

    def test_priority_high(self):
        assert self.tasks(
            self.file.grouped_tasks(priorities={Priority.HIGH})
        ) == ([], [], [], [], [], [])

    def test_priority_high_and_medium(self):
        assert self.tasks(
            self.file.grouped_tasks(priorities={Priority.HIGH, Priority.MEDIUM})
        ) == ([], [], [], [], [], [])


class TestGroupedTasksPrioritisation(GroupedTasksTestCase):
    file = MarkdownFile(source="docs/prioritisation.md", today=date.today())

    def test_no_args_returns_all_grouped_by_priority(self):
        assert self.tasks(self.file.grouped_tasks()) == (
            [],
            [
                (
                    "# Prioritisation",
                    "super-urgent task",
                    State.OPEN,
                    Priority.HIGH
                ),
                (
                    "# do these first",
                    "inherently high priority task, because of the header",
                    State.OPEN,
                    Priority.HIGH
                ),
                (
                    "# do these first",
                    "no extra priority, still listed second",
                    State.OPEN,
                    Priority.HIGH
                ),
            ],
            [
                (
                    "# Prioritisation",
                    "semi-urgent task",
                    State.OPEN,
                    Priority.MEDIUM
                ),
            ],
            [],
            [
                (
                    "# Prioritisation",
                    "not a high priority task",
                    State.IN_PROGRESS,
                    Priority.NORMAL
                ),
                (
                    "# Prioritisation",
                    "top, but not urgent, task",
                    State.OPEN,
                    Priority.NORMAL
                ),
            ],
            [
                (
                    "# do these first / grouped, but still highest priority",
                    "header priority cascades down",
                    State.COMPLETE,
                    None
                ),
                (
                    "# more tasks",
                    "normal priority, new header resets that",
                    State.CANCELLED,
                    None
                ),
            ],
        )

    def test_state_two_selected(self):
        assert self.tasks(
            self.file.grouped_tasks(states={State.IN_PROGRESS, State.BLOCKED})
        ) == (
            [],
            [],
            [],
            [],
            [
                (
                    "# Prioritisation",
                    "not a high priority task",
                    State.IN_PROGRESS,
                    Priority.NORMAL
                ),
            ],
            [],
        )

    def test_search_terms(self):
        assert self.tasks(self.file.grouped_tasks(search_terms=["priority"])) == (
            [],
            [
                (
                    "# do these first",
                    "inherently high priority task, because of the header",
                    State.OPEN,
                    Priority.HIGH
                ),
                (
                    "# do these first",
                    "no extra priority, still listed second",
                    State.OPEN,
                    Priority.HIGH
                ),
            ],
            [],
            [],
            [
                (
                    "# Prioritisation",
                    "not a high priority task",
                    State.IN_PROGRESS,
                    Priority.NORMAL
                ),
            ],
            [
                (
                    "# do these first / grouped, but still highest priority",
                    "header priority cascades down",
                    State.COMPLETE,
                    None
                ),
                (
                    "# more tasks",
                    "normal priority, new header resets that",
                    State.CANCELLED,
                    None
                ),
            ],
        )

    def test_search_terms_and_state(self):
        assert self.tasks(
            self.file.grouped_tasks(
                states={State.COMPLETE},
                search_terms=["header"],
            )
        ) == (
            [],
            [],
            [],
            [],
            [],
            [
                (
                    "# do these first / grouped, but still highest priority",
                    "header priority cascades down",
                    State.COMPLETE,
                    None
                ),
            ],
        )

    def test_search_terms_and_state_no_overlap(self):
        assert self.tasks(
            self.file.grouped_tasks(
                states={State.COMPLETE},
                search_terms=["urgent"],
            )
        ) == ([], [], [], [], [], [])

    def test_priority_high(self):
        assert self.tasks(
            self.file.grouped_tasks(priorities={Priority.HIGH})
        ) == (
            [],
            [
                (
                    "# Prioritisation",
                    "super-urgent task",
                    State.OPEN,
                    Priority.HIGH
                ),
                (
                    "# do these first",
                    "inherently high priority task, because of the header",
                    State.OPEN,
                    Priority.HIGH
                ),
                (
                    "# do these first",
                    "no extra priority, still listed second",
                    State.OPEN,
                    Priority.HIGH
                ),
            ],
            [],
            [],
            [],
            [],
        )

    def test_priority_high_and_medium(self):
        assert self.tasks(
            self.file.grouped_tasks(priorities={Priority.HIGH, Priority.MEDIUM})
        ) == (
            [],
            [
                (
                    "# Prioritisation",
                    "super-urgent task",
                    State.OPEN,
                    Priority.HIGH
                ),
                (
                    "# do these first",
                    "inherently high priority task, because of the header",
                    State.OPEN,
                    Priority.HIGH
                ),
                (
                    "# do these first",
                    "no extra priority, still listed second",
                    State.OPEN,
                    Priority.HIGH
                ),
            ],
            [
                (
                    "# Prioritisation",
                    "semi-urgent task",
                    State.OPEN,
                    Priority.MEDIUM
                ),
            ],
            [],
            [],
            [],
        )


class TestGroupedTasksDeadlines(GroupedTasksTestCase):
    def test_outside_all_windows_all_normal(self):
        file = MarkdownFile(source="docs/deadlines.md", today=date(2025, 1, 1))
        assert self.tasks(file.grouped_tasks()) == (
            [],
            [],
            [],
            [],
            [
                (
                    "# version 0.5",
                    "complete and release",
                    State.OPEN,
                    Priority.NORMAL
                ),
                (
                    "# Christmas dinner",
                    "book Christmas delivery",
                    State.OPEN,
                    Priority.NORMAL
                ),
                (
                    "# Christmas dinner",
                    "prep the make-ahead gravy",
                    State.OPEN,
                    Priority.NORMAL
                ),
                (
                    "# Christmas dinner",
                    "roast the potatoes",
                    State.OPEN,
                    Priority.NORMAL
                ),
                (
                    "# Christmas dinner",
                    "prep sprouts",
                    State.OPEN,
                    Priority.NORMAL
                ),
            ],
            [],
        )

    def test_inside_window_becomes_imminent(self):
        file = MarkdownFile(source="docs/deadlines.md", today=date(2025, 12, 2))
        assert self.tasks(file.grouped_tasks()) == (
            [],
            [],
            [],
            [
                (
                    "# version 0.5",
                    "complete and release",
                    State.OPEN,
                    Priority.IMMINENT
                ),
                (
                    "# Christmas dinner",
                    "book Christmas delivery",
                    State.OPEN,
                    Priority.IMMINENT
                ),
            ],
            [
                (
                    "# Christmas dinner",
                    "prep the make-ahead gravy",
                    State.OPEN,
                    Priority.NORMAL
                ),
                (
                    "# Christmas dinner",
                    "roast the potatoes",
                    State.OPEN,
                    Priority.NORMAL
                ),
                (
                    "# Christmas dinner",
                    "prep sprouts",
                    State.OPEN,
                    Priority.NORMAL
                ),
            ],
            [],
        )

    def test_emphasis_applies_inside_window(self):
        file = MarkdownFile(source="docs/deadlines.md", today=date(2025, 12, 24))
        assert self.tasks(file.grouped_tasks()) == (
            [
                (
                    "# version 0.5",
                    "complete and release",
                    State.OPEN,
                    Priority.OVERDUE
                ),
                (
                    "# Christmas dinner",
                    "book Christmas delivery",
                    State.OPEN,
                    Priority.OVERDUE
                ),
            ],
            [],
            [
                (
                    "# Christmas dinner",
                    "prep the make-ahead gravy",
                    State.OPEN,
                    Priority.MEDIUM
                ),
            ],
            [
                (
                    "# Christmas dinner",
                    "prep sprouts",
                    State.OPEN,
                    Priority.IMMINENT
                ),
            ],
            [
                (
                    "# Christmas dinner",
                    "roast the potatoes",
                    State.OPEN,
                    Priority.NORMAL
                ),
            ],
            [],
        )

    def test_high_emphasis_on_deadline_day(self):
        file = MarkdownFile(source="docs/deadlines.md", today=date(2025, 12, 25))
        assert self.tasks(file.grouped_tasks()) == (
            [
                (
                    "# version 0.5",
                    "complete and release",
                    State.OPEN,
                    Priority.OVERDUE
                ),
                (
                    "# Christmas dinner",
                    "book Christmas delivery",
                    State.OPEN,
                    Priority.OVERDUE
                ),
            ],
            [
                (
                    "# Christmas dinner",
                    "roast the potatoes",
                    State.OPEN,
                    Priority.HIGH
                ),
            ],
            [
                (
                    "# Christmas dinner",
                    "prep the make-ahead gravy",
                    State.OPEN,
                    Priority.MEDIUM
                ),
            ],
            [
                (
                    "# Christmas dinner",
                    "prep sprouts",
                    State.OPEN,
                    Priority.IMMINENT
                ),
            ],
            [],
            [],
        )

    def test_past_deadline_becomes_overdue(self):
        file = MarkdownFile(source="docs/deadlines.md", today=date(2025, 12, 26))
        assert self.tasks(file.grouped_tasks()) == (
            [
                (
                    "# version 0.5",
                    "complete and release",
                    State.OPEN,
                    Priority.OVERDUE
                ),
                (
                    "# Christmas dinner",
                    "book Christmas delivery",
                    State.OPEN,
                    Priority.OVERDUE
                ),
                (
                    "# Christmas dinner",
                    "prep the make-ahead gravy",
                    State.OPEN,
                    Priority.OVERDUE
                ),
                (
                    "# Christmas dinner",
                    "roast the potatoes",
                    State.OPEN,
                    Priority.OVERDUE
                ),
                (
                    "# Christmas dinner",
                    "prep sprouts",
                    State.OPEN,
                    Priority.OVERDUE
                ),
            ],
            [],
            [],
            [],
            [],
            [],
        )


class TestAnnotationParsing:
    def test_annotations_associated_with_headings(self):
        file = MarkdownFile(
            source="example/projects/obelisk.md",
            today=date(2025, 1, 1),
        )
        assert len(file.tasks) == 4
        assert file.tasks[0].as_dict() == {
            "heading": "# Project Obelisk",
            "state": State.OPEN,
            "text": "research into runic meaning",
            "priority": Priority.NORMAL,
            "due": None,
            "imminent": None,
            "annotation": "Something something star gate",
        }
        assert file.tasks[1].as_dict() == {
            "heading": "# Project Obelisk",
            "state": State.IN_PROGRESS,
            "text": "carve runes into obelisk",
            "priority": Priority.NORMAL,
            "due": None,
            "imminent": None,
            "annotation": "Something something star gate",
        }
        assert file.tasks[2].as_dict() == {
            "heading": "# Project Obelisk",
            "state": State.OPEN,
            "text": "bury obelisk in desert",
            "priority": Priority.NORMAL,
            "due": date(2026, 1, 5),
            "imminent": date(2025, 12, 22),
            "annotation": "Something something star gate",
        }
        assert file.tasks[3].as_dict() == {
            "heading": "# Project Obelisk / Discovery",
            "state": State.BLOCKED,
            "text": "watch archaeologists discover (needs time machine)",
            "priority": Priority.OVERDUE,
            "due": date(1994, 10, 28),
            "imminent": date(1994, 10, 14),
            "annotation": "Mess with Jackson",
        }

    def test_other_fenced_blocks_ignored(self):
        file = MarkdownFile(
            source_string=dedent("""\
                # Only 'whatnext' blocks

                ```
                notes notes notes
                ```

                - [ ] not this one

                ##

                ```python
                print("hello")
                ```

                - [ ] not this one either
            """),
            today=date(2025, 1, 1),
        )
        assert len(file.tasks) == 2
        assert file.tasks[0].as_dict() == {
            "heading": "# Only 'whatnext' blocks",
            "state": State.OPEN,
            "text": "not this one",
            "priority": Priority.NORMAL,
            "due": None,
            "imminent": None,
            "annotation": None,
        }
        assert file.tasks[1].as_dict() == {
            "heading": "# Only 'whatnext' blocks",
            "state": State.OPEN,
            "text": "not this one either",
            "priority": Priority.NORMAL,
            "due": None,
            "imminent": None,
            "annotation": None,
        }

    def test_multiple_annotations_combine(self):
        file = MarkdownFile(
            source_string=dedent("""\
                # Shattered thoughts

                ```whatnext
                notes notes notes
                ```

                ```whatnext
                more notes
                ```

                - [ ] something about notes

                ```whatnext
                what are this?
                ```

                - [ ] are this?
            """),
            today=date(2025, 1, 1),
        )
        assert len(file.tasks) == 2
        assert file.tasks[0].as_dict() == {
            "heading": "# Shattered thoughts",
            "state": State.OPEN,
            "text": "something about notes",
            "priority": Priority.NORMAL,
            "due": None,
            "imminent": None,
            "annotation": "notes notes notes more notes what are this?",
        }
        assert file.tasks[1].as_dict() == {
            "heading": "# Shattered thoughts",
            "state": State.OPEN,
            "text": "are this?",
            "priority": Priority.NORMAL,
            "due": None,
            "imminent": None,
            "annotation": "notes notes notes more notes what are this?",
        }
