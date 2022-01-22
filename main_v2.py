from vk_api import VkApi
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import os
from dotenv import load_dotenv
from machine import СonditionMachine
from request_db import get_all_name

load_dotenv()
GROUP_ID = os.getenv('GROUP_ID')
GROUP_TOKEN = os.getenv('SECRET_KEY')
API_VERSION = os.getenv('API_VERSION')


def generate_keyboard(get_db_info, add_butt=None):
    keyboard = VkKeyboard(one_time=True, inline=False)
    for item in get_db_info:
        keyboard.add_button(
            label=item,
            color=VkKeyboardColor.POSITIVE,
            payload={"type": 'click'}
        )
    if add_butt:
        if add_butt['add_butt_back']:
            keyboard.add_button(
                "Back",
                color=VkKeyboardColor.NEGATIVE,
                payload={"type": "back"},
            )
        elif add_butt['add_butt_basket']:
            keyboard.add_button(
                "add in basket",
                color=VkKeyboardColor.PRIMARY,
                payload={"type": "add_butt_basket"},
            )
    keyboard.add_line()
    keyboard.add_button(
            label='view basket',
            color=VkKeyboardColor.PRIMARY,
            payload={"type": 'click'}
        )
    return keyboard


def start_page_send(event, vk, condition):
    photo = condition['page_photo']
    vk.messages.send(
        user_id=event.obj.message["from_id"],
        random_id=get_random_id(),
        peer_id=event.obj.message["from_id"],
        keyboard=generate_keyboard(['Выбор категорий'], None).get_keyboard(),
        attachment=f'photo-{GROUP_ID}_{photo}',
        message="Добро пожаловать !",
    )


def page_view(event, vk, condition, butt_back=False):
    photo = condition['page_photo']
    discription = 'Бот-пекарня'
    if condition['discription'] is not None:
        discription = condition['discription']
    vk.messages.send(
        user_id=event.obj.message["from_id"],
        random_id=get_random_id(),
        peer_id=event.obj.message["from_id"],
        keyboard=generate_keyboard(condition['page_butt_name'],
                                   condition).get_keyboard(),
        attachment=f'photo-{GROUP_ID}_{photo}',
        message=discription
    )


def main():
    vk_session = VkApi(token=GROUP_TOKEN, api_version=API_VERSION)
    vk = vk_session.get_api()
    longpoll = VkBotLongPoll(vk_session, group_id=GROUP_ID)
    user = СonditionMachine()
    all_valid_name = get_all_name() + ['Back', 'Выбор категорий', 'add in basket', 'view basket']
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            message = event.obj.message["text"]
            if message == "start":
                user.state_stack = []
                user.user_id = event.obj.message['from_id']
                condition = user.get_page_view('start')
                start_page_send(event, vk, condition)
            elif message in all_valid_name:
                condition = user.get_page_view(message)
                page_view(event, vk, condition)


if __name__ == "__main__":
    print('Bot run')
    main()
