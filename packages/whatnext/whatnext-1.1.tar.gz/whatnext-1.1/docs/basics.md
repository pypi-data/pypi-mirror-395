# Indicating the state of a task

Tasks have states, which are indicated as such:

```markdown
- [ ] open, this task is outstanding
- [/] in progress, this task is partially complete
- [X] complete, this task has been finished
- [#] cancelled, this task has been scratched
- [<] blocked, this task needs more input

- [@] no idea what this means
```

By default, `whatnext` lists open, in progress, and blocked tasks. In progress
tasks are shown first, blocked tasks are shown last. Completed and cancelled
tasks are not listed unless `--all` is used.

Headers are used in grouping tasks. The second-level header that comes next
shows these tasks are a part of the main header. This does not indicate
a lower priority, only grouping.

An unknown state marker will generate a warning, but they can be suppressed
if you are using other states for a purpose.


## Multiline tasks and indentation

Tasks can be indented, and their text can continue across lines:

```markdown
    - [ ] Lorem ipsum dolor sit amet,
          consectetur adipisicing elit,
          sed do  eiusmod  tempor   incididunt
          ut labore et     dolore magna aliqua.
```

The output of `whatnext` will wrap text to the terminal width, and does not
consider spacing of individual words or line wrapping semantically important.

Indentation of individual tasks is ignored, but the continuation has
to be indented to match, unlike in this task which is detected as
"Ut enim ad minim veniam," only:

```markdown
    - [ ] Ut enim ad minim veniam,
         quis nostrud exercitation ullamco laboris
```
