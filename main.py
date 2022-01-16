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

last_photo = None

def get_lol(*arqs):
    return [{'name' : 'Выбор категорий'}]

def generate_keyboard(table_name, type, butt_back = False, name=None, last_photo=None):
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
            payload={"type": type, 'photo': item.get('photo'), 'name': item.get('name'), 'category_id': item.get('id')},
        )
    if butt_back:
        keyboard.add_callback_button(
        "Назад",
        color=VkKeyboardColor.NEGATIVE,
        payload={"type": "back", 'photo': last_photo},
    )
    return keyboard


def start_page_send(event, vk, name=None):
    photo = '457239027'
    vk.messages.send(
        user_id=event.obj.message["from_id"],
        random_id=get_random_id(),
        peer_id=event.obj.message["from_id"],
        keyboard=generate_keyboard('start_page', 'go_category',).get_keyboard(),
        message="Добро пожаловать !",
        attachment=f'photo-{GROUP_ID}_{photo}'
    )

def start_page_edit(event, vk, name=None):
    photo = '457239027'
    vk.messages.edit(
        conversation_message_id=event.obj.conversation_message_id,
        random_id=get_random_id(),
        peer_id=event.obj.peer_id,
        keyboard=generate_keyboard('start_page', 'go_category',).get_keyboard(),
        message="Добро пожаловать !",
        attachment=f'photo-{GROUP_ID}_{photo}'
    )

def goods_page(event, vk, name=None):
    photo = event.obj['payload'].get('photo')
    if photo is None:
        photo = last_photo
    vk.messages.edit(
        peer_id=event.obj.peer_id,
        message="Выбор товаров",
        conversation_message_id=event.obj.conversation_message_id,
        keyboard=(generate_keyboard('goods', 'get_photo', butt_back=True, name=name)).get_keyboard(),
        attachment=f'photo-{GROUP_ID}_{photo}'
    )

def view_good_page(event, vk, name=None):
    photo = event.obj['payload'].get('photo')
    print(f'GOOD PHOTO !!!!!!!!! {photo}')
    vk.messages.edit(
    peer_id=event.obj.peer_id,
    message="Это товар",
    conversation_message_id=event.obj.conversation_message_id,
    keyboard=(generate_keyboard('good', 'go_goods', butt_back=True, name=name)).get_keyboard(),
    attachment=f'photo-{GROUP_ID}_{photo}'
    )
    
def category_page(event, vk, name=None):
    photo = '457239031'
    vk.messages.edit(
        random_id=get_random_id(),
        peer_id=event.obj.peer_id,
        message="Выбор категории",
        conversation_message_id=event.obj.conversation_message_id,
        keyboard=generate_keyboard('category', 'go_goods', butt_back=True, name=name).get_keyboard(),
        attachment=f'photo-{GROUP_ID}_{photo}'
    )


states = {
    'start_page_send': None,
    'category_page': 'start_page_edit',
    'goods_page': 'category_page',
    'good_page': 'goods_page',
    }

def go_back(event, vk, condition):
    func = globals()[states[condition]]
    condition = states[condition]
    func(event, vk)
    return condition

def main():
    vk_session = VkApi(token=GROUP_TOKEN, api_version=API_VERSION)
    vk = vk_session.get_api()
    longpoll = VkBotLongPoll(vk_session, group_id=GROUP_ID)

    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            condition = None
            if event.obj.message["text"] != "":
                if event.from_user:
                    condition = 'start_page'
                    start_page_send(event, vk)
        elif event.type == VkBotEventType.MESSAGE_EVENT:
            but_name = event.object.payload.get('name', None)
            but_photo = event.object.payload.get('photo', None)
            if but_photo is not None:
                global last_photo
                last_photo = but_photo
            category_id = event.object.payload.get('category_id', None)
            print('-'*50)
            print(event.object.payload,  f'button_name = {but_name} , button_photo = {but_photo}, category_id = {category_id}, last_photo = {last_photo}')
            print('-'*50)
            if event.object.payload.get("type") == 'go_category':
                condition = 'category_page'
                category_page(event, vk, but_name)
            elif event.object.payload.get("type") == "go_goods":
                condition = 'goods_page'
                goods_page(event, vk, but_name)
            elif event.object.payload.get("type") == "get_photo":
                condition = 'good_page'
                view_good_page(event, vk, but_name)
            elif event.object.payload.get("type") == "back":
                condition = go_back(event, vk, condition)



if __name__ == "__main__":
    print('Bot run')
    main()
