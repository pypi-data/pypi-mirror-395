from __future__ import annotations

from collections.abc import Callable, Iterable
from pyexpat import model

from django.db import models
from django.db.backends.utils import names_digest, split_identifier
from django.db.models import ForeignObjectRel


def fields_by_column(model: type[models.Model]) -> dict[str, models.Field]:
    fields: dict[str, models.Field] = {}
    for field in model._meta.get_fields():
        if isinstance(field, ForeignObjectRel):
            continue
        _, column = field.get_attname_column()
        fields[column] = field
    return fields


def columns_by_field_name(
    model: type[models.Model], field_names: list[str]
) -> dict[str, str]:
    columns = {}
    for field_name in field_names:
        field = model._meta.get_field(field_name)
        if isinstance(field, ForeignObjectRel):
            continue
        name, column = field.get_attname_column()
        columns[name] = column
    return columns


def get_field_column(field: models.Field | models.ForeignObjectRel) -> str:
    if isinstance(field, models.ForeignObjectRel):
        return field.field.column
    return field.column


def find_constraint_by_name(
    model: type[models.Model], name: str
) -> models.BaseConstraint | None:
    for c in model._meta.constraints:
        if name == getattr(c, "name", None):
            return c
    return None


def find_constraints_by_field_names(
    model: type[models.Model], field_names: Iterable[str]
) -> list[models.BaseConstraint]:
    constraints = model._meta.constraints
    field_name_lookup = tuple(sorted(field_names))
    ret = []
    for constraint in constraints:
        fns = field_names_from_constraint(constraint)
        if field_name_lookup == tuple(sorted(fns)):
            ret.append(constraint)
    return ret


def create_virtual_unique_constraints(
    model: type[models.Model],
    key_namer: Callable[[str, model.Model], str],
    max_length: int | None = None,
) -> list[models.UniqueConstraint]:
    ret = []
    for field in model._meta.get_fields():
        if isinstance(field, ForeignObjectRel):
            continue
        unique = field.unique
        if unique:
            column = get_field_column(field)
            ret.append(
                models.UniqueConstraint(
                    fields=[field.name], name=key_namer(column, model)
                )
            )
    for field_names in model._meta.unique_together:
        columns = []
        for fn in field_names:
            field = model._meta.get_field(fn)
            _, col = field.get_attname_column()
            columns.append(col)
        name = generate_unique_constraint_name(
            model._meta.db_table,
            *columns,
            max_length=max_length,
        )
        ret.append(models.UniqueConstraint(fields=field_names, name=name))
    return ret


# Taken from Django.
def generate_unique_constraint_name(
    table_name: str, *column_names: str, max_length: int | None = None
) -> str:
    _, table_name = split_identifier(table_name)
    hash_suffix_part = f"{names_digest(table_name, *column_names, length=8)}_uniq"
    max_length = 200 if max_length is None else max_length
    # If everything fits into max_length, use that name.
    index_name = _create_index_name(
        table_name, "_".join(column_names), hash_suffix_part
    )
    if len(index_name) <= max_length:
        return index_name
    # Shorten a long suffix.
    if len(hash_suffix_part) > max_length / 3:
        hash_suffix_part = hash_suffix_part[: max_length // 3]
    other_length = (max_length - len(hash_suffix_part)) // 2 - 1
    index_name = _create_index_name(
        table_name[:other_length],
        "_".join(column_names)[:other_length],
        hash_suffix_part,
    )
    # Prepend D if needed to prevent the name from starting with an
    # underscore or a number (not permitted on Oracle).
    if index_name[0] == "_" or index_name[0].isdigit():
        index_name = f"D{index_name[:-1]}"
    return index_name


def _create_index_name(table_name: str, column_names: str, suffix: str) -> str:
    return f"{table_name}_{column_names}_{suffix}"


def field_names_from_constraint(constraint: models.BaseConstraint) -> list[str]:
    if isinstance(constraint, models.CheckConstraint):
        return field_names_from_expression(constraint.condition)
    if isinstance(constraint, models.UniqueConstraint):
        if constraint.fields:
            names = list(constraint.fields)
        else:
            names = []
            for e in constraint.expressions:
                names += field_names_from_expression(e)
        return names
    raise ValueError(
        f"Unable to handle constraints of type {type(constraint)} ({constraint=})"
    )


def field_names_from_expression(expression: models.Expression | models.Q) -> list[str]:
    if isinstance(expression, models.F):
        return [expression.name]
    if isinstance(expression, models.Q):
        ret = []
        for child in expression.children:
            if isinstance(child, tuple):
                ret.append(child[0].split("__")[0])
            else:
                ret += field_names_from_expression(child)
        return ret
    if not hasattr(expression, "get_source_expressions"):
        return []
    ret = []
    for e in expression.get_source_expressions():
        ret += field_names_from_expression(e)
    return ret
