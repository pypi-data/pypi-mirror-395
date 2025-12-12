from datetime import date, timedelta
from enum import Enum
import os
import re
import textwrap

from termcolor import colored


class Priority(Enum):
    def __new__(cls, config):
        obj = object.__new__(cls)
        obj._value_ = config["value"]
        obj.abbrev = config["abbrev"]
        obj.label = config["label"]
        return obj

    OVERDUE = {"value": 0, "abbrev": "!", "label": "Overdue"}
    HIGH = {"value": 1, "abbrev": "H", "label": "High"}
    MEDIUM = {"value": 2, "abbrev": "M", "label": "Medium"}
    IMMINENT = {"value": 3, "abbrev": "I", "label": "Imminent"}
    NORMAL = {"value": 4, "abbrev": "N", "label": "Normal"}


class State(Enum):
    def __new__(cls, config):
        obj = object.__new__(cls)
        obj._value_ = config["value"]
        obj.markers = config["markers"]
        obj.sort_order = config["sort_order"]
        obj.abbrev = config["abbrev"]
        obj.label = config["label"]
        return obj

    IN_PROGRESS = {
        "value": "in_progress",
        "markers": ["/"],
        "sort_order": 0,
        "abbrev": "P",
        "label": "Partial",
    }
    OPEN = {
        "value": "open",
        "markers": [" "],
        "sort_order": 1,
        "abbrev": "O",
        "label": "Open",
    }
    BLOCKED = {
        "value": "blocked",
        "markers": ["<"],
        "sort_order": 2,
        "abbrev": "B",
        "label": "Blocked",
    }
    COMPLETE = {
        "value": "complete",
        "markers": ["X", "x"],
        "sort_order": 3,
        "abbrev": "D",
        "label": "Done",
    }
    CANCELLED = {
        "value": "cancelled",
        "markers": ["#"],
        "sort_order": 4,
        "abbrev": "C",
        "label": "Cancelled",
    }

    @classmethod
    def from_marker(cls, marker):
        for state in cls:
            if marker in state.markers:
                return state
        return None


class Task:
    def __init__(
        self,
        file,
        heading,
        text,
        state,
        priority=Priority.NORMAL,
        due=None,
        imminent=None,
        annotation=None,
        line=None,
    ):
        self.file = file
        self.heading = heading
        self.text = text
        self.state = state
        self.priority = priority
        self.due = due
        self.imminent = imminent
        self.annotation = annotation
        self.line = line

    def as_dict(self):
        return {
            "heading": self.heading,
            "state": self.state,
            "text": self.text,
            "priority": self.priority,
            "due": self.due,
            "imminent": self.imminent,
            "annotation": self.annotation,
        }

    def wrapped_task(self, width=80, indent="    ", text_colour=None):
        task_text = " ".join(self.text.split())
        if text_colour:
            task_text = colored(task_text, text_colour, force_color=True)
        text = f"- [{self.state.markers[0]}] " + task_text
        if width is None or len(indent + text) <= width:
            return [indent + text]
        return textwrap.wrap(
            text,
            width=width,
            initial_indent=indent,
            subsequent_indent=indent + "      ",
        )

    def format_duration(self, days):
        if days >= 365:
            years = days // 365
            months = (days % 365) // 30
            if months:
                return f"{years}y {months}m"
            return f"{years}y"
        if days >= 30:
            months = days // 30
            weeks = (days % 30) // 7
            if weeks:
                return f"{months}m {weeks}w"
            return f"{months}m"
        if days >= 14:
            weeks = days // 7
            remainder = days % 7
            if remainder:
                return f"{weeks}w {remainder}d"
            return f"{weeks}w"
        return f"{days}d"

    def format_overdue_duration(self):
        return self.format_duration((self.file.today - self.due).days)

    def format_imminent_countdown(self):
        days = (self.due - self.file.today).days
        if days == 0:
            return "TODAY"
        return self.format_duration(days)

    def wrapped_annotation(self, width=80, indent="    "):
        if not self.annotation:
            return []
        text = " ".join(self.annotation.split())
        if width is None or len(indent + text) <= width:
            return [indent + text]
        return textwrap.wrap(
            text,
            width=width,
            initial_indent=indent,
            subsequent_indent=indent,
        )

    def wrapped_heading(self, width=80, indent="    "):
        if not self.heading:
            return []
        heading = self.heading
        if self.priority == Priority.OVERDUE:
            heading = f"{self.heading} / OVERDUE {self.format_overdue_duration()}"
        elif self.priority == Priority.IMMINENT:
            heading = f"{self.heading} / IMMINENT {self.format_imminent_countdown()}"
        elif self.priority is None:
            heading = f"{self.heading} / FINISHED"
        elif self.priority != Priority.NORMAL:
            heading = f"{self.heading} / {self.priority.label.upper()}"
        if width is None or len(indent + heading) <= width:
            return [indent + heading]
        return textwrap.wrap(
            heading,
            width=width,
            initial_indent=indent,
            subsequent_indent=indent + "  ",
        )


class MarkdownFile:
    HEADING_PATTERN = re.compile(r"""
        ^
            (\#+) \s+ (.*)
        $
    """, re.VERBOSE)
    TASK_PATTERN = re.compile(r"""
        ^
            (\s*) -[ ] \[ (.) \]
    """, re.VERBOSE)
    DEADLINE_PATTERN = re.compile(r"""
        ^
            (.+?)
            (?:
                \s+
                @(\d{4}-\d{2}-\d{2})
                (?:
                    /(\d+)([wd])
                )?
            )?
            \s*
        $
    """, re.VERBOSE)
    ANNOTATION_START = re.compile(r"^```whatnext\s*$")
    ANNOTATION_END = re.compile(r"^```\s*$")
    DEFAULT_URGENCY = timedelta(weeks=2)

    def __init__(
        self,
        *,
        source=None,
        source_string=None,
        path=None,
        base_dir=".",
        today,
    ):
        if source is not None and source_string is not None:
            raise ValueError("Cannot specify both source and source_string")
        if source is None and source_string is None:
            raise ValueError("Must specify either source or source_string")

        if source is not None:
            self.path = source
            self._lines = None
        else:
            self.path = path or "string"
            self._lines = source_string.splitlines()

        self.base_dir = base_dir
        self.today = today
        self.warnings = []
        self.tasks = self.extract_tasks()

    @staticmethod
    def parse_deadline(text):
        match = MarkdownFile.DEADLINE_PATTERN.match(text)
        cleaned = match.group(1)
        date_str = match.group(2)
        if date_str is None:
            return (None, None, cleaned)
        try:
            due = date.fromisoformat(date_str)
        except ValueError:
            # preserve invalid date in output so user can see and fix it
            return (None, None, text)
        urgency = MarkdownFile.DEFAULT_URGENCY
        if match.group(3) and match.group(4):
            amount = int(match.group(3))
            unit = match.group(4)
            if unit == "d":
                urgency = timedelta(days=amount)
            elif unit == "w":
                urgency = timedelta(weeks=amount)
        imminent = due - urgency
        return (due, imminent, cleaned)

    @staticmethod
    def parse_priority(text):
        if text.startswith("**") and text.endswith("**") and len(text) > 4:
            return Priority.HIGH
        if (
            text.startswith("_")
            and not text.startswith("__")
            and text.endswith("_")
            and not text.endswith("__")
            and len(text) > 2
        ):
            return Priority.MEDIUM
        return Priority.NORMAL

    @staticmethod
    def strip_emphasis(text):
        if text.startswith("**") and text.endswith("**") and len(text) > 4:
            return text[2:-2]
        if text.startswith("_") and text.endswith("_") and len(text) > 2:
            return text[1:-1]
        return text

    def extract_tasks(self):
        tasks = []
        for heading, lines, priority, annotation in self.sections():
            tasks.extend(
                self.tasks_in_section(heading, lines, priority, annotation)
            )
        return tasks

    def read_lines(self):
        if self._lines is not None:
            return self._lines
        with open(self.path) as handle:
            return [line.rstrip("\n") for line in handle]

    def sections(self):
        heading = None
        priority = Priority.NORMAL
        annotation_parts = []
        lines = []
        results = []

        # stack stores (level, text, priority) -- explicit level needed for
        # skipped headings (# -> ### -> ##, where position != depth)
        stack = []

        in_annotation = False
        annotation_delimiter = None

        for line_index, line in enumerate(self.read_lines(), 1):
            if in_annotation:
                if annotation_delimiter:
                    closes = (
                        line.startswith(annotation_delimiter)
                        and not line.strip()[len(annotation_delimiter):]
                    )
                    if closes:
                        in_annotation = False
                        annotation_delimiter = None
                    else:
                        annotation_parts.append(line)
                elif self.ANNOTATION_END.match(line):
                    in_annotation = False
                else:
                    annotation_parts.append(line)
                continue
            if self.ANNOTATION_START.match(line):
                annotation_delimiter = re.match(r'^(`+)', line).group(1)
                in_annotation = True
                continue
            if match := self.HEADING_PATTERN.match(line):
                if lines:
                    annotation = " ".join(" ".join(annotation_parts).split()) or None
                    results.append((heading, lines, priority, annotation))
                    lines = []
                    annotation_parts = []
                level = len(match.group(1))
                while stack and stack[-1][0] >= level:
                    stack.pop()
                heading_text = match.group(2)
                heading_priority = self.parse_priority(heading_text)
                stack.append((level, heading_text, heading_priority))
                heading = "# " + " / ".join(
                    self.strip_emphasis(text) for _, text, _ in stack
                )
                priority = min((p for _, _, p in stack), key=lambda p: p.value)
            else:
                lines.append((line_index, line))

        if lines:
            annotation = " ".join(" ".join(annotation_parts).split()) or None
            results.append((heading, lines, priority, annotation))

        return results

    def parse_task(
        self, heading, heading_priority, marker, task_content, line_index, annotation
    ):
        state = State.from_marker(marker)
        if state is None:
            self.warnings.append(
                f"WARNING: ignoring invalid state '{marker}' "
                f"in '{task_content}', {self.display_path} line {line_index}"
            )
            return None
        due, imminent_date, cleaned_text = self.parse_deadline(task_content)
        display_text = self.strip_emphasis(cleaned_text)
        display_text = " ".join(display_text.split())

        if state in {State.COMPLETE, State.CANCELLED}:
            priority = None
        elif due is None:
            task_priority = self.parse_priority(cleaned_text)
            priority = min(heading_priority, task_priority, key=lambda p: p.value)
        elif self.today > due:
            priority = Priority.OVERDUE
        elif self.today >= imminent_date:
            task_priority = self.parse_priority(cleaned_text)
            emphasis = min(heading_priority, task_priority, key=lambda p: p.value)
            if emphasis == Priority.NORMAL:
                priority = Priority.IMMINENT
            else:
                priority = emphasis
        else:
            priority = Priority.NORMAL

        return Task(
            self,
            heading,
            display_text,
            state,
            priority,
            due,
            imminent_date,
            annotation,
            line_index,
        )

    def tasks_in_section(
        self, heading, lines, heading_priority, annotation
    ):
        prefix_width = len("- [.] ")
        tasks = []
        index = -1
        while (index := index + 1) < len(lines):
            line_number, line_content = lines[index]
            if match := self.TASK_PATTERN.match(line_content):
                task_line = line_number
                marker = match.group(2)
                text = line_content.lstrip()
                indent = len(match.group(1)) + prefix_width
                while (
                    index + 1 < len(lines)
                    and self.is_continuation(lines[index + 1][1], indent)
                ):
                    index += 1
                    text += " " + lines[index][1].strip()
                task_content = text[prefix_width:]
                task = self.parse_task(
                    heading,
                    heading_priority,
                    marker,
                    task_content,
                    task_line,
                    annotation,
                )
                if task is not None:
                    tasks.append(task)

        return tasks

    def is_continuation(self, line, indent):
        if not line.strip():
            return False
        leading = len(line) - len(line.lstrip())
        return leading == indent

    @property
    def display_path(self):
        return os.path.relpath(self.path, self.base_dir)

    @property
    def incomplete(self):
        outstanding_states = {
            State.IN_PROGRESS,
            State.OPEN,
            State.BLOCKED,
        }
        return self.sort_by_state(
            task for task in self.tasks
                if task.state in outstanding_states
        )

    def sort_by_state(self, tasks):
        by_heading = {}
        for task in tasks:
            by_heading.setdefault(task.heading, []).append(task)
        result = []
        for heading in by_heading:
            result.extend(
                sorted(
                    by_heading[heading],
                    key=lambda task: task.state.sort_order
                )
            )
        return result

    def filtered_tasks(self, states=None, search_terms=None, priorities=None):
        tasks = self.tasks
        if states:
            tasks = [
                task for task in tasks
                    if task.state in states
            ]
        if priorities:
            tasks = [
                task for task in tasks
                    if task.priority in priorities
            ]
        if search_terms:
            filtered = []
            for task in tasks:
                heading_matches = task.heading and any(
                    term in task.heading.lower() for term in search_terms
                )
                task_matches = any(
                    term in task.text.lower() for term in search_terms
                )
                if heading_matches or task_matches:
                    filtered.append(task)
            tasks = filtered
        return tasks

    def grouped_tasks(self, states=None, search_terms=None, priorities=None):
        tasks = self.filtered_tasks(states, search_terms, priorities)
        return (
            self.sort_by_state(
                task for task in tasks
                    if task.priority == Priority.OVERDUE
            ),
            self.sort_by_state(
                task for task in tasks
                    if task.priority == Priority.HIGH
            ),
            self.sort_by_state(
                task for task in tasks
                    if task.priority == Priority.MEDIUM
            ),
            self.sort_by_state(
                task for task in tasks
                    if task.priority == Priority.IMMINENT
            ),
            self.sort_by_state(
                task for task in tasks
                    if task.priority == Priority.NORMAL
            ),
            self.sort_by_state(
                task for task in tasks
                    if task.priority is None
            ),
        )
