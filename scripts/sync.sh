#!/usr/bin/env bash
# Copy the specification into an SDK, or check an SDK's copy.
#
#   scripts/sync.sh <sdk-dir>          copy the files into <sdk-dir>/spec/ and
#                                      write the tag of this checkout to
#                                      <sdk-dir>/spec/VERSION
#   scripts/sync.sh --check <sdk-dir>  fail if <sdk-dir>/spec/ is different
#                                      from this checkout
#
# Run it from a checkout of mina-sdk-spec at a release tag. In an SDK's CI,
# check out mina-sdk-spec at the tag in spec/VERSION and run --check.
set -euo pipefail

FILES=(SPEC.md ITN.md operations.graphql itn-operations.graphql)

check=false
if [[ "${1:-}" == "--check" ]]; then
  check=true
  shift
fi
if [[ $# -ne 1 ]]; then
  echo "usage: $0 [--check] <sdk-dir>" >&2
  exit 2
fi

root="$(cd "$(dirname "$0")/.." && pwd)"
dest="$1/spec"

if $check; then
  status=0
  for f in "${FILES[@]}"; do
    if ! cmp -s "$root/$f" "$dest/$f"; then
      echo "spec/$f is different from mina-sdk-spec" >&2
      status=1
    fi
  done
  if [[ ! -s "$dest/VERSION" ]]; then
    echo "spec/VERSION is missing" >&2
    status=1
  fi
  if [[ $status -ne 0 ]]; then
    echo "Run scripts/sync.sh from mina-sdk-spec at the tag in spec/VERSION." >&2
    exit 1
  fi
  echo "spec/ is mina-sdk-spec $(cat "$dest/VERSION")"
  exit 0
fi

tag="$(git -C "$root" describe --tags --exact-match 2>/dev/null)" || {
  echo "mina-sdk-spec is not at a release tag; check out a tag first" >&2
  exit 1
}
mkdir -p "$dest"
for f in "${FILES[@]}"; do
  cp "$root/$f" "$dest/$f"
done
echo "$tag" > "$dest/VERSION"
echo "spec/ is now mina-sdk-spec $tag"
