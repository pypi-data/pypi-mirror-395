from typing import TypedDict

from moysklad_api import BaseFilter


class DefaultParams(TypedDict, total=False):
    """
    Фильтрация выборки с помощью параметра filter

    Attributes:

        expand: Замена ссылок объектами

          Примеры:
            expand="demand"
            expand="product.supplier",
            expand=("product", "product.supplier")

            Источник: https://dev.moysklad.ru/doc/api/remap/1.2/#mojsklad-json-api-obschie-swedeniq-zamena-ssylok-ob-ektami-s-pomosch-u-expand

        filters: Фильтрация выборки

          Примеры:
            filters=eq("id", "c1234-5668-98123-34567abc")
            filters=contains("description", "срочный")
            filters=startswith("name", "тестовый")
            filters=endswith("code", "-001")
            filters=gt("quantity", 100)
            filters=empty("barcode")
            filters=eq("archived", False).contains("name", "товар").gt("price", 1000)

            Источник: https://dev.moysklad.ru/doc/api/remap/1.2/#mojsklad-json-api-obschie-swedeniq-fil-traciq-wyborki-s-pomosch-u-parametra-filter

        limit: Максимальное количество элементов в списке равно 1000.

          Чтобы получить больше 1000 элементов, используйте параметр paginate

        offset: Отступ в выданном списке

        search: Контекстный поиск

                Источник: https://dev.moysklad.ru/doc/api/remap/1.2/#mojsklad-json-api-obschie-swedeniq-kontextnyj-poisk

        order: Строка с условиями сортировки, перечисленными через ';'.
               Каждое условие сортировки - это сочетание названия поля,
               запятой (опционально, если указывается направление сортировки),
               направления сортировки (опционально: может принимать значения asc и desc.
               Значение по умолчанию - asc).

               Источник: https://dev.moysklad.ru/doc/api/remap/1.2/#mojsklad-json-api-obschie-swedeniq-sortirowka-ob-ektow

        paginate: Используйте этот параметр для получения всех элементов в списке
    """

    expand: tuple[str, ...] | str | None
    filters: BaseFilter | tuple[BaseFilter, ...] | None
    limit: int | None
    offset: int | None
    search: str | None
    order: str | None
    paginate: bool | None
