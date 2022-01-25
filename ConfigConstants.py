Token = 'ODgwMDg3MjgwNTA3ODEzOTMw.YSZLJg.g7e7-MSwduvQxL6OVNdzIeGDXWw'
filename = "database.pkl"
# img = Image.new('RGBA', (400, 200), '#232529')
# url = str(ctx.author.avatar_url)[:-10]
# response = requests.get(url, stream=True)
# response = Image.open(io.BytesIO(response.content))
# response = response.convert('RGBA')
# response = response.resize((100, 100), Image.ANTIALIAS)
# img.paste(response, (15, 15, 115, 115))
# idraw = ImageDraw.Draw(img)
# name = ctx.author.name  # Получения имени
# tag = ctx.author.discriminator  # получения тега
# headline = ImageFont.truetype('arial.ttf', size=20)
# undertext = ImageFont.truetype('arial.ttf', size=12)
# idraw.text((145, 15), f'{name}#{tag}', font=headline)
# idraw.text((145, 50), f'ID:{ctx.author.id}', font=undertext)
# idraw.text((145, 70), f'status:{ctx.author.status}', font=undertext)
# img.save('user_card.png')
# await ctx.send(file=discord.File(fp='user_card.png'))
# Фильтр чата
#@client.event
#async def on_message(message):
#    author = message.author
    # bad_word = ['блядь', 'сука', 'ебал', 'заебал', 'пошел нахуй', 'иди в задницу', 'блять', 'бля', 'иди нахуй',
    #             'пошел нахуй', 'хуй', 'охуел', 'oxyeл', 'ебал', 'oхyел', 'охyeл', 'oxуел', 'иди нaxyй', 'иди наxуй',
    #             'иди нахyй', "соси", 'иди нах', 'Иди нах', 'пошёл нахуй', 'Пошёл нахуй']
    # await client.process_commands(message)
 #   msg = message.content.lower()

  #  pf = profanity_filter.ProfanityFilter(languages=["ru", "en"])

   # print(pf.censor(msg))

    #is_dirty = pf.is_profane(msg)
    #if is_dirty:
     #   await message.delete()
      #  a = random.randint(1, 2)
       # if a == 1:
        #    await message.author.send(f'{message.author.name},Мы культурные, не матерись, иначе проникну в твой Ass')
        #elif a == 2:
         #   await message.author.send(f'{message.author.name},В следущий раз твой Ass будет в опасности')
        #else:
         #   await message.author.send(f'{message.author.name},Плохой мальчик твой Ass в опасности')
        #AddXpToUser(-10, message.author.id)


   # elif not (message.content == "" or message.content is None or message.content == "\n"):
    #    logger.log(f"Message: {message.author} - {message.content}", "on_message")
     #   if not (message.content.lower().startswith(";/")):
     #       AddXpToUser(1, message.author.id)
   # else:
    #    logger.log(f"Message: {message.author} - {message.content}", "on_message")
# Фильтр чата
#@client.event
#async def on_message(message):
  #  author = message.author
    # bad_word = ['блядь', 'сука', 'ебал', 'заебал', 'пошел нахуй', 'иди в задницу', 'блять', 'бля', 'иди нахуй',
    #             'пошел нахуй', 'хуй', 'охуел', 'oxyeл', 'ебал', 'oхyел', 'охyeл', 'oxуел', 'иди нaxyй', 'иди наxуй',
    #             'иди нахyй', "соси", 'иди нах', 'Иди нах', 'пошёл нахуй', 'Пошёл нахуй']
    # await client.process_commands(message)
    #msg = message.content.lower()

   # pf = profanity_filter.ProfanityFilter(languages=["ru", "en"])

    #rint(pf.censor(msg))

    #is_dirty = pf.is_profane(msg)
    #if is_dirty:
       # await message.delete()
       # a = random.randint(1, 2)
       # if a == 1:
        #    await message.author.send(f'{message.author.name},Мы культурные, не матерись, иначе проникну в твой Ass')
        #elif a == 2:
        #    await message.author.send(f'{message.author.name},В следущий раз твой Ass будет в опасности')
       # else:
      #      await message.author.send(f'{message.author.name},Плохой мальчик твой Ass в опасности')
     #   AddXpToUser(-10, message.author.id)


    #elif not (message.content == "" or message.content is None or message.content == "\n"):
       # logger.log(f"Message: {message.author} - {message.content}", "on_message")
      #  if not (message.content.lower().startswith(";/")):
     #       AddXpToUser(1, message.author.id)
    #else:
     #   logger.log(f"Message: {message.author} - {message.content}", "on_message")
#spacy
#git+https://github.com/kmike/pymorphy2@ca1c13f6998ae2d835bdd5033c17197dcba84cf4#egg=pymorphy2