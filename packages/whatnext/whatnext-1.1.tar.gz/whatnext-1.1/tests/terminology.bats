bats_require_minimum_version 1.5.0

@test "we call tasks 'tasks' not 'todos'" {
    # whatnext terminology is "tasks" not "todos", and I keep forgetting;
    # enforce the use of tasks, except where it is used legitimately
    run rg -c todo .
    output=$(echo "$output" | sort)

    expected_output=$(sed -e 's/^        //' <<"        EOF"
        ./README.md:1
        ./pyproject.toml:1
        ./tests/terminology.bats:3
        EOF
    )
    diff -u <(echo "$expected_output") <(echo "$output")
    [ $status -eq 0 ]
}
