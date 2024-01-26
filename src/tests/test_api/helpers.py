from api.models import Apartment
from django.contrib.auth.models import User


def create_test_apartment(
    realtor: User,
    title: str = "Title",
    description: str = "Description",
    area: int = 100,
    rooms_no: int = 4,
    price_month: int = 1000,
    currency: str = "EUR",
) -> Apartment:
    return Apartment.objects.create(
        realtor=realtor,
        title=title,
        description=description,
        area=area,
        rooms_no=rooms_no,
        price_month=price_month,
        currency=currency,
    )
