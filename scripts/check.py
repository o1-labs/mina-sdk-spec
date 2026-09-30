#!/usr/bin/env python3
"""Validate the specification's GraphQL documents.

Offline (the default):
    every operation of operations.graphql is valid against
    schema/daemon.graphql, and every operation of itn-operations.graphql
    against schema/itn.graphql. Each operation has a unique name.

Live (--endpoint URL):
    the daemon's schema is read with a full introspection query, the
    operations of operations.graphql are validated against it, and it is
    compared with schema/daemon.graphql. An invalid operation fails the run.
    A schema difference fails the run only with --strict. --write-schema
    replaces schema/daemon.graphql with the live schema.

Needs graphql-core (pip install graphql-core).
"""

import argparse
import json
import sys
import urllib.request
from pathlib import Path

from graphql import (
    OperationDefinitionNode,
    build_client_schema,
    build_schema,
    get_introspection_query,
    parse,
    print_schema,
    validate,
)

ROOT = Path(__file__).resolve().parent.parent

# (operations file, schema snapshot)
DOCUMENTS = [
    ("operations.graphql", "schema/daemon.graphql"),
    ("itn-operations.graphql", "schema/itn.graphql"),
]


def check_document(ops_path, schema):
    """Return the problems of one operations file against a schema."""
    problems = []
    doc = parse((ROOT / ops_path).read_text())
    names = set()
    for d in doc.definitions:
        if not isinstance(d, OperationDefinitionNode):
            problems.append(f"{ops_path}: only operations are allowed, found {d.kind}")
            continue
        if d.name is None:
            problems.append(f"{ops_path}: an operation has no name")
            continue
        if d.name.value in names:
            problems.append(f"{ops_path}: operation {d.name.value} twice")
        names.add(d.name.value)
    for error in validate(schema, doc):
        problems.append(f"{ops_path}: {error.message}")
    return problems, len(names)


def offline():
    problems = []
    for ops_path, schema_path in DOCUMENTS:
        # The daemon's schemas are not strictly valid (the ITN server has an
        # empty subscription type); only the operations are validated.
        schema = build_schema((ROOT / schema_path).read_text(), assume_valid=True)
        found, count = check_document(ops_path, schema)
        problems += found
        print(f"{ops_path}: {count} operations against {schema_path}")
    return problems


def live(endpoint, strict, write_schema):
    body = json.dumps({"query": get_introspection_query(descriptions=True)}).encode()
    request = urllib.request.Request(
        endpoint, data=body, headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        result = json.load(response)
    if "data" not in result:
        sys.exit(f"introspection failed: {result.get('errors')}")
    schema = build_client_schema(result["data"], assume_valid=True)

    problems, count = check_document("operations.graphql", schema)
    print(f"operations.graphql: {count} operations against {endpoint}")

    snapshot = ROOT / "schema/daemon.graphql"
    live_sdl = print_schema(schema) + "\n"
    if live_sdl != snapshot.read_text():
        if write_schema:
            snapshot.write_text(live_sdl)
            print("schema/daemon.graphql: replaced with the live schema")
        else:
            message = "the live schema is different from schema/daemon.graphql"
            if strict:
                problems.append(message)
            else:
                print(f"warning: {message}")
    else:
        print("schema/daemon.graphql: same as the live schema")
    return problems


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--endpoint", help="GraphQL URL of a live daemon")
    parser.add_argument("--strict", action="store_true",
                        help="with --endpoint: fail on a schema difference")
    parser.add_argument("--write-schema", action="store_true",
                        help="with --endpoint: replace schema/daemon.graphql")
    args = parser.parse_args()

    if args.endpoint:
        problems = live(args.endpoint, args.strict, args.write_schema)
    else:
        problems = offline()
    for p in problems:
        print(f"error: {p}")
    if problems:
        sys.exit(1)
    print("OK")


if __name__ == "__main__":
    main()
