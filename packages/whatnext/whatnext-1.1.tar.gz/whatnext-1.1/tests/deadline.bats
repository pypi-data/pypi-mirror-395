bats_require_minimum_version 1.5.0

# docs/deadlines.md contains:
#   - [ ] complete and release @2025-12-05              (imminent from Nov 21)
#   - [ ] book Christmas delivery @2025-12-23/3w        (imminent from Dec 2)
#   - [ ] _prep the make-ahead gravy_ @2025-12-25/1d    (medium from Dec 24)
#   - [ ] **roast the potatoes** @2025-12-25/0d         (high on Dec 25 only)
#   - [ ] prep sprouts @2025-12-25                      (imminent from Dec 11)

@test "before any deadline window, all tasks normal priority" {
    WHATNEXT_TODAY=2025-01-01 \
        run --separate-stderr \
            whatnext \
                docs/deadlines.md

    expected_output=$(sed -e 's/^        //' <<"        EOF"
        docs/deadlines.md:
            # version 0.5
            - [ ] complete and release
            # Christmas dinner
            - [ ] book Christmas delivery
            - [ ] prep the make-ahead gravy
            - [ ] roast the potatoes
            - [ ] prep sprouts
        EOF
    )
    diff -u <(echo "$expected_output") <(echo "$output")
    [ $status -eq 0 ]
}

@test "within 3w window, book Christmas delivery becomes imminent" {
    # Dec 2 is exactly 3 weeks before Dec 23
    # "complete and release" is also imminent (Nov 21 was 2 weeks before Dec 5)
    WHATNEXT_TODAY=2025-12-02 \
        run --separate-stderr \
            whatnext \
                docs/deadlines.md

    expected_output=$(sed -e 's/^        //' <<"        EOF"
        docs/deadlines.md:
            # version 0.5 / IMMINENT 3d
            - [ ] complete and release
            # Christmas dinner / IMMINENT 3w
            - [ ] book Christmas delivery

        docs/deadlines.md:
            # Christmas dinner
            - [ ] prep the make-ahead gravy
            - [ ] roast the potatoes
            - [ ] prep sprouts
        EOF
    )
    diff -u <(echo "$expected_output") <(echo "$output")
    [ $status -eq 0 ]
}

@test "within default 2w window, complete and release becomes imminent" {
    # Nov 21 is exactly 2 weeks before Dec 5
    WHATNEXT_TODAY=2025-11-21 \
        run --separate-stderr \
            whatnext \
                docs/deadlines.md

    expected_output=$(sed -e 's/^        //' <<"        EOF"
        docs/deadlines.md:
            # version 0.5 / IMMINENT 2w
            - [ ] complete and release

        docs/deadlines.md:
            # Christmas dinner
            - [ ] book Christmas delivery
            - [ ] prep the make-ahead gravy
            - [ ] roast the potatoes
            - [ ] prep sprouts
        EOF
    )
    diff -u <(echo "$expected_output") <(echo "$output")
    [ $status -eq 0 ]
}

@test "on deadline day, 0d task becomes high" {
    WHATNEXT_TODAY=2025-12-25 \
        run --separate-stderr \
            whatnext \
                docs/deadlines.md

    expected_output=$(sed -e 's/^        //' <<"        EOF"
        docs/deadlines.md:
            # version 0.5 / OVERDUE 2w 6d
            - [ ] complete and release
            # Christmas dinner / OVERDUE 2d
            - [ ] book Christmas delivery

        docs/deadlines.md:
            # Christmas dinner / HIGH
            - [ ] roast the potatoes

        docs/deadlines.md:
            # Christmas dinner / MEDIUM
            - [ ] prep the make-ahead gravy

        docs/deadlines.md:
            # Christmas dinner / IMMINENT TODAY
            - [ ] prep sprouts
        EOF
    )
    diff -u <(echo "$expected_output") <(echo "$output")
    [ $status -eq 0 ]
}

@test "past deadline, task becomes overdue" {
    WHATNEXT_TODAY=2025-12-06 \
        run --separate-stderr \
            whatnext \
                docs/deadlines.md

    expected_output=$(sed -e 's/^        //' <<"        EOF"
        docs/deadlines.md:
            # version 0.5 / OVERDUE 1d
            - [ ] complete and release

        docs/deadlines.md:
            # Christmas dinner / IMMINENT 2w 3d
            - [ ] book Christmas delivery

        docs/deadlines.md:
            # Christmas dinner
            - [ ] prep the make-ahead gravy
            - [ ] roast the potatoes
            - [ ] prep sprouts
        EOF
    )
    diff -u <(echo "$expected_output") <(echo "$output")
    [ $status -eq 0 ]
}

@test "filter by overdue priority" {
    WHATNEXT_TODAY=2025-12-06 \
        run --separate-stderr \
            whatnext \
                --priority overdue \
                docs/deadlines.md

    expected_output=$(sed -e 's/^        //' <<"        EOF"
        docs/deadlines.md:
            # version 0.5 / OVERDUE 1d
            - [ ] complete and release
        EOF
    )
    diff -u <(echo "$expected_output") <(echo "$output")
    [ $status -eq 0 ]
}

@test "filter by medium priority" {
    WHATNEXT_TODAY=2025-12-24 \
        run --separate-stderr \
            whatnext \
                --priority medium \
                docs/deadlines.md

    expected_output=$(sed -e 's/^        //' <<"        EOF"
        docs/deadlines.md:
            # Christmas dinner / MEDIUM
            - [ ] prep the make-ahead gravy
        EOF
    )
    diff -u <(echo "$expected_output") <(echo "$output")
    [ $status -eq 0 ]
}

@test "filter by imminent priority" {
    WHATNEXT_TODAY=2025-12-06 \
        run --separate-stderr \
            whatnext \
                --priority imminent \
                docs/deadlines.md

    expected_output=$(sed -e 's/^        //' <<"        EOF"
        docs/deadlines.md:
            # Christmas dinner / IMMINENT 2w 3d
            - [ ] book Christmas delivery
        EOF
    )
    diff -u <(echo "$expected_output") <(echo "$output")
    [ $status -eq 0 ]
}

@test "deadline date stripped from output" {
    WHATNEXT_TODAY=2025-01-01 \
        run --separate-stderr \
            whatnext \
                docs/deadlines.md

    [[ ! "$output" =~ @2025 ]]
    [ $status -eq 0 ]
}
