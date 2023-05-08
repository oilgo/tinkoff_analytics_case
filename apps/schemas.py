from pydantic import BaseModel
from typing import Dict


class PurcaseRequest(BaseModel):
    """ Схема запроса для записи информации о покупках по партнерской акции в БД
    """

    customer_name: str
    phone_number: str
    email: str
    receipt: Dict[str, int]

    class Config:
        schema_extra = {
            "example": {
                "customer_name": 'Иванов Василий',
                "phone_number": "+7(000)123-45-67",
                "email": "vasya_ivanov@test.ru",
                "receipt": {
                    "рога": 2000,
                    "копыта": 5700
                }
            }
        }