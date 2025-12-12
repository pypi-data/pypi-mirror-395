from __future__ import annotations

import re
import string
from typing import overload

from django.db import IntegrityError, models
from django.db.models import Model

from rootcause import meta
from rootcause.base import UnexpectedErrorFormat, Unmatched
from rootcause.causes import BareCause, Cause


def resolve(cause: Cause) -> Cause:
    # If the fields are set, there's nothing we can offer here.
    if cause.fields:
        return cause
    if cause.kind == "unique":
        constraint = meta.find_constraint_by_name(cause.model, cause.name)
        if not constraint:
            virtual_constraints = meta.create_virtual_unique_constraints(
                model=cause.model, key_namer=default_key_name, max_length=64
            )
            for c in virtual_constraints:
                if c.name == cause.name:
                    constraint = c
                    break
    elif cause.kind == "check":
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
    name = None
    columns = []
    match e.args:
        # Error number: 1048; Symbol: ER_BAD_NULL_ERROR; SQLSTATE: 23000
        # Message: Column '%s' cannot be null
        case (1048, str(message)):
            kind = "not-null"
            groups = extract(message, "Column '{col}' cannot be null")
            columns = [groups["col"]]
        # Error number: 1452; Symbol: ER_NO_REFERENCED_ROW_2; SQLSTATE: 23000
        # Message: Cannot add or update a child row: a foreign key constraint fails (%s)
        case (1452, str(message)):
            kind = "foreign-key"
            groups = extract(
                message,
                r"(`{db}`.`{table}`, CONSTRAINT `{name}` FOREIGN KEY (`{col}`)",
            )
            name = groups["name"]
            columns = [groups["col"]]
        # Error number: 1062; Symbol: ER_DUP_ENTRY; SQLSTATE: 23000
        # Message: Duplicate entry '%s' for key %d
        case (1062, str(message)):
            kind = "unique"
            start = message.rfind("'", len("Duplicate entry '"), -2)
            key = message[start + 1 : -1]
            # Remove the table name for consistency with other databases.
            name = key.split(".")[-1]
        # Error number: 3819; Symbol: ER_CHECK_CONSTRAINT_VIOLATED; SQLSTATE: HY000
        # Message: Check constraint '%s' is violated.
        case (3819, str(message)):
            kind = "check"
            groups = extract(message, "Check constraint '{name}' is violated.")
            name = groups["name"]
        case _:
            raise Unmatched("Failed to match IntegrityError") from e
    bare = BareCause(kind=kind, name=name, columns=frozenset(columns))
    return bare if model is None else Cause.upgrade(bare, model)


def extract(value: str, pattern: str) -> dict[str, str]:
    pattern = re.escape(pattern)
    pattern = pattern.replace(r"\{", "{").replace(r"\}", "}")
    pattern = RegexShorthandFormatter().format(pattern)
    m = re.search(pattern, value)
    if m is None:
        raise UnexpectedErrorFormat(
            f"Message does not match expected formats: '{value}'"
        )
    return m.groupdict()


class RegexShorthandFormatter(string.Formatter):
    def get_value(self, key, args, kwargs) -> str:
        return f"(?P<{key}>[\\w\\-]+)"


def find_columns(possible_columns: list[str], model: type[Model]) -> list[str]:
    column_names = meta.fields_by_column(model)
    return [name for name in possible_columns if name in column_names]


def default_key_name(column_name: str, model: type[models.Model]) -> str:
    return column_name
