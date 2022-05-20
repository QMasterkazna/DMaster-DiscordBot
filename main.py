import discord
import random
from discord.ext import commands
import requests
import asyncio
import json
from datetime import datetime
import ConfigConstants as CC
import sqlite3
from music_module import Music
import math
import requests
from bs4 import BeautifulSoup

command_prefix = ';/'
Token = CC.Token
client = commands.Bot(command_prefix=command_prefix, intents=discord.Intents.all())
client.remove_command('help')
filename = CC.filename
dataBase = {}

playlist = []
isPlayingNow = False

connection = sqlite3.connect('bank.db')
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
            xp BITINT,
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
                cursor.execute(f"INSERT INTO users VALUES ('{member}',{member.id}, 0, 0, 1,0, {guild.id})")
            else:
                pass
    connection.commit()
    print('Я ПРОСНУЛСЯ МОЙ ГОСПОДИН!')


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


@client.command(aliases=['grab', 'robbery'])
@commands.cooldown(1, 3600, commands.BucketType.user)
async def __grab(ctx, member: discord.Member = None):
    if member is None:
        await ctx.send('Укажите пользователя которого вы хотите ограбить')
        await ctx.message.add_reaction('❎')
    elif member is ctx.author:
        await ctx.send('Нельзя грабить самого себя')
    else:
        rand = random.randint(1, 2)
        rand1 = rand
        print(rand1)
        if rand1 == 1:
            cash = random.randint(1, 100)
            cash1 = cash
            cursor.execute('UPDATE users SET cash = cash - {} WHERE id = {}'.format(cash1, member.id))
            cursor.execute('UPDATE users SET cash = cash + {} WHERE id = {}'.format(cash1, ctx.author.id))
            await ctx.send('Вы успешно ограбили {}, на {}'.format(member, cash1))
            await ctx.message.add_reaction('✅')
            connection.commit()
        else:
            await ctx.reply('Вы не успешно ограбили {}'.format(member))


@client.command(aliases=['removerole', 'remove-role'])
@commands.has_permissions(administrator=True)
async def __remove_role(ctx, role: discord.Role = None):
    if role is None:
        await ctx.send(f"**{ctx.author}**, укажите роль, которую вы желайте удалить")
        await ctx.message.add_reaction('❎')
    else:
        cursor.execute("DELETE FROM shop WHERE role_id = {}".format(role.id))
        await ctx.message.add_reaction('✅')
    connection.commit()


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
    await ctx.send(embed=embed)
    connection.commit()


@client.command(aliases=['buy', 'buy-role'])
async def __buy(ctx, role: discord.Role = None):
    time = datetime.now()
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
            embed = discord.embeds.Embed(title=f'пользователь: **{ctx.author}**, приобрел роль: {role}')
            embed.add_field(
                name= 'Вы приобрели роль: ',
                value = f'{role}'
            )
            embed.add_field(
                name = 'Время приобретения: ',
                value = f'День: {time.day} Часы: {time.hour} Минуты: {time.minute} Секунды: {time.second}',
                inline = False
            )
            await ctx.send(embed=embed)


@client.event
async def on_member_join(member):
    if cursor.execute(f"SELECT id FROM users WHERE id = {member.id}").fetchall() is None:
        cursor.execute(f"INSERT INTO users VALUES ('{member}',{member.id}, 0, 0, 1, {member.guild.id})")
        connection.commit()


@client.command(aliases=['balance', 'cash'])
async def ___balance(ctx, member: discord.Member = None):
    if member is None:
        await ctx.send(embed=discord.Embed(
            description=f"""Баланс пользователя **{ctx.author}** составляет **{cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]}**:coin:"""
        ))
    else:
        await ctx.send(embed=discord.Embed(
            description=f"""Баланс пользователя **{member}** составляет **{cursor.execute("SELECT cash FROM users WHERE id = {}".format(member.id, )).fetchone()[0]}**:coin:"""
        ))


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = ('**Вы уже выполняли это действие**, пожалуйста повторите через {:.2f}s'.format(error.retry_after))
        await ctx.send(msg)


@client.command(aliases=['work', 'работа'])
@commands.cooldown(1, 600, commands.BucketType.user)
async def __work(ctx):
    zp = random.randint(1, 1000)
    zp1 = zp
    cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(zp1, ctx.author.id))
    connection.commit()

    embed = discord.Embed(title='Работа')
    embed.add_field(
        name='Вы заработали:',
        value=f'{zp1}',
        inline=False
    )
    await ctx.send(embed=embed)
    await ctx.message.add_reaction('✅')


def LevelToXp(level):
    return 3 * level ** 2


# def Difference(xp):
#     return LevelToXp(math.ceil(math.sqrt(xp / 3))) - (xp - 1)


@client.event
async def on_message(message):
    if message.author.bot:
        print('Алё это бот')
    elif ';/' in message.content:
        print('Алё это команда')
    else:
        cursor.execute("UPDATE users SET xp = xp + {} WHERE id = {}".format(1, message.author.id))  # Обновляем xp на +1
    connection.commit()
    await client.process_commands(message)


@client.command(aliases=['addxp', 'Addxp', 'add-xp'])
@commands.has_permissions(administrator=True)
async def __add_xp(ctx, member: discord.Member = None, exp: int = None):
    if member is None:
        await ctx.send('Укажите пользователя')
        await ctx.message.add_reaction('❎')
    elif exp is None:
        await ctx.send('Укажите количество exp которое вы хотите добавить')
        await ctx.message.add_reaction('❎')
    else:
        cursor.execute("UPDATE users SET xp = xp + {} WHERE id = {}".format(exp, member.id))
        await ctx.send('Я обновил exp у данного пользователя: {} exp'.format(member))
        await ctx.message.add_reaction('✅')
        connection.commit()


@client.command(aliases=['deletexp', 'DeleteXp'])
@commands.has_permissions(administrator=True)
async def __deletexp(ctx, member: discord.Member = None, exp: int = None):
    if member is None:
        await ctx.send('Укажите пользователя')
        await ctx.message.add_reaction('❎')
    elif exp is None:
        await ctx.send('Укажите количество exp которое вы хотите убрать')
        await ctx.message.add_reaction('❎')
    else:
        cursor.execute("UPDATE users SET xp = xp - {} WHERE id = {}".format(exp, member.id))
        await ctx.send('Я убрал у данного пользователя: {}, столько exp: {}'.format(member, exp))
        await ctx.message.add_reaction('✅')
        connection.commit()


url = 'https://habr.com/ru/news/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.141 Safari/537.36'}


def parser():
    global convert
    global author
    global zaga
    global time
    full_page = requests.get(url, headers=headers)

    soup = BeautifulSoup(full_page.content, "html.parser")

    author = soup.find('a', {'class': "tm-user-info__username"})
    zaga = soup.find('a', {'class': "tm-article-snippet__title-link"})
    time = soup.find('span', {'class':"tm-article-snippet__datetime-published"})

@client.command(aliases=['news', 'News', 'Новости', 'новости'])
async def __news(ctx):
    parser()
    embed = discord.Embed(title='Материал был взят из habr.com', url='https://habr.com/ru/news/')
    embed.add_field(
        name=f'{author.text}',
        value=f'{zaga.text} \n время публикации: **{time.text}**',
        inline=False
    )
    await ctx.reply(embed=embed)


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
@commands.cooldown(1, 5000, commands.BucketType.user)
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


# clear message
@client.command(pass_context=True, aliases=["очистка", 'clear'])
@commands.has_permissions(administrator=True)
async def Clear(ctx, amount=100):
    if amount is None:
        await ctx.reply('Укажите количество')
    else:
        await ctx.channel.purge(limit=amount)


# Kick
@client.command(pass_context=True, aliases=['кик'])
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member = None, *, reason=None):
    time= datetime.now()
    if member is None:
        await ctx.send('Укажите пользователя для того чтобы его кикнуть')
    else:
        embed = discord.embeds.Embed(title='Кикнут')
        embed.add_field(name='Время: ', value=f'часы: {time.hour} \n минуты: {time.minute} \n секунды: {time.second}')
        embed.add_field(name='Пользователь: ', value=f'{member} , \n был кикнут')
        embed.add_field(name='Причина: ', value=f'{reason}')
        await member.kick(reason=reason)
        await ctx.send(embed=embed)


# ban
@client.command(pass_context=True, aliases=["бан"])
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member = None, *, reason=None):
    if member is None:
        await ctx.send('Укажите пользователя, которого вы хотите забанить')
        await ctx.message.add_reaction('❎')

    await member.ban(reason=reason)
    time = datetime.now()
    embed = discord.embeds.Embed(title=f'Забанен')
    embed.add_field(
        name='Пользователь: ',
        value=f'{member.mention}'
    )
    embed.add_field(
        name='Время бана:',
        value=f'часы: {time.hour} \n минуты: {time.minute} \n секунды: {time.second}'
    )
    embed.add_field(
        name='Причина:',
        value=f'{reason}'
    )
    embed.set_author(
        name=f"{member}",
        icon_url=f'{member.avatar_url}'
    )
    await ctx.send(embed=embed)


# unban
@client.command(pass_context=True, aliases=["разбан"])
@commands.has_permissions(administrator=True)
async def unban(ctx, *, member):
    time = datetime.now()
    banned_users = await ctx.guild.bans()
    for ban_entry in banned_users:
        user = ban_entry.user
        await ctx.guild.unban(user)
        embed = discord.embeds.Embed(title=f'Разбанен')
        embed.add_field(
            name='Пользователь: ',
            value=f'{user.mention}'
        )
        embed.add_field(
            name='Время разбана',
            value=f'часы: {time.hour} \n минуты: {time.minute} \n секунды: {time.second}'
        )
        await ctx.send(embed=embed)
        return


# mute
@client.command(pass_context=True, aliases=['мьют'])
@commands.has_permissions(administrator=True)
async def mute(ctx, member: discord.Member = None, reason=None, time: int = None):
    time1 = datetime.now()
    if member is None:
        await ctx.send('Укажите пользователя чтобы его замьютить')
    mute_role = discord.utils.get(ctx.message.guild.roles, name='Muted')
    if time is None:
        await member.add_roles(mute_role)
        embed = discord.embeds.Embed(title='Мьют выдан')
        embed.add_field(name='Пользователю: ', value=f'{member.mention}')
        embed.add_field(name='Время выдачи: ', value=f'{datetime.now()}')
        embed.add_field(name='Причина: ', value=f'{reason}')
        embed.add_field(name='На: ', value=f'часы: {time1.hour} \n минуты: {time1.minute} \n секунды: {time1.second}')
        await ctx.send(embed=embed)
    else:
        await member.add_roles(mute_role)
        embed = discord.embeds.Embed(title='Мьют выдан')
        embed.add_field(name='Пользователю: ', value=f'{member.mention}')
        embed.add_field(name='Время выдачи: ', value=f'часы: {time1.hour} \n минуты: {time1.minute} \n секунды: {time1.second}')
        embed.add_field(name='Причина: ', value=f'{reason}')
        embed.add_field(name='На: ', value=f'{time}')
        await ctx.send(embed=embed)
        await asyncio.sleep(time)
        await member.remove_roles(mute_role)


def XpToLevel(xp):
    return math.floor(math.sqrt(xp / 3))


# carduser
@client.command(aliases=['я', 'карта'])
async def profile(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author
    xp = cursor.execute("SELECT xp FROM users WHERE id = {}".format(member.id)).fetchone()[0]
    emb = discord.embeds.Embed(title=f"{member.name}#{member.discriminator}")
    emb.add_field(
        name=f"id: {member.id}", value=f"status:{member.status}"
    )
    emb.add_field(
        name=f"XP:{cursor.execute('SELECT xp FROM users WHERE id = {}'.format(member.id)).fetchone()[0]} ",
        value=f"Level: {XpToLevel(xp)}"
    )
    emb.add_field(
        name='Rep',
        value=f'{cursor.execute("SELECT rep FROM users WHERE id = {}".format(member.id)).fetchone()[0]}'
    )
    emb.set_image(url=member.avatar_url)
    await ctx.send(embed=emb)


# unmute
@client.command(aliases=['размьют'])
@commands.has_permissions(administrator=True)
async def unmute(ctx, member: discord.Member = None):
    time = datetime.now()
    if member is None:
        await ctx.send('Укажите пользователя которого хотите размьютить')
    else:
        mute_role = discord.utils.get(ctx.message.guild.roles, name='Muted')
        await member.remove_roles(mute_role)
        embed = discord.embeds.Embed(title='Размьют')
        embed.add_field(name='Пользователь: ', value=f'{member.mention}')
        embed.add_field(name='Время: ', value=f'часы: {time.hour} \n минуты: {time.minute} \n секунды: {time.second}')
        await ctx.send(embed=embed)


# Silence useless bug reports messages

client.add_cog(Music(client))


# create.DeleteText
@client.command()
@commands.has_permissions(administrator=True)
async def voice(ctx, name, channel: int = None):
    guild = ctx.message.guild
    await guild.create_voice_channel(name=name, category=client.get_channel(channel))
    await ctx.send(f"Я создал этот {name} голосовой канал")


@client.command()
@commands.has_permissions(administrator=True)
async def text(ctx, name = None, channel: int = None):
    guild = ctx.message.guild
    await guild.create_text_channel(name=name, category=client.get_channel(channel))
    await ctx.send(f"Я создал этот {name} текстовый канал")


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


@client.command()
async def hmusic(ctx):
    embed = discord.Embed(title='Комманды по музыке')
    embed.add_field(name='{}play [название или ссылка на видео]'.format(command_prefix), value='Запуск музыки')
    embed.add_field(name='{}leave'.format(command_prefix), value='Бот выйдет из голосового')
    embed.add_field(name='{}skip'.format(command_prefix), value='Пропустить музыку')
    embed.add_field(name='{}join'.format(command_prefix), value='Добавить бота в голосовой канал')
    embed.add_field(name='{}now'.format(command_prefix), value='Посмотреть что сейчас играет')
    await ctx.send(embed=embed)


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
    emb.add_field(name='{}stats'.format(command_prefix), value='Статистика сервера')
    emb.add_field(name='{}watch'.format(command_prefix), value='Смотреть ютуб')
    emb.add_field(name='{}profile'.format(command_prefix), value='Профиль пользователя')
    emb.add_field(name='{}hmusic'.format(command_prefix), value='Помощь в музыке')
    emb.add_field(
        name='{}balance/cash'.format(command_prefix),
        value='Посмотреть баланс кошелька'
    )
    emb.add_field(
        name='{}work'.format(command_prefix),
        value='Работа, для заработка денег'
    )
    emb.add_field(
        name='{}shop'.format(command_prefix),
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
    emb.add_field(
        name='{}rep'.format(command_prefix),
        value='Добавить репутацию пользователю'
    )
    await ctx.send(embed=emb)


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
    embed.set_footer(text=str(ctx.message.guild.name), icon_url=ctx.guild.icon_url)
    embed.add_field(name="\n:busts_in_silhouette: Члены :busts_in_silhouette:",
                    value=f"🤖 Боты: {Botsies}\n\n :bust_in_silhouette: Люди: {Realman} \n\n :busts_in_silhouette: Всего: {MemberCount}")
    embed.add_field(name="\nПо статусу",
                    value=f"Онлайн: {online}\n\n оффлайн: {offline} \n\n Не беспокоить: {dnd} \n\n Не активен: {idle}")
    await ctx.send("Стата", embed=embed)


# Connect
client.run(Token)
