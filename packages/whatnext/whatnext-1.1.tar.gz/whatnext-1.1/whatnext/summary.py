from collections import Counter

from termcolor import colored

from whatnext.models import Priority, State

# done states leftmost (darker), active states rightmost (lighter)
STATE_DISPLAY_ORDER = [
    State.CANCELLED,
    State.COMPLETE,
    State.BLOCKED,
    State.IN_PROGRESS,
    State.OPEN,
]
PRIORITY_DISPLAY_ORDER = [
    Priority.OVERDUE,
    Priority.IMMINENT,
    Priority.HIGH,
    Priority.MEDIUM,
    Priority.NORMAL,
]
SHADING = ["▚", "█", "▓", "▒", "░"]
SHADING_INDICES = {
    1: [1],
    2: [1, 4],
    3: [0, 2, 4],
    4: [0, 1, 3, 4],
    5: [0, 1, 2, 3, 4],
}


def build_visualisation_map(selected, display_order):
    selected_in_order = [
        item
            for item in display_order
                if item in selected
    ]
    indices = SHADING_INDICES.get(len(selected_in_order), [0, 1, 2, 3, 4])
    char_map = {}
    for index, item in enumerate(selected_in_order):
        char_map[item] = SHADING[indices[index]]
    for item in display_order:
        if item not in char_map:
            char_map[item] = SHADING[-1]
    return char_map, selected_in_order


def make_header(selected_in_order, has_remainder, col_widths=None):
    parts = [
        item.abbrev
            for item in selected_in_order
    ]
    if has_remainder:
        parts.append("~")
    if col_widths:
        parts = [
            part.rjust(width)
                for part, width in zip(parts, col_widths)
        ]
    return " ".join(parts)


def make_legend(
    char_map, selected_in_order, display_order, has_remainder, use_colour=False
):
    parts = []
    for item in selected_in_order:
        char = char_map[item]
        if use_colour:
            char = colored(char, "blue", force_color=True)
        parts.append(f"{char} {item.label}")
    if has_remainder:
        unselected = [
            state.label
                for state in display_order
                    if state not in selected_in_order
        ]
        char = SHADING[-1]
        if use_colour:
            char = colored(char, "blue", force_color=True)
        parts.append(f"{char} ({'/'.join(unselected)})")
    return "  ".join(parts)


def calculate_totals(file_counts):
    total = Counter()
    for counts in file_counts:
        total += counts
    return total


def get_count_parts(counts, selected_in_order, has_remainder):
    parts = [counts.get(item, 0) for item in selected_in_order]
    if has_remainder:
        parts.append(
            sum(
                count
                    for key, count in counts.items()
                        if key not in selected_in_order
            )
        )
    return parts


def format_counts(parts, col_widths):
    return " ".join(str(value).rjust(width) for value, width in zip(parts, col_widths))


def build_bar(counts, total, width, char_map, bar_order):
    parts = []
    cumulative = 0
    bar_pos = 0

    for item in bar_order:
        cumulative += counts.get(item, 0)
        end_pos = round(width * cumulative / total)
        parts.append(char_map[item] * (end_pos - bar_pos))
        bar_pos = end_pos

    remainder = sum(
        count for key, count in counts.items()
            if key not in bar_order
    )
    if remainder:
        cumulative += remainder
        end_pos = round(width * cumulative / total)
        parts.append(SHADING[-1] * (end_pos - bar_pos))
    return "".join(parts)


def format_summary(
    file_tasks,
    width,
    selected_states,
    selected_priorities=None,
    use_colour=False,
    relative=False,
    all_tasks_total=None,
):
    if selected_priorities:
        display_order = PRIORITY_DISPLAY_ORDER
        selected = selected_priorities
        count_attr = "priority"
    else:
        display_order = STATE_DISPLAY_ORDER
        selected = selected_states
        count_attr = "state"

    char_map, selected_in_order = build_visualisation_map(selected, display_order)
    remainder = [
        item
            for item in display_order
                if item not in selected
    ]
    bar_order = selected_in_order + remainder

    file_tasks = [
        (file, tasks)
            for file, tasks in file_tasks
                if tasks
    ]
    if not file_tasks:
        return ""

    file_counts = [
        Counter(
            getattr(task, count_attr)
                for task in tasks
        )
            for _, tasks in file_tasks
    ]
    has_remainder = any(
        key not in selected_in_order
            for counts in file_counts
                for key in counts
    )
    total_counts = calculate_totals(file_counts) if len(file_tasks) > 1 else None

    # calculate column widths
    all_counts = file_counts + ([total_counts] if total_counts else [])
    all_parts = [
        get_count_parts(counts, selected_in_order, has_remainder)
            for counts in all_counts
    ]
    num_cols = len(all_parts[0])
    col_widths = [
        max(
            len(str(parts[col]))
                for parts in all_parts
        )
            for col in range(num_cols)
    ]

    # calculate space taken
    gap = "  "
    count_width = len(format_counts(all_parts[0], col_widths))
    widest_file = max(
        len(file.display_path)
            for file, _ in file_tasks
    )
    bar_width = max(
        10,
        width - count_width - widest_file - len(gap) * 3,
    )
    widest_task_count = max(
        len(tasks)
            for _, tasks in file_tasks
    )

    # build output
    header = make_header(selected_in_order, has_remainder, col_widths)
    lines = [
        header.rjust(bar_width + len(gap) + count_width)
    ]

    for (file, tasks), counts in zip(file_tasks, file_counts):
        task_count = len(tasks)
        file_bar_width = round(bar_width * task_count / widest_task_count)
        bar = build_bar(counts, task_count, file_bar_width, char_map, bar_order)
        if use_colour:
            bar = colored(bar, "blue", force_color=True)
        padding = " " * (bar_width - file_bar_width)
        parts = get_count_parts(counts, selected_in_order, has_remainder)
        count = format_counts(parts, col_widths)
        lines.append(
            f"{bar}{padding}{gap}{count.rjust(count_width)}{gap}"
            f"{file.display_path}"
        )

    if total_counts:
        parts = get_count_parts(total_counts, selected_in_order, has_remainder)
        total_str = format_counts(parts, col_widths)
        displayed_total = sum(total_counts.values())
        if all_tasks_total is None:
            all_tasks_total = displayed_total
        lines.append(f"{' ' * bar_width}{gap}{'─' * count_width}")
        lines.append(
            f"{' ' * bar_width}{gap}{total_str.rjust(count_width)}{gap}"
            f"{displayed_total}, of {all_tasks_total} total"
        )

    lines.append("")
    lines.append(make_legend(
        char_map, selected_in_order, display_order, has_remainder, use_colour
    ))

    return "\n".join(lines)
