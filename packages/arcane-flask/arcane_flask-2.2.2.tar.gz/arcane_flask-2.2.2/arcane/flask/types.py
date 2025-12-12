from typing import TypeVar, Tuple, Union
from typing_extensions import TypedDict


class ErrorDict(TypedDict):
    detail: str


T = TypeVar('T')

ArcaneConnexionResponse = Tuple[Union[T, ErrorDict], int]
