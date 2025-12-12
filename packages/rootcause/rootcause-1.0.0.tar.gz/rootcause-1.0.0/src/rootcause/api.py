from __future__ import annotations

import logging
from typing import overload

from django.db import IntegrityError, connections, models

from . import mysql, postgres, sqlite
from .base import Unmatched, unmatched
from .causes import BareCause, Cause

logger = logging.getLogger("rootcause")


@overload
def resolve(
    error: IntegrityError,
    model: models.Model,
    using: str = "default",
    reraise_if_unknown: bool = True,
) -> Cause: ...


@overload
def resolve(
    error: IntegrityError,
    model: type[models.Model],
    using: str = "default",
    reraise_if_unknown: bool = True,
) -> Cause: ...


def resolve(
    error: IntegrityError,
    model: models.Model | type[models.Model],
    using: str = "default",
    reraise_if_unknown: bool = True,
) -> Cause:
    model_cls = _get_model_class(model=model)
    cause, vendor = _parse(
        error=error,
        model_cls=model_cls,
        using=using,
        reraise_if_unknown=reraise_if_unknown,
    )
    module = _get_vendor_module(vendor)
    return module.resolve(cause)


@overload
def of(
    error: IntegrityError,
    model: None = None,
    using: str = "default",
    reraise_if_unknown: bool = True,
) -> BareCause: ...


@overload
def of(
    error: IntegrityError,
    model: models.Model,
    using: str = "default",
    reraise_if_unknown: bool = True,
) -> Cause: ...


@overload
def of(
    error: IntegrityError,
    model: type[models.Model],
    using: str = "default",
    reraise_if_unknown: bool = True,
) -> Cause: ...


def of(
    error: IntegrityError,
    model: models.Model | type[models.Model] | None = None,
    using: str = "default",
    reraise_if_unknown: bool = True,
) -> BareCause | Cause:
    """
    Try to find the root cause of an IntegrityError.

    :param error: The IntegrityError to inspect.
    :type error: IntegrityError
    :param model: Upgrades result from BareCause to Cause.
    :type model: models.Model | type[models.Model] | None
    :param using: Database alias in the settings to check type of database
    :type using: str
    :param reraise_if_unknown: reraise IntegrityError when no info was found
    :type reraise_if_unknown: bool
    :return: The cause of the IntegrityError
    :rtype: BareCause | Cause
    :raises Unmatched: When no info was found and reraise_if_unknown=False
    :raises IntegrityError: When no info was found and reraise_if_unknown=True

    Pass in a model instance or class to upgrade from a
    BareCause to a Cause return value, which includes
    information about the involved fields.

    Usage:

        try:
            ... # something that raises IntegrityError
        except IntegrityError as e:
            # Grab the root cause with model info.
            # So we're dealing with field names, not
            # column names.
            cause = rootcause.of(e, model=MyModel)
            # Single unique field
            if cause.is_unique("name"):
                raise UniqueNameRequired(name=name)
            # Unique constraint with two fields.
            if cause.is_unique("shirt", "pants"):
                raise AttireUnavailable(
                    f"The {shirt} shirt and {pants} pants "
                    f"are already taken."
                )
            # A check constraint
            if cause.is_check(name="value_max_10"):
                raise MaxValueReached(max_value=10)
            # A unique constraint, but checked using
            # the constraint's name.
            if cause.is_unique(name="uq_rank"):
                raise RankTaken()
            raise

    """
    model_cls = _get_model_class(model=model)
    cause, _ = _parse(
        error=error,
        model_cls=model_cls,
        using=using,
        reraise_if_unknown=reraise_if_unknown,
    )
    return cause


def _parse(
    *,
    error: IntegrityError,
    model_cls: type[models.Model] | None,
    using: str,
    reraise_if_unknown: bool = True,
) -> tuple[BareCause | Cause, str]:
    conn = connections[using]
    vendor = conn.vendor
    module = _get_vendor_module(vendor)
    try:
        cause = module.parse(error, model=model_cls)
    except Unmatched:
        # Check whether there's a signal receiver that can help us out.
        # Return the first actual response.
        for _, response in unmatched.send(error, vendor=vendor):
            if not response:
                continue
            if not isinstance(response, BareCause | Cause):
                logger.error(
                    "Received a response from a receiver for the unmatched signal, "
                    "but the response is not an instance of BareCause or Cause: %s. "
                    "Ignoring.",
                    type(response),
                )
                continue
            cause = response
            break
        else:
            # Raise the original error
            if reraise_if_unknown:
                raise error
            # Raise Unmatched
            raise
    return cause, vendor


def _get_model_class(
    model: models.Model | type[models.Model] | None,
) -> type[models.Model]:
    if model is None:
        return None
    if isinstance(model, models.Model):
        return model.__class__
    if issubclass(model, models.Model):
        return model
    raise ValueError(
        f"model parameter should be a Model instance or subclass; "
        f"received {type(model)} ({model})"
    )


def _get_vendor_module(vendor: str):
    if vendor == "sqlite":
        return sqlite
    if vendor == "postgresql":
        return postgres
    if vendor == "mysql":
        return mysql
    raise RuntimeError(f"{vendor} is not supported")
