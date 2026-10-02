# Mina SDK specification

The API that the Mina SDKs have in common, independent of language:

| File | Contents |
|:--|:--|
| [`SPEC.md`](SPEC.md) | Methods, rules and result types of the daemon client (GraphQL port 3085) |
| [`operations.graphql`](operations.graphql) | The 22 GraphQL documents of the daemon client |
| [`ITN.md`](ITN.md) | Methods and authentication protocol of the ITN client (`--itn-graphql-port`) |
| [`itn-operations.graphql`](itn-operations.graphql) | The 10 GraphQL documents of the ITN client |
| [`schema/daemon.graphql`](schema/daemon.graphql) | The daemon's public schema, as SDL |
| [`schema/itn.graphql`](schema/itn.graphql) | The daemon's ITN schema, as SDL |

SDKs that follow this specification:
[mina-sdk-rust](https://github.com/o1-labs/mina-sdk-rust),
[mina-sdk-go](https://github.com/o1-labs/mina-sdk-go),
[mina-sdk-js](https://github.com/o1-labs/mina-sdk-js),
[mina-sdk-python](https://github.com/o1-labs/mina-sdk-python) (the daemon
client; not yet the ITN client).

## How an SDK uses it

Each SDK has a copy of `SPEC.md`, `ITN.md`, `operations.graphql` and
`itn-operations.graphql` in its `spec/` directory, and the release tag of
the copy in `spec/VERSION`:

- A test in the SDK checks that its query strings are the documents of the
  copy, up to white space.
- A CI job in the SDK checks out this repository at the tag in
  `spec/VERSION` and runs `scripts/sync.sh --check .`. It fails if the copy
  is different from the tag.

The copy keeps each SDK self-contained: a normal clone builds and tests, and
the packages on crates.io, the Go module proxy, npm and PyPI are not
affected.

To update an SDK to a new release:

```bash
git -C mina-sdk-spec checkout v0.2.0
mina-sdk-spec/scripts/sync.sh path/to/mina-sdk-go
# then change the SDK so that its conformance test passes
```

A CI job for an SDK:

```yaml
spec:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - id: spec
      run: echo "version=$(cat spec/VERSION)" >> "$GITHUB_OUTPUT"
    - uses: actions/checkout@v4
      with:
        repository: o1-labs/mina-sdk-spec
        ref: ${{ steps.spec.outputs.version }}
        path: .mina-sdk-spec
    - run: .mina-sdk-spec/scripts/sync.sh --check .
```

## Checks in this repository

`scripts/check.py` needs `graphql-core` (`pip install graphql-core`).

- `python scripts/check.py` validates every operation against the schema
  snapshots: fields, arguments, variable types and unique operation names.
  CI runs it on each push and pull request.
- `python scripts/check.py --endpoint http://127.0.0.1:3085/graphql` validates
  `operations.graphql` against a live daemon and compares the live schema
  with `schema/daemon.graphql`. `--strict` also fails on a schema difference,
  and `--write-schema` replaces the snapshot. The drift workflow runs it
  every week against the lightnet images of `master`, `compatible` and
  `develop`.

The ITN server needs signed requests, so the ITN schema is not read live in
CI. To refresh `schema/itn.graphql`, send a full introspection query with an
SDK's ITN client (custom-query method) and print the result as SDL.

The snapshots were read from daemon `4.0.0-6965b50` (devnet build).

## Changing the specification

1. Change the documents and the Markdown files. Keep existing field names:
   the result types are the union of what the SDKs returned.
2. Run `python scripts/check.py`.
3. Merge, add a line to [`CHANGELOG.md`](CHANGELOG.md), and tag a release.
4. Update each SDK with `scripts/sync.sh`.

## License

[Apache License 2.0](LICENSE)
