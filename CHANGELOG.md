# Changelog

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
