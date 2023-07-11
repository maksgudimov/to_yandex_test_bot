from aiogram import Bot,Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from starlette.config import Config
import logging

config = Config('.env')
MYID = config("MYID")
OPENTOKEN = config("OPENTOKEN")

bot = Bot(config("TOKEN"))
dp = Dispatcher(bot,storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)