# Deadlines

Tasks can be marked as needing to be done by a certain date:

```markdown
# version 0.5
- [ ] complete and release @2025-12-05
```

This task has not been given a priority, so would appear in the bulk of the
task list. That is, until two weeks before the date mentioned, at which point
it will be given a priority of `imminent`. And if the date is now in the past,
the priority set will be `overdue`.

The default two-week urgency window in which a task is marked imminent
can be controlled:

```markdown
# Christmas dinner
- [ ] book Christmas delivery @2025-12-23/3w
```

The `/1d` adjustment can be a number of days or weeks. `/0d` means the
task will only change priority on the day itself.


# Deadlines and priorities

Due date takes precedence over priorities. Assuming the date today was
December 1st, both of these tasks would be listed as having normal
priority.

```
# Christmas dinner
- [ ] _prep the make-ahead gravy_ @2025-12-25/1d
- [ ] **roast the potatoes** @2025-12-25/0d
- [ ] prep sprouts @2025-12-25
```

Later, gravy would appear as medium priority on December 24th,
and potatoes as high priority on December 25th.
