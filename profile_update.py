#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Updated:
#  1. 使用async来update lastname，更加稳定
#  2. 增加emoji clock，让时间显示更加有趣味
#  3. forked from cody
#  4. 改为使用datetime模块而非time，解决时区问题

from datetime import timedelta
import datetime
import os
import sys
import logging
import asyncio
import random
from telethon import TelegramClient
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.photos import UploadProfilePhotoRequest
from emoji import emojize
import dayscal


all_fun_emoji_name = ["no_smoking", "dash", "no_one_under_eighteen",
                      "firecracker", "party_popper", "lemon", "rocket", "high_voltage", "fire", "droplet"]
fun_emoji_symb = [emojize(":%s:" % s, use_aliases=True)
                  for s in all_fun_emoji_name]
all_time_emoji_name = ["clock12", "clock1230", "clock1", "clock130", "clock2", "clock230", "clock3", "clock330", "clock4", "clock430", "clock5",
                       "clock530", "clock6", "clock630", "clock7", "clock730", "clock8", "clock830", "clock9", "clock930", "clock10", "clock1030", "clock11", "clock1130"]
time_emoji_symb = [emojize(":%s:" % s, use_aliases=True)
                   for s in all_time_emoji_name]

api_auth_file = 'api_auth'
if not os.path.exists(api_auth_file+'.session'):
    api_id = input('api_id: ')
    api_hash = input('api_hash: ')
else:
    api_id = 123456
    api_hash = '00000000000000000000000000000000'

client1 = TelegramClient(api_auth_file, api_id, api_hash)

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


async def change_name_auto():
    # Set time zone to UTC+8
    # ln -sf /usr/share/zoneinfo/Asia/Chongqing /etc/localtime
    # https://stackoverflow.com/questions/4788533/python-strftime-gmtime-not-respecting-timezone

    print('Going to change name')

    while True:
        try:
            t = datetime.datetime.utcnow()+timedelta(hours=8)
            time_cur = t.strftime("%H:%M:%S:%p:%a")
            hour, minu, seco, p, abbwn = time_cur.split(':')
            day, delday, per = dayscal.today_of_year()
            if int(seco) % 10 == 0:
                shift = 0
                if int(minu) > 30:
                    shift = 1
                # hour symbols
                hsym = time_emoji_symb[(int(hour) % 12)*2+shift]

                for_fun = random.random()

                fsym = fun_emoji_symb[random.randint(0, 9)]

                if for_fun < 0.10:
                    last_name = '%s:%s %s UTC+8 %s' % (hour, minu, p, hsym)
                    about = '你好呀！'
                elif for_fun < 0.20:
                    last_name = '%s:%s %s %s %s' % (hour, minu, p, abbwn, hsym)
                    about = '为什么偷窥我？'
                elif for_fun < 0.30:
                    last_name = '今年已过%s%%' % format(per*100, '0.1f')
                    about = 'Always blue.'
                elif for_fun < 0.40:
                    last_name = '%s年%s月%s日' % (day.year, day.month, day.day)
                    about = '找我有什么事吗？'
                elif for_fun < 0.50:
                    last_name = '%s的第%s天' % (day.year, delday)
                    about = '害羞中～'
                elif for_fun < 0.60:
                    last_name = '%s' % fsym
                    about = '你好呀～'
                elif for_fun < 0.70:
                    last_name = '%s' % fsym
                    about = '机器人'
                elif for_fun < 0.80:
                    last_name = '%s' % fsym
                    about = '怎么又是你?'
                elif for_fun < 0.90:
                    last_name = '%s' % fsym
                    about = 'How old are you?'
                else:
                    last_name = '%s' % fsym
                    about = '再见了您嘞～'

                await client1(UpdateProfileRequest(last_name=last_name, about=about))
                logger.info('Updated -> %s %s' % (last_name, about))
                if int(hour) % 5 == 0:
                    name = random.randint(1, 10)
                    await client1(UploadProfilePhotoRequest(await client1.upload_file('/home/ron/test_tg/avator/%s.jpg' % name)))

        except KeyboardInterrupt:
            print('\nwill reset last name\n')
            await client1(UpdateProfileRequest(last_name=''))
            sys.exit()

        except Exception as e:
            print('%s: %s' % (type(e), e))

        await asyncio.sleep(1)


# main function
async def main(loop):

    await client1.start()

    # create new task
    print('creating task')
    task = loop.create_task(change_name_auto())
    await task

    print('It works.')
    await client1.run_until_disconnected()
    task.cancel()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
