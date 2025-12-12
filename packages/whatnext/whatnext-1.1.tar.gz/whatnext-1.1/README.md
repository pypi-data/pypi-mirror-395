# What next?

Document your tasks in Markdown files, using an expanded version of the
original [GitHub task list notation][sn]:

```markdown
- [ ] open, this task is outstanding
- [/] in progress, this task is partially complete
- [X] complete, this task has been finished
- [#] cancelled, this task has been scratched
- [<] blocked, this task needs more input

- [ ] _a little more important_
- [ ] **a lot more important**

- [ ] get NYE fireworks tickets @2025-12-31
```

Then install `whatnext`:

```bash
pip install whatnext
```

Now run it and it'll tell you what's next, sorting by priority and state:

```bash
(computer)% whatnext
README.md:
    # What next? / HIGH
    - [ ] a lot more important

README.md:
    # What next? / MEDIUM
    - [ ] a little more important

README.md:
    # What next? / IMMINENT 6d
    - [ ] get NYE fireworks tickets

README.md:
    # What next?
    - [/] in progress, this task is partially complete
    - [ ] open, this task is outstanding
    - [<] blocked, this task needs more input
```

More detail to be found:

- [The basics of task formatting](docs/basics.md)
- [Prioritisation](docs/prioritisation.md)
- [Deadlines](docs/deadlines.md)
- [Annotations](docs/annotations.md)
- [whatnext usage and arguments](docs/usage.md)
- [The `.whatnext` file](docs/dotwhatnext.md)


## The reason

I like to keep tasks in Markdown files. That way they can be interspersed
within instructions, serving as reminders, FIXMEs, and other todos.


[sn]: https://blog.github.com/2013-01-09-task-lists-in-gfm-issues-pulls-comments/
