from django.http.request import HttpRequest
from django.shortcuts import get_object_or_404
from ninja_extra import api_controller, route
from ninja_extra.pagination import PageNumberPaginationExtra, PaginatedResponseSchema, paginate
from ninja_jwt.authentication import JWTAuth


from .. import models, schemas, settings


@api_controller(
    tags=["Apartments"],
    auth=[JWTAuth()],
)
class ApartmentController:
    @route.post(
        "/apartment/search", response=PaginatedResponseSchema[schemas.ApartmentView], url_name="search_apartments"
    )
    @paginate(PageNumberPaginationExtra, page_size=settings.PAGINATION_PAGE_SIZE)
    def search_apartments(  # type: ignore
        self,
        request: HttpRequest,
        search_payload: schemas.SearchPayload,
    ):
        """Get all apartments"""
        search_payload_dict = search_payload.dict(exclude_unset=True)
        if description := search_payload_dict.pop("description", None):
            search_payload_dict["description__icontains"] = description
        if title := search_payload_dict.pop("title", None):
            search_payload_dict["title__icontains"] = title
        return models.Apartment.objects.filter(**search_payload_dict)

    @route.get("/apartment/{apartment_id}", response=schemas.ApartmentView, url_name="view_apartment")
    def view_apartment(self, request: HttpRequest, apartment_id: int):  # type: ignore
        """Get an apartment by id"""
        return get_object_or_404(models.Apartment, id=apartment_id)
