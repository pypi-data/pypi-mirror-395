#!/bin/bash
#
# generate or validate patch files between upstream files and our local overrides
# this is useful for detecting when upstream files get changed and potentially cause drift from our overrides
#
# this has the assumption that our local override files contain a marker like "base: <file/import path> [version]"

set -euo pipefail

errors=0
mode=0
patch_dir="tests/patches"
while getopts "d:" opt; do
    case "$opt" in
    d)
        patch_dir="${OPTARG}";;
    ?)
        echo >&2 "usage: $0 [-d patch_dir] [generate|validate]"; exit 1;;
    esac
done
shift $(( OPTIND - 1 ))

case "${1:-}" in
    validate) mode=0;;
    generate) mode=1;;
    *) echo >&2 "unknown command, using 'validate'";;
esac

if [[ ! -d "${patch_dir}" ]]; then
    echo "error: directory '${patch_dir}' does not exist"
    exit 1
fi

for line in $(python3 ./tests/list_overrides.py); do
    IFS=: read -r override base <<< "${line}"

    rel_override="$(realpath --relative-to=. "${override}")"
    rel_base="$(realpath --relative-to=. "${base}")"
    rel_patch="${patch_dir%/}/$(basename "${rel_override}").patch"

    if [[ -z "${base}" ]]; then
        echo >&2 "error: could not find base file for '${rel_override}'!"
        errors=$(( errors + 1 ))
    fi

    if [[ "${mode}" -eq 0 ]]; then
        # validate the patch-diffs
        temp_file="$(mktemp)"
        echo "validating patch for '${rel_override}'..."
        if [[ ! -f "${rel_patch}" ]]; then
            echo >&2 "error: patch file for '${rel_override}' not found!"
            errors=$(( errors + 1 ))

        elif ! patch --silent --output="${temp_file}" "${rel_override}" "${rel_patch}"; then
            echo >&2 "error: patch for '${rel_override}' could not be applied successfully!"
            errors=$(( errors + 1 ))

        elif ! diff --ignore-all-space --ignore-blank-lines "${temp_file}" "${rel_base}"; then
            echo >&2 "error: patch result '${rel_override}' differs from '${rel_base}'!"
            errors=$(( errors + 1 ))
        fi
        rm -f "${temp_file}"
    else
        # generate a patch-diff (with relative paths in the header) into "${output_dir}"
        # also, diff is somewhat expected to return a nonzero exit code:
        # https://askubuntu.com/questions/698784/exit-code-of-diff
        echo "generating patch for '${rel_override}'..."
        diff --unified --minimal --ignore-all-space --ignore-blank-lines "${rel_override}" "${rel_base}" > "${rel_patch}" || true
    fi
done

exit ${errors}
