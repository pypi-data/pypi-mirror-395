import random
from datetime import date

from whatnext.cli import flatten_by_priority, find_markdown_files
from whatnext.models import MarkdownFile, Priority, State

ACTIVE_STATES = {State.IN_PROGRESS, State.OPEN, State.BLOCKED}


class TestLimit:
    obelisk = MarkdownFile(
        source="example/projects/obelisk.md",
        today=date(2025, 12, 25),
    )

    def test_limit_of_one(self):
        filtered = [(self.obelisk, self.obelisk.filtered_tasks(states=ACTIVE_STATES))]
        tasks = flatten_by_priority(filtered)[:1]
        assert [
            task.as_dict()
                for task in tasks
        ] == [
            {
                "heading": "# Project Obelisk / Discovery",
                "state": State.BLOCKED,
                "text": "watch archaeologists discover (needs time machine)",
                "priority": Priority.OVERDUE,
                "due": date(1994, 10, 28),
                "imminent": date(1994, 10, 14),
                "annotation": "Mess with Jackson",
            },
        ]

    def test_limit_spans_priority_groups(self):
        filtered = [(self.obelisk, self.obelisk.filtered_tasks(states=ACTIVE_STATES))]
        tasks = flatten_by_priority(filtered)[:3]
        assert [
            task.as_dict()
                for task in tasks
        ] == [
            {
                "heading": "# Project Obelisk / Discovery",
                "state": State.BLOCKED,
                "text": "watch archaeologists discover (needs time machine)",
                "priority": Priority.OVERDUE,
                "due": date(1994, 10, 28),
                "imminent": date(1994, 10, 14),
                "annotation": "Mess with Jackson",
            },
            {
                "heading": "# Project Obelisk",
                "state": State.OPEN,
                "text": "bury obelisk in desert",
                "priority": Priority.HIGH,
                "due": date(2026, 1, 5),
                "imminent": date(2025, 12, 22),
                "annotation": "Something something star gate",
            },
            {
                "heading": "# Project Obelisk",
                "state": State.IN_PROGRESS,
                "text": "carve runes into obelisk",
                "priority": Priority.NORMAL,
                "due": None,
                "imminent": None,
                "annotation": "Something something star gate",
            },
        ]


class TestRandomSelection:
    today = date(2025, 12, 25)
    example_files = find_markdown_files("example", today)

    def _filter_active(self, files):
        return [
            (file, file.filtered_tasks(states=ACTIVE_STATES))
                for file in files
        ]

    def test_randomise(self):
        filtered = self._filter_active(self.example_files)
        all_tasks = flatten_by_priority(filtered)
        assert len(all_tasks) > 1

        first_task = all_tasks[0].text
        found_different = False

        # this should exit long before 10,000 iterations, that's just safety
        for _ in range(10000):
            filtered = self._filter_active(self.example_files)
            tasks = flatten_by_priority(filtered)
            random.shuffle(tasks)
            randomised = tasks[:1]
            if randomised[0].text != first_task:
                found_different = True
                break

        assert found_different

    def test_randomise_selects_from_full_pool(self):
        filtered = self._filter_active(self.example_files)
        all_tasks = flatten_by_priority(filtered)
        expected = {task.text for task in all_tasks}

        # in theory this can still fail because random
        seen = set()
        for _ in range(10000):
            filtered = self._filter_active(self.example_files)
            tasks = flatten_by_priority(filtered)
            random.shuffle(tasks)
            seen.add(tasks[0].text)

        assert seen == expected
