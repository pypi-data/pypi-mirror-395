from .base import BaseFilter


class Eq(BaseFilter):
    """Фильтрация по значению"""

    op = "="


class Empty(BaseFilter):
    """Фильтрация по пустому значению"""

    op = "="

    def __init__(
        self, field: str = None, value=None, previous_filter: BaseFilter = None
    ):
        super().__init__(field, value, previous_filter)


class Contains(BaseFilter):
    """Частичное совпадение"""

    op = "~"


class NotContains(BaseFilter):
    """Частичное совпадение не выводится"""

    op = "!~"


class Startswith(BaseFilter):
    """Полное совпадение в начале значения"""

    op = "~="


class Endswith(BaseFilter):
    """Полное совпадение в конце значения"""

    op = "=~"


class Gt(BaseFilter):
    """Больше"""

    op = ">"


class Lt(BaseFilter):
    """Меньше"""

    op = "<"


class Gte(BaseFilter):
    """Больше или равно"""

    op = ">="


class Lte(BaseFilter):
    """Меньше или равно"""

    op = "<="


def eq(field: str, value) -> Eq:
    """Фильтрация по значению

    Источник: https://dev.moysklad.ru/doc/api/remap/1.2/#/general#3-filtraciya-vyborki-s-pomoshyu-parametra-filter
    """
    return Eq(field, value)


def contains(field: str, value) -> Contains:
    """Частичное совпадение

    Источник: https://dev.moysklad.ru/doc/api/remap/1.2/#/general#3-filtraciya-vyborki-s-pomoshyu-parametra-filter
    """
    return Contains(field, value)


def not_contains(field: str, value) -> NotContains:
    """Частичное совпадение не выводится

    Источник: https://dev.moysklad.ru/doc/api/remap/1.2/#/general#3-filtraciya-vyborki-s-pomoshyu-parametra-filter
    """
    return NotContains(field, value)


def startswith(field: str, value) -> Startswith:
    """Полное совпадение в начале значения

    Источник: https://dev.moysklad.ru/doc/api/remap/1.2/#/general#3-filtraciya-vyborki-s-pomoshyu-parametra-filter
    """
    return Startswith(field, value)


def endswith(field: str, value) -> Endswith:
    """Полное совпадение в конце значения

    Источник: https://dev.moysklad.ru/doc/api/remap/1.2/#/general#3-filtraciya-vyborki-s-pomoshyu-parametra-filter
    """
    return Endswith(field, value)


def gt(field: str, value) -> Gt:
    """Больше

    Источник: https://dev.moysklad.ru/doc/api/remap/1.2/#/general#3-filtraciya-vyborki-s-pomoshyu-parametra-filter
    """
    return Gt(field, value)


def lt(field: str, value) -> Lt:
    """Меньше

    Источник: https://dev.moysklad.ru/doc/api/remap/1.2/#/general#3-filtraciya-vyborki-s-pomoshyu-parametra-filter
    """
    return Lt(field, value)


def gte(field: str, value) -> Gte:
    """Больше или равно

    Источник: https://dev.moysklad.ru/doc/api/remap/1.2/#/general#3-filtraciya-vyborki-s-pomoshyu-parametra-filter
    """
    return Gte(field, value)


def lte(field: str, value) -> Lte:
    """Меньше или равно

    Источник: https://dev.moysklad.ru/doc/api/remap/1.2/#/general#3-filtraciya-vyborki-s-pomoshyu-parametra-filter
    """
    return Lte(field, value)


def empty(field: str) -> Empty:
    """Фильтрация по пустому значению

    Источник: https://dev.moysklad.ru/doc/api/remap/1.2/#/general#3-filtraciya-vyborki-s-pomoshyu-parametra-filter
    """
    return Empty(field)
