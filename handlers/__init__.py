from aiogram import Dispatcher
from .start import router as start_router
from .capture import router as capture_router

def register_routers(dp: Dispatcher):
    dp.include_router(start_router)
    dp.include_router(capture_router)