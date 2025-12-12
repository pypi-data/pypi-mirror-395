#! /usr/bin/env bash

function test_bluer_academy_version() {
    local options=$1

    bluer_ai_eval ,$options \
        "bluer_academy version ${@:2}"
}
