from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.http.request import HttpRequest
from ninja.errors import HttpError
from ninja_extra import api_controller, route

from .. import schemas


@api_controller("/registration", tags=["User Registration"])
class UserRegistrationController:
    @route.post("/new-user", response={201: schemas.UserRegistered}, url_name="user_registration")
    def register(self, request: HttpRequest, request_data: schemas.UserRegistrationModel):  # type: ignore
        user_model = get_user_model()
        if user_model.objects.filter(username=request_data.email).exists():
            raise HttpError(400, "User already exists")

        try:
            validate_password(request_data.password1)
        except ValidationError as e:
            raise HttpError(400, " ".join(e.messages))

        user = user_model.objects.create_user(
            username=request_data.email, email=request_data.email, password=request_data.password1
        )

        if request_data.is_realtor:
            realtor_group, _ = Group.objects.get_or_create(name="realtor")
            realtor_group.user_set.add(user)

        return 201, schemas.UserRegistered(email=user.email, is_realtor=request_data.is_realtor)
