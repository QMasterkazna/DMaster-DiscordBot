import time

import discord
import random
from discord.ext import commands
import requests
from PIL import Image, ImageFont, ImageDraw
import io
import asyncio
import json
import youtube_dl
from datetime import datetime
import _pickle as pkl
import colorama as col
import ConfigConstants as CC
from math import sqrt, floor
import Logger
import sqlite3
from bs4 import BeautifulSoup
from music_module import Music
import status

command_prefix = ';/'
Token = CC.Token
client = commands.Bot(command_prefix=command_prefix, intents=discord.Intents.all())
client.remove_command('help')
filename = CC.filename
dataBase = {}

playlist = []
isPlayingNow = False
logger = Logger.Logger()


def CalcXpByFormula(x):
    n = (x ** 2) + 15
    return n


def CalcDifferenceOfLevels(x):
    n = (((x + 1) ** 2) + 15) - ((x ** 2) + 15)
    return n


def DrawProgressBar(x):
    filled = "═"
    empty = "─"
    symbolCount = 20
    filledSymbols = int(symbolCount * x)
    progressbar = ""

    for i in range(filledSymbols):
        progressbar += filled

    for f in range(symbolCount - filledSymbols):
        progressbar += empty

    progressbar += f" {round(x * 100, 1)}%"

    return progressbar


def FindLevelByXp(x):
    x = x if x >= 15 else 15
    n = floor(sqrt(x - 15)) + 1
    return n


def init():
    load()
    # TODO:


def load():
    global dataBase
    # TODO: load database from database.pkl file to dataBase variable
    input = open(filename, "rb")
    try:
        dataBase = pkl.load(input)
        input.close()
    except EOFError:
        logger.warn("Файл пустой", "Load")
    except FileNotFoundError:
        logger.warn("Файл не найден", "Load")


def save():
    output = open(filename, "wb")

    pkl.dump(dataBase, output, 2)
    logger.log("База Данных сохранена", "Save")


def AddXpToUser(amount, UserId):
    global dataBase
    dataBase[UserId] += amount
    logger.log(f"Added XP to {UserId} + {amount}", "AddXp")
    save()


def GetUserXp(UserId):
    return dataBase[UserId]


@client.command(pass_context=True, aliases=["xpmap"])
@commands.has_permissions(administrator=True)
async def MapXp(ctx):
    global dataBase
    members = ctx.guild.members
    for member in members:
        if dataBase.get(member.id) is None:
            dataBase[member.id] = 0
    save()
    await ctx.send('база данных сохранена')


@client.command(pass_context=True, aliases=["addxp"])
@commands.has_permissions(administrator=True)
async def AddXp(ctx, member: discord.Member, points: int):
    AddXpToUser(points, member.id)
    await ctx.send('Профиль изменён')


# clear message
@client.command(pass_context=True, aliases=["очистка", 'clear'])
@commands.has_permissions(administrator=True)
async def Clear(ctx, amount=100):
    await ctx.channel.purge(limit=amount)


# clear command
@client.command(pass_context=True, aliases=['билли', 'интим', 'Билли'])
async def Billy(ctx):
    await ctx.send("https://i.ytimg.com/vi/nYkHtNSvgD8/maxresdefault.jpg")


@client.command(pass_context=True)
async def run(ctx):
    await ctx.send("https://tenor.com/view/billy-herrington-herington-beach-party-gif-22706556")


# Kick
@client.command(pass_context=True, aliases=['кик'])
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await ctx.channel.purge(limit=1)
    await member.kick(reason=reason)
    await ctx.send(f'Мой cum у тебя на лице{member.mention}')


# ban
@client.command(pass_context=True, aliases=["бан"])
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await ctx.channel.purge(limit=1)
    await member.ban(reason=reason)
    await ctx.send(f'Отправляйся в ASS, теперь ты f@cking slave{member.mention}')


# unban
@client.command(pass_context=True, aliases=["разбан"])
@commands.has_permissions(administrator=True)
async def unban(ctx, *, member):
    await ctx.channel.purge(limit=1)
    banned_users = await ctx.guild.bans()
    for ban_entry in banned_users:
        user = ban_entry.user
        await ctx.guild.unban(user)
        await ctx.send(f"Boy nextdoor вернулся к Dungeon master{user.mention}")
        return


@client.command(aliases=['пошли в gym', 'хочу в gym'])
async def gym(ctx):
    author = ctx.message.author
    await ctx.send(f'♂{author.mention},Пошли со мной в Gym♂')


# mute
@client.command(pass_context=True, aliases=['мьют'])
@commands.has_permissions(administrator=True)
async def mute(ctx, member: discord.Member, time: int = 60):
    mute_role = discord.utils.get(ctx.message.guild.roles, name='Muted')
    await member.add_roles(mute_role)
    await ctx.send(f"{member.mention} Соси молча, и пей моё Wee wee")
    await asyncio.sleep(time)
    await member.remove_roles(mute_role)


# Dungeon coin
connection = sqlite3.connect("server.db")
cursor = connection.cursor()


@client.event
async def on_ready():
    cursor.execute("""CREATE TABLE IF NOT EXISTS users(
        name TEXT,
        id INT,
        cash BIGINT,
        rep INT,
        lvl INT,
    )""")
    for guild in client.guilds:
        for member in guild.members:
            if cursor.execute(f"SELECT id FROM users WHERE id = {member.id}").fetchone() is None:
                cursor.execute(f"INSERT INTO user VALUES ('{member}'),{member.id},0,0,1")
                connection.commit()
            else:
                pass
    connection.commit()
    print("Bot connected")


@client.event
async def on_member_join(member):
    if cursor.execute(f"SELECT id FROM users WHERE id = {member.id}").fetchone() is None:
        cursor.execute(f"INSERT INTO user VALUES ('{member}'),{member.id},0,0,1")
    else:
        pass


@client.command(aliases=['balance', 'cash', 'Balance', 'Cash'])
async def __balance(ctx, member: discord.Member = None):
    if member is None:
        await ctx.send(embed=discord.Embed(
            description=f"""Баланс пользователя**{ctx.author}** Составляет **{cursor.execute("SELECT cash FROM users WHERE id ={}".format(ctx.author.id)).fetchone()[0]}:leaves:**"""
        ))
    else:
        await ctx.send(embed=discord.Embed(
            description=f"""Баланс пользователя**{member}** Составляет **{cursor.execute("SELECT cash FROM users WHERE id ={}".format(member.id)).fetchone()[0]}:leaves:**"""
        ))


# carduser
@client.command(aliases=['я', 'карта'])
async def profile(ctx, member: discord.Member = None):
    # TODO: make database work properly
    # TODO: Заставить базу данных работать правильно
    if member is None:
        member = ctx.author

    emb = discord.embeds.Embed(title=f"{member.name}#{member.discriminator}")
    emb.add_field(name=f"id: {member.id}", value=f"status:{member.status}")
    emb.add_field(name=f"XP: {dataBase.get(member.id)}", value=f"Level {FindLevelByXp(dataBase.get(member.id))}")
    emb.add_field(name=f'Level Progress',
                  value=f"{DrawProgressBar((dataBase.get(member.id)) / (CalcXpByFormula(FindLevelByXp(dataBase.get(member.id)))))}",
                  inline=False)
    emb.set_image(url=member.avatar_url)
    await ctx.send(embed=emb)


# unmute
@client.command(aliases=['размьют'])
@commands.has_permissions(administrator=True)
async def unmute(ctx, member: discord.Member):
    await ctx.channel.purge(limit=1)
    mute_role = discord.utils.get(ctx.message.guild.roles, name='Muted')
    await member.remove_roles(mute_role)
    await ctx.send(f"{member.mention}Заканчивай, и держи свои Three hundred bucks")


@client.command()
async def cum(ctx):
    await ctx.send(
        'https://tenor.com/view/tyler1-autism-brennan-jrinking-cum-form-dada-drinking-water-in-less-than5seconds-cum-gif-17755097')


# Silence useless bug reports messages

client.add_cog(Music(client))


# LS
@client.command(pass_context=True, aliases=['Играть'])
async def play_custom(ctx):
    await ctx.author.send(' ♂️That turns me on!♂️')


# help
@client.command(pass_context=True, aliases=['Помощь', 'Help'])
async def help(ctx):
    emb = discord.Embed(title='Навигация по командам:')
    emb.add_field(name='{}команды для админов:'.format(command_prefix),
                  value='clear,\nban,\nunban,\nmute,\nunmute,\nkick,\nMapXp,\nAddXp')
    emb.add_field(name='{}команды для пользователей:'.format(command_prefix),
                  value='Играть, \nпривет, \nБилли, \nstats, \nprofile, \ngym, \ncum, \nwatch, \nrun')
    await ctx.send(embed=emb)


@client.command(pass_context=True, aliases=["Привет", "Здарова", 'здарова'])
async def hello(ctx):
    author = ctx.message.author
    await ctx.send(f"{author.mention}приветики, я Билли, рад познакомиться, мой мальчик")


# Смотреть ютуб
@client.command()
async def watch(ctx):
    nowdatetime = datetime.now().isoformat()
    data = {
        "max_age": 172800,
        "max_uses": 0,
        "target_application_id": 880218394199220334,  # Youtube Together
        "target_type": 2,
        "temporary": False,
        "validate": None,
        "created_at": nowdatetime
    }
    headers = {
        "Authorization": f"Bot {Token}",
        "Content-Type": "application/json"
    }
    global channel
    if ctx.author.voice is not None:
        if ctx.author.voice.channel is not None:
            channel = ctx.author.voice.channel.id
        else:
            await ctx.send("Зайдите в канал")
    else:
        await ctx.send("Зайдите в канал")
    response = requests.post(f"https://discord.com/api/v8/channels/{channel}/invites", data=json.dumps(data),
                             headers=headers)

    link = json.loads(response.content)
    await ctx.send(f"https://discord.com/invite/{link['code']}")


@client.command(aliases=['stats', 'ss'])
async def server_stats(ctx: discord.ext.commands.Context):
    embed = discord.embeds.Embed()

    members = ctx.guild.members
    Botsies = 0
    Realman = 0
    MemberCount = 0
    online = 0
    offline = 0
    idle = 0
    dnd = 0

    for member in members:
        member: discord.member = member
        MemberCount += 1
        if member.bot:
            Botsies += 1
        else:
            Realman += 1

        if member.raw_status == "online":
            online += 1
        elif member.raw_status == "offline":
            offline += 1
        elif member.raw_status == "idle":
            idle += 1
        elif member.raw_status == "dnd":
            dnd += 1

    embed.add_field(name="\n:busts_in_silhouette: Члены :busts_in_silhouette:",
                    value=f"🤖 Боты: {Botsies}\n\n :bust_in_silhouette: Люди: {Realman} \n\n :busts_in_silhouette: Всего: {MemberCount}")
    embed.add_field(name="\nПо статусу",
                    value=f"Онлайн: {online}\n\n оффлайн: {offline} \n\n Не беспокоить: {dnd} \n\n Не активен: {idle}")
    await ctx.send("Стата", embed=embed)


async def RemapOnStart():
    global dataBase
    for guild in client.guilds:
        logger.log(f"Mapping XP on start for {guild}", "RemapOnStart")
        members = guild.members
        for member in members:
            logger.log(f"Mapped XP on start for {member} with id {member.id}", "RemapOnStart")
            if dataBase.get(member.id) is None:
                dataBase[member.id] = 0
        save()


@client.event
async def on_connect():
    await RemapOnStart()


@client.event
async def on_ready():
    await RemapOnStart()


init()

# Connect
client.run(Token)
