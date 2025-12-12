#! /usr/bin/env bash

function test_bluer_academy_README() {
    local options=$1

    bluer_ai_eval ,$options \
        bluer_academy build_README
}
