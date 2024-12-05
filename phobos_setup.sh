#!/bin/bash

ARCHIVE_PATH=$(mktemp -d)

function error()
{
    echo $*
    exit 1
}

phobos dir add "$ARCHIVE_PATH" ||
    error "Could not add $ARCHIVE_PATH"
phobos dir format --fs posix --unlock "$ARCHIVE_PATH" ||
    error "Could not format $ARCHIVE_PATH"
