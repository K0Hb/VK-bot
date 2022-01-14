from vk_api import VkApi
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import os, vk_api, json
from dotenv import load_dotenv
from word_db import connect_to_database


load_dotenv()
GROUP_ID = '210104217'
GROUP_TOKEN = os.getenv('SECRET_KEY')
API_VERSION = '5.131'
DB_MYSCL = {'admin': 22081991, 'data_base': 'VK_BOT'}

def main():
    # Запускаем бот
    vk_session = VkApi(token=GROUP_TOKEN, api_version=API_VERSION)
    vk = vk_session.get_api()
    longpoll = VkBotLongPoll(vk_session, group_id=GROUP_ID)

    # Создаем клавиатуру
    keyboard_1 = VkKeyboard(one_time=False, inline=True)
    categor_db = connect_to_database()
    for category in categor_db:
        keyboard_1.add_callback_button(
            label=category['name'],
            color=VkKeyboardColor.POSITIVE ,
            payload={"type": "custom", "text": "Это исчезающее сообщение на экране"},
        )

    keyboard_2 = VkKeyboard(one_time=False, inline=True)
    keyboard_2.add_callback_button(
            label='new_button',
            color=VkKeyboardColor.POSITIVE ,
            payload={"type": "custom", "text": "Это исчезающее сообщение на экране"},
        )
    keyboard_2.add_callback_button(
        "Назад",
        color=VkKeyboardColor.NEGATIVE,
        payload={"type": "custom"},
    )


    f_toggle: bool = False
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            if event.obj.message["text"] != "":
                if event.from_user:
                    vk.messages.send(
                        user_id=event.obj.message["from_id"],
                        random_id=get_random_id(),
                        peer_id=event.obj.message["from_id"],
                        keyboard=keyboard_1.get_keyboard(),
                        message="Добро пожаловать !",
                    )
        elif event.type == VkBotEventType.MESSAGE_EVENT:
            if event.object.payload.get("type") == "custom":
                 last_id = vk.messages.edit(
                    peer_id=event.obj.peer_id,
                    message="Меню #2",
                    conversation_message_id=event.obj.conversation_message_id,
                    keyboard=(keyboard_1 if f_toggle else keyboard_2).get_keyboard(),
                )
            f_toggle = not f_toggle


if __name__ == "__main__":
    main()
