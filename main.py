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

connection = sqlite3.connect('Bank.db')
cursor = connection.cursor()


# dungeon coin
@client.event
async def on_ready():
    cursor.execute("""CREATE TABLE IF NOT EXISTS users(
        name TEXT,
        id INT,
        cash BIGINT,
        rep INT,
        lvl INT,
        server_id INT
    )""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS shop(
        role_id INT,
        id INT,
        cost BIGINT
    )""")
    for guild in client.guilds:
        for member in guild.members:
            if cursor.execute(f"SELECT id FROM users WHERE id = {member.id}").fetchone() is None:
                cursor.execute(f"INSERT INTO users VALUES ('{member}',{member.id}, 0, 0, 1, {guild.id})")
            else:
                pass
    connection.commit()


@client.command(aliases=['addshop', 'add-shop'])
@commands.has_permissions(administrator=True)
async def __add_shop(ctx, role: discord.Role = None, cost: int = None):
    if role is None:
        await ctx.send(f"**{ctx.author}**, укажите роль, которую вы желаете внести в магазин")
        await ctx.message.add_reaction('❎')
    else:
        if cost is None:
            await ctx.send(f"**{ctx.author}**, укажите стоимость роли")
            await ctx.message.add_reaction('❎')
        elif cost < 0:
            await ctx.send(f"**{ctx.author}**, стоимость роли не может быть такой маленькой")
            await ctx.message.add_reaction('❎')
        else:
            cursor.execute("INSERT INTO shop VALUES ({},{},{})".format(role.id, ctx.guild.id, cost))
            connection.commit()
            await ctx.message.add_reaction('✅')


@client.command(aliases=['removerole', 'remove-role'])
@commands.has_permissions(administrator=True)
async def __remove_role(ctx, role: discord.Role = None):
    if role is None:
        await ctx.send(f"**{ctx.author}**, укажите роль, которую вы желайте удалить")
        await ctx.message.add_reaction('❎')
    else:
        cursor.execute("DELETE FROM shop WHERE role_id = {}".format(role.id))
        await ctx.message.add_reaction('✅')


@client.command(aliases=['shop'])
async def __shop(ctx):
    embed = discord.Embed(title='Магазин Ролей')
    for row in cursor.execute("SELECT role_id, cost FROM shop WHERE id = {}".format(ctx.guild.id)):
        if ctx.guild.get_role(row[0]) != None:
            embed.add_field(
                name=f"Стоимость {row[1]}",
                value=f"Вы приобрете роль {ctx.guild.get_role(row[0]).mention}",
                inline=False
            )
        else:
            pass
    await ctx.send(embed=embed)


@client.command(aliases=['buy', 'buy-role'])
async def __buy(ctx, role: discord.Role = None):
    if role is None:
        await ctx.send(f"**{ctx.author}**, укажите роль, которую вы желаете приобрести")
    else:
        if role in ctx.author.roles:
            await ctx.send(f"**{ctx.author}**, у вас уже есть данная роль")
            await ctx.message.add_reaction('❎')
        elif cursor.execute("SELECT cost FROM shop WHERE role_id = {}".format(role.id)).fetchone()[0] > \
                cursor.execute("SELECT cash FROM users WHERE id ={}".format(ctx.author.id)).fetchone()[0]:
            await ctx.send(f"**{ctx.author}**,у вас недостаточно средств для покупки")
            await ctx.message.add_reaction('❎')
        else:
            await ctx.author.add_roles(role)
            cursor.execute("UPDATE users SET cash = cash - {0} WHERE id = {1}".format(
                cursor.execute("SELECT cost FROM shop WHERE role_id = {}".format(role.id)).fetchone()[0],
                ctx.author.id))
            connection.commit()
            await ctx.message.add_reaction('✅')


@client.event
async def on_member_join(member):
    if cursor.execute(f"SELECT id FROM users WHERE id = {member.id}").fetchone() is None:
        cursor.execute(f"INSERT INTO users VALUES ('{member}',{member.id}, 0, 0, 1, {member.guild.id})")
        connection.commit()
    else:
        pass


@client.command(aliases=['balance', 'cash'])
async def ___balance(ctx, member: discord.Member = None):
    if member is None:
        await ctx.send(embed=discord.Embed(
            description=f"""Баланс пользователя **{ctx.author}** составляет **{cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]}**:coin:"""
        ))
    else:
        await ctx.send(embed=discord.Embed(
            description=f"""Баланс пользователя **{member}** составляет **{cursor.execute("SELECT cash FROM users WHERE id = {}".format(member.id)).fetchone()[0]}**:coin:"""
        ))


@client.command(aliases=['work', 'работа'])
async def __work(ctx):
    zp = random.randint(1, 100)
    cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(zp, ctx.author.id))
    connection.commit()

    embed = discord.Embed(title='Работа')
    embed.add_field(
        name='Ваш баланс:',
        value=f'{cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]}',
        inline=False
    )
    await ctx.send(embed=embed)


@client.command(aliases=['award'])
@commands.has_permissions(administrator=True)
async def __award(ctx, member: discord.Member = None, amount: int = None):
    if member is None:
        await ctx.send(f"**{ctx.author}**, укажите пользователя, которому желаете выдать определенную сумму")
        await ctx.message.add_reaction('❎')
    else:
        if amount is None:
            await ctx.send(f"**{ctx.author}**, укажите сумму которую выхотите выдать")
            await ctx.message.add_reaction('❎')
        elif amount < 1:
            await ctx.send(f"**{ctx.author}**,укажите сумму больше 1 :coin:")
            await ctx.message.add_reaction('❎')
        else:
            cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(amount, member.id))
            connection.commit()
            await ctx.message.add_reaction('✅')


@client.command(aliases=['take'])
@commands.has_permissions(administrator=True)
async def __take(ctx, member: discord.Member = None, amount=None):
    if member is None:
        await ctx.send(f"**{ctx.author}**, укажите пользователя, которому желаете отнять определенную сумму")
        await ctx.message.add_reaction('❎')
    else:
        if amount is None:
            await ctx.send(f"**{ctx.author}**, укажите сумму которую выхотите отнять")
            await ctx.message.add_reaction('❎')
        elif amount == 'all':
            cursor.execute("UPDATE users SET cash = {} WHERE id = {}".format(0, member.id))
            connection.commit()
            await ctx.message.add_reaction('✅')

        elif int(amount) < 1:
            await ctx.send(f"**{ctx.author}**,укажите сумму больше 1 :coin:")
            await ctx.message.add_reaction('❎')
        else:
            cursor.execute("UPDATE users SET cash = cash - {} WHERE id = {}".format(int(amount), member.id))
            connection.commit()
            await ctx.message.add_reaction('✅')


@client.command(aliases=['rep', '+rep'])
async def __rep(ctx, member: discord.Member = None):
    if member is None:
        await ctx.send(f"**{ctx.author}**, укажите участника сервера")
    else:
        if member.id == ctx.author.id:
            await ctx.send(f'**{ctx.author}**, вы не можете указать самого себя')
        else:
            cursor.execute("UPDATE users SET rep = rep + {} WHERE id = {}".format(1, member.id))
            connection.commit()
            await ctx.message.add_reaction('✅')


@client.command(aliases=['lb', 'leaderboard'])
async def __leaderboard(ctx):
    embed = discord.Embed(title='Топ 10 сервера')
    counter = 0
    for row in cursor.execute(
            "SELECT name, cash FROM users WHERE server_id = {} ORDER BY cash DESC LIMIT 10".format(ctx.guild.id)):
        counter += 1
        embed.add_field(
            name=f"# {counter} | {row[0]}",
            value=f"Баланс: {row[1]}",
            inline=False
        )
    await ctx.send(embed=embed)


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


# # carduser
# @client.command(aliases=['я', 'карта'])
# async def profile(ctx, member: discord.Member = None):
#
#     if member is None:
#         member = ctx.author
#
#     emb = discord.embeds.Embed(title=f"{member.name}#{member.discriminator}")
#     emb.add_field(name=f"id: {member.id}", value=f"status:{member.status}")
#     emb.add_field(name=f"XP: {dataBase.get(member.id)}", value=f"Level {FindLevelByXp(dataBase.get(member.id))}")
#     emb.add_field(name=f'Level Progress',
#                   value=f"{DrawProgressBar((dataBase.get(member.id)) / (CalcXpByFormula(FindLevelByXp(dataBase.get(member.id)))))}",
#                   inline=False)
#     emb.set_image(url=member.avatar_url)
#     await ctx.send(embed=emb)
#

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


# create.DeleteText
@client.command()
@commands.has_permissions(administrator=True)
async def voice(ctx, name, channel: int = None):
    guild = ctx.message.guild
    await guild.create_voice_channel(name=name, category=client.get_channel(channel))
    await ctx.send(f"Я создал этот {name} голосовой канал для тебя пупсик :Billy_herrington: ")


@client.command()
@commands.has_permissions(administrator=True)
async def text(ctx, name, channel: int = None):
    guild = ctx.message.guild
    await guild.create_text_channel(name=name, category=client.get_channel(channel))
    await ctx.send(f"Я создал этот {name} текстовый канал для тебя пупсик :Billy_herrington:")


# deleteText.Voice
@client.command()
@commands.has_permissions(administrator=True)
async def deletevoice(ctx, voicechannel: discord.VoiceChannel):
    await voicechannel.delete()
    await ctx.send(f"Я удалил это канал")


@client.command()
@commands.has_permissions(administrator=True)
async def deletetext(ctx, channel: discord.TextChannel):
    await channel.delete()
    await ctx.send(f"Я удалил этот канал")


# help
@client.command(pass_context=True, aliases=['Помощь', 'Help'])
async def help(ctx):
    emb = discord.Embed(title='Навигация по командам:')
    emb.add_field(name='{}clear'.format(command_prefix), value='Очистка чата')
    emb.add_field(name='{}ban'.format(command_prefix), value='Забанить пользователя')
    emb.add_field(name='{}unban'.format(command_prefix), value='Разбанить пользователя')
    emb.add_field(name='{}mute'.format(command_prefix), value='Замьютить пользователя')
    emb.add_field(name='{}unmute'.format(command_prefix), value='Размьютить пользователя')
    emb.add_field(name='{}kick'.format(command_prefix), value='Кикнуть пользователя')
    emb.add_field(name='{}text'.format(command_prefix), value='Создать текстовый канал')
    emb.add_field(name='{}voice'.format(command_prefix), value='Создать голосовой канал')
    emb.add_field(name='{}deletetext'.format(command_prefix), value='Удалить канал')
    emb.add_field(name='{}deletevoice'.format(command_prefix), value='Удалить голосовой')
    emb.add_field(
        name='{}Играть,\n {}Привет,\n {}Билли,\n {}gym,\n {}cum,\n {}run'.format(command_prefix, command_prefix,
                                                                                 command_prefix, command_prefix,
                                                                                 command_prefix, command_prefix),
        value='Команды для приколюх')
    emb.add_field(name='{}stats'.format(command_prefix), value='Статистика сервера')
    emb.add_field(name='{}watch'.format(command_prefix), value='Смотреть ютуб')
    emb.add_field(name='{}profile'.format(command_prefix), value='Профиль пользователя')
    emb.add_field(
        name = '{}balance/cash'.format(command_prefix),
        value= 'Посмотреть баланс кошелька'
    )
    emb.add_field(
        name= '{}work'.format(command_prefix),
        value = 'Работа, для заработка денег'
    )
    emb.add_field(
        name= '{}shop'.format(command_prefix),
        value='Открыть магазин ролей'
    )
    emb.add_field(
        name='{}buy'.format(command_prefix),
        value='Купить роль'
    )
    emb.add_field(
        name='{}addshop'.format(command_prefix),
        value='Добавить роль в магазин, чтобы её оттуда убрать {}removerole'.format(command_prefix)
    )
    await ctx.send(embed=emb)
    emb.add_field(
        name='{}rep'.format(command_prefix),
        value='Добавить репутацию пользователю'
    )
    emb.add_field(
        name='{}leaderboard'.format(command_prefix),
        value='Посмотреть топ пользователей'
    )


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


R_D2 = "https://habr.com/ru/news/"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'}


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


# Connect
client.run(Token)
