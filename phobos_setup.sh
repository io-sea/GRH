#!/bin/bash

ARCHIVE_PATH=$(mktemp -d)
PHOBOSD_LOG=/tmp/phobosd.log
PHOBOSD_LOCK=/tmp/phobosd.lock
PHOBOSD_SOCKET=/tmp/lrs

function error()
{
    echo $*
    exit 1
}

sudo -u postgres phobos_db setup_db -p phobos
phobos_db setup_tables

export PHOBOS_LRS_lock_file="$PHOBOSD_LOCK"
export PHOBOS_LRS_server_socket="$PHOBOSD_SOCKET"
rm -f "$PHOBOSD_LOCK"

echo "Starting phobosd, log file: $PHOBOSD_LOG"
phobosd &> "$PHOBOSD_LOG" ||
    error "Failed to start phobosd"
PHOBOSD_PID=$(pgrep phobosd)

phobos dir add "$ARCHIVE_PATH" ||
    error "Could not add $ARCHIVE_PATH"
phobos dir format --fs posix --unlock "$ARCHIVE_PATH" ||
    error "Could not format $ARCHIVE_PATH"
