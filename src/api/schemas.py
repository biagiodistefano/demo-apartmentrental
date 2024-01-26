import datetime
from typing import Optional

from ninja import Schema
from pydantic import EmailStr, model_validator


class RealtorView(Schema):
    id: int
    email: EmailStr
    first_name: str
    last_name: str


class ApartmentCreate(Schema):
    title: str
    description: str
    area: int
    rooms_no: int
    price_month: int
    currency: str = "EUR"


class ApartmentView(Schema):
    id: int
    realtor: RealtorView
    title: str
    preview_image: str | None = None
    description: str
    area: int
    rooms_no: int
    price_month: int
    currency: str
    date_added: datetime.datetime
    last_edited: datetime.datetime


class ApartmentEdit(Schema):
    title: Optional[str] = None
    description: Optional[str] = None
    area: Optional[int] = None
    rooms_no: Optional[int] = None
    price_month: Optional[int] = None
    currency: Optional[str] = None


class SearchPayload(Schema):
    realtor_id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    area: Optional[int] = None
    area__gt: Optional[int] = None
    area__gte: Optional[int] = None
    area__lt: Optional[int] = None
    area__lte: Optional[int] = None
    rooms_no: Optional[int] = None
    rooms_no__gt: Optional[int] = None
    rooms_no__gte: Optional[int] = None
    rooms_no__lt: Optional[int] = None
    rooms_no__lte: Optional[int] = None
    price_month: Optional[int] = None
    price_month__gt: Optional[int] = None
    price_month__gte: Optional[int] = None
    price_month__lt: Optional[int] = None
    price_month__lte: Optional[int] = None


class UserRegistrationModel(Schema):
    email: EmailStr
    password1: str
    password2: str
    is_realtor: bool = False

    @model_validator(mode="after")
    def check_passwords_match(self) -> "UserRegistrationModel":
        pw1 = self.password1
        pw2 = self.password2
        if pw1 is not None and pw2 is not None and pw1 != pw2:
            raise ValueError("passwords do not match")
        return self


class UserRegistered(Schema):
    email: EmailStr
    is_realtor: bool = False
