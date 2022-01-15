from email import message
from vk_api import VkApi
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import os, vk_api, json
from dotenv import load_dotenv
from word_db import get_category, get_goods


load_dotenv()
GROUP_ID = '210104217'
GROUP_TOKEN = os.getenv('SECRET_KEY')
API_VERSION = '5.131'
DB_MYSCL = {'admin': 22081991, 'data_base': 'VK_BOT'}

condition = None
# name = None
category_id = None

def get_info(object):
    name = object.get('name')
    category_id = object.get('id')

def generate_keyboard(table_name, type, butt_back = False, name=None):
    keyboard = VkKeyboard(one_time=False, inline=True)
    db = {
        'category' : get_category(),
        'goods' : get_goods(1),
        'start_page' : [{'name' : 'Выбор категорий'}],
        'good' : [{'name' : 'Заказать'}]
    }
    table = db[table_name]
    for object in table:
        get_info(object)
        print( f"photo : {object.get('photo')}")
        keyboard.add_callback_button(
            label=object['name'],
            color=VkKeyboardColor.POSITIVE ,
            payload={"type": type, 'photo': object.get('photo'), 'name': object.get('name'), 'category_id': object.get('id')},
        )
    if butt_back:
        keyboard.add_callback_button(
        "Назад",
        color=VkKeyboardColor.NEGATIVE,
        payload={"type": "back", 'photo': object.get('photo')},
    )
    return keyboard

def start_page_send(event, vk):
    vk.messages.send(
        user_id=event.obj.message["from_id"],
        random_id=get_random_id(),
        peer_id=event.obj.message["from_id"],
        keyboard=generate_keyboard('start_page', 'go_category',).get_keyboard(),
        message="Добро пожаловать !",
        attachment=f'photo-{GROUP_ID}_457239027'
    )

def start_page_edit(event, vk):
    #  photo = event.obj['payload'].get('photo')
     vk.messages.edit(
        conversation_message_id=event.obj.conversation_message_id,
        random_id=get_random_id(),
        peer_id=event.obj.peer_id,
        keyboard=generate_keyboard('start_page', 'go_category',).get_keyboard(),
        message="Добро пожаловать !",
        attachment=f'photo-{GROUP_ID}_457239027'
    )

def goods_page(event, vk):
    photo = event.obj['payload'].get('photo')
    vk.messages.edit(
    peer_id=event.obj.peer_id,
    message="Выбор товаров",
    conversation_message_id=event.obj.conversation_message_id,
    keyboard=(generate_keyboard('goods', 'get_photo', butt_back=True)).get_keyboard(),
    attachment=f'photo-{GROUP_ID}_{photo}'
    )

def view_good_page(event, vk):
    photo = event.obj['payload'].get('photo')
    vk.messages.edit(
    peer_id=event.obj.peer_id,
    message="Это товар",
    conversation_message_id=event.obj.conversation_message_id,
    keyboard=(generate_keyboard('good', 'go_goods', butt_back=True)).get_keyboard(),
    attachment=f'photo-{GROUP_ID}_{photo}'
    )
    
def category_page(event, vk):
    vk.messages.edit(
        random_id=get_random_id(),
        peer_id=event.obj.peer_id,
        message="Выбор категории",
        conversation_message_id=event.obj.conversation_message_id,
        keyboard=generate_keyboard('category', 'go_goods', butt_back=True, name=None).get_keyboard(),
        attachment=f'photo-{GROUP_ID}_457239031'
    )

# def go_back(event, vk, condition):
#     print(condition)
#     func = globals()[condition]
    
#     return func(event, vk)

states = {
    'start_page_send': None,
    'category_page': 'start_page_edit',
    'goods_page': 'category_page',
    'good_page': 'goods_page',
    }

def go_back(event, vk, condition):
    print(f'Go to func {states[condition]}')
    func = globals()[states[condition]]
    condition = states[condition]
    print(f'Go back func {func(event, vk)}')
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
            if event.object.payload.get("type") == 'go_category':
                condition = 'category_page'
                category_page(event, vk)
            elif event.object.payload.get("type") == "go_goods":
                condition = 'goods_page'
                goods_page(event, vk)
            elif event.object.payload.get("type") == "get_photo":
                condition = 'good_page'
                view_good_page(event, vk)
            elif event.object.payload.get("type") == "back":
                condition = go_back(event, vk, condition)
        # print(f'Status: {condition}')
        print('-'*50)
        print(event.object.payload)
        print('-'*50)


if __name__ == "__main__":
    print('Bot run')
    main()
