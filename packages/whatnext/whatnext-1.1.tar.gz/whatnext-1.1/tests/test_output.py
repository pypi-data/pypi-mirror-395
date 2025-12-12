from datetime import date
from textwrap import dedent

from whatnext.cli import flatten_by_priority, format_tasks
from whatnext.models import MarkdownFile, Priority, State

ACTIVE_STATES = {State.IN_PROGRESS, State.OPEN, State.BLOCKED}


class TestColourOutput:
    obelisk = MarkdownFile(
        source="example/projects/obelisk.md",
        today=date(2025, 12, 25),
    )
    obelisk_early = MarkdownFile(
        source="example/projects/obelisk.md",
        today=date(1990, 1, 1),
    )
    tasks_file = MarkdownFile(
        source="example/tasks.md",
        today=date(2025, 12, 25),
    )

    def test_overdue_tasks_output(self):
        filtered = [(
            self.obelisk,
            self.obelisk.filtered_tasks(ACTIVE_STATES, priorities={Priority.OVERDUE}),
        )]
        tasks = flatten_by_priority(filtered)
        output = format_tasks(tasks, width=80)
        expected = dedent("""\
            example/projects/obelisk.md:
                # Project Obelisk / Discovery / OVERDUE 31y 2m
                Mess with Jackson
                - [<] watch archaeologists discover (needs time machine)""")
        assert output == expected

    def test_overdue_tasks_output_is_bold_magenta(self):
        filtered = [(
            self.obelisk,
            self.obelisk.filtered_tasks(ACTIVE_STATES, priorities={Priority.OVERDUE}),
        )]
        tasks = flatten_by_priority(filtered)
        output = format_tasks(tasks, width=80, use_colour=True)
        m = "\x1b[1m\x1b[35m"
        r = "\x1b[0m"
        expected = dedent(f"""\
            {m}example/projects/obelisk.md:{r}
            {m}    # Project Obelisk / Discovery / OVERDUE 31y 2m{r}
            {m}    Mess with Jackson{r}
            {m}    - [<] watch archaeologists discover (needs time machine){r}""")
        assert output == expected

    def test_imminent_tasks_output(self):
        filtered = [(
            self.tasks_file,
            self.tasks_file.filtered_tasks(
                ACTIVE_STATES, priorities={Priority.IMMINENT}
            ),
        )]
        tasks = flatten_by_priority(filtered)
        output = format_tasks(tasks, width=80)
        expected = dedent("""\
            example/tasks.md:
                # Get S Done / IMMINENT 11d
                - [ ] start third project""")
        assert output == expected

    def test_imminent_tasks_output_is_green(self):
        filtered = [(
            self.tasks_file,
            self.tasks_file.filtered_tasks(
                ACTIVE_STATES, priorities={Priority.IMMINENT}
            ),
        )]
        tasks = flatten_by_priority(filtered)
        output = format_tasks(tasks, width=80, use_colour=True)
        g = "\x1b[32m"
        r = "\x1b[0m"
        expected = dedent(f"""\
            {g}example/tasks.md:{r}
            {g}    # Get S Done / IMMINENT 11d{r}
            {g}    - [ ] start third project{r}""")
        assert output == expected

    def test_blocked_task_text_is_cyan(self):
        filtered = [(
            self.obelisk_early,
            self.obelisk_early.filtered_tasks(states={State.BLOCKED}),
        )]
        tasks = flatten_by_priority(filtered)
        output = format_tasks(tasks, width=80, use_colour=True)
        cyan = "\x1b[36m"
        reset = "\x1b[0m"
        task = f"{cyan}watch archaeologists discover (needs time machine){reset}"
        expected = dedent(f"""\
            example/projects/obelisk.md:
                # Project Obelisk / Discovery
                Mess with Jackson
                - [<] {task}""")
        assert output == expected

    def test_in_progress_task_text_is_yellow(self):
        filtered = [(
            self.obelisk_early,
            self.obelisk_early.filtered_tasks(states={State.IN_PROGRESS}),
        )]
        tasks = flatten_by_priority(filtered)
        output = format_tasks(tasks, width=80, use_colour=True)
        yellow = "\x1b[33m"
        reset = "\x1b[0m"
        expected = dedent(f"""\
            example/projects/obelisk.md:
                # Project Obelisk
                Something something star gate
                - [/] {yellow}carve runes into obelisk{reset}""")
        assert output == expected


class TestAnnotationOutput:
    obelisk = MarkdownFile(
        source="example/projects/obelisk.md",
        today=date(1990, 1, 1),
    )

    def test_annotation_shown_with_tasks(self):
        filtered = [(
            self.obelisk,
            self.obelisk.filtered_tasks(states={State.IN_PROGRESS}),
        )]
        tasks = flatten_by_priority(filtered)
        output = format_tasks(tasks, width=80)
        expected = dedent("""\
            example/projects/obelisk.md:
                # Project Obelisk
                Something something star gate
                - [/] carve runes into obelisk""")
        assert output == expected

    def test_annotation_not_shown_without_tasks(self):
        filtered = [(
            self.obelisk,
            self.obelisk.filtered_tasks(states={State.BLOCKED}),
        )]
        tasks = flatten_by_priority(filtered)
        output = format_tasks(tasks, width=80)
        expected = dedent("""\
            example/projects/obelisk.md:
                # Project Obelisk / Discovery
                Mess with Jackson
                - [<] watch archaeologists discover (needs time machine)""")
        assert output == expected
