from typing import Unpack

from moysklad_api.client.default import DefaultParams
from moysklad_api.client.remap import PRODUCTION
from moysklad_api.client.session import BaseSession, Headers, Method
from moysklad_api.loggers import api
from moysklad_api.methods import (
    GetAssortment,
    GetAudit,
    GetCounterparty,
    GetCurrentStock,
    GetEvents,
    GetProduct,
    GetProducts,
    GetPurchaseOrder,
    GetPurchaseOrders,
    GetStock,
    GetToken,
    GetVariant,
    GetVariants,
    GetWebhook,
    GetWebhooks,
    MSMethod,
    T,
    UpdateProduct,
    UpdateProducts,
    UpdateVariant,
    UpdateVariants,
)
from moysklad_api.methods.base import R
from moysklad_api.methods.get_counterparties import GetCounterparties
from moysklad_api.methods.get_demand import GetDemand
from moysklad_api.methods.get_demands import GetDemands
from moysklad_api.types import (
    Assortment,
    Audit,
    Barcode,
    BuyPrice,
    Counterparty,
    CurrentStock,
    Demand,
    Event,
    Image,
    MetaArray,
    MinPrice,
    Pack,
    Product,
    PurchaseOrder,
    SalePrice,
    Stock,
    Token,
    Variant,
    Webhook,
)
from moysklad_api.utils.token import validate_token


class MoyskladAPI:
    def __init__(self, token: str, session: BaseSession | None = None, **kwargs):
        """
        Клиент для работы с API МойСклад

        Attributes:

            token: Токен доступа

                Источник: https://api.moysklad.ru/api/remap/1.2/security/token
        """
        validate_token(token)
        if session is None:
            session = BaseSession(
                base=PRODUCTION.url,
                timeout=PRODUCTION.timeout,
            )

        self.__token = token
        self._session_headers = self._create_session_headers(self.__token)
        self._session = session
        self._session.headers = self._session_headers

    @property
    def session(self) -> BaseSession:
        return self._session

    @property
    def base(self) -> str:
        return self._session.base

    @property
    def timeout(self) -> int:
        return self._session.timeout

    @property
    def token(self) -> str:
        return self.__token

    @classmethod
    async def authenticate(
        cls, username: str, password: str, session: BaseSession | None = None
    ) -> "MoyskladAPI":
        if session is None:
            session = BaseSession(
                base=PRODUCTION.url,
                timeout=PRODUCTION.timeout,
            )

        dummy_api = cls(token="dummy", session=session)
        token = await dummy_api.get_token(username, password)
        api.warning(
            f"Используйте этот токен :code:`{token.access_token}` "
            f"для последующих запросов."
        )
        return cls(token=token.access_token, session=session)

    async def close(self):
        await self._session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        import asyncio

        asyncio.run(self.close())

    async def __call__(
        self, method: MSMethod[T], self_method: Method | None = Method.GET
    ) -> T | R:
        return await method.call(self.session, self_method)

    async def get_token(self, username: str, password: str) -> Token:
        call = GetToken(
            username=username,
            password=password,
        )
        return await self(call)

    @staticmethod
    def _create_session_headers(token: str) -> Headers:
        return Headers(token=token)

    async def get_assortment(
        self, **params: Unpack[DefaultParams]
    ) -> MetaArray[Assortment]:
        """
        Используйте этот метод для получения ассортимента

        Подробная документация по параметрам запроса: :class:`DefaultParams`

        Источник: https://dev.moysklad.ru/doc/api/remap/1.2/#/dictionaries/assortment#2-assortiment
        :return: :class:`MetaArray[Assortment]`: Ассортимент
        """
        call = GetAssortment(params=params)
        return await self(call)

    async def get_counterparty(
        self, counterparty_id: str, **params: Unpack[DefaultParams]
    ) -> Counterparty:
        """
        Используйте этот метод для получения контрагента по ID

        Подробная документация по параметрам запроса: :class:`DefaultParams`

        Источник: https://dev.moysklad.ru/doc/api/remap/1.2/#/dictionaries/counterparty#3-poluchit-kontragenta
        :return: :class:`Counterparty`: Контрагент
        """
        call = GetCounterparty(counterparty_id=counterparty_id, params=params)
        return await self(call)

    async def get_counterparties(
        self, **params: Unpack[DefaultParams]
    ) -> MetaArray[Counterparty]:
        """
        Используйте этот метод для получения списка контрагентов

        Подробная документация по параметрам запроса: :class:`DefaultParams`

        Источник: https://dev.moysklad.ru/doc/api/remap/1.2/#/dictionaries/counterparty#3-poluchit-spisok-kontragentov
        :return: :class:`MetaArray[Counterparty]`: Список контрагентов
        """
        call = GetCounterparties(params=params)
        return await self(call)

    async def get_product(
        self, product_id: str, **params: Unpack[DefaultParams]
    ) -> Product:
        """
        Используйте этот метод для получения товара по ID

        Подробная документация по параметрам запроса: :class:`DefaultParams`

        Источник: https://dev.moysklad.ru/doc/api/remap/1.2/#/dictionaries/product#3-zaprosy-tovar
        :return: :class:`Product`: Товар
        """
        call = GetProduct(product_id=product_id, params=params)
        return await self(call)

    async def get_products(self, **params: Unpack[DefaultParams]) -> MetaArray[Product]:
        """
        Используйте этот метод для получения списка товаров

        Подробная документация по параметрам запроса: :class:`DefaultParams`

        Источник: https://dev.moysklad.ru/doc/api/remap/1.2/#/dictionaries/product#3-poluchit-spisok-tovarov
        :return: :class:`MetaArray[Product]`: Список товаров
        """
        call = GetProducts(params=params)
        return await self(call)

    async def update_product(
        self,
        product_id: str,
        name: str | None = None,
        description: str | None = None,
        code: str | None = None,
        external_code: str | None = None,
        archived: bool | None = None,
        article: str | None = None,
        group: str | None = None,
        product_folder: str | None = None,
        sale_prices: list[dict] | None = None,
        attributes: list[dict] | None = None,
        barcodes: list[dict] | None = None,
        min_price: dict | None = None,
        uom: str | None = None,
        tracking_type: str | None = None,
        is_serial_trackable: bool | None = None,
        files: list[dict] | None = None,
        images: list[dict] | None = None,
        packs: list[dict] | None = None,
        owner: str | None = None,
        supplier: str | None = None,
        shared: bool | None = None,
        discount_prohibited: bool | None = None,
        use_parent_vat: bool | None = None,
    ) -> Product:
        """
        Используйте этот метод для обновления товара

        Источник: https://dev.moysklad.ru/doc/api/remap/1.2/#/dictionaries/product#3-izmenit-tovar
        :return: :class:`Product`: Обновленный товар
        """
        call = UpdateProduct(
            product_id=product_id,
            name=name,
            description=description,
            code=code,
            external_code=external_code,
            archived=archived,
            article=article,
            group=group,
            product_folder=product_folder,
            sale_prices=sale_prices,
            attributes=attributes,
            barcodes=barcodes,
            min_price=min_price,
            uom=uom,
            tracking_type=tracking_type,
            is_serial_trackable=is_serial_trackable,
            files=files,
            images=images,
            packs=packs,
            owner=owner,
            supplier=supplier,
            shared=shared,
            discount_prohibited=discount_prohibited,
            use_parent_vat=use_parent_vat,
        )
        return await self(call, self_method=Method.PUT)

    async def update_products(self, products: list[Product]) -> list[Product]:
        """
        Используйте этот метод для массового обновления товаров

        Источник: https://dev.moysklad.ru/doc/api/remap/1.2/#/dictionaries/product#3-massovoe-sozdanie-i-obnovlenie-tovarov
        :return: :class:`list[ProductUpdate]`: Список обновленных товаров
        """
        call = UpdateProducts(
            data=products,
        )
        return await self(call, self_method=Method.POST)

    async def get_stock(
        self,
        current: bool = True,
        **params: Unpack[DefaultParams],
    ) -> CurrentStock | MetaArray[Stock]:
        """
        Используйте этот метод для получения отчета об остатках

        Подробная документация по параметрам запроса: :class:`DefaultParams`

        Источники:
            https://dev.moysklad.ru/doc/api/remap/1.2/#/reports/report-stock#2-otchet-ostatki
            https://dev.moysklad.ru/doc/api/remap/1.2/#/reports/report-stock#3-kratkij-otchet-ob-ostatkah

        :param current: Получить краткий отчет об остатках вместо расширенного

        :return: :class:`CurrentStock` | :class:`MetaArray[Stock]`: Остатки
        """
        call = GetCurrentStock(params=params)
        if not current:
            call = GetStock(params=params)
        return await self(call)

    async def get_demand(
        self,
        demand_id: str,
        **params: Unpack[DefaultParams],
    ) -> Demand:
        """
        Используйте этот метод для получения отгрузки по ID

        Подробная документация по параметрам запроса: :class:`DefaultParams`

        Источник: https://dev.moysklad.ru/doc/api/remap/1.2/#/documents/demand#3-poluchit-otgruzku
        :return: :class:`Demand`: Отгрузка
        """
        call = GetDemand(demand_id=demand_id, params=params)
        return await self(call)

    async def get_demands(
        self,
        **params: Unpack[DefaultParams],
    ) -> MetaArray[Demand]:
        """
        Используйте этот метод для получения списка отгрузок

        Подробная документация по параметрам запроса: :class:`DefaultParams`

        Источник: https://dev.moysklad.ru/doc/api/remap/1.2/#/documents/demand#3-poluchit-spisok-otgruzok
        :return: :class:`MetaArray[Demand]`: Список отгрузок
        """
        call = GetDemands(params=params)
        return await self(call)

    async def get_audit(
        self,
        audit_id: str,
        **params: Unpack[DefaultParams],
    ) -> Audit:
        """
        Используйте этот метод для получения аудита (контекста) по ID

        Подробная документация по параметрам запроса: :class:`DefaultParams`

        Источник: https://dev.moysklad.ru/doc/api/remap/1.2/#/audit/audit#3-poluchit-konteksty
        :return: :class:`Audit`: Аудит
        """
        call = GetAudit(audit_id=audit_id, params=params)
        return await self(call)

    async def get_audit_events(
        self,
        audit_id: str,
        **params: Unpack[DefaultParams],
    ) -> MetaArray[Event]:
        """
        Используйте этот метод для получения событий аудита (контекста)

        Подробная документация по параметрам запроса: :class:`DefaultParams`

        Источник: https://dev.moysklad.ru/doc/api/remap/1.2/#/audit/audit#3-poluchit-sobytiya-po-kontekstu
        :return: :class:`MetaArray[Event]`: Список событий аудита
        """
        call = GetEvents(audit_id=audit_id, params=params)
        return await self(call)

    async def get_webhook(
        self,
        webhook_id: str,
        **params: Unpack[DefaultParams],
    ) -> Webhook:
        """
        Используйте этот метод для получения вебхука по ID

        Подробная документация по параметрам запроса: :class:`DefaultParams`

        Источник: https://dev.moysklad.ru/doc/api/remap/1.2/#/workbook/workbook-webhooks#3-kak-ispolzovat-vebhuki-cherez-json-api
        :return: :class:`Webhook`: Вебхук
        """
        call = GetWebhook(webhook_id=webhook_id, params=params)
        return await self(call)

    async def get_webhooks(
        self,
        **params: Unpack[DefaultParams],
    ) -> Webhook:
        """
        Используйте этот метод для получения списка вебхуков

        Подробная документация по параметрам запроса: :class:`DefaultParams`

        Источник: https://dev.moysklad.ru/doc/api/remap/1.2/#/workbook/workbook-webhooks#3-kak-ispolzovat-vebhuki-cherez-json-api
        :return: :class:`Webhook`: Список вебхуков
        """
        call = GetWebhooks(params=params)
        return await self(call)

    async def get_purchaseorder(
        self,
        purchaseorder_id: str,
        **params: Unpack[DefaultParams],
    ) -> PurchaseOrder:
        """
        Используйте этот метод для получения заказа поставщику по ID

        Подробная документация по параметрам запроса: :class:`DefaultParams`

        Источник: https://dev.moysklad.ru/doc/api/remap/1.2/#/documents/purchaseOrder#3-poluchit-zakaz-postavshiku
        :return: :class:`PurchaseOrder`: Заказ поставщику
        """
        call = GetPurchaseOrder(purchaseorder_id=purchaseorder_id, params=params)
        return await self(call)

    async def get_purchaseorders(
        self,
        **params: Unpack[DefaultParams],
    ) -> MetaArray[PurchaseOrder]:
        """
        Используйте этот метод для получения заказов поставщику

        Подробная документация по параметрам запроса: :class:`DefaultParams`

        Источник: https://dev.moysklad.ru/doc/api/remap/1.2/#/documents/purchaseOrder#3-poluchit-spisok-zakazov-postavshikam
        :return: :class:`MetaArray[PurchaseOrder]`: Список заказов поставщикам
        """
        call = GetPurchaseOrders(params=params)
        return await self(call)

    async def get_variant(
        self, variant_id: str, **params: Unpack[DefaultParams]
    ) -> Variant:
        """
        Используйте этот метод для получения модификации по ID

        Подробная документация по параметрам запроса: :class:`DefaultParams`

        Источник: https://dev.moysklad.ru/doc/api/remap/1.2/#/dictionaries/variant#3-modifikacii
        :return: :class:`Variant`: Модификация
        """
        call = GetVariant(variant_id=variant_id, params=params)
        return await self(call)

    async def get_variants(self, **params: Unpack[DefaultParams]) -> MetaArray[Variant]:
        """
        Используйте этот метод для получения списка модификаций

        Подробная документация по параметрам запроса: :class:`DefaultParams`

        Источник: https://dev.moysklad.ru/doc/api/remap/1.2/#/dictionaries/variant#3-poluchit-spisok-modifikacij
        :return: :class:`MetaArray[Variant]`: Список модификаций
        """
        call = GetVariants(params=params)
        return await self(call)

    async def update_variant(
        self,
        variant_id: str,
        name: str | None = None,
        description: str | None = None,
        code: str | None = None,
        external_code: str | None = None,
        archived: bool | None = None,
        barcodes: list[Barcode] | None = None,
        buy_price: BuyPrice | None = None,
        characteristics: list[dict] | None = None,
        discount_prohibited: bool | None = None,
        images: list[Image] | None = None,
        min_price: MinPrice | None = None,
        minimum_stock: dict | None = None,
        packs: list[Pack] | None = None,
        sale_prices: list[SalePrice] | None = None,
        product: Product | None = None,
    ) -> Variant:
        """
        Используйте этот метод для обновления модификации

        Источник: https://dev.moysklad.ru/doc/api/remap/1.2/#/dictionaries/variant#3-izmenit-modifikaciyu
        :return: :class:`Variant`: Обновленная модификация
        """
        call = UpdateVariant(
            variant_id=variant_id,
            name=name,
            description=description,
            code=code,
            external_code=external_code,
            archived=archived,
            barcodes=barcodes,
            buy_price=buy_price,
            characteristics=characteristics,
            discount_prohibited=discount_prohibited,
            images=images,
            min_price=min_price,
            minimum_stock=minimum_stock,
            packs=packs,
            sale_prices=sale_prices,
            product=product,
        )
        return await self(call, self_method=Method.PUT)

    async def update_variants(self, variants: list[Variant]) -> list[Variant]:
        """
        Используйте этот метод для массового обновления модификаций

        Источник: https://dev.moysklad.ru/doc/api/remap/1.2/#/dictionaries/variant#3-massovoe-sozdanie-i-obnovlenie-modifikacij
        :return: :class:`list[Variant]`: Список обновленных модификаций
        """
        call = UpdateVariants(
            data=variants,
        )
        return await self(call, self_method=Method.POST)
