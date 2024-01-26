from django.db import models
from django.conf import settings
from .settings import SUPPORTED_CURRENCIES


class Apartment(models.Model):
    CURRENCY_CHOICES = [(currency, currency) for currency in SUPPORTED_CURRENCIES]

    realtor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, db_index=True)
    preview_image = models.ImageField(upload_to="images/", blank=True, null=True)
    description = models.TextField()
    area = models.IntegerField(db_index=True)
    rooms_no = models.IntegerField(db_index=True)
    price_month = models.IntegerField(db_index=True)
    currency = models.CharField(max_length=3, default="EUR", choices=CURRENCY_CHOICES, db_index=True)
    date_added = models.DateTimeField(auto_now_add=True)
    last_edited = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.title} ({self.area}m2, {self.rooms_no} rooms, {self.price_month} {self.currency}/month)"  # pragma: no cover  # noqa

    class Meta:
        ordering = ("-date_added",)
        indexes = [models.Index(fields=["area", "rooms_no", "price_month", "price_month", "currency"])]
