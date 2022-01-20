from vk_api import VkApi
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import os
from dotenv import load_dotenv
from word_db import get_category, get_goods, get_price_good
from machine import СonditionMachine

load_dotenv()
GROUP_ID = os.getenv('GROUP_ID')
GROUP_TOKEN = os.getenv('SECRET_KEY')
API_VERSION = os.getenv('API_VERSION')


def generate_keyboard(get_db_info, type, butt_back=False, photo=None):
    keyboard = VkKeyboard(one_time=False, inline=True)
    for item in get_db_info:
        keyboard.add_button(
            label=item['name'],
            color=VkKeyboardColor.POSITIVE,
            payload={"type": type, 'photo': item.get('photo'),
                     'name': item.get('name')},
        )
    if butt_back:
        keyboard.add_button(
            "Назад",
            color=VkKeyboardColor.NEGATIVE,
            payload={"type": "back", 'photo': photo, 'name': 'back'},
        )
    return keyboard

def start_page_send(event, vk):
    photo = '457239027'
    vk.messages.send(
        user_id=event.obj.message["from_id"],
        random_id=get_random_id(),
        peer_id=event.obj.message["from_id"],
        keyboard=generate_keyboard([{'name': 'Выбор категорий'}],
                                'category_page').get_keyboard(),
        message="Добро пожаловать !",
        # attachment=f'photo-{GROUP_ID}_{photo}'
)
def call_back(event, vk):
    # photo = '457239027'
    vk.messages.edit(
        conversation_message_id=event.obj.conversation_message_id,
        random_id=get_random_id(),
        peer_id=event.obj.peer_id,
        message="Не Добро пожаловать !",
    )

def start_page_send(event, vk, condition):
    photo = condition['page_photo']
    vk.messages.send(
        user_id=event.obj.message["from_id"],
        random_id=get_random_id(),
        peer_id=event.obj.message["from_id"],
        keyboard=generate_keyboard([{'name': 'Выбор категорий'}],
                                'category_page').get_keyboard(),
        attachment=f'photo-{GROUP_ID}_{photo}',
        message="Добро пожаловать !",
    )


def page_view(event, vk, condition):
    photo = condition['page_photo']
    vk.messages.edit(
        conversation_message_id=event.obj.conversation_message_id,
        random_id=get_random_id(),
        peer_id=event.obj.peer_id,
        keyboard=None,
        attachment=f'photo-{GROUP_ID}_{photo}',
    )
    print(condition)

def main():
    vk_session = VkApi(token=GROUP_TOKEN, api_version=API_VERSION)
    vk = vk_session.get_api()
    longpoll = VkBotLongPoll(vk_session, group_id=GROUP_ID)
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            if event.obj.message["text"] == "start":
                print(event.obj)
                print('-'*50)
                user = СonditionMachine()
                user.user_id = event.obj.message['from_id']
                condition = user.get_page_view('start')
                start_page_send(event, vk, condition)
            elif event.obj.message["text"] != "start" and event.obj.message['from_id'] == user.user_id:
                print(event.obj)
                print('-'*50)

        # elif event.type == VkBotEventType.MESSAGE_REPLY:
        #     print('lol')
        #     print(event.object)
        #     call_back(event, vk)
        #             start_page_send(event, vk)
        # elif event.type == VkBotEventType.MESSAGE_EVENT:
        #     if event.object.payload.get("type") == "back":
        #         go_back(event, vk, state_cache)
        #     elif event.object.payload.get("type") == 'category_page':
        #         state_cache, but_name = chagne_status(state_cache, event)
        #         category_page(event, vk, but_name)
        #     elif event.object.payload.get("type") == "goods_page":
        #         state_cache, but_name = chagne_status(state_cache, event)
        #         goods_page(event, vk, but_name)
        #     elif event.object.payload.get("type") == "good_page":
        #         state_cache, but_name = chagne_status(state_cache, event)
        #         good_page(event, vk, but_name)


if __name__ == "__main__":
    print('Bot run')
    main()
