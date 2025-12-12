# The `.whatnext` file

If you need to ignore a file (or three), but don't want to keep typing out
the `--ignore` option, you can put a `.whatnext` file in the directory
being examined for tasks:

```toml
# not considered in any summaries
ignore = [
    'README.md',
    'tasks.md',
    'docs/usage.md',
]
```

If you need to store it somewhere else, or have it be a different
filename, you can use the `--config` option, or set the location
in the environment variable `WHATNEXT_CONFIG`.
