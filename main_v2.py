from tempfile import template
from vkbottle.bot import Bot, Message
from vkbottle import Keyboard, KeyboardButtonColor, Text, OpenLink, Location, EMPTY_KEYBOARD, template_gen, TemplateElement, GroupEventType, Callback, GroupTypes
from vkbottle.modules import json
from vk_api.utils import get_random_id
import os
from dotenv import load_dotenv
import asyncio
from word_db import get_category, get_goods, get_price_good, get_category_photo

load_dotenv()
GROUP_ID = os.getenv('GROUP_ID')
GROUP_TOKEN = os.getenv('SECRET_KEY')
API_VERSION = os.getenv('API_VERSION')


bot = Bot(token=GROUP_TOKEN)

@bot.on.message(text="start")
async def handler(message: Message):
	await message.answer(message="Добро пожаловать")

@bot.on.message(text="Добро пожаловать")
async def handler_lol(message: Message):
	await message.answer(message="Не Добро пожаловать")

# @bot.on.message(text="start")
# async def handler(message: Message):
# 	keyboard = (
# 		Keyboard(one_time=True)
# 		.add(Callback("Начнем!", {"cmd": "click", 'message_id': 'None'}))
# 	)
# 	await message.answer(message="Добро пожаловать", keyboard=keyboard)

# @bot.on.raw_event(GroupEventType.MESSAGE_EVENT, dataclass=GroupTypes.MessageEvent)
# async def message_event_handler(event: GroupTypes.MessageEvent):
#     keyboard1 = (Keyboard(one_time=True)
# 		.add(Callback("category1", {"cmd": "click1"}))
#         .add(Callback("category2", {"cmd": "click2"}))
#         .add(Callback("category3", {"cmd": "click3"}))
#         )
#     print(f'================={event.object}------------------------------------------------')
#     await event.ctx_api.messages.edit(
#         peer_id=event.object.peer_id,
#         keyboard=keyboard1,
#         message='Выбери категорию',
#         message_id=0,
#         conversation_message_id=0,
#     )



print('bot run')
bot.run_forever()