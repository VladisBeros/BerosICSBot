from .start import register_start_handler
from .capture_ics import register_capture_handler

def register_handlers(bot):
    register_start_handler(bot)
    register_capture_handler(bot)