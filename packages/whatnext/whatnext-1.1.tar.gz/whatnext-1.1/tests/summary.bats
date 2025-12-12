bats_require_minimum_version 1.5.0

@test "summarise incomplete tasks" {
    WHATNEXT_TODAY=2025-01-01 \
        run --separate-stderr \
            whatnext \
                --summary

    expected_output=$(sed -e 's/^        //' <<"        EOF"
                                                        B P  O
        ░░░░░░░░░░░░░░░                                 0 0  2  docs/annotations.md
        ▚▚▚▚▚▚▚▚▓▓▓▓▓▓▓░░░░░░░░░░░░░░░░░░░░░░░          1 1  3  docs/basics.md
        ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░          0 0  5  docs/deadlines.md
        ▓▓▓▓▓▓▓▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  0 1  5  docs/prioritisation.md
        ░░░░░░░░                                        0 0  1  tests/headerless.md
                                                        ──────
                                                        1 2 16  19, of 26 total

        ▚ Blocked  ▓ Partial  ░ Open
        EOF
    )
    diff -u <(echo "$expected_output") <(echo "$output")
    [ $status -eq 0 ]
}

@test "summarise all states" {
    WHATNEXT_TODAY=2025-01-01 \
        run --separate-stderr \
            whatnext \
                --summary \
                --all

    expected_output=$(sed -e 's/^        //' <<"        EOF"
                                                    C D B P  O
        ░░░░░░░░░░                                  0 0 0 0  2  docs/annotations.md
        ▚▚▚▚▚██████▓▓▓▓▓▒▒▒▒▒░░░░░░░░░░░░░░░░       1 1 1 1  3  docs/basics.md
        ░░░░░░░░░░░░░░░░░░░░░░░░░░                  0 0 0 0  5  docs/deadlines.md
        ▚▚▚▚▚█████▒▒▒▒▒▒░░░░░░░░░░░░░░░░░░░░░░░░░░  1 1 0 1  5  docs/prioritisation.md
        ░░░░░                                       0 0 0 0  1  tests/headerless.md
        ████████████████                            0 3 0 0  0  archive/done/tasks.md
                                                    ──────────
                                                    2 5 1 2 16  26, of 26 total

        ▚ Cancelled  █ Done  ▓ Blocked  ▒ Partial  ░ Open
        EOF
    )
    diff -u <(echo "$expected_output") <(echo "$output")
    [ $status -eq 0 ]

    # should be functionally equivalent...
    WHATNEXT_TODAY=2025-01-01 \
        run --separate-stderr \
            whatnext \
                --summary \
                --cancelled \
                --done \
                --blocked \
                --partial \
                --open
    diff -u <(echo "$expected_output") <(echo "$output")
    [ $status -eq 0 ]

    # ...and order of args is irrelevant, desired ordering is applied
    WHATNEXT_TODAY=2025-01-01 \
        run --separate-stderr \
            whatnext \
                --summary \
                --open \
                --blocked \
                --done \
                --partial \
                --cancelled
    diff -u <(echo "$expected_output") <(echo "$output")
    [ $status -eq 0 ]
}

@test "summarise all states, resized" {
    COLUMNS=40 \
    WHATNEXT_TODAY=2025-01-01 \
        run --separate-stderr \
            whatnext \
                --summary \
                --all

    expected_output=$(sed -e 's/^        //' <<"        EOF"
                    C D B P  O
        ░░          0 0 0 0  2  docs/annotations.md
        ▚██▓▒░░░░   1 1 1 1  3  docs/basics.md
        ░░░░░░      0 0 0 0  5  docs/deadlines.md
        ▚█▒▒░░░░░░  1 1 0 1  5  docs/prioritisation.md
        ░           0 0 0 0  1  tests/headerless.md
        ████        0 3 0 0  0  archive/done/tasks.md
                    ──────────
                    2 5 1 2 16  26, of 26 total

        ▚ Cancelled  █ Done  ▓ Blocked  ▒ Partial  ░ Open
        EOF
    )
    diff -u <(echo "$expected_output") <(echo "$output")
    [ $status -eq 0 ]
}

@test "summarise open tasks" {
    WHATNEXT_TODAY=2025-01-01 \
        run --separate-stderr \
            whatnext \
                --summary \
                --open

    expected_output=$(sed -e 's/^        //' <<"        EOF"
                                                             O
        ████████████████████                                 2  docs/annotations.md
        ██████████████████████████████                       3  docs/basics.md
        ██████████████████████████████████████████████████   5  docs/deadlines.md
        ██████████████████████████████████████████████████   5  docs/prioritisation.md
        ██████████                                           1  tests/headerless.md
                                                            ──
                                                            16  16, of 26 total

        █ Open
        EOF
    )
    diff -u <(echo "$expected_output") <(echo "$output")
    [ $status -eq 0 ]
}

@test "summarise open tasks, relative" {
    WHATNEXT_TODAY=2025-01-01 \
        run --separate-stderr \
            whatnext \
                --summary \
                --open \
                --relative

    expected_output=$(sed -e 's/^        //' <<"        EOF"
                                                          O  ~
        ████████████                                      2  0  docs/annotations.md
        ██████████████████░░░░░░░░░░░░░░░░░░░░░░░         3  4  docs/basics.md
        █████████████████████████████                     5  0  docs/deadlines.md
        █████████████████████████████░░░░░░░░░░░░░░░░░░   5  3  docs/prioritisation.md
        ██████                                            1  0  tests/headerless.md
        ░░░░░░░░░░░░░░░░░░                                0  3  archive/done/tasks.md
                                                         ─────
                                                         16 10  26, of 26 total

        █ Open  ░ (Cancelled/Done/Blocked/Partial)
        EOF
    )
    diff -u <(echo "$expected_output") <(echo "$output")
    [ $status -eq 0 ]
}

@test "summarise partial tasks" {
    WHATNEXT_TODAY=2025-01-01 \
        run --separate-stderr \
            whatnext \
                --summary \
                --partial \
                --relative

    expected_output=$(sed -e 's/^        //' <<"        EOF"
                                                          P  ~
        ░░░░░░░░░░░░                                      0  2  docs/annotations.md
        ██████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░        1  6  docs/basics.md
        ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░                    0  5  docs/deadlines.md
        ██████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  1  7  docs/prioritisation.md
        ░░░░░░                                            0  1  tests/headerless.md
        ░░░░░░░░░░░░░░░░░░                                0  3  archive/done/tasks.md
                                                          ────
                                                          2 24  26, of 26 total

        █ Partial  ░ (Cancelled/Done/Blocked/Open)
        EOF
    )
    diff -u <(echo "$expected_output") <(echo "$output")
    [ $status -eq 0 ]
}

@test "summarise blocked tasks" {
    WHATNEXT_TODAY=2025-01-01 \
        run --separate-stderr \
            whatnext \
                --summary \
                --blocked \
                --relative

    expected_output=$(sed -e 's/^        //' <<"        EOF"
                                                          B  ~
        ░░░░░░░░░░░░                                      0  2  docs/annotations.md
        ██████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░        1  6  docs/basics.md
        ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░                    0  5  docs/deadlines.md
        ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  0  8  docs/prioritisation.md
        ░░░░░░                                            0  1  tests/headerless.md
        ░░░░░░░░░░░░░░░░░░                                0  3  archive/done/tasks.md
                                                          ────
                                                          1 25  26, of 26 total

        █ Blocked  ░ (Cancelled/Done/Partial/Open)
        EOF
    )
    diff -u <(echo "$expected_output") <(echo "$output")
    [ $status -eq 0 ]
}

@test "summarise done tasks" {
    WHATNEXT_TODAY=2025-01-01 \
        run --separate-stderr \
            whatnext \
                --summary \
                --done \
                --relative

    expected_output=$(sed -e 's/^        //' <<"        EOF"
                                                          D  ~
        ░░░░░░░░░░░░                                      0  2  docs/annotations.md
        ██████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░        1  6  docs/basics.md
        ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░                    0  5  docs/deadlines.md
        ██████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  1  7  docs/prioritisation.md
        ░░░░░░                                            0  1  tests/headerless.md
        ██████████████████                                3  0  archive/done/tasks.md
                                                          ────
                                                          5 21  26, of 26 total

        █ Done  ░ (Cancelled/Blocked/Partial/Open)
        EOF
    )
    diff -u <(echo "$expected_output") <(echo "$output")
    [ $status -eq 0 ]
}

@test "summarise cancelled tasks" {
    WHATNEXT_TODAY=2025-01-01 \
        run --separate-stderr \
            whatnext \
                --summary \
                --cancelled \
                --relative

    expected_output=$(sed -e 's/^        //' <<"        EOF"
                                                          C  ~
        ░░░░░░░░░░░░                                      0  2  docs/annotations.md
        ██████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░        1  6  docs/basics.md
        ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░                    0  5  docs/deadlines.md
        ██████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  1  7  docs/prioritisation.md
        ░░░░░░                                            0  1  tests/headerless.md
        ░░░░░░░░░░░░░░░░░░                                0  3  archive/done/tasks.md
                                                          ────
                                                          2 24  26, of 26 total

        █ Cancelled  ░ (Done/Blocked/Partial/Open)
        EOF
    )
    diff -u <(echo "$expected_output") <(echo "$output")
    [ $status -eq 0 ]
}

@test "summarise multiple states" {
    WHATNEXT_TODAY=2025-01-01 \
        run --separate-stderr \
            whatnext \
                --summary \
                --open \
                --cancelled \
                --relative

    expected_output=$(sed -e 's/^        //' <<"        EOF"
                                                        C  O ~
        ░░░░░░░░░░░░                                    0  2 0  docs/annotations.md
        ██████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░        1  3 3  docs/basics.md
        ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░                   0  5 0  docs/deadlines.md
        ██████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  1  5 2  docs/prioritisation.md
        ░░░░░░                                          0  1 0  tests/headerless.md
        ░░░░░░░░░░░░░░░░░                               0  0 3  archive/done/tasks.md
                                                        ──────
                                                        2 16 8  26, of 26 total

        █ Cancelled  ░ Open  ░ (Done/Blocked/Partial)
        EOF
    )
    diff -u <(echo "$expected_output") <(echo "$output")
    [ $status -eq 0 ]
}

@test "summarise high priority tasks" {
    WHATNEXT_TODAY=2025-01-01 \
        run --separate-stderr \
            whatnext \
                --summary \
                --priority high \
                --relative

    expected_output=$(sed -e 's/^        //' <<"        EOF"
                                                          H  ~
        ░░░░░░░░░░░░                                      0  2  docs/annotations.md
        ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░        0  7  docs/basics.md
        ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░                    0  5  docs/deadlines.md
        ██████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  3  5  docs/prioritisation.md
        ░░░░░░                                            0  1  tests/headerless.md
        ░░░░░░░░░░░░░░░░░░                                0  3  archive/done/tasks.md
                                                          ────
                                                          3 23  26, of 26 total

        █ High  ░ (Overdue/Imminent/Medium/Normal)
        EOF
    )
    diff -u <(echo "$expected_output") <(echo "$output")
    [ $status -eq 0 ]
}

@test "summarise medium priority tasks" {
    WHATNEXT_TODAY=2025-01-01 \
        run --separate-stderr \
            whatnext \
                --summary \
                --priority medium \
                --relative

    expected_output=$(sed -e 's/^        //' <<"        EOF"
                                                          M  ~
        ░░░░░░░░░░░░                                      0  2  docs/annotations.md
        ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░        0  7  docs/basics.md
        ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░                    0  5  docs/deadlines.md
        ██████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  1  7  docs/prioritisation.md
        ░░░░░░                                            0  1  tests/headerless.md
        ░░░░░░░░░░░░░░░░░░                                0  3  archive/done/tasks.md
                                                          ────
                                                          1 25  26, of 26 total

        █ Medium  ░ (Overdue/Imminent/High/Normal)
        EOF
    )
    diff -u <(echo "$expected_output") <(echo "$output")
    [ $status -eq 0 ]
}

@test "summarise multiple priority levels" {
    WHATNEXT_TODAY=2025-01-01 \
        run --separate-stderr \
            whatnext \
                --summary \
                --priority high \
                --priority normal \
                --relative

    expected_output=$(sed -e 's/^        //' <<"        EOF"
                                                        H  N ~
        ░░░░░░░░░░░░                                    0  2 0  docs/annotations.md
        ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░        0  5 2  docs/basics.md
        ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░                   0  5 0  docs/deadlines.md
        █████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  3  2 3  docs/prioritisation.md
        ░░░░░░                                          0  1 0  tests/headerless.md
        ░░░░░░░░░░░░░░░░░                               0  0 3  archive/done/tasks.md
                                                        ──────
                                                        3 15 8  26, of 26 total

        █ High  ░ Normal  ░ (Overdue/Imminent/Medium)
        EOF
    )
    diff -u <(echo "$expected_output") <(echo "$output")
    [ $status -eq 0 ]
}
