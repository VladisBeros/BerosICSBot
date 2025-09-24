import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    def __init__(self, BOT_TOKEN: str):
        self.BOT_TOKEN = BOT_TOKEN

def load_config() -> Config:
    return Config(
        BOT_TOKEN=os.getenv("BOT_TOKEN")
    )