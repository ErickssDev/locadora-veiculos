from fastapi import APIRouter

from .routes import admin, auth, notifications, reservations, users, vehicles

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(vehicles.router, prefix="/vehicles", tags=["Vehicles"])
api_router.include_router(reservations.router, prefix="/reservations", tags=["Reservations"])
api_router.include_router(admin.router, prefix="/admin", tags=["Admin"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["Notifications"])
