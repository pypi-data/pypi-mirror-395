from typing import Self


class BaseFilter:
    op = "="

    __slots__ = ("_field", "_value", "_previous_filters")

    def __init__(
        self, field: str = None, value=None, previous_filter: "BaseFilter" = None
    ):
        self._field = field
        self._value = value
        self._previous_filters = []
        if previous_filter:
            self._previous_filters = previous_filter._previous_filters + [
                previous_filter
            ]

    def build(self) -> list[tuple[str, str, any]]:
        conditions = []

        for prev_filter in self._previous_filters:
            if prev_filter._field is not None:
                if isinstance(prev_filter._value, (list | tuple)):
                    for item in prev_filter._value:
                        conditions.append((prev_filter._field, prev_filter.op, item))
                else:
                    conditions.append(
                        (prev_filter._field, prev_filter.op, prev_filter._value)
                    )

        if self._field is not None:
            if isinstance(self._value, (list | tuple)):
                for item in self._value:
                    conditions.append((self._field, self.op, item))
            else:
                conditions.append((self._field, self.op, self._value))

        return conditions

    def __call__(self, field: str, value) -> Self:
        self._field = field
        self._value = value
        return self

    def __dir__(self):
        return [
            "eq",
            "contains",
            "not_contains",
            "startswith",
            "endswith",
            "gt",
            "lt",
            "gte",
            "lte",
            "empty",
            "build",
        ]

    def eq(self, field: str, value) -> Self:
        from .operators import Eq

        new_filter = Eq(field, value, self)
        return new_filter

    def contains(self, field: str, value) -> Self:
        from .operators import Contains

        new_filter = Contains(field, value, self)
        return new_filter

    def not_contains(self, field: str, value) -> Self:
        from .operators import NotContains

        new_filter = NotContains(field, value, self)
        return new_filter

    def startswith(self, field: str, value) -> Self:
        from .operators import Startswith

        new_filter = Startswith(field, value, self)
        return new_filter

    def endswith(self, field: str, value) -> Self:
        from .operators import Endswith

        new_filter = Endswith(field, value, self)
        return new_filter

    def gt(self, field: str, value) -> Self:
        from .operators import Gt

        new_filter = Gt(field, value, self)
        return new_filter

    def lt(self, field: str, value) -> Self:
        from .operators import Lt

        new_filter = Lt(field, value, self)
        return new_filter

    def gte(self, field: str, value) -> Self:
        from .operators import Gte

        new_filter = Gte(field, value, self)
        return new_filter

    def lte(self, field: str, value) -> Self:
        from .operators import Lte

        new_filter = Lte(field, value, self)
        return new_filter

    def empty(self, field: str) -> Self:
        from .operators import Empty

        new_filter = Empty(field, None, self)
        return new_filter


def build_filters(filter_obj: BaseFilter) -> str:
    if filter_obj is None:
        return ""

    conditions = filter_obj.build()
    combined = []

    for field, op, value in conditions:
        if value is None:
            combined.append(f"{field}{op}")
        else:
            value = str(value).lower()
            combined.append(f"{field}{op}{value}")

    return ";".join(combined)
