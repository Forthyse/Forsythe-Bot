import discord
from discord.ext import commands
import traceback
import os
from discord.ext import commands


intents = discord.Intents.all()
client = commands.Bot(command_prefix="~", case_insensitive=True, intents=intents)
client.remove_command("help")
client.load_extension('jishaku')

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="5 Guilds"))
    print(f"Currently in {len(list(client.guilds))} guilds.")

@client.event
async def on_message(message):
    if message.content in [f'<@!{client.user.id}>', f'<@{client.user.id}>']:
      await message.channel.send('**My current prefix here is** ~')
    await client.process_commands(message)



    
    
if __name__ == '__main__':
    for file in os.listdir("cogs"):
        print("found file", file)
        if file.endswith(".py"):
            print("loading", file)
            try:
                client.load_extension(f"cogs.{file[:-3]}")
            except (discord.ClientException, ModuleNotFoundError):
                print(traceback.format_exc())

client.run("TOKEN")
