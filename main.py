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


def generate_keyboard(table_name, type, butt_back = False):
    keyboard = VkKeyboard(one_time=False, inline=True)
    db = {
        'category' : get_category(),
        'goods' : get_goods(1)
    }
    table = db[table_name]
    for object in table:
        keyboard.add_callback_button(
            label=object['name'],
            color=VkKeyboardColor.POSITIVE ,
            payload={"type": type},
        )
    if butt_back:
        keyboard.add_callback_button(
        "Назад",
        color=VkKeyboardColor.NEGATIVE,
        payload={"type": "back"},
    )
    return keyboard

def start_page(event, vk, message_id=None, new_event=False):
    if new_event:
        vk.messages.edit(
            random_id=get_random_id(),
            peer_id=event.obj.peer_id,
            message="Добро пожаловать !",
            conversation_message_id=event.obj.conversation_message_id,
            keyboard=generate_keyboard('category', 'go_goods',).get_keyboard(),
            attachment=f'photo-{GROUP_ID}_457239027'
        )
    else:
        vk.messages.send(
            user_id=event.obj.message["from_id"],
            random_id=get_random_id(),
            peer_id=event.obj.message["from_id"],
            keyboard=generate_keyboard('category', 'go_goods',).get_keyboard(),
            message="Добро пожаловать !",
            attachment=f'photo-{GROUP_ID}_457239027'
        )

def goods_page(event, vk, goods_page=True, photo=False):
    if photo:
            vk.messages.send(
            peer_id=event.obj.peer_id,
            message="товары",
            conversation_message_id=event.obj.conversation_message_id,
            attachment='photo-210104217_457239025',
            keyboard=(generate_keyboard('goods', 'get_photo', butt_back=True)).get_keyboard(),
        )
    else: vk.messages.edit(
            peer_id=event.obj.peer_id,
            message="товары",
            conversation_message_id=event.obj.conversation_message_id,
            keyboard=(generate_keyboard('goods', 'get_photo', butt_back=True)).get_keyboard(),
        )


def main():
    # Запускаем бот
    vk_session = VkApi(token=GROUP_TOKEN, api_version=API_VERSION)
    vk = vk_session.get_api()
    longpoll = VkBotLongPoll(vk_session, group_id=GROUP_ID)

    # message_id = None

    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            if event.obj.message["text"] != "":
                if event.from_user:
                    start_page(event, vk)
                    # message_id = event.obj.message["id"]
        elif event.type == VkBotEventType.MESSAGE_EVENT:
            if event.object.payload.get("type") in ['back']:
                start_page(event, vk, new_event=True)
            elif event.object.payload.get("type") in ["go_goods"]:
                goods_page(event, vk)
            elif event.object.payload.get("type") == "get_photo":
                goods_page(event, vk, True)


if __name__ == "__main__":
    print('Bot run')
    main()
