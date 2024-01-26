from ninja_extra import NinjaExtraAPI
from ninja_jwt.controller import NinjaJWTDefaultController
from . import controllers

API_VERSION = "v0.0.1"

api = NinjaExtraAPI(
    title="Demo Apartment rentals backend API",
    version=API_VERSION,
    description=f"Apartment rentals backend API {API_VERSION}",
    app_name=f"apartmentrentals-api-{API_VERSION}",
    urls_namespace="api",
    servers=[
        # {"url": "https://yourdomain.com", "description": "Production Server"},
        # {"url": "http://localhost:8000", "description": "Development Server"},
    ],
)

api.register_controllers(
    NinjaJWTDefaultController,
    controllers.UserRegistrationController,
    controllers.RealtorController,
    controllers.ApartmentController,
)
