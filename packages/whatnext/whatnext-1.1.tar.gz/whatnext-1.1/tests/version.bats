bats_require_minimum_version 1.5.0

@test "version" {
    run whatnext --version

    [[ "$output" =~ ^whatnext\ version\ v[0-9]+\.[0-9]+[^$'\n']*$ ]]
    [ ${#lines[@]} -eq 1 ]
    [ $status -eq 0 ]
}
