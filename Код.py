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
"Роли"
ROLIFORBESEDA = {0: 'Житель',
                 1: 'Полицейский',
                 2: 'Детектив',
                 3: 'Министр',
                 4: 'Президент',
                 5: 'Бог'}
ROLIFORBESEDA2 = {'Житель': 0,
                 'Полицейский': 1,
                 'Детектив': 2,
                 'Министр': 3,
                 'Президент': 4,
                 'Бог': 5}
'Роли конец'
'bog'
bogid = 542650732
'bog'
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
import sqlite3


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



                    besedainfo = vk.messages.getConversationMembers(peer_id=2000000000+event.chat_id, random_id=random.randint(0, 2 ** 64))
                    users = besedainfo['profiles']
                    con = sqlite3.connect("groups.db")
                    cur = con.cursor()
                    checkbase = 'BESEDANUMBER'+str(event.chat_id) in cur.execute('''SELECT * FROM Sqlite_master WHERE type = "table"''').fetchall()[0] if cur.execute('''SELECT * FROM Sqlite_master WHERE type = "table"''').fetchall() else []
                    if checkbase:
                        pass
                    else:
                        result = cur.execute(f"""CREATE TABLE {'BESEDANUMBER'+str(event.chat_id)} (
ID int,
BANONOFF int,
STATUS int);""")
                        result = cur.execute(f'''INSERT INTO {'BESEDANUMBER'+str(event.chat_id)}(ID, BANONOFF, STATUS) VALUES({bogid}, 0, 5) ''')
                        con.commit()
                    blacklist = cur.execute(f'''SELECT ID FROM {'BESEDANUMBER'+str(event.chat_id)} WHERE BANONOFF=1''').fetchall()
                    con.close()
                    for i in users:
                        if i['id'] in [i[0] for i in blacklist] if blacklist else []:
                            vk.messages.removeChatUser(chat_id=int(event.chat_id),
                                                               user_id=i['id'],
                                                               random_id=random.randint(0, 2 ** 64))


                    
                    if x:
                        if x[:8] == '!мбповтори':
                            vk.messages.send(chat_id=int(event.chat_id),
                                             message=x[8:] if x[8:] else 'Вы не сказали что повторять!',
                                             random_id=random.randint(0, 2 ** 64))
                        elif x[:5] == '!мбкик ':
                            vk.messages.removeChatUser(chat_id=int(event.chat_id),
                                                       user_id=int(x[5:]),
                                                       random_id=random.randint(0, 2 ** 64))
                        elif x[:11] == '!мбмультикик ':
                            x = x[11:].split()
                            for i in x:
                                vk.messages.removeChatUser(chat_id=int(event.chat_id),
                                                           user_id=i,
                                                           random_id=random.randint(0, 2 ** 64))
                        elif x[:12] == '!мбдатьроль ':
                            x = x[12:].split()
                            numberrol = ROLIFORBESEDA2[x[0]]
                            con = sqlite3.connect("groups.db")
                            cur = con.cursor()
                            checkbase = 'BESEDANUMBER'+str(event.chat_id) in cur.execute('''SELECT * FROM Sqlite_master WHERE type = "table"''').fetchall()[0]
                            if checkbase:
                                pass
                            else:
                                result = cur.execute(f"""CREATE TABLE {'BESEDANUMBER'+str(event.chat_id)} (
ID int,
BANONOFF int,
STATUS int);""")
                                result = cur.execute(f'''INSERT INTO {'BESEDANUMBER'+str(event.chat_id)}(ID, BANONOFF, STATUS) VALUES({bogid}, 0, 5) ''')
                                con.commit()
                            if x[1] not in [i[0] for i in cur.execute('''SELECT ID FROM {'BESEDANUMBER'+str(event.chat_id)}''').fetchall()]:
                                result = cur.execute(f'''INSERT INTO {'BESEDANUMBER'+str(event.chat_id)}(ID, BANONOFF, STATUS) VALUES({int(x[1])}, 0, {numberrol}) ''')
                            else:
                                result = cur.execute(f'''UPDATE {'BESEDANUMBER'+str(event.chat_id)}
SET STATUS = {numberrol}
WHERE ID = {x[1]}''')
                            con.commit()
                            con.close()
                        elif x[:8] == '!мброль ':
                            x = x[8:]
                            con = sqlite3.connect("groups.db")
                            cur = con.cursor()
                            checkbase = 'BESEDANUMBER'+str(event.chat_id) in cur.execute('''SELECT * FROM Sqlite_master WHERE type = "table"''').fetchall()[0]
                            if checkbase:
                                pass
                            else:
                                result = cur.execute(f"""CREATE TABLE {'BESEDANUMBER'+str(event.chat_id)} (
ID int,
BANONOFF int,
STATUS int);""")
                                result = cur.execute(f'''INSERT INTO {'BESEDANUMBER'+str(event.chat_id)}(ID, BANONOFF, STATUS) VALUES({bogid}, 0, 5) ''')
                                con.commit()
                            result = cur.execute(f'''SELECT STATUS FROM {'BESEDANUMBER'+str(event.chat_id)} WHERE ID = {x}''').fetchall()
                            if result:
                                print(ROLIFORBESEDA[result[0][0]])
                                vk.messages.send(chat_id=int(event.chat_id),
                                             message=f'Роль {x}:' + ROLIFORBESEDA[result[0][0]],
                                             random_id=random.randint(0, 2 ** 64))
                        elif x[:7] == '!мббан ':
                            x = x[7:]
                            con = sqlite3.connect("groups.db")
                            cur = con.cursor()
                            checkbase = 'BESEDANUMBER'+str(event.chat_id) in cur.execute('''SELECT * FROM Sqlite_master WHERE type = "table"''').fetchall()[0]
                            if checkbase:
                                pass
                            else:
                                result = cur.execute(f"""CREATE TABLE {'BESEDANUMBER'+str(event.chat_id)} (
ID int,
BANONOFF int,
STATUS int);""")
                                result = cur.execute(f'''INSERT INTO {'BESEDANUMBER'+str(event.chat_id)}(ID, BANONOFF, STATUS) VALUES({bogid}, 0, 5) ''')
                                con.commit()
                            if x not in [i[0] for i in cur.execute(f'''SELECT ID FROM {'BESEDANUMBER'+str(event.chat_id)}''').fetchall()]:
                                result = cur.execute(f'''INSERT INTO {'BESEDANUMBER'+str(event.chat_id)}(ID, BANONOFF, STATUS) VALUES({int(x)}, 1, 0) ''')
                            else:
                                result = cur.execute(f'''UPDATE {'BESEDANUMBER'+str(event.chat_id)}
SET STATUS = 0,
BANONOFF = 1
WHERE ID = {x}''')
                            con.commit()
                            con.close()
                            vk.messages.removeChatUser(chat_id=int(event.chat_id),
                                                       user_id=int(x),
                                                       random_id=random.randint(0, 2 ** 64))
                            print('BAN!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                        elif x[:13] == '!мбмультибан ':
                            x = x[13:].split()
                            for i in x:
                                xi = i
                                con = sqlite3.connect("groups.db")
                                cur = con.cursor()
                                checkbase = 'BESEDANUMBER'+str(event.chat_id) in cur.execute(f'''SELECT * FROM Sqlite_master WHERE type = "table"''').fetchall()[0]
                                if checkbase:
                                    pass
                                else:
                                    result = cur.execute(f"""CREATE TABLE {'BESEDANUMBER'+str(event.chat_id)} (
    ID int,
    BANONOFF int,
    STATUS int);""")
                                    result = cur.execute(f'''INSERT INTO {'BESEDANUMBER'+str(event.chat_id)}(ID, BANONOFF, STATUS) VALUES({bogid}, 0, 5) ''')
                                    con.commit()
                                if xi not in [i[0] for i in cur.execute(f'''SELECT ID FROM {'BESEDANUMBER'+str(event.chat_id)}''').fetchall()]:
                                    result = cur.execute(f'''INSERT INTO {'BESEDANUMBER'+str(event.chat_id)}(ID, BANONOFF, STATUS) VALUES({int(xi)}, 1, 0) ''')
                                else:
                                    result = cur.execute(f'''UPDATE {'BESEDANUMBER'+str(event.chat_id)}
SET STATUS = 0,
BANONOFF = 1
WHERE ID = {xi}''')
                                con.commit()
                                con.close()
                                vk.messages.removeChatUser(chat_id=int(event.chat_id),
                                                           user_id=int(xi),
                                                           random_id=random.randint(0, 2 ** 64))
                                print('BAN!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                        elif x[:10] == '!мбразбан ':
                            x = x[10:]
                            con = sqlite3.connect("groups.db")
                            cur = con.cursor()
                            checkbase = 'BESEDANUMBER'+str(event.chat_id) in cur.execute(f'''SELECT * FROM Sqlite_master WHERE type = "table"''').fetchall()[0]
                            if checkbase:
                                pass
                            else:
                                result = cur.execute(f"""CREATE TABLE {'BESEDANUMBER'+str(event.chat_id)} (
ID int,
BANONOFF int,
STATUS int);""")
                                result = cur.execute(f'''INSERT INTO {'BESEDANUMBER'+str(event.chat_id)}(ID, BANONOFF, STATUS) VALUES({bogid}, 0, 5) ''')
                                con.commit()
                            result = cur.execute(f'''UPDATE {'BESEDANUMBER'+str(event.chat_id)}
SET STATUS = 0,
BANONOFF = 0
WHERE ID = {x}''')
                            con.commit()
                            con.close()
                        elif x[:17] == '!мбайдиучастников':
                            besedainfo = vk.messages.getConversationMembers(peer_id=2000000000+event.chat_id, random_id=random.randint(0, 2 ** 64))
                            users = besedainfo['profiles']
                            for i in users:
                                print(i['first_name'] + ' ' + i['last_name'], 'first_id:'+str(i['id']), 'second_id:'+i['screen_name'], 'Online:'+str(bool(i['online'])), sep='\n')
                                vk.messages.send(chat_id=int(event.chat_id),
                                             message='\n'.join([i['first_name'] + ' ' + i['last_name'], 'first_id:'+str(i['id']), 'second_id:'+i['screen_name'], 'Online:'+str(bool(i['online']))]),
                                             random_id=random.randint(0, 2 ** 64))
                        
                        elif x[:3]=='!мб':
                            vk.messages.send(chat_id=int(event.chat_id),
                                             message='Не знаю такой команды(',
                                             random_id=random.randint(0, 2 ** 64))
        except vk_api.exceptions.ApiError:
            
            vk.messages.send(chat_id=int(event.chat_id),
                                             message='Низзя!',
                                             random_id=random.randint(0, 2 ** 64))
        except ValueError:
            pass

        #
        
