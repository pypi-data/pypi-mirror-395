bats_require_minimum_version 1.5.0

@test "default config is in the dir root" {
    WHATNEXT_DIR=example \
    WHATNEXT_TODAY=2025-01-01 \
        run --separate-stderr \
            whatnext

    diff -u <(echo "") <(echo "$output")
    [ $status -eq 0 ]
}


@test "config arg is also relative to the dir root" {
    WHATNEXT_DIR=example \
    WHATNEXT_TODAY=2025-01-01 \
        run --separate-stderr \
            whatnext \
                --config .whatnext.all \
                --all

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

        archived/projects/tangerine.md:
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

@test "config arg from environment" {
    WHATNEXT_CONFIG=.whatnext.all \
    WHATNEXT_DIR=example \
    WHATNEXT_TODAY=2025-01-01 \
        run --separate-stderr \
            whatnext \
                --all

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

        archived/projects/tangerine.md:
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

@test "absolute config is relative to running dir" {
    WHATNEXT_DIR=example \
    WHATNEXT_TODAY=2025-01-01 \
        run --separate-stderr \
            whatnext \
                --config ./tests/dot-whatnext

    expected_output=$(sed -e 's/^        //' <<"        EOF"
        tasks.md:
            # Get S Done / MEDIUM
            - [ ] question entire existence

        tasks.md:
            # Get S Done
            - [ ] come up with better projects
            - [ ] start third project
        EOF
    )
    diff -u <(echo "$expected_output") <(echo "$output")
    [ $status -eq 0 ]

    WHATNEXT_CONFIG=./tests/dot-whatnext \
    WHATNEXT_DIR=example \
    WHATNEXT_TODAY=2025-01-01 \
        run --separate-stderr \
            whatnext
    diff -u <(echo "$expected_output") <(echo "$output")
    [ $status -eq 0 ]
}
