bats_require_minimum_version 1.5.0

@test "list tasks" {
    WHATNEXT_TODAY=2025-12-25 \
        run --separate-stderr \
            whatnext

    expected_output=$(sed -e 's/^        //' <<"        EOF"
        docs/deadlines.md:
            # version 0.5 / OVERDUE 2w 6d
            - [ ] complete and release
            # Christmas dinner / OVERDUE 2d
            - [ ] book Christmas delivery

        docs/deadlines.md:
            # Christmas dinner / HIGH
            - [ ] roast the potatoes
        docs/prioritisation.md:
            # Prioritisation / HIGH
            - [ ] super-urgent task
            # do these first / HIGH
            - [ ] inherently high priority task, because of the header
            - [ ] no extra priority, still listed second

        docs/deadlines.md:
            # Christmas dinner / MEDIUM
            - [ ] prep the make-ahead gravy
        docs/prioritisation.md:
            # Prioritisation / MEDIUM
            - [ ] semi-urgent task

        docs/deadlines.md:
            # Christmas dinner / IMMINENT TODAY
            - [ ] prep sprouts

        docs/annotations.md:
            # Project Anvil
            Let the anvils ring!
            - [ ] introduce ourselves
            - [ ] inherit throne
        docs/basics.md:
            # Indicating the state of a task
            - [/] in progress, this task is partially complete
            - [ ] open, this task is outstanding
            - [<] blocked, this task needs more input
            # Indicating the state of a task / Multiline tasks and indentation
            - [ ] Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do
                  eiusmod tempor incididunt ut labore et dolore magna aliqua.
            - [ ] Ut enim ad minim veniam,
        docs/prioritisation.md:
            # Prioritisation
            - [/] not a high priority task
            - [ ] top, but not urgent, task
        tests/headerless.md:
            - [ ] I am not a task, I am a free list!
        EOF
    )
    diff -u <(echo "$expected_output") <(echo "$output")

    expected_stderr="WARNING: ignoring invalid state '@' in 'no idea what this means',"
    expected_stderr+=" docs/basics.md line 12"
    diff -u <(echo "$expected_stderr") <(echo "$stderr")

    # no extraneous blank lines at the end
    [ $(WHATNEXT_TODAY=2025-12-25 whatnext 2>/dev/null | wc -l) -eq 47 ]

    [ $status -eq 0 ]
}

@test "default list is open, partial, blocked" {
    diff -u <(whatnext) <(whatnext --open --partial --blocked)
}


@test "list tasks, changes width" {
    COLUMNS=40 \
    WHATNEXT_TODAY=2025-01-01 \
        run --separate-stderr \
            whatnext

    expected_output=$(sed -e 's/^        //' <<"        EOF"
        docs/prioritisation.md:
            # Prioritisation / HIGH
            - [ ] super-urgent task
            # do these first / HIGH
            - [ ] inherently high priority task,
                  because of the header
            - [ ] no extra priority, still
                  listed second

        docs/prioritisation.md:
            # Prioritisation / MEDIUM
            - [ ] semi-urgent task

        docs/annotations.md:
            # Project Anvil
            Let the anvils ring!
            - [ ] introduce ourselves
            - [ ] inherit throne
        docs/basics.md:
            # Indicating the state of a task
            - [/] in progress, this task is
                  partially complete
            - [ ] open, this task is outstanding
            - [<] blocked, this task needs more
                  input
            # Indicating the state of a task /
              Multiline tasks and indentation
            - [ ] Lorem ipsum dolor sit amet,
                  consectetur adipisicing elit,
                  sed do eiusmod tempor
                  incididunt ut labore et dolore
                  magna aliqua.
            - [ ] Ut enim ad minim veniam,
        docs/deadlines.md:
            # version 0.5
            - [ ] complete and release
            # Christmas dinner
            - [ ] book Christmas delivery
            - [ ] prep the make-ahead gravy
            - [ ] roast the potatoes
            - [ ] prep sprouts
        docs/prioritisation.md:
            # Prioritisation
            - [/] not a high priority task
            - [ ] top, but not urgent, task
        tests/headerless.md:
            - [ ] I am not a task, I am a free
                  list!
        EOF
    )
    diff -u <(echo "$expected_output") <(echo "$output")
    [ $status -eq 0 ]
}

@test "list all tasks" {
    WHATNEXT_TODAY=2025-01-01 \
        run --separate-stderr \
            whatnext \
                --all

    expected_output=$(sed -e 's/^        //' <<"        EOF"
        docs/prioritisation.md:
            # Prioritisation / HIGH
            - [ ] super-urgent task
            # do these first / HIGH
            - [ ] inherently high priority task, because of the header
            - [ ] no extra priority, still listed second

        docs/prioritisation.md:
            # Prioritisation / MEDIUM
            - [ ] semi-urgent task

        docs/annotations.md:
            # Project Anvil
            Let the anvils ring!
            - [ ] introduce ourselves
            - [ ] inherit throne
        docs/basics.md:
            # Indicating the state of a task
            - [/] in progress, this task is partially complete
            - [ ] open, this task is outstanding
            - [<] blocked, this task needs more input
            # Indicating the state of a task / Multiline tasks and indentation
            - [ ] Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do
                  eiusmod tempor incididunt ut labore et dolore magna aliqua.
            - [ ] Ut enim ad minim veniam,
        docs/deadlines.md:
            # version 0.5
            - [ ] complete and release
            # Christmas dinner
            - [ ] book Christmas delivery
            - [ ] prep the make-ahead gravy
            - [ ] roast the potatoes
            - [ ] prep sprouts
        docs/prioritisation.md:
            # Prioritisation
            - [/] not a high priority task
            - [ ] top, but not urgent, task
        tests/headerless.md:
            - [ ] I am not a task, I am a free list!

        docs/basics.md:
            # Indicating the state of a task / FINISHED
            - [X] complete, this task has been finished
            - [#] cancelled, this task has been scratched
        docs/prioritisation.md:
            # do these first / grouped, but still highest priority / FINISHED
            - [X] header priority cascades down
            # more tasks / FINISHED
            - [#] normal priority, new header resets that
        archive/done/tasks.md:
            # Some old stuff / FINISHED
            - [X] Do the first thing
            - [X] Do the second thing
            - [X] do the last thing all lowercase
        EOF
    )
    diff -u <(echo "$expected_output") <(echo "$output")
    [ $status -eq 0 ]
}

@test "list tasks with --dir" {
    cp -r . "$BATS_TEST_TMPDIR/project"

    WHATNEXT_TODAY=2025-01-01 \
        run --separate-stderr \
            whatnext \
                --dir "$BATS_TEST_TMPDIR/project"

    expected_output=$(sed -e 's/^        //' <<"        EOF"
        docs/prioritisation.md:
            # Prioritisation / HIGH
            - [ ] super-urgent task
            # do these first / HIGH
            - [ ] inherently high priority task, because of the header
            - [ ] no extra priority, still listed second

        docs/prioritisation.md:
            # Prioritisation / MEDIUM
            - [ ] semi-urgent task

        docs/annotations.md:
            # Project Anvil
            Let the anvils ring!
            - [ ] introduce ourselves
            - [ ] inherit throne
        docs/basics.md:
            # Indicating the state of a task
            - [/] in progress, this task is partially complete
            - [ ] open, this task is outstanding
            - [<] blocked, this task needs more input
            # Indicating the state of a task / Multiline tasks and indentation
            - [ ] Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do
                  eiusmod tempor incididunt ut labore et dolore magna aliqua.
            - [ ] Ut enim ad minim veniam,
        docs/deadlines.md:
            # version 0.5
            - [ ] complete and release
            # Christmas dinner
            - [ ] book Christmas delivery
            - [ ] prep the make-ahead gravy
            - [ ] roast the potatoes
            - [ ] prep sprouts
        docs/prioritisation.md:
            # Prioritisation
            - [/] not a high priority task
            - [ ] top, but not urgent, task
        tests/headerless.md:
            - [ ] I am not a task, I am a free list!
        EOF
    )
    diff -u <(echo "$expected_output") <(echo "$output")
    [ $status -eq 0 ]
}

@test "warnings can be suppressed" {
    run --separate-stderr \
        whatnext \
            --quiet
    [ $status -eq 0 ]
    [ -z "$stderr" ]

    WHATNEXT_QUIET=1 \
        run --separate-stderr \
            whatnext
    [ $status -eq 0 ]
    [ -z "$stderr" ]
}

@test "filter just open tasks" {
    run --separate-stderr \
        whatnext \
            --open \
            docs/basics.md

    expected_output=$(sed -e 's/^        //' <<"        EOF"
        docs/basics.md:
            # Indicating the state of a task
            - [ ] open, this task is outstanding
            # Indicating the state of a task / Multiline tasks and indentation
            - [ ] Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do
                  eiusmod tempor incididunt ut labore et dolore magna aliqua.
            - [ ] Ut enim ad minim veniam,
        EOF
    )
    diff -u <(echo "$expected_output") <(echo "$output")
    [ $status -eq 0 ]

    # short flag
    run --separate-stderr \
        whatnext \
            -o \
            docs/basics.md
    diff -u <(echo "$expected_output") <(echo "$output")
    [ $status -eq 0 ]
}

@test "filter just in progress tasks" {
    run --separate-stderr \
        whatnext \
            --partial \
            docs/basics.md

    expected_output=$(sed -e 's/^        //' <<"        EOF"
        docs/basics.md:
            # Indicating the state of a task
            - [/] in progress, this task is partially complete
        EOF
    )
    diff -u <(echo "$expected_output") <(echo "$output")
    [ $status -eq 0 ]

    # short flag
    run --separate-stderr \
        whatnext \
            -p \
            docs/basics.md
    diff -u <(echo "$expected_output") <(echo "$output")
    [ $status -eq 0 ]
}

@test "filter just blocked tasks" {
    run --separate-stderr \
        whatnext \
            --blocked \
            docs/basics.md

    expected_output=$(sed -e 's/^        //' <<"        EOF"
        docs/basics.md:
            # Indicating the state of a task
            - [<] blocked, this task needs more input
        EOF
    )
    diff -u <(echo "$expected_output") <(echo "$output")
    [ $status -eq 0 ]

    # short flag
    run --separate-stderr \
        whatnext \
            -b \
            docs/basics.md
    diff -u <(echo "$expected_output") <(echo "$output")
    [ $status -eq 0 ]
}

@test "filter just completed tasks" {
    run --separate-stderr \
        whatnext \
            --done \
            docs/basics.md

    expected_output=$(sed -e 's/^        //' <<"        EOF"
        docs/basics.md:
            # Indicating the state of a task / FINISHED
            - [X] complete, this task has been finished
        EOF
    )
    diff -u <(echo "$expected_output") <(echo "$output")
    [ $status -eq 0 ]

    # short flag
    run --separate-stderr \
        whatnext \
            -d \
            docs/basics.md
    diff -u <(echo "$expected_output") <(echo "$output")
    [ $status -eq 0 ]
}

@test "filter just cancelled tasks" {
    run --separate-stderr \
        whatnext \
            --cancelled \
            docs/basics.md

    expected_output=$(sed -e 's/^        //' <<"        EOF"
        docs/basics.md:
            # Indicating the state of a task / FINISHED
            - [#] cancelled, this task has been scratched
        EOF
    )
    diff -u <(echo "$expected_output") <(echo "$output")
    [ $status -eq 0 ]

    # short flag
    run --separate-stderr \
        whatnext \
            -c \
            docs/basics.md
    diff -u <(echo "$expected_output") <(echo "$output")
    [ $status -eq 0 ]
}

@test "state filters can be combined" {
    run --separate-stderr \
        whatnext \
            --blocked \
            --cancelled \
            docs/basics.md

    expected_output=$(sed -e 's/^        //' <<"        EOF"
        docs/basics.md:
            # Indicating the state of a task
            - [<] blocked, this task needs more input

        docs/basics.md:
            # Indicating the state of a task / FINISHED
            - [#] cancelled, this task has been scratched
        EOF
    )
    diff -u <(echo "$expected_output") <(echo "$output")
    [ $status -eq 0 ]

    run --separate-stderr \
        whatnext \
            --open \
            --partial \
            docs/basics.md

    expected_output=$(sed -e 's/^        //' <<"        EOF"
        docs/basics.md:
            # Indicating the state of a task
            - [/] in progress, this task is partially complete
            - [ ] open, this task is outstanding
            # Indicating the state of a task / Multiline tasks and indentation
            - [ ] Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do
                  eiusmod tempor incididunt ut labore et dolore magna aliqua.
            - [ ] Ut enim ad minim veniam,
        EOF
    )
    diff -u <(echo "$expected_output") <(echo "$output")
    [ $status -eq 0 ]

    run --separate-stderr \
        whatnext \
            --blocked \
            --cancelled \
            --done \
            --open \
            --partial \
            docs/basics.md

    expected_output=$(sed -e 's/^        //' <<"        EOF"
        docs/basics.md:
            # Indicating the state of a task
            - [/] in progress, this task is partially complete
            - [ ] open, this task is outstanding
            - [<] blocked, this task needs more input
            # Indicating the state of a task / Multiline tasks and indentation
            - [ ] Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do
                  eiusmod tempor incididunt ut labore et dolore magna aliqua.
            - [ ] Ut enim ad minim veniam,

        docs/basics.md:
            # Indicating the state of a task / FINISHED
            - [X] complete, this task has been finished
            - [#] cancelled, this task has been scratched
        EOF
    )
    diff -u <(echo "$expected_output") <(echo "$output")
    [ $status -eq 0 ]
}

@test "state filter combines with search" {
    run --separate-stderr \
        whatnext \
            --open \
            lorem \
            docs/basics.md

    expected_output=$(sed -e 's/^        //' <<"        EOF"
        docs/basics.md:
            # Indicating the state of a task / Multiline tasks and indentation
            - [ ] Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do
                  eiusmod tempor incididunt ut labore et dolore magna aliqua.
        EOF
    )
    diff -u <(echo "$expected_output") <(echo "$output")
    [ $status -eq 0 ]
}

@test "filter by priority" {
    run --separate-stderr \
        whatnext \
            --priority high \
            docs/prioritisation.md

    expected_output=$(sed -e 's/^        //' <<"        EOF"
        docs/prioritisation.md:
            # Prioritisation / HIGH
            - [ ] super-urgent task
            # do these first / HIGH
            - [ ] inherently high priority task, because of the header
            - [ ] no extra priority, still listed second
        EOF
    )
    diff -u <(echo "$expected_output") <(echo "$output")
    [ $status -eq 0 ]
}

@test "filter multiple priorities" {
    run --separate-stderr \
        whatnext \
            --priority high \
            --priority medium \
            docs/prioritisation.md

    expected_output=$(sed -e 's/^        //' <<"        EOF"
        docs/prioritisation.md:
            # Prioritisation / HIGH
            - [ ] super-urgent task
            # do these first / HIGH
            - [ ] inherently high priority task, because of the header
            - [ ] no extra priority, still listed second

        docs/prioritisation.md:
            # Prioritisation / MEDIUM
            - [ ] semi-urgent task
        EOF
    )
    diff -u <(echo "$expected_output") <(echo "$output")
    [ $status -eq 0 ]
}

@test "filter by priority and search" {
    run --separate-stderr \
        whatnext \
            --priority high \
            header \
            docs/prioritisation.md

    expected_output=$(sed -e 's/^        //' <<"        EOF"
        docs/prioritisation.md:
            # do these first / HIGH
            - [ ] inherently high priority task, because of the header
        EOF
    )
    diff -u <(echo "$expected_output") <(echo "$output")
    [ $status -eq 0 ]
}

@test "numeric argument limits output" {
    WHATNEXT_TODAY=2025-01-01 \
        run --separate-stderr \
            whatnext \
                5

    expected_output=$(sed -e 's/^        //' <<"        EOF"
        docs/prioritisation.md:
            # Prioritisation / HIGH
            - [ ] super-urgent task
            # do these first / HIGH
            - [ ] inherently high priority task, because of the header
            - [ ] no extra priority, still listed second

        docs/prioritisation.md:
            # Prioritisation / MEDIUM
            - [ ] semi-urgent task

        docs/annotations.md:
            # Project Anvil
            Let the anvils ring!
            - [ ] introduce ourselves
        EOF
    )
    diff -u <(echo "$expected_output") <(echo "$output")
    [ $status -eq 0 ]
}

@test "limits combine" {
    WHATNEXT_TODAY=2025-01-01 \
        run --separate-stderr \
            whatnext \
                --blocked \
                5

    expected_output=$(sed -e 's/^        //' <<"        EOF"
        docs/basics.md:
            # Indicating the state of a task
            - [<] blocked, this task needs more input
        EOF
    )
    diff -u <(echo "$expected_output") <(echo "$output")
    [ $status -eq 0 ]
}

@test "random selection" {
    first_output=$(WHATNEXT_TODAY=2025-01-01 whatnext 3r)
    task_count=$(echo "$first_output" | grep -c '    - \[')
    [ "$task_count" -eq 3 ]

    # should exit long before 10,000 iterations, that's just safety
    found_different=0
    for i in $(seq 1 10000); do
        current=$(WHATNEXT_TODAY=2025-01-01 whatnext 3r)
        if [ "$current" != "$first_output" ]; then
            found_different=1
            break
        fi
    done

    [ "$found_different" -eq 1 ]
}
