from __future__ import annotations

from django.dispatch import Signal

unmatched = Signal()


class Unmatched(Exception):
    pass


class UnexpectedErrorFormat(Unmatched):
    pass


class PossibleModelMismatch(Exception):
    pass
