# Changelog

## [0.2.0] - unreleased

### Added
- Five ITN operations for harnesses, which need a daemon with
  MinaProtocol/mina#19616: `CommitId`, `ScheduledTransactions`,
  `SchedulePaymentsWithHandle`, `ScheduleZkappCommandsWithHandle` and
  `CreateAccounts`. `ITN.md` describes them.

### Changed
- `schema/itn.graphql` is read from a daemon with MinaProtocol/mina#19616.

The existing operations do not change.

## [0.1.2] - 2026-10-02

### Changed
- `ITN.md` has the Python ITN names (`mina_sdk.itn`, extra `mina-sdk[itn]`):
  all four SDKs implement the ITN client.

The operations are the same as in 0.1.0.

## [0.1.1] - 2026-10-01

### Changed
- `SPEC.md` and `ITN.md` have a Python column; `SPEC.md` names Python's
  custom-query method (`execute_query`) and its `from_` field. The Python SDK
  has no ITN client yet.
- `ITN.md` links to `schema/itn.graphql` with an absolute URL, so that the
  link works in the SDKs' copies, which do not include `schema/`.

The operations are the same as in 0.1.0.

## [0.1.0] - 2026-09-30

### Added
- The daemon client API: `SPEC.md` and `operations.graphql` (22 operations),
  moved from mina-sdk-rust.
- The ITN client API: `ITN.md` and `itn-operations.graphql` (10 operations).
  The operations have the documents that the SDKs already sent, now with
  operation names.
- Schema snapshots as SDL, from a full introspection of daemon
  `4.0.0-6965b50`: `schema/daemon.graphql` and `schema/itn.graphql`.
- `scripts/check.py` (validation against the snapshots or a live daemon) and
  `scripts/sync.sh` (copy into an SDK, or check an SDK's copy).
