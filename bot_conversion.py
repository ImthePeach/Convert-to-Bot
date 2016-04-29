import discord
import asyncio
import aiohttp

OWNER_EMAIL = 'email'
OWNER_PASSWORD = 'password'

BOT_EMAIL = 'email'
BOT_PASSWORD = 'password'

APPLICATIONS = 'https://discordapp.com/api/oauth2/applications'

owner = discord.Client()
bot = discord.Client()

async def get_bot_name():
    global bot
    url = 'https://discordapp.com/api/users/@me'
    async with aiohttp.get(url, headers=bot.headers) as resp:
        js = await resp.json()
        bot.name = js['username']

async def create_application():
    global owner
    global bot

    headers = {
        'authorization': owner.token,
        'content-type': 'application/json'
    }

    payload = {
        'name': bot.name
    }

    print('Creating application')
    async with aiohttp.post(APPLICATIONS, headers=headers, data=discord.utils.to_json(payload)) as resp:
        data = await resp.json()
        owner.client_id = data['id']
        print('Successfully created an application.')
        print('Client ID: {0[id]}\nSecret: {0[secret]}'.format(data))

async def do_conversion():
    global owner
    global bot
    url = '{0}/{1.client_id}/bot'.format(APPLICATIONS, owner)
    headers = {
        'authorization': owner.token,
        'content-type': 'application/json'
    }

    payload = {
        'token': bot.token
    }

    print('Converting account into a bot account.')
    async with aiohttp.post(url, headers=headers, data=discord.utils.to_json(payload)) as resp:
        data = await resp.json()
        print('Bot conversion complete.')
        print(data)


loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(owner.login(OWNER_EMAIL, OWNER_PASSWORD))
    loop.run_until_complete(owner.session.close())
    loop.run_until_complete(bot.login(BOT_EMAIL, BOT_PASSWORD))
    loop.run_until_complete(bot.session.close())
except Exception as e:
    print('oops, something happened: ' + str(e))
else:
    loop.run_until_complete(get_bot_name())
    loop.run_until_complete(create_application())
    loop.run_until_complete(do_conversion())
finally:
    loop.close()