from __future__ import annotations

from abc import ABC, abstractmethod
from typing import (
    TYPE_CHECKING,
    ClassVar,
    Generic,
    TypeVar,
    final,
    get_origin,
)
from urllib.parse import urlencode

from pydantic import BaseModel, ConfigDict

from moysklad_api import build_filters
from moysklad_api.client.default import DefaultParams
from moysklad_api.client.remap import PRODUCTION
from moysklad_api.client.session import BaseSession, Method
from moysklad_api.exceptions import MSApiError
from moysklad_api.types import Meta, MetaArray


T = TypeVar("T", bound=BaseModel)
R = TypeVar("R", bound=MetaArray)


class MSMethod(BaseModel, Generic[T], ABC):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
        extra="allow",
    )

    params: DefaultParams | None = None

    def model_dump(self, **kwargs):
        # Temporarily remove filters from params to avoid serialization errors
        # since custom filter objects cannot be serialized by Pydantic
        filters = None
        if self.params and "filters" in self.params:
            filters = self.params.pop("filters")
        result = super().model_dump(**kwargs)

        if filters is not None:
            self.params["filters"] = filters

        return result

    if TYPE_CHECKING:
        __return__: BaseModel
        __api_method__: ClassVar[str]
    else:

        @property
        @abstractmethod
        def __return__(self) -> type[T]:
            pass

        @property
        @abstractmethod
        def __api_method__(self) -> str:
            pass

    @final
    def __get_query_params(self) -> dict[str, str]:
        params = {}

        if self.params is None:
            return params

        if limit := self.params.get("limit"):
            params["limit"] = str(limit)

        if expand := self.params.get("expand"):
            if isinstance(expand, tuple):
                params["expand"] = ",".join(expand)
            else:
                params["expand"] = str(expand)
            params["limit"] = "100"

        if filters := self.params.get("filters"):
            params["filter"] = build_filters(filters)

        if offset := self.params.get("offset"):
            params["offset"] = str(offset)

        return params

    def _prepare_request_data(self, data: dict) -> dict | list[dict]:
        if hasattr(self, "data") and isinstance(data.get("data"), list):
            prepared_data = []
            for item in data["data"]:
                if isinstance(item, dict) and "id" in item:
                    meta = self._create_meta(item["id"]).model_dump(by_alias=True)
                    prepared_item = {
                        "meta": meta,
                        **{k: v for k, v in item.items() if k != "id"},
                    }
                    prepared_data.append(prepared_item)
                else:
                    prepared_data.append(item)
            return prepared_data

        elif hasattr(self, "id") and self.id:
            meta = self._create_meta(self.id).model_dump(by_alias=True)
            return {"meta": meta, **{k: v for k, v in data.items() if k != "id"}}
        return data

    def _create_meta(self, _id: str | None = None) -> Meta:
        if hasattr(self.__return__, "__args__") and self.__return__.__args__:
            type_name = self.__return__.__args__[0].__name__
        else:
            type_name = self.__return__.__name__

        words = []
        current_word = ""
        for char in type_name:
            if char.isupper() and current_word:
                words.append(current_word.lower())
                current_word = char
            else:
                current_word += char
        if current_word:
            words.append(current_word.lower())
        if words:
            _meta_type = words[0]
        else:
            _meta_type = type_name.lower()

        __meta_href__ = f"{PRODUCTION.url}/{self.__api_method__}/{_id}"

        return Meta(
            href=__meta_href__,
            type=_meta_type,
        )

    async def __get_rows(self, session: BaseSession, url: str) -> MetaArray:
        all_rows = []
        first_meta = None

        while url:
            response = await session.get(url)
            if not response.ok:
                raise MSApiError(
                    message=f"{response.error} (code: {response.status})",
                    url=getattr(response, "more_info", "https://dev.moysklad.ru"),
                )

            resp_data = response.data
            if isinstance(resp_data, dict):
                if first_meta is None:
                    first_page = self.__return__.model_validate(resp_data)
                    first_meta = first_page.meta
                    all_rows.extend(first_page.rows)
                else:
                    page = self.__return__.model_validate(resp_data)
                    all_rows.extend(page.rows)

                meta = resp_data.get("meta", {})
                url = meta.get("nextHref")
            else:
                break

        if first_meta:
            updated_meta = first_meta.model_dump()
            updated_meta.update(
                {
                    "size": len(all_rows),
                    "nextHref": None,
                    "limit": len(all_rows),
                    "offset": 0,
                }
            )

            return MetaArray(rows=all_rows, meta=Meta(**updated_meta))

        return MetaArray(rows=all_rows, meta=Meta(href=url, type=""))

    async def call(
        self, session: BaseSession, self_method: Method = Method.GET
    ) -> T | list[T] | R[T]:
        url = f"{session.base_url}/{self.__api_method__}"
        template = "{id}" in self.__api_method__ and hasattr(self, "id")
        obj_id = getattr(self, "id", None)

        raw_data = self.model_dump(mode="json", exclude_none=True, by_alias=True)

        data = self._prepare_request_data(raw_data)
        query_params = self.__get_query_params()

        if template and obj_id:
            url = url.replace("{id}", obj_id)
        elif obj_id:
            url = f"{url}/{obj_id}"

        if query_params:
            url += "?" + urlencode(query_params, doseq=True)

        params_dict = getattr(self, "params", {}) or {}
        paginate = params_dict.get("paginate", False)

        if self_method == Method.GET and paginate:
            result = await self.__get_rows(session, url)
            return result
        elif self_method == Method.PUT:
            response = await session.put(url, json=data)
        elif self_method == Method.POST:
            response = await session.post(url, json=data)
        else:
            response = await session.get(url)

        if not response.ok:
            raise MSApiError(
                message=f"{response.error} (code: {response.status})",
                url=getattr(response, "more_info", "https://dev.moysklad.ru"),
            )

        resp_data = response.data
        origin = get_origin(self.__return__)

        if isinstance(resp_data, dict) and "rows" in resp_data:
            return self.__return__.model_validate(resp_data)

        if isinstance(resp_data, list):
            if origin is list:
                item_model = self.__return__.__args__[0]
                return [item_model.model_validate(item) for item in resp_data]
            else:
                return self.__return__.model_validate(resp_data[0])
        return self.__return__.model_validate(resp_data)

    def __await__(self):
        raise RuntimeError(f"{self.cls.__name__} cannot be called directly.")
