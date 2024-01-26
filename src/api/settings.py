from django.conf import settings


SUPPORTED_CURRENCIES = getattr(settings, "SUPPORTED_CURRENCIES", ["EUR", "USD"])
PAGINATION_PAGE_SIZE = getattr(settings, "PAGINATION_PAGE_SIZE", 10)
