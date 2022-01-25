import discord
from discord.ext import commands
import ConfigConstants as CC
from datetime import datetime
import asyncio
import colorama
command_prefix = ';/'
Token = CC.Token
client = commands.Bot(command_prefix=command_prefix, intents=discord.Intents.all())

@client.command(aliases=['мьют', 'мут'])
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member = None, amout: str = None, *, reason=None):
    times_start = datetime.datetime.today()
    emb_user = discord.Embed(title='**Уведомление - Mute**', color="Red")
    emb_user.add_field(name='**Выдал:**', value=ctx.author.mention, inline=False)
    emb_user.add_field(name='**Причина:**', value=reason, inline=False)
    emb_user.add_field(name='**Длительность:**', value=amout, inline=False)
    emb_user.add_field(name='**Сервер:**', value=ctx.guild.name, inline=False)
    emb_user.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')

    emb_user_stop = discord.Embed(title='**Уведомление - Unmute**', color="Red")
    emb_user_stop.add_field(name='**Снял:**', value=ctx.author.mention, inline=False)
    emb_user_stop.add_field(name='**Сервер:**', value=ctx.guild.name, inline=False)
    emb_user_stop.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')
    mute_role = discord.utils.get(ctx.message.guild.roles, id=886953646582022165)

    if member is None:
        emb = discord.Embed(title='[ERROR] Mute', description=f'{ctx.author.mention}, Укажите пользователя!', color="Red")
        emb.add_field(name='Пример:', value=f'{ctx.prefix}мьют [@участник] <время(с, м, ч, д)> [причина]', inline=False)
        emb.add_field(name='Пример 1:', value=f'{ctx.prefix}мьют @Xpeawey 1ч пример')
        emb.add_field(name='Время:', value=f'с - секунды\nм - минуты\nч - часы\nд - дни')

        await ctx.send(embed=emb)
    else:
        end_time = amout[-1:]
        time = int(amout[:-1])
        if time <= 0:
            emb = discord.Embed(title='[ERROR] Mute',
                                description=f'{ctx.author.mention}, Время не может быть меньше 1!', color="Red")
            emb.add_field(name='Пример:', value=f'{ctx.prefix}мьют [@участник] <время> [причина]', inline=False)
            emb.add_field(name='Пример 1:', value=f'{ctx.prefix}мьют @Xpeawey 1ч пример')
            emb.add_field(name='Время:', value=f'с - секунды\nм - минуты\nч - часы\nд - дни')

            await ctx.send(embed=emb)
        else:
            if end_time == 'с':
                if reason is None:
                    emb = discord.Embed(title=f'**System - Mute**', color="Red")
                    emb.add_field(name='Выдал:', value=ctx.author.mention, inline=False)
                    emb.add_field(name='Нарушитель:', value=member.mention, inline=False)
                    emb.add_field(name='ID нарушителя:', value=member.id, inline=False)
                    emb.add_field(name='Причина:', value='Не указано', inline=False)
                    emb.add_field(name='Длительность:', value='{} секунд'.format(time))
                    emb.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')
                    await member.add_roles(mute_role)
                    await ctx.send(embed=emb)
                    await member.send(embed=emb_user)
                    await asyncio.sleep(time)
                    await member.remove_roles(mute_role)
                    await member.send(embed=emb_user_stop)
                else:
                    emb = discord.Embed(title=f'**System - Mute**', color="Red")
                    emb.add_field(name='Выдал:', value=ctx.author.mention, inline=False)
                    emb.add_field(name='Нарушитель:', value=member.mention, inline=False)
                    emb.add_field(name='ID нарушителя:', value=member.id, inline=False)
                    emb.add_field(name='Причина:', value=reason, inline=False)
                    emb.add_field(name='Длительность:', value='{} секунд'.format(time))
                    emb.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')
                    await member.add_roles(mute_role)
                    await ctx.send(embed=emb)
                    await member.send(embed=emb_user)
                    await asyncio.sleep(time)
                    await member.remove_roles(mute_role)
                    await member.send(embed=emb_user_stop)
            elif end_time == 'м':
                if reason is None:
                    emb = discord.Embed(title=f'**System - Mute**', color="Red")
                    emb.add_field(name='Выдал:', value=ctx.author.mention, inline=False)
                    emb.add_field(name='Нарушитель:', value=member.mention, inline=False)
                    emb.add_field(name='ID нарушителя:', value=member.id, inline=False)
                    emb.add_field(name='Причина:', value='Не указано', inline=False)
                    emb.add_field(name='Длительность:', value='{} минут'.format(time))
                    emb.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')
                    await member.add_roles(mute_role)
                    await ctx.send(embed=emb)
                    await member.send(embed=emb_user)
                    await asyncio.sleep(time * 60)
                    await member.remove_roles(mute_role)
                    await member.send(embed=emb_user_stop)
                else:
                    emb = discord.Embed(title=f'**System - Mute**', color="Red")
                    emb.add_field(name='Выдал:', value=ctx.author.mention, inline=False)
                    emb.add_field(name='Нарушитель:', value=member.mention, inline=False)
                    emb.add_field(name='ID нарушителя:', value=member.id, inline=False)
                    emb.add_field(name='Причина:', value=reason, inline=False)
                    emb.add_field(name='Длительность:', value='{} минут'.format(time))
                    emb.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')
                    await member.add_roles(mute_role)
                    await ctx.send(embed=emb)
                    await member.send(embed=emb_user)
                    await asyncio.sleep(time * 60)
                    await member.remove_roles(mute_role)
                    await member.send(embed=emb_user_stop)
            elif end_time == 'ч':
                if reason is None:
                    if time == '1':

                        emb = discord.Embed(title=f'**System - Mute**', color="Red")
                        emb.add_field(name='Выдал:', value=ctx.author.mention, inline=False)
                        emb.add_field(name='Нарушитель:', value=member.mention, inline=False)
                        emb.add_field(name='ID нарушителя:', value=member.id, inline=False)
                        emb.add_field(name='Причина:', value='Не указано', inline=False)
                        emb.add_field(name='Длительность:', value='{} час'.format(time))
                        emb.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')
                        await member.add_roles(mute_role)
                        await ctx.send(embed=emb)
                        await member.send(embed=emb_user)
                        await asyncio.sleep(time * 60 * 60)
                        await member.remove_roles(mute_role)
                        await member.send(embed=emb_user_stop)
                    elif time == '4' or time == '3' or time == '2':
                        emb = discord.Embed(title=f'**System - Mute**', color="Red")
                        emb.add_field(name='**Выдал:**', value=ctx.author.mention, inline=False)
                        emb.add_field(name='**Нарушитель:**', value=member.mention, inline=False)
                        emb.add_field(name='**ID нарушителя:**', value=member.id, inline=False)
                        emb.add_field(name='**Причина:**', value='Не указано', inline=False)
                        emb.add_field(name='**Длительность:**', value='{} часов'.format(time))
                        emb.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')
                        await member.add_roles(mute_role)
                        await ctx.send(embed=emb)
                        await member.send(embed=emb_user)
                        await asyncio.sleep(time * 60 * 60)
                        await member.remove_roles(mute_role)
                        await member.send(embed=emb_user_stop)
                    elif time >= '5':
                        emb = discord.Embed(title=f'**System - Mute**', color="Red")
                        emb.add_field(name='**Выдал:', value=ctx.author.mention, inline=False)
                        emb.add_field(name='**Нарушитель:', value=member.mention, inline=False)
                        emb.add_field(name='**ID нарушителя:', value=member.id, inline=False)
                        emb.add_field(name='**Причина:', value='Не указано', inline=False)
                        emb.add_field(name='**Длительность:', value='{} часов'.format(time))
                        emb.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')
                        await member.add_roles(mute_role)
                        await ctx.send(embed=emb)
                        await member.send(embed=emb_user)
                        await asyncio.sleep(time * 60 * 60)
                        await member.remove_roles(mute_role)
                        await member.send(embed=emb_user_stop)
                else:
                    if time == '1':
                        emb = discord.Embed(title=f'**System - Mute**', color='Red')
                        emb.add_field(name='**Выдал:**', value=ctx.author.mention, inline=False)
                        emb.add_field(name='**Нарушитель:**', value=member.mention, inline=False)
                        emb.add_field(name='**ID нарушителя:**', value=member.id, inline=False)
                        emb.add_field(name='**Причина:**', value=reason, inline=False)
                        emb.add_field(name='**Длительность:**', value='{} час'.format(time))
                        emb.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')
                        await member.add_roles(mute_role)
                        await ctx.send(embed=emb)
                        await member.send(embed=emb_user)
                        await asyncio.sleep(time * 60 * 60)
                        await member.remove_roles(mute_role)
                        await member.send(embed=emb_user_stop)
                    elif time == '4' or time == '3' or time == '2':
                        emb = discord.Embed(title=f'**System - Mute**', color='Red')
                        emb.add_field(name='**Выдал:**', value=ctx.author.mention, inline=False)
                        emb.add_field(name='**Нарушитель:**', value=member.mention, inline=False)
                        emb.add_field(name='**ID нарушителя:**', value=member.id, inline=False)
                        emb.add_field(name='**Причина:**', value=reason, inline=False)
                        emb.add_field(name='**Длительность:**', value='{} часа'.format(time))
                        emb.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')
                        await member.add_roles(mute_role)
                        await ctx.send(embed=emb)
                        await member.send(embed=emb_user)
                        await asyncio.sleep(time * 60 * 60)
                        await member.remove_roles(mute_role)
                        await member.send(embed=emb_user_stop)
                    elif time >= '5':
                        emb = discord.Embed(title=f'**System - Mute**', color='Red')
                        emb.add_field(name='**Выдал:**', value=ctx.author.mention, inline=False)
                        emb.add_field(name='**Нарушитель:**', value=member.mention, inline=False)
                        emb.add_field(name='**ID нарушителя:**', value=member.id, inline=False)
                        emb.add_field(name='**Причина:**', value=reason, inline=False)
                        emb.add_field(name='**Длительность:**', value='{} часов'.format(time))
                        emb.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')

                        await member.add_roles(mute_role)
                        await ctx.send(embed=emb)
                        await member.send(embed=emb_user)
                        await asyncio.sleep(time * 60 * 60)
                        await member.remove_roles(mute_role)
                        await member.send(embed=emb_user_stop)
            elif time == 'д':
                if reason is None:
                    emb = discord.Embed(title=f'**System - Mute**', color='Red')
                    emb.add_field(name='**Выдал:**', value=ctx.author.mention, inline=False)
                    emb.add_field(name='**Нарушитель:**', value=member.mention, inline=False)
                    emb.add_field(name='**ID нарушителя:**', value=member.id, inline=False)
                    emb.add_field(name='**Причина:**', value='Не указано', inline=False)
                    emb.add_field(name='**Длительность:**', value='{} день(ей)'.format(time))
                    emb.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')

                    await member.send(embed=emb_user)
                    await member.add_roles(mute_role)
                    await ctx.send(embed=emb)
                    await member.send(embed=emb_user)
                    await asyncio.sleep(time * 60 * 60 * 24)
                    await member.remove_roles(mute_role)
                    await member.send(embed=emb_user_stop)
                else:
                    emb = discord.Embed(title=f'**System - Mute**', color='Red')
                    emb.add_field(name='**Выдал:**', value=ctx.author.mention, inline=False)
                    emb.add_field(name='**Нарушитель:**', value=member.mention, inline=False)
                    emb.add_field(name='**ID нарушителя:**', value=member.id, inline=False)
                    emb.add_field(name='**Причина:**', value=reason, inline=False)
                    emb.add_field(name='**Длительность:**', value='{} день(ей)'.format(time), inline=False)
                    emb.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')

                    await member.add_roles(mute_role)
                    await ctx.send(embed=emb)
                    await member.send(embed=emb_user)
                    await asyncio.sleep(time * 60 * 60 * 24)
                    await member.remove_roles(mute_role)
                    await member.send(embed=emb_user_stop)