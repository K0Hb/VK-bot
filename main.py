from email import message
from vk_api import VkApi
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import os, vk_api, json
from dotenv import load_dotenv
from word_db import get_category, get_goods, get_price_good


load_dotenv()
GROUP_ID = '210104217'
GROUP_TOKEN = os.getenv('SECRET_KEY')
API_VERSION = '5.131'
DB_MYSCL = {'admin': 22081991, 'data_base': 'VK_BOT'}

# but_name = None
# but_photo = None
# last_name = None
# last_photo = None

def get_lol(*arqs):
    return [{'name' : 'Выбор категорий'}]

def generate_keyboard(table_name, type, butt_back = False, name=None, photo=None):
    keyboard = VkKeyboard(one_time=False, inline=True)

    def request_db(table_name):
        db = {
            'category' : 'get_category',
            'goods' : 'get_goods',
            'start_page' : 'get_lol',
            'good' : 'get_price_good',
        }
        func = globals()[db[table_name]]
        result = func(name)
        return result
    table = request_db(table_name)
    for item in table:
        keyboard.add_callback_button(
            label=item['name'],
            color=VkKeyboardColor.POSITIVE ,
            payload={"type": type, 'photo': item.get('photo'), 'name': item.get('name')},
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
        keyboard=generate_keyboard('start_page', 'category_page',).get_keyboard(),
        message="Добро пожаловать !",
        attachment=f'photo-{GROUP_ID}_{photo}'
    )

def start_page_edit(event, vk, name=None):
    photo = '457239027'
    vk.messages.edit(
        conversation_message_id=event.obj.conversation_message_id,
        random_id=get_random_id(),
        peer_id=event.obj.peer_id,
        keyboard=generate_keyboard('start_page', 'category_page',).get_keyboard(),
        message="Добро пожаловать !",
        attachment=f'photo-{GROUP_ID}_{photo}'
    )

def goods_page(event, vk, name=None, last_photo=None):
    photo = event.obj['payload'].get('photo')
    vk.messages.edit(
        peer_id=event.obj.peer_id,
        message="Выбор товаров",
        conversation_message_id=event.obj.conversation_message_id,
        keyboard=(generate_keyboard('goods', 'good_page', butt_back=True, name=name, photo=photo)).get_keyboard(),
        attachment=f'photo-{GROUP_ID}_{photo}'
    )

def good_page(event, vk, name=None):
    photo = event.obj['payload'].get('photo')
    vk.messages.edit(
    peer_id=event.obj.peer_id,
    message="Это товар",
    conversation_message_id=event.obj.conversation_message_id,
    keyboard=(generate_keyboard('good', 'good_page', butt_back=True, name=name, photo=photo)).get_keyboard(),
    attachment=f'photo-{GROUP_ID}_{photo}'
    )
    
def category_page(event, vk, name=None, last_photo=None):
    photo = '457239031'
    vk.messages.edit(
        random_id=get_random_id(),
        peer_id=event.obj.peer_id,
        message="Выбор категории",
        conversation_message_id=event.obj.conversation_message_id,
        keyboard=generate_keyboard('category', 'goods_page', name=name, photo=photo).get_keyboard(),
        attachment=f'photo-{GROUP_ID}_{photo}'
    )


states = {
    'start_page_send': None,
    'category_page': 'start_page_edit',
    'goods_page': 'category_page',
    'good_page': 'goods_page',
    }

def go_back(event, vk, state_cache):
    state_cache.pop()
    condition = state_cache[-1]
    page_view = condition['page_view']
    but_name = condition['but_name']
    func = globals()[page_view]
    print(f'Start back view {condition}')
    func(event, vk, but_name)

def chagne_status(state_cache, event):
    condition = {
        'but_name' : event.object.payload.get('name', None),
        'but_photo' : event.object.payload.get('photo', None),
        'page_view' : event.object.payload.get('type', None)
    }
    state_cache.append(condition)
    but_name = event.object.payload.get('name', None)
    but_photo = event.object.payload.get('photo', None)
    type_view = event.object.payload.get('type', None)
    print('-'*50)
    print(event.object.payload,  f'button_name = {but_name}, button_photo = {but_photo}, type_view = {type_view}')
    print('-'*50)
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
