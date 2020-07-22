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
god_id = int(open('Пароли явки.txt', 'r').read().split()[1])
NAMETABLE = open('Пароли явки.txt', 'r').read().split()[0]
BotOperationFlag = 1
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
import sqlite3


def AccessCheck(idkto, dannonbeseda, nf, idob=False, gforrol=False):
    con = sqlite3.connect(NAMETABLE)
    cur = con.cursor()
    rol = cur.execute(f'''SELECT STATUS FROM {dannonbeseda} WHERE ID = {idkto}''').fetchall()
    if rol:
        rol = rol[0][0]
    else:
        rol = 0
    rol2 = cur.execute(f'''SELECT STATUS FROM {dannonbeseda} WHERE ID = {idob}''').fetchall()[0][0] if idob else -1000
    con.close()
    if rol > rol2:
        if nf == 1:
            return True
        elif nf == 2:
            return True if rol >= 1 else False
        elif nf == 3:
            return True if rol >= 2 else False
        elif nf == 4:
            return True if gforrol < rol else False
        elif nf == 5:
            return True if rol >= 2 else False
        elif nf == 6:
            return True if rol >= 2 else False
        elif nf == 7:
            return True if rol >= 3 else False
        elif nf == 8:
            return True if rol >= 2 else False
        elif nf == 9:
            return True if rol >= 3 else False
        elif nf == 10:
            return True if rol >= 1 else False
        elif nf == 11:
            return True if rol >= 4 else False
        elif nf == 12:
            return True if rol >= 4 else False
    else:
        return False


if __name__ == '__main__':
    while 1:
        try:
            if BotOperationFlag:
                vk_session = vk_api.VkApi(
                    token='5b0326f036d243d4d08f827d12a3a1a04a28a39c820905e72c71b95286c124e408924571449b6afb5f866')
                vk = vk_session.get_api()
                longpoll = VkBotLongPoll(vk_session,'193996085')
                for event in longpoll.listen():

                    if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat:
                        print('Новое сообщение:')
                        print('Для меня от:', event.obj.message['from_id'])
                        print('Текст:', event.obj.message['text'])
                        textmessage = event.obj.message['text']
                        besedainfo = vk.messages.getConversationMembers(peer_id=2000000000+event.chat_id, random_id=random.randint(0, 2 ** 64))
                        users = besedainfo['profiles']
                        con = sqlite3.connect(NAMETABLE)
                        cur = con.cursor()
                        checkbase = 'BESEDANUMBER'+str(event.chat_id) in [j for i in cur.execute('''SELECT * FROM Sqlite_master WHERE type = "table"''').fetchall() for j in i] if cur.execute('''SELECT * FROM Sqlite_master WHERE type = "table"''').fetchall() else []
                        if checkbase:
                            pass
                        else:
                            result = cur.execute(f"""CREATE TABLE {'BESEDANUMBER'+str(event.chat_id)} (
    ID int,
    BANONOFF int,
    STATUS int,
    WARNINGS int);""")
                            result = cur.execute(f'''INSERT INTO {'BESEDANUMBER'+str(event.chat_id)}(ID, BANONOFF, STATUS, WARNINGS) VALUES({god_id}, 0, 5, -100000000000000000000000) ''')
                            con.commit()
                        blacklist = cur.execute(f'''SELECT ID FROM {'BESEDANUMBER'+str(event.chat_id)} WHERE BANONOFF=1''').fetchall()
                        con.close()
                        for i in users:
                            con = sqlite3.connect(NAMETABLE)
                            cur = con.cursor()
                            if i['id'] not in [i[0] for i in cur.execute(f'''SELECT ID FROM {'BESEDANUMBER'+str(event.chat_id)}''').fetchall()]:
                                result = cur.execute(f'''INSERT INTO {'BESEDANUMBER'+str(event.chat_id)}(ID, BANONOFF, STATUS, WARNINGS) VALUES({int(i['id'])}, 0, 0, 0) ''')
                                con.commit()
                            m = cur.execute(f'''SELECT WARNINGS FROM {'BESEDANUMBER'+str(event.chat_id)} WHERE ID = {i['id']}''').fetchall()[0][0]
                            con.commit()
                            con.close()
                            if (i['id'] in [i[0] for i in blacklist] if blacklist else []):
                                vk.messages.removeChatUser(chat_id=int(event.chat_id),
                                                                   user_id=i['id'],
                                                                   random_id=random.randint(0, 2 ** 64))
                            if m == 3:
                                vk.messages.removeChatUser(chat_id=int(event.chat_id),
                                                                   user_id=i['id'],
                                                                   random_id=random.randint(0, 2 ** 64))
                                con = sqlite3.connect(NAMETABLE)
                                cur = con.cursor()
                                result = cur.execute(f'''UPDATE {'BESEDANUMBER'+str(event.chat_id)}
    SET WARNINGS = 2
    WHERE ID = {i['id']}''')
                                con.commit()
                                con.close()


                        
                        if textmessage:
                            if textmessage[:3] != '!мб':
                                pass
                            elif textmessage[:10] == '!мбповтори':#проверка , какая именно поступила команда
                                vk.messages.send(chat_id=int(event.chat_id),
                                                 message=textmessage[10:] if textmessage[10:] else 'Вы не сказали что повторять!',
                                                 random_id=random.randint(0, 2 ** 64))
                            elif textmessage[:5] == '!мбкик ':#2
                                if AccessCheck(event.obj.message['from_id'], 'BESEDANUMBER'+str(event.chat_id), 2, idob=int(textmessage[5:])):
                                    vk.messages.removeChatUser(chat_id=int(event.chat_id),
                                                               user_id=int(textmessage[5:]),
                                                               random_id=random.randint(0, 2 ** 64))
                                else:
                                    print(1 + 'b')#вызов ошибки, при которой напишется в беседу что прав недостаточно
                            elif textmessage[:11] == '!мбмультикик ':#3
                                if AccessCheck(event.obj.message['from_id'], 'BESEDANUMBER'+str(event.chat_id), 3):
                                    textmessage = textmessage[11:].split()
                                    for i in textmessage:
                                        if AccessCheck(event.obj.message['from_id'], 'BESEDANUMBER'+str(event.chat_id), 2, idob=i):
                                            vk.messages.removeChatUser(chat_id=int(event.chat_id),
                                                                       user_id=i,
                                                                       random_id=random.randint(0, 2 ** 64))
                                        else:
                                            print(1 + 'b')
                                else:
                                    print(1 + 'b')
                            elif textmessage[:12] == '!мбдатьроль ':#4
                                textmessage = textmessage[12:].split()
                                numberrol = ROLIFORBESEDA2[textmessage[0]]
                                con = sqlite3.connect(NAMETABLE)
                                cur = con.cursor()
                                checkbase = 'BESEDANUMBER'+str(event.chat_id) in [j for i in cur.execute(f'''SELECT * FROM Sqlite_master WHERE type = "table"''').fetchall() for j in i]
                                if checkbase:
                                    pass
                                else:
                                    result = cur.execute(f"""CREATE TABLE {'BESEDANUMBER'+str(event.chat_id)} (
    ID int,
    BANONOFF int,
    STATUS int,
    WARNINGS int);""")
                                    result = cur.execute(f'''INSERT INTO {'BESEDANUMBER'+str(event.chat_id)}(ID, BANONOFF, STATUS, WARNINGS) VALUES({god_id}, 0, 5, -100000000000000000000000) ''')
                                    con.commit()
                                if AccessCheck(event.obj.message['from_id'], 'BESEDANUMBER'+str(event.chat_id), 4, gforrol=numberrol):
                                    print('Yes')
                                    if int(textmessage[1]) not in [i[0] for i in cur.execute(f'''SELECT ID FROM {'BESEDANUMBER'+str(event.chat_id)}''').fetchall()]:
                                        print('New')
                                        result = cur.execute(f'''INSERT INTO {'BESEDANUMBER'+str(event.chat_id)}(ID, BANONOFF, STATUS, WARNINGS) VALUES({int(textmessage[1])}, 0, {numberrol}, 0) ''')
                                    else:
                                        print('Old')
                                        result = cur.execute(f'''UPDATE {'BESEDANUMBER'+str(event.chat_id)}
        SET STATUS = {numberrol}
        WHERE ID = {x[1]}''')
                                    con.commit()
                                    con.close()
                                else:
                                    con.close()
                                    print(1 + 'b')
                            elif textmessage[:8] == '!мброль ':#5
                                textmessage = textmessage[8:]
                                con = sqlite3.connect(NAMETABLE)
                                cur = con.cursor()
                                checkbase = 'BESEDANUMBER'+str(event.chat_id) in [j for i in cur.execute(f'''SELECT * FROM Sqlite_master WHERE type = "table"''').fetchall() for j in i]
                                if checkbase:
                                    pass
                                else:
                                    result = cur.execute(f"""CREATE TABLE {'BESEDANUMBER'+str(event.chat_id)} (
    ID int,
    BANONOFF int,
    STATUS int,
    WARNINGS int);""")
                                    result = cur.execute(f'''INSERT INTO {'BESEDANUMBER'+str(event.chat_id)}(ID, BANONOFF, STATUS, WARNINGS) VALUES({god_id}, 0, 5, -100000000000000000000000) ''')
                                    con.commit()
                                if AccessCheck(event.obj.message['from_id'], 'BESEDANUMBER'+str(event.chat_id), 5):
                                    result = cur.execute(f'''SELECT STATUS FROM {'BESEDANUMBER'+str(event.chat_id)} WHERE ID = {textmessage}''').fetchall()
                                    if result:
                                        print(ROLIFORBESEDA[result[0][0]])
                                        vk.messages.send(chat_id=int(event.chat_id),
                                                     message=f'Роль {textmessage}:\n' + ROLIFORBESEDA[result[0][0]],
                                                     random_id=random.randint(0, 2 ** 64))
                                    con.close()
                                else:
                                    con.close()
                                    print(1 + 'b')
                            elif textmessage[:7] == '!мббан ':#6
                                textmessage = textmessage[7:]
                                con = sqlite3.connect(NAMETABLE)
                                cur = con.cursor()
                                checkbase = 'BESEDANUMBER'+str(event.chat_id) in [j for i in cur.execute(f'''SELECT * FROM Sqlite_master WHERE type = "table"''').fetchall() for j in i]
                                if checkbase:
                                    pass
                                else:
                                    result = cur.execute(f"""CREATE TABLE {'BESEDANUMBER'+str(event.chat_id)} (
    ID int,
    BANONOFF int,
    STATUS int,
    WARNINGS int);""")
                                    result = cur.execute(f'''INSERT INTO {'BESEDANUMBER'+str(event.chat_id)}(ID, BANONOFF, STATUS, WARNINGS) VALUES({god_id}, 0, 5, -100000000000000000000000) ''')
                                    con.commit()
                                if AccessCheck(event.obj.message['from_id'], 'BESEDANUMBER'+str(event.chat_id), 6, idob=x):
                                    if textmessage not in [i[0] for i in cur.execute(f'''SELECT ID FROM {'BESEDANUMBER'+str(event.chat_id)}''').fetchall()]:
                                        result = cur.execute(f'''INSERT INTO {'BESEDANUMBER'+str(event.chat_id)}(ID, BANONOFF, STATUS, WARNINGS) VALUES({int(textmessage)}, 1, 0, 2) ''')
                                    else:
                                        result = cur.execute(f'''UPDATE {'BESEDANUMBER'+str(event.chat_id)}
        SET STATUS = 0,
        BANONOFF = 1,
        WARNINGS = 2,
        WHERE ID = {x}''')
                                    con.commit()
                                    con.close()
                                    vk.messages.removeChatUser(chat_id=int(event.chat_id),
                                                               user_id=int(textmessage),
                                                               random_id=random.randint(0, 2 ** 64))
                                    print('BAN!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                                else:
                                    con.close()
                                    print(1 + 'b')
                            elif textmessage[:13] == '!мбмультибан ':#7
                                textmessage = textmessage[13:].split()
                                for i in textmessage:
                                    xi = i
                                    con = sqlite3.connect(NAMETABLE)
                                    cur = con.cursor()
                                    checkbase = 'BESEDANUMBER'+str(event.chat_id) in [j for i in cur.execute(f'''SELECT * FROM Sqlite_master WHERE type = "table"''').fetchall() for j in i]
                                    if checkbase:
                                        pass
                                    else:
                                        result = cur.execute(f"""CREATE TABLE {'BESEDANUMBER'+str(event.chat_id)} (
        ID int,
        BANONOFF int,
        STATUS int,
    WARNINGS int);""")
                                        result = cur.execute(f'''INSERT INTO {'BESEDANUMBER'+str(event.chat_id)}(ID, BANONOFF, STATUS, WARNINGS) VALUES({god_id}, 0, 5, -100000000000000000000000) ''')
                                        con.commit()
                                    if AccessCheck(event.obj.message['from_id'], 'BESEDANUMBER'+str(event.chat_id), 7, idob=xi):
                                        if xi not in [i[0] for i in cur.execute(f'''SELECT ID FROM {'BESEDANUMBER'+str(event.chat_id)}''').fetchall()]:
                                            result = cur.execute(f'''INSERT INTO {'BESEDANUMBER'+str(event.chat_id)}(ID, BANONOFF, STATUS, WARNINGS) VALUES({int(xi)}, 1, 0, 2) ''')
                                        else:
                                            result = cur.execute(f'''UPDATE {'BESEDANUMBER'+str(event.chat_id)}
        SET STATUS = 0,
        BANONOFF = 1,
        WARNINGS = 2
        WHERE ID = {xi}''')
                                        con.commit()
                                        con.close()
                                        vk.messages.removeChatUser(chat_id=int(event.chat_id),
                                                                   user_id=int(xi),
                                                                   random_id=random.randint(0, 2 ** 64))
                                        print('BAN!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                                    else:
                                        con.close()
                                        print(1 + 'b')
                            elif textmessage[:10] == '!мбразбан ':#8
                                textmessage = textmessage[10:]
                                con = sqlite3.connect(NAMETABLE)
                                cur = con.cursor()
                                checkbase = 'BESEDANUMBER'+str(event.chat_id) in [j for i in cur.execute(f'''SELECT * FROM Sqlite_master WHERE type = "table"''').fetchall() for j in i]
                                if checkbase:
                                    pass
                                else:
                                    result = cur.execute(f"""CREATE TABLE {'BESEDANUMBER'+str(event.chat_id)} (
    ID int,
    BANONOFF int,
    STATUS int,
    WARNINGS int);""")
                                    result = cur.execute(f'''INSERT INTO {'BESEDANUMBER'+str(event.chat_id)}(ID, BANONOFF, STATUS, WARNINGS) VALUES({god_id}, 0, 5, -100000000000000000000000) ''')
                                    con.commit()
                                if AccessCheck(event.obj.message['from_id'], 'BESEDANUMBER'+str(event.chat_id), 8):
                                    result = cur.execute(f'''UPDATE {'BESEDANUMBER'+str(event.chat_id)}
        SET STATUS = 0,
        BANONOFF = 0,
        WARNINGS = 0
        WHERE ID = {x}''')
                                    con.commit()
                                    con.close()
                                else:
                                    con.close()
                                    print(1 + 'b')
                            elif textmessage[:17] == '!мбайдиучастников':#9
                                if AccessCheck(event.obj.message['from_id'], 'BESEDANUMBER'+str(event.chat_id), 9):
                                    besedainfo = vk.messages.getConversationMembers(peer_id=2000000000+event.chat_id, random_id=random.randint(0, 2 ** 64))
                                    users = besedainfo['profiles']
                                    for i in users:
                                        con = sqlite3.connect(NAMETABLE)
                                        cur = con.cursor()
                                        checkbase = 'BESEDANUMBER'+str(event.chat_id) in [j for i in cur.execute(f'''SELECT * FROM Sqlite_master WHERE type = "table"''').fetchall() for j in i]
                                        if checkbase:
                                            pass
                                        else:
                                            result = cur.execute(f"""CREATE TABLE {'BESEDANUMBER'+str(event.chat_id)} (
            ID int,
            BANONOFF int,
            STATUS int,
            WARNINGS int);""")
                                            result = cur.execute(f'''INSERT INTO {'BESEDANUMBER'+str(event.chat_id)}(ID, BANONOFF, STATUS, WARNINGS) VALUES({god_id}, 0, 5, -100000000000000000000000) ''')
                                            con.commit()
                                        if i['id'] not in [i[0] for i in cur.execute(f'''SELECT ID FROM {'BESEDANUMBER'+str(event.chat_id)}''').fetchall()]:
                                            result = cur.execute(f'''INSERT INTO {'BESEDANUMBER'+str(event.chat_id)}(ID, BANONOFF, STATUS, WARNINGS) VALUES({int(i['id'])}, 0, 0, 0) ''')
                                            con.commit()
                                        m = cur.execute(f'''SELECT WARNINGS FROM {'BESEDANUMBER'+str(event.chat_id)} WHERE ID = {i['id']}''').fetchall()[0][0]
                                        con.commit()
                                        con.close()
                                        print(i['first_name'] + ' ' + i['last_name'], 'first_id:'+str(i['id']), 'second_id:'+i['screen_name'], 'Online:'+str(bool(i['online'])), 'Warnings:'+str(m), sep='\n')
                                        vk.messages.send(chat_id=int(event.chat_id),
                                                     message='\n'.join([i['first_name'] + ' ' + i['last_name'], 'first_id:'+str(i['id']), 'second_id:'+i['screen_name'], 'Online:'+str(bool(i['online'])), 'Warnings:'+str(m)]),
                                                     random_id=random.randint(0, 2 ** 64))
                                else:
                                    con.close()
                                    print(1 + 'b')
                            elif textmessage[:18] == '!мбпредупреждение ':#10
                                textmessage = textmessage[18:]
                                con = sqlite3.connect(NAMETABLE)
                                cur = con.cursor()
                                checkbase = 'BESEDANUMBER'+str(event.chat_id) in [j for i in cur.execute(f'''SELECT * FROM Sqlite_master WHERE type = "table"''').fetchall() for j in i]
                                if checkbase:
                                    pass
                                else:
                                    result = cur.execute(f"""CREATE TABLE {'BESEDANUMBER'+str(event.chat_id)} (
    ID int,
    BANONOFF int,
    STATUS int,
    WARNINGS int);""")
                                    result = cur.execute(f'''INSERT INTO {'BESEDANUMBER'+str(event.chat_id)}(ID, BANONOFF, STATUS, WARNINGS) VALUES({god_id}, 0, 5, -100000000000000000000000) ''')
                                    con.commit()
                                if AccessCheck(event.obj.message['from_id'], 'BESEDANUMBER'+str(event.chat_id), 10):
                                    if int(textmessage) not in [i[0] for i in cur.execute(f'''SELECT ID FROM {'BESEDANUMBER'+str(event.chat_id)}''').fetchall()]:
                                        result = cur.execute(f'''INSERT INTO {'BESEDANUMBER'+str(event.chat_id)}(ID, BANONOFF, STATUS, WARNINGS) VALUES({int(textmessage)}, 0, 0, 1) ''')
                                    else:
                                        mb = cur.execute(f'''SELECT WARNINGS FROM {'BESEDANUMBER'+str(event.chat_id)} WHERE ID = {x}''').fetchall()[0][0]+1
                                        result = cur.execute(f'''UPDATE {'BESEDANUMBER'+str(event.chat_id)}
        SET WARNINGS = {mb}
        WHERE ID = {x}''')
                                    con.commit()
                                    con.close()
                                else:
                                    con.close()
                                    print(1 + 'b')

                            elif textmessage[:16] == '!мбпросветление ':#11
                                textmessage = textmessage[16:]
                                con = sqlite3.connect(NAMETABLE)
                                cur = con.cursor()
                                checkbase = 'BESEDANUMBER'+str(event.chat_id) in [j for i in cur.execute(f'''SELECT * FROM Sqlite_master WHERE type = "table"''').fetchall() for j in i]
                                if checkbase:
                                    pass
                                else:
                                    result = cur.execute(f"""CREATE TABLE {'BESEDANUMBER'+str(event.chat_id)} (
        ID int,
        BANONOFF int,
        STATUS int,
        WARNINGS int);""")
                                    result = cur.execute(f'''INSERT INTO {'BESEDANUMBER'+str(event.chat_id)}(ID, BANONOFF, STATUS, WARNINGS) VALUES({god_id}, 0, 5, -100000000000000000000000) ''')
                                    con.commit()
                                if AccessCheck(event.obj.message['from_id'], 'BESEDANUMBER'+str(event.chat_id), 11):
                                    if int(textmessage) not in [i[0] for i in cur.execute(f'''SELECT ID FROM {'BESEDANUMBER'+str(event.chat_id)}''').fetchall()]:
                                        result = cur.execute(f'''INSERT INTO {'BESEDANUMBER'+str(event.chat_id)}(ID, BANONOFF, STATUS, WARNINGS) VALUES({int(textmessage)}, 0, 3, 0) ''')
                                    else:
                                        mb = cur.execute(f'''SELECT WARNINGS FROM {'BESEDANUMBER'+str(event.chat_id)} WHERE ID = {x}''').fetchall()[0][0]+1
                                        result = cur.execute(f'''UPDATE {'BESEDANUMBER'+str(event.chat_id)}
            SET WARNINGS = 0,
            STATUS = 3
            WHERE ID = {x}''')
                                    con.commit()
                                    con.close()
                                else:
                                    con.close()
                                    print(1 + 'b')
                                
                            elif textmessage[:13] == '!мбобнуление ':#12
                                textmessage = textmessage[13:]
                                con = sqlite3.connect(NAMETABLE)
                                cur = con.cursor()
                                if AccessCheck(event.obj.message['from_id'], 'BESEDANUMBER'+str(event.chat_id), 12):
                                    result = cur.execute(f'''UPDATE {'BESEDANUMBER'+str(event.chat_id)}
            SET WARNINGS = 0,
            STATUS = 0,
            BANONOFF = 0
            WHERE ID = {x}''')
                                    con.commit()
                                    con.close()
                                else:
                                    con.close()
                                    print(1 + 'b')
                            elif textmessage == '!мбвыключениебота':
                                if event.obj.message['from_id'] == god_id:
                                    BotOperationFlag=0
                                    break
                                else:
                                    vk.messages.send(chat_id=int(event.chat_id),
                                             message='Недостаточно прав!',
                                             random_id=random.randint(0, 2 ** 64))
                                    
                            elif textmessage[:3]=='!мб':
                                vk.messages.send(chat_id=int(event.chat_id),
                                                 message='Не знаю такой команды(',
                                                 random_id=random.randint(0, 2 ** 64))
            else:
                break
        except vk_api.exceptions.ApiError:
            
            vk.messages.send(chat_id=int(event.chat_id),
                                             message='Низзя!',
                                             random_id=random.randint(0, 2 ** 64))
        except TypeError:
            vk.messages.send(chat_id=int(event.chat_id),
                                             message='Недостаточно прав!',
                                             random_id=random.randint(0, 2 ** 64))
        except ValueError:
            pass
            

        
        
