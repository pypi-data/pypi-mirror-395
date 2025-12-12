from __future__ import annotations

from typing import overload

from django.db import IntegrityError
from django.db.models import Model

from rootcause import meta
from rootcause.base import Unmatched
from rootcause.causes import BareCause, Cause


def resolve(cause: Cause) -> Cause:
    # If the fields and name are set, there's nothing we can offer here.
    # If neither of those are, we can't do anything either.
    if bool(cause.fields) and bool(cause.name):
        return cause
    if cause.kind == "unique":
        if cause.name:
            constraint = meta.find_constraint_by_name(cause.model, cause.name)
        else:
            constraints = meta.find_constraints_by_field_names(
                cause.model, cause.field_names
            )
            if len(constraints) == 1:
                constraint = constraints[0]
            else:
                # We're not going to guess when there are
                # multiple matching constraints. And there's
                # nothing to guess when there is no match.
                constraint = None
    elif cause.kind == "check":
        constraint = meta.find_constraint_by_name(cause.model, cause.name)
    else:
        constraint = None
    if not constraint:
        return cause
    field_names = meta.field_names_from_constraint(constraint)
    columns = meta.columns_by_field_name(cause.model, field_names)
    bare = BareCause(
        kind=cause.kind,
        name=constraint.name,
        columns=frozenset(columns.values()),
    )
    return Cause.upgrade(bare, model=cause.model)


@overload
def parse(e: IntegrityError, model: None = None) -> BareCause: ...


@overload
def parse(e: IntegrityError, model: type[Model]) -> Cause: ...


def parse(e: IntegrityError, model: type[Model] | None = None) -> Cause | BareCause:
    if not isinstance(e.args, tuple) or not e.args:
        raise Unmatched("Could not find meaning in IntegrityError") from e
    message = e.args[0]
    # Example: "UNIQUE constraint failed: index 'index_name'"
    if rest := prefix_match(message, "UNIQUE constraint failed: index "):
        # Strip quotes
        name = rest.strip("'")
        kind = "unique"
        columns = frozenset()
    # Example: "UNIQUE constraint failed: table.col1, table.col2"
    elif rest := prefix_match(message, "UNIQUE constraint failed: "):
        name = None
        kind = "unique"
        columns = parse_columns(rest)
    # Example: "CHECK constraint failed: value_gt_2"
    elif rest := prefix_match(message, "CHECK constraint failed: "):
        name = rest
        kind = "check"
        columns = frozenset()
    # Example: "NOT NULL constraint failed: sample_notnull.name"
    elif rest := prefix_match(message, "NOT NULL constraint failed: "):
        kind = "not-null"
        name = None
        columns = parse_columns(rest)
    # Example: "FOREIGN KEY constraint failed"
    elif message.startswith("FOREIGN KEY constraint failed"):
        kind = "foreign-key"
        name = None
        columns = frozenset()
    else:
        raise Unmatched(f"Message not matched: '{message}'")
    bare = BareCause(kind=kind, name=name, columns=columns)
    return bare if model is None else Cause.upgrade(bare, model)


def prefix_match(message: str, prefix: str) -> str | None:
    rest = message.removeprefix(prefix)
    return None if rest == message else rest.strip()


def parse_columns(mention: str) -> frozenset[str]:
    names = mention.split(", ")
    columns = []
    for name in names:
        columns.append(name.split(".")[-1])
    return frozenset(columns)


def default_key_name(column: str, model: type[Model]) -> str:
    # Sqlite doesn't use default keys...?
    return f"_______{column}"
