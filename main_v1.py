from vk_api import VkApi
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import os
from dotenv import load_dotenv
from request_db import get_category, get_goods, get_price_good

load_dotenv()
GROUP_ID = os.getenv('GROUP_ID')
GROUP_TOKEN = os.getenv('SECRET_KEY')
API_VERSION = os.getenv('API_VERSION')


def generate_keyboard(get_db_info, type, butt_back=False, photo=None):
    keyboard = VkKeyboard(one_time=False, inline=True)
    for item in get_db_info:
        keyboard.add_callback_button(
            label=item['name'],
            color=VkKeyboardColor.POSITIVE,
            payload={"type": type, 'photo': item.get('photo'),
                     'name': item.get('name')},
        )
    if butt_back:
        keyboard.add_callback_button(
            "Назад",
            color=VkKeyboardColor.NEGATIVE,
            payload={"type": "back", 'photo': photo, 'name': 'back'},
        )
    return keyboard


def start_page_send(event, vk, name=None):
    photo = '457239027'
    vk.messages.send(
        user_id=event.obj.message["from_id"],
        random_id=get_random_id(),
        peer_id=event.obj.message["from_id"],
        keyboard=generate_keyboard([{'name': 'Выбор категорий'}],
                                   'category_page').get_keyboard(),
        message="Добро пожаловать !",
        attachment=f'photo-{GROUP_ID}_{photo}'
    )


def start_page_edit(event, vk, name=None):
    photo = '457239027'
    vk.messages.edit(
        conversation_message_id=event.obj.conversation_message_id,
        random_id=get_random_id(),
        peer_id=event.obj.peer_id,
        keyboard=generate_keyboard([{'name': 'Выбор категорий'}],
                                   'category_page').get_keyboard(),
        message="Добро пожаловать !",
        attachment=f'photo-{GROUP_ID}_{photo}'
    )


def goods_page(event, vk, name=None, last_photo=None):
    photo = event.obj['payload'].get('photo')
    if last_photo is not None:
        photo = last_photo
    get_db_info = get_goods(name)
    vk.messages.edit(
        peer_id=event.obj.peer_id,
        message="Выбор товаров",
        conversation_message_id=event.obj.conversation_message_id,
        keyboard=(generate_keyboard(get_db_info,
                                    'good_page',
                                    butt_back=True,
                                    photo=photo)).get_keyboard(),
        attachment=f'photo-{GROUP_ID}_{photo}'
    )


def good_page(event, vk, name=None, last_photo=None):
    photo = event.obj['payload'].get('photo')
    get_db_info = get_price_good(name)
    vk.messages.edit(
        peer_id=event.obj.peer_id,
        message=f"Описание:  {get_db_info[0]['discription']}",
        conversation_message_id=event.obj.conversation_message_id,
        keyboard=(generate_keyboard(get_db_info,
                                    'good_page',
                                    butt_back=True,
                                    photo=photo)).get_keyboard(),
        attachment=f'photo-{GROUP_ID}_{photo}'
    )


def category_page(event, vk, name=None, last_photo=None):
    photo = '457239031'
    get_db_info = get_category(name)
    vk.messages.edit(
        random_id=get_random_id(),
        peer_id=event.obj.peer_id,
        message="Выбор категории",
        conversation_message_id=event.obj.conversation_message_id,
        keyboard=generate_keyboard(get_db_info,
                                   'goods_page',
                                   photo=photo).get_keyboard(),
        attachment=f'photo-{GROUP_ID}_{photo}'
    )


def go_back(event, vk, state_cache):
    state_cache.pop()
    condition = state_cache[-1]
    page_view = condition['page_view']
    but_name = condition['but_name']
    last_photo = condition['but_photo']
    func = globals()[page_view]
    print(f'Start back view {condition}')
    func(event, vk, but_name, last_photo)


def chagne_status(state_cache, event):
    condition = {
        'but_name': event.object.payload.get('name', None),
        'but_photo': event.object.payload.get('photo', None),
        'page_view': event.object.payload.get('type', None)
    }
    state_cache.append(condition)
    but_name = event.object.payload.get('name', None)
    but_photo = event.object.payload.get('photo', None)
    type_view = event.object.payload.get('type', None)
    print('-' * 50)
    print(event.object.payload,
          f'button_name = {but_name},'
          f'button_photo = {but_photo},'
          f'type_view = {type_view}')
    print('-' * 50)
    return state_cache, but_name


def main():
    vk_session = VkApi(token=GROUP_TOKEN, api_version=API_VERSION)
    vk = vk_session.get_api()
    longpoll = VkBotLongPoll(vk_session, group_id=GROUP_ID)

    state_cache = []

    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            if event.obj.message["text"] != "":
                if event.from_user:
                    start_page_send(event, vk)
        elif event.type == VkBotEventType.MESSAGE_EVENT:
            if event.object.payload.get("type") == "back":
                go_back(event, vk, state_cache)
            elif event.object.payload.get("type") == 'category_page':
                state_cache, but_name = chagne_status(state_cache, event)
                category_page(event, vk, but_name)
            elif event.object.payload.get("type") == "goods_page":
                state_cache, but_name = chagne_status(state_cache, event)
                goods_page(event, vk, but_name)
            elif event.object.payload.get("type") == "good_page":
                state_cache, but_name = chagne_status(state_cache, event)
                good_page(event, vk, but_name)


if __name__ == "__main__":
    print('Bot run')
    main()
