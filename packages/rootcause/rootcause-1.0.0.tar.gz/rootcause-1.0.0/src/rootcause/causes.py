from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from functools import cached_property
from typing import Literal

from django import forms
from django.core.exceptions import ValidationError
from django.db import models

from rootcause import meta
from rootcause.base import PossibleModelMismatch

# The different kinds of constraint errors rootcause tries to support.
Kind = Literal["check", "unique", "not-null", "foreign-key"]


@dataclass(frozen=True, slots=True)
class BareCause:
    """
    Cause of an integrity error with nothing Model-specific.

    This will include the involved column names when available.
    Note: column names, not model field names.
    """

    kind: Kind
    # Name of the constraint. Might not be available.
    name: str | None
    # The columns involved in the constraint. Might not be set.
    columns: frozenset[str]

    def matches(
        self, *columns: str, name: str | None = None, kind: Kind | None = None
    ) -> bool:
        """
        Match the criteria to this cause.

        The more specific checks are probably what you want,
        so have a look at is_foreign_key, is_not_null,...

        For example:

            # Being very precise
            cause.matches("name", "value", name="uq_name_value", kind="unique")
            # Less precise
            cause.matches("name", "value", kind="unique")
            # But this will *not* match if "value" is involved
            cause.matches("name", kind="unique")

        - columns: if supplied must be all the involved columns
        - name: name of the constraint
        - kind: kind of constraint
        """
        assert name or columns or kind, (
            "At least one of name, kind or *columns is required"
        )
        return (
            (not name or self.is_constraint(name))
            and (not columns or self.on_columns(*columns))
            and (not kind or kind == self.kind)
        )

    def is_foreign_key(self, *columns: str, name: str | None = None) -> bool:
        return self.matches(*columns, kind="foreign-key", name=name)

    def is_not_null(self, *columns: str, name: str | None = None) -> bool:
        return self.matches(*columns, kind="not-null", name=name)

    def is_check(self, *columns: str, name: str | None = None) -> bool:
        return self.matches(*columns, kind="check", name=name)

    def is_unique(self, *columns: str, name: str | None = None) -> bool:
        return self.matches(*columns, kind="unique", name=name)

    def is_constraint(self, name: str) -> bool:
        return self.name == name

    def on_columns(self, *columns: str) -> bool:
        return bool(self.columns) and self.columns == set(columns)


@dataclass(frozen=True)
class Cause:
    """
    Cause of an IntegrityError enriched with Django data.

    Wraps the BareCause and encodes the fields that are involved,
    rather than the table columns. Same caveats apply as with
    BareCause: not all information is guaranteed to be included.
    """

    bare: BareCause
    fields: frozenset[models.Field]
    model: type[models.Model]

    @classmethod
    def upgrade(cls, bare: BareCause, model: type[models.Model]) -> Cause:
        if bare.columns:
            model_fields = meta.fields_by_column(model)
            fields = []
            for col in bare.columns:
                try:
                    fields.append(model_fields[col])
                except KeyError:
                    raise PossibleModelMismatch(
                        f"No field found for column {col} on {model.__name__}"
                    )
        else:
            fields = []
        return Cause(bare=bare, fields=frozenset(fields), model=model)

    @property
    def kind(self) -> Kind:
        return self.bare.kind

    @property
    def name(self) -> str | None:
        return self.bare.name

    @property
    def columns(self) -> frozenset[str]:
        return self.bare.columns

    @cached_property
    def field_names(self) -> frozenset[str]:
        return frozenset(field.name for field in self.fields)

    def is_foreign_key(self, *fields: str, name: str | None = None) -> bool:
        return self.matches(*fields, kind="foreign-key", name=name)

    def is_check(self, *fields: str, name: str | None = None) -> bool:
        return self.matches(*fields, kind="check", name=name)

    def is_unique(self, *fields: str, name: str | None = None) -> bool:
        return self.matches(*fields, kind="unique", name=name)

    def is_not_null(self, *fields: str, name: str | None = None) -> bool:
        return self.matches(*fields, kind="not-null", name=name)

    def matches(
        self,
        *fields: str,
        columns: Iterable[str] | None = None,
        name: str | None = None,
        kind: Kind | None = None,
    ) -> bool:
        """
        Check whether the cause matches the parameters.

        If fields or columns are passed, the check will
        require that all fields or columns are matched.
        Meaning "name" will not be matched if the constraint
        covers columns/fields "name" and "alias".
        """
        assert fields or columns or name or kind, (
            "At least one of fields, columns, name or kind is required."
        )
        if kind and self.kind != kind:
            return False
        if name and not self.is_constraint(name):
            return False
        if columns and not self.on_columns(*columns):
            return False
        if fields:
            return self.on_fields(*fields)
        return True

    def is_constraint(self, name: str) -> bool:
        """Check if the cause is a constraint with the name."""
        app_label = self.model._meta.app_label.lower()
        cls = self.model.__name__.lower()
        return self.bare.is_constraint(name % {"app_label": app_label, "class": cls})

    def on_columns(self, *columns: str) -> bool:
        """Check if the cause is a constraint with the given columns."""
        return self.bare.on_columns(*columns)

    def on_fields(self, *names: str) -> bool:
        """Check if the cause is a constraint with the given fields."""
        return self.field_names == set(names)

    def validation_error(self) -> ValidationError:
        """
        Always build a ValidationError.

        In case maybe_build_validation_error doesn't have
        enough information to build a ValidationError that
        matches the one Django would construct during validation,
        this will create one. Its code is set to
        "ROOTCAUSE:FORCE_NAMED".
        """
        error = self.maybe_validation_error()
        if error:
            return error
        name = self.name if self.name else self.kind
        msg = self._default_error_message() % {"name": name}
        return ValidationError(msg, code="ROOTCAUSE:FORCE_NAMED")

    def maybe_validation_error(self) -> ValidationError | None:
        """
        Try to build a ValidationError.

        This should result in the same ValidationError as would be
        raised by Django during model validation.

        And it might not. Therefor: ValidationError | None.
        """
        if self.name:
            c = meta.find_constraint_by_name(self.model, self.name)
            if c:
                if (
                    isinstance(c, models.UniqueConstraint)
                    and self.fields
                    and c.violation_error_message == c.default_violation_error_message
                ):
                    # Django has backwards compatibility for unique_error_message
                    # on UniqueConstraint.
                    return self._get_unique_error_message()
                code = getattr(c, "violation_error_code", None)
                msg = getattr(c, "get_violation_error_message", None)
                if not msg:
                    msg = self._default_error_message()
                    msg = msg % {"name": self.name}
                else:
                    msg = msg()
                return ValidationError(
                    msg,
                    code=code,
                )
        if self.kind == "unique" and self.fields:
            return self._get_unique_error_message()
        return None

    def add_to_form(self, form: forms.Form):
        """
        Add a ValidationError to the form.

        Builds the validation error and adds it to the
        form, either using the name of only included field,
        or using "__all__".
        """
        error = self.validation_error()
        if len(self.field_names) == 1:
            name = next(iter(self.field_names))
        else:
            name = "__all__"
        form.add_error(name, error)

    def _get_unique_error_message(self) -> ValidationError:
        instance = self.model()
        # Sort the field names for consistency.
        return instance.unique_error_message(self.model, sorted(self.field_names))

    def _default_error_message(self) -> str:
        return models.BaseConstraint.default_violation_error_message


RootCause = BareCause | Cause
