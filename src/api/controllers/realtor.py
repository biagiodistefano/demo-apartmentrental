from django.http.request import HttpRequest
from django.shortcuts import get_object_or_404
from ninja import File, UploadedFile
from ninja_extra import api_controller, route
from ninja_extra.pagination import PageNumberPaginationExtra, PaginatedResponseSchema, paginate
from ninja_jwt.authentication import JWTAuth
from ninja.errors import HttpError

from .. import models, schemas, settings
from ..permissions import IsRealtor


@api_controller("/realtors", tags=["Realtors"], auth=[JWTAuth()], permissions=[IsRealtor])
class RealtorController:
    @route.post("/apartment", response={201: schemas.ApartmentView}, url_name="create_apartment")
    def create_apartment(self, request: HttpRequest, apartment: schemas.ApartmentCreate):  # type: ignore
        """Create a new apartment"""
        user_id = request.user.id
        return 201, models.Apartment.objects.create(realtor_id=user_id, **apartment.dict(exclude_unset=True))

    @route.post(
        "/apartment/{apartment_id}/image",
        response={200: schemas.ApartmentView},
        url_name="set_apartment_image",
    )
    def set_apartment_image(self, request: HttpRequest, apartment_id: int, image: UploadedFile = File(...)):  # type: ignore  # noqa: E501
        """
        Create a new apartment image
        """
        instance = get_object_or_404(models.Apartment, id=apartment_id)
        if instance.realtor_id != request.user.id:
            raise HttpError(403, "You are not allowed to edit this apartment")
        instance.preview_image.save(image.name, image)
        instance.save()
        return 200, instance

    @route.get(
        "/apartment/all", response=PaginatedResponseSchema[schemas.ApartmentView], url_name="get_all_own_apartments"
    )
    @paginate(PageNumberPaginationExtra, page_size=settings.PAGINATION_PAGE_SIZE)
    def get_all_own_apartments(self, request: HttpRequest):  # type: ignore
        """Get all apartments"""
        return models.Apartment.objects.filter(realtor_id=request.user.id)

    @route.put("/apartment/{apartment_id}", response={200: schemas.ApartmentView}, url_name="update_apartment")
    def update_apartment(self, request: HttpRequest, apartment_id: int, apartment: schemas.ApartmentEdit):  # type: ignore  # noqa: E501
        """Update an apartment by id"""
        instance = get_object_or_404(models.Apartment, id=apartment_id)
        if instance.realtor_id != request.user.id:
            raise HttpError(403, "You are not allowed to edit this apartment")
        models.Apartment.objects.filter(id=apartment_id).update(**apartment.dict(exclude_unset=True))
        return 200, models.Apartment.objects.get(id=apartment_id)

    @route.delete("/apartment/{apartment_id}", response={204: None}, url_name="delete_apartment")
    def delete_apartment(self, request: HttpRequest, apartment_id: int):  # type: ignore
        """Delete an apartment by id"""
        instance = get_object_or_404(models.Apartment, id=apartment_id)
        if instance.realtor_id != request.user.id:
            raise HttpError(403, "You are not allowed to delete this apartment")
        models.Apartment.objects.filter(id=apartment_id, realtor_id=request.user.id).delete()
        return 204, None
