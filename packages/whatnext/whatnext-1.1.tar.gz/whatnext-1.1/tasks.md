Development on `whatnext`.

(This file is used in tests/matching.bats,
which will start to fail if it is removed.)

# version 0.1 - basic functionality

- [X] show outstanding tasks in any Markdown file anywhere in the directory
- [X] be able to exclude set files from being considered
- [X] produce a summary of complete vs incomplete
- [X] document installation
- [X] document use
- [X] document `.whatnext` file structure
- [X] publish on pypi


# version 0.2 - searching

- [X] fix README links on pypi
- [X] autoversioning
- [X] `--version`
- [X] implement changelog
- [X] args that match dir search the dir
- [X] args that match files add them to the list
- [X] args that match neither are substring matches applied to tasks


# version 0.3 - new statuses

- [X] decide upon and implement "in progress"
- [X] decide upon and implement "cancelled"
- [X] decide upon and implement "blocked"
- [X] warnings for unknown formats
- [X] filter on incomplete
- [X] filter on in progress
- [X] filter on cancelled
- [X] filter on blocked
- [X] filter on complete
- [X] summarise individual states, but not combos


# version 0.4 - priorities

- [X] mark a single task as _medium_ priority
- [X] mark a single task **high** priority
- [X] mark a block of tasks via the header
- [X] sort higher priority tasks to the top -- decide if within files
      only or entire project
- [X] filter output to a subset of priorities
- [X] summarise priorities?


# version 0.5 - deadlines

- [X] mark a single task as having a deadline
- [X] embellish deadlines with custom urgency windows
- [X] filter output based on urgency
- [X] summarise urgency?
- [X] rework sample.md to example.md, and use it for docs/usage.md
- [X] completed/cancelled in sixth category


# version 1 - random enhancements

- [X] usage needs to document priority and deadline formats
- [X] colour-code the output
- [X] {n} most important tasks
- [X] pick tasks at random
- [X] some way to mark a section of Markdown for inclusion in the default
      output
- [X] add totals to summaries


# version 1.1 - bug fixes, improvements and editing files

- [X] fix tasks missing from `--summary --relative`
- [X] remove slashes from columns in summary, its just visual noise
- [X] `-e`/`--edit` to open matching task files in editor at the line
      number of the first match
