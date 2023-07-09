from dataclasses import dataclass


@dataclass
class BaseResponse:
    message: str


@dataclass
class DataResponse(BaseResponse):
    data: list
