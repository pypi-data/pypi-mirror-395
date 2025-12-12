from dataclasses import dataclass


@dataclass
class Remap:
    url: str
    timeout: int


PRODUCTION = Remap(
    url="https://api.moysklad.ru/api/remap/1.2",
    timeout=30,
)
