'''import vk_api


def main():
    login, password = 'tae1982@yandex.ru', 'Utjhubq2311'
    vk_session = vk_api.VkApi(login, password)
    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return
    vk = vk_session.get_api()
    # Используем метод wall.get
    response = vk.wall.get(count=3, offset=1)
    if response['items']:
        for i in response['items']:
            print(i['text'])
            print(i['copy_history'][0]['text'])
            print('-----------------------------------------------------')


if __name__ == '__main__':
    main()
'''
"""
    MESSAGE_NEW = 'message_new'
    MESSAGE_REPLY = 'message_reply'
    MESSAGE_EDIT = 'message_edit'
    MESSAGE_TYPING_STATE = 'message_typing_state'
    MESSAGE_ALLOW = 'message_allow'
    MESSAGE_DENY = 'message_deny'
    PHOTO_NEW = 'photo_new'
    PHOTO_COMMENT_NEW = 'photo_comment_new'
    PHOTO_COMMENT_EDIT = 'photo_comment_edit'
    PHOTO_COMMENT_RESTORE = 'photo_comment_restore'
    PHOTO_COMMENT_DELETE = 'photo_comment_delete'
    AUDIO_NEW = 'audio_new'
    VIDEO_NEW = 'video_new'
    VIDEO_COMMENT_NEW = 'video_comment_new'
    VIDEO_COMMENT_EDIT = 'video_comment_edit'
    VIDEO_COMMENT_RESTORE = 'video_comment_restore'
    VIDEO_COMMENT_DELETE = 'video_comment_delete'
    WALL_POST_NEW = 'wall_post_new'
    WALL_REPOST = 'wall_repost'
    WALL_REPLY_NEW = 'wall_reply_new'
    WALL_REPLY_EDIT = 'wall_reply_edit'
    WALL_REPLY_RESTORE = 'wall_reply_restore'
    WALL_REPLY_DELETE = 'wall_reply_delete'
    BOARD_POST_NEW = 'board_post_new'
    BOARD_POST_EDIT = 'board_post_edit'
    BOARD_POST_RESTORE = 'board_post_restore'
    BOARD_POST_DELETE = 'board_post_delete'
    MARKET_COMMENT_NEW = 'market_comment_new'
    MARKET_COMMENT_EDIT = 'market_comment_edit'
    MARKET_COMMENT_RESTORE = 'market_comment_restore'
    MARKET_COMMENT_DELETE = 'market_comment_delete'
    GROUP_LEAVE = 'group_leave'
    GROUP_JOIN = 'group_join'
    USER_BLOCK = 'user_block'
    USER_UNBLOCK = 'user_unblock'
    POLL_VOTE_NEW = 'poll_vote_new'
    GROUP_OFFICERS_EDIT = 'group_officers_edit'
    GROUP_CHANGE_SETTINGS = 'group_change_settings'
    GROUP_CHANGE_PHOTO = 'group_change_photo'
    VKPAY_TRANSACTION = 'vkpay_transaction'
"""
'193996085-,jn'
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random


if __name__ == '__main__':
    while 1:
        try:
            vk_session = vk_api.VkApi(
                token='5b0326f036d243d4d08f827d12a3a1a04a28a39c820905e72c71b95286c124e408924571449b6afb5f866')
            vk = vk_session.get_api()
            longpoll = VkBotLongPoll(vk_session,'193996085')

            for event in longpoll.listen():

                if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat:
                    print(event)
                    print('Новое сообщение:')
                    print('Для меня от:', event.obj.message['from_id'])
                    print('Текст:', event.obj.message['text'])
                    x = event.obj.message['text']
                    
                    if x:
                        if x[:8] == '!повтори':
                            vk.messages.send(chat_id=int(event.chat_id),
                                             message=x[8:] if x[8:] else 'Вы не сказали что повторять!',
                                             random_id=random.randint(0, 2 ** 64))
                        elif x[:5] == '!бан ':
                            vk.messages.removeChatUser(chat_id=int(event.chat_id),
                                                       user_id=int(x[5:]),
                                                       random_id=random.randint(0, 2 ** 64))
                        elif x[:11] == '!мультибан ':
                            x = x[11:].split()
                            for i in x:
                                vk.messages.removeChatUser(chat_id=int(event.chat_id),
                                                           user_id=i,
                                                           random_id=random.randint(0, 2 ** 64))
                        elif x[0]=='!':
                            vk.messages.send(chat_id=int(event.chat_id),
                                             message='Не знаю такой команды(',
                                             random_id=random.randint(0, 2 ** 64))
                elif event.type == VkBotEventType.MESSAGE_NEW:
                    print(event)
                    print('Новое сообщение:')
                    print('Для меня от:', event.obj.message['from_id'])
                    print('Текст:', event.obj.message['text'])
                    x = event.obj.message['text']
                    
                    if x:
                        if x[:8] == '!повтори':
                            vk.messages.send(user_id=event.obj.message['from_id'],
                                             message=x[8:] if x[8:] else 'Вы не сказали что повторять!',
                                             random_id=random.randint(0, 2 ** 64))
                        elif x[0]=='!':
                            vk.messages.send(user_id=event.obj.message['from_id'],
                                             message='Не знаю такой команды(',
                                             random_id=random.randint(0, 2 ** 64))
        except vk_api.exceptions.ApiError:
            vk.messages.send(chat_id=int(event.chat_id),
                                             message='Низзя!',
                                             random_id=random.randint(0, 2 ** 64))
        except ValueError:
            pass
