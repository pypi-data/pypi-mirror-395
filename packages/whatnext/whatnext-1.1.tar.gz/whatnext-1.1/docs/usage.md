# Usage

Without arguments, `whatnext` will show all outstanding tasks listed in any
Markdown file in the current directory:

(all examples assume you are running it in the [example](example/) directory
on December 25th 2025):

```bash
(computer)% whatnext
tasks.md:
    # Get S Done / OVERDUE 1m 3w
    - [ ] come up with better projects
projects/obelisk.md:
    # Project Obelisk / Discovery / OVERDUE 31y 2m
    Mess with Jackson
    - [<] watch archaeologists discover (needs time machine)

projects/obelisk.md:
    # Project Obelisk / HIGH
    Something something star gate
    - [ ] bury obelisk in desert

tasks.md:
    # Get S Done / MEDIUM
    - [ ] question entire existence

tasks.md:
    # Get S Done / IMMINENT 11d
    - [ ] start third project

projects/obelisk.md:
    # Project Obelisk
    Something something star gate
    - [/] carve runes into obelisk
    - [ ] research into runic meaning
```

They will be arranged:

- by [priority](prioritisation.md) and [deadline](deadlines.md):
  overdue, high, medium, imminent, normal
- within each priority by file, depth-last, in alphabetical order
- grouped under the heading within the file (including parental
  headings to show task hierarchy)


## Matching

Any argument(s) can be used to filter the output:

-   **\[term\]** - only show tasks that contain 'term', or tasks under
    a heading that contains 'term' (matching is case-insensitive)
-   **file** - if the argument matches a directory, the tasks in that file
    will be searched
-   **directory** - if the argument matches a directory, files under
    that directory will be searched (if you have directories with short
    names like "doc", this could be ambiguous, use "./doc" to clarify)

```bash
(computer)% whatnext research
projects/obelisk.md:
    # Project Obelisk
    Something something star gate
    - [ ] research into runic meaning

(computer)% whatnext research question
tasks.md:
    # Get S Done / MEDIUM
    - [ ] question entire existence

projects/obelisk.md:
    # Project Obelisk
    Something something star gate
    - [ ] research into runic meaning
```

## Limiting output

To show only a subset of tasks, pass a number as an argument:

```bash
(computer)% whatnext 3
tasks.md:
    # Get S Done / OVERDUE 1m 3w
    - [ ] come up with better projects
projects/obelisk.md:
    # Project Obelisk / Discovery / OVERDUE 31y 2m
    Mess with Jackson
    - [<] watch archaeologists discover (needs time machine)

projects/obelisk.md:
    # Project Obelisk / HIGH
    Something something star gate
    - [ ] bury obelisk in desert
```

Tasks are shown in priority order, so the limit returns the most urgent first.
The limit can be combined with other arguments.

To show a random selection of tasks rather than by priority, use `5r`.


## Arguments

`whatnext` takes the following optional arguments:

-   `-a` / `--all` — show all tasks, the default is to list
    `--open --partial --blocked`.

    ```bash
    (computer)% whatnext --all
    tasks.md:
        # Get S Done / OVERDUE 1m 3w
        - [ ] come up with better projects
    projects/obelisk.md:
        # Project Obelisk / Discovery / OVERDUE 31y 2m
        Mess with Jackson
        - [<] watch archaeologists discover (needs time machine)

    projects/obelisk.md:
        # Project Obelisk / HIGH
        Something something star gate
        - [ ] bury obelisk in desert

    tasks.md:
        # Get S Done / MEDIUM
        - [ ] question entire existence

    tasks.md:
        # Get S Done / IMMINENT 11d
        - [ ] start third project

    projects/obelisk.md:
        # Project Obelisk
        Something something star gate
        - [/] carve runes into obelisk
        - [ ] research into runic meaning

    archived/projects/tangerine.md:
        # Project Tangerine / FINISHED
        - [X] acquire trebuchet plans
        - [X] source counterweight materials
        - [X] build it
        - [#] throw fruit at neighbours (they moved away)
    ```

-   `-o` / `--open` — show only open tasks.

-   `-p` / `--partial` — show only in progress tasks.

-   `-b` / `--blocked` — show only blocked tasks.

-   `-d` / `--done` — show only completed tasks.

-   `-c` / `--cancelled` — show only cancelled tasks.

-   `--priority [level]` — show only tasks of 'level' priority; levels are
    `overdue`, `imminent`, `high`, `medium`, `normal`.

-   `-s` / `--summary` — summarise the tasks found in files,
    rather than listing the tasks within:

    ```bash
    (computer)% whatnext --summary
                                                        B P O
    ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░              0 0 3  tasks.md
    ▚▚▚▚▚▚▚▚▚▚▚▚▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░░░░░░░░░░░░░░░░  1 1 2  projects/obelisk.md
                                                        ─────
                                                        1 1 5  7, of 11 total

    ▚ Blocked  ▓ Partial  ░ Open
    ```

    When there are multiple files, the progress bars are sized relative to the
    task file with the most tasks.

    By default it only summarises the incomplete tasks, add `--all` to see
    the full state of your task files:

    ```bash
    (computer)% whatnext --summary --all
                                         C D B P O
    ░░░░░░░░░░░░░░░░░░░░░░░░░░           0 0 0 0 3  tasks.md
    ▓▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒░░░░░░░░░░░░░░░░░  0 0 1 1 2  projects/obelisk.md
    ▚▚▚▚▚▚▚▚▚██████████████████████████  1 3 0 0 0  archived/projects/tangerine.md
                                         ─────────
                                         1 3 1 1 5  11, of 11 total

    ▚ Cancelled  █ Done  ▓ Blocked  ▒ Partial  ░ Open
    ```

    Individual states and priorities can be summarised alone:

    ```bash
    (computer)% whatnext --summary --blocked
                                                            B
    ██████████████████████████████████████████████████████  1  projects/obelisk.md

    █ Blocked
    ```

    or as part of the whole with `--relative`:

    ```bash
    (computer)% whatnext --summary --relative --priority high
                                              H  ~
    ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░            0  3  tasks.md
    ██████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  1  3  projects/obelisk.md
    ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  0  4  archived/projects/tangerine.md
                                              ────
                                              1 10  11, of 11 total

    █ High  ░ (Overdue/Imminent/Medium/Normal)
    ```

-   `-q` / `--quiet` — suppress warnings (or `$WHATNEXT_QUIET=1`).

-   `--ignore [pattern]` — ignore files matching the given
    [filename pattern][glob]; can be specified multiple times
    or put in the config file.

-   `--config` — path to the [config file](dotwhatnext.md), defaults
    to `.whatnext` or `$WHATNEXT_CONFIG`.

-   `--dir` — the directory to search through for Markdown files,
    defaults to `.` or `$WHATNEXT_DIR`.

-   `-h` / `--help` — show a short or full usage reminder.

-   `--version` — show the version and exit.


[glob]: https://docs.python.org/3/library/fnmatch.html
