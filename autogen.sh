#! /bin/sh

set -e

# Make sure we are in the right directory
PROJECT_DIR="$(dirname "$(readlink -m "${BASH_SOURCE[0]}")")"

pushd "$PROJECT_DIR" >/dev/null
mkdir -p m4
autoreconf --install
popd >/dev/null

# vim:noexpandtab:shiftwidth=4:tabstop=4:softtabstop=4:
