from __future__ import annotations

from typing import overload

from django.db import IntegrityError
from django.db.models import Model

from rootcause import meta
from rootcause.base import Unmatched
from rootcause.causes import BareCause, Cause


def resolve(cause: Cause) -> Cause:
    # Nothing left to do here.
    if cause.fields:
        return cause
    # There's two cases where Postgres doesn't include
    # (usable) column information:
    # - Unique constraints with expressions
    # - Check constraints
    if cause.kind in ("unique", "check"):
        constraint = meta.find_constraint_by_name(cause.model, cause.name)
    else:
        constraint = None
    if not constraint:
        return cause
    field_names = meta.field_names_from_constraint(constraint)
    columns = meta.columns_by_field_name(cause.model, field_names)
    bare = BareCause(
        kind=cause.kind, name=cause.name, columns=frozenset(columns.values())
    )
    return Cause.upgrade(bare, model=cause.model)


@overload
def parse(e: IntegrityError, model: None = None) -> BareCause: ...


@overload
def parse(e: IntegrityError, model: type[Model]) -> Cause: ...


def parse(e: IntegrityError, model: type[Model] | None = None) -> Cause | BareCause:
    cause = getattr(e, "__cause__", None) or getattr(e, "__context__", None)
    diag = getattr(cause, "diag", None)
    if not cause or not diag or not getattr(diag, "constraint_name", None):
        message = e.args[0]
        # Example:
        # "null value in column "name" of relation "sample_notnull"
        # violates not-null constraint"
        if "violates not-null constraint" in message:
            bare = parse_not_null(message)
            return bare if model is None else Cause.upgrade(bare, model)
        raise Unmatched("Could not find meaning in IntegrityError") from e
    message = cause.args[0]
    if "violates unique constraint" in message:
        kind = "unique"
        includes_columns = True
    elif "violates check constraint" in message:
        kind = "check"
        includes_columns = False
    elif "violates foreign key constraint" in message:
        kind = "foreign-key"
        includes_columns = True
    else:
        raise Unmatched(f"Unsure what to do with '{message}'")
    name = diag.constraint_name
    if includes_columns:
        columns = parse_columns(diag.message_detail)
    else:
        columns = frozenset()
    bare = BareCause(kind=kind, name=name, columns=columns)
    return bare if model is None else Cause.upgrade(bare, model)


def parse_not_null(message: str) -> BareCause:
    marker = " in column "
    start = message.find(marker) + len(marker) + 1
    end = message.find('"', start)
    column = message[start:end]
    return BareCause(kind="not-null", name=None, columns=frozenset({column}))


def parse_columns(detail: str) -> frozenset[str]:
    detail = detail.strip().removeprefix("Key (")
    detail = detail[0 : detail.find(")")]
    if "(" in detail:
        # The detail will probably look at bit like this:
        # "Key (lower(name::text))=(sam) already exists.""
        # And we're not going to parse expressions.
        return frozenset()
    return frozenset(detail.split(", "))
