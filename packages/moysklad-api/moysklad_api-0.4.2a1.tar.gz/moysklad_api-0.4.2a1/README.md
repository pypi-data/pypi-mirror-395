<p align="center">
  <a href="https://api.moysklad.ru"><img src="https://www.moysklad.ru/upload/logos/logoMS500.png" alt="MoyskladAPI"></a>
</p>

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://img.shields.io/pypi/v/moysklad-api.svg)](https://pypi.org/project/moysklad-api/)
[![Downloads](https://img.shields.io/pypi/dm/moysklad-api.svg)](https://pypi.python.org/pypi/moysklad-api)
[![Status](https://img.shields.io/badge/status-pre--alpha-8B5CF6.svg?logo=git&logoColor=white)]()
[![API Version](https://img.shields.io/badge/Мой_Склад_API-1.2-blue.svg)](https://dev.moysklad.ru/doc/api/remap/1.2/)

</div>

> [!CAUTION]
> Библиотека находится в активной разработке и 100% **не рекомендуется для использования в продакшн среде**.

## Установка

```console
pip install moysklad-api
```

## Пример использования

```Python
import asyncio

from moysklad_api import MoyskladAPI
from moysklad_api import eq, empty

ms_api = MoyskladAPI(token="my_token")


async def get_filtered_products():
    return await ms_api.get_products(
        filters=(eq("archived", True), empty("description")),
        expand="supplier"
    )


if __name__ == __main__
    asyncio.run(get_filtered_products())
```
