import discord, json
from discord.ext import commands

with open('cogs/config.json', 'r') as json_file:
    config = json.load(json_file)

intents = discord.Intents.all()
client = commands.Bot(command_prefix=config["prefix"], owner_ids=config["owner_ids"], case_insensitive=True, intents=intents)
client.remove_command("help")

@client.event
async def on_ready():
    print(f"Logged in as {client.user.name}. Currently in {len(client.guilds)} guilds.")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"with {len(client.guilds)} guilds"))

@client.event
async def on_message(message):
    if message.author.bot: return
    if message.content in [f'<@!{client.user.id}>', f'<@{client.user.id}>']:
        return await message.channel.send(f'**My current prefix here is `{config["prefix"]}`**')
    await client.process_commands(message)

@client.event
async def on_command_error(ctx, error):
    if hasattr(ctx.command, 'on_error'): return
    if isinstance(error, commands.CommandNotFound): return
    await ctx.send(error)

if __name__ == '__main__':
    for extension in config["initial_extensions"]:
        try:
            client.load_extension(extension)
            extension = extension.replace('cogs.', '')
            print(f'Loaded extension \'{extension}\'.')
        except Exception as e:
            exception = f'{type(e).__name__}: {e}'
            extension = extension.replace('cogs.', '')
            print(f'Failed to load extension \'{extension}\'.\n{exception}')

client.run(config["token"])

