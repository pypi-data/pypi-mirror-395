from dataclasses import dataclass


@dataclass
class Remap:
    url: str


PRODUCTION = Remap(
    url="https://api.moysklad.ru/api/remap/1.2",
)
