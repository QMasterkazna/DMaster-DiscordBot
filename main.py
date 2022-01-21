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

    print(progressbar)
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
        print(dataBase)
        input.close()
    except EOFError:
        print(col.Fore.RED + "Файл пустой")
    except FileNotFoundError:
        print(col.Fore.RED + "Файл не найден")


def save():
    output = open(filename, "wb")

    pkl.dump(dataBase, output, 2)
    print(col.Fore.GREEN + "База Данных сохранена ♥")


def AddXpToUser(amount, UserId):
    global dataBase
    dataBase[UserId] += amount
    print(dataBase[UserId])
    save()


def GetUserXp(UserId):
    print(UserId)
    print(dataBase)
    return dataBase[UserId]


@client.command(pass_context=True, aliases=["xpmap"])
@commands.has_permissions(administrator=True)
async def MapXp(ctx):
    global dataBase
    members = ctx.guild.members
    for member in members:
        print(member.id)
        if dataBase.get(member.id) is None:
            dataBase[member.id] = 0
    save()


@client.command(pass_context=True, aliases=["addxp"])
@commands.has_permissions(administrator=True)
async def AddXp(ctx, member: discord.Member, points: int):
    print(ctx.message.content)
    print(member.id)
    print(points)
    AddXpToUser(points, member.id)


# clear message
@client.command(pass_context=True, aliases=["очистка", 'clear'])
@commands.has_permissions(administrator=True)
async def Clear(ctx, amount=100):
    await ctx.channel.purge(limit=amount)


# clear command
@client.command(pass_context=True, aliases=['билли', 'интим'])
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


# Фильтр чата
@client.event
async def on_message(message):
    author = message.author
    bad_word = ['блядь', 'сука', 'ебал', 'заебал', 'пошел нахуй', 'иди в задницу', 'блять', 'бля', 'иди нахуй',
                'пошел нахуй', 'хуй', 'охуел', 'oxyeл', 'ебал', 'oхyел', 'охyeл', 'oxуел', 'иди нaxyй', 'иди наxуй',
                'иди нахyй', "соси", 'иди нах', 'Иди нах', 'пошёл нахуй', 'Пошёл нахуй']
    await client.process_commands(message)
    msg = message.content.lower()
    if msg in bad_word:
        await message.delete()
        a = random.randint(1, 2)
        if a == 1:
            await message.author.send(f'{message.author.name},Мы культурные, не матерись, иначе проникну в твой Ass')
        elif a == 2:
            await message.author.send(f'{message.author.name},В следущий раз твой Ass будет в опасности')
        else:
            await message.author.send(f'{message.author.name},Плохой мальчик твой Ass в опасности')
        AddXpToUser(-10, message.author.id)


    elif not (message.content == "" or message.content is None or message.content == "\n"):
        print(message.content)
        if not (message.content.lower().startswith(";/")):
            AddXpToUser(1, message.author.id)
    else:
        print(message.content)


@client.command(aliases=['пошли в gym', 'хочу в gym'])
async def gym(ctx):
    author = ctx.message.author
    await ctx.send(f'♂{author.mention},Пошли со мной в Gym♂')


# mute
@client.command(pass_context=True, aliases=['мьют'])
@commands.has_permissions(administrator=True)
async def mute(ctx, member: discord.Member, time: int = 60):
    await ctx.channel.purge(limit=1)
    mute_role = discord.utils.get(ctx.message.guild.roles, name='Muted')
    await member.add_roles(mute_role)
    await ctx.send(f"{member.mention} Соси молча, и пей моё Wee wee")
    await asyncio.sleep(time)
    await member.remove_roles(mute_role)


# carduser
@client.command(aliases=['я', 'карта'])
async def profile(ctx, member: discord.Member = None):
    # TODO: make database work properly
    # TODO: Заставить базу данных работать правильно
    if member is None:
        member = ctx.author
    print(type(member))

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
    emb.add_field(name='{}очистка'.format(command_prefix), value='Очистка чата')
    emb.add_field(name='{}бан'.format(command_prefix), value='Заблокировать пользователя')
    emb.add_field(name='{}кик'.format(command_prefix), value='Выгнать пользователя')
    emb.add_field(name='{}разбан'.format(command_prefix), value='Разблокировать пользователя')
    emb.add_field(name="{}мьют".format(command_prefix), value='Замьютить пользователя')
    emb.add_field(name='{}размьют'.format(command_prefix), value='Размьютить пользователя')
    emb.add_field(name='{}Билли'.format(command_prefix), value='Ну введи посмари что выдает')
    emb.add_field(name='{}играть'.format(command_prefix), value='Ну введи посмари что выдает')
    emb.add_field(name='{}gym'.format(command_prefix), value='Ну введи посмари что даст, отказываться нельзя')
    emb.add_field(name='{}run'.format(command_prefix), value='Бежим вместе с Билли')
    emb.add_field(name='{}play'.format(command_prefix),
                  value='Запустить музыку')
    emb.add_field(name='{}Привет'.format(command_prefix), value='По здароваться с Билли')
    emb.add_field(name='{}watch'.format(command_prefix), value='Смотреть ютуб')
    emb.add_field(name='{}pause'.format(command_prefix), value='Остановить музыку')
    emb.add_field(name='{}resume'.format(command_prefix), value='Продолжить музыку')
    emb.add_field(name='{}disconnect'.format(command_prefix), value='Чтобы Бот отключился от голосового')
    emb.add_field(name='{}cum'.format((command_prefix)), value='Введи но будь осторожен')
    emb.add_field(name='{}profile'.format((command_prefix)), value='Посмотреть на сколько ты прокачен')
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
    print(json.loads(response.content))
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

    embed.add_field(name="\n:busts_in_silhouette: Члены :busts_in_silhouette:", value=f"🤖 Боты: {Botsies}\n\n :bust_in_silhouette: Люди: {Realman} \n\n :busts_in_silhouette: Всего: {MemberCount}")
    embed.add_field(name="\nПо статусу", value=f"Онлайн: {online}\n\n оффлайн: {offline} \n\n Не беспокоить: {dnd} \n\n Не активен: {idle}")

    await ctx.send("Стата", embed=embed)


init()

DrawProgressBar(0.56)
DrawProgressBar(0.20)
DrawProgressBar(0.75)

# Connect
client.run(Token)
