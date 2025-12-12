bats_require_minimum_version 1.5.0

setup_file() {
    export FAKE_EDITOR="$BATS_FILE_TMPDIR/fake-editor"
    export EDITOR_LOG="$BATS_FILE_TMPDIR/editor.log"
    export WHATNEXT_EDITOR="$FAKE_EDITOR"
    export WHATNEXT_TODAY=2025-01-01
    export WHATNEXT_QUIET=1
    export WHATNEXT_DIR=example
    export WHATNEXT_CONFIG=/dev/null
    cat > "$FAKE_EDITOR" << 'SCRIPT'
#!/bin/bash
echo "$@" >> "$EDITOR_LOG"
SCRIPT
    chmod +x "$FAKE_EDITOR"
}

setup() {
    rm -f "$EDITOR_LOG"
}

@test "open first task in editor" {
    run --separate-stderr \
        whatnext \
            --edit \
            projects/obelisk.md

    expected_output=$(sed -e 's/^        //' <<"        EOF"
        example/projects/obelisk.md:
            # Project Obelisk / Discovery / OVERDUE 30y 2m
            Mess with Jackson
            - [<] watch archaeologists discover (needs time machine)

        example/projects/obelisk.md:
            # Project Obelisk
            Something something star gate
            - [/] carve runes into obelisk
            - [ ] research into runic meaning
            - [ ] bury obelisk in desert
        EOF
    )
    diff -u <(echo "$expected_output") <(echo "$output")
    diff -u <(echo "+17 example/projects/obelisk.md") <(cat "$EDITOR_LOG")
    [ $status -eq 0 ]
}

@test "open first matching task in editor" {
    run --separate-stderr \
        whatnext \
            --edit \
            runes

    diff -u <(echo "+8 example/projects/obelisk.md") <(cat "$EDITOR_LOG")
    [ $status -eq 0 ]
}

@test "opens all matching files one by one" {
    run --separate-stderr \
        whatnext \
            --edit \
            --all

    expected_output=$(sed -e 's/^        //' <<"        EOF"
        +17 example/projects/obelisk.md
        +5 example/tasks.md
        +3 example/archived/projects/tangerine.md
        EOF
    )
    diff -u <(echo "$expected_output") <(cat "$EDITOR_LOG")
    [ $status -eq 0 ]
}

@test "no tasks does not open editor" {
    run --separate-stderr \
        whatnext \
            --edit \
            nonexistent-search-term-xyz

    [ ! -f "$EDITOR_LOG" ]
    [ $status -eq 0 ]
}
