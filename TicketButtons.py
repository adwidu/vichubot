from gc import callbacks
import discord, asyncio
from discord.ui import Button, View
class TicketButtons(View):
    def __init__(self,style,text,func):
        super().__init__()
        b = Button(style=style, label=text, emoji="\U0001F4E9")
        b.callback = func
        self.add_item(b)
    def add_button(self,style,text,func):
        b = Button(style=style, label=text, emoji="\U0001F4E9")
        b.callback = func
        self.add_item(b)