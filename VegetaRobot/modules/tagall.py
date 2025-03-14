import os
import logging
import asyncio

from telethon import Button
from telethon import events
from telethon.tl.types import ChannelParticipantsAdmins

from VegetaRobot import telethn

@telethn.on(events.NewMessage(pattern="^/tagall|@all?(.*)"))
async def mentionall(event):
  if event.is_private:
    return await event.respond("Use This In Channel or Group!")

  admins = []
  async for admin in telethn.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins):
    admins.append(admin.id)
  if event.sender_id not in admins:
    return await event.respond("Only admins can mention all!")

  if event.pattern_match.group(1):
    mode = "text_on_cmd"
    msg = event.pattern_match.group(1)
  elif event.reply_to_msg_id:
    mode = "text_on_reply"
    msg = event.reply_to_msg_id
    if msg is None:
        return await event.respond("__I can't mention members for older messages! (messages which sended before i added to group)__")
  elif event.pattern_match.group(1) and event.reply_to_msg_id:
    return await event.respond("__Give me one argument!__")
  else:
    return await event.respond("__Reply to a message or give me some text to mention others!__")

  if mode == "text_on_cmd":
    usrnum = 0
    usrtxt = ""
    async for usr in telethn.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
      if usrnum == 5:
        await telethn.send_message(event.chat_id, f"{usrtxt}\n\n{msg}")
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""

  elif mode == "text_on_reply":
    usrnum = 0
    usrtxt = ""
    async for usr in telethn.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
      if usrnum == 5:
        await telethn.send_message(event.chat_id, usrtxt, reply_to=msg)
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""

# Cancle 

@telethn.on(events.NewMessage(pattern="^/cancel$"))
async def cancel_spam(event):
  if not event.chat_id in spam_chats:
    return await event.respond('__There is no proccess on going...__')
  else:
    try:
      spam_chats.remove(event.chat_id)
    except:
      pass
    return await event.respond('**__Stoped__**\n\n**__Powered By:__ @lifeinsinn**')
        

        
#© @pegasusXteam
