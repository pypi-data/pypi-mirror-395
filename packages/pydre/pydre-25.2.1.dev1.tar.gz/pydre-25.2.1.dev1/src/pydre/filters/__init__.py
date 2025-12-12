from loguru import logger
from typing import Optional, Callable, Concatenate

__all__ = ["common", "eyetracking", "gazeangle"]

import pydre.core

filtersList: dict[
    str, Callable[Concatenate[pydre.core.DriveData, ...], pydre.core.DriveData]
] = {}


def registerFilter(filtername: Optional[str] = None) -> Callable:
    def registering_decorator(
        func: Callable[Concatenate[pydre.core.DriveData, ...], pydre.core.DriveData],
    ) -> Callable[Concatenate[pydre.core.DriveData, ...], pydre.core.DriveData]:
        name = filtername
        if not name:
            name = func.__name__
        # register function
        filtersList[name] = func
        return func

    return registering_decorator
