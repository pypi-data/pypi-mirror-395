# Prioritisation

Tasks have an inherent prioritisation when appearing higher in your task
files, and task files in the project root appear before task files
buried in directories.

But if you still need a way to maintain the order but still be able to flag
an individual task, that is done with Markdown emphasis:

```markdown
- [ ] top, but not urgent, task
- [ ] _semi-urgent task_
- [ ] **super-urgent task**
```

Flagging a header makes every task under it higher priority, including
anything in a subordinate grouping.

Flagging a task and the header doesn't make it even higher priority,
there are only three states of priority.

```markdown
- [/] not a high priority task

# **do these first**

- [ ] inherently high priority task, because of the header
- [ ] **no extra priority, still listed second**

## grouped, but still highest priority

- [X] header priority cascades down

# more tasks

- [#] normal priority, new header resets that
```

Highest priority wins, so a _high_ priority task under a **highest** priority
header is still highest priority.

There are two even higher priorities `imminent` and `overdue`, which are
[triggered by deadlines](deadlines.md).
