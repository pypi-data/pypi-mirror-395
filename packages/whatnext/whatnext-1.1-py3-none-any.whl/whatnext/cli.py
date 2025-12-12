import argparse
from datetime import date
import fnmatch
import importlib.metadata
import os
import random
import re
import shutil
import subprocess
import sys
import toml

from termcolor import colored

from whatnext.models import MarkdownFile, Priority, State
from whatnext.summary import format_summary

STATE_COLOURS = {
    State.BLOCKED: "cyan",
    State.IN_PROGRESS: "yellow",
}

PRIORITY_COLOURS = {
    Priority.OVERDUE: ("magenta", ["bold"]),
    Priority.IMMINENT: ("green", None),
}


def get_terminal_width():
    columns_env = os.environ.get("COLUMNS")
    if columns_env:
        width = int(columns_env)
    else:
        width = shutil.get_terminal_size().columns
    if width < 40:
        width = 80
    return width


def get_editor():
    for var in ("WHATNEXT_EDITOR", "VISUAL", "EDITOR"):
        if value := os.environ.get(var):
            return value
    return "vi"


def load_config(config_path=None, directory="."):
    if config_path is None:
        config_path = os.path.join(directory, ".whatnext")
    elif not (config_path.startswith("./") or os.path.isabs(config_path)):
        config_path = os.path.join(directory, config_path)
    if os.path.exists(config_path):
        with open(config_path) as handle:
            return toml.load(handle)
    return {}


def is_ignored(filepath, ignore_patterns):
    for pattern in ignore_patterns:
        if fnmatch.fnmatch(filepath, pattern):
            return True
    return False


def find_markdown_files(paths, today, ignore_patterns=None, quiet=False):
    if ignore_patterns is None:
        ignore_patterns = []
    if isinstance(paths, str):
        paths = [paths]

    seen = set()
    unique_paths = []
    for path in paths:
        abs_path = os.path.abspath(path)
        if abs_path not in seen:
            seen.add(abs_path)
            unique_paths.append(path)
    paths = unique_paths

    multiple = len(paths) > 1
    task_files = {}

    for path in paths:
        base_dir = "." if multiple else path

        if os.path.isfile(path):
            if path.endswith(".md"):
                abs_path = os.path.abspath(path)
                if abs_path not in task_files:
                    file = MarkdownFile(source=path, today=today)
                    if not quiet:
                        for warning in file.warnings:
                            print(warning, file=sys.stderr)
                    if file.tasks:
                        task_files[abs_path] = file
            continue

        for root, dirs, files in os.walk(path):
            for filename in files:
                if filename.endswith(".md"):
                    filepath = os.path.join(root, filename)
                    abs_path = os.path.abspath(filepath)
                    if abs_path in task_files:
                        continue
                    relative_path = os.path.relpath(filepath, path)
                    if is_ignored(relative_path, ignore_patterns):
                        continue
                    file = MarkdownFile(source=filepath, base_dir=base_dir, today=today)
                    if not quiet:
                        for warning in file.warnings:
                            print(warning, file=sys.stderr)
                    if file.tasks:
                        task_files[abs_path] = file

    # files are examined depth-last as a lightweight prioritisation
    return sorted(
        task_files.values(),
        key=lambda file: (
            file.display_path.count(os.sep),
            file.display_path,
        )
    )


def flatten_by_priority(filtered_data):
    groups = [[] for _ in range(len(Priority) + 1)]
    for file, tasks in filtered_data:
        # Sort by state within each heading, preserving heading order
        sorted_tasks = file.sort_by_state(tasks)
        for task in sorted_tasks:
            if task.priority is None:
                groups[-1].append(task)
            else:
                groups[task.priority.value].append(task)

    result = []
    for group in groups:
        result.extend(group)
    return result


def format_tasks(tasks, width, use_colour=False):
    output = []
    current_priority = None
    current_file = None
    current_heading = None

    for task in tasks:
        if task.priority != current_priority:
            if output:
                output.append("")
            current_priority = task.priority
            current_file = None
            current_heading = None

        text_colour = None
        block_colour = None
        block_attrs = None
        if use_colour:
            if task.priority in PRIORITY_COLOURS:
                block_colour, block_attrs = PRIORITY_COLOURS[task.priority]
            else:
                text_colour = STATE_COLOURS.get(task.state)

        # collect this task's output for block_colour
        lines = []
        if task.file != current_file:
            lines.append(f"{task.file.display_path}:")
            current_file = task.file
            current_heading = None

        if task.heading and task.heading != current_heading:
            lines.extend(task.wrapped_heading(width))
            current_heading = task.heading
            if task.annotation:
                lines.extend(task.wrapped_annotation(width))

        lines.extend(task.wrapped_task(width, text_colour=text_colour))

        if block_colour:
            lines = [
                colored(line, block_colour, attrs=block_attrs, force_color=True)
                for line in lines
            ]

        # now it becomes part of the output
        output.extend(lines)

    return "\n".join(output)


class CapitalisedHelpFormatter(argparse.RawDescriptionHelpFormatter):
    def add_usage(self, usage, actions, groups, prefix=None):
        if prefix is None:
            prefix = "Usage: "
        super().add_usage(usage, actions, groups, prefix)

    def start_section(self, heading):
        super().start_section(heading.capitalize() if heading else heading)

    def _split_lines(self, text, width):
        if '\n' in text:
            return text.splitlines()
        return super()._split_lines(text, width)


class ShortHelpAction(argparse.Action):
    def __init__(self, option_strings, dest, **kwargs):
        super().__init__(option_strings, dest, nargs=0, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        print(parser.format_usage().rstrip())
        parser.exit()


def main():
    parser = argparse.ArgumentParser(
        description="List tasks found in Markdown files",
        epilog="""\
Task States:
  - [ ] Open
  - [/] In progress
  - [<] Blocked
  - [X] Done (hidden by default)
  - [#] Cancelled (hidden by default)

Task Priority:
  - [ ] _Underscore means medium priority_
  - [ ] **Double asterisk means high priority**

  Headers can also be emphasised to set priority for all tasks beneath.

Deadlines:
  - [ ] Celebrate the New Year @2025-12-31
  - [ ] Get Halloween candy @2025-10-31/3w

  Are "immiment" priority two weeks before (or as specified -- /2d),
  and are "overdue" priority after the date passes.

Annotations:
  ```whatnext
  Short notes that appear in the output
  ```
""",
        add_help=False,
        formatter_class=CapitalisedHelpFormatter,
    )
    parser.add_argument(
        "-h",
        action=ShortHelpAction,
        help="Show the usage reminder and exit",
    )
    parser.add_argument(
        "--help",
        action="help",
        help="Show this help message and exit",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"whatnext version v{importlib.metadata.version('whatnext')}",
    )
    parser.add_argument(
        "--dir",
        default=os.environ.get("WHATNEXT_DIR", "."),
        help="Directory to search (default: WHATNEXT_DIR, or '.')",
    )
    parser.add_argument(
        "-s", "--summary",
        action="store_true",
        help="Show summary of task counts per file",
    )
    parser.add_argument(
        "-e", "--edit",
        action="store_true",
        help="Open matching files in your editor "
             "(WHATNEXT_EDITOR, VISUAL, EDITOR, or vi)",
    )
    parser.add_argument(
        "--relative",
        action="store_true",
        help="Show selected states relative to all others (use with --summary)",
    )
    parser.add_argument(
        "-a", "--all",
        action="store_true",
        help="Include all tasks and files, not just incomplete",
    )
    parser.add_argument(
        "--config",
        default=os.environ.get("WHATNEXT_CONFIG"),
        help="Path to config file (default: WHATNEXT_CONFIG, or '.whatnext' in --dir)",
    )
    parser.add_argument(
        "--ignore",
        action="append",
        default=[],
        metavar="PATTERN",
        help="Ignore files matching pattern (can be specified multiple times)",
    )
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        default=os.environ.get("WHATNEXT_QUIET") == "1",
        help="Suppress warnings (or set WHATNEXT_QUIET)",
    )
    parser.add_argument(
        "-o", "--open",
        action="store_true",
        help="Show only open tasks",
    )
    parser.add_argument(
        "-p", "--partial",
        action="store_true",
        help="Show only in progress tasks",
    )
    parser.add_argument(
        "-b", "--blocked",
        action="store_true",
        help="Show only blocked tasks",
    )
    parser.add_argument(
        "-d", "--done",
        action="store_true",
        help="Show only completed tasks",
    )
    parser.add_argument(
        "-c", "--cancelled",
        action="store_true",
        help="Show only cancelled tasks",
    )
    parser.add_argument(
        "--priority",
        action="append",
        default=[],
        choices=[
            priority.name.lower()
                for priority in Priority
        ],
        metavar="LEVEL",
        help="Show only tasks of this priority (can be specified multiple times)",
    )
    parser.add_argument(
        "--color",
        action=argparse.BooleanOptionalAction,
        default={"1": True, "0": False}.get(os.environ.get("WHATNEXT_COLOR")),
        help="Force colour output (or WHATNEXT_COLOR=1/0)",
    )
    parser.add_argument(
        "match",
        nargs="*",
        help="filter results:\n"
             "    [file/dir] - only include results from files within\n"
             "    [string]   - only include tasks with this string in the\n"
             "                 task text, or header grouping\n"
             "    [n]        - limit to n results, in priority order\n"
             "    [n]r       - limit to n results, selected at random",
    )
    args = parser.parse_args()

    # build the search space
    paths = []
    search_terms = []
    limit = None
    randomise = False
    for target in args.match:
        if match := re.match(r'^(\d+)(r?)$', target):
            limit = int(match.group(1))
            randomise = bool(match.group(2))
            continue
        target_path = os.path.join(args.dir, target)
        if os.path.isdir(target_path) or os.path.isfile(target_path):
            paths.append(target_path)
        else:
            search_terms.append(target.lower())

    if not paths:
        paths = [args.dir]

    config = load_config(args.config, args.dir)
    ignore_patterns = config.get("ignore", []) + args.ignore
    quiet = args.quiet

    if "WHATNEXT_TODAY" in os.environ:
        today = date.fromisoformat(os.environ["WHATNEXT_TODAY"])
    else:
        today = date.today()
    task_files = find_markdown_files(paths, today, ignore_patterns, quiet)

    if not task_files:
        return

    states = set()
    if args.open:
        states.add(State.OPEN)
    if args.partial:
        states.add(State.IN_PROGRESS)
    if args.blocked:
        states.add(State.BLOCKED)
    if args.done:
        states.add(State.COMPLETE)
    if args.cancelled:
        states.add(State.CANCELLED)
    if args.all:
        states = {
            State.OPEN, State.IN_PROGRESS, State.BLOCKED,
            State.COMPLETE, State.CANCELLED,
        }
    elif not states:
        # default view is incomplete tasks
        states = {State.OPEN, State.IN_PROGRESS, State.BLOCKED}

    priorities = {
        Priority[priority.upper()]
            for priority in args.priority
    }

    if args.color is None:
        args.color = sys.stdout.isatty()

    if args.summary and args.relative:
        # relative summary mode includes all tasks,
        # filters used only for visualisation
        filtered_data = [
            (file, file.filtered_tasks(None, search_terms, None))
                for file in task_files
        ]
    else:
        filtered_data = [
            (file, file.filtered_tasks(states, search_terms, priorities))
                for file in task_files
        ]

    if args.summary:
        output = format_summary(
            filtered_data,
            get_terminal_width(),
            states,
            priorities,
            args.color,
            args.relative,
            sum(
                len(file.tasks)
                    for file in task_files
            ),
        )
    else:
        tasks = flatten_by_priority(filtered_data)
        if randomise:
            random.shuffle(tasks)
        if limit:
            tasks = tasks[:limit]
        if args.edit:
            seen_files = set()
            files_to_edit = []
            for task in tasks:
                if task.file.path not in seen_files:
                    seen_files.add(task.file.path)
                    files_to_edit.append((task.line, task.file.path))
            editor = get_editor()
            for line, filepath in files_to_edit:
                subprocess.run([editor, f"+{line}", filepath])

        output = format_tasks(
            tasks,
            get_terminal_width(),
            args.color,
        )

    print(output)
