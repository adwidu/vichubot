#imports
import json
import random
import discord
import time
import configparser
import miscellaneousFunctions as mf
import TicketButtons as TB
import requests
import re
import os
import asyncio
import glob

from pytube import YouTube, Search
from discord.ui import Button, View
from discord.ext import commands, tasks
from moviepy.editor import *

#declarations
sentForStream = False
connected_to_voice = False
intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix='vb/', intents=intents,help_command=None)

#Variable Initialization
iniFile = configparser.ConfigParser()
iniFile.read('configData.ini')

token = iniFile.get('Initialization data','token')
warningsTillMute = iniFile.get('Initialization data','warningsTillKick')
canUseReloadCommand = iniFile.getboolean("On run data", "canUseReloadCommand")
memesQuantity = iniFile.getint("On run data", "memesQuantity")
emailsQuantity = iniFile.getint("On run data", "emailsQuantity")
passwordQuantity = iniFile.getint("On run data", "passwordsQuantity")
print("Loaded .ini Data")

memesJso = open("memes.json","r")
memesJson = memesJso.readline()
memesJso.close()

emailsJso = open("FakeEmailAddresses.json","r")
emailsJson = emailsJso.readline()
emailsJso.close()

passwordsJso = open("FakePasswords.json","r")
passwordsJson = passwordsJso.readline()
passwordsJso.close()

ticketJso = open("ticketMessages.json","r")
ticketJson = json.loads(ticketJso.readline())
print("Loaded .json Data")

helpFile = open("helpCommand.hlp")
helpData = helpFile.readlines()
helpEmbed = discord.Embed()
helpEmbed.set_author(name=helpData[0],icon_url=helpData[2])
helpEmbed.color = discord.Color.from_str(helpData[1])
helpEmbed.description = helpData[3]
helpFile.close()
for i in range(4,len(helpData), 2):
    helpEmbed.add_field(name=helpData[i],value=helpData[i+1],inline=False)
print("Loaded .hlp Data")

__temp_adminsids = open("admins.conf","r").readlines()
_adminsids = []
for i in range(len(__temp_adminsids)):
    _adminsids += [int(__temp_adminsids[i])]

print("Loaded .conf Data")

pasturl = ["","",""]

#Bot Events
@bot.event
async def on_ready():
    activity = discord.Game(name="", type=3)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="el servidor del vichu"))
    
    print("Starting youtube thread")
    #youtubeThread.start()

    print("Starting twitch thread")
    #twitchThread.start()

    print("Bot is ready!") #On_ready

#Separate threads
"""
@tasks.loop(seconds=1)
async def youtubeThread():
    global bot,pasturl


    # Videos
    jsonData = json.loads(open("YoutubeTwitchMessage.json","r").readline())
    channel = jsonData["youtubeChannel"]
    ctx_id = jsonData["textChannel"]
    html = requests.get(channel + "/videos").text
    info = re.search('(?<={"label":").*?(?="})', html).group()
    try:
        url = "https://www.youtube.com/watch?v=" + re.search('(?<="videoId":").*?(?=")', html).group()
    except Exception:
        url = ""
    if(url != pasturl[0]):
        pasturl[0] = url
        ctx = bot.guilds[0].get_channel(ctx_id)
        message = str(jsonData["youtubeVidMessage"])
        message = message.format(jsonData["ping"],jsonData["vichuPing"],url)
        await ctx.send(message) 

    # Shorts
    html = requests.get(channel + "/shorts").text
    info = re.search('(?<={"label":").*?(?="})', html).group()
    try:
        url = "https://www.youtube.com/watch?v=" + re.search('(?<="videoId":").*?(?=")', html).group()
    except Exception:
        url = ""
    if(url != pasturl[1]):

        pasturl[1] = url
        ctx = bot.guilds[0].get_channel(ctx_id)
        message = str(jsonData["youtubeStMessage"])
        message = message.format(jsonData["ping"],jsonData["vichuPing"],url)
        await ctx.send(message) #Youtube thread

@tasks.loop(seconds=1)
async def twitchThread():
    global bot, sentForStream
    jsonData = json.loads(open("YoutubeTwitchMessage.json","r").readline())
     
    HEADERS = { 'client-id' : 'kimne78kx3ncx6brgo4mv6wki5h1ko' }
    GQL_QUERY = 
    query($login: String) {
        user(login: $login) {
            stream {
                id
            }
        }
    }
    
    
    def isLive(username):
        QUERY = {
            'query': GQL_QUERY,
            'variables': {
                'login': username
            }
        }

        response = requests.post('https://gql.twitch.tv/gql',
                                 json=QUERY, headers=HEADERS)
        dict_response = response.json()
        return True if dict_response['data']['user']['stream'] is not None else False


    user = jsonData["twitchChannel"]
    IS_LIVE = isLive(user)
    if IS_LIVE:
        if sentForStream == False:
            sentForStream = True
            message = str(jsonData["twitchMessage"])
            ctx_id = jsonData["textChannel"]
            message = str(jsonData["twitchMessage"])
            message = message.format(jsonData["ping"],jsonData["vichuPing"],jsonData["twitchURL"])
            ctx = bot.guilds[0].get_channel(ctx_id)
            print(message)
            await ctx.send(message)

    else:
        sentForStream = False #Twitch thread
"""

#Fun commands

@bot.command()
async def elpepe(ctx):
    await ctx.send('ETEESEECH') #Elpepe

@bot.command()
async def meme(ctx):
    global iniFile, memesJson, memesQuantity
    rnumber = random.Random().randint(1, memesQuantity)
    (image, text) = mf.get_memes_by_num(rnumber,memesJson)
    await ctx.send(text, file=discord.File(image)) #Meme

@bot.command()
async def voltear_moneda(ctx):
    await ctx.send("Volteando moneda..")
    time.sleep(0.5)
    rnumber = random.Random().randint(0,1)
    if(rnumber == 1):
        await ctx.send("Salio sello")
    else:
        await ctx.send("Salio cara") #Voltear_moneda

@bot.command()
async def cachipun(ctx):
    async def t(self:discord.interactions.Interaction):
        result = compare_results(rnumber, 0) # bot, user
        if result == 0:
            await self.response.send_message("Tijeras, contra tijeras? No me lo creo, empatamos :O")
        if result == 1:
            await self.response.send_message("Papel contra tijeras? Te diste cuenta de que el boton de la piedra es un moai?, ganaste \U0001F5FF")
        if result == 2:
            await self.response.send_message("Piedra contra tijeras? Cuanta suerte tengo, Gane, me voy a comprar un loto")
        b = Button(style=discord.ButtonStyle.red, label="Tijeras", emoji="\U00002702")
        await disable_buttons()

    async def p(self:discord.interactions.Interaction):
        result = compare_results(rnumber, 1)
        if result == 0:
            await self.response.send_message("Piedra y piedra? No me copies porfa xd, empatamos :P")
        if result == 1:
            await self.response.send_message("Tijeras contra piedra? Como supiste?, ganaste :O")
        if result == 2:
            await self.response.send_message("Papel contra piedra? Yay, Gane :D")

        await disable_buttons()

    async def pp(self:discord.interactions.Interaction):
        result = compare_results(rnumber, 2)
        if result == 0:
            await self.response.send_message("Papel contra papel? cuanta suerte, empatamos :O")
        if result == 1:
            await self.response.send_message("Piedra contra papel? Bah, ganaste :(")
        if result == 2:
            await self.response.send_message("Tijeras contra papel? Je, Gane :D")

        
        await disable_buttons()
    async def disable_buttons():
        mview = View()
        b = Button(style=discord.ButtonStyle.red, label="Tijeras", emoji="\U00002702")
        b.disabled = True
        mview.add_item(b)
        b = Button(style=discord.ButtonStyle.gray, label="Piedra", emoji="\U0001F5FF")
        b.disabled = True
        mview.add_item(b)
        b = Button(style=discord.ButtonStyle.blurple, label="Papel", emoji="\U0001F4C4")
        b.disabled = True
        mview.add_item(b)
        await message.edit(view=mview)
    def compare_results(bot,user):
        print("bot " + str(bot))
        print("user " + str(user))
        if bot == 0:
            if user == 0:
                return 0
            if user == 1:
                return 1
            if user == 2:
                return 2
        if bot == 1:
            if user == 1:
                return 0
            if user == 2:
                return 1
            if user == 0:
                return 2
        if bot == 2:
            if user == 2:
                return 0
            if user == 1:
                return 2
            if user == 0:
                return 1
            #tijeras = 0
            #piedra = 1
            #papel = 2

            #empate = 0
            #gana usuario = 1
            #pierde usuario = 2
    #rnumber = random.Random().randint(0,2)
    rnumber = 2
    mview = View()
    b = Button(style=discord.ButtonStyle.red, label="Tijeras", emoji="\U00002702")
    b.callback = t
    mview.add_item(b)
    b = Button(style=discord.ButtonStyle.gray, label="Piedra", emoji="\U0001F5FF")
    b.callback = p
    mview.add_item(b)
    b = Button(style=discord.ButtonStyle.blurple, label="Papel", emoji="\U0001F4C4")
    b.callback = pp
    mview.add_item(b)
    message = await ctx.send("Caaa- chiii- pun", view=mview) #Cachipun

@bot.command()
async def hackear(ctx):
    global emailsQuantity, emailsJson, passwordQuantity, passwordsJson
    message = str(ctx.message.content)
    try:
        message = message.replace(ctx.message.content.split(" ")[1], ctx.message.content.split(" ")[1].removesuffix(">").removeprefix("<@"))
    except Exception:
        message = ""
    if ctx.author.id in _adminsids:
        if message == "":
            await ctx.send("Error al ejecutar el comando: Se necesita un argumento")
            return
        else:
                publicIpAddress = [random.Random().randint(120,289), random.Random().randint(20,255), random.Random().randint(40,255),random.Random().randint(16,255)]
                privateIpAddress = [192,168,1,random.Random().randint(20,255)]
                gateway = [192,168,1,1]
                dns = [8,8,8,8,1,1,1,1]

                await ctx.send("Direccion ip de <@" + message.split(" ")[1] + ">: \nIp publica: " + str(publicIpAddress[0]) + "." + str(publicIpAddress[1]) + "." + str(publicIpAddress[2]) + "." + str(publicIpAddress[3]) + 
                               "\nIp privada: " + str(privateIpAddress[0]) + "." + str(privateIpAddress[1]) + "." + str(privateIpAddress[2]) + "." + str(privateIpAddress[3]) +
                               "\nGateway: " + str(gateway[0]) + "." + str(gateway[1]) + "." + str(gateway[2]) + "." + str(gateway[3]) +
                               "\nDNS: " + str(dns[0]) + "." + str(dns[1]) + "." + str(dns[2]) + "." + str(dns[3]) +"   "+ str(dns[4]) + "." + str(dns[5]) + "." + str(dns[6]) + "." + str(dns[7]))
                
                rnum = random.Random().randint(0,emailsQuantity)
                await ctx.send("Direccion de correo electronico de <@" + message.split(" ")[1] + ">:\n\t" + mf.get_email_by_num(rnum, emailsJson))

                rnum = random.Random().randint(0,passwordQuantity)
                await ctx.send("Direccion de correo electronico de <@" + message.split(" ")[1] + ">:\n\t" + mf.get_password_by_num(rnum, passwordsJson)) #Hackear

@bot.command()
async def quegei(ctx): #quegei
    message = str(ctx.message.content)
    try:
        message = message.replace(ctx.message.content.split(" ")[1], ctx.message.content.split(" ")[1].removesuffix(">").removeprefix("<@"))
    except Exception:
        message = ""
    if message == "":
        await ctx.send("Error al ejecutar el comando: Se necesita un argumento")
        return
    else:
        rnumber = random.Random().randint(0,100)
        if message.split(" ")[1] in [""]:
            rnumber = 0
        await ctx.send("<@{}> es {}% gay :rainbow_flag:".format(message.split(" ")[1], rnumber))

        if rnumber >= 70:
            await ctx.send(file=discord.File("LoSuponia.jpg")) #Quegei

@bot.command()
async def musica(ctx: commands.Context, *url):
    global connected_to_voice
    realurl = ""
    for i in range(len(url)):
        realurl += url[i] + " "
    voicechannel = None if not ctx.author.voice else ctx.author.voice.channel
    if voicechannel:
        if not connected_to_voice:
            connected_to_voice = True
            def download():
                nonlocal realurl
                
                print("downloading")
                try:
                    url = YouTube(realurl)
                except Exception:
                    url = Search(realurl).results[0]

                video = url.streams.filter(progressive=True).order_by('resolution').desc().first()
                realurl = video.default_filename

                if os.path.exists(".\\music\\"+realurl+".mp3"):
                    return
                video.download(".\\music\\")

                
                convert(realurl)
            def convert(url):
                video = VideoFileClip(".\\music\\" + url)

                video.audio.write_audiofile(".\\music\\" + url + ".mp3")

                
            try:
                vc = await voicechannel.connect(self_deaf = True)
            except Exception:
                vc = bot.voice_clients[0]
            await asyncio.to_thread(download)
            
            # Open the MP3 file as a binary file
            fp = open(f"./music/{realurl}.mp3", "rb")
                # Wrap the binary data in a PCMVolumeTransformer
            audio_source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(executable="ffmpeg.exe",source=f"./music/{realurl}.mp3"))
            await ctx.reply("Claro! conectando y reproduciendo '" + realurl.replace(".mp4","") + "'")
            
                # Play the audio
            vc.play(audio_source)
            while vc.is_playing() == True:
                await asyncio.sleep(1)

            await vc.disconnect(force=True)
            connected_to_voice = False
            
        else:
            await ctx.reply("Ya estoy conectado a un canal, espera a que termine y me podras llamar")
    else:
        await ctx.reply("No se ha encontrado el canal al que estas conectado, si no estas conectado a ningun canal de voz conectate para escuchar musica") #Musica

@bot.command()
async def parar_musica(ctx):
    global connected_to_voice
    if connected_to_voice:
        await ctx.reply("Parando")
        vc = bot.voice_clients[0]
        await vc.disconnect(force=True)
        connected_to_voice = False                   

    else:
        await ctx.reply("No estoy reproduciendo nada") #Parar_musica
        
@bot.command()
async def musica_ar(ctx):
    
    # Set the directory path and file pattern
    dir_path = ".\\music\\"
    file_pattern = "*.mp3"

    # List the files in the directory that match the pattern
    file_list = glob.glob(os.path.join(dir_path, file_pattern))
    ar = "```"
    # Print the file names
    for file_name in file_list:
        ar += file_name.removeprefix(dir_path).removesuffix(".mp4.mp3") + "\n"
    await ctx.send("Canciones que estan listas para su uso:")
    await ctx.send(ar+"```")
#Functionality commands
@bot.command()
async def shutdown(ctx):
    if ctx.author.id in _adminsids:
        await ctx.message.delete()
        await bot.close()
        print("Bot Closed") 
    else: 
        await ctx.send("No tienes permiso para hacer eso")
        await mf.need_adminsconf_permision(ctx) #Shutdown

@bot.command()
async def reload(ctx):
    global _adminsids, __temp_adminsids, canUseReloadCommand, iniFile, helpEmbed, helpData, helpFile, token, memesQuantity, memesJson, memesJso, emailsJso, emailsJson, emailsQuantity
    global passwordsJso, passwordsJson, passwordsQuantity, ticketJso, ticketJson, warningsTillMute
    
    if ctx.author.id in _adminsids:
        if canUseReloadCommand:
            await ctx.send("Detectando si hay nuevos admins")
            adminsDetectedNO = 0
            async with ctx.typing():
                for member in bot.guilds[0].members:
                    if member.get_role(1025894129244315671):
                        if member.id in _adminsids:
                            await ctx.send("Usuario encontrado, ya poseia los derechos del bot")
                        else:
                            await ctx.send("Usuario encontrado, agregando a <@{}>".format(str(member.id)))
                            adminsDetectedNO += 1
                            _adminsids += [member.id]
                            f = open("admins.conf","w")
                            for i in range(len(_adminsids)):
                                f.write(str(_adminsids[i]) + '\n')
            if adminsDetectedNO == 0:
                await ctx.send("No se encontraron nuevos admins")
            elif adminsDetectedNO == 1:
                await ctx.send("Se ha encontrado 1 admin nuevo")
            else: 
                await ctx.send("Se han encontrado {} nuevos admins".format(str(adminsDetectedNO)))
            time.sleep(0.2)
            #Variable Initialization
            iniFile = configparser.ConfigParser()
            iniFile.read('configData.ini')
    
            token = iniFile.get('Initialization data','token')
            warningsTillMute = iniFile.get('Initialization data','warningsTillKick')
            canUseReloadCommand = iniFile.getboolean("On run data", "canUseReloadCommand")
            memesQuantity = iniFile.getint("On run data", "memesQuantity")
            emailsQuantity = iniFile.getint("On run data", "emailsQuantity")
            passwordsQuantity = iniFile.getint("On run data", "passwordsQuantity")

            print("Loaded .ini Data")
            await ctx.send("Se ha recargado la data de configData.ini")


            memesJso = open("memes.json","r")
            memesJson = memesJso.readline()
            memesJso.close()
            await ctx.send("Se ha recargado la data de memes.json")


            emailsJso = open("FakeEmailAddresses.json","r")
            emailsJson = emailsJso.readline()
            emailsJso.close()
            await ctx.send("Se ha recargado la data de FakeEmailAddresses.json")

            
            passwordsJso = open("FakePasswords.json","r")
            passwordsJson = passwordsJso.readline()
            passwordsJso.close()
            await ctx.send("Se ha recargado la data de FakePasswords.json")

            
            ticketJso = open("ticketMessages.json","r")
            ticketJson = json.loads(ticketJso.readline())
            await ctx.send("Se ha recargado la data de ticketMessages.json")
            print("Loaded .json Data")


            helpFile = open("helpCommand.hlp")
            helpData = helpFile.readlines()
            helpEmbed = discord.Embed()
            helpEmbed.set_author(name=helpData[0],icon_url=helpData[2])
            helpEmbed.color = discord.Color.from_str(helpData[1])
            helpEmbed.description = helpData[3]
            helpFile.close()
            for i in range(4,len(helpData), 2):
                helpEmbed.add_field(name=helpData[i],value=helpData[i+1],inline=False)
            print("Loaded .hlp Data")
            await ctx.send("Se ha recargado la data de helpCommand.hlp")

            __temp_adminsids = open("admins.conf","r").readlines()
            _adminsids = []
            for i in range(len(__temp_adminsids)):
                _adminsids += [int(__temp_adminsids[i])]

            print("Loaded .conf Data")
            await ctx.send("Se ha recargado la data de admins.conf")

            await ctx.send("Bot recargado exitosamente")
        else:
            await ctx.send("este comando no esta habilitado")
    else:
        await ctx.send("No tienes permiso para hacer eso")
        await mf.need_adminsconf_permision(ctx) #Reload

@bot.command()
async def ayuda(ctx):
    global helpEmbed
    await ctx.send(embed=helpEmbed) #Ayuda


#Administrative commands
@bot.command()
async def add_admin(ctx):
    global _adminsids, __temp_adminsids

    message = str(ctx.message.content)
    try:
        message = message.replace(ctx.message.content.split(" ")[1], ctx.message.content.split(" ")[1].removesuffix(">").removeprefix("<@"))
    except Exception:
        message = ""
    if ctx.author.id in _adminsids:
        if message == "":
            await ctx.send("Error al ejecutar el comando: Se necesita un argumento")
            return

        user_id = message.split(" ")[1]
        user = await bot.fetch_user(user_id)

        if int(message.split(" ")[1]) in _adminsids:
            await ctx.send("El usuario <@" + message.split(" ")[1] + "> ya forma parte de los administradores del bot")
            return
        
    
        if user is not None:
            member = ctx.guild.get_member(user.id)
            if member is not None:
                _adminsids += [message.split(" ")[1]]
                f = open("admins.conf","w")
                for i in range(len(_adminsids)):
                    f.write(str(_adminsids[i]) + '\n')
                
                if ctx.author.id in _adminsids:
                    time.sleep(0.2)
                    __temp_adminsids = open("admins.conf","r").readlines()
                    _adminsids = []
                    for i in range(len(__temp_adminsids)):
                        _adminsids += [int(__temp_adminsids[i])]
                await ctx.send("<@" + message.split(" ")[1] + "> ahora es un administrador del bot")
            else:
                await ctx.send("Ese usuario no forma parte del servidor")
        else:
            await ctx.send("Ese usuario no existe") 
    else: 
        await ctx.send("No tienes permiso para hacer eso")
        await mf.need_adminsconf_permision(ctx) #Add_admin

@bot.command()
async def print_admins(ctx):
    if ctx.author.id in _adminsids:
        for i in range(len(_adminsids)):
            await ctx.send("<@" + str(_adminsids[i]) + ">") 
    else: 
        await ctx.send("No tienes permiso para hacer eso")
        await mf.need_adminsconf_permision(ctx) #Print_admins

@bot.command()
async def ban(ctx): 
    global _adminsids, __temp_adminsids

    message = str(ctx.message.content)
    try:
        message = message.replace(ctx.message.content.split(" ")[1], ctx.message.content.split(" ")[1].removesuffix(">").removeprefix("<@"))
    except Exception:
        message = ""

    if ctx.author.id in _adminsids:
        if message == "":
            await ctx.send("Error al ejecutar el comando: Se necesita un argumento")
            return

        user_id = message.split(" ")[1]
        user = await bot.fetch_user(user_id)
        
        if user is not None:
            member = ctx.guild.get_member(user.id)
            if member is not None:
                
                await ctx.guild.ban(user, reason = message.removeprefix("vb/ban " + str(user.id) + " "))
                await ctx.send("<@" + message.split(" ")[1] + "> ha sido baneado")
            else:
                await ctx.send("Ese usuario no forma parte del servidor")
        else:
            await ctx.send("Ese usuario no existe") 
    else: 
        await ctx.send("No tienes permiso para hacer eso")
        await mf.need_adminsconf_permision(ctx) #Ban

@bot.command()
async def kick(ctx):
    global _adminsids, __temp_adminsids

    message = str(ctx.message.content)
    try:
        message = message.replace(ctx.message.content.split(" ")[1], ctx.message.content.split(" ")[1].removesuffix(">").removeprefix("<@"))
    except Exception:
        message = ""

    if ctx.author.id in _adminsids:
        if message == "":
            await ctx.send("Error al ejecutar el comando: Se necesita un argumento")
            return

        user_id = message.split(" ")[1]
        user = await bot.fetch_user(user_id)
        
        if user is not None:
            member = ctx.guild.get_member(user.id)
            if member is not None:
                
                await ctx.guild.kick(user, reason = message.removeprefix("vb/kick " + str(user.id) + " "))
                await ctx.send("<@" + message.split(" ")[1] + "> ha sido kickeado")
            else:
                await ctx.send("Ese usuario no forma parte del servidor")
        else:
            await ctx.send("Ese usuario no existe") 
    else: 
        await ctx.send("No tienes permiso para hacer eso")
        await mf.need_adminsconf_permision(ctx) #Kick

@bot.command()
async def warn(ctx: commands.Context):
    global _adminsids, __temp_adminsids, warningsTillBan

    message = str(ctx.message.content)
    try:
        message = message.replace(ctx.message.content.split(" ")[1], ctx.message.content.split(" ")[1].removesuffix(">").removeprefix("<@"))
    except Exception:
        message = ""

    if ctx.author.id in _adminsids:
        if message == "":
            await ctx.send("Error al ejecutar el comando: Se necesita un argumento")
            return

        user_id = message.split(" ")[1]
        user = await bot.fetch_user(user_id)
        
        if user is not None:
            member = ctx.guild.get_member(user.id)
            if member is not None:

                mf.add_warning(member)
                warningsTxt = mf.get_warnings(member, str)
                if mf.get_warnings(member, int) <= warningsTillMute:
                    await ctx.send("<@" + message.split(" ")[1] + "> ha obtenido una advertencia, tiene " + warningsTxt + " de " + warningsTillMute)
                else:
                    await member.kick("Excedida la maxima cantidad de advertencias en el servidor")
            else:
                await ctx.send("Ese usuario no forma parte del servidor")
        else:
            await ctx.send("Ese usuario no existe") 
    else: 
        await ctx.send("No tienes permiso para hacer eso")
        await mf.need_adminsconf_permision(ctx) #Warn

@bot.command()
async def get_warnings(ctx):
    global _adminsids, __temp_adminsids, warningsTillBan

    message = str(ctx.message.content)
    try:
        message = message.replace(ctx.message.content.split(" ")[1], ctx.message.content.split(" ")[1].removesuffix(">").removeprefix("<@"))
    except Exception:
        message = ""

    if ctx.author.id in _adminsids:
        if message == "":
            await ctx.send("Error al ejecutar el comando: Se necesita un argumento")
            return

        user_id = message.split(" ")[1]
        user = await bot.fetch_user(user_id)
        
        if user is not None:
            member = ctx.guild.get_member(user.id)
            #member = bot.guilds[0].get_member(user_id)
            if member is not None:
                warningsTxt = mf.get_warnings(member, str)
                warningsInt = mf.get_warnings(member, int)
                if warningsInt == 0:
                    await ctx.send("<@" + message.split(" ")[1] + "> no tiene advertencias")
                if warningsInt == 1:
                    await ctx.send("<@" + message.split(" ")[1] + "> tiene " + warningsTxt + " advertencia de " + warningsTillBan)
                if warningsInt >= 2:
                    await ctx.send("<@" + message.split(" ")[1] + "> tiene " + warningsTxt + " de " + warningsTillBan + " advertencias")
            else:
                await ctx.send("Ese usuario no forma parte del servidor")
        else:
            await ctx.send("Ese usuario no existe") 
    else: 
        await ctx.send("No tienes permiso para hacer eso")
        await mf.need_adminsconf_permision(ctx) #Get_warnings

@bot.command()
async def delete_channel(ctx):
    global _adminsids, __temp_adminsids

    if ctx.author.id in _adminsids:
        channel = ctx.channel

        await channel.delete()
    else: 
        await ctx.send("No tienes permiso para hacer eso")
        await mf.need_adminsconf_permision(ctx) #Delete_channel

@bot.command()
async def clean(ctx):
    if ctx.author.id == 758050009210945636:
        async with ctx.typing():
            await ctx.channel.purge()

    else:
        ctx.send("Este comando solo puede ser ejecutado por <@758050009210945636>") #Clean
        
@bot.command()
async def ticket_buttons(ctx):
    async def ticketButton(self:discord.interactions.Interaction):
        ticketCategory = None
        for i in range(len(bot.guilds[0].categories)):
            if bot.guilds[0].categories[i].name == "tickets":
                ticketCategory = bot.guilds[0].categories[i]

        role = discord.utils.get(bot.guilds[0].roles, name="SUSCRIPTORES")
        user = self.user
        overwrite = discord.PermissionOverwrite()
        overwrite.read_messages = False
        
        ticketchannel = await ticketCategory.create_text_channel("ticket")
        await ticketchannel.set_permissions(role, overwrite=overwrite)
        
        overwrite.read_messages = True
        await ticketchannel.set_permissions(user, overwrite=overwrite)
        
        member = bot.guilds[0].get_member(user.id)
        await ticketchannel.send(ticketJson["message"].format(str(user.id), str(ticketJson["adminPing"])))
        await self.response.defer()

    if ctx.author.id == 758050009210945636:
        tk = TB.TicketButtons(discord.ButtonStyle.green,"Hacer un ticket", ticketButton)


        ticketEmbed = discord.Embed()
        ticketEmbed.set_author(name="Haz un ticket",icon_url="https://adwidu.000webhostapp.com/VichuBot/logo.png")
        ticketEmbed.color = discord.Color.from_str("#248044")
        ticketEmbed.description = "Preciona el boton (\U0001F4E9 Hacer un ticket) para iniciar un ticket y que el staff del servidor te brinde soporte"
        message = await ctx.send(embed=ticketEmbed, view=tk) #Ticket_buttons

@bot.command()
async def vote(ctx: commands.Context, *args):
    if args == ():
        await ctx.send("Error al ejecutar el comando, se necesita un argumento")
        return
    b1 = int(0)
    b2 = int(0)
    b3 = int(0)
    b4 = int(0)
    b5 = int(0)
    sender = ctx.author.id
    mview = View()
    already_voted = []
    styles = [
        discord.ButtonStyle.blurple,
        discord.ButtonStyle.green,
        discord.ButtonStyle.gray,
        discord.ButtonStyle.success,
        discord.ButtonStyle.secondary
    ]
    async def disable_buttons():
        mview = View()
        b = Button(style=discord.ButtonStyle.red, label="Votacion Cerrada", emoji="\U0000274C")
        b.disabled = True
        mview.add_item(b)
        await message.edit(view=mview) #Disable buttons

    async def call1(self:discord.interactions.Interaction):
        nonlocal b1
        b1 += 1
        if self.user.id not in already_voted:
           
            await self.response.send_message('Gracias por votar, tu voto ha sido por "{}"'.format(args[0]), ephemeral=True)
            already_voted.append(self.user.id)
        else:
            b1 -= 1
            await self.response.send_message("Hey, no puedes votar denuevo", ephemeral=True) #Call1 

    async def call2(self:discord.interactions.Interaction):
        nonlocal b2
        b2 += 1
        if self.user.id not in already_voted:

            await self.response.send_message('Gracias por votar, tu voto ha sido por "{}"'.format(args[1]), ephemeral=True)
            already_voted.append(self.user.id)
        else:
            b2 -= 1
            await self.response.send_message("Hey, no puedes votar denuevo", ephemeral=True) #Call2 

    async def call3(self:discord.interactions.Interaction):
        nonlocal b3
        b3 += 1
        if self.user.id not in already_voted:
            await self.response.send_message('Gracias por votar, tu voto ha sido por "{}"'.format(args[2]), ephemeral=True)
            already_voted.append(self.user.id)

        else:
            b3 -= 1
            await self.response.send_message("Hey, no puedes votar denuevo", ephemeral=True) #Call3 

    async def call4(self:discord.interactions.Interaction):
        nonlocal b4
        b4 += 1
        if self.user.id not in already_voted:

            await self.response.send_message('Gracias por votar, tu voto ha sido por "{}"'.format(args[3]), ephemeral=True)
            already_voted.append(self.user.id)
            
        else:
            b4 -= 1
            await self.response.send_message("Hey, no puedes votar denuevo", ephemeral=True) #Call4 

    async def call5(self:discord.interactions.Interaction):
        nonlocal b5
        b5 += 1
        if self.user.id not in already_voted:
 
            await self.response.send_message('Gracias por votar, tu voto ha sido por "{}"'.format(args[4]), ephemeral=True)
            already_voted.append(self.user.id)
            
        else:
            b5 -= 1

            await self.response.send_message("Hey, no puedes votar denuevo", ephemeral=True) #Call5

    async def call6(self:discord.interactions.Interaction):
        nonlocal b1,b2,b3,b4,b5
        if self.user.id == sender:
            async with ctx.typing():
                options = mf.VoteList()
                op = [b1,b2,b3,b4,b5]
                for option in range(len(args)):
                    options.add(op[option],args[option])
                options.sort()
                _places = "lugares: \n"
                for i in range(len(args)):
                    votes = options.get(i)[0]
                    name = options.get(i)[1]
                    _places += "{}.- {} con {}\n".format(str(i + 1), name, str(votes))
                _places += "gana: {}".format(options.get(0)[1]) 
                await self.response.send_message(_places)
                await disable_buttons()
        else:
            
            await self.response.send_message("Hey, no puedes terminar la votacion, no la hiciste tu", ephemeral=True) #Call6 

    if len(args) > len(styles):
        await ctx.send("Demasiados argumentos",ephimeral=True)
        return
    calls = [
        call1,
        call2,
        call3,
        call4,
        call5
    ]

    for arg in range(len(args)):
        b = Button(style=styles[arg], label=args[arg], emoji="\U0001F4C4")
        b.callback = calls[arg]
        mview.add_item(b)
    b = Button(style=discord.ButtonStyle.red, label="CERRAR VOTACION",emoji="\U0000274C")
    b.callback = call6
    mview.add_item(b)
    
    print(args)
    await ctx.message.delete()
    message = await ctx.send(view=mview) #Vote
bot.run(token)