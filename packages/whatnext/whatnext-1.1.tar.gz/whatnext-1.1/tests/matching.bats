bats_require_minimum_version 1.5.0

@test "arg is task search" {
    run --separate-stderr \
        whatnext \
            dolor

    expected_output=$(sed -e 's/^        //' <<"        EOF"
        docs/basics.md:
            # Indicating the state of a task / Multiline tasks and indentation
            - [ ] Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do
                  eiusmod tempor incididunt ut labore et dolore magna aliqua.
        EOF
    )
    diff -u <(echo "$expected_output") <(echo "$output")
    [ $status -eq 0 ]

    # check it will find later parts of the name
    run --separate-stderr \
        whatnext \
            dolore
    diff -u <(echo "$expected_output") <(echo "$output")
    [ $status -eq 0 ]

    # case insensitive
    run --separate-stderr \
        whatnext \
            MAGNA
    diff -u <(echo "$expected_output") <(echo "$output")
    [ $status -eq 0 ]
}

@test "search term matches all under a heading" {
    run --separate-stderr \
        whatnext \
            dentat

    expected_output=$(sed -e 's/^        //' <<"        EOF"
        docs/basics.md:
            # Indicating the state of a task / Multiline tasks and indentation
            - [ ] Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do
                  eiusmod tempor incididunt ut labore et dolore magna aliqua.
            - [ ] Ut enim ad minim veniam,
        EOF
    )
    diff -u <(echo "$expected_output") <(echo "$output")
    [ $status -eq 0 ]

    # case insensitive
    run --separate-stderr \
        whatnext \
            MULTI
    diff -u <(echo "$expected_output") <(echo "$output")
    [ $status -eq 0 ]
}

@test "args is additive search" {
    run --separate-stderr \
        whatnext \
            dolor \
            open

    expected_output=$(sed -e 's/^        //' <<"        EOF"
        docs/basics.md:
            # Indicating the state of a task
            - [ ] open, this task is outstanding
            # Indicating the state of a task / Multiline tasks and indentation
            - [ ] Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do
                  eiusmod tempor incididunt ut labore et dolore magna aliqua.
        EOF
    )
    diff -u <(echo "$expected_output") <(echo "$output")
    [ $status -eq 0 ]

    # check it will find later parts of the name
    run --separate-stderr \
        whatnext \
            dolore \
            tstanding
    diff -u <(echo "$expected_output") <(echo "$output")
    [ $status -eq 0 ]

    # case insensitive
    run --separate-stderr \
        whatnext \
            MAGNA \
            OPEN
    diff -u <(echo "$expected_output") <(echo "$output")
    [ $status -eq 0 ]

    # order is immaterial
    run --separate-stderr \
        whatnext \
            open \
            dolor
    diff -u <(echo "$expected_output") <(echo "$output")
    [ $status -eq 0 ]
}

@test "args can mix tasks and headings" {
    run --separate-stderr \
        whatnext \
            dentat \
            open

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

    # case insensitive
    run --separate-stderr \
        whatnext \
            DENTAT \
            OPEN
    diff -u <(echo "$expected_output") <(echo "$output")
    [ $status -eq 0 ]

    # order is immaterial
    run --separate-stderr \
        whatnext \
            OPEN \
            DENTAT
    diff -u <(echo "$expected_output") <(echo "$output")
    [ $status -eq 0 ]
}

@test "arg matching dir restricts input" {
    WHATNEXT_TODAY=2025-01-01 \
        run --separate-stderr \
            whatnext \
                example

    expected_output=$(sed -e 's/^        //' <<"        EOF"
        projects/obelisk.md:
            # Project Obelisk / Discovery / OVERDUE 30y 2m
            Mess with Jackson
            - [<] watch archaeologists discover (needs time machine)

        projects/obelisk.md:
            # Project Obelisk
            Something something star gate
            - [/] carve runes into obelisk
            - [ ] research into runic meaning
            - [ ] bury obelisk in desert
        EOF
    )
    diff -u <(echo "$expected_output") <(echo "$output")
    [ $status -eq 0 ]

    # if you need disambiguation
    WHATNEXT_TODAY=2025-01-01 \
        run --separate-stderr \
            whatnext \
                ./example
    diff -u <(echo "$expected_output") <(echo "$output")
    [ $status -eq 0 ]
}

@test "args match multiple dirs" {
    WHATNEXT_TODAY=2025-01-01 \
        run --separate-stderr \
            whatnext \
                --config /dev/null \
                --all \
                example \
                archive

    expected_output=$(sed -e 's/^        //' <<"        EOF"
        example/projects/obelisk.md:
            # Project Obelisk / Discovery / OVERDUE 30y 2m
            Mess with Jackson
            - [<] watch archaeologists discover (needs time machine)

        example/tasks.md:
            # Get S Done / MEDIUM
            - [ ] question entire existence

        example/tasks.md:
            # Get S Done
            - [ ] come up with better projects
            - [ ] start third project
        example/projects/obelisk.md:
            # Project Obelisk
            Something something star gate
            - [/] carve runes into obelisk
            - [ ] research into runic meaning
            - [ ] bury obelisk in desert

        archive/done/tasks.md:
            # Some old stuff / FINISHED
            - [X] Do the first thing
            - [X] Do the second thing
            - [X] do the last thing all lowercase
        example/archived/projects/tangerine.md:
            # Project Tangerine / FINISHED
            - [X] acquire trebuchet plans
            - [X] source counterweight materials
            - [X] build it
            - [#] throw fruit at neighbours (they moved away)
        EOF
    )
    diff -u <(echo "$expected_output") <(echo "$output")
    [ $status -eq 0 ]
}

@test "dirs plus search" {
    run --separate-stderr \
        whatnext \
            --config /dev/null \
            example \
            runic

    expected_output=$(sed -e 's/^        //' <<"        EOF"
        projects/obelisk.md:
            # Project Obelisk
            Something something star gate
            - [ ] research into runic meaning
        EOF
    )
    diff -u <(echo "$expected_output") <(echo "$output")
    [ $status -eq 0 ]

    # if you need disambiguation
    run --separate-stderr \
        whatnext \
            --config /dev/null \
            ./example \
            runic
    diff -u <(echo "$expected_output") <(echo "$output")
    [ $status -eq 0 ]

    # order is immaterial
    run --separate-stderr \
        whatnext \
            --config /dev/null \
            runic \
            ./example
    diff -u <(echo "$expected_output") <(echo "$output")
    [ $status -eq 0 ]
}

@test "duplicate dirs do not duplicate output" {
    expected_output=$(sed -e 's/^        //' <<"        EOF"
        projects/obelisk.md:
            # Project Obelisk / Discovery / OVERDUE 30y 2m
            Mess with Jackson
            - [<] watch archaeologists discover (needs time machine)

        tasks.md:
            # Get S Done / MEDIUM
            - [ ] question entire existence

        tasks.md:
            # Get S Done
            - [ ] come up with better projects
            - [ ] start third project
        projects/obelisk.md:
            # Project Obelisk
            Something something star gate
            - [/] carve runes into obelisk
            - [ ] research into runic meaning
            - [ ] bury obelisk in desert
        EOF
    )

    WHATNEXT_TODAY=2025-01-01 \
        run --separate-stderr \
            whatnext \
                --config /dev/null \
                example
    diff -u <(echo "$expected_output") <(echo "$output")
    [ $status -eq 0 ]

    WHATNEXT_TODAY=2025-01-01 \
        run --separate-stderr \
            whatnext \
                --config /dev/null \
                example \
                example
    diff -u <(echo "$expected_output") <(echo "$output")
    [ $status -eq 0 ]

    WHATNEXT_TODAY=2025-01-01 \
        run --separate-stderr \
            whatnext \
                --config /dev/null \
                example \
                example/../example
    diff -u <(echo "$expected_output") <(echo "$output")
    [ $status -eq 0 ]
}

@test "arg matching file restricts input" {
    run --separate-stderr \
        whatnext \
            tests/headerless.md

    expected_output=$(sed -e 's/^        //' <<"        EOF"
        tests/headerless.md:
            - [ ] I am not a task, I am a free list!
        EOF
    )
    diff -u <(echo "$expected_output") <(echo "$output")
    [ $status -eq 0 ]
}

@test "multiple files" {
    run --separate-stderr \
        whatnext \
            tests/headerless.md \
            docs/usage.md

    expected_output=$(sed -e 's/^        //' <<"        EOF"
        docs/usage.md:
            # Usage
            - [/] carve runes into obelisk
            - [ ] come up with better projects
            - [ ] bury obelisk in desert
            - [ ] question entire existence
            - [ ] start third project
            - [ ] research into runic meaning
            - [<] watch archaeologists discover (needs time machine)
            # Usage / Matching
            - [ ] research into runic meaning
            - [ ] question entire existence
            - [ ] research into runic meaning
            # Usage / Limiting output
            - [ ] come up with better projects
            - [ ] bury obelisk in desert
            - [<] watch archaeologists discover (needs time machine)
            # Usage / Arguments
            - [/] carve runes into obelisk
            - [ ] come up with better projects
            - [ ] bury obelisk in desert
            - [ ] question entire existence
            - [ ] start third project
            - [ ] research into runic meaning
            - [<] watch archaeologists discover (needs time machine)
        tests/headerless.md:
            - [ ] I am not a task, I am a free list!
        EOF
    )
    diff -u <(echo "$expected_output") <(echo "$output")
    [ $status -eq 0 ]

    # order is irrelevant
    run --separate-stderr \
        whatnext \
            docs/usage.md \
            tests/headerless.md
    diff -u <(echo "$expected_output") <(echo "$output")
    [ $status -eq 0 ]
}

@test "duplicate files do not duplicate output" {
    expected_output=$(sed -e 's/^        //' <<"        EOF"
        tests/headerless.md:
            - [ ] I am not a task, I am a free list!
        EOF
    )

    run --separate-stderr \
        whatnext \
            tests/headerless.md
    diff -u <(echo "$expected_output") <(echo "$output")
    [ $status -eq 0 ]

    run --separate-stderr \
        whatnext \
            tests/headerless.md \
            tests/headerless.md
    diff -u <(echo "$expected_output") <(echo "$output")
    [ $status -eq 0 ]
}

@test "arg file path is respected in output" {
    run --separate-stderr \
        whatnext \
            docs/usage.md

    expected_output=$(sed -e 's/^        //' <<"        EOF"
        docs/usage.md:
            # Usage
            - [/] carve runes into obelisk
            - [ ] come up with better projects
            - [ ] bury obelisk in desert
            - [ ] question entire existence
            - [ ] start third project
            - [ ] research into runic meaning
            - [<] watch archaeologists discover (needs time machine)
            # Usage / Matching
            - [ ] research into runic meaning
            - [ ] question entire existence
            - [ ] research into runic meaning
            # Usage / Limiting output
            - [ ] come up with better projects
            - [ ] bury obelisk in desert
            - [<] watch archaeologists discover (needs time machine)
            # Usage / Arguments
            - [/] carve runes into obelisk
            - [ ] come up with better projects
            - [ ] bury obelisk in desert
            - [ ] question entire existence
            - [ ] start third project
            - [ ] research into runic meaning
            - [<] watch archaeologists discover (needs time machine)
        EOF
    )
    diff -u <(echo "$expected_output") <(echo "$output")
    [ $status -eq 0 ]
}

@test "files plus search" {
    run --separate-stderr \
        whatnext \
            docs/usage.md \
            obelisk

    expected_output=$(sed -e 's/^        //' <<"        EOF"
        docs/usage.md:
            # Usage
            - [/] carve runes into obelisk
            - [ ] bury obelisk in desert
            # Usage / Limiting output
            - [ ] bury obelisk in desert
            # Usage / Arguments
            - [/] carve runes into obelisk
            - [ ] bury obelisk in desert
        EOF
    )
    diff -u <(echo "$expected_output") <(echo "$output")
    [ $status -eq 0 ]
}

@test "matchers override default search space" {
    run --separate-stderr \
        whatnext \
            --dir . \
            archive
    [ "$output" = "" ]
    [ $status -eq 0 ]
}

@test "no results is not an error" {
    run --separate-stderr \
        whatnext \
            smurf
    diff -u <(echo "") <(echo "$output")
    [ $status -eq 0 ]

    run --separate-stderr \
        whatnext \
            docs \
            smurf
    diff -u <(echo "") <(echo "$output")
    [ $status -eq 0 ]

    run --separate-stderr \
        whatnext \
            smurf \
            docs
    diff -u <(echo "") <(echo "$output")
    [ $status -eq 0 ]
}

@test "explicit file overrides ignore" {
    # tasks.md is ignored
    grep -q "tasks.md" .whatnext

    run --separate-stderr \
        whatnext \
            -all
    [ -z "$(echo "$output" | grep tasks.md)" ]

    # but you can still query it directly
    run --separate-stderr \
        whatnext \
            --all \
            tasks.md
    [ -n "$(echo "$output" | grep tasks.md)" ]
    [ $status -eq 0 ]
}
