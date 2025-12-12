class BaseFilter:
    _op = "="

    __slots__ = ("_field", "_value")

    def __init__(self, field: str = None, value=None):
        self._field = field
        self._value = value

    def build(self) -> list[tuple[str, str, any]]:
        if self._field is None:
            return []

        if isinstance(self._value, (list | tuple)):
            return [(self._field, self._op, item) for item in self._value]
        else:
            return [(self._field, self._op, self._value)]


def build_filters(filters) -> str:
    if not filters:
        return ""

    if isinstance(filters, BaseFilter):
        filters = [filters]

    parts = []
    for f in filters:
        for field, op, value in f.build():
            if value is None:
                parts.append(f"{field}{op}")
            else:
                parts.append(f"{field}{op}{str(value).lower()}")

    return ";".join(parts)
