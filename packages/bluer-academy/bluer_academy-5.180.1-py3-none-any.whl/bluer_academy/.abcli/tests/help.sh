#! /usr/bin/env bash

function test_bluer_academy_help() {
    local options=$1

    local module
    for module in \
        "@academy" \
        \
        "@academy pypi" \
        "@academy pypi browse" \
        "@academy pypi build" \
        "@academy pypi install" \
        \
        "@academy pytest" \
        \
        "@academy test" \
        "@academy test list" \
        \
        "bluer_academy"; do
        bluer_ai_eval ,$options \
            bluer_ai_help $module
        [[ $? -ne 0 ]] && return 1

        bluer_ai_hr
    done

    return 0
}
